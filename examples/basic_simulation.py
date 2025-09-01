#!/usr/bin/env python3
"""
Basic Simulation Example

Project: Virtual Cavity RF Simulator
Author: Ming Liu (mliu@ihep.ac.cn)
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: 2025-09-01
Version: 1.0.0

Description:
    Basic example demonstrating how to use the Virtual Cavity RF Simulator
    for simple cavity simulation without GUI.

Usage:
    python basic_simulation.py

License:
    MIT License - see LICENSE file for details
"""

import numpy as np
import matplotlib.pyplot as plt
from llrflibs.rf_sim import cav_ss_mech, sim_scav_step
from llrflibs.rf_control import ss_discrete

def basic_cavity_simulation():
    """
    Demonstrate basic cavity simulation
    """
    print("Virtual Cavity RF Simulator - Basic Example")
    print("=" * 50)
    
    # Simulation parameters
    Ts = 1e-6  # Time step (1 μs)
    num_steps = 5000  # Number of simulation steps
    
    # Cavity parameters
    f0 = 1.3e9  # Resonant frequency (1.3 GHz)
    QL = 3e6    # Loaded quality factor
    beta = 1e4  # Coupling coefficient
    roQ = 1036  # R/Q ratio
    RL = 0.5 * roQ * QL  # Load resistance
    wh = np.pi * f0 / QL  # Half bandwidth
    
    # Mechanical modes
    mech_modes = {
        'f': [280, 341, 460, 487, 618],  # Frequencies (Hz)
        'Q': [40, 20, 50, 80, 100],      # Quality factors
        'K': [2, 0.8, 2, 0.6, 0.2]      # Coupling strengths
    }
    
    # Initialize state space model
    print("Initializing mechanical state space model...")
    status, Am, Bm, Cm, Dm = cav_ss_mech(mech_modes)
    status, Ad, Bd, Cd, Dd, _ = ss_discrete(
        Am, Bm, Cm, Dm, Ts=Ts, method='zoh', plot=False, plot_pno=10000)
    
    # Initial conditions
    state_vc = 0.0  # Cavity voltage state
    state_m = np.matrix(np.zeros(Bd.shape))  # Mechanical states
    dw = 0  # Detuning
    
    # RF parameters
    amplitude = 1.0  # RF amplitude
    frequency_offset = -460  # Frequency offset (Hz)
    beam_current = 0.008  # Beam current (A)
    
    # Storage arrays
    time_array = np.zeros(num_steps)
    cavity_voltage = np.zeros(num_steps, dtype=complex)
    reflected_voltage = np.zeros(num_steps, dtype=complex)
    detuning_array = np.zeros(num_steps)
    
    print(f"Running simulation for {num_steps} steps...")
    
    # Simulation loop
    for step in range(num_steps):
        current_time = step * Ts
        time_array[step] = current_time
        
        # RF source signal
        rf_signal = amplitude * np.exp(1j * 2 * np.pi * frequency_offset * current_time)
        
        # Beam voltage
        vb = -RL * beam_current
        
        # Microphonics (random vibrations)
        dw_micr = 2.0 * np.pi * np.random.randn() * 10
        
        # Cavity simulation step
        status, vc, vr, dw, state_m = sim_scav_step(
            wh,                    # Half bandwidth
            dw,                    # Current detuning
            0 + dw_micr,          # Detuning step with microphonics
            rf_signal,            # Forward voltage
            vb,                   # Beam voltage
            state_vc,             # Current cavity state
            Ts,                   # Time step
            beta=beta,            # Coupling coefficient
            state_m0=state_m,     # Mechanical states
            Am=Ad, Bm=Bd, Cm=Cd, Dm=Dd,  # State space matrices
            mech_exe=True         # Enable mechanical coupling
        )
        
        # Update states
        state_vc = vc
        
        # Store results
        cavity_voltage[step] = vc
        reflected_voltage[step] = vr
        detuning_array[step] = dw / (2 * np.pi)  # Convert to Hz
        
        # Progress indicator
        if step % 1000 == 0:
            progress = (step / num_steps) * 100
            print(f"Progress: {progress:.1f}%")
    
    print("Simulation completed!")
    
    # Calculate results
    vc_magnitude = np.abs(cavity_voltage) * 1e-6  # Convert to MV
    vc_phase = np.angle(cavity_voltage) * 180 / np.pi  # Convert to degrees
    vr_magnitude = np.abs(reflected_voltage) * 1e-6  # Convert to MV
    
    # Print summary statistics
    print(f"\nSimulation Results:")
    print(f"Average cavity voltage: {np.mean(vc_magnitude):.2f} MV")
    print(f"Peak cavity voltage: {np.max(vc_magnitude):.2f} MV")
    print(f"Average reflected voltage: {np.mean(vr_magnitude):.2f} MV")
    print(f"Final detuning: {detuning_array[-1]:.1f} Hz")
    
    # Create plots
    create_plots(time_array, vc_magnitude, vc_phase, vr_magnitude, detuning_array)
    
    return time_array, cavity_voltage, reflected_voltage, detuning_array

def create_plots(time_array, vc_magnitude, vc_phase, vr_magnitude, detuning_array):
    """
    Create visualization plots
    """
    print("Creating plots...")
    
    # Convert time to milliseconds for better readability
    time_ms = time_array * 1000
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Virtual Cavity RF Simulator - Basic Example Results', fontsize=14)
    
    # Cavity voltage magnitude
    axes[0, 0].plot(time_ms, vc_magnitude, 'b-', linewidth=1)
    axes[0, 0].set_title('Cavity Voltage Magnitude')
    axes[0, 0].set_xlabel('Time (ms)')
    axes[0, 0].set_ylabel('Magnitude (MV)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Cavity voltage phase
    axes[0, 1].plot(time_ms, vc_phase, 'r-', linewidth=1)
    axes[0, 1].set_title('Cavity Voltage Phase')
    axes[0, 1].set_xlabel('Time (ms)')
    axes[0, 1].set_ylabel('Phase (degrees)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Reflected voltage magnitude
    axes[1, 0].plot(time_ms, vr_magnitude, 'g-', linewidth=1)
    axes[1, 0].set_title('Reflected Voltage Magnitude')
    axes[1, 0].set_xlabel('Time (ms)')
    axes[1, 0].set_ylabel('Magnitude (MV)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Detuning
    axes[1, 1].plot(time_ms, detuning_array, 'm-', linewidth=1)
    axes[1, 1].set_title('Frequency Detuning')
    axes[1, 1].set_xlabel('Time (ms)')
    axes[1, 1].set_ylabel('Detuning (Hz)')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("Plots displayed. Close the plot window to continue.")

def main():
    """
    Main function
    """
    try:
        # Run basic simulation
        time_data, vc_data, vr_data, detuning_data = basic_cavity_simulation()
        
        print("\nBasic simulation example completed successfully!")
        print("For more advanced features, try:")
        print("- python launch_gui.py  (GUI interface)")
        print("- python sim_cavity_standalone.py  (Standalone with more features)")
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Please ensure LLRFLibsPy is properly installed.")
        print("See docs/installation.md for installation instructions.")
        
    except Exception as e:
        print(f"Error during simulation: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    main()
