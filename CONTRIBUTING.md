# How to Submit a Score to TrustEval-Mini

This repository hosts a small, auditable RAG evaluation and a public leaderboard.

---

## 0) Requirements
- Python **3.9+**
- Your model’s predictions in **JSONL** (see `examples/` for format)

---

## 1) Run the evaluator (DERIVED mode — simplest)

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
