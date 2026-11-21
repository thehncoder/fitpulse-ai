import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
Test suite for FitPulse AI Sizing and Telemetry Engines
"""

import pytest
from core.sizing_engine import SizingIntelligenceEngine
from core.stylist_engine import GenerativeStylistEngine
from core.metrics_telemetry import ProductTelemetryTracker

def test_sizing_baseline():
    engine = SizingIntelligenceEngine()
    res = engine.calculate_fit('levis', 'M', 'levis', 'shirt', 'regular')
    assert res['recommended_size'] == 'M'
    assert res['confidence_score'] >= 85.0
    assert res['latency_ms'] < 100.0  # Guardrail test

def test_cross_brand_offset():
    # Zara runs smaller than Levis; someone wearing Levis M typically needs L in Zara for regular fit
    engine = SizingIntelligenceEngine()
    res = engine.calculate_fit('levis', 'M', 'zara', 'shirt', 'regular')
    assert res['recommended_size'] in ('M', 'L')
    assert 'recommended_size' in res
    assert res['return_risk_score'] >= 0.0

def test_latency_guardrail():
    engine = SizingIntelligenceEngine()
    for _ in range(50):
        res = engine.calculate_fit('h&m', 'L', 'nike', 'shirt', 'slim')
        assert res['latency_ms'] < 100.0

def test_stylist_engine():
    stylist = GenerativeStylistEngine()
    res = stylist.generate_style_advice('Linen Shirt', 'shirt', 'casual')
    assert len(res['recommended_pairings']) > 0
    assert 'curated_stylist_tip' in res

def test_telemetry():
    tracker = ProductTelemetryTracker()
    tracker.record_request(15.2, converted=True)
    tracker.record_request(22.8, converted=True)
    metrics = tracker.get_aggregate_metrics()
    assert metrics['business_impact_model']['net_return_reduction'] == '4.5%'
    assert metrics['business_impact_model']['relative_conversion_lift'] == '6.8%'
    assert metrics['sla_guardrail_status'] == 'COMPLIANT (< 100ms)'
