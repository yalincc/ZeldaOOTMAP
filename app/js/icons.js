/* ==========================================================================
   OoT Custom Vector Icon System (自制高清矢量图标库)
   每个图标均为精心绘制的 SVG，具备高对比度底座、发光轮廓与主题配色，
   在地图无级缩放时始终保持极致清晰。
   ========================================================================== */

(function (window) {
  "use strict";

  var ICONS = {
    heart: {
      color: "#ef4444",
      bg: "linear-gradient(135deg, #ef4444, #991b1b)",
      border: "#fca5a5",
      svg: '<path fill="#fff" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>' +
           '<path fill="#fecaca" opacity="0.6" d="M12 5.5c-1-1.8-3-2.5-4.5-2.5-2.5 0-4.5 2-4.5 4.5 0 2.8 2.6 5.3 7 9.3l2-1.8V5.5z"/>'
    },
    skull: {
      color: "#f59e0b",
      bg: "linear-gradient(135deg, #f59e0b, #b45309)",
      border: "#fde68a",
      svg: '<circle cx="12" cy="11" r="5" fill="#fff"/>' +
           '<path fill="#78350f" d="M9.5 10a1.2 1.2 0 1 0 0-2.4 1.2 1.2 0 0 0 0 2.4zm5 0a1.2 1.2 0 1 0 0-2.4 1.2 1.2 0 0 0 0 2.4z"/>' +
           '<path fill="#78350f" d="M11 12.5h2v2h-2z"/>' +
           '<path stroke="#fff" stroke-width="1.8" stroke-linecap="round" fill="none" d="M7 8L3 6M7 11L2 11M7 14L3 16M17 8l4-2M17 11l5 0M17 14l4 2M10 16v3M14 16v3"/>'
    },
    fairy: {
      color: "#c084fc",
      bg: "linear-gradient(135deg, #a855f7, #6b21a8)",
      border: "#e9d5ff",
      svg: '<circle cx="12" cy="12" r="3.2" fill="#fff"/>' +
           '<path fill="#f3e8ff" opacity="0.85" d="M12 9c-3-6-9-4-7 1 1.5 3.5 6 2 7-1z"/>' +
           '<path fill="#f3e8ff" opacity="0.85" d="M12 9c3-6 9-4 7 1-1.5 3.5-6 2-7-1z"/>' +
           '<path fill="#e9d5ff" opacity="0.7" d="M11.5 14c-3 4-7 4-5.5.5 1-2.5 4.5-1.5 5.5-.5z"/>' +
           '<path fill="#e9d5ff" opacity="0.7" d="M12.5 14c3 4 7 4 5.5.5-1-2.5-4.5-1.5-5.5-.5z"/>'
    },
    bean: {
      color: "#10b981",
      bg: "linear-gradient(135deg, #10b981, #065f46)",
      border: "#a7f3d0",
      svg: '<path fill="#fff" d="M12 4c-4.4 0-8 3.6-8 8 0 3.5 2.5 6.5 6 7.5.5.1 1-.3 1-.8v-4.2c-1.5.3-2.5-.5-2.8-1.5 1-.2 2 .2 2.8.8V11c0-2 1.5-3.5 3.5-3.5.5 0 1 .1 1.5.3-1-2.3-3.3-3.8-6-3.8z"/>' +
           '<path fill="#6ee7b7" d="M13.5 7.5c2.5 0 4.5 2 4.5 4.5 0 2-1.3 3.7-3.2 4.3v-4.3c0-1.2-.8-2.2-2-2.4.2-.7.4-1.4.7-2.1z"/>'
    },
    grotto: {
      color: "#d97706",
      bg: "linear-gradient(135deg, #d97706, #78350f)",
      border: "#fde68a",
      svg: '<path fill="#fff" d="M3 19h18c-1-7-4-12-9-12s-8 5-9 12z"/>' +
           '<path fill="#451a03" d="M6 19h12c-.8-4.5-3-8-6-8s-5.2 3.5-6 8z"/>' +
           '<circle cx="12" cy="15" r="1.5" fill="#fef3c7"/>'
    },
    bottle: {
      color: "#06b6d4",
      bg: "linear-gradient(135deg, #06b6d4, #0e7490)",
      border: "#a5f3fc",
      svg: '<path fill="#fef08a" d="M10 3h4v2h-4z"/>' +
           '<path fill="#fff" d="M9 5h6v2.5l2.5 3.5v9a2 2 0 0 1-2 2h-7a2 2 0 0 1-2-2v-9L9 7.5V5z"/>' +
           '<path fill="#67e8f9" d="M8.5 13h7v7a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1v-7z"/>' +
           '<circle cx="11" cy="16" r="1" fill="#fff" opacity="0.8"/>'
    },
    poe: {
      color: "#818cf8",
      bg: "linear-gradient(135deg, #6366f1, #3730a3)",
      border: "#c7d2fe",
      svg: '<path fill="#fff" d="M12 3c-4.4 0-8 3.6-8 8 0 3.2 1.9 6 4.6 7.3-.2.9-.6 1.7-1.1 2.4 1.8 0 3.5-.8 4.5-2.2 1 .5 2.1.8 3.3.8 4.4 0 8-3.6 8-8s-3.6-8-8-8z"/>' +
           '<circle cx="10" cy="10" r="1.5" fill="#312e81"/>' +
           '<circle cx="15" cy="10" r="1.5" fill="#312e81"/>' +
           '<path fill="#fbcfe8" d="M12 13c1.5 0 2.5 1 2.5 2s-1 1.5-2.5 1.5-2.5-.5-2.5-1.5 1-2 2.5-2z"/>'
    },
    stone: {
      color: "#94a3b8",
      bg: "linear-gradient(135deg, #64748b, #334155)",
      border: "#cbd5e1",
      svg: '<path fill="#fff" d="M7 4h10l2 16H5L7 4z"/>' +
           '<path fill="#1e293b" d="M12 8c-2.5 0-4.5 2-4.5 4.5s2 4.5 4.5 4.5 4.5-2 4.5-4.5S14.5 8 12 8z"/>' +
           '<circle cx="12" cy="12.5" r="2" fill="#38bdf8"/>' +
           '<path fill="#e2e8f0" d="M11 6h2v1h-2z"/>'
    },
    shop: {
      color: "#f97316",
      bg: "linear-gradient(135deg, #f97316, #c2410c)",
      border: "#fed7aa",
      svg: '<path fill="#fff" d="M4 6l1-3h14l1 3v2H4V6z"/>' +
           '<path fill="#fff" opacity="0.9" d="M5 9v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9H5z"/>' +
           '<path fill="#ea580c" d="M9 12h6v7H9z"/>' +
           '<circle cx="12" cy="15.5" r="1" fill="#fef08a"/>'
    },
    minigame: {
      color: "#ec4899",
      bg: "linear-gradient(135deg, #ec4899, #be185d)",
      border: "#fbcfe8",
      svg: '<circle cx="12" cy="12" r="9" fill="#fff"/>' +
           '<circle cx="12" cy="12" r="6.5" fill="#ec4899"/>' +
           '<circle cx="12" cy="12" r="4" fill="#fff"/>' +
           '<circle cx="12" cy="12" r="1.8" fill="#be185d"/>'
    },
    item: {
      color: "#14b8a6",
      bg: "linear-gradient(135deg, #14b8a6, #0f766e)",
      border: "#99f6e4",
      svg: '<path fill="#fff" d="M12 2l2.5 4.5H19l-3 4 1.5 5.5-5-3-5 3L9 10.5 6 6.5h4.5z"/>' +
           '<path fill="#ccfbf1" d="M12 5.5l1.5 3h3.5l-2.5 2.5 1 3.5-3.5-2-3.5 2 1-3.5-2.5-2.5h3.5z"/>'
    },
    dungeon: {
      color: "#e11d48",
      bg: "linear-gradient(135deg, #e11d48, #9f1239)",
      border: "#fecdd3",
      svg: '<path fill="#fff" d="M12 2L3 8v13h18V8L12 2z"/>' +
           '<path fill="#881337" d="M9 13a3 3 0 0 1 6 0v8H9v-8z"/>' +
           '<polygon points="12,5 15,9 9,9" fill="#fef08a"/>'
    },
    chest: {
      color: "#eab308",
      bg: "linear-gradient(135deg, #eab308, #854d0e)",
      border: "#fef08a",
      svg: '<path fill="#fff" d="M4 7c0-2 2-3 8-3s8 1 8 3v4H4V7z"/>' +
           '<path fill="#fff" opacity="0.9" d="M4 12h16v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-7z"/>' +
           '<rect x="10.5" y="10" width="3" height="4" rx="0.8" fill="#713f12"/>' +
           '<circle cx="12" cy="12" r="0.6" fill="#fef08a"/>'
    },
    warp: {
      color: "#0284c7",
      bg: "linear-gradient(135deg, #0284c7, #075985)",
      border: "#bae6fd",
      svg: '<polygon points="12,2 21,18 3,18" fill="#fef08a"/>' +
           '<polygon points="12,18 7.5,10 16.5,10" fill="#0369a1"/>'
    },
    door: {
      color: "#64748b",
      bg: "linear-gradient(135deg, #475569, #1e293b)",
      border: "#cbd5e1",
      svg: '<path fill="#fff" d="M5 3h14v18H5z"/>' +
           '<path fill="#0f172a" d="M7 5h10v16H7z"/>' +
           '<circle cx="9" cy="13" r="1" fill="#facc15"/>'
    },
    npc: {
      color: "#38bdf8",
      bg: "linear-gradient(135deg, #38bdf8, #0369a1)",
      border: "#bae6fd",
      svg: '<circle cx="12" cy="7" r="4" fill="#fff"/>' +
           '<path fill="#fff" d="M4 20c0-4.4 3.6-7 8-7s8 2.6 8 7v1H4v-1z"/>'
    },
    heartc: {
      color: "#f43f5e",
      bg: "linear-gradient(135deg, #f43f5e, #9f1239)",
      border: "#fecdd3",
      svg: '<path fill="#fff" d="M12 20.5l-1.6-1.5C5.3 14.7 2.6 12.2 2.6 9.3c0-2.4 1.9-4.3 4.3-4.3 1.5 0 2.9.7 3.9 1.9.9-1.2 2.3-1.9 3.8-1.9 2.4 0 4.3 1.9 4.3 4.3 0 2.9-2.7 5.4-7.8 9.7L12 20.5z"/>' +
           '<path fill="#fecdd3" d="M12 7.2l1.2 2.5 2.7.3-2 1.9.5 2.7-2.4-1.3-2.4 1.3.5-2.7-2-1.9 2.7-.3z" opacity="0.85"/>'
    },
    song: {
      color: "#a3e635",
      bg: "linear-gradient(135deg, #a3e635, #4d7c0f)",
      border: "#ecfccb",
      svg: '<path fill="#fff" d="M9 17.5V6.2l9-2.4v11.2a3 3 0 1 1-2-2.8V7.4l-5 1.3v9.3a3 3 0 1 1-2-1.1z"/>'
    },
    medal: {
      color: "#fbbf24",
      bg: "linear-gradient(135deg, #fbbf24, #b45309)",
      border: "#fef3c7",
      svg: '<circle cx="12" cy="12" r="8" fill="none" stroke="#fff" stroke-width="1.8"/>' +
           '<path fill="#fff" d="M12 7l1.6 3.3 3.6.5-2.6 2.5.6 3.6-3.2-1.7-3.2 1.7.6-3.6-2.6-2.5 3.6-.5z"/>' +
           '<path fill="#fef3c7" d="M9 20l3-2 3 2-1-3.2h-4z"/>'
    },
    upgrade: {
      color: "#22c55e",
      bg: "linear-gradient(135deg, #22c55e, #166534)",
      border: "#bbf7d0",
      svg: '<path fill="#fff" d="M12 3.5l5.5 6.5h-3.3v4.5h-4.4V10H6.5z"/>' +
           '<path fill="#bbf7d0" d="M5 17.5h14v3H5z"/>'
    },
    owl: {
      color: "#cbd5e1",
      bg: "linear-gradient(135deg, #64748b, #1e293b)",
      border: "#e2e8f0",
      svg: '<path fill="#fff" d="M3 9c0-3.2 2.6-5.5 6-5.5S15 5.8 15 9v7.5c0 2.2-1.8 4-4 4h-4c-2.2 0-4-1.8-4-4V9z"/>' +
           '<circle cx="7" cy="10" r="2.4" fill="#1e293b"/><circle cx="13" cy="10" r="2.4" fill="#1e293b"/>' +
           '<path fill="#fbbf24" d="M10 13.5l2 3.5h-4z"/>'
    },
    keyitem: {
      color: "#14b8a6",
      bg: "linear-gradient(135deg, #14b8a6, #0f766e)",
      border: "#99f6e4",
      svg: '<circle cx="8" cy="9" r="5" fill="none" stroke="#fff" stroke-width="2.2"/>' +
           '<path fill="#fff" d="M11 11.5l8.5 8.5-2 2-2-2-2 2-2-2 2-2-2.5-2.5z"/>'
    },
    merchant: {
      color: "#facc15",
      bg: "linear-gradient(135deg, #facc15, #a16207)",
      border: "#fef9c3",
      svg: '<path fill="#fff" d="M12 3l6 5-6 5-6-5z"/>' +
           '<path fill="#fef9c3" d="M12 11l6 5-6 5-6-5z" opacity="0.9"/>' +
           '<path fill="#fff" d="M4 18.5h16v2.5H4z" opacity="0.7"/>'
    }
  };

  /* 分类 MapIcon PNG 映射（assets/ui/ 下，统一 128×128 透明底，主体占比 84%）。
     13 个官方原图 + 14 个柔和版 AI 补全图；iconDone 为「已收集」状态图标。 */
  var OFFICIAL = {
    heart: ["MapIconCollectHeartPiece_00.png", "MapIconCollectHeartPieceCheck_00.png"],
    skull: ["MapIconCollectSkullSign_00.png", "MapIconCollectSkullSignCheck_00.png"],
    chest: ["MapIconTreasure_00.png", "MapIconTreasure_01.png"],
    boss: ["MapIconBoss_01.png"],
    dungeon: ["MapIconDoor_01.png"],
    soil: ["MapIconMagicBean_00.png"],
    sign: ["MapIconSign_00.png"],
    shop: ["MapIconShopGeneral_00.png"],
    minigame: ["MapIconMiniGameTarget_00.png"],
    fairy: ["MapIconGreatFairy_00.png"],
    training: ["MapIconTraining_00.png"],
    carpenter: ["MapIconCarpenter_00.png"],
    mask: ["MapIconShopMask_00.png"],
    heartc: ["MapIconAi_heartc.png"],
    song: ["MapIconAi_song.png"],
    medal: ["MapIconAi_medal.png"],
    bottle: ["MapIconAi_bottle.png"],
    upgrade: ["MapIconAi_upgrade.png"],
    owl: ["MapIconAi_owl.png"],
    poe: ["MapIconAi_poe.png"],
    keyitem: ["MapIconAi_keyitem.png"],
    grotto: ["MapIconAi_grotto.png"],
    stone: ["MapIconAi_stone.png"],
    warp: ["MapIconAi_warp.png"],
    item: ["MapIconAi_item.png"],
    npc: ["MapIconAi_npc.png"],
    merchant: ["MapIconAi_merchant.png"]
  };

  /**
   * 生成统一风格的 SVG 图标 HTML
   * @param {string} cat 分类 ID
   * @param {number} size 像素尺寸 (默认 28)
   * @returns {string} SVG HTML 字符串
   */
  function makeIconSvg(cat, size) {
    size = size || 28;
    var info = ICONS[cat] || ICONS.item;
    return '<svg class="oot-pin-svg" viewBox="0 0 24 24" width="' + size + '" height="' + size + '" style="filter: drop-shadow(0 2px 4px rgba(0,0,0,0.6));">' +
           '<circle cx="12" cy="12" r="11" fill="' + info.color + '" stroke="' + info.border + '" stroke-width="1.6"/>' +
           '<g transform="scale(0.72) translate(4.6, 4.6)">' + info.svg + '</g>' +
           '</svg>';
  }

  /**
   * 点位图标 HTML：优先官方 MapIcon PNG，缺图回落矢量图标。
   * @param {string} cat
   * @param {number} size
   * @param {boolean} done 是否已收集（用官方 Check 状态图）
   */
  function makeIconHtml(cat, size, done) {
    size = size || 20;
    var pair = OFFICIAL[cat];
    if (pair) {
      var file = (done && pair[1]) ? pair[1] : pair[0];
      return '<img class="oot-pin-img" src="assets/ui/' + file + '" width="' + size + '" height="' + size +
             '" alt="" draggable="false">';
    }
    return makeIconSvg(cat, size);
  }

  function getCatColor(cat) {
    return (ICONS[cat] && ICONS[cat].color) || "#d9b45a";
  }

  window.OOT_ICONS = {
    defs: ICONS,
    official: OFFICIAL,
    svg: makeIconSvg,
    html: makeIconHtml,
    color: getCatColor
  };

})(window);
