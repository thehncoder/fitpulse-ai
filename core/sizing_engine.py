"""
FitPulse AI - Sizing Intelligence Engine
Cross-brand dimensional normalization and return-risk scoring for fashion e-commerce storefronts.
"""

import time
import math
from typing import Dict, Any, Tuple

# Baseline standardized garment dimensions in inches (Chest, Waist, Shoulder, Length)
STANDARD_BODY_MEASUREMENTS = {
    'XS': {'chest': (34, 36), 'waist': (28, 30), 'shoulder': 16.5, 'hip': 35},
    'S':  {'chest': (36, 38), 'waist': (30, 32), 'shoulder': 17.2, 'hip': 37},
    'M':  {'chest': (38, 40), 'waist': (32, 34), 'shoulder': 18.0, 'hip': 39},
    'L':  {'chest': (40, 42), 'waist': (34, 36), 'shoulder': 18.8, 'hip': 41},
    'XL': {'chest': (42, 44), 'waist': (36, 38), 'shoulder': 19.5, 'hip': 43},
    'XXL':{'chest': (44, 47), 'waist': (38, 41), 'shoulder': 20.2, 'hip': 45}
}

# Brand tolerance offsets (in inches) relative to standard international sizing
BRAND_OFFSETS = {
    'zara': {'chest': -0.8, 'waist': -0.7, 'cut': 'European Slim'},
    'h&m': {'chest': -0.3, 'waist': -0.2, 'cut': 'Regular Standard'},
    'levis': {'chest': 0.6, 'waist': 0.5, 'cut': 'American Relaxed'},
    'uniqlo': {'chest': 0.0, 'waist': 0.0, 'cut': 'True to Size'},
    'mango': {'chest': -0.5, 'waist': -0.4, 'cut': 'Tailored European'},
    'nike': {'chest': 0.4, 'waist': 0.3, 'cut': 'Athletic Cut'},
    'standard': {'chest': 0.0, 'waist': 0.0, 'cut': 'Standard'}
}

class SizingIntelligenceEngine:
    def __init__(self):
        self.brand_matrix = BRAND_OFFSETS
        self.dimension_table = STANDARD_BODY_MEASUREMENTS

    def calculate_fit(self, 
                      reference_brand: str, 
                      reference_size: str, 
                      target_brand: str, 
                      category: str = 'shirt', 
                      fit_preference: str = 'regular') -> Dict[str, Any]:
        """
        Calculates optimal size for target garment based on reference brand sizing,
        returns confidence score, fit explanation, and return-risk probability.
        """
        start_time = time.perf_counter()
        
        ref_brand_key = reference_brand.lower().strip()
        target_brand_key = target_brand.lower().strip()
        ref_size = reference_size.upper().strip()

        if ref_size not in self.dimension_table:
            ref_size = 'M'

        ref_offset = self.brand_matrix.get(ref_brand_key, self.brand_matrix['standard'])
        target_offset = self.brand_matrix.get(target_brand_key, self.brand_matrix['standard'])

                # Calculate estimated physical user chest from reference brand size
        std_chest_mid = (self.dimension_table[ref_size]['chest'][0] + self.dimension_table[ref_size]['chest'][1]) / 2.0
        # If reference brand has +0.6 offset, it means the garment is 0.6 inches larger than standard.
        # User who fits comfortably in reference brand size M has chest ~ std_chest_mid
        user_body_chest = std_chest_mid

        # Adjust for fit preference
        pref_delta = 0.0
        if fit_preference.lower() == 'slim':
            pref_delta = -1.0
        elif fit_preference.lower() in ('oversized', 'relaxed'):
            pref_delta = 1.5

        # To find target brand size:
        # If target brand runs smaller (e.g. Zara -0.8), the user needs a garment with larger standard size to fit their chest!
        target_effective_chest = user_body_chest + (ref_offset['chest'] - target_offset['chest']) + pref_delta

        # Find best matching size in standard table
        best_size = 'M'
        min_diff = 999.0
        for sz, dims in self.dimension_table.items():
            mid_val = (dims['chest'][0] + dims['chest'][1]) / 2.0
            diff = abs(target_effective_chest - mid_val)
            if diff < min_diff:
                min_diff = diff
                best_size = sz

        # Confidence calculation
        confidence = max(82.0, min(98.5, 100.0 - (min_diff * 9.5)))
        
        # Return risk scoring (0.0 to 1.0)
        # Higher discrepancy between brands increases return probability
        brand_disparity = abs(ref_offset['chest'] - target_offset['chest'])
        base_return_risk = 0.28  # Industry average ~28%
        # Our tool mitigates risk when confidence is high
        calculated_return_risk = max(0.04, base_return_risk - (confidence / 400.0) + (brand_disparity * 0.02))

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Construct actionable explanation
        explanation = f"Based on your {reference_brand.title()} size {ref_size}, {target_brand.title()} runs {target_offset['cut'].lower()}. "
        if best_size == ref_size:
            explanation += f"Size {best_size} will give you your requested {fit_preference} fit."
        else:
            explanation += f"We recommend sizing to {best_size} for an ideal {fit_preference} fit."

        return {
            'recommended_size': best_size,
            'confidence_score': round(confidence, 1),
            'fit_explanation': explanation,
            'return_risk_score': round(calculated_return_risk * 100, 1),
            'target_brand_cut': target_offset['cut'],
            'latency_ms': round(elapsed_ms, 2),
            'latency_status': 'PASS (Guardrail < 100ms)' if elapsed_ms < 100.0 else 'WARN'
        }
