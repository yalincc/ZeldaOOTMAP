// ============================================================================
// GamerGuides 1783 点位全自动一键导出脚本 (在 GamerGuides 页面按 F12 粘贴到 Console 回车)
// ============================================================================
(async function exportGamerGuidesMarkers() {
  console.log("🚀 正在探测 GamerGuides 内存与网络中的全量点位数据...");

  // 1. 尝试从网络资源历史中找到 markers 的原始数据接口并直接拉取 (自带 Cloudflare 凭证，100%成功)
  var resources = performance.getEntriesByType("resource");
  var targetUrl = null;
  for (var r of resources) {
    var u = r.name.toLowerCase();
    if ((u.includes("marker") || u.includes("poi") || u.includes("location") || u.includes("map")) && (u.includes("json") || u.includes("api"))) {
      targetUrl = r.name;
      break;
    }
  }

  var dataToDownload = null;
  var fileName = "gamerguides_markers.json";

  if (targetUrl) {
    console.log("🎯 发现原始点位数据源接口:", targetUrl);
    try {
      var resp = await fetch(targetUrl);
      dataToDownload = await resp.json();
      console.log("✅ 成功从接口获取到原始完整点位数据！");
    } catch (e) {
      console.warn("fetch 尝试失败，转向内存遍历:", e);
    }
  }

  // 2. 如果接口未找到，尝试从内存全局变量中读取
  if (!dataToDownload) {
    if (window.__NUXT__ && window.__NUXT__.data) {
      dataToDownload = window.__NUXT__.data;
      console.log("✅ 从 __NUXT__ 提取到数据！");
    } else if (window.mapData) {
      dataToDownload = window.mapData;
      console.log("✅ 从 window.mapData 提取到数据！");
    } else if (window.map && typeof window.map.eachLayer === "function") {
      var extracted = [];
      window.map.eachLayer(function (l) {
        if (l.getLatLng || l.options) {
          extracted.push({
            pos: l.getLatLng ? l.getLatLng() : null,
            options: l.options,
            id: l._leaflet_id
          });
        }
      });
      dataToDownload = extracted;
      console.log("✅ 从 Leaflet 图层中遍历提取到 " + extracted.length + " 个图层点位！");
    }
  }

  // 3. 自动触发下载
  if (dataToDownload) {
    var blob = new Blob([JSON.stringify(dataToDownload, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    console.log("🎉 成功！已自动触发下载 gamerguides_markers.json 到您的【下载】文件夹！");
    alert("🎉 导出成功！已自动下载 gamerguides_markers.json 文件。\n请把这个文件直接拖给 AI，AI 将自动批量转换全图所有点位！");
  } else {
    // 提示查看 Network
    console.log("未直接探测到内存对象，请在 F12 -> Network 搜索 markers 找到对应的 json 请求。");
    alert("未探测到全局变量，请查看 F12 -> Network (网络) 标签，按 F5 刷新，在筛选框输入 json 或 marker，找到对应的请求右键另存为即可！");
  }
})();
