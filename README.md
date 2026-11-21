# ⚡ FitPulse AI — Fashion Sizing & Style Intelligence Engine

> An open-source, ultra-low latency GenAI sizing recommendation, return-risk mitigation, and automated outfit styling engine for modern fashion e-commerce storefronts.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/)
[![Latency SLA](https://img.shields.io/badge/P95%20Latency-%3C50ms-success.svg)]()
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

---

## 🎯 1. The Core E-Commerce Problem
* **The Returns Crisis:** In global apparel e-commerce, return rates hover between **30% and 35%**. Over **50% of these returns** stem directly from **size and fit uncertainty** rather than garment defects.
* **Customer Friction & Bracketing:** Shoppers frequently engage in *"bracketing"* (ordering multiple sizes of the identical item with the upfront intention of returning one). This ties up high-velocity inventory and inflates reverse-logistics shipping costs by 18–22% per returned unit.
* **Catalog Inconsistency:** Brand size charts are notoriously fragmented (e.g., a *Medium* in European tailored cuts fits like a *Small* in relaxed American cuts).

---

## 💡 2. The FitPulse Solution
**FitPulse AI** bridges the gap between consumer fit expectations and heterogeneous catalog specifications directly on the Product Detail Page (PDP):
1. **Cross-Brand Size Normalization:** Maps user sizing preferences against a cross-brand dimensional matrix (standardizing chest, waist, and shoulder variances across international brands like Zara, Levi's, H&M, Uniqlo).
2. **Dynamic Return-Risk Scoring:** Computes real-time return probability score based on dimensional variance before purchase.
3. **Generative Style Assistant:** Generates contextual outfit pairings and stylist tips for enhanced cart value.
4. **Sub-100ms Performance Guardrail:** Engineered for high-throughput e-commerce traffic without degrading Core Web Vitals.

---

## 📊 3. Business Impact & Product Metrics Model

| Metric | Baseline | Target with FitPulse AI | Measurement Method |
|---|---|---|---|
| **Apparel Return Rate** | 30.0% | **25.5% (-4.5% net)** | Cohort return differential over 30-day post-delivery cycle |
| **Cart-to-Checkout Conversion** | 30.0% | **32.0% (+6.8% lift)** | A/B testing checkout funnel conversion on PDP traffic |
| **Inference Latency SLA** | N/A | **< 100ms (P95 < 50ms)** | Client telemetry / API response time tracking |
| **North Star Metric** | N/A | **Fit-Accurate Checkout Rate** | % of clothing orders completed without a size-related return |

---

## 🏗️ 4. System Architecture

`	ext
[ Consumer on Storefront PDP ]
             │
             ▼
   [ FitPulse Web API / Endpoint ]
             │
   ┌─────────┴──────────────────────┐
   ▼                                ▼
[ Sizing Intelligence Engine ]   [ GenAI Stylist Engine ]
  • Cross-Brand Matrix             • Prompt Orchestration
  • Dimension Normalization        • Color Harmony Rules
  • Return-Risk Scorer             • Complementary Pairings
   │                                │
   └─────────┬──────────────────────┘
             ▼
[ Product Telemetry & SLA Guardrail ] (Latency < 100ms)
             │
             ▼
[ Structured JSON Response to Storefront UI ]
`

---

## 🚀 5. Quickstart Guide

### Prerequisites
* Python 3.10 or higher
* Git

### Installation
`ash
# Clone the repository
git clone https://github.com/thehncoder/fitpulse-ai.git
cd fitpulse-ai

# Install dependencies
pip install -r requirements.txt
`

### Running the Local Web Dashboard & API
`ash
python app.py
`
Open your browser and navigate to:  
👉 **http://127.0.0.1:5000**

### Running Unit Tests & Latency Guardrails
`ash
pytest tests/
`

---

## 🔌 6. API Reference

### 1. Predict Optimal Size
* **Endpoint:** POST /api/v1/recommend-size
* **Payload:**
`json
{
  "reference_brand": "levis",
  "reference_size": "M",
  "target_brand": "zara",
  "category": "shirt",
  "fit_preference": "regular"
}
`
* **Sample Response:**
`json
{
  "recommended_size": "L",
  "confidence_score": 92.4,
  "fit_explanation": "Based on your Levis size M, Zara runs european slim. We recommend sizing to L for an ideal regular fit.",
  "return_risk_score": 7.8,
  "target_brand_cut": "European Slim",
  "latency_ms": 14.2,
  "latency_status": "PASS (Guardrail < 100ms)"
}
`

### 2. Generative Style Assistant
* **Endpoint:** POST /api/v1/style-assist
* **Payload:**
`json
{
  "item_name": "Textured Linen Shirt",
  "category": "shirt",
  "occasion": "casual"
}
`

### 3. Product Telemetry & Metrics
* **Endpoint:** GET /api/v1/metrics

---

## 🧪 7. Test Suite Coverage
* Cross-brand tolerance regression testing
* Sub-100ms latency SLA enforcement
* Return-risk boundary validation
* Stylist recommendation schema compliance

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
