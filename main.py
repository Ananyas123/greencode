from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>GreenCode</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #050f08; --surface: #0a1f10; --card: #0f2916;
    --green: #00ff6a; --green2: #0F9D58; --text: #e8f5e9;
    --muted: #4a7a56; --accent: #aaff00; --red: #ff4444;
    --border: rgba(0,255,106,0.2);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: 'Syne', sans-serif; min-height: 100vh; }
  body::before {
    content: ''; position: fixed; inset: 0;
    background-image: linear-gradient(rgba(0,255,106,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,255,106,0.03) 1px, transparent 1px);
    background-size: 40px 40px; pointer-events: none; z-index: 0;
  }
  .container { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: 48px 24px; }
  header { text-align: center; margin-bottom: 56px; }
  .badge {
    display: inline-block; font-family: 'Space Mono', monospace; font-size: 11px;
    letter-spacing: 0.2em; color: var(--green); border: 1px solid var(--border);
    padding: 6px 16px; border-radius: 100px; margin-bottom: 24px;
    background: rgba(0,255,106,0.15);
  }
  h1 { font-size: clamp(42px, 8vw, 80px); font-weight: 800; line-height: 0.95; letter-spacing: -0.03em; margin-bottom: 16px; }
  h1 .green { color: var(--green); text-shadow: 0 0 40px rgba(0,255,106,0.5); }
  .subtitle { font-family: 'Space Mono', monospace; font-size: 13px; color: var(--muted); }
  .card {
    background: var(--card); border: 1px solid var(--border); border-radius: 20px;
    padding: 40px; margin-bottom: 24px; position: relative; overflow: hidden;
  }
  .section-label { font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 0.2em; color: var(--muted); margin-bottom: 20px; }
  .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }
  .input-group label { display: block; font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted); margin-bottom: 10px; }
  .input-group input[type="number"] {
    width: 100%; background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 16px; color: var(--text);
    font-family: 'Space Mono', monospace; font-size: 16px; outline: none;
  }
  .input-group input:focus { border-color: var(--green); box-shadow: 0 0 0 3px rgba(0,255,106,0.1); }
  .toggle-group { display: flex; gap: 12px; }
  .toggle-btn {
    flex: 1; padding: 14px; border-radius: 10px; border: 1px solid var(--border);
    background: var(--surface); color: var(--muted); font-family: 'Space Mono', monospace;
    font-size: 12px; cursor: pointer; transition: all 0.2s; text-align: center;
  }
  .toggle-btn.active { border-color: var(--green); background: rgba(0,255,106,0.08); color: var(--green); }
  .btn-calculate {
    width: 100%; padding: 18px; background: var(--green); color: #050f08; border: none;
    border-radius: 12px; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 16px;
    cursor: pointer; transition: all 0.2s;
  }
  .btn-calculate:hover { background: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,255,106,0.3); }
  .results { display: none; }
  .results.show { display: block; }
  .results-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
  .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 24px 20px; text-align: center; }
  .stat-card.highlight { border-color: var(--green); background: rgba(0,255,106,0.05); }
  .stat-value { font-size: 32px; font-weight: 800; color: var(--green); line-height: 1; margin-bottom: 8px; }
  .stat-label { font-family: 'Space Mono', monospace; font-size: 10px; color: var(--muted); text-transform: uppercase; }
  .comparison { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 24px; }
  .compare-row { display: flex; align-items: center; gap: 16px; margin-bottom: 14px; }
  .compare-row:last-child { margin-bottom: 0; }
  .compare-label { font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted); width: 80px; flex-shrink: 0; }
  .bar-track { flex: 1; height: 8px; background: rgba(255,255,255,0.05); border-radius: 100px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 100px; transition: width 1s cubic-bezier(0.16,1,0.3,1); }
  .bar-fill.bad { background: var(--red); width: 0; }
  .bar-fill.good { background: var(--green); width: 0; }
  .compare-ops { font-family: 'Space Mono', monospace; font-size: 12px; color: var(--text); width: 90px; text-align: right; flex-shrink: 0; }
  .success-msg { background: rgba(0,255,106,0.08); border: 1px solid rgba(0,255,106,0.3); border-radius: 12px; padding: 16px 20px; font-family: 'Space Mono', monospace; font-size: 13px; color: var(--green); margin-top: 16px; text-align: center; }
  .error-msg { background: rgba(255,68,68,0.08); border: 1px solid rgba(255,68,68,0.3); border-radius: 12px; padding: 16px 20px; color: var(--red); font-family: 'Space Mono', monospace; font-size: 13px; display: none; margin-top: 16px; }
  @media (max-width: 600px) { .input-row { grid-template-columns: 1fr; } .results-grid { grid-template-columns: 1fr 1fr; } .card { padding: 24px; } }
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="badge">🌱 HACKATHON 2025 · GREENCODE</div>
    <h1>Code <span class="green">Greener.</span><br>Emit Less.</h1>
    <p class="subtitle">// Measure CO₂ saved by algorithm optimization</p>
  </header>
  <div class="card">
    <div class="section-label">// Configure Analysis</div>
    <div class="input-row">
      <div class="input-group">
        <label>INPUT SIZE (n)</label>
        <input type="number" id="inputN" value="1000" min="1" max="1000000"/>
      </div>
      <div class="input-group">
        <label>ORIGINAL ALGORITHM</label>
        <div class="toggle-group">
          <button class="toggle-btn active" id="btnBad" onclick="setMode(true)">O(n²) Bad</button>
          <button class="toggle-btn" id="btnGood" onclick="setMode(false)">O(n) Good</button>
        </div>
      </div>
    </div>
    <button class="btn-calculate" id="calcBtn" onclick="calculate()">⚡ CALCULATE CARBON SAVINGS</button>
    <div class="error-msg" id="errorMsg"></div>
  </div>
  <div class="card results" id="results">
    <div class="section-label">// Results</div>
    <div class="results-grid">
      <div class="stat-card highlight"><div class="stat-value" id="resCO2">—</div><div class="stat-label">CO₂ Saved (grams)</div></div>
      <div class="stat-card"><div class="stat-value" id="resEfficiency">—</div><div class="stat-label">Efficiency Boost</div></div>
      <div class="stat-card"><div class="stat-value" id="resComplexity">—</div><div class="stat-label">Complexity Reduction</div></div>
    </div>
    <div class="comparison">
      <div class="compare-row"><span class="compare-label">BEFORE</span><div class="bar-track"><div class="bar-fill bad" id="barBad"></div></div><span class="compare-ops" id="opsBad">—</span></div>
      <div class="compare-row"><span class="compare-label">AFTER</span><div class="bar-track"><div class="bar-fill good" id="barGood"></div></div><span class="compare-ops" id="opsGood">—</span></div>
    </div>
    <div class="success-msg" id="successMsg"></div>
  </div>
</div>
<script>
  let wasBad = true;
  function setMode(bad) {
    wasBad = bad;
    document.getElementById('btnBad').classList.toggle('active', bad);
    document.getElementById('btnGood').classList.toggle('active', !bad);
  }
  async function calculate() {
    const n = parseInt(document.getElementById('inputN').value) || 1000;
    const btn = document.getElementById('calcBtn');
    const errMsg = document.getElementById('errorMsg');
    btn.textContent = '⏳ Calculating...';
    errMsg.style.display = 'none';
    try {
      const res = await fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ n, was_bad: wasBad })
      });
      const data = await res.json();
      if (data.status !== 'success') throw new Error(data.message);
      document.getElementById('results').classList.add('show');
      document.getElementById('resCO2').textContent = data.carbon_saved_grams;
      document.getElementById('resEfficiency').textContent = data.efficiency_boost;
      document.getElementById('resComplexity').textContent = data.original_complexity + ' → ' + data.optimized_complexity;
      document.getElementById('opsBad').textContent = data.original_ops.toLocaleString() + ' ops';
      document.getElementById('opsGood').textContent = data.optimized_ops.toLocaleString() + ' ops';
      setTimeout(() => {
        document.getElementById('barBad').style.width = '100%';
        const ratio = data.optimized_ops / data.original_ops;
        document.getElementById('barGood').style.width = Math.max(ratio * 100, 1) + '%';
      }, 100);
      document.getElementById('successMsg').textContent = '🌿 ' + data.message;
    } catch (err) {
      errMsg.style.display = 'block';
      errMsg.textContent = '⚠ Error: ' + err.message;
    } finally {
      btn.textContent = '⚡ CALCULATE CARBON SAVINGS';
    }
  }
</script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args
        n = int(data.get('n', 1000))
        was_bad = str(data.get('was_bad', 'true')).lower() == 'true'
        original_ops = n ** 2 if was_bad else n
        green_ops = n
        saved_co2 = (original_ops - green_ops) * 0.00001
        return jsonify({
            "status": "success",
            "input_size": n,
            "original_complexity": "O(n\u00b2)" if was_bad else "O(n)",
            "optimized_complexity": "O(n)",
            "original_ops": original_ops,
            "optimized_ops": green_ops,
            "carbon_saved_grams": round(saved_co2, 4),
            "efficiency_boost": "99.9%" if was_bad else "0%",
            "message": f"Successfully saved {round(saved_co2, 2)}g of CO2!"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
