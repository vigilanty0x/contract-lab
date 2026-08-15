"""Offline webhook validator; no listener or network access."""
import argparse, hashlib, json
from pathlib import PurePosixPath

def inspect_webhook(event, max_body=65536):
    errors=[]
    method=event.get("method"); path=event.get("path"); headers=event.get("headers",{}); body=event.get("body","")
    if method not in {"POST","PUT","PATCH"}: errors.append("method_not_allowed")
    if not isinstance(path,str) or not path.startswith("/") or ".." in PurePosixPath(path).parts: errors.append("invalid_path")
    if not isinstance(headers,dict) or len(headers)>100: errors.append("invalid_headers")
    if not isinstance(body,str) or len(body.encode("utf-8"))>max_body: errors.append("body_limit")
    canonical=json.dumps({"method":method,"path":path,"headers":headers,"body":body},sort_keys=True,separators=(",",":"))
    return {"accepted":not errors,"errors":errors,"request_sha256":hashlib.sha256(canonical.encode()).hexdigest(),"bytes":len(body.encode()) if isinstance(body,str) else 0}

def probe():
    good=inspect_webhook({"method":"POST","path":"/demo","headers":{},"body":"{}"}); bad=inspect_webhook({"method":"GET","path":"../x","headers":{},"body":""})
    return {"ok":good["accepted"] and not bad["accepted"],"control":good["accepted"],"counter_proof":not bad["accepted"]}

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("command",choices=("inspect","probe")); p.add_argument("--input"); a=p.parse_args(argv)
    out=probe() if a.command=="probe" else inspect_webhook(json.load(open(a.input,encoding="utf-8")))
    print(json.dumps(out,sort_keys=True)); return 0 if out.get("ok",out.get("accepted")) else 2
