package main

import (
	"encoding/binary"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"syscall"
	"time"
	"unsafe"
)

const (
	saveMagic        = 0x01020304
	hashActorSetFlag = 0xa3db7114
)

// SaveSnapshot 为前端 /save 接口返回的轻量只读存档摘要。
type SaveSnapshot struct {
	OK      bool     `json:"ok"`
	Path    string   `json:"path,omitempty"`
	Mtime   string   `json:"mtime,omitempty"`
	GD32    []string `json:"gd32,omitempty"`
	Actor64 []string `json:"actor64,omitempty"`
	Error   string   `json:"error,omitempty"`
}

type SaveWatcher struct {
	mu           sync.Mutex
	explicitPath string
	cachedPath   string
	cachedMtime  time.Time
	cachedSnap   SaveSnapshot
}

func NewSaveWatcher(explicitPath string) *SaveWatcher {
	return &SaveWatcher{explicitPath: strings.TrimSpace(explicitPath)}
}

func findLatestProgressSav(explicit string) (string, time.Time) {
	if explicit != "" {
		if st, err := os.Stat(explicit); err == nil && !st.IsDir() {
			return explicit, st.ModTime()
		}
	}

	var patterns []string
	// 1. 若 longshot.exe / hookshot.exe 正在运行，优先从其安装目录探测
	if proc, err := findTargetProcess([]string{"longshot.exe", "hookshot.exe"}); err == nil && proc != nil {
		if exePath, err := getProcessImagePath(proc.PID); err == nil && exePath != "" {
			dir := filepath.Dir(exePath)
			patterns = append(patterns,
				filepath.Join(dir, "LongshotLauncher-data", "user", "save", "*", "slot_*", "progress.sav"),
				filepath.Join(dir, "..", "LongshotLauncher-data", "user", "save", "*", "slot_*", "progress.sav"),
				filepath.Join(dir, "user", "save", "*", "slot_*", "progress.sav"),
			)
		}
	}
	// 2. 常见默认路径兜底
	patterns = append(patterns,
		`F:\SWITCH2\Longshot\LongshotLauncher-data\user\save\*\slot_*\progress.sav`,
		`D:\SWITCH2\Longshot\LongshotLauncher-data\user\save\*\slot_*\progress.sav`,
		`C:\SWITCH2\Longshot\LongshotLauncher-data\user\save\*\slot_*\progress.sav`,
	)

	var bestPath string
	var bestTime time.Time
	seen := map[string]bool{}
	for _, pat := range patterns {
		matches, _ := filepath.Glob(pat)
		for _, m := range matches {
			if seen[m] {
				continue
			}
			seen[m] = true
			if st, err := os.Stat(m); err == nil && !st.IsDir() {
				if bestPath == "" || st.ModTime().After(bestTime) {
					bestPath = m
					bestTime = st.ModTime()
				}
			}
		}
	}
	return bestPath, bestTime
}

func getProcessImagePath(pid uint32) (string, error) {
	h, err := syscall.OpenProcess(syscall.PROCESS_QUERY_INFORMATION, false, pid)
	if err != nil {
		return "", err
	}
	defer syscall.CloseHandle(h)
	buf := make([]uint16, 1024)
	sz := uint32(len(buf))
	r1, _, e1 := procQueryFullProcessImageNameW.Call(uintptr(h), 0, uintptr(unsafe.Pointer(&buf[0])), uintptr(unsafe.Pointer(&sz)))
	if r1 == 0 {
		return "", e1
	}
	return syscall.UTF16ToString(buf[:sz]), nil
}

var procQueryFullProcessImageNameW = syscall.NewLazyDLL("kernel32.dll").NewProc("QueryFullProcessImageNameW")

func parseProgressSav(buf []byte, path string, mtime time.Time) SaveSnapshot {
	if len(buf) < 0x30 {
		return SaveSnapshot{OK: false, Error: "存档过小"}
	}
	if binary.LittleEndian.Uint32(buf[0:4]) != saveMagic {
		return SaveSnapshot{OK: false, Error: "魔数不匹配"}
	}
	endTable := int(binary.LittleEndian.Uint32(buf[8:12]))
	if endTable < 0x28 || endTable > len(buf) {
		return SaveSnapshot{OK: false, Error: "表结构异常"}
	}

	var gd32 []string
	var actorPtr int
	for off := 0x28; off+8 <= endTable; off += 8 {
		h := binary.LittleEndian.Uint32(buf[off : off+4])
		v := binary.LittleEndian.Uint32(buf[off+4 : off+8])
		if h == hashActorSetFlag {
			actorPtr = int(v)
		}
		if v != 0 {
			gd32 = append(gd32, fmt.Sprintf("%08x", h))
		}
	}

	var actor64 []string
	if actorPtr >= endTable && actorPtr+8 <= len(buf) {
		arrEnd := len(buf) - 8
		for p := actorPtr; p+8 <= arrEnd; p += 8 {
			q := binary.LittleEndian.Uint64(buf[p : p+8])
			actor64 = append(actor64, fmt.Sprintf("%016x", q))
		}
	}

	return SaveSnapshot{
		OK:      true,
		Path:    path,
		Mtime:   mtime.UTC().Format(time.RFC3339Nano),
		GD32:    gd32,
		Actor64: actor64,
	}
}

func (w *SaveWatcher) Snapshot() SaveSnapshot {
	path, mtime := findLatestProgressSav(w.explicitPath)
	if path == "" {
		return SaveSnapshot{OK: false, Error: "未检测到 progress.sav"}
	}

	w.mu.Lock()
	defer w.mu.Unlock()
	if w.cachedSnap.OK && w.cachedPath == path && w.cachedMtime.Equal(mtime) {
		return w.cachedSnap
	}
	buf, err := readFileShared(path)
	if err != nil {
		return SaveSnapshot{OK: false, Path: path, Error: err.Error()}
	}
	snap := parseProgressSav(buf, path, mtime)
	if snap.OK {
		w.cachedPath = path
		w.cachedMtime = mtime
		w.cachedSnap = snap
	}
	return snap
}
