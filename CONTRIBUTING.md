# How to Submit a Score to TrustEval-Mini

This repository hosts a small, auditable RAG evaluation and a public leaderboard.

---

## 0) Requirements
- Python **3.9+**
- Your model’s predictions in **JSONL** (see `examples/` for format)

---

## 1) Run the evaluator (DERIVED mode – simplest)

Open a terminal **in this repo’s folder** (after downloading or forking it) and run:

```bash
python trusieval.py \
  --sources data/sources.jsonl \
  --manifest data/manifest.json \
  --manifest-hash data/manifest.sha256 \
  --qas data/qas.jsonl \
  --pred path/to/your_predictions.jsonl \
  --out report.json --html report.html \
  --run-name <your_run_name> --provenance DERIVED
### STRICT mode (provenance-verified)

```bash
python trusieval.py \
  --sources data/sources.jsonl \
  --manifest data/manifest.json \
  --manifest-hash data/manifest.sha256 \
  --manifest-sig data/manifest.json.sig \
  --pubkey keys/pubkey.pem \
  --qas data/qas.jsonl \
  --pred path/to/your_predictions.jsonl \
  --out report.json --html report.html \
  --run-name <your_run_name> --provenance STRICT


3) Click **Commit changes**.

Yes—you can replace/add with pure copy-paste. No other edits needed.

---

## (Optional, recommended) CI guard
If you haven’t yet, add a small CI check so nobody can claim STRICT without a verified signature.

- Open `.github/workflows/validate-submission.yml` → **✏️ Edit**  
- After the step that compares the CSV to `report.json`, paste:

```yaml
      - name: Enforce STRICT provenance when used
        shell: python
        env:
          REPORT: ${{ steps.find.outputs.REPORT }}
        run: |
          import json, os, sys
          p = os.environ["REPORT"]
          with open(p,"r") as f:
            rep = json.load(f)
          prov = (rep.get("provenance") or "").upper()
          if prov == "STRICT" and not rep.get("signature_verified"):
            sys.exit("STRICT run must have signature_verified=true in report.json")
          print("Provenance check OK")
