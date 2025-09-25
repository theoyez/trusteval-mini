<!-- CONTRIBUTING.md (single paste-once file with full formatting) -->

<h1>How to Submit a Score to TrustEval-Mini</h1>
<p>This repo hosts a small, auditable RAG evaluation and a public leaderboard.</p>
<hr>

<h2>0) Requirements</h2>
<ul>
  <li>Python <b>3.9+</b></li>
  <li>Your model’s predictions in <b>JSONL</b> (see <code>examples/</code> for the format)</li>
</ul>

<div style="padding:10px 12px;border:1px solid #e5e7eb;border-radius:10px;background:#f8fafc;margin:16px 0">
  <b>Choose ONE run mode below. Do not run both.</b>
</div>

<h2>1) Run the evaluator</h2>

<h3>A) DERIVED (simplest)</h3>
<pre><code>python trusieval.py \
  --sources data/sources.jsonl \
  --manifest data/manifest.json \
  --manifest-hash data/manifest.sha256 \
  --qas data/qas.jsonl \
  --pred path/to/your_predictions.jsonl \
  --out report.json --html report.html \
  --run-name &lt;your_run_name&gt; --provenance DERIVED
</code></pre>

<h3>B) STRICT (provenance-verified)</h3>
<p style="margin-top:-4px;color:#475569">
  Uses our signed manifest and public key. If STRICT succeeds, your <code>report.json</code> will include:
  <code>"provenance": "STRICT"</code> and <code>"signature_verified": true</code>.
</p>
<pre><code>python trusieval.py \
  --sources data/sources.jsonl \
  --manifest data/manifest.json \
  --manifest-hash data/manifest.sha256 \
  --manifest-sig data/manifest.json.sig \
  --pubkey keys/pubkey.pem \
  --qas data/qas.jsonl \
  --pred path/to/your_predictions.jsonl \
  --out report.json --html report.html \
  --run-name &lt;your_run_name&gt; --provenance STRICT
</code></pre>

<hr>

<h2>2) Add your files to this repo</h2>
<ol>
  <li>Create a folder for your run:
    <pre><code>submissions/&lt;your_run_name&gt;/</code></pre>
  </li>
  <li>Put these files inside it:
    <pre><code>submissions/&lt;your_run_name&gt;/report.json
submissions/&lt;your_run_name&gt;/report.html</code></pre>
  </li>
  <li>Open <b>scores.csv</b> and add <b>one</b> new row <i>under the header</i>:
    <pre><code>run_name,AEM,TokenF1,SpanF1,PI,When,Notes
&lt;your_run_name&gt;,&lt;AEM&gt;,&lt;TokenF1&gt;,&lt;SpanF1&gt;,&lt;PI&gt;,&lt;YYYY-MM-DD&gt;,&lt;short note&gt;</code></pre>
  </li>
</ol>
<p><b>Notes</b></p>
<ul>
  <li>Keep the CSV <b>header</b> as the first line.</li>
  <li><code>&lt;When&gt;</code> is a date like <code>2025-09-25</code>.</li>
  <li>Avoid extra commas in the <b>Notes</b> field.</li>
</ul>

<hr>

<h2>3) Open a Pull Request</h2>
<ol>
  <li>Push your fork and open a PR to <b>theoyez/trusteval-mini</b>.</li>
  <li>CI will verify that the CSV row matches your <code>report.json</code>.
    If it fails, read the CI message, fix locally, and push again.</li>
</ol>

<hr>

<h3>Provenance modes (at a glance)</h3>
<ul>
  <li><b>DERIVED</b> — quickest start: uses the published manifest + hash.</li>
  <li><b>STRICT</b> — cryptographically verified: uses our signature (<code>data/manifest.json.sig</code>) and public key (<code>keys/pubkey.pem</code>).</li>
</ul>
<p>We only need your <b>reports</b> and <b>one CSV row</b> — not your data or model.</p>
