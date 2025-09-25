# How to submit a score

## 1) Run the evaluator (DERIVED mode)
- Download this repo as ZIP or fork it, then on your computer open a terminal in the repo folder.
- Have Python 3.9+ installed.

Run:
python trusieval.py
--sources data/sources.jsonl
--manifest data/manifest.json
--manifest-hash data/manifest.sha256
--qas data/qas.jsonl
--pred path/to/your_predictions.jsonl
--out report.json --html report.html
--run-name <your_run_name> --provenance DERIVED

## 2) Add your files
- Create a folder: `submissions/<your_run_name>/`
- Put `report.json` and `report.html` inside that folder.
- Open `scores.csv` and add ONE row like:
run_name,AEM,TokenF1,SpanF1,PI,timestamp,notes
<your_run_name>,<AEM>,<TokenF1>,<SpanF1>,<PI>,<YYYY-MM-DD>,<short note>

## 3) Open a Pull Request
- Push your fork and open a PR back to `theoyez/trusteval-mini`.
- Our checks will verify the CSV matches your report. If it fails, read the CI message, fix, and push again.
