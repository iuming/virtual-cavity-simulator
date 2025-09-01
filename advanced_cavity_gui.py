#!/usr/bin/env python3
"""
Virtual Cavity Simulator - Advanced GUI Interface

Project: Virtual Cavity RF Simulator
Author: Ming Liu (mliu@ihep.ac.cn)
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: 2025-09-01
Version: 1.0.0

Description:
    Advanced graphical user interface for real-time RF cavity simulation.
    Features comprehensive control panels, multi-curve visualization,
    historical data analysis, and parameter scanning capabilities.

Features:
    1. Real-time multi-parameter control interface with sliders
    2. Multi-curve dynamic display for cavity voltage, reflection, detuning, mechanical modes
    3. Historical data analysis with recording, playback, and export functions
    4. Parameter scanning analysis with automatic range scanning and response charts

Dependencies:
    - numpy: Numerical computing
    - matplotlib: Plotting and visualization
    - tkinter: GUI framework
    - llrflibs: RF cavity simulation library

Usage:
    python advanced_cavity_gui.py

License:
    MIT License - see LICENSE file for details

Changelog:
    v1.0.0 (2025-09-01): Initial release with full GUI functionality
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import csv
import json
from datetime import datetime
from llrflibs.rf_sim import cav_ss_mech, sim_scav_step
from llrflibs.rf_control import ss_discrete

class CavitySimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Cavity Simulation Control Panel")
        self.root.geometry("1400x900")
        
        # Simulation parameters
        self.init_simulation_params()
        
        # Data storage
        self.max_history = 10000
        self.history_data = {
            'time': [],
            'vc_real': [], 'vc_imag': [], 'vc_mag': [], 'vc_phase': [],
            'vr_real': [], 'vr_imag': [], 'vr_mag': [], 'vr_phase': [],
            'detuning': [],
            'mech_modes': [[] for _ in range(len(self.mech_modes['f']))],
            'control_params': {'amp': [], 'phase': [], 'fsrc': [], 'pulsed': []}
        }
        
        # Control variables
        self.simulation_running = False
        self.recording = False
        self.playback_mode = False
        self.playback_index = 0
        
        # GUI setup
        self.setup_gui()
        
        # Start simulation thread
        self.sim_thread = None
        self.start_simulation()
    
    def init_simulation_params(self):
        """Initialize simulation parameters"""
        # Simulation parameters
        self.Ts = 1e-6
        self.t_fill = 510
        self.t_flat = 1300
        self.buf_size = 2048 * 8
        self.pul_len = 2048 * 10
        
        # Cavity parameters
        self.mech_modes = {'f': [280, 341, 460, 487, 618],
                          'Q': [40, 20, 50, 80, 100],
                          'K': [2, 0.8, 2, 0.6, 0.2]}
        self.f0 = 1.3e9
        self.beta = 1e4
        self.roQ = 1036
        self.QL = 3e6
        self.RL = 0.5 * self.roQ * self.QL
        self.wh = np.pi * self.f0 / self.QL
        self.ib = 0.008
        
        # State space initialization
        status, Am, Bm, Cm, Dm = cav_ss_mech(self.mech_modes)
        status, self.Ad, self.Bd, self.Cd, self.Dd, _ = ss_discrete(
            Am, Bm, Cm, Dm, Ts=self.Ts, method='zoh', plot=False, plot_pno=10000)
        
        # Initial states
        self.state_m = np.matrix(np.zeros(self.Bd.shape))
        self.state_vc = 0.0
        self.pha_src = 0.0
        self.buf_id = 0
        self.dw = 0
        
        # Beam and baseband setup
        self.beam_pul = np.zeros(self.buf_size, dtype=complex)
        self.beam_cw = 0
        self.beam_pul[self.t_fill:self.t_flat] = self.ib
        
        self.base_pul = np.zeros(self.buf_size, dtype=complex)
        self.base_cw = 1
        self.base_pul[:self.t_flat] = 1.0
        
        # Control parameters (will be controlled by GUI)
        self.control_params = {
            'amp': 1.0,
            'phase': 0.0,
            'fsrc': -460,
            'pulsed': False,
            'ib': 0.008,
            'gain_dB': 20 * np.log10(12e6)
        }
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Create main frames
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Setup control panel
        self.setup_control_panel()
        
        # Setup plot area
        self.setup_plot_area()
    
    def setup_control_panel(self):
        """Setup the control panel with sliders and buttons"""
        # Control Parameters Section
        params_frame = ttk.LabelFrame(self.control_frame, text="Control Parameters")
        params_frame.pack(fill=tk.X, pady=5)
        
        # Amplitude control
        ttk.Label(params_frame, text="Amplitude:").pack()
        self.amp_var = tk.DoubleVar(value=self.control_params['amp'])
        self.amp_scale = ttk.Scale(params_frame, from_=0.0, to=2.0, variable=self.amp_var, 
                                  orient=tk.HORIZONTAL, length=200, command=self.update_params)
        self.amp_scale.pack()
        self.amp_label = ttk.Label(params_frame, text=f"Value: {self.amp_var.get():.3f}")
        self.amp_label.pack()
        
        # Phase control
        ttk.Label(params_frame, text="Phase (deg):").pack()
        self.phase_var = tk.DoubleVar(value=self.control_params['phase'])
        self.phase_scale = ttk.Scale(params_frame, from_=-180, to=180, variable=self.phase_var,
                                    orient=tk.HORIZONTAL, length=200, command=self.update_params)
        self.phase_scale.pack()
        self.phase_label = ttk.Label(params_frame, text=f"Value: {self.phase_var.get():.1f}")
        self.phase_label.pack()
        
        # Frequency offset control
        ttk.Label(params_frame, text="Freq Offset (Hz):").pack()
        self.fsrc_var = tk.DoubleVar(value=self.control_params['fsrc'])
        self.fsrc_scale = ttk.Scale(params_frame, from_=-2000, to=2000, variable=self.fsrc_var,
                                   orient=tk.HORIZONTAL, length=200, command=self.update_params)
        self.fsrc_scale.pack()
        self.fsrc_label = ttk.Label(params_frame, text=f"Value: {self.fsrc_var.get():.0f}")
        self.fsrc_label.pack()
        
        # Beam current control
        ttk.Label(params_frame, text="Beam Current (A):").pack()
        self.ib_var = tk.DoubleVar(value=self.control_params['ib'])
        self.ib_scale = ttk.Scale(params_frame, from_=0.0, to=0.02, variable=self.ib_var,
                                 orient=tk.HORIZONTAL, length=200, command=self.update_params)
        self.ib_scale.pack()
        self.ib_label = ttk.Label(params_frame, text=f"Value: {self.ib_var.get():.4f}")
        self.ib_label.pack()
        
        # Pulsed mode control
        self.pulsed_var = tk.BooleanVar(value=self.control_params['pulsed'])
        self.pulsed_check = ttk.Checkbutton(params_frame, text="Pulsed Mode", 
                                           variable=self.pulsed_var, command=self.update_params)
        self.pulsed_check.pack()
        
        # Simulation Control Section
        sim_frame = ttk.LabelFrame(self.control_frame, text="Simulation Control")
        sim_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = ttk.Button(sim_frame, text="Start", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = ttk.Button(sim_frame, text="Stop", command=self.stop_simulation)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        self.reset_btn = ttk.Button(sim_frame, text="Reset", command=self.reset_simulation)
        self.reset_btn.pack(side=tk.LEFT, padx=2)
        
        # Data Recording Section
        record_frame = ttk.LabelFrame(self.control_frame, text="Data Recording")
        record_frame.pack(fill=tk.X, pady=5)
        
        self.record_btn = ttk.Button(record_frame, text="Start Recording", command=self.toggle_recording)
        self.record_btn.pack(side=tk.LEFT, padx=2)
        
        self.save_btn = ttk.Button(record_frame, text="Save Data", command=self.save_data)
        self.save_btn.pack(side=tk.LEFT, padx=2)
        
        self.load_btn = ttk.Button(record_frame, text="Load Data", command=self.load_data)
        self.load_btn.pack(side=tk.LEFT, padx=2)
        
        # Playback Control Section
        playback_frame = ttk.LabelFrame(self.control_frame, text="Playback Control")
        playback_frame.pack(fill=tk.X, pady=5)
        
        self.playback_btn = ttk.Button(playback_frame, text="Start Playback", command=self.toggle_playback)
        self.playback_btn.pack(side=tk.LEFT, padx=2)
        
        self.playback_var = tk.DoubleVar(value=0)
        self.playback_scale = ttk.Scale(playback_frame, from_=0, to=100, variable=self.playback_var,
                                       orient=tk.HORIZONTAL, length=200, command=self.set_playback_position)
        self.playback_scale.pack()
        
        # Parameter Scanning Section
        scan_frame = ttk.LabelFrame(self.control_frame, text="Parameter Scanning")
        scan_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(scan_frame, text="Scan Parameter:").pack()
        self.scan_param_var = tk.StringVar(value="amp")
        scan_combo = ttk.Combobox(scan_frame, textvariable=self.scan_param_var, 
                                 values=["amp", "phase", "fsrc", "ib"])
        scan_combo.pack()
        
        ttk.Label(scan_frame, text="Range:").pack()
        range_frame = ttk.Frame(scan_frame)
        range_frame.pack()
        
        ttk.Label(range_frame, text="Min:").pack(side=tk.LEFT)
        self.scan_min_var = tk.DoubleVar(value=0.5)
        self.scan_min_entry = ttk.Entry(range_frame, textvariable=self.scan_min_var, width=8)
        self.scan_min_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(range_frame, text="Max:").pack(side=tk.LEFT)
        self.scan_max_var = tk.DoubleVar(value=1.5)
        self.scan_max_entry = ttk.Entry(range_frame, textvariable=self.scan_max_var, width=8)
        self.scan_max_entry.pack(side=tk.LEFT, padx=2)
        
        self.scan_btn = ttk.Button(scan_frame, text="Start Scan", command=self.start_parameter_scan)
        self.scan_btn.pack(pady=5)
        
        # Status Section
        status_frame = ttk.LabelFrame(self.control_frame, text="Status")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack()
        
        self.sim_time_label = ttk.Label(status_frame, text="Sim Time: 0.000 s")
        self.sim_time_label.pack()
        
        self.data_points_label = ttk.Label(status_frame, text="Data Points: 0")
        self.data_points_label.pack()
    
    def setup_plot_area(self):
        """Setup the plot area with multiple subplots"""
        self.fig = Figure(figsize=(12, 8), dpi=100)
        
        # Create subplots
        self.ax1 = self.fig.add_subplot(2, 3, 1)  # Cavity voltage magnitude
        self.ax2 = self.fig.add_subplot(2, 3, 2)  # Cavity voltage phase
        self.ax3 = self.fig.add_subplot(2, 3, 3)  # Reflected voltage
        self.ax4 = self.fig.add_subplot(2, 3, 4)  # Detuning
        self.ax5 = self.fig.add_subplot(2, 3, 5)  # Mechanical modes
        self.ax6 = self.fig.add_subplot(2, 3, 6)  # Parameter scan results
        
        # Setup plot properties
        self.ax1.set_title('Cavity Voltage Magnitude')
        self.ax1.set_ylabel('Magnitude (MV)')
        self.ax1.grid(True)
        
        self.ax2.set_title('Cavity Voltage Phase')
        self.ax2.set_ylabel('Phase (deg)')
        self.ax2.grid(True)
        
        self.ax3.set_title('Reflected Voltage')
        self.ax3.set_ylabel('Magnitude (MV)')
        self.ax3.grid(True)
        
        self.ax4.set_title('Detuning')
        self.ax4.set_ylabel('Frequency (Hz)')
        self.ax4.grid(True)
        
        self.ax5.set_title('Mechanical Modes')
        self.ax5.set_ylabel('Amplitude')
        self.ax5.grid(True)
        
        self.ax6.set_title('Parameter Scan Results')
        self.ax6.set_ylabel('Response')
        self.ax6.grid(True)
        
        # Initialize plot lines
        self.init_plot_lines()
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        toolbar = tk.Frame(self.plot_frame)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.fig.tight_layout()
    
    def init_plot_lines(self):
        """Initialize plot lines"""
        self.line1, = self.ax1.plot([], [], 'b-', linewidth=1)
        self.line2, = self.ax2.plot([], [], 'r-', linewidth=1)
        self.line3, = self.ax3.plot([], [], 'g-', linewidth=1)
        self.line4, = self.ax4.plot([], [], 'm-', linewidth=1)
        
        # Mechanical mode lines
        self.mech_lines = []
        colors = ['c', 'y', 'k', 'orange', 'purple']
        for i in range(len(self.mech_modes['f'])):
            line, = self.ax5.plot([], [], colors[i % len(colors)], 
                                 linewidth=1, label=f'Mode {i+1} ({self.mech_modes["f"][i]} Hz)')
            self.mech_lines.append(line)
        self.ax5.legend()
        
        self.scan_line, = self.ax6.plot([], [], 'ro-', linewidth=1)
    
    def sim_helper_functions(self):
        """Simulation helper functions"""
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
        
        return sim_rfsrc, sim_iqmod, sim_amp, sim_cav
    
    def simulation_step(self):
        """Execute one simulation step"""
        sim_rfsrc, sim_iqmod, sim_amp, sim_cav = self.sim_helper_functions()
        
        # Get current parameters
        params = self.control_params.copy()
        
        # Update beam profile if needed
        self.beam_pul[self.t_fill:self.t_flat] = params['ib']
        
        # RF signal source
        S0, self.pha_src = sim_rfsrc(params['fsrc'], params['amp'], self.pha_src, self.Ts)
        
        # emulate the pulse
        if params['pulsed']:
            self.buf_id += 1
            if self.buf_id >= self.pul_len:
                self.buf_id = 0
        
        # I/Q modulator
        S1 = sim_iqmod(S0, 
                       pulsed=params['pulsed'],
                       base_pul=self.base_pul,
                       base_cw=self.base_cw,
                       buf_id=self.buf_id)
        
        # Amplifier
        S2 = sim_amp(S1, params['gain_dB'])
        
        # Microphonics
        dw_micr = 2.0 * np.pi * np.random.randn() * 10
        
        # Cavity dynamics
        vc, vr, self.dw, self.state_vc, self.state_m = sim_cav(
            self.wh, self.RL, self.dw, 0 + dw_micr, S2, self.state_vc, self.Ts, 
            beta=self.beta,
            state_m0=self.state_m, 
            Am=self.Ad, 
            Bm=self.Bd, 
            Cm=self.Cd,
            Dm=self.Dd,
            pulsed=params['pulsed'], 
            beam_pul=self.beam_pul, 
            beam_cw=self.beam_cw, 
            buf_id=self.buf_id)
        
        return vc, vr, self.dw
    
    def simulation_loop(self):
        """Main simulation loop"""
        start_time = time.time()
        step_count = 0
        
        while self.simulation_running:
            if not self.playback_mode:
                # Run simulation step
                vc, vr, dw = self.simulation_step()
                current_time = time.time() - start_time
                
                # Store data
                self.store_data(current_time, vc, vr, dw)
                
                step_count += 1
                
                # Update GUI every 100 steps
                if step_count % 100 == 0:
                    self.root.after(0, self.update_plots)
                    self.root.after(0, self.update_status, current_time, len(self.history_data['time']))
            else:
                # Playback mode
                time.sleep(0.01)
                self.root.after(0, self.update_plots)
            
            time.sleep(self.Ts * 100)  # Adjust timing for GUI responsiveness
    
    def store_data(self, current_time, vc, vr, dw):
        """Store simulation data"""
        # Limit history size
        if len(self.history_data['time']) >= self.max_history:
            for key in self.history_data:
                if key != 'mech_modes' and key != 'control_params':
                    self.history_data[key].pop(0)
                elif key == 'mech_modes':
                    for mode_data in self.history_data[key]:
                        if mode_data:
                            mode_data.pop(0)
                elif key == 'control_params':
                    for param_data in self.history_data[key].values():
                        if param_data:
                            param_data.pop(0)
        
        # Store new data
        self.history_data['time'].append(current_time)
        self.history_data['vc_real'].append(np.real(vc))
        self.history_data['vc_imag'].append(np.imag(vc))
        self.history_data['vc_mag'].append(np.abs(vc))
        self.history_data['vc_phase'].append(np.angle(vc) * 180 / np.pi)
        self.history_data['vr_real'].append(np.real(vr))
        self.history_data['vr_imag'].append(np.imag(vr))
        self.history_data['vr_mag'].append(np.abs(vr))
        self.history_data['vr_phase'].append(np.angle(vr) * 180 / np.pi)
        self.history_data['detuning'].append(dw / (2 * np.pi))
        
        # Store mechanical mode data
        for i in range(len(self.mech_modes['f'])):
            try:
                mode_val = np.real(self.state_m[0, i])
                self.history_data['mech_modes'][i].append(mode_val)
            except:
                self.history_data['mech_modes'][i].append(0)
        
        # Store control parameters if recording
        if self.recording:
            for param, value in self.control_params.items():
                self.history_data['control_params'][param].append(value)
    
    def update_plots(self):
        """Update all plots with current data"""
        if not self.history_data['time']:
            return
        
        try:
            time_data = np.array(self.history_data['time'])
            
            # Update cavity voltage magnitude
            if self.history_data['vc_mag']:
                vc_mag_data = np.array(self.history_data['vc_mag'], dtype=float) * 1e-6  # Convert to MV
                self.line1.set_data(time_data, vc_mag_data)
                self.ax1.relim()
                self.ax1.autoscale_view()
            
            # Update cavity voltage phase
            if self.history_data['vc_phase']:
                vc_phase_data = np.array(self.history_data['vc_phase'], dtype=float)
                self.line2.set_data(time_data, vc_phase_data)
                self.ax2.relim()
                self.ax2.autoscale_view()
            
            # Update reflected voltage
            if self.history_data['vr_mag']:
                vr_mag_data = np.array(self.history_data['vr_mag'], dtype=float) * 1e-6  # Convert to MV
                self.line3.set_data(time_data, vr_mag_data)
                self.ax3.relim()
                self.ax3.autoscale_view()
            
            # Update detuning
            if self.history_data['detuning']:
                detuning_data = np.array(self.history_data['detuning'], dtype=float)
                self.line4.set_data(time_data, detuning_data)
                self.ax4.relim()
                self.ax4.autoscale_view()
            
            # Update mechanical modes
            for i, line in enumerate(self.mech_lines):
                if (i < len(self.history_data['mech_modes']) and 
                    self.history_data['mech_modes'][i] and 
                    len(self.history_data['mech_modes'][i]) == len(time_data)):
                    mech_data = np.array(self.history_data['mech_modes'][i], dtype=float)
                    line.set_data(time_data, mech_data)
            self.ax5.relim()
            self.ax5.autoscale_view()
            
            self.canvas.draw_idle()
            
        except Exception as e:
            print(f"Plot update error: {e}")
            pass
    
    def update_params(self, *args):
        """Update control parameters from GUI"""
        self.control_params['amp'] = self.amp_var.get()
        self.control_params['phase'] = self.phase_var.get()
        self.control_params['fsrc'] = self.fsrc_var.get()
        self.control_params['ib'] = self.ib_var.get()
        self.control_params['pulsed'] = self.pulsed_var.get()
        
        # Update labels
        self.amp_label.config(text=f"Value: {self.amp_var.get():.3f}")
        self.phase_label.config(text=f"Value: {self.phase_var.get():.1f}")
        self.fsrc_label.config(text=f"Value: {self.fsrc_var.get():.0f}")
        self.ib_label.config(text=f"Value: {self.ib_var.get():.4f}")
    
    def update_status(self, sim_time, data_points):
        """Update status labels"""
        self.sim_time_label.config(text=f"Sim Time: {sim_time:.3f} s")
        self.data_points_label.config(text=f"Data Points: {data_points}")
    
    def start_simulation(self):
        """Start the simulation"""
        if not self.simulation_running:
            self.simulation_running = True
            self.status_label.config(text="Running")
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            
            if self.sim_thread is None or not self.sim_thread.is_alive():
                self.sim_thread = threading.Thread(target=self.simulation_loop, daemon=True)
                self.sim_thread.start()
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.simulation_running = False
        self.status_label.config(text="Stopped")
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
    
    def reset_simulation(self):
        """Reset the simulation"""
        self.stop_simulation()
        
        # Reset states
        self.state_m = np.matrix(np.zeros(self.Bd.shape))
        self.state_vc = 0.0
        self.pha_src = 0.0
        self.buf_id = 0
        self.dw = 0
        
        # Clear history
        for key in self.history_data:
            if key != 'mech_modes' and key != 'control_params':
                self.history_data[key].clear()
            elif key == 'mech_modes':
                for mode_data in self.history_data[key]:
                    mode_data.clear()
            elif key == 'control_params':
                for param_data in self.history_data[key].values():
                    param_data.clear()
        
        # Clear plots
        for line in [self.line1, self.line2, self.line3, self.line4] + self.mech_lines + [self.scan_line]:
            line.set_data([], [])
        
        self.canvas.draw()
        self.status_label.config(text="Reset")
    
    def toggle_recording(self):
        """Toggle data recording"""
        self.recording = not self.recording
        if self.recording:
            self.record_btn.config(text="Stop Recording")
            self.status_label.config(text="Recording")
        else:
            self.record_btn.config(text="Start Recording")
            if self.simulation_running:
                self.status_label.config(text="Running")
            else:
                self.status_label.config(text="Stopped")
    
    def save_data(self):
        """Save recorded data to file"""
        if not self.history_data['time']:
            messagebox.showwarning("Warning", "No data to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    # Save as JSON
                    save_data = {
                        'metadata': {
                            'timestamp': datetime.now().isoformat(),
                            'simulation_params': {
                                'Ts': self.Ts,
                                'f0': self.f0,
                                'QL': self.QL,
                                'mech_modes': self.mech_modes
                            }
                        },
                        'data': self.history_data
                    }
                    with open(filename, 'w') as f:
                        json.dump(save_data, f, indent=2, default=str)
                else:
                    # Save as CSV
                    with open(filename, 'w', newline='') as f:
                        writer = csv.writer(f)
                        
                        # Write header
                        header = ['time', 'vc_mag', 'vc_phase', 'vr_mag', 'detuning']
                        header.extend([f'mech_mode_{i+1}' for i in range(len(self.mech_modes['f']))])
                        writer.writerow(header)
                        
                        # Write data
                        for i in range(len(self.history_data['time'])):
                            row = [
                                self.history_data['time'][i],
                                self.history_data['vc_mag'][i],
                                self.history_data['vc_phase'][i],
                                self.history_data['vr_mag'][i],
                                self.history_data['detuning'][i]
                            ]
                            for j in range(len(self.mech_modes['f'])):
                                if i < len(self.history_data['mech_modes'][j]):
                                    row.append(self.history_data['mech_modes'][j][i])
                                else:
                                    row.append(0)
                            writer.writerow(row)
                
                messagebox.showinfo("Success", f"Data saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def load_data(self):
        """Load data from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    # Load JSON
                    with open(filename, 'r') as f:
                        loaded_data = json.load(f)
                    self.history_data = loaded_data['data']
                else:
                    # Load CSV
                    self.history_data = {
                        'time': [], 'vc_real': [], 'vc_imag': [], 'vc_mag': [], 'vc_phase': [],
                        'vr_real': [], 'vr_imag': [], 'vr_mag': [], 'vr_phase': [],
                        'detuning': [],
                        'mech_modes': [[] for _ in range(len(self.mech_modes['f']))],
                        'control_params': {'amp': [], 'phase': [], 'fsrc': [], 'pulsed': []}
                    }
                    
                    with open(filename, 'r') as f:
                        reader = csv.reader(f)
                        header = next(reader)  # Skip header
                        
                        for row in reader:
                            self.history_data['time'].append(float(row[0]))
                            self.history_data['vc_mag'].append(float(row[1]))
                            self.history_data['vc_phase'].append(float(row[2]))
                            self.history_data['vr_mag'].append(float(row[3]))
                            self.history_data['detuning'].append(float(row[4]))
                            
                            for i in range(len(self.mech_modes['f'])):
                                if i + 5 < len(row):
                                    self.history_data['mech_modes'][i].append(float(row[i + 5]))
                
                self.update_plots()
                messagebox.showinfo("Success", f"Data loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def toggle_playback(self):
        """Toggle playback mode"""
        if not self.history_data['time']:
            messagebox.showwarning("Warning", "No data to playback!")
            return
        
        self.playback_mode = not self.playback_mode
        if self.playback_mode:
            self.playback_btn.config(text="Stop Playback")
            self.playback_scale.config(to=len(self.history_data['time'])-1)
        else:
            self.playback_btn.config(text="Start Playback")
    
    def set_playback_position(self, *args):
        """Set playback position"""
        if self.playback_mode and self.history_data['time']:
            self.playback_index = int(self.playback_var.get())
            # Update plots to show data up to current position
            # This could be implemented to show progressive playback
    
    def start_parameter_scan(self):
        """Start parameter scanning"""
        param = self.scan_param_var.get()
        min_val = self.scan_min_var.get()
        max_val = self.scan_max_var.get()
        
        if min_val >= max_val:
            messagebox.showerror("Error", "Minimum value must be less than maximum value!")
            return
        
        # Run scan in separate thread
        scan_thread = threading.Thread(target=self.parameter_scan, 
                                       args=(param, min_val, max_val), daemon=True)
        scan_thread.start()
    
    def parameter_scan(self, param, min_val, max_val):
        """Execute parameter scanning"""
        num_points = 20
        param_values = np.linspace(min_val, max_val, num_points)
        responses = []
        
        # Store original parameter value
        original_value = self.control_params[param]
        
        self.root.after(0, lambda: self.status_label.config(text=f"Scanning {param}..."))
        
        for i, value in enumerate(param_values):
            # Set parameter value
            self.control_params[param] = value
            
            # Run simulation for a short time to get steady state
            temp_state_vc = 0.0
            temp_state_m = np.matrix(np.zeros(self.Bd.shape))
            
            for _ in range(100):  # Run 100 steps
                vc, vr, dw = self.simulation_step()
            
            # Record response (cavity voltage magnitude)
            responses.append(np.abs(vc) * 1e-6)  # Convert to MV
            
            # Update progress
            progress = (i + 1) / num_points * 100
            self.root.after(0, lambda p=progress: self.status_label.config(text=f"Scanning {param}... {p:.0f}%"))
        
        # Restore original parameter value
        self.control_params[param] = original_value
        
        # Update scan plot
        self.root.after(0, self.update_scan_plot, param_values, responses, param)
        self.root.after(0, lambda: self.status_label.config(text="Scan complete"))
    
    def update_scan_plot(self, param_values, responses, param_name):
        """Update parameter scan plot"""
        self.scan_line.set_data(param_values, responses)
        self.ax6.relim()
        self.ax6.autoscale_view()
        self.ax6.set_xlabel(f'{param_name}')
        self.ax6.set_ylabel('Cavity Voltage (MV)')
        self.ax6.set_title(f'Parameter Scan: {param_name}')
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = CavitySimulationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
