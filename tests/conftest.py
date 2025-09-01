#!/usr/bin/env python3
"""
Test Configuration for Virtual Cavity RF Simulator

Project: Virtual Cavity RF Simulator
Author: Ming Liu (mliu@ihep.ac.cn)
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: 2025-09-01
Version: 1.0.0

Description:
    Pytest configuration file with fixtures and test setup.

License:
    MIT License - see LICENSE file for details
"""

import pytest
import numpy as np
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def cavity_parameters():
    """
    Standard cavity parameters for testing
    """
    return {
        'f0': 1.3e9,      # Resonant frequency (Hz)
        'QL': 3e6,        # Loaded quality factor
        'beta': 1e4,      # Coupling coefficient
        'roQ': 1036,      # R/Q ratio
        'Ts': 1e-6,       # Time step (s)
        'ib': 0.008,      # Beam current (A)
    }

@pytest.fixture
def mechanical_modes():
    """
    Standard mechanical mode parameters for testing
    """
    return {
        'f': [280, 341, 460, 487, 618],    # Frequencies (Hz)
        'Q': [40, 20, 50, 80, 100],        # Quality factors
        'K': [2, 0.8, 2, 0.6, 0.2]        # Coupling strengths
    }

@pytest.fixture
def simulation_parameters():
    """
    Standard simulation parameters for testing
    """
    return {
        'num_steps': 100,      # Short test run
        'amplitude': 1.0,      # RF amplitude
        'phase': 0.0,          # RF phase (degrees)
        'frequency_offset': -460,  # Frequency offset (Hz)
    }

@pytest.fixture
def sample_data():
    """
    Generate sample simulation data for testing
    """
    num_points = 100
    time_data = np.linspace(0, 0.0001, num_points)  # 100 μs
    
    # Simple sinusoidal cavity voltage
    frequency = 1000  # 1 kHz for testing
    cavity_voltage = 10e6 * np.exp(1j * 2 * np.pi * frequency * time_data)
    
    # Simple reflected voltage (fraction of cavity voltage)
    reflected_voltage = 0.1 * cavity_voltage
    
    # Linear detuning for testing
    detuning = np.linspace(-100, 100, num_points)
    
    return {
        'time': time_data,
        'cavity_voltage': cavity_voltage,
        'reflected_voltage': reflected_voltage,
        'detuning': detuning
    }

@pytest.fixture(scope="session")
def test_output_dir(tmp_path_factory):
    """
    Create temporary directory for test outputs
    """
    return tmp_path_factory.mktemp("test_outputs")

# Configure matplotlib for headless testing
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Test configuration
pytest_plugins = []

def pytest_configure(config):
    """
    Configure pytest with custom markers
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "gui: marks tests that require GUI (may be skipped in CI)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )

def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers automatically
    """
    for item in items:
        # Add slow marker to tests that take long time
        if "parameter_scan" in item.name or "long_simulation" in item.name:
            item.add_marker(pytest.mark.slow)
        
        # Add gui marker to GUI tests
        if "gui" in item.name or "widget" in item.name:
            item.add_marker(pytest.mark.gui)

@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    Set up test environment before each test
    """
    # Set random seed for reproducible tests
    np.random.seed(42)
    
    # Suppress warnings during testing
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    yield
    
    # Cleanup after test
    # (Add any cleanup code here if needed)
