package main

import (
	"fmt"
	"log"
	"math"
	"sync"
	"syscall"
	"time"
)

type PosSnapshot struct {
	OK        bool    `json:"ok"`
	GX        float64 `json:"gx"`
	GY        float64 `json:"gy"`
	GZ        float64 `json:"gz"`
	X         float64 `json:"x"`
	Y         float64 `json:"y"`
	Facing    float64 `json:"facing"`
	CamFacing float64 `json:"camFacing"`
	Scene     string  `json:"scene"`
	Era       string  `json:"era"`
	Verified  bool    `json:"verified"`
	Source    string  `json:"source"`
	Updated   float64 `json:"updated"`
	App       string  `json:"app"`
	LanURL    string  `json:"lanUrl,omitempty"`
}

type vec3 struct {
	x, y, z float64
}

type Tracker struct {
	mu          sync.RWMutex
	h           syscall.Handle
	proc        *procInfo
	guestBase   uintptr
	chains      []staticChainSpec
	debug       bool
	lastScene   string
	lastEra     string
	snap        PosSnapshot
	hist        []vec3
	pingPongCnt int
	missCnt     int
	lastL1Try   time.Time
}

func NewTracker(debug bool) *Tracker {
	return &Tracker{
		guestBase: defaultGuestBase,
		debug:     debug,
		snap: PosSnapshot{
			App: "ootnavi",
		},
	}
}

func (t *Tracker) Close() {
	t.mu.Lock()
	defer t.mu.Unlock()
	if t.h != 0 {
		closeHandle(t.h)
		t.h = 0
	}
}

func (t *Tracker) Snapshot(lanURL string) PosSnapshot {
	t.mu.RLock()
	defer t.mu.RUnlock()
	s := t.snap
	if s.OK && float64(time.Now().UnixNano())/1e9-s.Updated > 5.0 {
		s.OK = false
	}
	s.LanURL = lanURL
	return s
}

func (t *Tracker) ensureAttached() bool {
	if t.h != 0 && processAlive(t.h) {
		return true
	}
	if t.h != 0 {
		log.Println("[ootnavi] 游戏进程已退出，释放句柄并等待重启...")
		closeHandle(t.h)
		t.h = 0
		t.proc = nil
		t.chains = nil
		t.hist = nil
		t.snap.OK = false
		t.snap.Verified = false
		t.snap.Source = "waiting"
	}

	pi, err := findTargetProcess([]string{"longshot.exe", "hookshot.exe"})
	if err != nil {
		return false
	}
	h, err := openProcessRead(pi.PID)
	if err != nil {
		if t.debug {
			log.Printf("[debug] %v", err)
		}
		return false
	}
	t.h = h
	t.proc = pi
	log.Printf("[ootnavi] 已附加 %s (pid=%d, size=%.1fMB)", pi.Name, pi.PID, float64(pi.ExeSize)/1024/1024)

	// Load L0: cached chains (if exeSize matches) + builtin Longshot chains
	var chains []staticChainSpec
	if cached := loadChainCache(pi.ExeSize); len(cached) > 0 {
		chains = append(chains, cached...)
	}
	chains = append(chains, builtinLongshotChains...)
	t.chains = chains
	return true
}

func dist3(a, b vec3) float64 {
	dx, dy, dz := a.x-b.x, a.y-b.y, a.z-b.z
	return math.Sqrt(dx*dx + dy*dy + dz*dz)
}

func round3(v float64) float64 {
	return math.Round(v*1000) / 1000
}

func (t *Tracker) Tick() {
	t.mu.Lock()
	defer t.mu.Unlock()

	if !t.ensureAttached() {
		return
	}

	type hit struct {
		chain     staticChainSpec
		pos       vec3
		facing    float64
		camFacing float64
		hasCam    bool
		scene     string
		era       string
	}

	var hits []hit
	for _, c := range t.chains {
		x, y, z, facing, camFacing, hasCam, scene, era, ok := readChainSample(t.h, t.guestBase, c)
		if ok {
			hits = append(hits, hit{
				chain:     c,
				pos:       vec3{float64(x), float64(y), float64(z)},
				facing:    facing,
				camFacing: camFacing,
				hasCam:    hasCam,
				scene:     scene,
				era:       era,
			})
		}
	}

	// If no builtin/cached chain hit, try L1 discovery at most once every 3s
	if len(hits) == 0 {
		t.missCnt++
		if t.missCnt >= 3 {
			t.snap.OK = false // hold last coords for up to 3 misses, then mark !OK
		}
		if time.Since(t.lastL1Try) > 3*time.Second && t.proc != nil {
			t.lastL1Try = time.Now()
			if ax, ay, az, _, aok := readLatestSaveAnchor(t.proc.ExePath); aok {
				if discovered := discoverStaticChainsL1(t.h, t.guestBase, ax, ay, az); len(discovered) > 0 {
					log.Printf("[ootnavi] L1 发现 %d 条静态链，已缓存", len(discovered))
					t.chains = append(discovered, builtinLongshotChains...)
					saveChainCache(t.proc.ExeSize, discovered)
				}
			}
		}
		return
	}
	t.missCnt = 0

	// Pick primary hit (first valid, preferring one with scene/rot)
	best := hits[0]
	agreeCount := 0
	var scene, era string
	var facing, camFacing float64
	hasFacing := false
	hasCam := false
	for _, h := range hits {
		if dist3(h.pos, best.pos) < 1.0 {
			agreeCount++
		}
		if scene == "" && h.scene != "" {
			scene = h.scene
		}
		if era == "" && h.era != "" {
			era = h.era
		}
		if !hasFacing && h.chain.RotOffset != 0 {
			facing = h.facing
			hasFacing = true
		}
		if !hasCam && h.hasCam {
			camFacing = h.camFacing
			hasCam = true
		}
	}
	if !hasCam {
		camFacing = facing
	}

	if scene != "" {
		t.lastScene = scene
	}
	if era != "" {
		t.lastEra = era
	}

	// Ping-pong oscillation self-healing
	t.hist = append(t.hist, best.pos)
	if len(t.hist) > 32 {
		t.hist = t.hist[1:]
	}
	if len(t.hist) >= 3 {
		p0 := t.hist[len(t.hist)-1]
		p1 := t.hist[len(t.hist)-2]
		p2 := t.hist[len(t.hist)-3]
		if dist3(p0, p1) >= 50.0 && dist3(p0, p2) < 10.0 {
			t.pingPongCnt++
			if t.pingPongCnt >= 2 {
				log.Println("[ootnavi] 检测到乒乓振荡，重置历史并重新校验")
				t.hist = nil
				t.pingPongCnt = 0
				t.snap.Verified = false
				return
			}
		} else {
			t.pingPongCnt = 0
		}
	}

	verified := t.snap.Verified
	if !verified {
		if agreeCount >= 2 {
			verified = true
		} else if len(t.hist) >= 2 && dist3(t.hist[0], best.pos) > 1.0 {
			verified = true
		}
	}

	now := float64(time.Now().UnixNano()) / 1e9
	t.snap = PosSnapshot{
		OK:        true,
		GX:        round3(best.pos.x),
		GY:        round3(best.pos.y),
		GZ:        round3(best.pos.z),
		X:         round3(best.pos.x),
		Y:         round3(best.pos.z),
		Facing:    math.Round(facing*10) / 10,
		CamFacing: math.Round(camFacing*10) / 10,
		Scene:     t.lastScene,
		Era:       t.lastEra,
		Verified:  verified,
		Source:    fmt.Sprintf("%s (%d/%d)", best.chain.Name, agreeCount, len(t.chains)),
		Updated:   math.Round(now*100) / 100,
		App:       "ootnavi",
	}
}
