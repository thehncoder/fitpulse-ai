"""
FitPulse AI - Generative Stylist Engine
Rules-based prompt and styling intelligence for cross-category outfit recommendations.
"""

import time
import random
from typing import Dict, Any, List

STYLE_KNOWLEDGE_BASE = {
    'shirt': {
        'casual': {
            'pairing': ['Slim Chinos in Olive/Beige', 'White Minimalist Sneakers', 'Leather Chrono Watch'],
            'color_accents': ['Earth Tones', 'Navy', 'Muted Grey'],
            'advice': 'Roll sleeves to mid-forearm for a relaxed, sharp aesthetic.'
        },
        'formal': {
            'pairing': ['Tailored Navy Trousers', 'Dark Brown Oxford Shoes', 'Full-Grain Leather Belt'],
            'color_accents': ['Charcoal', 'Burgundy', 'Classic White'],
            'advice': 'Tuck cleanly with collar stays to preserve architectural lines.'
        }
    },
    'jeans': {
        'casual': {
            'pairing': ['Structured Heavyweight T-Shirt', 'Retro Runner Sneakers', 'Utility Overshirt'],
            'color_accents': ['Monochrome White/Black', 'Washed Indigo'],
            'advice': 'Single cuff hem above the ankle maintains clean silhouette.'
        }
    },
    'jacket': {
        'casual': {
            'pairing': ['Merino Wool Crewneck', 'Dark Denim', 'Suede Chelsea Boots'],
            'color_accents': ['Cognac', 'Forest Green', 'Black'],
            'advice': 'Leave unbuttoned for visual layering depth.'
        }
    }
}

class GenerativeStylistEngine:
    def __init__(self):
        self.kb = STYLE_KNOWLEDGE_BASE

    def generate_style_advice(self, item_name: str, category: str = 'shirt', occasion: str = 'casual') -> Dict[str, Any]:
        start_time = time.perf_counter()
        
        cat = category.lower().strip()
        occ = occasion.lower().strip()

        cat_data = self.kb.get(cat, self.kb['shirt'])
        style_pack = cat_data.get(occ, cat_data.get('casual'))

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            'item': item_name,
            'category': category.title(),
            'occasion': occasion.title(),
            'recommended_pairings': style_pack['pairing'],
            'color_palette': style_pack['color_accents'],
            'curated_stylist_tip': style_pack['advice'],
            'latency_ms': round(elapsed_ms, 2)
        }
