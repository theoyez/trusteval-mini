How to Submit a Score to TrustEval-Mini

This repo hosts a small, auditable RAG evaluation and a public leaderboard.

Quickstart — choose ONE command (don’t run both)

A) DERIVED (simplest)
python trusieval.py
--sources data/sources.jsonl
--manifest data/manifest.json
--manifest-hash data/manifest.sha256
--qas data/qas.jsonl
--pred path/to/your_predictions.jsonl
--out report.json --html report.html
--run-name <your_run_name> --provenance DERIVED

B) STRICT (provenance-verified)
python trusieval.py
--sources data/sources.jsonl
--manifest data/manifest.json
--manifest-hash data/manifest.sha256
--manifest-sig data/manifest.json.sig
--pubkey keys/pubkey.pem
--qas data/qas.jsonl
--pred path/to/your_predictions.jsonl
--out report.json --html report.html
--run-name <your_run_name> --provenance STRICT

If you used STRICT, your report.json must include:
"provenance": "STRICT" and "signature_verified": true

Then add your files

Create a folder: submissions/<your_run_name>/

Put report.json and report.html inside that folder.

Open scores.csv and add ONE new row (under the header):
run_name,AEM,TokenF1,SpanF1,PI,When,Notes
<your_run_name>,<AEM>,<TokenF1>,<SpanF1>,<PI>,<YYYY-MM-DD>,<short note>

Open a Pull Request

Push your fork and open a PR to theoyez/trusteval-mini. CI verifies the CSV against report.json. If it fails, read the CI message, fix locally, and push again.
