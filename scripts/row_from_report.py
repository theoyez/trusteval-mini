import json, sys, datetime
if len(sys.argv) < 2:
    print("Usage: python scripts/row_from_report.py submissions/<run>/report.json [notes]")
    raise SystemExit(1)
r = json.load(open(sys.argv[1]))
s = r["summary"]
run = r.get("run_name","run")
date = datetime.date.today().isoformat()
notes = sys.argv[2] if len(sys.argv)>2 else ""
print(f"{run},{s['AEM']:.4f},{s['TokenF1']:.4f},{s['SpanF1']:.4f},{s['PI']:.4f},{date},{notes}")
