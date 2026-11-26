package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"time"
)

func openBrowser(url string) {
	_ = exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
}

func main() {
	watch := flag.Bool("watch", false, "命令行实时打印坐标")
	port := flag.Int("port", 8766, "HTTP 起始端口")
	noOpen := flag.Bool("no-open", false, "启动时不自动打开浏览器")
	appDirFlag := flag.String("app-dir", "", "指定 app/ 静态目录路径")
	saveFlag := flag.String("save", "", "指定 progress.sav 路径（留空则自动探测最新槽位）")
	debug := flag.Bool("debug", false, "打印调试日志")
	flag.Parse()

	tracker := NewTracker(*debug)
	defer tracker.Close()
	saveWatcher := NewSaveWatcher(*saveFlag)

	if *watch {
		fmt.Println("=== OOTNavi PC 实时坐标监视 (5Hz, Ctrl+C 退出) ===")
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, os.Interrupt, syscall.SIGTERM)
		tk := time.NewTicker(50 * time.Millisecond)
		defer tk.Stop()
		for {
			select {
			case <-sig:
				return
			case <-tk.C:
				tracker.Tick()
				s := tracker.Snapshot("")
				if s.OK {
					fmt.Printf("\r(%8.3f, %8.3f, %8.3f)  facing=%5.1f°  scene=%-18s era=%-5s verified=%v   ",
						s.GX, s.GY, s.GZ, s.Facing, s.Scene, s.Era, s.Verified)
				} else {
					fmt.Printf("\r等待 longshot.exe / 3D 画面…                                                      ")
				}
			}
		}
	}

	appDir := findAppDir(*appDirFlag)
	if appDir == "" {
		log.Println("[ootnavi] 警告：未找到 app/ 目录，/oot/ 静态托管不可用（仅提供 /pos）")
	} else {
		log.Printf("[ootnavi] 托管静态目录: %s", appDir)
	}

	actualPort, lanURL, err := startServer(tracker, saveWatcher, *port, appDir)
	if err != nil {
		log.Fatalf("[ootnavi] %v", err)
	}

	log.Printf("[ootnavi] 服务已启动:")
	log.Printf("  状态页:   http://127.0.0.1:%d/", actualPort)
	log.Printf("  本地地图: http://127.0.0.1:%d/oot/?follow=1", actualPort)
	log.Printf("  手机同源: %s", lanURL)
	log.Printf("  坐标接口: http://127.0.0.1:%d/pos (app=ootnavi)", actualPort)

	if !*noOpen {
		if appDir != "" {
			openBrowser(fmt.Sprintf("http://127.0.0.1:%d/oot/?follow=1", actualPort))
		} else {
			openBrowser(fmt.Sprintf("http://127.0.0.1:%d/", actualPort))
		}
	}

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt, syscall.SIGTERM)
	tk := time.NewTicker(50 * time.Millisecond)
	defer tk.Stop()
	for {
		select {
		case <-sig:
			log.Println("[ootnavi] 正在退出...")
			return
		case <-tk.C:
			tracker.Tick()
		}
	}
}
