#!/usr/bin/env python3
"""
Python Reference Test - Extract core calculation from advanced_cavity_gui.py
for comparison with JavaScript implementation
"""

import numpy as np
import time

class PythonCavitySimulator:
    def __init__(self):
        # Simulation parameters (matching JavaScript exactly)
        self.Ts = 1e-6  # Time step
        self.f0 = 1.3e9  # Cavity frequency
        self.QL = 3e6   # Loaded Q
        self.roQ = 1036 # R/Q
        self.beta = 1e4 # Coupling
        self.RL = 0.5 * self.roQ * self.QL
        
        # Derived parameters
        self.wh = np.pi * self.f0 / self.QL  # Half bandwidth
        self.gain_dB = 20 * np.log10(12e6)   # Amplifier gain
        self.gain_linear = 10**(self.gain_dB / 20.0)
        
        # Initial state
        self.vc = 0.0 + 0.0j  # Complex cavity voltage
        self.time = 0.0
        self.step_count = 0
        
        # Control parameters
        self.amp = 1.0
        self.phase = 0.0  # degrees
        self.fsrc = -460.0  # Hz
        self.beam_current = 0.008  # A
        
        print(f"Python Simulator Initialized:")
        print(f"  Half bandwidth: {self.wh:.3e} rad/s")
        print(f"  Gain (dB): {self.gain_dB:.1f}")
        print(f"  Gain (linear): {self.gain_linear:.3e}")
        print(f"  RL: {self.RL:.3e} Ohms")
    
    def sim_rfsrc(self, fsrc, Asrc, pha_src, Ts):
        """RF source simulation (from advanced_cavity_gui.py)"""
        pha = pha_src + 2.0 * np.pi * fsrc * Ts
        return Asrc * np.exp(1j * pha), pha
    
    def sim_amp(self, sig_in, gain_dB):
        """Amplifier simulation (from advanced_cavity_gui.py)"""
        return sig_in * 10.0**(gain_dB / 20.0)
    
    def sim_scav_step_simplified(self, wh, dw_step0, detuning0, vf_step, vb, state_vc, Ts, beta=1e4):
        """
        Simplified cavity step simulation (extracted from LLRFLibsPy algorithm)
        Based on the differential equation approach
        """
        # Cavity equation: dVc/dt = -(wh - j*dw)*Vc + 2*wh*(beta*Vf/(beta+1) + Vb)
        
        # Coupled forward voltage
        vf_coupled = beta * vf_step / (beta + 1)
        
        # Total drive
        drive_total = 2 * wh * (vf_coupled + vb)
        
        # Cavity dynamics factor
        factor = 1 - Ts * (wh - 1j * (detuning0))
        
        # Update cavity voltage
        vc_new = factor * state_vc + Ts * drive_total
        
        # Calculate reflected voltage
        vr = state_vc - vf_step
        
        return vc_new, vr, detuning0
    
    def step(self):
        """Execute one simulation step"""
        # Update time
        self.time += self.Ts
        self.step_count += 1
        
        # RF source (base signal)
        S0 = self.amp * np.exp(1j * np.deg2rad(self.phase)) * np.exp(1j * 2 * np.pi * self.fsrc * self.time)
        
        # Apply amplifier gain
        S2 = self.sim_amp(S0, self.gain_dB)
        
        # Beam voltage
        vb = -self.RL * self.beam_current
        
        # Microphonics (simple random detuning)
        dw_micr = 2.0 * np.pi * np.random.randn() * 10
        
        # Cavity simulation
        self.vc, vr, dw = self.sim_scav_step_simplified(
            self.wh, 0, dw_micr, S2, vb, self.vc, self.Ts, self.beta)
        
        # Calculate results
        vc_magnitude = abs(self.vc)
        vc_phase = np.angle(self.vc) * 180 / np.pi
        vr_magnitude = abs(vr)
        
        # Power calculations
        R_cavity = self.roQ * self.QL
        forward_power = abs(S2)**2 / (2 * R_cavity) / 1000  # kW
        reflected_power = abs(vr)**2 / (2 * R_cavity) / 1000  # kW
        
        # Stored energy
        stored_energy = abs(self.vc)**2 * self.QL / (2 * R_cavity * 2 * np.pi * self.f0)
        
        return {
            'time': self.time * 1e6,  # Convert to microseconds
            'vc_magnitude': vc_magnitude / 1e6,  # Convert to MV
            'vc_phase': vc_phase,
            'vr_magnitude': vr_magnitude / 1e6,  # Convert to MV
            'forward_power': forward_power,
            'reflected_power': reflected_power,
            'detuning': dw / (2 * np.pi),  # Convert to Hz
            'beam_current': self.beam_current,
            'stored_energy': stored_energy,
            'vf_magnitude': abs(S2) / 1e6  # Forward voltage in MV
        }

def run_python_test(steps=100):
    """Run Python reference test"""
    print("=" * 60)
    print("PYTHON REFERENCE TEST")
    print("=" * 60)
    
    sim = PythonCavitySimulator()
    
    print(f"\nRunning {steps} simulation steps...")
    
    # Store results for analysis
    results = []
    
    # Run simulation
    for i in range(steps):
        result = sim.step()
        results.append(result)
        
        # Print every 20 steps
        if i % 20 == 0:
            print(f"Step {i:3d}: "
                  f"Vc={result['vc_magnitude']:.3f} MV, "
                  f"Pf={result['forward_power']:.1f} kW, "
                  f"Pr={result['reflected_power']:.1f} kW, "
                  f"Det={result['detuning']:.1f} Hz")
    
    # Final statistics
    final = results[-1]
    print(f"\nFINAL PYTHON VALUES (Step {steps}):")
    print(f"  Cavity Voltage: {final['vc_magnitude']:.6f} MV")
    print(f"  Cavity Phase: {final['vc_phase']:.3f}°")
    print(f"  Forward Power: {final['forward_power']:.3f} kW")
    print(f"  Reflected Power: {final['reflected_power']:.3f} kW")
    print(f"  Forward Voltage: {final['vf_magnitude']:.6f} MV")
    print(f"  Detuning: {final['detuning']:.3f} Hz")
    print(f"  Stored Energy: {final['stored_energy']:.6f} J")
    
    # Calculate averages over last 50 steps for steady state
    last_50 = results[-50:]
    avg_vc = np.mean([r['vc_magnitude'] for r in last_50])
    avg_pf = np.mean([r['forward_power'] for r in last_50])
    avg_pr = np.mean([r['reflected_power'] for r in last_50])
    
    print(f"\nSTEADY STATE AVERAGES (last 50 steps):")
    print(f"  Average Cavity Voltage: {avg_vc:.6f} MV")
    print(f"  Average Forward Power: {avg_pf:.3f} kW")
    print(f"  Average Reflected Power: {avg_pr:.3f} kW")
    
    return results

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    
    results = run_python_test(100)
    
    print(f"\nPython test completed. Results stored for comparison.")
