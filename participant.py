#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import json
import threading

lock = threading.Lock()
TX = {}
KV = {}

class Handler(BaseHTTPRequestHandler):

    def send_json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/status":
            with lock:
                self.send_json({"tx": TX, "kv": KV})
            return
        self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        txid = body.get("txid")

        if self.path == "/prepare":
            with lock:
                TX[txid] = {"state": "READY", "op": body["op"]}
            self.send_json({"vote": "YES"})
            return

        if self.path == "/commit":
            with lock:
                op = TX[txid]["op"]
                if op["type"] == "SET":
                    KV[op["key"]] = op["value"]
                TX[txid]["state"] = "COMMITTED"
            self.send_json({"state": "COMMITTED"})
            return

        if self.path == "/abort":
            with lock:
                TX[txid] = {"state": "ABORTED"}
            self.send_json({"state": "ABORTED"})
            return

        if self.path == "/can_commit":
            with lock:
                TX[txid] = {"state": "READY", "op": body["op"]}
            self.send_json({"vote": "YES"})
            return

        if self.path == "/precommit":
            with lock:
                TX[txid]["state"] = "PRECOMMIT"
            self.send_json({"state": "PRECOMMIT"})
            return

        self.send_error(404)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    args = ap.parse_args()

    server = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    print("[PARTICIPANT] running on port", args.port)
    server.serve_forever()

if __name__ == "__main__":
    main()
