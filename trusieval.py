#!/usr/bin/env python3
import argparse, json, hashlib, datetime, subprocess, shutil, os, sys

def read_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line: continue
            rows.append(json.loads(line))
    return rows

def normalize(s):
    return " ".join((s or "").strip().lower().split())

def f1(a, b):
    at = normalize(a).split()
    bt = normalize(b).split()
    if not at and not bt: return 1.0
    if not at or not bt:  return 0.0
    overlap = 0
    bt_used = [False]*len(bt)
    for tok in at:
        for j,tb in enumerate(bt):
            if not bt_used[j] and tb==tok:
                bt_used[j]=True
                overlap += 1
                break
    prec = overlap/len(at)
    rec  = overlap/len(bt)
    if prec+rec==0: return 0.0
    return 2*prec*rec/(prec+rec)

def score_one(pred, golds):
    # AEM (exact after normalization) against any gold
    aem = 1.0 if any(normalize(pred)==normalize(g) for g in golds) else 0.0
    # TokenF1: best F1 vs any gold
    tfs = [f1(pred, g) for g in golds]
    token_f1 = max(tfs) if tfs else 0.0
    # SpanF1 (proxy here = token F1)
    span_f1 = token_f1
    return aem, token_f1, span_f1

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def verify_manifest_hash(manifest_json, manifest_sha256):
    # manifest_sha256 file can be "HEX  filename" or just HEX
    with open(manifest_sha256,'r',encoding='utf-8') as f:
        line = f.read().strip().split()[0]
    return line == sha256_file(manifest_json), line

def verify_signature(manifest_sha256, sigfile, pubkey):
    # Try openssl from PATH, then Homebrew path if needed
    openssl = shutil.which("openssl") or "/opt/homebrew/opt/openssl@3/bin/openssl"
    if not os.path.exists(openssl):
        return False, "openssl not found"
    # openssl pkeyutl -verify -pubin -inkey pubkey.pem -in manifest.sha256 -sigfile manifest.json.sig
    cmd = [openssl, "pkeyutl", "-verify", "-pubin", "-inkey", pubkey, "-in", manifest_sha256, "-sigfile", sigfile]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ok = (res.returncode==0)
    msg = (res.stdout.decode() or res.stderr.decode()).strip()
    return ok, msg or ("returncode="+str(res.returncode))

def main():
    ap = argparse.ArgumentParser(description="TrustEval-Mini (simple evaluator)")
    ap.add_argument("--sources", required=True)
    ap.add_argument("--qas", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--manifest-hash", required=True)
    ap.add_argument("--manifest-sig")         # STRICT only
    ap.add_argument("--pubkey")               # STRICT only
    ap.add_argument("--provenance", required=True, choices=["DERIVED","STRICT"])
    ap.add_argument("--run-name", required=True)
    ap.add_argument("--out", default="report.json")
    ap.add_argument("--html", default="report.html")
    args = ap.parse_args()

    # Verify manifest hash always
    mh_ok, mh_expected = verify_manifest_hash(args.manifest, args.manifest_hash)

    sig_ok = False
    sig_msg = ""
    if args.provenance == "STRICT":
        if not (args.manifest_sig and args.pubkey):
            print("STRICT requires --manifest-sig and --pubkey", file=sys.stderr)
            sys.exit(2)
        sig_ok, sig_msg = verify_signature(args.manifest_hash, args.manifest_sig, args.pubkey)

    # Load data
    # (sources not used for scoring here, but required for completeness)
    _sources = read_jsonl(args.sources)
    qas = read_jsonl(args.qas)
    preds = read_jsonl(args.pred)

    # Index preds by id
    pred_by_id = {}
    for r in preds:
        pid = r.get("id") or r.get("qid") or r.get("question_id")
        pred_by_id[pid] = r.get("answer") or r.get("prediction") or ""

    # Score
    aems, tfs, sfs = [], [], []
    for q in qas:
        qid = q.get("id") or q.get("qid") or q.get("question_id")
        golds = q.get("answers") or q.get("gold") or []
        pred = pred_by_id.get(qid, "")
        aem, tf, sf = score_one(pred, golds)
        aems.append(aem); tfs.append(tf); sfs.append(sf)

    AEM     = round(sum(aems)/len(aems), 4) if aems else 0.0
    TokenF1 = round(sum(tfs)/len(tfs), 4) if tfs else 0.0
    SpanF1  = round(sum(sfs)/len(sfs), 4) if sfs else 0.0
    PI      = 1.0 if (args.provenance=="STRICT" and sig_ok and mh_ok) else (0.5 if args.provenance=="DERIVED" else 0.0)

    report = {
        "run_name": args.run_name,
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
        "AEM": AEM, "TokenF1": TokenF1, "SpanF1": SpanF1, "PI": PI,
        "provenance": args.provenance,
        "manifest_hash_ok": mh_ok,
        "signature_verified": bool(sig_ok),
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>TrustEval-Mini Report — {args.run_name}</title>
<style>body{{font-family:system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding:24px;}}
table{{border-collapse:collapse}} th,td{{border:1px solid #ddd; padding:8px}}</style></head>
<body>
<h1>TrustEval-Mini Report</h1>
<p><b>Run:</b> {args.run_name} &nbsp; <b>Date (UTC):</b> {report['timestamp']}</p>
<table>
<tr><th>AEM</th><th>TokenF1</th><th>SpanF1</th><th>PI</th></tr>
<tr><td>{AEM}</td><td>{TokenF1}</td><td>{SpanF1}</td><td>{PI}</td></tr>
</table>
<p><b>Provenance:</b> {args.provenance} &nbsp; | &nbsp; <b>manifest_hash_ok:</b> {mh_ok} &nbsp; | &nbsp; <b>signature_verified:</b> {bool(sig_ok)}</p>
</body></html>"""
    with open(args.html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {args.out} and {args.html}")
    if args.provenance=="STRICT":
        print("Signature verify:", "OK" if sig_ok else f"FAIL ({sig_msg})")
        if not sig_ok:
            sys.exit(3)

if __name__ == "__main__":
    main()
