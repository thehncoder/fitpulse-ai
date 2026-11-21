"""
FitPulse AI - Web Service & API Gateway
"""

from flask import Flask, render_template, request, jsonify
from core.sizing_engine import SizingIntelligenceEngine
from core.stylist_engine import GenerativeStylistEngine
from core.metrics_telemetry import ProductTelemetryTracker

app = Flask(__name__)
sizing_engine = SizingIntelligenceEngine()
stylist_engine = GenerativeStylistEngine()
telemetry = ProductTelemetryTracker()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/recommend-size', methods=['POST'])
def recommend_size():
    data = request.get_json() or {}
    ref_brand = data.get('reference_brand', 'levis')
    ref_size = data.get('reference_size', 'M')
    target_brand = data.get('target_brand', 'zara')
    category = data.get('category', 'shirt')
    fit_pref = data.get('fit_preference', 'regular')

    result = sizing_engine.calculate_fit(
        reference_brand=ref_brand,
        reference_size=ref_size,
        target_brand=target_brand,
        category=category,
        fit_preference=fit_pref
    )
    telemetry.record_request(result['latency_ms'], converted=True)
    return jsonify(result)

@app.route('/api/v1/style-assist', methods=['POST'])
def style_assist():
    data = request.get_json() or {}
    item = data.get('item_name', 'Oxford Cotton Shirt')
    category = data.get('category', 'shirt')
    occasion = data.get('occasion', 'casual')

    result = stylist_engine.generate_style_advice(
        item_name=item,
        category=category,
        occasion=occasion
    )
    return jsonify(result)

@app.route('/api/v1/metrics', methods=['GET'])
def get_metrics():
    return jsonify(telemetry.get_aggregate_metrics())

if __name__ == '__main__':
    print('FitPulse AI Server starting on http://127.0.0.1:5000')
    app.run(debug=True, port=5000)
