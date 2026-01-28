#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib import request
import argparse, json, threading, time

NODE_ID = "COORD"
PARTICIPANTS = []
TIMEOUT = 3.0
TX = {}
lock = threading.Lock()

def post_json(url, payload):
    data = json.dumps(payload).encode()
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read())

def run_2pc(txid, op):
    votes = {}
    decision = "COMMIT"

    for p in PARTICIPANTS:
        try:
            r = post_json(p + "/prepare", {"txid": txid, "op": op})
            votes[p] = r["vote"]
            if r["vote"] != "YES":
                decision = "ABORT"
        except:
            votes[p] = "NO_TIMEOUT"
            decision = "ABORT"

    endpoint = "/commit" if decision == "COMMIT" else "/abort"
    for p in PARTICIPANTS:
        try:
            post_json(p + endpoint, {"txid": txid})
        except:
            pass

    with lock:
        TX[txid]["decision"] = decision
        TX[txid]["votes"] = votes
        TX[txid]["state"] = "DONE"

def run_3pc(txid, op):
    try:
        for p in PARTICIPANTS:
            r = post_json(p + "/can_commit", {"txid": txid, "op": op})
            if r["vote"] != "YES":
                raise Exception()

        for p in PARTICIPANTS:
            post_json(p + "/precommit", {"txid": txid})

        for p in PARTICIPANTS:
            post_json(p + "/commit", {"txid": txid})

        decision = "COMMIT"
    except:
        decision = "ABORT"
        for p in PARTICIPANTS:
            try:
                post_json(p + "/abort", {"txid": txid})
            except:
                pass

    with lock:
        TX[txid]["decision"] = decision
        TX[txid]["state"] = "DONE"

class Handler(BaseHTTPRequestHandler):

    def send_json(self, obj):
        try:
            data = json.dumps(obj).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except:
            pass

    def do_GET(self):
        if self.path == "/status":
            with lock:
                self.send_json({
                    "ok": True,
                    "node": NODE_ID,
                    "participants": PARTICIPANTS,
                    "tx": TX
                })
            return
        self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        if self.path == "/tx/start":
            txid = body["txid"]
            protocol = body["protocol"]
            op = body["op"]

            with lock:
                TX[txid] = {"state": "STARTED", "protocol": protocol}

            if protocol == "2PC":
                threading.Thread(target=run_2pc, args=(txid, op), daemon=True).start()
            else:
                threading.Thread(target=run_3pc, args=(txid, op), daemon=True).start()

            self.send_json({"ok": True, "txid": txid, "status": "STARTED"})
            return

        self.send_error(404)

def main():
    global PARTICIPANTS
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9100)
    ap.add_argument("--participants", required=True)
    args = ap.parse_args()

    PARTICIPANTS = [p.strip() for p in args.participants.split(",")]

    server = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    print("[COORD] running")
    server.serve_forever()

if __name__ == "__main__":
    main()
