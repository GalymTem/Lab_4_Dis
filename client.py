#!/usr/bin/env python3
from urllib import request
import argparse, json

def post(url, data):
    req = request.Request(url, json.dumps(data).encode(),
        headers={"Content-Type": "application/json"})
    with request.urlopen(req, timeout=5) as r:
        return json.loads(r.read())

def get(url):
    with request.urlopen(url) as r:
        return json.loads(r.read())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coord", required=True)
    ap.add_argument("cmd", choices=["start", "status"])
    ap.add_argument("txid", nargs="?")
    ap.add_argument("protocol", nargs="?")
    ap.add_argument("op", nargs="?")
    ap.add_argument("key", nargs="?")
    ap.add_argument("value", nargs="?")
    args = ap.parse_args()

    base = args.coord.rstrip("/")

    if args.cmd == "status":
        print(get(base + "/status"))
        return

    payload = {
        "txid": args.txid,
        "protocol": args.protocol,
        "op": {"type": args.op, "key": args.key, "value": args.value}
    }

    print(post(base + "/tx/start", payload))

if __name__ == "__main__":
    main()
