/* ootnavi 前端实时定位与同源跟随模块 */
(function () {
  "use strict";

  var POLL_MS = 80;
  var naviState = {
    enabled: false,
    followCam: false,
    autoSwitch: true,
    panelOpen: false,
    timer: null,
    rafId: 0,
    lastPos: null,
    lastScene: "",
    connected: false,
    lanUrl: "",
    // 平滑插值状态（60fps）
    hasTarget: false,
    targetRegion: "",
    targetU: 0,
    targetV: 0,
    targetFacing: 0,
    targetCamFacing: 0,
    curU: 0,
    curV: 0,
    curFacing: 0,
    curCamFacing: 0,
  };

  function $(id) {
    return document.getElementById(id);
  }

  function posEndpoint() {
    if (location.protocol.indexOf("http") === 0 && location.pathname.indexOf("/oot") === 0) {
      return "/pos";
    }
    return "http://127.0.0.1:8766/pos";
  }

  function worldToUV(regionId, gx, gz) {
    var projs = window.OOT_PROJECTIONS || {};
    var p = projs[regionId];
    if (!p || !p.crop || p.crop.length < 4) return null;
    var scale = 1920 / p.captureHeight;
    var px = p.origW / 2 + (gx - p.camX) * scale;
    var py = p.origH / 2 + (gz - p.camZ) * scale;
    var cw = p.crop[2] - p.crop[0];
    var ch = p.crop[3] - p.crop[1];
    if (cw <= 0 || ch <= 0) return null;
    var u = ((px * (p.resizedW / p.origW) - p.crop[0]) / cw) * 100;
    var v = ((py * (p.resizedH / p.origH) - p.crop[1]) / ch) * 100;
    return { u: u, v: v };
  }

  function matchRegionId(scene) {
    if (!scene) return "";
    var regs = (window.OOT_REGIONS && window.OOT_REGIONS.areas) || [];
    var sLow = scene.toLowerCase();
    for (var i = 0; i < regs.length; i++) {
      if (regs[i].id.toLowerCase() === sLow) return regs[i].id;
    }
    var projs = window.OOT_PROJECTIONS || {};
    for (var key in projs) {
      var bns = projs[key].bancNames || [];
      for (var j = 0; j < bns.length; j++) {
        var bn = bns[j].replace(/_(Child|Adult)$/i, "").toLowerCase();
        if (bn === sLow) return key;
      }
    }
    return "";
  }

  function ensureLayer() {
    var layer = $("naviLayer");
    if (!layer) return null;
    var dot = $("naviLinkDot");
    if (!dot) {
      dot = document.createElement("div");
      dot.id = "naviLinkDot";
      dot.className = "navi-link-dot";
      dot.hidden = true;
      dot.innerHTML =
        '<div class="navi-fov" id="naviFov">' +
          '<svg viewBox="0 0 180 180" style="width:100%;height:100%;display:block">' +
            '<defs>' +
              '<radialGradient id="naviFovGrad" cx="90" cy="90" r="84" gradientUnits="userSpaceOnUse">' +
                '<stop offset="0%" stop-color="#fffbe6" stop-opacity="0.78"/>' +
                '<stop offset="45%" stop-color="#fff8d6" stop-opacity="0.42"/>' +
                '<stop offset="80%" stop-color="#fff8d6" stop-opacity="0.10"/>' +
                '<stop offset="100%" stop-color="#fff8d6" stop-opacity="0"/>' +
              '</radialGradient>' +
            '</defs>' +
            '<path d="M90 90 L35 24 A86 86 0 0 1 145 24 Z" fill="url(#naviFovGrad)"/>' +
          "</svg>" +
        "</div>" +
        '<div class="navi-arrow" id="naviArrow">' +
          '<img class="navi-arrow-img" src="assets/ui/MapIconPlayer_01.png" alt="林克" draggable="false">' +
        "</div>";
      layer.appendChild(dot);
    }
    return dot;
  }

  function hideDot() {
    naviState.hasTarget = false;
    var dot = $("naviLinkDot");
    if (dot) dot.hidden = true;
  }

  function lerpAngle(cur, target, alpha) {
    var diff = ((target - cur + 540) % 360) - 180;
    return (cur + diff * alpha + 360) % 360;
  }

  function startAnimLoop() {
    if (naviState.rafId) return;
    function frame() {
      naviState.rafId = 0;
      if (!naviState.enabled || !naviState.hasTarget) return;
      var api = window.OOT_MAP_API;
      var dot = $("naviLinkDot");
      if (!api || !dot) return;

      var st = api.getState();
      if (st.mode !== "region" || (naviState.targetRegion && naviState.targetRegion !== st.area)) {
        dot.hidden = true;
        naviState.rafId = requestAnimationFrame(frame);
        return;
      }

      var du = naviState.targetU - naviState.curU;
      var dv = naviState.targetV - naviState.curV;
      var df = ((naviState.targetFacing - naviState.curFacing + 540) % 360) - 180;
      var dc = ((naviState.targetCamFacing - naviState.curCamFacing + 540) % 360) - 180;
      var settled = Math.abs(du) < 0.002 && Math.abs(dv) < 0.002 && Math.abs(df) < 0.05 && Math.abs(dc) < 0.05;

      if (!settled || dot.hidden) {
        var alpha = 0.28;
        naviState.curU += du * alpha;
        naviState.curV += dv * alpha;
        naviState.curFacing = lerpAngle(naviState.curFacing, naviState.targetFacing, alpha);
        naviState.curCamFacing = lerpAngle(naviState.curCamFacing, naviState.targetCamFacing, alpha);

        dot.style.left = naviState.curU.toFixed(3) + "%";
        dot.style.top = naviState.curV.toFixed(3) + "%";
        dot.hidden = false;

        var arrow = $("naviArrow");
        if (arrow) {
          arrow.style.transform = "rotate(" + naviState.curFacing.toFixed(1) + "deg)";
        }
        var fov = $("naviFov");
        if (fov) {
          fov.style.transform = "translate(-50%, -50%) rotate(" + naviState.curCamFacing.toFixed(1) + "deg)";
        }

        if (naviState.followCam) {
          api.centerRegionUV(naviState.curU, naviState.curV);
        }
      }

      naviState.rafId = requestAnimationFrame(frame);
    }
    naviState.rafId = requestAnimationFrame(frame);
  }

  function renderDot(pos) {
    var api = window.OOT_MAP_API;
    if (!api) return;
    var st = api.getState();
    ensureLayer();

    if (!pos || !pos.ok || st.mode !== "region") {
      hideDot();
      return;
    }

    var targetReg = matchRegionId(pos.scene);
    if (targetReg && naviState.autoSwitch && targetReg !== st.area) {
      naviState.lastScene = targetReg;
      api.openRegion(targetReg, { keepZoom: true });
    } else if (targetReg) {
      naviState.lastScene = targetReg;
    }

    var activeReg = targetReg || st.area;
    var uv = worldToUV(activeReg, pos.gx, pos.gz);
    if (!uv || uv.u < -20 || uv.u > 120 || uv.v < -20 || uv.v > 120) {
      hideDot();
      return;
    }

    var switched = !naviState.hasTarget || naviState.targetRegion !== activeReg;
    naviState.targetRegion = activeReg;
    naviState.targetU = uv.u;
    naviState.targetV = uv.v;
    naviState.targetFacing = typeof pos.facing === "number" ? pos.facing : 0;
    naviState.targetCamFacing = typeof pos.camFacing === "number" ? pos.camFacing : naviState.targetFacing;

    if (switched) {
      naviState.curU = naviState.targetU;
      naviState.curV = naviState.targetV;
      naviState.curFacing = naviState.targetFacing;
      naviState.curCamFacing = naviState.targetCamFacing;
    }
    naviState.hasTarget = true;
    startAnimLoop();
  }

  function updatePanelUI() {
    var stEl = $("naviStatusBadge");
    var coordEl = $("naviCoords");
    var lanInput = $("naviLanInput");
    var enChk = $("naviEnableChk");
    var folChk = $("naviFollowChk");
    var swChk = $("naviAutoSwitchChk");
    var navBtn = $("navBtn");

    if (enChk) enChk.checked = naviState.enabled;
    if (folChk) folChk.checked = naviState.followCam;
    if (swChk) swChk.checked = naviState.autoSwitch;
    if (navBtn) navBtn.classList.toggle("active", naviState.enabled && naviState.connected);

    if (stEl) {
      if (!naviState.enabled) {
        stEl.className = "navi-badge off";
        stEl.textContent = "未开启";
      } else if (!naviState.connected) {
        stEl.className = "navi-badge warn";
        stEl.textContent = "等待 ootnavi-pc (:8766)…";
      } else if (!naviState.lastPos || !naviState.lastPos.ok) {
        stEl.className = "navi-badge warn";
        stEl.textContent = "已连服务 · 等待游戏 3D 画面";
      } else {
        stEl.className = "navi-badge ok";
        var p = naviState.lastPos;
        var nowStr = new Date().toLocaleTimeString("zh-CN", { hour12: false });
        stEl.textContent = (p.scene || "未知区域") + (p.era ? " · " + p.era : "") + " · " + nowStr;
      }
    }

    if (coordEl) {
      var lp = naviState.lastPos;
      if (naviState.enabled && naviState.connected && lp && lp.ok) {
        coordEl.textContent =
          "X " + lp.gx.toFixed(1) + "  Y " + lp.gy.toFixed(1) + "  Z " + lp.gz.toFixed(1) +
          "  朝向 " + Math.round(lp.facing || 0) + "°";
      } else {
        coordEl.textContent = "—";
      }
    }

    if (lanInput && naviState.lanUrl) {
      lanInput.value = naviState.lanUrl;
    }
  }

  function pollOnce() {
    if (!naviState.enabled) return;
    fetch(posEndpoint() + "?t=" + Date.now(), { cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || d.app !== "ootnavi") throw new Error("not ootnavi");
        naviState.connected = true;
        naviState.lastPos = d;
        if (d.lanUrl) naviState.lanUrl = d.lanUrl;
        renderDot(d);
        updatePanelUI();
      })
      .catch(function (err) {
        if (window.console && console.warn) console.warn("[ootnavi]", err);
        naviState.connected = false;
        naviState.lastPos = null;
        hideDot();
        updatePanelUI();
      })
      .finally(function () {
        if (naviState.enabled) {
          naviState.timer = setTimeout(pollOnce, POLL_MS);
        }
      });
  }

  function setEnabled(on) {
    naviState.enabled = !!on;
    if (naviState.timer) {
      clearTimeout(naviState.timer);
      naviState.timer = null;
    }
    if (naviState.enabled) {
      pollOnce();
    } else {
      naviState.connected = false;
      naviState.lastPos = null;
      hideDot();
    }
    updatePanelUI();
  }

  function togglePanel(force) {
    var panel = $("naviPanel");
    if (!panel) return;
    naviState.panelOpen = force !== undefined ? !!force : panel.hidden;
    panel.hidden = !naviState.panelOpen;
    if (naviState.panelOpen && !naviState.enabled) {
      setEnabled(true);
    }
    updatePanelUI();
  }

  function initNavi() {
    var panel = $("naviPanel");
    var enChk = $("naviEnableChk");
    var folChk = $("naviFollowChk");
    var swChk = $("naviAutoSwitchChk");
    var closeBtn = $("naviCloseBtn");
    var copyBtn = $("naviCopyLanBtn");

    if (panel) {
      panel.addEventListener("click", function (e) { e.stopPropagation(); });
      document.addEventListener("click", function () {
        if (!panel.hidden) togglePanel(false);
      });
    }
    if (enChk) enChk.addEventListener("change", function () { setEnabled(enChk.checked); });
    if (folChk) folChk.addEventListener("change", function () {
      naviState.followCam = folChk.checked;
      if (naviState.followCam && naviState.lastPos) renderDot(naviState.lastPos);
    });
    if (swChk) swChk.addEventListener("change", function () {
      naviState.autoSwitch = swChk.checked;
    });
    if (closeBtn) closeBtn.addEventListener("click", function () { togglePanel(false); });
    if (copyBtn) copyBtn.addEventListener("click", function () {
      var inp = $("naviLanInput");
      if (inp && inp.value && navigator.clipboard) {
        navigator.clipboard.writeText(inp.value);
        copyBtn.textContent = "已复制";
        setTimeout(function () { copyBtn.textContent = "复制"; }, 1200);
      }
    });

    try {
      var sp = new URLSearchParams(location.search);
      if (sp.get("follow") === "1") {
        naviState.followCam = true;
        setEnabled(true);
      }
    } catch (e) {}
    updatePanelUI();
  }

  window.OOT_NAVI = {
    togglePanel: togglePanel,
    setEnabled: setEnabled,
    onRegionRendered: function () {
      if (naviState.enabled && naviState.lastPos) renderDot(naviState.lastPos);
    },
  };

  window.addEventListener("DOMContentLoaded", initNavi);
})();
