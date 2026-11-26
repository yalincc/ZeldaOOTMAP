# ootnavi/server.py — 定位 HTTP 服务（链路 A：局域网同源）
#
# 参照 totknavi-pc/server_pc.go：一个端口同时提供
#   GET /pos      → 实时坐标 JSON（网页轮询）
#   GET /         → 状态页（内嵌）
#   /oot/*        → 静态托管地图页副本（手机同源访问，规避混合内容）
#   GET /lanUrl   → 当前局域网地址（二维码用）
#
# 协议对齐 xnavi /pos（网页端 app 只认这些字段）：
#   ok, gx, gy, gz, x, y, facing, verified, source, updated, app
#   OoT 坐标口径：(gx=X东, gy=Y高, gz=Z北)，Y 是高度（无 -105 偏置）

import json
import time
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket


def local_ip():
    """取本机局域网 IP（UDP 连外部地址，不真的发包）。"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def run_server(loc, port=8766, app_dir=None):
    ip = local_ip()
    lan_url = f"http://{ip}:{port}/oot/?follow=1"

    # 后台定位线程
    def locator_loop():
        while True:
            loc.tick()
            time.sleep(0.2)  # 5Hz

    t = threading.Thread(target=locator_loop, daemon=True)
    t.start()

    STATE_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OOT Navi 定位</title></head><body style="font-family:system-ui;padding:24px;max-width:600px;margin:auto">
<h2>时之笛实时定位</h2>
<p id="s">连接中…</p><pre id="p"></pre>
<script>
setInterval(async()=>{try{const r=await fetch('/pos');const d=await r.json();
document.getElementById('s').textContent=d.ok?('已定位 · '+(d.verified?'已验证':'待走动验证')):'未定位';
document.getElementById('p').textContent=JSON.stringify(d,null,2);}catch(e){document.getElementById('s').textContent='服务异常';}},1000);
</script></body></html>"""

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, obj, cors=True):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            if cors:
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Private-Network", "true")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/pos":
                p = loc.pos
                now = time.time()
                self._json({
                    "ok": bool(loc.ok and p and now - loc.updated < 5),
                    "gx": round(p[0], 3) if p else 0,       # X 东
                    "gy": round(p[1], 3) if p else 0,       # Y 高
                    "gz": round(p[2], 3) if p else 0,       # Z 北
                    "x": round(p[0], 3) if p else 0,        # 地图平面（备用）
                    "y": round(p[2], 3) if p else 0,
                    "facing": 0,                            # 朝向（阶段 3 从矩阵取）
                    "verified": loc.verified,
                    "source": loc.source,
                    "updated": round(loc.updated, 2),
                    "app": "ootnavi",                       # 网页端口发现指纹，勿改
                    "lanUrl": lan_url,
                })
            elif path == "/lanUrl":
                self._json({"url": lan_url})
            elif path in ("/", "/status"):
                body = STATE_HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif path.startswith("/oot/") and app_dir:
                # 静态托管地图页副本（阶段 3 用；暂未接）
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()

    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"\n=== 定位服务已启动 ===")
    print(f"  本机状态页: http://127.0.0.1:{port}/")
    print(f"  手机局域网: {lan_url}")
    print(f"  /pos 坐标接口已就绪（app=ootnavi）")
    print(f"  Ctrl+C 停止\n", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.shutdown()
