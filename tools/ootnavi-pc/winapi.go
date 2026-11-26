package main

import (
	"encoding/binary"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"strings"
	"syscall"
	"unsafe"
)

var (
	kernel32               = syscall.NewLazyDLL("kernel32.dll")
	procOpenProcess        = kernel32.NewProc("OpenProcess")
	procCloseHandle        = kernel32.NewProc("CloseHandle")
	procReadProcessMemory  = kernel32.NewProc("ReadProcessMemory")
	procVirtualQueryEx     = kernel32.NewProc("VirtualQueryEx")
	procGetExitCodeProcess = kernel32.NewProc("GetExitCodeProcess")

	psapi                   = syscall.NewLazyDLL("psapi.dll")
	procGetProcessMemoryInfo = psapi.NewProc("GetProcessMemoryInfo")
	procGetModuleFileNameExW = psapi.NewProc("GetModuleFileNameExW")

	procCreateToolhelp32Snapshot = kernel32.NewProc("CreateToolhelp32Snapshot")
	procProcess32FirstW          = kernel32.NewProc("Process32FirstW")
	procProcess32NextW           = kernel32.NewProc("Process32NextW")
)

const (
	processQueryInformation = 0x0400
	processVMRead           = 0x0010
	memCommit               = 0x1000
	stillActive             = 259
	th32csSnapProcess       = 0x00000002
)

type processEntry32W struct {
	Size              uint32
	CntUsage          uint32
	ProcessID         uint32
	DefaultHeapID     uintptr
	ModuleID          uint32
	CntThreads        uint32
	ParentProcessID   uint32
	PriClassBase      int32
	Flags             uint32
	ExeFile           [260]uint16
}

type processMemoryCounters struct {
	CB                         uint32
	PageFaultCount             uint32
	PeakWorkingSetSize         uintptr
	WorkingSetSize             uintptr
	QuotaPeakPagedPoolUsage    uintptr
	QuotaPagedPoolUsage        uintptr
	QuotaPeakNonPagedPoolUsage uintptr
	QuotaNonPagedPoolUsage     uintptr
	PagefileUsage              uintptr
	PeakPagefileUsage          uintptr
}

type memoryBasicInformation struct {
	BaseAddress       uintptr
	AllocationBase    uintptr
	AllocationProtect uint32
	PartitionId       uint16
	RegionSize        uintptr
	State             uint32
	Protect           uint32
	Type              uint32
}

type procInfo struct {
	PID        uint32
	Name       string
	ExePath    string
	ExeSize    int64
	WorkingSet uintptr
}

func findTargetProcess(names []string) (*procInfo, error) {
	snap, _, err := procCreateToolhelp32Snapshot.Call(th32csSnapProcess, 0)
	if snap == uintptr(syscall.InvalidHandle) {
		return nil, fmt.Errorf("CreateToolhelp32Snapshot: %w", err)
	}
	defer procCloseHandle.Call(snap)

	var pe processEntry32W
	pe.Size = uint32(unsafe.Sizeof(pe))
	r, _, _ := procProcess32FirstW.Call(snap, uintptr(unsafe.Pointer(&pe)))
	if r == 0 {
		return nil, fmt.Errorf("no processes")
	}

	var best *procInfo
	for {
		exeName := syscall.UTF16ToString(pe.ExeFile[:])
		matched := false
		for _, target := range names {
			if strings.EqualFold(exeName, target) {
				matched = true
				break
			}
		}
		if matched {
			h, _, _ := procOpenProcess.Call(processQueryInformation|processVMRead, 0, uintptr(pe.ProcessID))
			if h != 0 {
				var pmc processMemoryCounters
				pmc.CB = uint32(unsafe.Sizeof(pmc))
				procGetProcessMemoryInfo.Call(h, uintptr(unsafe.Pointer(&pmc)), uintptr(pmc.CB))

				var pathBuf [520]uint16
				n, _, _ := procGetModuleFileNameExW.Call(h, 0, uintptr(unsafe.Pointer(&pathBuf[0])), uintptr(len(pathBuf)))
				exePath := ""
				var exeSize int64
				if n > 0 {
					exePath = syscall.UTF16ToString(pathBuf[:n])
					if st, err := os.Stat(exePath); err == nil {
						exeSize = st.Size()
					}
				}
				procCloseHandle.Call(h)

				if best == nil || pmc.WorkingSetSize > best.WorkingSet {
					best = &procInfo{
						PID:        pe.ProcessID,
						Name:       exeName,
						ExePath:    exePath,
						ExeSize:    exeSize,
						WorkingSet: pmc.WorkingSetSize,
					}
				}
			}
		}
		pe.Size = uint32(unsafe.Sizeof(pe))
		r, _, _ := procProcess32NextW.Call(snap, uintptr(unsafe.Pointer(&pe)))
		if r == 0 {
			break
		}
	}
	if best == nil {
		return nil, fmt.Errorf("未找到游戏进程 (%s)", strings.Join(names, "/"))
	}
	return best, nil
}

func openProcessRead(pid uint32) (syscall.Handle, error) {
	h, _, err := procOpenProcess.Call(processQueryInformation|processVMRead, 0, uintptr(pid))
	if h == 0 {
		return 0, fmt.Errorf("OpenProcess(pid=%d): %w", pid, err)
	}
	return syscall.Handle(h), nil
}

func closeHandle(h syscall.Handle) {
	if h != 0 {
		procCloseHandle.Call(uintptr(h))
	}
}

func processAlive(h syscall.Handle) bool {
	if h == 0 {
		return false
	}
	var code uint32
	r, _, _ := procGetExitCodeProcess.Call(uintptr(h), uintptr(unsafe.Pointer(&code)))
	return r != 0 && code == stillActive
}

func readMem(h syscall.Handle, addr uintptr, buf []byte) bool {
	if h == 0 || len(buf) == 0 {
		return false
	}
	var read uintptr
	r, _, _ := procReadProcessMemory.Call(
		uintptr(h),
		addr,
		uintptr(unsafe.Pointer(&buf[0])),
		uintptr(len(buf)),
		uintptr(unsafe.Pointer(&read)),
	)
	return r != 0 && read == uintptr(len(buf))
}

func readU64(h syscall.Handle, addr uintptr) (uint64, bool) {
	var b [8]byte
	if !readMem(h, addr, b[:]) {
		return 0, false
	}
	return binary.LittleEndian.Uint64(b[:]), true
}

func readF32Vec3(h syscall.Handle, addr uintptr) (float32, float32, float32, bool) {
	var b [12]byte
	if !readMem(h, addr, b[:]) {
		return 0, 0, 0, false
	}
	x := math.Float32frombits(binary.LittleEndian.Uint32(b[0:4]))
	y := math.Float32frombits(binary.LittleEndian.Uint32(b[4:8]))
	z := math.Float32frombits(binary.LittleEndian.Uint32(b[8:12]))
	return x, y, z, true
}

func readF32Mat3(h syscall.Handle, addr uintptr) ([9]float32, bool) {
	var b [36]byte
	var m [9]float32
	if !readMem(h, addr, b[:]) {
		return m, false
	}
	for i := 0; i < 9; i++ {
		m[i] = math.Float32frombits(binary.LittleEndian.Uint32(b[i*4 : i*4+4]))
	}
	return m, true
}

func readCString(h syscall.Handle, addr uintptr, maxLen int) string {
	buf := make([]byte, maxLen)
	var read uintptr
	r, _, _ := procReadProcessMemory.Call(
		uintptr(h),
		addr,
		uintptr(unsafe.Pointer(&buf[0])),
		uintptr(len(buf)),
		uintptr(unsafe.Pointer(&read)),
	)
	if r == 0 || read == 0 {
		return ""
	}
	buf = buf[:read]
	for i, c := range buf {
		if c == 0 {
			return string(buf[:i])
		}
		if c < 0x20 || c > 0x7E {
			return ""
		}
	}
	return string(buf)
}

// readFileShared uses FILE_SHARE_READ|WRITE|DELETE so reading caption.sav never blocks game atomic saves (Error 5).
func readFileShared(path string) ([]byte, error) {
	p16, err := syscall.UTF16PtrFromString(filepath.Clean(path))
	if err != nil {
		return nil, err
	}
	h, err := syscall.CreateFile(
		p16,
		syscall.GENERIC_READ,
		syscall.FILE_SHARE_READ|syscall.FILE_SHARE_WRITE|syscall.FILE_SHARE_DELETE,
		nil,
		syscall.OPEN_EXISTING,
		syscall.FILE_ATTRIBUTE_NORMAL,
		0,
	)
	if err != nil {
		return nil, err
	}
	defer syscall.CloseHandle(h)

	var fi syscall.ByHandleFileInformation
	if err := syscall.GetFileInformationByHandle(h, &fi); err != nil {
		return nil, err
	}
	size := int(fi.FileSizeLow)
	if size <= 0 || size > 10*1024*1024 {
		return nil, fmt.Errorf("unexpected file size: %d", size)
	}
	buf := make([]byte, size)
	var done uint32
	if err := syscall.ReadFile(h, buf, &done, nil); err != nil {
		return nil, err
	}
	return buf[:done], nil
}
