/* ==========================================================================
 * 存档只读同步（纯本地解析 progress.sav + ootnavi-pc /save 自动同步 + GUI 面板）
 * ========================================================================== */
(function () {
  "use strict";

  var HASH_ACTOR_SET = 0xa3db7114;
  var MAGIC_SAVE = 0x01020304;
  var POLL_SAVE_MS = 5000;
  var lastAutoMtime = "";
  var toastTimer = 0;
  var syncInfo = { mode: "off", label: "尚未同步存档", timeText: "—" };

  var CAT_SUMMARY = [
    { id: "heart", label: "心之碎片" },
    { id: "skull", label: "黄金骷髅蜘蛛" },
    { id: "heartc", label: "心之容器" },
    { id: "song", label: "歌曲" },
    { id: "medal", label: "精灵石 / 勋章" },
    { id: "fairy", label: "大妖精之泉" },
    { id: "upgrade", label: "容量 / 升级" },
    { id: "keyitem", label: "关键道具" }
  ];

  function $(id) { return document.getElementById(id); }

  function showToast(msg, isErr) {
    var el = $("saveToast");
    if (!el) return;
    el.textContent = msg;
    el.classList.toggle("err", !!isErr);
    el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.hidden = true; }, 4500);
  }

  function hex8(n) {
    return (n >>> 0).toString(16).padStart(8, "0");
  }

  function hex64(lo, hi) {
    return (hi >>> 0).toString(16).padStart(8, "0") + (lo >>> 0).toString(16).padStart(8, "0");
  }

  function formatNow() {
    var d = new Date();
    return d.toTimeString().slice(0, 8);
  }

  function extractSlotName(pathStr) {
    if (!pathStr) return "progress.sav";
    var m = pathStr.match(/(slot_\d+)/i);
    return m ? m[1] : "progress.sav";
  }

  function renderModalState() {
    var pill = $("saveStatusPill");
    var tm = $("saveStatusTime");
    if (pill) {
      pill.className = "save-status-pill " + syncInfo.mode;
      var icon = syncInfo.mode === "ok" ? "🟢 " : (syncInfo.mode === "manual" ? "📁 " : "⚪ ");
      pill.textContent = icon + syncInfo.label;
    }
    if (tm) tm.textContent = syncInfo.timeText;

    var grid = $("saveCatGrid");
    if (!grid) return;
    var pins = window.OOT_PINS_DATA || [];
    var done = (window.OOT_MAP_API && window.OOT_MAP_API.getState) ? window.OOT_MAP_API.getState().donePins : {};
    var html = "";
    for (var i = 0; i < CAT_SUMMARY.length; i++) {
      var c = CAT_SUMMARY[i];
      var tot = 0;
      var got = 0;
      for (var j = 0; j < pins.length; j++) {
        if (pins[j].cat === c.id) {
          tot++;
          if (done[pins[j].id]) got++;
        }
      }
      var pct = tot > 0 ? Math.round((got / tot) * 100) : 0;
      html +=
        '<div class="save-cat-item">' +
          '<div class="save-cat-row"><span class="save-cat-name">' + c.label + '</span><span class="save-cat-num">' + got + " / " + tot + "</span></div>" +
          '<div class="save-cat-bar"><div class="save-cat-fill" style="width:' + pct + '%"></div></div>' +
        "</div>";
    }
    grid.innerHTML = html;
  }

  function openModal() {
    var modal = $("saveHelpModal");
    if (!modal) return;
    renderModalState();
    modal.hidden = false;
  }

  function parseProgressSav(buf) {
    if (!buf || buf.byteLength < 0x30) {
      throw new Error("文件过小，不是有效的 progress.sav");
    }
    var dv = new DataView(buf);
    var magic = dv.getUint32(0, true);
    if (magic !== MAGIC_SAVE) {
      throw new Error("魔数不匹配，请确认选择的是 Switch 2 版 progress.sav");
    }
    var endTable = dv.getUint32(8, true);
    if (endTable < 0x28 || endTable > buf.byteLength) {
      throw new Error("存档表结构异常");
    }

    var flags = window.OOT_SAVE_FLAGS || { actor64: {}, gd32: {} };
    var actorMap = flags.actor64 || {};
    var gdMap = flags.gd32 || {};
    var matched = {};
    var actorArrPtr = 0;

    for (var off = 0x28; off + 8 <= endTable; off += 8) {
      var h = dv.getUint32(off, true);
      var v = dv.getUint32(off + 4, true);
      if (h === HASH_ACTOR_SET) {
        actorArrPtr = v;
      }
      if (v !== 0) {
        var pids = gdMap[hex8(h)];
        if (pids) {
          for (var i = 0; i < pids.length; i++) matched[pids[i]] = true;
        }
      }
    }

    if (actorArrPtr >= endTable && actorArrPtr + 8 <= buf.byteLength) {
      var arrEnd = buf.byteLength - 8;
      for (var p = actorArrPtr; p + 8 <= arrEnd; p += 8) {
        var lo = dv.getUint32(p, true);
        var hi = dv.getUint32(p + 4, true);
        var pids64 = actorMap[hex64(lo, hi)];
        if (pids64) {
          for (var j = 0; j < pids64.length; j++) matched[pids64[j]] = true;
        }
      }
    }

    return Object.keys(matched);
  }

  function buildSummary(ids) {
    var pins = window.OOT_PINS_DATA || [];
    var byId = {};
    for (var i = 0; i < pins.length; i++) byId[pins[i].id] = pins[i];
    var counts = { heart: 0, skull: 0, heartc: 0, visited: 0 };
    var nonCollect = { boss: 1, dungeon: 1, minigame: 1, npc: 1, soil: 1, shop: 1, grotto: 1, stone: 1, warp: 1, chest: 1 };
    for (var j = 0; j < ids.length; j++) {
      var p = byId[ids[j]];
      if (!p) continue;
      if (counts.hasOwnProperty(p.cat)) counts[p.cat]++;
      if (nonCollect[p.cat]) counts.visited++;
    }
    return "心碎 " + counts.heart + "/36 · 蜘蛛 " + counts.skull + "/100 · 容器 " + counts.heartc + "/8 · 已访问/任务 " + counts.visited;
  }

  function applySyncedIds(ids, sourceLabel, silentIfEmpty) {
    var api = window.OOT_MAP_API;
    if (!api || typeof api.mergeDonePins !== "function") return;
    var res = api.mergeDonePins(ids);
    var modal = $("saveHelpModal");
    if (modal && !modal.hidden) renderModalState();
    if (silentIfEmpty && res.added === 0) return;
    showToast(
      sourceLabel + "：新增 " + res.added + " 项（存档命中 " + ids.length + " 项：" + buildSummary(ids) + "）"
    );
  }

  function handleFile(file) {
    if (!file) return;
    if (file.name && file.name.toLowerCase().indexOf(".sav") === -1) {
      showToast("请选择 progress.sav 文件", true);
      return;
    }
    var reader = new FileReader();
    reader.onload = function () {
      try {
        var ids = parseProgressSav(reader.result);
        syncInfo = { mode: "manual", label: "手动导入：" + (file.name || "progress.sav"), timeText: "同步于 " + formatNow() };
        applySyncedIds(ids, "已同步存档", false);
      } catch (err) {
        showToast(err && err.message ? err.message : "存档解析失败", true);
      }
    };
    reader.onerror = function () {
      showToast("读取文件失败", true);
    };
    reader.readAsArrayBuffer(file);
  }

  function saveEndpoint() {
    if (location.protocol.indexOf("http") === 0 && location.pathname.indexOf("/oot") === 0) {
      return "/save";
    }
    return "http://127.0.0.1:8766/save";
  }

  function pollAutoSave(force) {
    if (location.protocol === "file:") {
      if (force) showToast("当前为 file:// 离线模式，请直接选择或拖入 progress.sav", true);
      return;
    }
    fetch(saveEndpoint(), { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) return null;
        return r.json();
      })
      .then(function (d) {
        if (!d || !d.ok || !d.mtime) {
          if (force) showToast((d && d.error) || "未连接到 ootnavi-pc / 未检测到存档", true);
          return;
        }
        syncInfo = {
          mode: "ok",
          label: "ootnavi-pc 自动同步 · " + extractSlotName(d.path),
          timeText: "检测于 " + formatNow()
        };
        if (!force && d.mtime === lastAutoMtime) return;
        lastAutoMtime = d.mtime;
        var flags = window.OOT_SAVE_FLAGS || { actor64: {}, gd32: {} };
        var matched = {};
        var gd = d.gd32 || [];
        for (var i = 0; i < gd.length; i++) {
          var pids = flags.gd32[gd[i]];
          if (pids) {
            for (var a = 0; a < pids.length; a++) matched[pids[a]] = true;
          }
        }
        var a64 = d.actor64 || [];
        for (var j = 0; j < a64.length; j++) {
          var pids64 = flags.actor64[a64[j]];
          if (pids64) {
            for (var b = 0; b < pids64.length; b++) matched[pids64[b]] = true;
          }
        }
        applySyncedIds(Object.keys(matched), "自动同步存档", !force);
      })
      .catch(function () {
        if (force) showToast("未检测到运行中的 ootnavi-pc（请先运行 serve.bat）", true);
      });
  }

  function bindUI() {
    var btn = $("saveSyncBtn");
    var helpBtn = $("saveHelpBtn");
    var pickBtn = $("savePickFileBtn");
    var refreshBtn = $("saveRefreshAutoBtn");
    var inp = $("saveFileInput");
    var modal = $("saveHelpModal");
    var closeBtn = $("saveHelpClose");
    var doneBtn = $("saveHelpDoneBtn");
    var clearModalBtn = $("saveClearDoneBtn");

    if (btn) btn.addEventListener("click", openModal);
    if (helpBtn) helpBtn.addEventListener("click", openModal);
    if (pickBtn && inp) pickBtn.addEventListener("click", function () { inp.click(); });
    if (refreshBtn) refreshBtn.addEventListener("click", function () { pollAutoSave(true); });

    if (inp) {
      inp.addEventListener("change", function () {
        var f = inp.files && inp.files[0];
        if (f) handleFile(f);
        inp.value = "";
      });
    }

    // 拖拽 progress.sav 到地图或面板内拖放区
    var overlay = $("saveDropOverlay");
    var dz = $("saveModalDropZone");
    var dragDepth = 0;
    document.addEventListener("dragenter", function (e) {
      if (!e.dataTransfer || Array.prototype.indexOf.call(e.dataTransfer.types || [], "Files") === -1) return;
      dragDepth++;
      if (dz) dz.classList.add("dragover");
      if (overlay && (!modal || modal.hidden)) overlay.hidden = false;
    });
    document.addEventListener("dragleave", function () {
      dragDepth = Math.max(0, dragDepth - 1);
      if (dragDepth === 0) {
        if (dz) dz.classList.remove("dragover");
        if (overlay) overlay.hidden = true;
      }
    });
    document.addEventListener("dragover", function (e) {
      if (e.dataTransfer && Array.prototype.indexOf.call(e.dataTransfer.types || [], "Files") !== -1) {
        e.preventDefault();
      }
    });
    document.addEventListener("drop", function (e) {
      dragDepth = 0;
      if (dz) dz.classList.remove("dragover");
      if (overlay) overlay.hidden = true;
      var files = e.dataTransfer && e.dataTransfer.files;
      if (files && files.length > 0) {
        e.preventDefault();
        handleFile(files[0]);
      }
    });

    if (closeBtn && modal) closeBtn.addEventListener("click", function () { modal.hidden = true; });
    if (doneBtn && modal) doneBtn.addEventListener("click", function () { modal.hidden = true; });
    if (modal) {
      modal.addEventListener("click", function (e) {
        if (e.target === modal) modal.hidden = true;
      });
    }
    if (clearModalBtn) {
      clearModalBtn.addEventListener("click", function () {
        if (!window.confirm("确定清空所有已收集标记吗？此操作不会修改你的游戏存档文件。")) return;
        if (window.OOT_MAP_API && window.OOT_MAP_API.clearDonePins) {
          window.OOT_MAP_API.clearDonePins();
          lastAutoMtime = "";
          renderModalState();
          showToast("已清空本地收集记录");
        }
      });
    }

    pollAutoSave(false);
    setInterval(function () { pollAutoSave(false); }, POLL_SAVE_MS);
  }

  window.addEventListener("DOMContentLoaded", bindUI);
})();
