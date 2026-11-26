package main

import (
	"encoding/binary"
	"encoding/json"
	"math"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"syscall"
)

const (
	defaultGuestBase uintptr = 0x100000000000
	guestHeapLo      uint64  = 0x1000000000
	guestHeapHi      uint64  = 0x1200000000
)

type staticChainSpec struct {
	Name        string `json:"name"`
	PtrGuestVA  uint64 `json:"ptrGuestVA"`
	PosOffset   uint64 `json:"posOffset"`
	RotOffset   uint64 `json:"rotOffset,omitempty"`   // 3x3 float32 matrix
	CamOffset   uint64 `json:"camOffset,omitempty"`   // camera eye [3]float32
	SceneOffset uint64 `json:"sceneOffset,omitempty"` // null-terminated scene name
	EraOffset   uint64 `json:"eraOffset,omitempty"`   // e.g. "ZoraRiver_Child"
}

type chainCache struct {
	ExeSize int64             `json:"exeSize"`
	Chains  []staticChainSpec `json:"chains"`
}

// builtinLongshotChains verified on Longshot v3.2.0 (2026-11-26).
var builtinLongshotChains = []staticChainSpec{
	{
		Name:        "primary-0x84E8CA78",
		PtrGuestVA:  0x84E8CA78,
		PosOffset:   0x138,
		RotOffset:   0x158,
		CamOffset:   0x17C,
		SceneOffset: 0xF7C,
	},
	{
		Name:       "backup-0x84E41108",
		PtrGuestVA: 0x84E41108,
		PosOffset:  0xAC,
		EraOffset:  0xCC4,
	},
	{
		Name:       "backup-0x84DF4DA8",
		PtrGuestVA: 0x84DF4DA8,
		PosOffset:  0x7C,
	},
	{
		Name:       "backup-0x84E63B60",
		PtrGuestVA: 0x84E63B60,
		PosOffset:  0xEC,
	},
	{
		Name:       "backup-0x84E9CFA0",
		PtrGuestVA: 0x84E9CFA0,
		PosOffset:  0xE0,
	},
}

func validCoord(x, y, z float32) bool {
	if math.IsNaN(float64(x)) || math.IsNaN(float64(y)) || math.IsNaN(float64(z)) {
		return false
	}
	if math.IsInf(float64(x), 0) || math.IsInf(float64(y), 0) || math.IsInf(float64(z), 0) {
		return false
	}
	if x < -5000 || x > 5000 || y < -2000 || y > 5000 || z < -5000 || z > 5000 {
		return false
	}
	// Reject origin-zeroed slots
	if math.Abs(float64(x)) < 0.001 && math.Abs(float64(y)) < 0.001 && math.Abs(float64(z)) < 0.001 {
		return false
	}
	return true
}

func readChainSample(h syscall.Handle, guestBase uintptr, c staticChainSpec) (x, y, z float32, facing float64, camFacing float64, hasCam bool, scene string, era string, ok bool) {
	ptr, pok := readU64(h, guestBase+uintptr(c.PtrGuestVA))
	if !pok || ptr < guestHeapLo || ptr >= guestHeapHi || (ptr&3) != 0 {
		return 0, 0, 0, 0, 0, false, "", "", false
	}
	objBase := guestBase + uintptr(ptr)
	x, y, z, cok := readF32Vec3(h, objBase+uintptr(c.PosOffset))
	if !cok || !validCoord(x, y, z) {
		return 0, 0, 0, 0, 0, false, "", "", false
	}

	if c.RotOffset != 0 {
		if m, mok := readF32Mat3(h, objBase+uintptr(c.RotOffset)); mok {
			// Forward vector is 3rd column: (m[2], m[5], m[8]).
			// Map north = -Z, east = +X -> heading 0 = North, 90 = East.
			fx := float64(m[2])
			fz := float64(m[8])
			if fx*fx+fz*fz > 0.01 {
				deg := math.Atan2(fx, -fz) * 180.0 / math.Pi
				if deg < 0 {
					deg += 360.0
				}
				facing = deg
			}
		}
	}

	if c.CamOffset != 0 {
		if cx, _, cz, camOk := readF32Vec3(h, objBase+uintptr(c.CamOffset)); camOk && validCoord(cx, 100, cz) {
			dx := float64(x - cx)
			dz := float64(z - cz)
			if dx*dx+dz*dz > 0.04 {
				cdeg := math.Atan2(dx, -dz) * 180.0 / math.Pi
				if cdeg < 0 {
					cdeg += 360.0
				}
				camFacing = cdeg
				hasCam = true
			}
		}
	}

	if c.SceneOffset != 0 {
		s := readCString(h, objBase+uintptr(c.SceneOffset), 64)
		if isCleanSceneName(s) {
			scene = s
		}
	}

	if c.EraOffset != 0 {
		s := readCString(h, objBase+uintptr(c.EraOffset), 64)
		if strings.HasSuffix(s, "_Child") {
			era = "child"
			if scene == "" {
				scene = strings.TrimSuffix(s, "_Child")
			}
		} else if strings.HasSuffix(s, "_Adult") {
			era = "adult"
			if scene == "" {
				scene = strings.TrimSuffix(s, "_Adult")
			}
		}
	}

	return x, y, z, facing, camFacing, hasCam, scene, era, true
}

func isCleanSceneName(s string) bool {
	if len(s) < 3 || len(s) > 48 {
		return false
	}
	for i := 0; i < len(s); i++ {
		c := s[i]
		if !((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '_') {
			return false
		}
	}
	return true
}

func chainCachePath() string {
	exe, err := os.Executable()
	if err != nil {
		return "ootnavi-pc-chain.json"
	}
	return filepath.Join(filepath.Dir(exe), "ootnavi-pc-chain.json")
}

func loadChainCache(exeSize int64) []staticChainSpec {
	data, err := os.ReadFile(chainCachePath())
	if err != nil {
		return nil
	}
	var c chainCache
	if err := json.Unmarshal(data, &c); err != nil {
		return nil
	}
	if exeSize > 0 && c.ExeSize != exeSize {
		return nil
	}
	return c.Chains
}

func saveChainCache(exeSize int64, chains []staticChainSpec) {
	if len(chains) == 0 {
		return
	}
	b, err := json.MarshalIndent(chainCache{ExeSize: exeSize, Chains: chains}, "", "  ")
	if err != nil {
		return
	}
	_ = os.WriteFile(chainCachePath(), b, 0644)
}

// readLatestSaveAnchor reads (x, y, z) @0x2A0 from newest caption.sav near the game exe.
func readLatestSaveAnchor(exePath string) (x, y, z float32, scene string, ok bool) {
	if exePath == "" {
		return 0, 0, 0, "", false
	}
	// Longshot: .../builds/stable/v3.2.0/bin/longshot.exe -> .../LongshotLauncher-data/user/save*/*/slot_*/caption.sav
	// Hookshot: .../hookshot.exe -> .../user/save*/*/slot_*/caption.sav
	dir := filepath.Dir(exePath)
	var candidates []string
	for up := 0; up < 5; up++ {
		for _, sub := range []string{"user/save", "user/save-work"} {
			pattern := filepath.Join(dir, sub, "*", "slot_*", "caption.sav")
			if matches, err := filepath.Glob(pattern); err == nil {
				candidates = append(candidates, matches...)
			}
		}
		dir = filepath.Dir(dir)
	}
	if len(candidates) == 0 {
		return 0, 0, 0, "", false
	}

	type sf struct {
		path  string
		mtime int64
	}
	var files []sf
	for _, p := range candidates {
		if st, err := os.Stat(p); err == nil {
			files = append(files, sf{p, st.ModTime().UnixNano()})
		}
	}
	sort.Slice(files, func(i, j int) bool { return files[i].mtime > files[j].mtime })

	for _, f := range files {
		data, err := readFileShared(f.path)
		if err != nil || len(data) < 0x2AC {
			continue
		}
		ax := math.Float32frombits(binary.LittleEndian.Uint32(data[0x2A0:0x2A4]))
		ay := math.Float32frombits(binary.LittleEndian.Uint32(data[0x2A4:0x2A8]))
		az := math.Float32frombits(binary.LittleEndian.Uint32(data[0x2A8:0x2AC]))
		if validCoord(ax, ay, az) {
			return ax, ay, az, "", true
		}
	}
	return 0, 0, 0, "", false
}

// discoverStaticChainsL1 scans the static .bss/.data region (0x84D00000..0x85000000)
// for 1-hop pointers whose structs contain coordinates within 15m of the save anchor.
func discoverStaticChainsL1(h syscall.Handle, guestBase uintptr, ax, ay, az float32) []staticChainSpec {
	const bssStart uint64 = 0x84D00000
	const bssSize = 0x300000 // 3MB
	buf := make([]byte, bssSize)
	if !readMem(h, guestBase+uintptr(bssStart), buf) {
		return nil
	}

	var found []staticChainSpec
	seenTarget := make(map[uint64]bool)
	obj := make([]byte, 0x200)

	for off := 0; off+8 <= len(buf); off += 8 {
		ptr := binary.LittleEndian.Uint64(buf[off : off+8])
		if ptr < guestHeapLo || ptr >= guestHeapHi || (ptr&3) != 0 {
			continue
		}
		if seenTarget[ptr] {
			continue
		}
		seenTarget[ptr] = true
		if !readMem(h, guestBase+uintptr(ptr), obj) {
			continue
		}
		for posOff := 0; posOff+12 <= len(obj); posOff += 4 {
			x := math.Float32frombits(binary.LittleEndian.Uint32(obj[posOff : posOff+4]))
			y := math.Float32frombits(binary.LittleEndian.Uint32(obj[posOff+4 : posOff+8]))
			z := math.Float32frombits(binary.LittleEndian.Uint32(obj[posOff+8 : posOff+12]))
			dx, dy, dz := float64(x-ax), float64(y-ay), float64(z-az)
			if dx*dx+dy*dy+dz*dz < 15.0*15.0 && validCoord(x, y, z) {
				found = append(found, staticChainSpec{
					Name:       "l1-discovered",
					PtrGuestVA: bssStart + uint64(off),
					PosOffset:  uint64(posOff),
				})
				if len(found) >= 6 {
					return found
				}
				break
			}
		}
	}
	return found
}
