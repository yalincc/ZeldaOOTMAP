package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func detectLanIP() string {
	conn, err := net.Dial("udp", "8.8.8.8:80")
	if err != nil {
		return "127.0.0.1"
	}
	defer conn.Close()
	if addr, ok := conn.LocalAddr().(*net.UDPAddr); ok {
		return addr.IP.String()
	}
	return "127.0.0.1"
}

func findAppDir(explicit string) string {
	if explicit != "" {
		if st, err := os.Stat(filepath.Join(explicit, "index.html")); err == nil && !st.IsDir() {
			return explicit
		}
	}
	var roots []string
	if wd, err := os.Getwd(); err == nil {
		roots = append(roots, wd, filepath.Join(wd, ".."), filepath.Join(wd, "..", ".."))
	}
	if exe, err := os.Executable(); err == nil {
		ed := filepath.Dir(exe)
		roots = append(roots, ed, filepath.Join(ed, ".."), filepath.Join(ed, "..", ".."))
	}
	for _, r := range roots {
		cand := filepath.Join(r, "app")
		if st, err := os.Stat(filepath.Join(cand, "index.html")); err == nil && !st.IsDir() {
			abs, _ := filepath.Abs(cand)
			return abs
		}
	}
	return ""
}

func writeCORS(w http.ResponseWriter) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "*")
	w.Header().Set("Access-Control-Allow-Private-Network", "true")
}

func startServer(tracker *Tracker, startPort int, appDir string) (int, string, error) {
	var ln net.Listener
	port := startPort
	var err error
	for p := startPort; p <= startPort+4; p++ {
		ln, err = net.Listen("tcp", fmt.Sprintf("0.0.0.0:%d", p))
		if err == nil {
			port = p
			break
		}
	}
	if ln == nil {
		return 0, "", fmt.Errorf("无法监听端口 %d~%d: %w", startPort, startPort+4, err)
	}

	lanURL := fmt.Sprintf("http://%s:%d/oot/?follow=1", detectLanIP(), port)

	mux := http.NewServeMux()
	mux.HandleFunc("/pos", func(w http.ResponseWriter, r *http.Request) {
		writeCORS(w)
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		w.Header().Set("Content-Type", "application/json; charset=utf-8")
		w.Header().Set("Cache-Control", "no-store")
		_ = json.NewEncoder(w).Encode(tracker.Snapshot(lanURL))
	})

	mux.HandleFunc("/lanUrl", func(w http.ResponseWriter, r *http.Request) {
		writeCORS(w)
		w.Header().Set("Content-Type", "application/json; charset=utf-8")
		_ = json.NewEncoder(w).Encode(map[string]string{"url": lanURL})
	})

	if appDir != "" {
		fs := http.FileServer(http.Dir(appDir))
		mux.HandleFunc("/oot", func(w http.ResponseWriter, r *http.Request) {
			http.Redirect(w, r, "/oot/", http.StatusMovedPermanently)
		})
		mux.Handle("/oot/", http.StripPrefix("/oot/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			if strings.HasSuffix(r.URL.Path, ".html") || r.URL.Path == "" || strings.HasSuffix(r.URL.Path, "/") {
				w.Header().Set("Cache-Control", "no-store")
			}
			fs.ServeHTTP(w, r)
		})))
	}

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" && r.URL.Path != "/status" {
			http.NotFound(w, r)
			return
		}
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Header().Set("Cache-Control", "no-store")
		_, _ = fmt.Fprintf(w, statusPageHTML, lanURL, lanURL)
	})

	go func() {
		if err := http.Serve(ln, mux); err != nil {
			log.Printf("[server] %v", err)
		}
	}()

	return port, lanURL, nil
}

const statusPageHTML = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OOTNavi PC · 实时定位服务</title>
<style>
  body { font-family: system-ui, -apple-system, sans-serif; background:#120d0a; color:#efe4d2; margin:0; padding:24px; }
  .card { max-width:560px; margin:0 auto; background:#1c1510; border:1px solid #3c2f23; border-radius:12px; padding:20px; }
  h2 { margin:0 0 12px; color:#f0c36d; font-size:20px; }
  .badge { display:inline-block; padding:4px 10px; border-radius:999px; font-size:13px; background:#2a2018; }
  .ok { color:#7ce38b; } .wait { color:#f0c36d; }
  pre { background:#0e0a08; padding:12px; border-radius:8px; overflow:auto; font-size:13px; line-height:1.45; }
  .row { display:flex; gap:10px; flex-wrap:wrap; margin:14px 0; align-items:center; }
  a.btn, button.btn { background:#c69749; color:#120d0a; border:none; border-radius:8px; padding:8px 14px; font-weight:600; text-decoration:none; cursor:pointer; font-size:14px; }
  input.url { flex:1; min-width:220px; background:#0e0a08; color:#efe4d2; border:1px solid #3c2f23; border-radius:8px; padding:8px 10px; font-size:13px; }
</style>
</head>
<body>
<div class="card">
  <h2>OOTNavi PC · 时之笛实时定位</h2>
  <div id="st" class="badge wait">连接中…</div>
  <div class="row">
    <a class="btn" href="/oot/?follow=1" target="_blank">打开地图（跟随模式）</a>
    <button class="btn" onclick="navigator.clipboard?.writeText(document.getElementById('lan').value)">复制手机链接</button>
  </div>
  <div class="row">
    <input id="lan" class="url" readonly value="%s">
  </div>
  <p style="font-size:12px;opacity:.75;margin:4px 0 10px">手机连接同一 WiFi 后访问上方链接：%s</p>
  <pre id="out">{}</pre>
</div>
<script>
async function poll() {
  try {
    const r = await fetch('/pos');
    const d = await r.json();
    const st = document.getElementById('st');
    if (d.ok) {
      st.className = 'badge ok';
      st.textContent = (d.scene || '未知区域') + (d.era ? ' (' + d.era + ')' : '') + ' · ' + (d.verified ? '已锁定' : '待验证');
    } else {
      st.className = 'badge wait';
      st.textContent = '等待游戏进入 3D 画面…';
    }
    document.getElementById('out').textContent = JSON.stringify(d, null, 2);
  } catch (e) {
    document.getElementById('st').textContent = '服务离线';
  }
}
poll();
setInterval(poll, 500);
</script>
</body>
</html>`
