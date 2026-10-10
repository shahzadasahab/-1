#!/usr/bin/env python3
"""Open the HTML guide, wait for MathJax, print A4 PDF via Chrome."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "web" / "index.html"
PDF = ROOT / "Class_XI_Computer_Science_Teach_Yourself_Study_Guide.pdf"
PORT = 9322


def chrome_bin() -> str:
    for c in ("/usr/bin/google-chrome-stable", "/usr/bin/google-chrome", "/usr/local/bin/google-chrome"):
        if os.path.exists(c):
            return c
    raise SystemExit("google-chrome not found")


def wait_json(url: str, tries: int = 40) -> list:
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                return json.loads(r.read().decode())
        except Exception as exc:
            last = exc
            time.sleep(0.25)
    raise SystemExit(f"Chrome debug port never came up: {last}")


def main() -> None:
    if not HTML.exists():
        raise SystemExit(f"missing {HTML}; run generate_web.py first")
    uri = HTML.resolve().as_uri()
    cmd = [
        chrome_bin(),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        f"--remote-debugging-port={PORT}",
        "--remote-allow-origins=*",
        uri,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        targets = wait_json(f"http://127.0.0.1:{PORT}/json")
        ws = None
        for t in targets:
            if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                ws = t["webSocketDebuggerUrl"]
                break
        if not ws:
            raise SystemExit(f"no page target: {targets}")

        try:
            import websocket  # type: ignore
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "websocket-client"])
            import websocket  # type: ignore

        sock = websocket.create_connection(ws, timeout=60)
        mid = 0

        def call(method: str, params: dict | None = None, timeout: float = 60):
            nonlocal mid
            mid += 1
            sock.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
            deadline = time.time() + timeout
            while time.time() < deadline:
                msg = json.loads(sock.recv())
                if msg.get("id") == mid:
                    if "error" in msg:
                        raise RuntimeError(msg["error"])
                    return msg.get("result", {})
            raise TimeoutError(method)

        call("Runtime.enable")
        # Wait until MathJax marks the document ready.
        call(
            "Runtime.evaluate",
            {
                "expression": """
                  new Promise((resolve) => {
                    const done = () => resolve(document.documentElement.dataset.mathjax || '');
                    if (document.documentElement.dataset.mathjax === 'ready') return done();
                    const t = setInterval(() => {
                      if (document.documentElement.dataset.mathjax === 'ready') {
                        clearInterval(t); done();
                      }
                    }, 100);
                    setTimeout(() => { clearInterval(t); done(); }, 20000);
                  })
                """,
                "awaitPromise": True,
            },
            timeout=30,
        )
        time.sleep(0.4)
        result = call(
            "Page.printToPDF",
            {
                "paperWidth": 8.27,
                "paperHeight": 11.69,
                "marginTop": 0.35,
                "marginBottom": 0.4,
                "marginLeft": 0.35,
                "marginRight": 0.35,
                "printBackground": True,
                "preferCSSPageSize": False,
                "displayHeaderFooter": False,
            },
            timeout=90,
        )
        import base64

        PDF.write_bytes(base64.b64decode(result["data"]))
        print(f"Wrote {PDF} ({PDF.stat().st_size} bytes)")
        sock.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
