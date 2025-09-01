#!/usr/bin/env python3
"""
Virtual Cavity Simulator - GUI Launcher

Project: Virtual Cavity RF Simulator
Author: Ming Liu (mliu@ihep.ac.cn)
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: 2025-09-01
Version: 1.0.0

Description:
    Launcher script for the Virtual Cavity Simulation GUI.
    Handles dependency checking and launches the main GUI application.

Features:
    - Automatic dependency verification
    - LLRFLibsPy availability checking
    - Error handling and user guidance
    - Clean application startup

Dependencies:
    - numpy: Numerical computing
    - matplotlib: Plotting and visualization
    - tkinter: GUI framework (usually included with Python)
    - llrflibs: RF cavity simulation library

Usage:
    python launch_gui.py

License:
    MIT License - see LICENSE file for details

Changelog:
    v1.0.0 (2025-09-01): Initial release with dependency checking
"""
import sys
import os

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        'numpy',
        'matplotlib', 
        'tkinter'  # Usually comes with Python
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_llrflibs():
    """Check LLRFLibsPy availability"""
    try:
        from llrflibs.rf_sim import cav_ss_mech, sim_scav_step
        from llrflibs.rf_control import ss_discrete
        print("✓ LLRFLibsPy is available")
        return True
    except ImportError as e:
        print(f"✗ LLRFLibsPy import error: {e}")
        print("Please ensure LLRFLibsPy is properly installed")
        return False

def launch_gui():
    """Launch the GUI application"""
    try:
        from advanced_cavity_gui import main
        print("Starting Advanced Cavity Simulation GUI...")
        main()
    except Exception as e:
        print(f"Error launching GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Advanced Cavity Simulation GUI Launcher")
    print("=" * 50)
    
    print("\nChecking basic dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\nChecking LLRFLibsPy...")
    if not check_llrflibs():
        print("\nWarning: LLRFLibsPy not available. GUI will launch but simulation may not work.")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("\nAll dependencies checked. Launching GUI...")
    launch_gui()
