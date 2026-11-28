/* ==========================================================================
   ZeldaOOTMAP · 任务板块（侧栏任务大类 / 本区任务 / 地图流程气泡 / 任务卡）
   ========================================================================== */
(function (window, document) {
  "use strict";

  var KEY_DONE_QUESTS = "oot_map_done_quests_v1";
  var QUESTS = Array.isArray(window.OOT_QUESTS) ? window.OOT_QUESTS : [];
  if (!QUESTS.length) return;

  var QUEST_BY_KEY = {};
  QUESTS.forEach(function (q) { QUEST_BY_KEY[q.key] = q; });

  var GROUP_META = {
    main:    { zh: "主线任务", en: "Main Quest",   color: "#eab308" },
    side:    { zh: "支线与长链", en: "Side / Chain", color: "#38bdf8" },
    dungeon: { zh: "迷宫攻略", en: "Dungeon",      color: "#f43f5e" }
  };

  var REGION_GUIDE_MAP = {
    InsideTheDekuTree:   { key: "dekuTree",         zh: "迷宫攻略", en: "Walkthrough" },
    DodongoCavern:       { key: "dodongoCavern",    zh: "迷宫攻略", en: "Walkthrough" },
    InsideJabuJabuBelly: { key: "jabuJabusBelly",   zh: "迷宫攻略", en: "Walkthrough" },
    ForestTemple:        { key: "forestTemple",     zh: "迷宫攻略", en: "Walkthrough" },
    FireTemple:          { key: "fireTemple",       zh: "迷宫攻略", en: "Walkthrough" },
    IceCavern:           { key: "iceCavern",        zh: "迷宫攻略", en: "Walkthrough" },
    WaterTemple:         { key: "waterTemple",      zh: "迷宫攻略", en: "Walkthrough" },
    BottomOfTheWell:     { key: "bottomOfTheWell",  zh: "迷宫攻略", en: "Walkthrough" },
    ShadowTemple:        { key: "shadowTemple",     zh: "迷宫攻略", en: "Walkthrough" },
    SpiritTemple:        { key: "spiritTemple",     zh: "迷宫攻略", en: "Walkthrough" },
    GanonCastle:         { key: "ganonsCastle",     zh: "迷宫攻略", en: "Walkthrough" },
    Market:              { key: "templeOfTime",     zh: "时之神殿", en: "Temple of Time" }
  };

  // 加侬多夫城堡「城内六道结界（示意）」与 ganon_inside_schematic.webp 对齐的步骤坐标
  var GANON_INSIDE_STEP_POS = {
    1: { x: 22, y: 67 },
    2: { x: 78, y: 67 },
    3: { x: 83, y: 45 },
    4: { x: 78, y: 23 },
    6: { x: 22, y: 23 },
    7: { x: 17, y: 45 },
    8: { x: 50, y: 22 }
  };

  var state = {
    done: {},
    panelOpen: false,
    mainOpen: true,
    sideOpen: true,
    activeKey: null,
    focusedStepNo: null
  };

  function $(id) { return document.getElementById(id); }

  function loadDone() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY_DONE_QUESTS) || "{}");
      if (raw && typeof raw === "object") state.done = raw;
    } catch (_) {}
  }

  function saveDone() {
    try {
      localStorage.setItem(KEY_DONE_QUESTS, JSON.stringify(state.done));
    } catch (_) {}
  }

  function mapApi() { return window.OOT_MAP_API || null; }

  function mapState() {
    var api = mapApi();
    return api ? api.getState() : { mode: "region", era: "All", lang: "zh", area: "KokiriForest", floor: "All" };
  }

  function isQuestInEra(q, era) {
    if (!era || era === "All" || q.era === "Both") return true;
    return q.era === era;
  }

  function regionName(areaId, isZh) {
    var api = mapApi();
    var regs = (api && api.getRegions) ? api.getRegions() : [];
    var r = regs.find(function (x) { return x.id === areaId; });
    return r ? (isZh ? r.zh : r.en) : areaId;
  }

  function groupList(grp) {
    return QUESTS.filter(function (q) { return q.group === grp; }).sort(function (a, b) {
      return (a.seq || 0) - (b.seq || 0);
    });
  }

  function eraFilteredGroup(grp, era) {
    return QUESTS.filter(function (q) {
      return q.group === grp && isQuestInEra(q, era);
    }).sort(function (a, b) {
      return (a.seq || 0) - (b.seq || 0);
    });
  }

  function renderSubGrid(items, toggleEl, labelEl, cntEl, caretEl, listEl, isOpen, labelZh, labelEn, isZh) {
    if (!toggleEl || !listEl) return;
    listEl.innerHTML = "";
    if (!items.length) {
      toggleEl.hidden = true;
      listEl.hidden = true;
      return;
    }
    toggleEl.hidden = false;
    toggleEl.setAttribute("aria-expanded", String(!!isOpen));
    if (caretEl) caretEl.textContent = isOpen ? "▾" : "▸";
    listEl.hidden = !isOpen;
    if (labelEl) labelEl.textContent = isZh ? labelZh : labelEn;
    if (cntEl) cntEl.textContent = String(items.length);

    items.forEach(function (q) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quest-grid-item" + (state.activeKey === q.key ? " on" : "") + (state.done[q.key] ? " is-done" : "");
      var name = isZh ? q.zh : (q.en || q.zh);
      var stepsCnt = q.flow ? q.flow.length : 0;
      btn.title = "#" + q.seq + " " + name + (isZh ? ("（" + stepsCnt + " 步）") : (" (" + stepsCnt + " steps)"));
      btn.innerHTML = '<span class="qi-name"></span>' + (state.done[q.key] ? '<span class="qi-check">✓</span>' : '');
      btn.querySelector(".qi-name").textContent = name;
      btn.addEventListener("click", function () {
        selectQuest(q.key);
      });
      listEl.appendChild(btn);
    });
  }

  function renderSidebarQuestGroup() {
    var cntEl = $("questGroupCount");
    var ms = mapState();
    var isZh = ms.lang === "zh";
    var era = ms.era;

    var mainItems = eraFilteredGroup("main", era);
    var sideItems = eraFilteredGroup("side", era);
    var visible = mainItems.concat(sideItems);
    var doneVisible = visible.filter(function (q) { return !!state.done[q.key]; }).length;
    if (cntEl) cntEl.textContent = doneVisible + "/" + visible.length;

    renderSubGrid(mainItems, $("questMainToggle"), $("questMainLabel"), $("questMainCount"), $("questMainCaret"), $("questMainList"), state.mainOpen, "主线", "Main", isZh);
    renderSubGrid(sideItems, $("questSideToggle"), $("questSideLabel"), $("questSideCount"), $("questSideCaret"), $("questSideList"), state.sideOpen, "支线", "Side", isZh);
  }

  function renderAreaQuests() {
    var wrap = $("areaQuestWrap");
    var listEl = $("areaQuestList");
    var cntEl = $("areaQuestCount");
    var headTxtEl = $("areaQuestHeadTxt");
    if (!wrap || !listEl) return;

    var ms = mapState();
    if (ms.mode !== "region") {
      wrap.hidden = true;
      return;
    }

    var isZh = ms.lang === "zh";
    if (headTxtEl) headTxtEl.textContent = isZh ? "任务" : "Quests";
    var curArea = ms.area;
    var matched = QUESTS.filter(function (q) {
      return isQuestInEra(q, ms.era) && Array.isArray(q.areas) && q.areas.indexOf(curArea) !== -1;
    }).sort(function (a, b) {
      var ord = { main: 0, side: 1, dungeon: 2 };
      if (ord[a.group] !== ord[b.group]) return ord[a.group] - ord[b.group];
      return (a.seq || 0) - (b.seq || 0);
    });

    if (!matched.length) {
      wrap.hidden = true;
      return;
    }

    wrap.hidden = false;
    if (cntEl) cntEl.textContent = String(matched.length);
    listEl.innerHTML = "";

    matched.forEach(function (q) {
      var stepNos = (q.flow || []).filter(function (s) { return s.area === curArea; }).map(function (s) { return s.no; });
      var stepBadge = stepNos.length ? (stepNos[0] + (stepNos.length > 1 ? "+" : "")) : "";
      var grpTxt = q.group === "main" ? (isZh ? "主" : "M") : (q.group === "dungeon" ? (isZh ? "迷" : "D") : (isZh ? "支" : "S"));

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "area-quest-item" + (state.activeKey === q.key ? " on" : "") + (state.done[q.key] ? " is-done" : "");
      btn.innerHTML =
        '<span class="qi-no">[' + grpTxt + ']</span>' +
        '<span class="qi-name"></span>' +
        (stepBadge ? '<span class="qi-meta">' + stepBadge + '</span>' : '');
      btn.querySelector(".qi-name").textContent = isZh ? q.zh : (q.en || q.zh);
      btn.addEventListener("click", function () {
        selectQuest(q.key, { stayInArea: true });
      });
      listEl.appendChild(btn);
    });
  }

  function renderRegionGuideBtn() {
    var btn = $("regionGuideBtn");
    if (!btn) return;
    var ms = mapState();
    var entry = (ms.mode === "region") ? REGION_GUIDE_MAP[ms.area] : null;
    var q = entry ? QUEST_BY_KEY[entry.key] : null;
    if (!entry || !q) {
      btn.hidden = true;
      return;
    }
    var isZh = ms.lang === "zh";
    var card = $("questCard");
    var isOpen = (state.activeKey === entry.key && card && !card.hidden);
    btn.hidden = false;
    btn.classList.toggle("on", !!isOpen);
    btn.textContent = "📖 " + (isZh ? entry.zh : entry.en);
    btn.title = isZh ? q.zh : (q.en || q.zh);
    btn.onclick = function (ev) {
      ev.stopPropagation();
      if (state.activeKey === entry.key && card && !card.hidden) {
        closeQuest(true);
      } else {
        selectQuest(entry.key, { stayInArea: true });
      }
    };
  }

  function makeInlineQuestLink(targetKey, isZh) {
    var tq = QUEST_BY_KEY[targetKey];
    if (!tq) return document.createTextNode(targetKey);
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "dc-link" + (state.done[targetKey] ? " is-done" : "");
    btn.textContent = (tq.seq ? "#" + tq.seq + " " : "") + (isZh ? tq.zh : (tq.en || tq.zh));
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      selectQuest(targetKey);
    });
    return btn;
  }

  function makeInlinePinLink(pinId, label) {
    var api = mapApi();
    var p = api && api.getPinById ? api.getPinById(pinId) : null;
    if (!p) return document.createTextNode(label);
    var ms = mapState();
    var done = !!(ms.donePins && ms.donePins[pinId]);
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "dc-link" + (done ? " is-done" : "");
    btn.textContent = label;
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      if (api && api.jumpToPin) api.jumpToPin(pinId);
    });
    return btn;
  }

  function appendSep(container) {
    var sep = document.createElement("span");
    sep.className = "dc-sep";
    sep.textContent = "/";
    container.appendChild(sep);
  }

  function renderQuestRelationSlot(slotEl, vEl, items, isZh) {
    vEl.innerHTML = "";
    if (!items || !items.length) {
      slotEl.hidden = true;
      return false;
    }
    items.forEach(function (it, idx) {
      if (idx > 0) appendSep(vEl);
      if (it.type === "quest" && QUEST_BY_KEY[it.key]) {
        vEl.appendChild(makeInlineQuestLink(it.key, isZh));
      } else {
        vEl.appendChild(document.createTextNode(it.text || ""));
      }
    });
    slotEl.hidden = false;
    return true;
  }

  function findMatchingPinForReward(q, rewardText) {
    var api = mapApi();
    if (!api || !api.getPinById || !Array.isArray(q.pinIds)) return null;
    for (var i = 0; i < q.pinIds.length; i++) {
      var p = api.getPinById(q.pinIds[i]);
      if (!p) continue;
      var s = (p.shortZh || "").replace(/（[^）]*）/g, "").replace(/^Boss：/, "");
      if (s && (rewardText.indexOf(s) !== -1 || s.indexOf(rewardText) !== -1)) {
        return p.id;
      }
    }
    return null;
  }

  function jumpToQuestStep(q, st) {
    state.focusedStepNo = st.no;
    var api = mapApi();
    if (!api) return;
    var ms = mapState();

    // Ensure compatible era
    if (q.era !== "Both" && ms.era !== "All" && ms.era !== q.era && api.setEra) {
      api.setEra(q.era);
    }

    var pin = st.pinId && api.getPinById ? api.getPinById(st.pinId) : null;
    var targetArea = st.area || q.areas[0];
    var targetFloor = "All";
    if (q.key === "ganonsCastle") {
      targetFloor = (st.no === 5) ? "All" : "Inside";
    } else if (pin && pin.map && pin.map !== "hyrule" && pin.area) {
      targetFloor = pin.area;
    }

    if (ms.mode !== "region" || ms.area !== targetArea || ms.floor !== targetFloor) {
      api.openRegion(targetArea, { floor: targetFloor });
    } else {
      renderRegionQuestFlow();
    }

    if (pin && !(q.key === "ganonsCastle" && targetFloor === "Inside") && ms.mode === "region" && api.centerRegionUV && targetArea === mapState().area) {
      api.centerRegionUV(pin.x, pin.y);
    }
    renderQuestCard(q);
  }

  function renderQuestCard(q) {
    var card = $("questCard");
    if (!card || !q) return;

    var api = mapApi();
    var ms = mapState();
    var isZh = ms.lang === "zh";
    var gm = GROUP_META[q.group] || GROUP_META.main;

    var catEl = $("questCatTag");
    if (catEl) {
      catEl.textContent = isZh ? gm.zh : gm.en;
      catEl.style.background = gm.color + "24";
      catEl.style.color = gm.color;
    }

    var seqEl = $("questSeqBadge");
    if (seqEl) seqEl.textContent = "#" + q.seq;
    var titleEl = $("questTitle");
    if (titleEl) titleEl.textContent = isZh ? q.zh : (q.en || q.zh);

    // Header pager
    var list = (q.group === "main" || q.group === "side") ? eraFilteredGroup(q.group, ms.era) : groupList(q.group);
    var idx = list.findIndex(function (x) { return x.key === q.key; });
    if (idx === -1) {
      list = groupList(q.group);
      idx = list.findIndex(function (x) { return x.key === q.key; });
    }
    var pager = $("questPager");
    var prevBtn = $("questPrevBtn");
    var nextBtn = $("questNextBtn");
    if (pager && prevBtn && nextBtn) {
      if (list.length > 1) {
        var prevQ = list[(idx - 1 + list.length) % list.length];
        var nextQ = list[(idx + 1) % list.length];
        pager.hidden = false;
        prevBtn.title = (isZh ? "上一个：" : "Prev: ") + (isZh ? prevQ.zh : (prevQ.en || prevQ.zh));
        nextBtn.title = (isZh ? "下一个：" : "Next: ") + (isZh ? nextQ.zh : (nextQ.en || nextQ.zh));
        prevBtn.onclick = function (e) { e.stopPropagation(); selectQuest(prevQ.key); };
        nextBtn.onclick = function (e) { e.stopPropagation(); selectQuest(nextQ.key); };
      } else {
        pager.hidden = true;
      }
    }

    var slotOrder = [];
    // 前置
    var reqItems = [];
    if (q.era !== "Both" && isZh) reqItems.push({ type: "text", text: q.era === "Child" ? "幼年林克" : "成年林克" });
    (q.requires || []).forEach(function (r) { reqItems.push(r); });
    if (renderQuestRelationSlot($("qslot-req"), $("qslotReqV"), reqItems, isZh)) slotOrder.push($("qslot-req"));

    // 后续
    if (renderQuestRelationSlot($("qslot-next"), $("qslotNextV"), q.unlocks || [], isZh)) slotOrder.push($("qslot-next"));

    // 奖励
    var rwSlot = $("qslot-reward");
    var rwV = $("qslotRewardV");
    rwV.innerHTML = "";
    var rewards = q.rewardZh || [];
    if (rewards.length) {
      rewards.forEach(function (rw, i) {
        if (i > 0) appendSep(rwV);
        var pid = findMatchingPinForReward(q, rw);
        rwV.appendChild(pid ? makeInlinePinLink(pid, rw) : document.createTextNode(rw));
      });
      rwSlot.hidden = false;
      slotOrder.push(rwSlot);
    } else {
      rwSlot.hidden = true;
    }

    // 流程步骤
    var stSlot = $("qslot-steps");
    var stV = $("qslotStepsV");
    stV.innerHTML = "";
    var multiArea = (q.areas && q.areas.length > 1);
    if (q.flow && q.flow.length) {
      var ul = document.createElement("div");
      ul.className = "q-step-list";
      q.flow.forEach(function (st) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "q-step-item" + (state.focusedStepNo === st.no ? " is-cur" : "");
        var aTxt = (multiArea || st.area !== ms.area) ? regionName(st.area, isZh) : "";
        btn.innerHTML =
          '<span class="q-step-no">' + st.no + '</span>' +
          '<span class="q-step-tx"></span>';
        var txEl = btn.querySelector(".q-step-tx");
        txEl.textContent = st.text;
        if (aTxt) {
          var badge = document.createElement("span");
          badge.className = "q-step-area";
          badge.textContent = aTxt;
          txEl.appendChild(badge);
        }
        btn.addEventListener("click", function (ev) {
          ev.stopPropagation();
          jumpToQuestStep(q, st);
        });
        ul.appendChild(btn);
      });
      stV.appendChild(ul);
      stSlot.hidden = false;
      slotOrder.push(stSlot);
    } else {
      stSlot.hidden = true;
    }

    // 提示
    var tipParts = [];
    if (q.bossZh) tipParts.push("Boss：" + q.bossZh);
    if (q.mainKeyZh) tipParts.push("核心道具：" + q.mainKeyZh);
    if (q.skulltula) tipParts.push("蜘蛛：" + q.skulltula + " 只");
    if (q.startZh) tipParts.push(q.startZh.replace(/[。；\s]+$/, ""));
    if (q.deliverZh) tipParts.push("交付：" + q.deliverZh.replace(/[。；\s]+$/, ""));
    if (q.officialTip && tipParts.length < 3) tipParts.push(q.officialTip.replace(/[。；\s]+$/, ""));
    if (q.note) tipParts.push(q.note.replace(/[。；\s]+$/, ""));

    var tipSlot = $("qslot-tip");
    var tipV = $("qslotTipV");
    if (tipParts.length) {
      tipV.textContent = tipParts.join("；");
      tipSlot.hidden = false;
      slotOrder.push(tipSlot);
    } else {
      tipSlot.hidden = true;
    }

    ["qslot-req", "qslot-next", "qslot-reward", "qslot-steps", "qslot-tip"].forEach(function (id) {
      var el = $(id);
      if (el) el.classList.remove("is-first");
    });
    if (slotOrder.length) slotOrder[0].classList.add("is-first");

    // Footer button
    var doneBtn = $("questDoneBtn");
    if (doneBtn) {
      var done = !!state.done[q.key];
      doneBtn.classList.toggle("is-done", done);
      doneBtn.textContent = done ? (isZh ? "已完成 ✓" : "Completed ✓") : (isZh ? "标记已完成" : "Mark Completed");
      doneBtn.onclick = function () {
        if (state.done[q.key]) delete state.done[q.key];
        else state.done[q.key] = true;
        saveDone();
        renderSidebarQuestGroup();
        renderAreaQuests();
        renderQuestCard(q);
      };
    }

    card.hidden = false;
    if (api && api.makeDraggable) api.makeDraggable(card);
    if (api && api.positionDetailCard) api.positionDetailCard(card, document.querySelector(".quest-step-bubble") || null);
  }

  function renderRegionQuestFlow() {
    var box = $("regionPins");
    if (!box) return;
    box.querySelectorAll(".quest-flow-svg, .quest-step-bubble").forEach(function (el) { el.remove(); });
    if (!state.activeKey) return;
    var q = QUEST_BY_KEY[state.activeKey];
    if (!q) return;

    var api = mapApi();
    var ms = mapState();
    var curArea = ms.area;
    var curFloor = ms.floor || "All";

    var pts = [];
    if (curArea === "GanonCastle" && curFloor === "Inside" && q.key === "ganonsCastle") {
      (q.flow || []).forEach(function (st) {
        var pos = GANON_INSIDE_STEP_POS[st.no];
        if (pos) pts.push({ step: st, pin: { x: pos.x, y: pos.y } });
      });
    } else {
      (q.flow || []).forEach(function (st) {
        if (st.area !== curArea || !st.pinId) return;
        var p = api && api.getPinById ? api.getPinById(st.pinId) : null;
        if (!p) return;
        if (curFloor !== "All" && p.map !== "hyrule" && p.area !== curFloor && !(curFloor === "1F" && p.area === "0F")) return;
        pts.push({ step: st, pin: p });
      });
    }

    if (!pts.length) return;

    if (pts.length >= 2) {
      var ns = "http://www.w3.org/2000/svg";
      var svg = document.createElementNS(ns, "svg");
      svg.setAttribute("class", "quest-flow-svg");
      svg.setAttribute("viewBox", "0 0 100 100");
      svg.setAttribute("preserveAspectRatio", "none");
      var poly = document.createElementNS(ns, "polyline");
      poly.setAttribute("class", "quest-flow-line");
      poly.setAttribute("points", pts.map(function (it) { return it.pin.x + "," + it.pin.y; }).join(" "));
      svg.appendChild(poly);
      box.appendChild(svg);
    }

    // 同一坐标（或极近距离）的多个步骤合并为一个胶囊气泡，避免互相遮挡无法点击
    var groups = [];
    pts.forEach(function (it) {
      var hit = groups.find(function (g) {
        return Math.hypot(g.x - it.pin.x, g.y - it.pin.y) < 0.8;
      });
      if (hit) hit.items.push(it);
      else groups.push({ x: it.pin.x, y: it.pin.y, items: [it] });
    });

    groups.forEach(function (g) {
      var b = document.createElement("button");
      b.type = "button";
      var isMulti = g.items.length > 1;
      var curInGroup = g.items.some(function (it) { return state.focusedStepNo === it.step.no; });
      b.className = "quest-step-bubble" + (isMulti ? " is-multi" : "") + (curInGroup ? " is-cur" : "");
      b.style.left = g.x + "%";
      b.style.top = g.y + "%";
      b.textContent = g.items.map(function (it) { return String(it.step.no); }).join("·");
      b.title = g.items.map(function (it) { return "#" + it.step.no + " " + it.step.text; }).join("\n");
      b.addEventListener("click", function (ev) {
        ev.stopPropagation();
        if (isMulti) {
          var idx = g.items.findIndex(function (it) { return it.step.no === state.focusedStepNo; });
          var next = g.items[(idx + 1) % g.items.length];
          state.focusedStepNo = next.step.no;
        } else {
          state.focusedStepNo = g.items[0].step.no;
        }
        renderQuestCard(q);
        renderRegionQuestFlow();
      });
      box.appendChild(b);
    });
  }

  function renderWorldQuestFlow() {
    var box = $("worldPins");
    if (!box) return;
    box.querySelectorAll(".quest-flow-svg, .quest-step-bubble").forEach(function (el) { el.remove(); });
    if (!state.activeKey || !window.OOT_WORLD) return;
    var q = QUEST_BY_KEY[state.activeKey];
    if (!q || !q.areas || !q.areas.length) return;

    var anchors = {};
    (window.OOT_WORLD.fields || []).forEach(function (f) { anchors[f.id] = { x: f.x * 100, y: f.y * 100 }; });
    (window.OOT_WORLD.dungeons || []).forEach(function (d) { anchors[d.id] = { x: d.x * 100, y: d.y * 100 }; });

    var pts = [];
    q.areas.forEach(function (aid, idx) {
      if (anchors[aid]) pts.push({ no: idx + 1, area: aid, pos: anchors[aid] });
    });
    if (!pts.length) return;

    if (pts.length >= 2) {
      var ns = "http://www.w3.org/2000/svg";
      var svg = document.createElementNS(ns, "svg");
      svg.setAttribute("class", "quest-flow-svg");
      svg.setAttribute("viewBox", "0 0 100 100");
      svg.setAttribute("preserveAspectRatio", "none");
      var poly = document.createElementNS(ns, "polyline");
      poly.setAttribute("class", "quest-flow-line");
      poly.setAttribute("points", pts.map(function (it) { return it.pos.x.toFixed(2) + "," + it.pos.y.toFixed(2); }).join(" "));
      svg.appendChild(poly);
      box.appendChild(svg);
    }

    pts.forEach(function (it) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "quest-step-bubble is-world";
      b.style.left = it.pos.x + "%";
      b.style.top = it.pos.y + "%";
      b.textContent = String(it.no);
      b.title = regionName(it.area, mapState().lang === "zh");
      b.addEventListener("click", function (ev) {
        ev.stopPropagation();
        var api = mapApi();
        if (api) api.openRegion(it.area);
      });
      box.appendChild(b);
    });
  }

  function selectQuest(key, opts) {
    opts = opts || {};
    var q = QUEST_BY_KEY[key];
    if (!q) return false;

    state.activeKey = key;
    var ms = mapState();

    var api = mapApi();
    if (api && api.closeDetailCard) api.closeDetailCard();

    if (api) {
      if (q.era !== "Both" && ms.era !== "All" && ms.era !== q.era && api.setEra) {
        api.setEra(q.era);
        ms = mapState();
      }
      var curMatch = opts.stayInArea && q.areas.indexOf(ms.area) !== -1;
      var targetArea = curMatch ? ms.area : (q.areas[0] || ms.area);
      var firstInArea = (q.flow || []).find(function (s) { return s.area === targetArea; }) || (q.flow || [])[0];
      state.focusedStepNo = firstInArea ? firstInArea.no : null;
      var wantFloor = (q.key === "ganonsCastle" && targetArea === "GanonCastle") ? "Inside" : null;
      if (ms.mode !== "world" && (ms.mode !== "region" || ms.area !== targetArea || (wantFloor && ms.floor !== wantFloor))) {
        api.openRegion(targetArea, wantFloor ? { floor: wantFloor } : undefined);
      }
    }

    renderSidebarQuestGroup();
    renderAreaQuests();
    renderQuestCard(q);
    renderRegionGuideBtn();
    renderRegionQuestFlow();
    renderWorldQuestFlow();
    return true;
  }

  function closeQuest(clearSelection) {
    var card = $("questCard");
    if (card) {
      card.hidden = true;
      if (clearSelection !== false) card.__dcDragPinned = false;
    }
    if (clearSelection !== false) {
      state.activeKey = null;
      state.focusedStepNo = null;
      renderSidebarQuestGroup();
      renderAreaQuests();
      renderRegionGuideBtn();
      renderRegionQuestFlow();
      renderWorldQuestFlow();
    } else {
      renderRegionGuideBtn();
    }
  }

  function initQuests() {
    loadDone();

    var toggle = $("questGroupToggle");
    var panel = $("questPanel");
    var caret = $("questGroupCaret");
    if (toggle && panel) {
      toggle.addEventListener("click", function () {
        state.panelOpen = !state.panelOpen;
        panel.hidden = !state.panelOpen;
        toggle.setAttribute("aria-expanded", String(state.panelOpen));
        if (caret) caret.textContent = state.panelOpen ? "▾" : "▸";
      });
    }

    function bindSubToggle(btnId, listId, caretId, prop) {
      var b = $(btnId);
      var l = $(listId);
      var c = $(caretId);
      if (!b || !l) return;
      b.addEventListener("click", function () {
        state[prop] = !state[prop];
        l.hidden = !state[prop];
        b.setAttribute("aria-expanded", String(state[prop]));
        if (c) c.textContent = state[prop] ? "▾" : "▸";
      });
    }
    bindSubToggle("questMainToggle", "questMainList", "questMainCaret", "mainOpen");
    bindSubToggle("questSideToggle", "questSideList", "questSideCaret", "sideOpen");

    var closeBtn = $("questClose");
    if (closeBtn) closeBtn.addEventListener("click", function () { closeQuest(true); });

    document.addEventListener("keydown", function (ev) {
      var card = $("questCard");
      if (!card || card.hidden || !state.activeKey) return;
      var tag = (document.activeElement && document.activeElement.tagName) || "";
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (ev.key === "ArrowLeft" && $("questPrevBtn") && !$("questPager").hidden) {
        ev.preventDefault();
        $("questPrevBtn").click();
      } else if (ev.key === "ArrowRight" && $("questNextBtn") && !$("questPager").hidden) {
        ev.preventDefault();
        $("questNextBtn").click();
      }
    });

    window.addEventListener("oot:regionRendered", function () {
      renderRegionQuestFlow();
      renderAreaQuests();
      renderRegionGuideBtn();
    });
    window.addEventListener("oot:worldRendered", function () {
      renderWorldQuestFlow();
      renderAreaQuests();
      renderRegionGuideBtn();
    });
    window.addEventListener("oot:stateChanged", function () {
      renderSidebarQuestGroup();
      renderAreaQuests();
      renderRegionGuideBtn();
      renderRegionQuestFlow();
      var card = $("questCard");
      if (state.activeKey && QUEST_BY_KEY[state.activeKey] && card && !card.hidden) {
        renderQuestCard(QUEST_BY_KEY[state.activeKey]);
      }
    });

    renderSidebarQuestGroup();
    renderAreaQuests();
    renderRegionGuideBtn();
    renderRegionQuestFlow();

    window.OOT_QUESTS_API = {
      selectQuest: selectQuest,
      closeQuest: closeQuest,
      closeCardOnly: function () { closeQuest(false); },
      getState: function () { return state; }
    };
  }

  window.addEventListener("DOMContentLoaded", function () {
    setTimeout(initQuests, 0);
  });
})(window, document);
