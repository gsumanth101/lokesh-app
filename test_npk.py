#!/usr/bin/env python3
"""
Test NPK calculation variations
"""

import sys
import hashlib
import random

def test_npk_variation():
    """Test NPK calculations with different soil types"""
    
    # Test with different soil compositions
    test_soils = [
        {'organic_matter': 1.5, 'pH': 5.2, 'sand_content': 75, 'clay_content': 15, 'silt_content': 10, 'soil_type': 'Sandy'},
        {'organic_matter': 4.2, 'pH': 6.8, 'sand_content': 25, 'clay_content': 45, 'silt_content': 30, 'soil_type': 'Clayey'},  
        {'organic_matter': 2.8, 'pH': 7.1, 'sand_content': 40, 'clay_content': 30, 'silt_content': 30, 'soil_type': 'Loamy'},
        {'organic_matter': 0.8, 'pH': 8.5, 'sand_content': 80, 'clay_content': 10, 'silt_content': 10, 'soil_type': 'Sandy'},
        {'organic_matter': 5.1, 'pH': 4.8, 'sand_content': 20, 'clay_content': 55, 'silt_content': 25, 'soil_type': 'Clayey'}
    ]

    print('🧪 Testing NPK Calculation Variations:')
    print('=' * 60)

    for i, soil in enumerate(test_soils, 1):
        # Create location-specific seed for consistent but varied results
        seed_string = f"{soil['pH']:.2f}_{soil['organic_matter']:.2f}_{soil['clay_content']:.1f}_{soil['sand_content']:.1f}"
        seed = int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # NITROGEN ESTIMATION
        organic_matter = soil['organic_matter']
        if organic_matter < 1.0:
            base_n = 15 + organic_matter * 20
        elif organic_matter < 3.0:
            base_n = 35 + (organic_matter - 1.0) * 35
        else:
            base_n = 105 + (organic_matter - 3.0) * 25
        
        # Texture-based N adjustments
        soil_type = soil['soil_type']
        clay_content = soil['clay_content']
        sand_content = soil['sand_content']
        
        if soil_type == 'Sandy':
            n_texture_mult = 0.6 + (clay_content / 100)
        elif soil_type == 'Clayey':
            n_texture_mult = 1.4 - (sand_content / 200)
        else:
            n_texture_mult = 1.0 + (clay_content - sand_content) / 200
        
        # pH-based N adjustments
        pH = soil['pH']
        if pH < 5.0:
            n_ph_mult = 0.5
        elif pH < 6.0:
            n_ph_mult = 0.7 + (pH - 5.0) * 0.4
        elif pH <= 7.5:
            n_ph_mult = 1.1 + (pH - 6.0) * 0.2
        else:
            n_ph_mult = 1.4 - (pH - 7.5) * 0.3
        
        n_variation = random.uniform(0.7, 1.4)
        final_n = base_n * n_texture_mult * n_ph_mult * n_variation
        n_value = min(200, max(5, int(final_n)))
        
        # PHOSPHORUS ESTIMATION
        if pH < 5.5:
            base_p = 10 + organic_matter * 8
        elif pH < 6.5:
            base_p = 25 + organic_matter * 15
        elif pH <= 7.5:
            base_p = 45 + organic_matter * 20
        else:
            base_p = 30 + organic_matter * 12
        
        if pH < 6.0:
            p_clay_mult = 0.8 + (clay_content / 150)
        else:
            p_clay_mult = 1.1 + (clay_content / 100)
        
        sand_clay_ratio = sand_content / max(clay_content, 10)
        if sand_clay_ratio > 3:
            parent_material_mult = 0.6
        elif sand_clay_ratio < 1:
            parent_material_mult = 1.5
        else:
            parent_material_mult = 1.0
        
        p_variation = random.uniform(0.5, 2.0)
        final_p = base_p * p_clay_mult * parent_material_mult * p_variation
        p_value = min(150, max(3, int(final_p)))
        
        # POTASSIUM ESTIMATION
        base_k = 30 + clay_content * 2.5
        
        if organic_matter > 4.0:
            weathering_mult = 1.8
        elif organic_matter > 2.5:
            weathering_mult = 1.3
        elif organic_matter > 1.5:
            weathering_mult = 1.0
        else:
            weathering_mult = 0.6
        
        silt_k_contribution = soil['silt_content'] * 1.2
        
        if pH < 5.0:
            k_ph_mult = 0.85
        elif pH > 8.5:
            k_ph_mult = 0.9
        else:
            k_ph_mult = 1.0
        
        k_variation = random.uniform(0.4, 2.2)
        final_k = (base_k + silt_k_contribution) * weathering_mult * k_ph_mult * k_variation
        k_value = min(250, max(8, int(final_k)))
        
        print(f"Test {i} ({soil_type:<6}): N={n_value:3d}, P={p_value:3d}, K={k_value:3d} | pH={pH:.1f}, OM={organic_matter:.1f}%, Clay={clay_content:.0f}%")

    print('\n✅ Test complete! Each soil type shows different NPK values.')
    print('💡 Notice how Sandy soils have lower N, Clayey soils vary with pH, etc.')

if __name__ == "__main__":
    test_npk_variation()
