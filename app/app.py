from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


app = Flask(__name__)


# Prometheus metric: number of optimizations run
OPT_RUNS = Counter('costopt_runs_total', 'Number of optimization runs')


@app.route('/')
def index():
return jsonify({"message": "Cost Optimizer Service — SoftDrinks UK", "status": "ok"})


@app.route('/optimize', methods=['POST'])
def optimize():
data = request.get_json() or {}
# Very simple mocked logic: return suggestions for cost saving
usage = data.get('monthly_spend', 100)
suggestions = []
if usage > 1000:
suggestions.append('Move some workloads to spot instances or reserved capacity')
if usage > 300:
suggestions.append('Right-size RDS instance, consider gp3 storage')
if not suggestions:
suggestions.append('No immediate cost savings identified — monitor for anomalies')
OPT_RUNS.inc()
return jsonify({"input": usage, "suggestions": suggestions})


@app.route('/metrics')
def metrics():
return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
app.run(host='0.0.0.0', port=8000)