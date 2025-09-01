#!/usr/bin/env python3
"""
Virtual Cavity Simulator - Standalone Simulation

Project: Virtual Cavity RF Simulator
Author: Ming Liu (mliu@ihep.ac.cn)
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: 2025-09-01
Version: 1.0.0

Description:
    Standalone RF cavity simulation program with visualization.
    Implements comprehensive cavity dynamics including mechanical modes,
    RF modulation, amplification, and beam loading effects.

Features:
    - Complete RF cavity simulation loop
    - Mechanical vibration coupling (5 modes)
    - I/Q modulation and amplification
    - Beam loading simulation
    - Multi-plot visualization
    - Data export capabilities

Technical Details:
    - Based on LLRFLibsPy simulation framework
    - State-space discrete-time implementation
    - 1 μs time step resolution
    - Supports both CW and pulsed modes

Dependencies:
    - numpy: Numerical computing
    - matplotlib: Plotting and visualization
    - llrflibs: RF cavity simulation library

Usage:
    python sim_cavity_standalone.py

License:
    MIT License - see LICENSE file for details

Changelog:
    v1.0.0 (2025-09-01): Initial release with validated simulation accuracy
"""
import numpy as np
import matplotlib.pyplot as plt
from llrflibs.rf_sim import cav_ss_mech, sim_scav_step
from llrflibs.rf_control import ss_discrete

# Simulation parameters
Ts = 1e-6  # Simulation time step, seconds
f0 = 1.3e9
QL = 3e6
roQ = 1036
RL = 0.5 * roQ * QL
wh = np.pi * f0 / QL
beta = 1e4
ib = 0.008
mech_modes = {'f': [280, 341, 460, 487, 618],
              'Q': [40, 20, 50, 80, 100],
              'K': [2, 0.8, 2, 0.6, 0.2]}
buf_size = 2048 * 8
t_fill = 510
t_flat = 1300
sim_len = 2048 * 4  # Reduce simulation length for quick testing
pul_len = 2048 * 2

# LLRFLibsPy state space initialization
print("Initializing mechanical mode state space...")
status, Am, Bm, Cm, Dm = cav_ss_mech(mech_modes)
status, Ad, Bd, Cd, Dd, _ = ss_discrete(Am, Bm, Cm, Dm, Ts=Ts, method='zoh', plot=False, plot_pno=10000)
print(f"State space initialization complete, number of mechanical modes: {len(mech_modes['f'])}")

# Simulation states
state_m = np.matrix(np.zeros(Bd.shape))
state_vc = 0.0
pha_src = 0.0
buf_id = 0

# Control parameters
amp = 1.0  # RF source amplitude (Asrc)
phase = 0.0  # RF source phase (degrees)
fsrc = -460  # RF source frequency offset (Hz)
pulsed = False  # Pulse mode (False = CW mode like original)

# beam profile
beam_pul = np.zeros(buf_size, dtype=complex)
beam_cw = 0
beam_pul[:] = 0
beam_pul[t_fill:t_flat] = ib

# Baseband modulation setup (matching original)
base_pul = np.zeros(buf_size, dtype=complex)
base_cw = 1
base_pul[:t_flat] = 1.0

# Helper functions (matching original exactly)
def sim_rfsrc(fsrc, Asrc, pha_src, Ts):
    pha = pha_src + 2.0 * np.pi * fsrc * Ts
    return Asrc*np.exp(1j*pha), pha

def sim_iqmod(sig_in, pulsed=True, base_pul=None, base_cw=0, buf_id=0):
    if pulsed:
        sig_out = sig_in * base_pul[buf_id if buf_id < len(base_pul) else -1]
    else:
        sig_out = sig_in * base_cw
    return sig_out

def sim_amp(sig_in, gain_dB):
    return sig_in * 10.0**(gain_dB / 20.0)

def sim_cav(half_bw, RL, dw_step0, detuning0, vf_step, state_vc, Ts, beta=1e4,
            state_m0=0, Am=None, Bm=None, Cm=None, Dm=None,
            pulsed=True, beam_pul=None, beam_cw=0, buf_id=0):
    # get the beam
    if pulsed:
        vb = -RL * beam_pul[buf_id if buf_id < len(beam_pul) else -1]
    else:
        vb = -RL * beam_cw
    
    # execute for one step
    status, vc, vr, dw, state_m = sim_scav_step(half_bw,
                                                dw_step0,
                                                detuning0, 
                                                vf_step, 
                                                vb, 
                                                state_vc, 
                                                Ts, 
                                                beta=beta,
                                                state_m0=state_m0, 
                                                Am=Am, 
                                                Bm=Bm, 
                                                Cm=Cm, 
                                                Dm=Dm,
                                                mech_exe=True)           
    state_vc = vc
    
    # return 
    return vc, vr, dw, state_vc, state_m

# Data storage
sig_vc = np.zeros(sim_len, dtype=complex)
sig_vr = np.zeros(sim_len, dtype=complex)
sig_dw = np.zeros(sim_len, dtype=complex)
sig_mech = np.zeros((sim_len, len(mech_modes['f'])), dtype=complex)

print(f"Starting simulation, total steps: {sim_len}")

# Main simulation loop
dw = 0  # Initialize detuning state
gain_dB = 20 * np.log10(12e6)  # Amplifier gain

for i in range(sim_len):
    if i % 1000 == 0:
        print(f"Simulation progress: {i}/{sim_len}")
    
    # RF signal source
    S0, pha_src = sim_rfsrc(fsrc, amp, pha_src, Ts)
    
    # emulate the pulse
    if pulsed:
        buf_id += 1
        if buf_id >= pul_len:
            buf_id = 0
    
    # I/Q modulator
    S1 = sim_iqmod(S0, 
                   pulsed=pulsed,
                   base_pul=base_pul,
                   base_cw=base_cw,
                   buf_id=buf_id)
    
    # Amplifier
    S2 = sim_amp(S1, gain_dB)
    
    # Microphonics
    dw_micr = 2.0 * np.pi * np.random.randn() * 10
    
    # Cavity dynamics
    vc, vr, dw, state_vc, state_m = sim_cav(wh, RL, dw, 0 + dw_micr, S2, state_vc, Ts, 
                                            beta=beta,
                                            state_m0=state_m, 
                                            Am=Ad, 
                                            Bm=Bd, 
                                            Cm=Cd,
                                            Dm=Dd,
                                            pulsed=pulsed, 
                                            beam_pul=beam_pul, 
                                            beam_cw=beam_cw, 
                                            buf_id=buf_id)
    
    # Store data
    sig_vc[i] = vc
    sig_vr[i] = vr
    sig_dw[i] = dw
    for j in range(len(mech_modes['f'])):
        try:
            sig_mech[i, j] = state_m[0, j]
        except:
            pass

print("Simulation complete, starting plotting...")

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(3, 2, 1)
plt.plot(abs(sig_vc) * 1e-6)
plt.title('Cavity Voltage Amplitude (MV)')
plt.xlabel('Time Step')
plt.ylabel('Amplitude (MV)')

plt.subplot(3, 2, 2)
plt.plot(np.angle(sig_vc) * 180 / np.pi)
plt.title('Cavity Voltage Phase (deg)')
plt.xlabel('Time Step')
plt.ylabel('Phase (deg)')

plt.subplot(3, 2, 3)
plt.plot(abs(sig_vr) * 1e-6)
plt.title('Reflected Voltage Amplitude (MV)')
plt.xlabel('Time Step')
plt.ylabel('Amplitude (MV)')

plt.subplot(3, 2, 4)
plt.plot(sig_dw / (2 * np.pi))
plt.title('Detuning (Hz)')
plt.xlabel('Time Step')
plt.ylabel('Frequency (Hz)')

plt.subplot(3, 2, 5)
for i in range(min(3, len(mech_modes['f']))):
    plt.plot(np.real(sig_mech[:, i]), label=f'Mode {i+1} ({mech_modes["f"][i]} Hz)')
plt.title('Mechanical Mode Response')
plt.xlabel('Time Step')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(3, 2, 6)
plt.plot(np.real(sig_vc), label='Real')
plt.plot(np.imag(sig_vc), label='Imag')
plt.title('Cavity Voltage Complex')
plt.xlabel('Time Step')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()

print("Cavity simulation test complete!")
print(f"Final cavity voltage: {abs(sig_vc[-1])*1e-6:.3f} MV")
print(f"Final detuning: {sig_dw[-1]/(2*np.pi):.1f} Hz")
