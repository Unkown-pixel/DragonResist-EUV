"""
DragonResist-EUV: Validation Test Suite
Validates simulation against real-world EUV lithography data
"""

import pytest
import numpy as np
from models.euv_exposure import EUVExposureModel

def test_photon_statistics():
    """Validate photon count against ASML specifications"""
    model = EUVExposureModel()
    stats = model.calculate_photon_statistics(target_area_um2=1.0)
    
    # ASML NXE:3800E at 30 mJ/cm² should have ~2.45e15 photons/cm²
    expected_photons_per_nm2 = 2.45e15 * 1e-14  # convert to per nm²
    assert abs(stats['photons_per_nm2'] - expected_photons_per_nm2) / expected_photons_per_nm2 < 0.02

def test_secondary_electron_yield():
    """Validate secondary electron yield model"""
    model = EUVExposureModel()
    
    # Create a simple pattern (single pixel exposure)
    pattern = np.zeros((10, 10))
    pattern[5, 5] = 1.0
    
    results = model.run_full_simulation(pattern, target_cd_nm=32.0)
    
    # For a single photon, electron map should have ~3.2 electrons
    electron_count = np.sum(results['electron_map'])
    assert 3.0 < electron_count < 3.4  # 3.2 ± 6%

def test_acid_diffusion():
    """Validate acid diffusion model against measured data"""
    model = EUVExposureModel()
    model.resist['acid_diffusion_length_nm'] = 5.2
    
    # Create a sharp edge pattern
    pattern = np.zeros((100, 100))
    pattern[:, 50:] = 1.0
    
    results = model.run_full_simulation(pattern, target_cd_nm=32.0)
    
    # Measure acid diffusion at the edge
    acid_profile = np.mean(results['diffused_acid'], axis=0)
    edge_width = np.argmax(acid_profile > 0.1) - np.argmax(acid_profile > 0.9)
    
    # Edge width should be ~2.35 * diffusion length (for Gaussian)
    expected_edge_width = 2.35 * 5.2
    assert abs(edge_width - expected_edge_width) / expected_edge_width < 0.05

def test_ler_at_32nm_hp():
    """Validate LER against SEMATECH database"""
    model = EUVExposureModel()
    model.tool['dose_mJ_cm2'] = 30.0
    
    # Create 32nm half-pitch line-space pattern
    height, width = 1000, 1000
    target_cd_nm = 16.0  # Half-pitch = 32nm
    pixel_size = model.constants['nm_per_pixel']
    
    pattern = np.zeros((height, width))
    line_width = int(target_cd_nm / pixel_size)
    pitch = int(32.0 / pixel_size)
    
    for x in range(0, width, pitch):
        pattern[:, x:x+line_width] = 1.0
    
    # Run Monte Carlo simulation (100 runs for statistics)
    lers = []
    for _ in range(100):
        results = model.run_full_simulation(pattern, target_cd_nm=16.0)
        lers.append(results['metrics']['ler_nm'])
    
    avg_ler = np.mean(lers)
    std_ler = np.std(lers)
    
    # SEMATECH target: 1.70-1.80 nm LER at 32nm HP, 30 mJ/cm²
    assert 1.65 < avg_ler < 1.85
    print(f"PASS: Simulated LER = {avg_ler:.2f} ± {std_ler:.2f} nm (target 1.70-1.80 nm)")

def test_process_window():
    """Validate process window against IMEC data"""
    model = EUVExposureModel()
    model.tool['dose_mJ_cm2'] = 30.0
    
    # Calculate process window for 32nm HP
    pw = model.calculate_process_window(target_cd_nm=16.0, steps=15)
    
    # Expected process window for 32nm HP: ~20% dose latitude, 40nm focus latitude
    dose_lat = (pw['dose_values'][-1] - pw['dose_values'][0]) * np.mean(np.diff(pw['dose_values']) > 0)
    focus_lat = (pw['focus_values'][-1] - pw['focus_values'][0]) * np.mean(np.diff(pw['focus_values']) > 0)
    
    assert 18.0 < dose_lat < 22.0  # 20% ± 10%
    assert 36.0 < focus_lat < 44.0  # 40nm ± 10%
    print(f"PASS: Simulated process window: {dose_lat:.1f}% dose latitude, {focus_lat:.1f}nm focus latitude")

def test_stochastic_defect_density():
    """Validate stochastic defect density model"""
    model = EUVExposureModel()
    model.tool['dose_mJ_cm2'] = 25.0  # Lower dose = more defects
    
    # Create dense pattern
    height, width = 1000, 1000
    target_cd_nm = 16.0
    pixel_size = model.constants['nm_per_pixel']
    
    pattern = np.zeros((height, width))
    line_width = int(target_cd_nm / pixel_size)
    pitch = int(32.0 / pixel_size)
    
    for x in range(0, width, pitch):
        pattern[:, x:x+line_width] = 1.0
    
    results = model.run_full_simulation(pattern, target_cd_nm=target_cd_nm)
    
    # At 25 mJ/cm², expect ~0.5-1.0 defects/um² for 32nm HP
    defect_density = results['metrics']['stochastic_defects_per_um2']
    assert 0.4 < defect_density < 1.2
    print(f"PASS: Simulated defect density = {defect_density:.2f} defects/um² (expected 0.5-1.0)")
