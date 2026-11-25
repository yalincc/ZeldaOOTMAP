/* ==========================================================================
   The Legend of Zelda: Ocarina of Time Topological Mindmap Engine
   思维导图出入口拓扑与连接网络交互引擎
   ========================================================================== */

(function () {
  "use strict";

  // 版本号单一真源：页脚徽章由此渲染，不在 index.html 另写一处
  var APP_VERSION = "0.1.0";

  var TOPOLOGY = window.OOT_TOPOLOGY;
  var NODES = TOPOLOGY.nodes;
  var EDGES = TOPOLOGY.edges;
  var DATA_CATS = window.OOT_CATEGORIES || [];
  var CAT_TREE = window.OOT_CAT_TREE || { groups: [] };
  var CATS = (function () {
    var out = [];
    var byId = {};
    (CAT_TREE.groups || []).forEach(function (g) {
      (g.cats || []).forEach(function (c) {
        var cat = {
          id: c.id,
          zh: c.zh || c.id,
          short: c.short || c.zh || c.id,
          en: c.en || c.zh || c.id,
          badge: c.badge || "#d9b45a",
          group: g.id,
          icon: c.icon || null,
          iconDone: c.iconDone || null,
          defOff: !!c.defOff
        };
        out.push(cat);
        byId[cat.id] = cat;
      });
    });
    // 数据里存在、树里没写的分类兜底收进「其他」，避免点位变不可见
    DATA_CATS.forEach(function (dc) {
      var hit = byId[dc.id];
      if (hit) {
        if (dc.badge) hit.badge = dc.badge;
        if (dc.zh && !hit.zh) hit.zh = dc.zh;
        if (dc.en && !hit.en) hit.en = dc.en;
        return;
      }
      var cat = { id: dc.id, zh: dc.zh || dc.id, short: dc.zh || dc.id, en: dc.en || dc.id, badge: dc.badge || "#d9b45a", group: "other", icon: null };
      out.push(cat);
      byId[cat.id] = cat;
    });
    return out;
  })();
  var GROUPS = (CAT_TREE.groups && CAT_TREE.groups.length) ? CAT_TREE.groups.slice() : [{ id: "other", zh: "分类", en: "Categories" }];
  if (CATS.some(function (c) { return c.group === "other"; }) && !GROUPS.some(function (g) { return g.id === "other"; })) {
    GROUPS.push({ id: "other", zh: "其他", en: "Other" });
  }
  var PINS = window.OOT_PINS_DATA || [];
  var REGIONS = (window.OOT_REGIONS && window.OOT_REGIONS.areas) || [];
  var ICONS = window.OOT_ICONS;

  var KEY_DONE = "oot_map_done_pins_v3";
  var KEY_LANG = "oot_map_lang";
  var KEY_ERA = "oot_map_era";
  var KEY_HIDE_DONE = "oot_map_hide_done";
  var KEY_AUTO_LEVEL = "oot_map_auto_level";
  var KEY_CUSTOM_COORDS = "oot_map_custom_coords_v2";
  var KEY_VIEW = "oot_map_view";
  var KEY_AREA = "oot_map_area";

  // 计算 object-fit: contain 下底图在卡片内的实际渲染矩形
  function getNodeImageRect(node, imgEl) {
    var iw = (imgEl && imgEl.naturalWidth) || node.imgW || node.w;
    var ih = (imgEl && imgEl.naturalHeight) || node.imgH || node.h;
    var scale = Math.min(node.w / iw, node.h / ih);
    var rw = iw * scale;
    var rh = ih * scale;
    return {
      ox: (node.w - rw) / 2,
      oy: (node.h - rh) / 2,
      rw: rw,
      rh: rh
    };
  }

  function applyOverlayRect(el, rect) {
    if (!el || !rect) return;
    el.style.left = rect.ox + "px";
    el.style.top = rect.oy + "px";
    el.style.width = rect.rw + "px";
    el.style.height = rect.rh + "px";
  }

  // 状态管理
  var state = {
    mode: "region", // region | topology | world
    era: "Child", // Child | Adult | All
    lang: "zh",   // 默认简体中文，支持一键切 EN
    hideDone: false,
    autoLevel: true,
    activeCats: new Set(CATS.map(function (c) { return c.id; })),
    donePins: {},
    selectedPinId: null,

    // 区域模式
    area: "KokiriForest",
    floor: "All",
    regionZoom: 1,
    regionTx: 0,
    regionTy: 0,
    regionDragging: false,
    regionDragMoved: false,
    regionDragStartX: 0,
    regionDragStartY: 0,
    regionCamStartX: 0,
    regionCamStartY: 0,

    // 全图层
    worldZoom: 1,
    worldTx: 0,
    worldTy: 0,
    worldDragging: false,
    worldDragMoved: false,
    worldDragStartX: 0,
    worldDragStartY: 0,
    worldCamStartX: 0,
    worldCamStartY: 0,

    // 三层缩放换层
    levelTimer: null,
    levelLockUntil: 0,
    levelFrom: "",
    levelFocusX: undefined,
    levelFocusY: undefined,

    // 画布与相机
    zoom: 1,
    minZoom: 0.14,
    maxZoom: 2.6,
    tx: 0,
    ty: 0,
    isDragging: false,
    dragMoved: false,
    dragStartX: 0,
    dragStartY: 0,
    camStartX: 0,
    camStartY: 0,

    // 拓扑平移原点偏移
    originOffsetX: 0,
    originOffsetY: 0,
    boardW: 0,
    boardH: 0
  };

  // 点位校准微调状态
  var calState = {
    active: false,
    draggingPin: null,
    targetBox: null
  };

  function toggleCalibrationMode() {
    calState.active = !calState.active;
    document.body.classList.toggle("cal-mode", calState.active);
    var btn = $("btnEditMode");
    if (btn) btn.classList.toggle("on", calState.active);
    var toast = $("calibrationToast");
    if (toast) toast.hidden = !calState.active;
  }

  function saveCustomPinCoords(id, x, y) {
    try {
      var map = JSON.parse(localStorage.getItem(KEY_CUSTOM_COORDS) || "{}");
      map[id] = { x: x, y: y };
      localStorage.setItem(KEY_CUSTOM_COORDS, JSON.stringify(map));
    } catch (e) {}
  }

  function applyCustomPinCoords() {
    try {
      var map = JSON.parse(localStorage.getItem(KEY_CUSTOM_COORDS) || "{}");
      PINS.forEach(function (p) {
        if (map[p.id]) {
          p.x = map[p.id].x;
          p.y = map[p.id].y;
        }
      });
    } catch (e) {}
  }

  var $ = function (id) { return document.getElementById(id); };

  function initStorage() {
    applyCustomPinCoords();
    try {
      var d = JSON.parse(localStorage.getItem(KEY_DONE) || "{}");
      if (d && typeof d === "object") state.donePins = d;
      var l = localStorage.getItem(KEY_LANG);
      if (l === "en" || l === "zh") state.lang = l;
      var e = localStorage.getItem(KEY_ERA);
      if (e === "All" || e === "Child" || e === "Adult") state.era = e;
      var hd = localStorage.getItem(KEY_HIDE_DONE);
      if (hd !== null) state.hideDone = (hd === "1");
      var al = localStorage.getItem(KEY_AUTO_LEVEL);
      if (al !== null) state.autoLevel = (al === "1");
      var ar = localStorage.getItem(KEY_AREA);
      if (ar) state.area = ar;
    } catch (e) {}
  }

  function saveStorage() {
    try {
      localStorage.setItem(KEY_DONE, JSON.stringify(state.donePins));
      localStorage.setItem(KEY_LANG, state.lang);
      localStorage.setItem(KEY_ERA, state.era);
      localStorage.setItem(KEY_HIDE_DONE, state.hideDone ? "1" : "0");
      localStorage.setItem(KEY_AREA, state.area);
    } catch (e) {}
  }

  // -------------------------------------------------------------
  // 相机与视口缩放平移
  // -------------------------------------------------------------
  var cameraRafPending = false;

  function updateCameraTransform() {
    var board = $("mindmapBoard");
    if (board) {
      board.style.transform = "translate3d(" + state.tx + "px, " + state.ty + "px, 0) scale(" + state.zoom + ")";
      board.classList.toggle("lod-far", state.zoom < 0.48);
    }
  }

  function updateZoomMetrics() {
    document.documentElement.style.setProperty("--zoom-inv", (1 / state.zoom).toFixed(4));
    var zp = $("zoomPercent");
    if (zp) zp.textContent = Math.round(state.zoom * 100) + "%";
  }

  function updateCamera() {
    updateCameraTransform();
    updateZoomMetrics();
  }

  function requestCameraPan() {
    if (cameraRafPending) return;
    cameraRafPending = true;
    requestAnimationFrame(function () {
      updateCameraTransform();
      cameraRafPending = false;
    });
  }

  function fitCamera() {
    var stage = $("mapStage");
    var sw = stage.clientWidth;
    var sh = stage.clientHeight;
    if (!sw || !sh || !state.boardW || !state.boardH) return;

    var s = Math.min(sw / state.boardW, sh / state.boardH) * 0.92;
    state.zoom = s;
    state.tx = (sw - state.boardW * s) / 2;
    state.ty = (sh - state.boardH * s) / 2;
    updateCamera();
  }

  function zoomAt(factor, clientX, clientY) {
    var stage = $("mapStage");
    var rect = stage.getBoundingClientRect();
    var px = (clientX !== undefined ? clientX - rect.left : rect.width / 2);
    var py = (clientY !== undefined ? clientY - rect.top : rect.height / 2);

    var oldZoom = state.zoom;
    var newZoom = Math.max(state.minZoom, Math.min(state.maxZoom, oldZoom * factor));
    if (Math.abs(newZoom - oldZoom) < 0.001) return;

    var wx = (px - state.tx) / oldZoom;
    var wy = (py - state.ty) / oldZoom;

    state.zoom = newZoom;
    state.tx = px - wx * newZoom;
    state.ty = py - wy * newZoom;
    state.levelFocusX = clientX;
    state.levelFocusY = clientY;

    updateCamera();
    if (state.mode === "topology") scheduleLevelCheck();
  }

  // 平滑聚焦到某个节点
  function focusNode(nodeId, targetZoom) {
    var node = NODES.find(function (n) { return n.id === nodeId; });
    if (!node) return;

    var stage = $("mapStage");
    var sw = stage.clientWidth || (window.innerWidth - 320);
    var sh = stage.clientHeight || window.innerHeight;
    var z = targetZoom || 1.1;

    state.zoom = z;
    var centerWorldX = node.x + state.originOffsetX + node.w / 2;
    var centerWorldY = node.y + state.originOffsetY + node.h / 2;

    state.tx = sw / 2 - centerWorldX * z;
    state.ty = sh / 2 - centerWorldY * z;

    updateCamera();
  }

  function bindCameraEvents() {
    var stage = $("mapStage");

    stage.addEventListener("mousedown", function (e) {
      if (state.mode !== "topology") return;
      if (e.button !== 0) return;
      if (e.target.closest(".map-pin") || e.target.closest(".detail-card") || e.target.closest(".zoom-controls") || e.target.closest(".floor-btn")) return;
      state.isDragging = true;
      state.dragMoved = false;
      state.dragStartX = e.clientX;
      state.dragStartY = e.clientY;
      state.camStartX = state.tx;
      state.camStartY = state.ty;
    });

    window.addEventListener("mousemove", function (e) {
      if (calState.active && calState.draggingPin && calState.targetBox) {
        var rect = calState.targetBox.getBoundingClientRect();
        var px = Math.max(0, Math.min(100, ((e.clientX - rect.left) / rect.width) * 100));
        var py = Math.max(0, Math.min(100, ((e.clientY - rect.top) / rect.height) * 100));
        calState.draggingPin.x = Math.round(px * 10) / 10;
        calState.draggingPin.y = Math.round(py * 10) / 10;
        var pel = $("pin-" + calState.draggingPin.id);
        if (pel) {
          pel.style.left = calState.draggingPin.x + "%";
          pel.style.top = calState.draggingPin.y + "%";
        }
        return;
      }
      if (!state.isDragging) return;
      var dx = e.clientX - state.dragStartX;
      var dy = e.clientY - state.dragStartY;
      if (Math.hypot(dx, dy) > 5) {
        state.dragMoved = true;
      }
      state.tx = state.camStartX + dx;
      state.ty = state.camStartY + dy;
      requestCameraPan();
    });

    window.addEventListener("mouseup", function () {
      if (calState.active && calState.draggingPin) {
        console.log("📍 已校准点位 [" + calState.draggingPin.id + "]: x=" + calState.draggingPin.x + "%, y=" + calState.draggingPin.y + "% (" + calState.draggingPin.zh + ")");
        saveCustomPinCoords(calState.draggingPin.id, calState.draggingPin.x, calState.draggingPin.y);
        calState.draggingPin = null;
        calState.targetBox = null;
        return;
      }
      state.isDragging = false;
      setTimeout(function () {
        state.dragMoved = false;
      }, 50);
    });

    stage.addEventListener("wheel", function (e) {
      if (state.mode !== "topology") return;
      e.preventDefault();
      var factor = e.deltaY < 0 ? 1.18 : 0.85;
      zoomAt(factor, e.clientX, e.clientY);
    }, { passive: false });

    stage.addEventListener("dblclick", function (e) {
      if (state.mode !== "topology") return;
      if (e.target.closest(".map-pin") || e.target.closest(".node-card") || e.target.closest(".detail-card")) return;
      zoomAt(1.5, e.clientX, e.clientY);
    });

    // 触屏手势
    var touchDist = 0;
    stage.addEventListener("touchstart", function (e) {
      if (state.mode !== "topology") return;
      if (e.touches.length === 1) {
        if (e.target.closest(".map-pin") || e.target.closest(".detail-card")) return;
        state.isDragging = true;
        state.dragStartX = e.touches[0].clientX;
        state.dragStartY = e.touches[0].clientY;
        state.camStartX = state.tx;
        state.camStartY = state.ty;
      } else if (e.touches.length === 2) {
        state.isDragging = false;
        var dx = e.touches[0].clientX - e.touches[1].clientX;
        var dy = e.touches[0].clientY - e.touches[1].clientY;
        touchDist = Math.hypot(dx, dy);
      }
    }, { passive: true });

    stage.addEventListener("touchmove", function (e) {
      if (state.mode !== "topology") return;
      if (e.touches.length === 1 && state.isDragging) {
        var dx = e.touches[0].clientX - state.dragStartX;
        var dy = e.touches[0].clientY - state.dragStartY;
        if (Math.hypot(dx, dy) > 5) {
          state.dragMoved = true;
        }
        state.tx = state.camStartX + dx;
        state.ty = state.camStartY + dy;
        requestCameraPan();
      } else if (e.touches.length === 2) {
        var dx = e.touches[0].clientX - e.touches[1].clientX;
        var dy = e.touches[0].clientY - e.touches[1].clientY;
        var newDist = Math.hypot(dx, dy);
        if (touchDist > 0) {
          var factor = newDist / touchDist;
          var midX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
          var midY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
          zoomAt(factor, midX, midY);
        }
        touchDist = newDist;
      }
    }, { passive: true });

    stage.addEventListener("touchend", function () {
      state.isDragging = false;
      touchDist = 0;
      setTimeout(function () {
        state.dragMoved = false;
      }, 50);
    });

    $("btnZoomIn").addEventListener("click", function () {
      if (state.mode === "region") regionZoomAt(1.25);
      else if (state.mode === "world") worldZoomAt(1.18);
      else zoomAt(1.25);
    });
    $("btnZoomOut").addEventListener("click", function () {
      if (state.mode === "region") regionZoomAt(0.8);
      else if (state.mode === "world") worldZoomAt(0.85);
      else zoomAt(0.8);
    });
    $("btnZoomFit").addEventListener("click", function () {
      if (state.mode === "region") fitRegion();
      else if (state.mode === "world") enterWorldDefault();
      else focusNode("HyruleField", 0.33);
    });
  }

  // =============================================================
  // 区域单图模式：区域列表 / 楼层 / 缩放 / 点位
  // =============================================================

  var regionFile = "";
  var regionBase = { w: 0, h: 0, left: 0, top: 0 };

  function currentRegion() {
    return REGIONS.find(function (r) { return r.id === state.area; }) || REGIONS[0] || null;
  }

  function pinBelongsToRegion(pin, r) {
    if (!r) return false;
    if (r.kind === "field") return pin.map === "hyrule" && pin.area === r.id;
    return pin.map === r.id;
  }

  function regionPinsForEra(r) {
    return PINS.filter(function (p) {
      if (state.era !== "All" && p.era !== "Both" && p.era !== state.era) return false;
      return pinBelongsToRegion(p, r);
    });
  }

  function isRegionAvailable(r) {
    if (!r) return false;
    var eraPins = regionPinsForEra(r);
    if (r.kind === "field") {
      if (state.era === "All") return !!(r.maps && ((r.maps.Adult || []).length || (r.maps.Child || []).length));
      return !!(r.maps && (r.maps[state.era] || []).length);
    }
    return eraPins.length > 0;
  }

  function regionMapFile(r) {
    if (!r) return "";
    if (r.kind === "dungeon") {
      var floors = r.floors || [];
      var pick = floors.find(function (f) { return f.label === state.floor; });
      if (!pick) pick = floors.find(function (f) { return f.label === "All"; });
      if (!pick && floors.length) pick = floors[0];
      return pick ? pick.file : "";
    }
    var order = state.era === "Adult" ? ["Adult", "Child"] : state.era === "Child" ? ["Child", "Adult"] : ["Child", "Adult"];
    for (var i = 0; i < order.length; i++) {
      var list = (r.maps && r.maps[order[i]]) || [];
      if (list.length) {
        var item = list[0];
        return typeof item === "string" ? item : ((item && item.file) || "");
      }
    }
    return "";
  }

  function regionFloorLabel(r) {
    if (!r || r.kind !== "dungeon") return "";
    var fl = state.floor === "All" ? "全层" : state.floor;
    return fl;
  }

  function renderRegionList() {
    var fieldBox = $("regionFieldList");
    var dungBox = $("regionDungeonList");
    if (!fieldBox || !dungBox) return;
    fieldBox.innerHTML = "";
    dungBox.innerHTML = "";

    var available = REGIONS.filter(isRegionAvailable);
    var field = available.filter(function (r) { return r.kind === "field"; });
    var dungeon = available.filter(function (r) { return r.kind === "dungeon"; });
    var hiddenCount = REGIONS.length - available.length;

    $("regionFieldCount").textContent = field.length;
    $("regionDungeonCount").textContent = dungeon.length;
    var eraLbl = $("regionEraLbl");
    if (eraLbl) eraLbl.textContent = state.era === "All" ? "全部时代" : (state.era === "Child" ? "童年" : "成年");

    function buildOne(r, box) {
      var b = document.createElement("button");
      var rPins = regionPinsForEra(r);
      var n = rPins.length;
      var d = 0;
      for (var i = 0; i < rPins.length; i++) {
        if (state.donePins[rPins[i].id]) d++;
      }
      b.className = "region-item" + (r.id === state.area ? " on" : "") + (d > 0 ? " has-done" : "");
      b.setAttribute("data-region", r.id);
      b.innerHTML = "<span>" + (state.lang === "zh" ? r.zh : r.en) + "</span>" +
        "<em>" + d + "/" + n + "</em>";
      b.addEventListener("click", function () { openRegion(r.id); });
      box.appendChild(b);
    }
    field.forEach(function (r) { buildOne(r, fieldBox); });
    dungeon.forEach(function (r) { buildOne(r, dungBox); });

    var note = $("regionEraNote");
    if (hiddenCount > 0) {
      note.textContent = "已隐藏 " + hiddenCount + " 个仅" + (state.era === "Child" ? "成年" : "童年") + "可进入的区域，切换时代可见。";
    } else {
      note.textContent = "当前时代 31 个区域全部可进入。";
    }
  }

  function updateRegionHead(r) {
    if (!r) return;
    $("regionKicker").textContent = r.kind === "field" ? "FIELD REGION" : "DUNGEON · " + Math.max(0, (r.floors || []).length - 1) + " FLOORS";
    $("regionName").textContent = state.lang === "zh" ? r.zh : r.en;
    var available = isRegionAvailable(r);
    var sub = "";
    if (available) {
      var total = regionPinsForEra(r).length;
      if (r.kind === "dungeon" && state.floor !== "All") {
        var shown = PINS.filter(function (p) {
          if (state.era !== "All" && p.era !== "Both" && p.era !== state.era) return false;
          return pinBelongsToRegion(p, r) && pinOnFloor(p, state.floor);
        }).length;
        sub = shown + " / " + total + " 个点位 · " + state.floor;
      } else {
        var mapNote = r.kind === "dungeon" ? regionFloorLabel(r) : (state.era === "Adult" ? "成年底图" : "童年底图");
        sub = total + " 个点位 · " + mapNote;
      }
    } else {
      sub = "当前时代不可进入";
    }
    $("regionSub").textContent = sub;
    $("regionEmpty").hidden = available;
    $("regionWorld").style.visibility = available ? "" : "hidden";
  }

  function buildRegionFloorBar(r) {
    var bar = $("regionFloorBar");
    if (!bar) return;
    if (!r || r.kind !== "dungeon") {
      bar.hidden = true;
      bar.innerHTML = "";
      return;
    }
    var floors = (r.floors || []).slice();
    floors.sort(function (a, b) {
      if (a.label === "All") return -1;
      if (b.label === "All") return 1;
      function rank(x) {
        if (x.charAt(0) === "B") return 100 + parseInt(x.slice(1), 10);
        return parseInt(x, 10) || 0;
      }
      return rank(a.label) - rank(b.label);
    });
    if (!floors.length) { bar.hidden = true; return; }
    bar.innerHTML = "";
    floors.forEach(function (f) {
      var b = document.createElement("button");
      b.className = "region-floor-btn" + (state.floor === f.label ? " on" : "");
      b.textContent = f.label === "All" ? "全层" : f.label;
      b.setAttribute("data-floor", f.label);
      b.addEventListener("click", function (e) {
        e.stopPropagation();
        state.floor = f.label;
        buildRegionFloorBar(r);
        updateRegionHead(r);
        loadRegionMap(r, true);
      });
      bar.appendChild(b);
    });
    bar.hidden = false;
  }

  function layoutRegionBase() {
    var board = $("regionBoard");
    var img = $("regionImg");
    if (!board || !img) return;
    var W = board.clientWidth;
    var H = board.clientHeight;
    if (!W || !H) return;
    var iw = img.naturalWidth || 1024;
    var ih = img.naturalHeight || 1024;
    var s = Math.min(W / iw, H / ih);
    regionBase.w = iw * s;
    regionBase.h = ih * s;
    regionBase.left = (W - regionBase.w) / 2;
    regionBase.top = (H - regionBase.h) / 2;
    var world = $("regionWorld");
    world.style.width = regionBase.w + "px";
    world.style.height = regionBase.h + "px";
    world.style.left = regionBase.left + "px";
    world.style.top = regionBase.top + "px";
  }

  function applyRegionCam() {
    var world = $("regionWorld");
    if (!world) return;
    world.style.transform = "translate3d(" + state.regionTx + "px," + state.regionTy + "px,0) scale(" + state.regionZoom + ")";
    var inv = (1 / state.regionZoom).toFixed(4);
    var board = $("regionBoard");
    if (board) board.style.setProperty("--region-inv", inv);
    var zp = $("zoomPercent");
    if (zp && state.mode === "region") zp.textContent = Math.round(state.regionZoom * 100) + "%";
  }

  function fitRegion() {
    var board = $("regionBoard");
    var z = 1;
    var tx = 0;
    var ty = 0;
    // 手机窄屏下若底图（如德库树 1F）远窄于视口，自动放大以铺满可用宽度
    if (board && window.innerWidth <= 900 && regionBase.w > 0 && board.clientWidth > 0) {
      if (regionBase.w < board.clientWidth * 0.72) {
        z = Math.min(1.65, (board.clientWidth * 0.88) / regionBase.w);
        var cx = board.clientWidth / 2;
        var cy = board.clientHeight / 2;
        tx = cx - regionBase.left - (regionBase.w / 2) * z;
        ty = cy - regionBase.top - (regionBase.h / 2) * z;
      }
    }
    state.regionZoom = z;
    state.regionTx = tx;
    state.regionTy = ty;
    applyRegionCam();
  }

  function regionZoomAt(factor, clientX, clientY) {
    var board = $("regionBoard");
    if (!board) return;
    var rect = board.getBoundingClientRect();
    var px = (clientX !== undefined ? clientX - rect.left : rect.width / 2);
    var py = (clientY !== undefined ? clientY - rect.top : rect.height / 2);
    var oldZoom = state.regionZoom;
    var newZoom = Math.max(0.32, Math.min(2.0, oldZoom * factor));
    if (Math.abs(newZoom - oldZoom) < 0.001) return;
    var wx = (px - regionBase.left - state.regionTx) / oldZoom;
    var wy = (py - regionBase.top - state.regionTy) / oldZoom;
    state.regionZoom = newZoom;
    state.regionTx = px - regionBase.left - wx * newZoom;
    state.regionTy = py - regionBase.top - wy * newZoom;
    state.levelFocusX = clientX;
    state.levelFocusY = clientY;
    applyRegionCam();
    scheduleLevelCheck();
  }

  function pinOnFloor(pin, floor) {
    if (floor === "All") return true;
    if (floor === "1F") return pin.area === "1F" || pin.area === "0F";
    return pin.area === floor;
  }

  function renderRegionPins() {
    var box = $("regionPins");
    if (!box) return;
    box.innerHTML = "";
    var r = currentRegion();
    if (!r || !isRegionAvailable(r)) return;

    var list = PINS.filter(function (p) {
      return isPinVisible(p) && pinBelongsToRegion(p, r) && pinOnFloor(p, state.floor);
    });

    list.forEach(function (pin) {
      var el = document.createElement("div");
      el.className = "map-pin" +
        (state.donePins[pin.id] ? " done" : "") +
        (state.selectedPinId === pin.id ? " selected" : "");
      el.id = "rpin-" + pin.id;
      el.style.left = pin.x + "%";
      el.style.top = pin.y + "%";
      el.innerHTML = ICONS.html(pin.cat, pinIconSize(), !!state.donePins[pin.id]);

      el.addEventListener("mousedown", function (e) {
        if (calState.active) {
          e.stopPropagation();
          calState.draggingPin = pin;
          calState.targetBox = box;
        }
      });
      el.addEventListener("click", function (e) {
        e.stopPropagation();
        if (!calState.active) selectPin(pin);
      });
      box.appendChild(el);
    });

    renderRegionGateways(r, box);
  }

  function renderRegionGateways(r, box) {
    var topoNode = NODES.find(function (n) { return n.id === r.id; });
    if (!topoNode || !topoNode.gateways || !topoNode.gateways.length) return;
    topoNode.gateways.forEach(function (gw) {
      var targetNode = NODES.find(function (n) { return n.id === gw.target; });
      var targetReg = REGIONS.find(function (x) { return x.id === gw.target; });
      if (targetReg && !isRegionAvailable(targetReg)) return;
      var targetName = targetNode ? (state.lang === "zh" ? targetNode.zh : targetNode.en) : gw.target;
      var gwEl = document.createElement("button");
      gwEl.type = "button";
      gwEl.className = "region-gw";
      gwEl.style.left = gw.x + "%";
      gwEl.style.top = gw.y + "%";
      // MapIconArrow_00.png 原图朝上(▲)，仅保留上下左右四方向（up:0 / right:90 / down:180 / left:270）
      var dirMap = { up: 0, right: 90, down: 180, left: 270 };
      var ang = (gw.dir && Object.prototype.hasOwnProperty.call(dirMap, gw.dir))
        ? dirMap[gw.dir]
        : Math.round((Math.atan2(gw.y - 50, gw.x - 50) * 180 / Math.PI + 90) / 90) * 90;
      gwEl.innerHTML =
        '<img class="rgw-arrow" src="assets/ui/MapIconArrow_00.png" width="28" height="28" style="transform:rotate(' + ang + 'deg)" alt="">' +
        '<span class="rgw-txt">' + targetName + '</span>';
      gwEl.title = (state.lang === "zh" ? "前往 " : "To ") + targetName;
      gwEl.addEventListener("click", function (e) {
        e.stopPropagation();
        openRegion(gw.target);
      });
      box.appendChild(gwEl);
    });
  }

  function loadRegionMap(r, keepZoom) {
    var file = regionMapFile(r);
    var img = $("regionImg");
    var world = $("regionWorld");
    if (!img || !file) return;
    if (file === regionFile) {
      if (!keepZoom) fitRegion();
      renderRegionPins();
      return;
    }
    regionFile = file;
    if (world) world.style.opacity = "0";
    var box = $("regionPins");
    if (box) box.innerHTML = "";
    img.onload = function () {
      layoutRegionBase();
      if (!keepZoom) fitRegion(); else applyRegionCam();
      renderRegionPins();
      if (world) world.style.opacity = "1";
    };
    img.onerror = function () {
      if (world) world.style.opacity = "1";
      $("regionSub").textContent = "底图加载失败：" + file;
    };
    img.src = file;
  }

  function openRegion(id, opts) {
    opts = opts || {};
    var r = REGIONS.find(function (x) { return x.id === id; });
    if (!r) return;
    state.area = id;
    state.floor = opts.floor || "All";
    state.selectedPinId = null;
    closeDetailCard();
    saveStorage();
    if (state.mode !== "region") {
      setMode("region");
      return;
    }
    renderRegionList();
    renderCategoriesSidebar();
    updateRegionHead(r);
    buildRegionFloorBar(r);
    if (isRegionAvailable(r)) loadRegionMap(r, opts.keepZoom);
    else renderRegionPins();
    updateUrl();
  }

  function chooseRegionForEra() {
    var cur = currentRegion();
    if (cur && isRegionAvailable(cur)) return cur;
    var preferred = REGIONS.find(function (r) { return r.id === "KokiriForest"; });
    var first = preferred && isRegionAvailable(preferred) ? preferred :
      REGIONS.find(isRegionAvailable);
    return first || null;
  }

  function syncRegionForEra() {
    if (!REGIONS.length) return;
    // 时代切换后当前选中的点位可能不属于新图层，先收起详情卡
    var card = $("detailCard");
    if (card && !card.hidden) closeDetailCard();
    var pick = chooseRegionForEra();
    if (pick && (!currentRegion() || !isRegionAvailable(currentRegion()))) {
      openRegion(pick.id, { keepZoom: false });
      return;
    }
    renderRegionList();
    var r = currentRegion();
    if (r) {
      updateRegionHead(r);
      buildRegionFloorBar(r);
      loadRegionMap(r, true);
      renderRegionPins();
    }
  }

  function setMode(mode) {
    state.mode = mode;
    closeDetailCard();
    saveStorage();
    document.body.setAttribute("data-view", mode);
    var regionBoard = $("regionBoard");
    var mindmap = $("mindmapBoard");
    var worldBoard = $("worldBoard");
    var rp = $("regionPanel");
    var js = $("jumpSection");
    if (regionBoard) regionBoard.hidden = (mode !== "region");
    if (mindmap) mindmap.hidden = (mode !== "topology");
    if (worldBoard) worldBoard.hidden = (mode !== "world");
    if (rp) rp.hidden = (mode === "topology");
    if (js) js.hidden = (mode !== "topology");

    document.querySelectorAll("#viewTabs .view-tab").forEach(function (b) {
      b.classList.toggle("on", b.getAttribute("data-view") === mode);
    });

    if (mode === "world") {
      var wi = $("worldImg");
      var wl = $("worldLoading");
      var loadWorld = function () {
        if (wl) wl.hidden = true;
        layoutWorldBase();
        enterWorldDefault();
        renderWorldPins();
      };
      if (wi && !wi.getAttribute("src")) {
        if (wl) wl.hidden = false;
        wi.onload = loadWorld;
        wi.onerror = function () { if (wl) { wl.hidden = false; wl.textContent = "全图载入失败"; } };
        wi.src = wi.getAttribute("data-src");
      } else if (wi && wi.complete && wi.naturalWidth) {
        loadWorld();
      } else if (wi) {
        if (wl) wl.hidden = false;
        wi.addEventListener("load", loadWorld, { once: true });
      }
      renderRegionList();
      renderCategoriesSidebar();
      updateUrl();
      return;
    }

    if (mode === "region") {
      renderRegionList();
      renderCategoriesSidebar();
      var r = currentRegion();
      if (r && !isRegionAvailable(r)) {
        var pick = chooseRegionForEra();
        if (pick) { openRegion(pick.id, { keepZoom: false }); return; }
      }
      if (r) {
        updateRegionHead(r);
        buildRegionFloorBar(r);
        loadRegionMap(r, false);
      }
      applyRegionCam();
    } else {
      // 拓扑模式保留原有的“聚焦海拉鲁平原 hub”视野
      renderCategoriesSidebar();
      focusNode("HyruleField", 0.52);
    }
    updateUrl();
  }

  function updateUrl(pinId) {
    try {
      var p = new URLSearchParams(window.location.search);
      p.set("mode", state.mode);
      p.set("era", state.era);
      p.delete("node");
      if (state.mode === "region") {
        p.set("area", state.area);
        if (state.floor && state.floor !== "All") p.set("floor", state.floor); else p.delete("floor");
      } else {
        p.delete("area");
        p.delete("floor");
      }
      if (pinId) p.set("pin", pinId); else p.delete("pin");
      history.replaceState(null, "", window.location.pathname + "?" + p.toString());
    } catch (e) {}
  }

  function bindRegionEvents() {
    var board = $("regionBoard");
    if (!board) return;

    board.addEventListener("pointerdown", function (e) {
      if (e.button !== undefined && e.button !== 0) return;
      if (e.target.closest(".map-pin") || e.target.closest(".detail-card") || e.target.closest(".zoom-controls") || e.target.closest(".region-floor-bar")) return;
      state.regionDragging = true;
      state.regionDragMoved = false;
      state.regionDragStartX = e.clientX;
      state.regionDragStartY = e.clientY;
      state.regionCamStartX = state.regionTx;
      state.regionCamStartY = state.regionTy;
      board.classList.add("dragging");
    });

    window.addEventListener("pointermove", function (e) {
      if (!state.regionDragging) return;
      var dx = e.clientX - state.regionDragStartX;
      var dy = e.clientY - state.regionDragStartY;
      if (Math.hypot(dx, dy) > 4) state.regionDragMoved = true;
      state.regionTx = state.regionCamStartX + dx;
      state.regionTy = state.regionCamStartY + dy;
      applyRegionCam();
    });

    window.addEventListener("pointerup", function () {
      if (state.regionDragging) {
        state.regionDragging = false;
        board.classList.remove("dragging");
      }
      setTimeout(function () { state.regionDragMoved = false; }, 50);
    });

    board.addEventListener("wheel", function (e) {
      e.preventDefault();
      regionZoomAt(e.deltaY < 0 ? 1.14 : 0.88, e.clientX, e.clientY);
    }, { passive: false });

    board.addEventListener("dblclick", function (e) {
      if (e.target.closest(".map-pin")) return;
      regionZoomAt(1.5, e.clientX, e.clientY);
    });

    var pinchDist = 0;
    board.addEventListener("touchstart", function (e) {
      if (e.touches.length === 2) {
        pinchDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      }
    }, { passive: true });

    board.addEventListener("touchmove", function (e) {
      if (e.touches.length === 2) {
        e.preventDefault();
        var d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
        if (pinchDist > 0) {
          var rect = board.getBoundingClientRect();
          var mx = (e.touches[0].clientX + e.touches[1].clientX) / 2;
          var my = (e.touches[0].clientY + e.touches[1].clientY) / 2;
          regionZoomAt(d / pinchDist, mx, my);
        }
        pinchDist = d;
      }
    }, { passive: false });

    board.addEventListener("touchend", function () { pinchDist = 0; }, { passive: true });
  }

  // -------------------------------------------------------------
  // 全图层：官方手绘全图 + 21 区域印章 + 10 迷宫入口
  // -------------------------------------------------------------
  var worldBase = { w: 0, h: 0, left: 0, top: 0 };
  var worldZoomRaf = 0;

  function availableRegion(id) {
    return REGIONS.find(function (r) { return r.id === id; });
  }

  function layoutWorldBase() {
    var board = $("worldBoard");
    var img = $("worldImg");
    var canvas = $("worldCanvas");
    if (!board || !img || !canvas) return;
    var W = board.clientWidth;
    var H = board.clientHeight;
    if (!W || !H) return;
    var iw = img.naturalWidth || 4608;
    var ih = img.naturalHeight || 3360;
    var s = Math.min(W / iw, H / ih);
    worldBase.w = iw * s;
    worldBase.h = ih * s;
    var spareX = Math.max(0, (W - worldBase.w) / 2);
    var sideW = $("sidebar") ? $("sidebar").offsetWidth : 0;
    var desktopOpen = window.innerWidth > 900 && !document.body.classList.contains("side-collapsed");
    var shift = desktopOpen ? Math.min(sideW / 2, spareX) : 0;
    worldBase.left = spareX + shift;
    worldBase.top = (H - worldBase.h) / 2;
    canvas.style.width = worldBase.w + "px";
    canvas.style.height = worldBase.h + "px";
    canvas.style.left = worldBase.left + "px";
    canvas.style.top = worldBase.top + "px";
  }

  function applyWorldCam() {
    var canvas = $("worldCanvas");
    if (!canvas) return;
    canvas.style.transform = "translate3d(" + state.worldTx + "px," + state.worldTy + "px,0) scale(" + state.worldZoom + ")";
    var pins = $("worldPins");
    if (pins) {
      pins.style.left = (worldBase.left + state.worldTx) + "px";
      pins.style.top = (worldBase.top + state.worldTy) + "px";
      pins.style.width = (worldBase.w * state.worldZoom) + "px";
      pins.style.height = (worldBase.h * state.worldZoom) + "px";
      var sc = Math.min(1.45, Math.max(1, 0.85 + state.worldZoom * 0.15));
      pins.style.setProperty("--world-scale", sc.toFixed(3));
    }
    var zp = $("zoomPercent");
    if (zp && state.mode === "world") zp.textContent = Math.round(state.worldZoom * 100) + "%";
  }

  function focusWorldPoint(x, y, z) {
    var board = $("worldBoard");
    if (!board || !worldBase.w) return;
    if (worldZoomRaf) { cancelAnimationFrame(worldZoomRaf); worldZoomRaf = 0; }
    var W = board.clientWidth;
    var H = board.clientHeight;
    state.worldZoom = z;
    state.worldTx = W / 2 - worldBase.left - x * worldBase.w * z;
    state.worldTy = H / 2 - worldBase.top - y * worldBase.h * z;
    applyWorldCam();
  }

  function enterWorldDefault() {
    if (window.innerWidth <= 900 && window.OOT_WORLD) {
      var f = window.OOT_WORLD.fields.find(function (x) { return x.id === "HyruleField"; });
      if (f) { focusWorldPoint(f.x, f.y, 2.0); return; }
    }
    fitWorld();
  }

  function fitWorld() {
    if (worldZoomRaf) { cancelAnimationFrame(worldZoomRaf); worldZoomRaf = 0; }
    state.worldZoom = 1;
    state.worldTx = 0;
    state.worldTy = 0;
    applyWorldCam();
  }

  function animateWorldCam(targetZ, targetX, targetY) {
    if (worldZoomRaf) cancelAnimationFrame(worldZoomRaf);
    var z0 = state.worldZoom;
    var x0 = state.worldTx;
    var y0 = state.worldTy;
    if (Math.abs(targetZ - z0) < 0.0005) {
      state.worldTx = targetX;
      state.worldTy = targetY;
      applyWorldCam();
      return;
    }
    var t0 = performance.now();
    var step = function (now) {
      var p = Math.min(1, (now - t0) / 90);
      var e = 1 - Math.pow(1 - p, 3);
      state.worldZoom = z0 + (targetZ - z0) * e;
      state.worldTx = x0 + (targetX - x0) * e;
      state.worldTy = y0 + (targetY - y0) * e;
      applyWorldCam();
      if (p < 1) {
        worldZoomRaf = requestAnimationFrame(step);
      } else {
        worldZoomRaf = 0;
      }
    };
    worldZoomRaf = requestAnimationFrame(step);
  }

  function worldZoomAt(factor, clientX, clientY) {
    var board = $("worldBoard");
    if (!board) return;
    var rect = board.getBoundingClientRect();
    var px = (clientX !== undefined ? clientX - rect.left : rect.width / 2);
    var py = (clientY !== undefined ? clientY - rect.top : rect.height / 2);
    var oldZoom = state.worldZoom;
    var maxWorldZoom = state.autoLevel ? (worldInThreshold() + 0.01) : 4.0;
    var newZoom = Math.max(0.85, Math.min(maxWorldZoom, oldZoom * factor));
    if (Math.abs(newZoom - oldZoom) < 0.001) return;
    var wx = (px - worldBase.left - state.worldTx) / oldZoom;
    var wy = (py - worldBase.top - state.worldTy) / oldZoom;
    var nx = px - worldBase.left - wx * newZoom;
    var ny = py - worldBase.top - wy * newZoom;
    state.levelFocusX = clientX;
    state.levelFocusY = clientY;
    animateWorldCam(newZoom, nx, ny);
    scheduleLevelCheck();
  }

  function renderWorldPins() {
    var box = $("worldPins");
    if (!box || !window.OOT_WORLD) return;
    box.innerHTML = "";
    var fieldCount = 0;
    var entryCount = 0;

    window.OOT_WORLD.fields.forEach(function (f) {
      var r = availableRegion(f.id);
      if (!r || !isRegionAvailable(r)) return;
      fieldCount++;
      var list = regionPinsForEra(r);
      var done = list.filter(function (p) { return !!state.donePins[p.id]; }).length;
      var total = list.length;
      var pct = total ? Math.round(done / total * 100) : 0;
      var seal = document.createElement("div");
      seal.className = "world-seal";
      seal.style.left = (f.x * 100) + "%";
      seal.style.top = (f.y * 100) + "%";
      seal.style.setProperty("--pct", pct);
      seal.setAttribute("role", "button");
      seal.setAttribute("tabindex", "0");
      seal.setAttribute("aria-label", (state.lang === "zh" ? r.zh : r.en) + " " + done + "/" + total);
      seal.innerHTML = '<span class="ws-mark">' + (state.lang === "zh" ? r.zh.slice(0, 1) : r.en.slice(0, 1)) + '</span>' +
        '<span class="ws-label"><em>' + (state.lang === "zh" ? r.zh : r.en) + '</em><b>' + done + '/' + total + '</b></span>';
      seal.title = (state.lang === "zh" ? r.zh : r.en) + " · " + done + "/" + total;
      seal.addEventListener("click", function (e) {
        e.stopPropagation();
        openRegion(f.id);
      });
      seal.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openRegion(f.id); }
      });
      box.appendChild(seal);
    });

    window.OOT_WORLD.dungeons.forEach(function (d) {
      var r = availableRegion(d.id);
      if (!r || !isRegionAvailable(r)) return;
      entryCount++;
      var host = availableRegion(d.host);
      var mark = document.createElement("div");
      mark.className = "world-entry";
      mark.style.left = (d.x * 100) + "%";
      mark.style.top = (d.y * 100) + "%";
      mark.setAttribute("role", "button");
      mark.setAttribute("tabindex", "0");
      mark.setAttribute("aria-label", (state.lang === "zh" ? r.zh : r.en));
      mark.innerHTML = '<span class="we-mark">◆</span>' +
        '<span class="ws-label"><em>' + (state.lang === "zh" ? r.zh : r.en) + '</em><b>入口</b></span>';
      mark.title = (state.lang === "zh" ? r.zh : r.en) + (host ? " · 进入 " + (state.lang === "zh" ? host.zh : host.en) : "");
      mark.addEventListener("click", function (e) {
        e.stopPropagation();
        openRegion(d.host || d.id);
      });
      mark.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openRegion(d.host || d.id); }
      });
      box.appendChild(mark);
    });

    var sub = $("worldCaptionSub");
    if (sub) {
      var mobile = window.innerWidth <= 900;
      sub.textContent = state.lang === "zh"
        ? (mobile ? fieldCount + "+" + entryCount + " · 双指缩放 · ⤢ 总览 · 点印章进区域"
                  : fieldCount + " 区域 · " + entryCount + " 迷宫入口 · 点印章进区域")
        : (mobile ? fieldCount + "+" + entryCount + " · pinch · ⤢ overview · tap a seal"
                  : fieldCount + " regions · " + entryCount + " dungeon entrances · click a seal");
    }
  }

  function bindWorldEvents() {
    var board = $("worldBoard");
    if (!board) return;

    board.addEventListener("pointerdown", function (e) {
      if (state.mode !== "world") return;
      if (e.button !== undefined && e.button !== 0) return;
      if (e.target.closest(".world-seal") || e.target.closest(".world-entry") ||
          e.target.closest(".zoom-controls") || e.target.closest(".world-caption")) return;
      if (worldZoomRaf) { cancelAnimationFrame(worldZoomRaf); worldZoomRaf = 0; }
      state.worldDragging = true;
      state.worldDragMoved = false;
      state.worldDragStartX = e.clientX;
      state.worldDragStartY = e.clientY;
      state.worldCamStartX = state.worldTx;
      state.worldCamStartY = state.worldTy;
      board.classList.add("dragging");
    });

    window.addEventListener("pointermove", function (e) {
      if (!state.worldDragging) return;
      var dx = e.clientX - state.worldDragStartX;
      var dy = e.clientY - state.worldDragStartY;
      if (Math.hypot(dx, dy) > 4) state.worldDragMoved = true;
      state.worldTx = state.worldCamStartX + dx;
      state.worldTy = state.worldCamStartY + dy;
      applyWorldCam();
    });

    window.addEventListener("pointerup", function () {
      if (state.worldDragging) {
        state.worldDragging = false;
        board.classList.remove("dragging");
      }
    });

    board.addEventListener("wheel", function (e) {
      if (state.mode !== "world") return;
      e.preventDefault();
      worldZoomAt(e.deltaY < 0 ? 1.18 : 0.88, e.clientX, e.clientY);
    }, { passive: false });

    board.addEventListener("dblclick", function (e) {
      if (state.mode !== "world") return;
      if (e.target.closest(".world-seal") || e.target.closest(".world-entry")) return;
      var hit = nearestWorldFieldAt(e.clientX, e.clientY, 120);
      if (hit) { openRegion(hit.id); return; }
      worldZoomAt(1.3, e.clientX, e.clientY);
    });

    var pinchDist = 0;
    board.addEventListener("touchstart", function (e) {
      if (state.mode !== "world") return;
      if (e.touches.length === 2) {
        pinchDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      }
    }, { passive: true });

    board.addEventListener("touchmove", function (e) {
      if (state.mode !== "world" || e.touches.length !== 2) return;
      e.preventDefault();
      var d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      if (pinchDist > 0) {
        var mx = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        var my = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        worldZoomAt(d / pinchDist, mx, my);
      }
      pinchDist = d;
    }, { passive: false });

    board.addEventListener("touchend", function () { pinchDist = 0; }, { passive: true });
  }

  // -------------------------------------------------------------
  // 三层缩放换层：默认 区域(33%~200%) ↔ 拓扑(15%~250%) ↔ 全图(85%~250%)
  // 可在设置面板自定义阈值，持久化到 localStorage
  // -------------------------------------------------------------
  var KEY_LEVEL_TH = "oot_map_level_thresholds";
  var LEVEL_DEFAULTS = { regionOut: 0.33, topoOut: 0.15, worldIn: 2.5, topoIn: 2.5, settle: 140, lock: 550 };
  var LEVEL = Object.assign({}, LEVEL_DEFAULTS);
  try {
    var savedTh = JSON.parse(localStorage.getItem(KEY_LEVEL_TH) || "null");
    if (savedTh && typeof savedTh === "object") {
      ["regionOut", "topoOut", "worldIn", "topoIn"].forEach(function (k) {
        if (typeof savedTh[k] === "number" && savedTh[k] > 0) LEVEL[k] = savedTh[k];
      });
    }
  } catch (e) {}

  function worldInThreshold() {
    return LEVEL.worldIn;
  }

  function scheduleLevelCheck() {
    clearTimeout(state.levelTimer);
    state.levelTimer = setTimeout(checkLevelThresholds, LEVEL.settle);
  }

  function nearestNodeAt(clientX, clientY, maxScreenDist) {
    var stage = $("mapStage");
    var rect = stage.getBoundingClientRect();
    var lx = (clientX !== undefined ? clientX - rect.left : rect.width / 2);
    var ly = (clientY !== undefined ? clientY - rect.top : rect.height / 2);
    var best = null;
    var bestD = Infinity;
    NODES.forEach(function (n) {
      var cx = state.tx + (n.x + state.originOffsetX + n.w / 2) * state.zoom;
      var cy = state.ty + (n.y + state.originOffsetY + n.h / 2) * state.zoom;
      var d = Math.hypot(cx - lx, cy - ly);
      if (d < bestD) { bestD = d; best = n; }
    });
    if (best && bestD <= (maxScreenDist || Infinity)) return best;
    return null;
  }

  function nearestWorldFieldAt(clientX, clientY, maxScreenDist) {
    if (!window.OOT_WORLD) return null;
    var stage = $("mapStage");
    var rect = stage.getBoundingClientRect();
    var lx = (clientX !== undefined ? clientX - rect.left : rect.width / 2);
    var ly = (clientY !== undefined ? clientY - rect.top : rect.height / 2);
    var best = null;
    var bestD = Infinity;
    window.OOT_WORLD.fields.forEach(function (f) {
      var r = availableRegion(f.id);
      if (!r || !isRegionAvailable(r)) return;
      var cx = worldBase.left + state.worldTx + f.x * worldBase.w * state.worldZoom;
      var cy = worldBase.top + state.worldTy + f.y * worldBase.h * state.worldZoom;
      var d = Math.hypot(cx - lx, cy - ly);
      if (d < bestD) { bestD = d; best = f; }
    });
    if (best && bestD <= (maxScreenDist || Infinity)) return best;
    return null;
  }

  function checkLevelThresholds() {
    if (!state.autoLevel) return;
    if (Date.now() < state.levelLockUntil) return;
    var fx = state.levelFocusX;
    var fy = state.levelFocusY;

    if (state.mode === "region" && state.regionZoom <= LEVEL.regionOut) {
      state.levelLockUntil = Date.now() + LEVEL.lock;
      var fromArea = state.area;
      setMode("topology");
      focusNode(NODES.some(function (n) { return n.id === fromArea; }) ? fromArea : "HyruleField", 0.52);
      return;
    }

    if (state.mode === "topology" && state.zoom <= LEVEL.topoOut) {
      state.levelLockUntil = Date.now() + LEVEL.lock;
      setMode("world");
      return;
    }

    if (state.mode === "topology" && state.zoom >= LEVEL.topoIn) {
      var node = nearestNodeAt(fx, fy, 240);
      if (!node) return;
      state.levelLockUntil = Date.now() + LEVEL.lock;
      openRegion(node.id);
      return;
    }

    if (state.mode === "world" && state.worldZoom >= worldInThreshold()) {
      var field = nearestWorldFieldAt(fx, fy);
      state.levelLockUntil = Date.now() + LEVEL.lock;
      setMode("topology");
      focusNode(field ? field.id : "HyruleField", 1.0);
    }
  }

  // -------------------------------------------------------------
  // 思维导图拓扑网络与连线构建
  // -------------------------------------------------------------
  function buildTopologyBoard() {
    var board = $("mindmapBoard");
    var svg = $("topologySvg");
    var nodesLayer = $("nodesLayer");

    board.innerHTML = "";
    nodesLayer.innerHTML = "";

    // 1. 计算所有节点的包围盒
    var minX = Infinity, maxX = -Infinity;
    var minY = Infinity, maxY = -Infinity;

    NODES.forEach(function (n) {
      if (n.x < minX) minX = n.x;
      if (n.x + n.w > maxX) maxX = n.x + n.w;
      if (n.y < minY) minY = n.y;
      if (n.y + n.h > maxY) maxY = n.y + n.h;
    });

    var padding = 240;
    state.originOffsetX = -minX + padding;
    state.originOffsetY = -minY + padding;
    state.boardW = (maxX - minX) + padding * 2;
    state.boardH = (maxY - minY) + padding * 2;

    board.style.width = state.boardW + "px";
    board.style.height = state.boardH + "px";

    svg.setAttribute("width", state.boardW);
    svg.setAttribute("height", state.boardH);
    svg.setAttribute("viewBox", "0 0 " + state.boardW + " " + state.boardH);

    // 重新把 SVG 和节点层放回 board
    board.appendChild(svg);
    board.appendChild(nodesLayer);

    // 2. 渲染各区域与迷宫节点卡片
    var nodeById = {};
    NODES.forEach(function (node) {
      nodeById[node.id] = node;

      var nodeLeft = node.x + state.originOffsetX;
      var nodeTop = node.y + state.originOffsetY;

      var card = document.createElement("div");
      card.className = "node-card type-" + node.type;
      card.id = "node-" + node.id;
      card.style.left = nodeLeft + "px";
      card.style.top = nodeTop + "px";
      card.style.width = node.w + "px";
      card.style.height = node.h + "px";

      // 顶部黑底胶囊标签
      var header = document.createElement("div");
      header.className = "node-header";
      header.id = "header-" + node.id;

      var badgeType = document.createElement("span");
      badgeType.className = "node-badge-type";
      badgeType.textContent = node.type === "dungeon" ? (state.lang === "zh" ? "神殿" : "DUNGEON") : (state.lang === "zh" ? "区域" : "FIELD");

      var titleText = document.createElement("span");
      titleText.className = "node-title-txt";
      titleText.textContent = state.lang === "zh" ? node.zh : node.en;

      header.appendChild(badgeType);
      header.appendChild(titleText);
      card.appendChild(header);

      // 区域手绘地图底图
      var img = document.createElement("img");
      img.className = "node-map-img";
      img.id = "img-" + node.id;
      img.alt = node.en;
      img.draggable = false;
      img.decoding = "async";
      var mapSrc = (state.era === "Adult" && node.adultMap) ? node.adultMap : (node.childMap || node.adultMap);
      img.src = mapSrc;
      card.appendChild(img);

      // 节点内部点位层（严格对齐 object-fit: contain 后的底图实际像素矩形）
      var initRect = getNodeImageRect(node, null);
      var pinsBox = document.createElement("div");
      pinsBox.className = "node-pins";
      pinsBox.id = "pins-" + node.id;
      applyOverlayRect(pinsBox, initRect);
      card.appendChild(pinsBox);

      // 节点内部真实出入口传送门地标层 (Gateways Layer)
      var gatewaysBox = document.createElement("div");
      gatewaysBox.className = "node-gateways";
      gatewaysBox.id = "gateways-" + node.id;
      applyOverlayRect(gatewaysBox, initRect);

      img.addEventListener("load", function () {
        var r = getNodeImageRect(node, img);
        applyOverlayRect(pinsBox, r);
        applyOverlayRect(gatewaysBox, r);
      });
      if (node.gateways && node.gateways.length > 0) {
        node.gateways.forEach(function (gw) {
          var gwEl = document.createElement("div");
          gwEl.className = "map-gateway";
          gwEl.id = "gw-" + gw.id;
          gwEl.style.left = gw.x + "%";
          gwEl.style.top = gw.y + "%";
          var targetNodeObj = NODES.find(function (n) { return n.id === gw.target; });
          var targetName = targetNodeObj ? (state.lang === "zh" ? targetNodeObj.zh : targetNodeObj.en) : gw.target;
          var gwName = state.lang === "zh" ? gw.zh : gw.en;
          gwEl.title = gwName + " ➜ " + targetName;

          gwEl.innerHTML = '<span class="gateway-icon">🚪</span><span class="gateway-label">' + gwName + '</span>';

          // 悬停高亮连线与两端传送门
          gwEl.addEventListener("mouseenter", function (e) {
            e.stopPropagation();
            highlightGatewayPortal(gw, node.id, true);
          });
          gwEl.addEventListener("mouseleave", function (e) {
            e.stopPropagation();
            highlightGatewayPortal(gw, node.id, false);
          });

          // 点击平滑飞跃到目标区域
          gwEl.addEventListener("click", function (e) {
            e.stopPropagation();
            jumpToGatewayTarget(gw);
          });

          gatewaysBox.appendChild(gwEl);
        });
      }
      card.appendChild(gatewaysBox);

      // 拓扑图保持单张总览，迷宫楼层切换专注留在区域地图 (#regionFloorBar)

      // 悬停高亮与相连连线
      card.addEventListener("mouseenter", function () {
        highlightEdges(node.id, true);
      });
      card.addEventListener("mouseleave", function () {
        highlightEdges(node.id, false);
      });

      // 点击节点居中放大 (仅单击有效，拖动松手不触发)
      card.addEventListener("click", function (e) {
        if (state.dragMoved) return;
        if (e.target.closest(".map-pin") || e.target.closest(".map-gateway") || e.target.closest(".floor-btn")) return;
        focusNode(node.id, 1.25);
      });

      // 双击节点卡片：进入该区域单图
      card.addEventListener("dblclick", function (e) {
        if (e.target.closest(".map-pin") || e.target.closest(".map-gateway") || e.target.closest(".floor-btn")) return;
        e.stopPropagation();
        openRegion(node.id);
      });

      nodesLayer.appendChild(card);
    });

    // 3. 渲染 SVG 连接线 (标准思维导图平滑树状连线与出入口路标)
    svg.innerHTML = "";
    EDGES.forEach(function (edge, idx) {
      var n1 = nodeById[edge.from];
      var n2 = nodeById[edge.to];
      if (!n1 || !n2) return;

      var b1 = {
        left: n1.x + state.originOffsetX,
        right: n1.x + state.originOffsetX + n1.w,
        top: n1.y + state.originOffsetY,
        bottom: n1.y + state.originOffsetY + n1.h,
        cx: n1.x + state.originOffsetX + n1.w / 2,
        cy: n1.y + state.originOffsetY + n1.h / 2
      };
      var b2 = {
        left: n2.x + state.originOffsetX,
        right: n2.x + state.originOffsetX + n2.w,
        top: n2.y + state.originOffsetY,
        bottom: n2.y + state.originOffsetY + n2.h,
        cx: n2.x + state.originOffsetX + n2.w / 2,
        cy: n2.y + state.originOffsetY + n2.h / 2
      };

      var p1x, p1y, p2x, p2y, c1x, c1y, c2x, c2y;
      var gw1 = null;
      var gw2 = null;

      if (n1.gateways && n1.gateways.length > 0) {
        gw1 = n1.gateways.find(function (g) { return g.id === edge.fromGw || g.target === edge.to; });
      }
      if (n2.gateways && n2.gateways.length > 0) {
        gw2 = n2.gateways.find(function (g) { return g.id === edge.toGw || g.target === edge.from; });
      }

      var r1 = getNodeImageRect(n1, null);
      var r2 = getNodeImageRect(n2, null);

      if (gw1) {
        p1x = b1.left + r1.ox + r1.rw * (gw1.x / 100);
        p1y = b1.top + r1.oy + r1.rh * (gw1.y / 100);
      } else {
        p1x = b1.cx;
        p1y = b1.cy;
      }

      if (gw2) {
        p2x = b2.left + r2.ox + r2.rw * (gw2.x / 100);
        p2y = b2.top + r2.oy + r2.rh * (gw2.y / 100);
      } else {
        p2x = b2.cx;
        p2y = b2.cy;
      }

      var dx = p2x - p1x;
      var dy = p2y - p1y;
      var dist = Math.hypot(dx, dy) || 1;

      if (edge.type === "shortcut") {
        // 近道快捷连线采用柔和大弧线
        var normX = -dy / dist;
        var normY = dx / dist;
        var arcOffset = Math.min(180, dist * 0.22);
        c1x = p1x + dx * 0.35 + normX * arcOffset;
        c1y = p1y + dy * 0.35 + normY * arcOffset;
        c2x = p1x + dx * 0.65 + normX * arcOffset;
        c2y = p1y + dy * 0.65 + normY * arcOffset;
      } else if (Math.abs(dy) > Math.abs(dx) * 0.75) {
        // 主垂直走向 (例如从科奇里上层树洞往北连入迷失森林入口)
        c1x = p1x;
        c1y = p1y + dy * 0.5;
        c2x = p2x;
        c2y = p2y - dy * 0.5;
      } else {
        // 主水平走向 (例如从科奇里东部树干进入德库树)
        c1x = p1x + dx * 0.5;
        c1y = p1y;
        c2x = p2x - dx * 0.5;
        c2y = p2y;
      }

      var d = "M " + p1x + " " + p1y + " C " + c1x + " " + c1y + ", " + c2x + " " + c2y + ", " + p2x + " " + p2y;

      // 宽热区透明连线 (极大改善细线条悬停与点击命中率)
      var hitPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
      hitPath.setAttribute("d", d);
      hitPath.setAttribute("class", "edge-hitarea");
      svg.appendChild(hitPath);

      var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", d);
      path.setAttribute("class", "edge-path " + edge.type);
      path.setAttribute("id", "edge-" + edge.from + "-" + edge.to);
      svg.appendChild(path);

      // 连线中心路标文字
      var midX = (p1x + p2x) / 2;
      var midY = (p1y + p2y) / 2;
      if (edge.type === "shortcut") {
        midX = (c1x + c2x) / 2;
        midY = (c1y + c2y) / 2;
      }
      var labelTxt = state.lang === "zh" ? edge.zh : edge.en;

      var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", "edge-label-group");
      g.setAttribute("id", "edge-label-" + edge.from + "-" + edge.to);

      var textW = labelTxt.length * 13 + 22;
      var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", midX - textW / 2);
      rect.setAttribute("y", midY - 12);
      rect.setAttribute("width", textW);
      rect.setAttribute("height", 24);
      rect.setAttribute("class", "edge-label-bg");

      var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", midX);
      text.setAttribute("y", midY);
      text.setAttribute("class", "edge-label");
      text.textContent = labelTxt;

      g.appendChild(rect);
      g.appendChild(text);
      svg.appendChild(g);

      // 悬停提示与点击双向跳转事件
      function handleEdgeHover(e) {
        path.classList.add("highlight");
        showEdgeTooltip(edge, n1, n2, e);
      }
      function handleEdgeLeave() {
        path.classList.remove("highlight");
        hideEdgeTooltip();
      }
      function handleEdgeClick(e) {
        e.stopPropagation();
        toggleEdgeJump(edge);
      }

      hitPath.addEventListener("mouseenter", handleEdgeHover);
      hitPath.addEventListener("mousemove", handleEdgeHover);
      hitPath.addEventListener("mouseleave", handleEdgeLeave);
      hitPath.addEventListener("click", handleEdgeClick);

      path.addEventListener("mouseenter", handleEdgeHover);
      path.addEventListener("mousemove", handleEdgeHover);
      path.addEventListener("mouseleave", handleEdgeLeave);
      path.addEventListener("click", handleEdgeClick);

      g.addEventListener("mouseenter", handleEdgeHover);
      g.addEventListener("mousemove", handleEdgeHover);
      g.addEventListener("mouseleave", handleEdgeLeave);
      g.addEventListener("click", handleEdgeClick);
    });

    // 初始居中聚焦在海拉鲁平原核心 hub，视野舒适，纵览周边相连森林与城镇
    setTimeout(function () {
      if (state.mode === "topology") focusNode("HyruleField", 0.52);
    }, 60);
    renderAllPins();
    updateCategoriesCount();
    updateProgress();
  }

  // -------------------------------------------------------------
  // 出入口与近道悬浮说明框与双向跳转
  // -------------------------------------------------------------
  function showEdgeTooltip(edge, n1, n2, e) {
    var tt = $("edgeTooltip");
    if (!tt) return;

    var badge = $("edgeTtBadge");
    var title = $("edgeTtTitle");
    var route = $("edgeTtRoute");
    var desc = $("edgeTtDesc");

    badge.className = "edge-tt-badge " + edge.type;
    badge.textContent = edge.type === "shortcut" ? "🌀 隐藏近道" : (edge.type === "dungeon" ? "⛩️ 神殿出入口" : "🚪 区域通路");
    title.textContent = state.lang === "zh" ? edge.zh : edge.en;
    route.textContent = (state.lang === "zh" ? n1.zh : n1.en) + " ⟷ " + (state.lang === "zh" ? n2.zh : n2.en);
    desc.textContent = state.lang === "zh" ? (edge.descZh || "游戏内直接相通的出入口路径") : (edge.descEn || "Direct in-game passage between areas");

    tt.hidden = false;
    var stageRect = $("mapStage").getBoundingClientRect();
    var tipX = e.clientX - stageRect.left;
    var tipY = e.clientY - stageRect.top;
    tt.style.left = tipX + "px";
    tt.style.top = (tipY - 14) + "px";
  }

  function hideEdgeTooltip() {
    var tt = $("edgeTooltip");
    if (tt) tt.hidden = true;
  }

  // 沿连线在两端地图之间来回跳转 (双向切换)
  function toggleEdgeJump(edge) {
    var n1 = NODES.find(function (n) { return n.id === edge.from; });
    var n2 = NODES.find(function (n) { return n.id === edge.to; });
    if (!n1 || !n2) return;

    var stage = $("mapStage");
    var sw = stage.clientWidth || 1200;
    var sh = stage.clientHeight || 800;

    var camWorldX = (sw / 2 - state.tx) / state.zoom;
    var camWorldY = (sh / 2 - state.ty) / state.zoom;

    var c1x = n1.x + state.originOffsetX + n1.w / 2;
    var c1y = n1.y + state.originOffsetY + n1.h / 2;
    var c2x = n2.x + state.originOffsetX + n2.w / 2;
    var c2y = n2.y + state.originOffsetY + n2.h / 2;

    var dist1 = Math.hypot(camWorldX - c1x, camWorldY - c1y);
    var dist2 = Math.hypot(camWorldX - c2x, camWorldY - c2y);

    // 离哪端近就跳转到另一端，实现点击来回自如切换
    var targetNode = (dist1 < dist2) ? n2 : n1;
    focusNode(targetNode.id, Math.max(state.zoom, 0.72));

    var card = $("node-" + targetNode.id);
    if (card) {
      card.style.transition = "box-shadow 0.25s, transform 0.25s";
      card.style.boxShadow = "0 0 35px #38bdf8, 0 0 15px #38bdf8";
      setTimeout(function () {
        card.style.boxShadow = "";
      }, 1200);
    }
  }

  // 高亮特定传送门出入口及连线
  function highlightGatewayPortal(gw, sourceNodeId, enable) {
    var gwEl = $("gw-" + gw.id);
    if (gwEl) {
      if (enable) gwEl.classList.add("highlight");
      else gwEl.classList.remove("highlight");
    }

    // 寻找目标节点对应出入口
    var targetNode = NODES.find(function (n) { return n.id === gw.target; });
    if (targetNode && targetNode.gateways) {
      var oppositeGw = targetNode.gateways.find(function (g) { return g.target === sourceNodeId; });
      if (oppositeGw) {
        var oppEl = $("gw-" + oppositeGw.id);
        if (oppEl) {
          if (enable) oppEl.classList.add("highlight");
          else oppEl.classList.remove("highlight");
        }
      }
    }

    // 高亮相连连线
    EDGES.forEach(function (e) {
      if ((e.from === sourceNodeId && e.to === gw.target) || (e.from === gw.target && e.to === sourceNodeId)) {
        var path = $("edge-" + e.from + "-" + e.to);
        if (path) {
          if (enable) path.classList.add("highlight");
          else path.classList.remove("highlight");
        }
      }
    });
  }

  // 点击传送门直接平滑飞跃至目标地图
  function jumpToGatewayTarget(gw) {
    if (!gw.target) return;
    focusNode(gw.target, Math.max(state.zoom, 1.0));

    var targetCard = $("node-" + gw.target);
    if (targetCard) {
      targetCard.style.transition = "box-shadow 0.25s, transform 0.25s";
      targetCard.style.boxShadow = "0 0 35px #38bdf8, 0 0 15px #38bdf8";
      setTimeout(function () {
        targetCard.style.boxShadow = "";
      }, 1200);
    }

    // 目标端传送门呼吸动画
    var targetNode = NODES.find(function (n) { return n.id === gw.target; });
    if (targetNode && targetNode.gateways) {
      var oppGw = targetNode.gateways.find(function (g) { return g.target === gw.target; });
      if (!oppGw && targetNode.gateways.length > 0) oppGw = targetNode.gateways[0];
      if (oppGw) {
        var oppEl = $("gw-" + oppGw.id);
        if (oppEl) {
          oppEl.classList.add("highlight");
          setTimeout(function () { oppEl.classList.remove("highlight"); }, 1800);
        }
      }
    }
  }

  // 高亮相连的连线
  function highlightEdges(nodeId, enable) {
    EDGES.forEach(function (e) {
      if (e.from === nodeId || e.to === nodeId) {
        var path = $("edge-" + e.from + "-" + e.to);
        if (path) {
          if (enable) path.classList.add("highlight");
          else path.classList.remove("highlight");
        }
      }
    });
  }

  // 更新时代贴图
  function updateEraTextures() {
    NODES.forEach(function (node) {
      var img = $("img-" + node.id);
      if (img) {
        var mapSrc = (state.era === "Adult" && node.adultMap) ? node.adultMap : (node.childMap || node.adultMap);
        img.src = mapSrc;
      }
    });
  }

  // 切换地下城神殿楼层
  function switchDungeonFloor(node, floor) {
    var img = $("img-" + node.id);
    if (!img) return;

    if (floor === "All") {
      img.src = (state.era === "Adult" && node.adultMap) ? node.adultMap : (node.childMap || node.adultMap);
    } else {
      var dMaps = TOPOLOGY.dungeonFloorMaps;
      if (dMaps && dMaps[node.id] && dMaps[node.id][floor]) {
        img.src = dMaps[node.id][floor];
      }
    }
    renderAllPins();
  }

  // -------------------------------------------------------------
  // 点位渲染与交互
  // -------------------------------------------------------------
  // 画布图标基准尺寸：桌面 20 / 手机 18（UI 规范：命中区仍由 padding 撑到 32）
  function pinIconSize() {
    return (window.innerWidth <= 900) ? 30 : 34;
  }

  function isPinVisible(pin) {
    if (state.era !== "All") {
      if (pin.era !== "Both" && pin.era !== state.era) return false;
    }
    if (!state.activeCats.has(pin.cat)) return false;
    if (state.hideDone && state.donePins[pin.id]) return false;
    return true;
  }

  function renderAllPins() {
    NODES.forEach(function (node) {
      var box = $("pins-" + node.id);
      if (box) box.innerHTML = "";
    });

    PINS.forEach(function (pin) {
      if (!isPinVisible(pin)) return;

      // 神殿楼层过滤：若该神殿选定了具体楼层，非本楼层的点位暂时隐藏
      var hostNode = NODES.find(function (n) { return n.id === pin.area || n.id === pin.map; });
      if (hostNode && hostNode.type === "dungeon" && hostNode.currentFloor && hostNode.currentFloor !== "All") {
        if (pin.area !== hostNode.currentFloor) return;
      }

      var targetBox = $("pins-" + pin.area);
      if (!targetBox) {
        // 如果是迷宫点位直接挂在对应迷宫节点上
        if (pin.map && pin.map !== "hyrule") {
          targetBox = $("pins-" + pin.map);
        }
      }
      if (!targetBox) return;

      var el = document.createElement("div");
      el.className = "map-pin" +
                     (state.donePins[pin.id] ? " done" : "") +
                     (state.selectedPinId === pin.id ? " selected" : "");
      el.id = "pin-" + pin.id;
      el.style.left = pin.x + "%";
      el.style.top = pin.y + "%";

      el.innerHTML = ICONS.html(pin.cat, pinIconSize(), !!state.donePins[pin.id]);

      // 点位拖拽微调支持
      el.addEventListener("mousedown", function (e) {
        if (calState.active) {
          e.stopPropagation();
          calState.draggingPin = pin;
          calState.targetBox = targetBox;
        }
      });

      el.addEventListener("click", function (e) {
        e.stopPropagation();
        if (!calState.active) {
          selectPin(pin);
        }
      });

      targetBox.appendChild(el);
    });

    if (state.mode === "region") renderRegionPins();
    renderWorldPins();
  }

  function selectPin(pin) {
    state.selectedPinId = pin.id;

    var prev = document.querySelectorAll(".map-pin.selected");
    prev.forEach(function (el) { el.classList.remove("selected"); });
    var cur = $("pin-" + pin.id);
    if (cur) cur.classList.add("selected");
    var rcur = $("rpin-" + pin.id);
    if (rcur) rcur.classList.add("selected");

    var card = $("detailCard");
    $("cardIconWrap").innerHTML = ICONS.html(pin.cat, 26, !!state.donePins[pin.id]);

    var catObj = CATS.find(function (c) { return c.id === pin.cat; });
    $("cardCatTag").textContent = catObj ? (state.lang === "zh" ? catObj.zh : catObj.en) : pin.cat;
    var catColor = (catObj && catObj.badge) || ICONS.color(pin.cat);
    $("cardCatTag").style.background = catColor + "25";
    $("cardCatTag").style.color = catColor;

    var eraTxt = pin.era === "Both" ? (state.lang === "zh" ? "全时代" : "All Eras") : (state.lang === "zh" ? (pin.era === "Child" ? "童年期" : "成年期") : pin.era);
    $("cardEraTag").textContent = eraTxt;

    var timeTxt = pin.time === "Night" ? (state.lang === "zh" ? "夜晚限定" : "Night") : (pin.time === "Day" ? (state.lang === "zh" ? "白天限定" : "Day") : (state.lang === "zh" ? "昼夜均可" : "Any Time"));
    $("cardTimeTag").textContent = timeTxt;

    $("cardTitle").textContent = state.lang === "zh" ? pin.zh : pin.en;

    // 位置：区域名 + 楼层 + 世界坐标，替代原来只显示 area / 楼层
    var hostId = (pin.map && pin.map !== "hyrule") ? pin.map : pin.area;
    var hostRegion = REGIONS.find(function (r) { return r.id === hostId; });
    var regionName = hostRegion ? (state.lang === "zh" ? hostRegion.zh : hostRegion.en) : hostId;
    var floorTxt = (pin.map && pin.map !== "hyrule" && pin.area) ? pin.area : "";
    $("cardArea").textContent = "📍 " + regionName + (floorTxt ? " · " + floorTxt : "");
    $("cardLocRow").hidden = !floorTxt;
    $("cardLocVal").textContent = floorTxt ? ((state.lang === "zh" ? "楼层 " : "Floor ") + floorTxt) : "";

    // 怎么拿：优先结构化 howto，没写则回落到官方点位说明
    var hasHowto = !!(pin.howto || pin.howtoEn);
    var howTxt = state.lang === "zh" ? (pin.howto || pin.descZh || pin.zh) : (pin.howtoEn || pin.descEn || pin.en);
    $("cardHowVal").textContent = howTxt;

    if (pin.req) {
      $("cardReqRow").hidden = false;
      $("cardReqVal").textContent = pin.req;
    } else {
      $("cardReqRow").hidden = true;
    }

    var rewardTxt = state.lang === "zh" ? (pin.reward || "") : (pin.rewardEn || "");
    $("cardRewardRow").hidden = !rewardTxt;
    if (rewardTxt) $("cardRewardVal").textContent = rewardTxt;

    var noteTxt = state.lang === "zh" ? (pin.note || "") : (pin.noteEn || "");
    $("cardNoteRow").hidden = !noteTxt;
    if (noteTxt) $("cardNoteVal").textContent = noteTxt;

    var descTxt = state.lang === "zh" ? (pin.descZh || "") : (pin.descEn || "");
    var showDesc = !!descTxt && hasHowto;
    $("cardDesc").hidden = !showDesc;
    $("cardDesc").textContent = showDesc ? descTxt : "";

    var world = pin.world || [];
    $("cardCoordVal").textContent = world.length >= 3
      ? "X " + world[0] + " · Y " + world[1] + " · Z " + world[2]
      : (state.lang === "zh" ? "地图定位 " + pin.x + "% · " + pin.y + "%" : "Map " + pin.x + "% / " + pin.y + "%");

    var chk = $("cardDoneChk");
    chk.checked = !!state.donePins[pin.id];
    chk.onchange = function () {
      if (chk.checked) {
        state.donePins[pin.id] = true;
      } else {
        delete state.donePins[pin.id];
      }
      saveStorage();
      renderAllPins();
      renderRegionList();
      updateCategoriesCount();
      updateProgress();
    };

    card.hidden = false;
    positionDetailCard(card, (state.mode === "region" ? rcur : cur) || rcur || cur);
    updateUrl(pin.id);
  }

  function positionDetailCard(card, anchorEl) {
    if (!card) return;
    var vw = window.innerWidth, vh = window.innerHeight;
    if (vw <= 900 || !anchorEl) {
      card.style.left = "";
      card.style.top = "";
      card.style.right = "";
      return;
    }
    var ar = anchorEl.getBoundingClientRect();
    var ax = ar.left + ar.width / 2;
    var ay = ar.top + ar.height / 2;
    var cw = card.offsetWidth || 360;
    var ch = card.offsetHeight || 280;
    var sb = $("sidebar");
    var minL = (sb && !sb.classList.contains("collapsed")) ? (sb.offsetWidth + 14) : 14;
    var maxL = vw - cw - 14;
    var minT = 14;
    var maxT = vh - ch - 14;
    var pad = 28;
    // 依次探测：右侧 → 左侧 → 下方 → 上方
    var candidates = [
      { l: ax + pad, t: ay - ch * 0.35 },
      { l: ax - pad - cw, t: ay - ch * 0.35 },
      { l: ax - cw / 2, t: ay + pad },
      { l: ax - cw / 2, t: ay - pad - ch }
    ];
    var chosen = null;
    for (var i = 0; i < candidates.length; i++) {
      var c = candidates[i];
      if (c.l >= minL && c.l <= maxL && c.t >= minT && c.t <= maxT) {
        chosen = c;
        break;
      }
    }
    if (!chosen) {
      chosen = {
        l: Math.max(minL, Math.min(maxL, ax + pad <= maxL ? ax + pad : ax - pad - cw)),
        t: Math.max(minT, Math.min(maxT, ay - ch * 0.35))
      };
    }
    card.style.right = "auto";
    card.style.left = Math.round(chosen.l) + "px";
    card.style.top = Math.round(chosen.t) + "px";
  }

  function closeDetailCard() {
    $("detailCard").hidden = true;
    state.selectedPinId = null;
    document.querySelectorAll(".map-pin.selected").forEach(function (el) { el.classList.remove("selected"); });
  }

  // -------------------------------------------------------------
  // 分类统计与全收集进度管理 (GamerGuides 核心体验)
  // -------------------------------------------------------------
  function updateCategoriesCount() {
    renderCategoriesSidebar();
  }

  var exploreTab = "region";

  function renderExplorePanel() {
    var panel = $("explorePanel");
    var grid = $("exploreGrid");
    if (!panel || !grid || panel.hidden) return;
    grid.innerHTML = "";

    var items = [];
    if (exploreTab === "region") {
      REGIONS.forEach(function (r) {
        if (!isRegionAvailable(r)) return;
        var total = 0, done = 0;
        PINS.forEach(function (p) {
          if (state.era !== "All" && p.era !== "Both" && p.era !== state.era) return;
          var host = (p.map && p.map !== "hyrule") ? p.map : p.area;
          if (host !== r.id) return;
          total++;
          if (state.donePins[p.id]) done++;
        });
        if (!total) return;
        items.push({
          id: r.id,
          label: state.lang === "zh" ? r.zh : (r.en || r.id),
          done: done,
          total: total,
          isRegion: true
        });
      });
    } else {
      CATS.forEach(function (c) {
        var total = 0, done = 0;
        PINS.forEach(function (p) {
          if (state.era !== "All" && p.era !== "Both" && p.era !== state.era) return;
          if (p.cat !== c.id) return;
          total++;
          if (state.donePins[p.id]) done++;
        });
        if (!total) return;
        items.push({
          id: c.id,
          label: state.lang === "zh" ? (c.short || c.zh) : (c.en || c.id),
          done: done,
          total: total,
          badge: c.badge,
          isRegion: false
        });
      });
    }

    items.forEach(function (it) {
      var pct = it.total > 0 ? Math.round((it.done / it.total) * 100) : 0;
      var card = document.createElement("button");
      card.type = "button";
      card.className = "explore-card" + (pct === 100 ? " full" : "");
      card.title = it.label + " (" + it.done + "/" + it.total + ")";
      card.innerHTML =
        '<div class="ec-top">' +
          (it.badge ? '<span class="ec-dot" style="background:' + it.badge + '"></span>' : '') +
          '<span class="ec-name">' + it.label + '</span>' +
          '<span class="ec-num">' + it.done + '/' + it.total + '</span>' +
        '</div>' +
        '<div class="ec-bar"><i style="width:' + pct + '%"></i></div>';
      card.addEventListener("click", function () {
        if (it.isRegion) {
          openRegion(it.id);
          if (window.innerWidth <= 900) {
            $("sidebar").classList.add("collapsed");
            document.body.classList.add("side-collapsed");
          }
        } else {
          state.activeCats.add(it.id);
          renderCategoriesSidebar();
          renderAllPins();
        }
      });
      grid.appendChild(card);
    });
  }

  function updateProgress() {
    var total = 0;
    var completed = 0;

    PINS.forEach(function (p) {
      if (state.era !== "All" && p.era !== "Both" && p.era !== state.era) return;
      total++;
      if (state.donePins[p.id]) completed++;
    });

    var pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    $("progNum").textContent = completed + " / " + total;
    $("progPct").textContent = pct + "%";
    $("progBar").style.width = pct + "%";
    renderExplorePanel();
  }

  function renderCategoriesSidebar() {
    var list = $("catList");
    if (!list) return;
    list.innerHTML = "";

    var titleEl = $("catPanelTitle");
    var subEl = $("catPanelSub");
    var r = (state.mode === "region") ? currentRegion() : null;
    if (titleEl) {
      titleEl.textContent = r
        ? (state.lang === "zh" ? "本区图标" : "Area Icons")
        : (state.lang === "zh" ? "全图图标" : "All Icons");
    }
    if (subEl) {
      subEl.textContent = r
        ? (state.lang === "zh" ? r.zh : r.en)
        : (state.lang === "zh" ? "海拉鲁全境" : "Hyrule");
    }

    var stats = {};
    PINS.forEach(function (p) {
      if (state.era !== "All" && p.era !== "Both" && p.era !== state.era) return;
      if (r && !pinBelongsToRegion(p, r)) return;
      if (!stats[p.cat]) stats[p.cat] = { total: 0, done: 0 };
      stats[p.cat].total++;
      if (state.donePins[p.id]) stats[p.cat].done++;
    });

    var visibleCats = CATS.filter(function (c) {
      return stats[c.id] && stats[c.id].total > 0;
    });

    if (!visibleCats.length) {
      list.innerHTML = '<div class="cat-empty">' +
        (state.lang === "zh" ? "当前时代暂无图标" : "No icons in this era") +
        "</div>";
      return;
    }

    visibleCats.forEach(function (cat) {
      var st = stats[cat.id];
      var isActive = state.activeCats.has(cat.id);
      var item = document.createElement("button");
      item.type = "button";
      item.className = "cat-item" + (isActive ? " active" : "") + (st.done > 0 ? " has-done" : "");
      item.title = (state.lang === "zh" ? cat.zh : cat.en) + " (" + st.done + "/" + st.total + ")";

      var iconSlot = document.createElement("div");
      iconSlot.className = "cat-icon-slot";
      iconSlot.innerHTML = ICONS.html(cat.id, 16);

      var name = document.createElement("span");
      name.className = "cat-name";
      name.textContent = state.lang === "zh" ? cat.short : cat.en;

      var badge = document.createElement("span");
      badge.className = "cat-badge";
      badge.textContent = st.done + "/" + st.total;

      item.appendChild(iconSlot);
      item.appendChild(name);
      item.appendChild(badge);
      item.addEventListener("click", function () {
        if (state.activeCats.has(cat.id)) {
          state.activeCats.delete(cat.id);
          item.classList.remove("active");
        } else {
          state.activeCats.add(cat.id);
          item.classList.add("active");
        }
        renderAllPins();
      });
      list.appendChild(item);
    });
  }

  function renderJumpChips() {
    var chips = $("jumpChips");
    chips.innerHTML = "";

    NODES.forEach(function (node) {
      var chip = document.createElement("button");
      chip.className = "jump-chip";
      chip.textContent = state.lang === "zh" ? node.zh : node.en;
      chip.addEventListener("click", function () {
        focusNode(node.id, 1.25);
      });
      chips.appendChild(chip);
    });
  }

  // -------------------------------------------------------------
  // 搜索功能实现
  // -------------------------------------------------------------
  function bindSearch() {
    var input = $("searchInput");
    var resBox = $("searchResults");

    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      if (!q) {
        resBox.hidden = true;
        resBox.innerHTML = "";
        return;
      }

      var regionMatches = REGIONS.filter(function (r) {
        if (!isRegionAvailable(r)) return false;
        return (r.zh && r.zh.toLowerCase().indexOf(q) !== -1) ||
               (r.en && r.en.toLowerCase().indexOf(q) !== -1);
      }).slice(0, 5);

      var matches = PINS.filter(function (p) {
        if (state.era !== "All" && p.era !== "Both" && p.era !== state.era) return false;
        return (p.zh && p.zh.toLowerCase().indexOf(q) !== -1) ||
               (p.en && p.en.toLowerCase().indexOf(q) !== -1) ||
               (p.descZh && p.descZh.toLowerCase().indexOf(q) !== -1) ||
               (p.area && p.area.toLowerCase().indexOf(q) !== -1) ||
               (p.req && p.req.toLowerCase().indexOf(q) !== -1);
      }).slice(0, 12);

      if (!matches.length && !regionMatches.length) {
        resBox.innerHTML = '<div style="padding:10px;font-size:12px;color:#7d725d;text-align:center;">未找到匹配点位</div>';
        resBox.hidden = false;
        return;
      }

      resBox.innerHTML = "";
      regionMatches.forEach(function (r) {
        var row = document.createElement("div");
        row.className = "search-item";
        row.innerHTML = '<div style="flex:0 0 24px;color:#eab308;text-align:center;">▣</div>' +
                        '<div class="search-item-info">' +
                        '  <span class="search-item-title">' + (state.lang === "zh" ? r.zh : r.en) + '</span>' +
                        '  <span class="search-item-area">区域 · ' + regionPinsForEra(r).length + ' 点</span>' +
                        '</div>';
        row.addEventListener("click", function () {
          resBox.hidden = true;
          input.value = "";
          openRegion(r.id);
        });
        resBox.appendChild(row);
      });
      matches.forEach(function (m) {
        var row = document.createElement("div");
        row.className = "search-item";
        row.innerHTML = '<div style="flex:0 0 24px;">' + ICONS.html(m.cat, 18) + '</div>' +
                        '<div class="search-item-info">' +
                        '  <span class="search-item-title">' + (state.lang === "zh" ? m.zh : m.en) + '</span>' +
                        '  <span class="search-item-area">' + (m.area || m.map) + '</span>' +
                        '</div>';
        row.addEventListener("click", function () {
          resBox.hidden = true;
          input.value = "";

          var hostId = (m.map && m.map !== "hyrule") ? m.map : m.area;
          var floor = (m.map && m.map !== "hyrule") ? (m.area === "0F" ? "1F" : m.area) : "All";
          if (state.mode === "region" || state.mode === "world") {
            openRegion(hostId, { floor: floor });
            setTimeout(function () { selectPin(m); }, 180);
          } else {
            focusNode(hostId, 1.35);
            setTimeout(function () { selectPin(m); }, 200);
          }
        });
        resBox.appendChild(row);
      });
      resBox.hidden = false;
    });

    document.addEventListener("click", function (e) {
      if (!e.target.closest(".search-box")) {
        resBox.hidden = true;
      }
    });
  }

  // -------------------------------------------------------------
  // 顶栏与交互绑定
  // -------------------------------------------------------------
  function bindUI() {
    function refreshMapAfterShell() {
      setTimeout(function () {
        if (state.mode === "region") { layoutRegionBase(); applyRegionCam(); }
        else if (state.mode === "topology") fitCamera();
        else if (state.mode === "world") applyWorldCam();
      }, 300);
    }

    $("sidebarToggle").addEventListener("click", function () {
      $("sidebar").classList.add("collapsed");
      document.body.classList.add("side-collapsed");
      refreshMapAfterShell();
    });
    $("sidebarOpen").addEventListener("click", function () {
      $("sidebar").classList.remove("collapsed");
      document.body.classList.remove("side-collapsed");
      refreshMapAfterShell();
    });

    // 视图 tabs：区域 / 拓扑 / 全图
    document.querySelectorAll("#viewTabs .view-tab").forEach(function (btn) {
      btn.addEventListener("click", function () {
        setMode(btn.getAttribute("data-view"));
      });
    });

    // 左下角设置面板
    var settingsBtn = $("settingsBtn");
    var settingsPanel = $("settingsPanel");
    var settingsClose = $("settingsClose");
    if (settingsBtn && settingsPanel) {
      settingsBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        settingsPanel.hidden = !settingsPanel.hidden;
      });
      settingsPanel.addEventListener("click", function (e) { e.stopPropagation(); });
      document.addEventListener("click", function () {
        if (!settingsPanel.hidden) settingsPanel.hidden = true;
      });
      if (settingsClose) settingsClose.addEventListener("click", function () { settingsPanel.hidden = true; });
    }

    // 本区图标面板折叠
    var catPanelToggle = $("catPanelToggle");
    if (catPanelToggle) {
      catPanelToggle.addEventListener("click", function () {
        var list = $("catList");
        var caret = $("catCaret");
        var isHidden = list.hidden;
        list.hidden = !isHidden;
        catPanelToggle.setAttribute("aria-expanded", isHidden ? "true" : "false");
        if (caret) caret.textContent = isHidden ? "▾" : "▴";
      });
    }

    // 区域列表折叠（TOTKmap 式收起/展开）
    var regionToggle = $("regionToggle");
    if (regionToggle) {
      regionToggle.addEventListener("click", function () {
        var body = $("regionBody");
        var hidden = body.hidden;
        body.hidden = !hidden;
        this.textContent = hidden ? "收起" : "展开";
      });
    }

    var eraBtns = document.querySelectorAll("#eraSeg .era-btn");
    eraBtns.forEach(function (btn) {
      if (btn.getAttribute("data-era") === state.era) btn.classList.add("on");
      else btn.classList.remove("on");

      btn.addEventListener("click", function () {
        eraBtns.forEach(function (b) { b.classList.remove("on"); });
        btn.classList.add("on");
        state.era = btn.getAttribute("data-era");
        saveStorage();
        updateEraTextures();
        renderAllPins();
        updateCategoriesCount();
        updateProgress();
        syncRegionForEra();
        updateUrl();
      });
    });

    var navBtn = $("navBtn");
    if (navBtn) {
      navBtn.addEventListener("click", function () {
        var orig = navBtn.textContent;
        navBtn.textContent = state.lang === "zh" ? "即将上线" : "Soon";
        setTimeout(function () { navBtn.textContent = orig; }, 1200);
      });
    }

    var saveSyncBtn = $("saveSyncBtn");
    if (saveSyncBtn) {
      saveSyncBtn.addEventListener("click", function () {
        var orig = saveSyncBtn.textContent;
        saveSyncBtn.textContent = state.lang === "zh" ? "存档同步即将上线" : "Coming soon";
        setTimeout(function () { saveSyncBtn.textContent = orig; }, 1200);
      });
    }

    var saveHelpBtn = $("saveHelpBtn");
    if (saveHelpBtn) {
      saveHelpBtn.addEventListener("click", function () {
        if (saveSyncBtn) saveSyncBtn.click();
      });
    }

    // 所有画布点击空白处关闭打开的卡片/面板
    var mapStageEl = $("mapStage");
    if (mapStageEl) {
      mapStageEl.addEventListener("click", function (e) {
        if (state.dragMoved || state.regionDragMoved || state.worldDragMoved) return;
        if (e.target.closest(".detail-card") || e.target.closest(".map-pin") ||
            e.target.closest(".region-gw") || e.target.closest(".world-seal") ||
            e.target.closest(".world-entry") || e.target.closest(".settings-panel") ||
            e.target.closest(".zoom-controls") || e.target.closest("button")) return;
        var dc = $("detailCard");
        if (dc && !dc.hidden) closeDetailCard();
        var sp = $("settingsPanel");
        if (sp && !sp.hidden) sp.hidden = true;
        var ep = $("explorePanel");
        if (ep && !ep.hidden) {
          ep.hidden = true;
          var caret = $("progCaret");
          if (caret) caret.textContent = "▴";
        }
      });
    }

    var hideChk = $("hideDoneChk");
    hideChk.checked = state.hideDone;
    hideChk.addEventListener("change", function () {
      state.hideDone = hideChk.checked;
      saveStorage();
      renderAllPins();
    });

    var autoLevelChk = $("autoLevelChk");
    if (autoLevelChk) {
      autoLevelChk.checked = state.autoLevel;
      autoLevelChk.addEventListener("change", function () {
        state.autoLevel = autoLevelChk.checked;
        try { localStorage.setItem(KEY_AUTO_LEVEL, state.autoLevel ? "1" : "0"); } catch (e) {}
      });
    }

    var langBtn = $("langBtn");
    langBtn.addEventListener("click", function () {
      state.lang = state.lang === "zh" ? "en" : "zh";
      saveStorage();
      updateLanguageUI();
    });

    // 设置页：三层缩放换层阈值调节
    var thMap = [
      ["thRegionOut", "regionOut"],
      ["thTopoIn", "topoIn"],
      ["thTopoOut", "topoOut"],
      ["thWorldIn", "worldIn"]
    ];
    function syncThresholdInputs() {
      thMap.forEach(function (pair) {
        var inp = $(pair[0]);
        if (inp) inp.value = Math.round(LEVEL[pair[1]] * 100);
      });
    }
    function saveThresholds() {
      try {
        localStorage.setItem(KEY_LEVEL_TH, JSON.stringify({
          regionOut: LEVEL.regionOut,
          topoOut: LEVEL.topoOut,
          worldIn: LEVEL.worldIn,
          topoIn: LEVEL.topoIn
        }));
      } catch (e) {}
    }
    syncThresholdInputs();
    thMap.forEach(function (pair) {
      var inp = $(pair[0]);
      if (!inp) return;
      inp.addEventListener("change", function () {
        var v = parseFloat(inp.value);
        if (!isFinite(v) || v <= 0) { syncThresholdInputs(); return; }
        var min = parseFloat(inp.min) || 10;
        var max = parseFloat(inp.max) || 400;
        v = Math.max(min, Math.min(max, v));
        LEVEL[pair[1]] = v / 100;
        inp.value = Math.round(v);
        saveThresholds();
      });
    });
    var thReset = $("thReset");
    if (thReset) {
      thReset.addEventListener("click", function () {
        LEVEL.regionOut = LEVEL_DEFAULTS.regionOut;
        LEVEL.topoIn = LEVEL_DEFAULTS.topoIn;
        LEVEL.topoOut = LEVEL_DEFAULTS.topoOut;
        LEVEL.worldIn = LEVEL_DEFAULTS.worldIn;
        syncThresholdInputs();
        saveThresholds();
      });
    }

    $("cardClose").addEventListener("click", closeDetailCard);

    var copyBtn = $("cardCopyCoord");
    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        var pin = PINS.find(function (p) { return p.id === state.selectedPinId; });
        if (!pin) return;
        var w = pin.world || [];
        var txt = (pin.zh || pin.id) + (w.length >= 3 ? "  X " + w[0] + " Y " + w[1] + " Z " + w[2] : "");
        function doneCopy() {
          copyBtn.textContent = state.lang === "zh" ? "已复制" : "Copied";
          setTimeout(function () { copyBtn.textContent = state.lang === "zh" ? "复制坐标" : "Copy"; }, 1200);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(txt).then(doneCopy, doneCopy);
        } else {
          doneCopy();
        }
      });
    }

    var editBtn = $("btnEditMode");
    if (editBtn) editBtn.addEventListener("click", toggleCalibrationMode);

    var exitCalBtn = $("btnExitCalMode");
    if (exitCalBtn) exitCalBtn.addEventListener("click", toggleCalibrationMode);

    var exportBtn = $("btnExportPins");
    if (exportBtn) {
      exportBtn.addEventListener("click", function () {
        var jsonStr = JSON.stringify(PINS, null, 2);
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(jsonStr).then(function () {
            alert("🎉 全部点位校准数据已复制到系统剪贴板！\n您可以直接将数据粘贴并发送给 AI，或者直接点击旁边的【下载更新文件】一键替换。");
          });
        } else {
          console.log(jsonStr);
          alert("数据已打印到浏览器 F12 控制台！");
        }
      });
    }

    var downloadBtn = $("btnDownloadPins");
    if (downloadBtn) {
      downloadBtn.addEventListener("click", function () {
        var fileContent = "/* ==========================================================================\n" +
          "   OoT Complete Points of Interest Database (时之笛全要素攻略点位数据库)\n" +
          "   ========================================================================== */\n\n" +
          "(function (window) {\n  \"use strict\";\n\n" +
          "  window.OOT_CATEGORIES = " + JSON.stringify(window.OOT_CATEGORIES || [], null, 2) + ";\n\n" +
          "  window.OOT_PINS_DATA = " + JSON.stringify(PINS, null, 2) + ";\n\n" +
          "})(window);\n";

        var blob = new Blob([fileContent], { type: "application/javascript;charset=utf-8" });
        var u = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = u;
        a.download = "pins_data.js";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(u);
        alert("📥 已生成并开始下载 pins_data.js！\n直接将下载的文件覆盖到 app/data/pins_data.js 即可持久生效。");
      });
    }

    // 键盘快捷键 E 开启/关闭点位校准微调模式
    window.addEventListener("keydown", function (e) {
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
      if (e.key === "e" || e.key === "E") {
        toggleCalibrationMode();
      }
    });

    window.addEventListener("resize", function () {
      // 保持当前视口平移缩放，仅更新相机
      if (state.mode === "region") { layoutRegionBase(); applyRegionCam(); }
      else updateCamera();
    });
  }

  function updateLanguageUI() {
    // 刷新节点标签
    NODES.forEach(function (node) {
      var header = $("header-" + node.id);
      if (header) {
        var badge = header.querySelector(".node-badge-type");
        var title = header.querySelector(".node-title-txt");
        if (badge) badge.textContent = node.type === "dungeon" ? (state.lang === "zh" ? "神殿" : "DUNGEON") : (state.lang === "zh" ? "区域" : "FIELD");
        if (title) title.textContent = state.lang === "zh" ? node.zh : node.en;
      }
    });

    // 刷新连线路标
    EDGES.forEach(function (edge) {
      var g = $("edge-label-" + edge.from + "-" + edge.to);
      if (g) {
        var text = g.querySelector(".edge-label");
        var rect = g.querySelector(".edge-label-bg");
        var labelTxt = state.lang === "zh" ? edge.zh : edge.en;
        if (text) text.textContent = labelTxt;
        if (rect) {
          var textW = labelTxt.length * 13 + 22;
          var x = parseFloat(text.getAttribute("x"));
          rect.setAttribute("x", x - textW / 2);
          rect.setAttribute("y", parseFloat(text.getAttribute("y")) - 12);
          rect.setAttribute("width", textW);
          rect.setAttribute("height", 24);
        }
      }
    });

    renderCategoriesSidebar();
    renderJumpChips();
    renderRegionList();
    renderWorldPins();
    var rHead = currentRegion();
    if (rHead) updateRegionHead(rHead);

    if (state.selectedPinId) {
      var p = PINS.find(function (pin) { return pin.id === state.selectedPinId; });
      if (p) selectPin(p);
    }
  }

  // 高亮特定传送门出入口及连线
  function highlightGatewayPortal(gw, sourceNodeId, enable) {
    var gwEl = $("gw-" + gw.id);
    if (gwEl) {
      if (enable) gwEl.classList.add("highlight");
      else gwEl.classList.remove("highlight");
    }

    // 寻找目标节点对应出入口
    var targetNode = NODES.find(function (n) { return n.id === gw.target; });
    if (targetNode && targetNode.gateways) {
      var oppositeGw = targetNode.gateways.find(function (g) { return g.target === sourceNodeId; });
      if (oppositeGw) {
        var oppEl = $("gw-" + oppositeGw.id);
        if (oppEl) {
          if (enable) oppEl.classList.add("highlight");
          else oppEl.classList.remove("highlight");
        }
      }
    }

    // 高亮相连连线
    EDGES.forEach(function (e) {
      if ((e.from === sourceNodeId && e.to === gw.target) || (e.from === gw.target && e.to === sourceNodeId)) {
        var path = $("edge-" + e.from + "-" + e.to);
        if (path) {
          if (enable) path.classList.add("highlight");
          else path.classList.remove("highlight");
        }
      }
    });
  }

  // 点击传送门直接平滑飞跃至目标地图
  function jumpToGatewayTarget(gw) {
    if (!gw.target) return;
    focusNode(gw.target, Math.max(state.zoom, 1.0));

    var targetCard = $("node-" + gw.target);
    if (targetCard) {
      targetCard.style.transition = "box-shadow 0.25s, transform 0.25s";
      targetCard.style.boxShadow = "0 0 35px #38bdf8, 0 0 15px #38bdf8";
      setTimeout(function () {
        targetCard.style.boxShadow = "";
      }, 1200);
    }

    // 目标端传送门呼吸动画
    var targetNode = NODES.find(function (n) { return n.id === gw.target; });
    if (targetNode && targetNode.gateways) {
      var oppGw = targetNode.gateways.find(function (g) { return g.target === gw.target; });
      if (!oppGw && targetNode.gateways.length > 0) oppGw = targetNode.gateways[0];
      if (oppGw) {
        var oppEl = $("gw-" + oppGw.id);
        if (oppEl) {
          oppEl.classList.add("highlight");
          setTimeout(function () { oppEl.classList.remove("highlight"); }, 1800);
        }
      }
    }
  }

  // -------------------------------------------------------------
  // 版本徽章 / 移动端侧栏初始态
  // -------------------------------------------------------------
  function renderVersion() {
    var el = $("verBadge");
    if (el) el.textContent = "OOTMAP V" + APP_VERSION + " © 2026 yalincc";
  }

  function initResponsiveShell() {
    var sb = $("sidebar");
    if (!sb) return;
    // 小屏默认收起侧栏；收起后由浮动按钮展开
    var collapsed = window.innerWidth <= 900;
    sb.classList.toggle("collapsed", collapsed);
    document.body.classList.toggle("side-collapsed", collapsed);
    window.addEventListener("resize", function () {
      if (window.innerWidth > 900) {
        sb.classList.remove("collapsed");
        document.body.classList.remove("side-collapsed");
      }
    });
  }

  // -------------------------------------------------------------
  // 程序入口
  // -------------------------------------------------------------
  function prefetchWorldImage() {
    var wi = $("worldImg");
    if (!wi || wi.getAttribute("src")) return;
    setTimeout(function () {
      if (!wi || wi.getAttribute("src")) return;
      wi.src = wi.getAttribute("data-src");
      if (wi.decode) wi.decode().catch(function () {});
    }, 2200);
  }

  function init() {
    initStorage();
    initResponsiveShell();
    bindCameraEvents();
    bindRegionEvents();
    bindWorldEvents();
    bindUI();
    bindSearch();
    // 探索度总览面板交互
    var progBox = $("progressBox");
    var expPanel = $("explorePanel");
    var expClose = $("exploreClose");
    var expTabs = $("exploreTabs");
    if (progBox && expPanel) {
      var toggleExp = function () {
        expPanel.hidden = !expPanel.hidden;
        var caret = $("progCaret");
        if (caret) caret.textContent = expPanel.hidden ? "▴" : "▾";
        if (!expPanel.hidden) renderExplorePanel();
      };
      progBox.addEventListener("click", toggleExp);
      progBox.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleExp(); }
      });
    }
    if (expClose && expPanel) {
      expClose.addEventListener("click", function (e) {
        e.stopPropagation();
        expPanel.hidden = true;
        var caret = $("progCaret");
        if (caret) caret.textContent = "▴";
      });
    }
    if (expTabs) {
      expTabs.querySelectorAll(".explore-tab").forEach(function (btn) {
        btn.addEventListener("click", function () {
          exploreTab = btn.getAttribute("data-etab") || "region";
          expTabs.querySelectorAll(".explore-tab").forEach(function (b) {
            b.classList.toggle("on", b === btn);
          });
          renderExplorePanel();
        });
      });
    }
    renderVersion();
    renderCategoriesSidebar();
    renderJumpChips();
    buildTopologyBoard();

    // 支持 URL 深度链接：
    // 区域模式 ?mode=region&area=KokiriForest&floor=1F&pin=xxx
    // 拓扑模式 ?mode=topology&node=KokiriForest 或旧链接 ?node=
    try {
      var params = new URLSearchParams(window.location.search);
      var qNode = params.get("node");
      var qPin = params.get("pin");
      var qMode = params.get("mode") || params.get("view");
      var qArea = params.get("area");
      var qFloor = params.get("floor");
      var qEra = params.get("era");

      if (qEra === "All" || qEra === "Child" || qEra === "Adult") {
        state.era = qEra;
        document.querySelectorAll("#eraSeg .era-btn").forEach(function (b) {
          b.classList.toggle("on", b.getAttribute("data-era") === qEra);
        });
        updateCategoriesCount();
        updateProgress();
      }
      if (qMode === "region" || qMode === "topology" || qMode === "world") state.mode = qMode;
      if (qNode) state.mode = "topology";
      if (qArea && REGIONS.some(function (r) { return r.id === qArea; })) state.area = qArea;
      if (qFloor) state.floor = qFloor;

      // 当前区域在当前时代不可进入时，自动落到第一个可进入区域
      var cur = currentRegion();
      if (!cur || !isRegionAvailable(cur)) {
        var pick = chooseRegionForEra();
        if (pick) state.area = pick.id;
      }

      setMode(state.mode);

      if (params.get("cal") === "1") {
        setTimeout(toggleCalibrationMode, 100);
      }
      if (qNode) {
        setTimeout(function () { focusNode(qNode, 0.85); }, 150);
      }
      if (qPin) {
        var targetPin = PINS.find(function (pin) { return pin.id === qPin; });
        if (targetPin) {
          var hostId = (targetPin.map && targetPin.map !== "hyrule") ? targetPin.map : targetPin.area;
          var floor = (targetPin.map && targetPin.map !== "hyrule") ? (targetPin.area === "0F" ? "1F" : targetPin.area) : "All";
          setTimeout(function () {
            if (state.mode === "region") {
              openRegion(hostId, { floor: floor });
            } else {
              focusNode(hostId, 1.0);
            }
            selectPin(targetPin);
          }, 220);
        }
      }
    } catch (e) {}
    prefetchWorldImage();
  }

  window.addEventListener("DOMContentLoaded", init);

})();

