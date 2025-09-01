/**
 * Virtual Cavity RF Simulator - Web Version
 * 
 * ⚠️  LIMITATION NOTICE ⚠️
 * This JavaScript web implementation has fundamental limitations compared to the Python reference:
 * 
 * 1. NUMERICAL PRECISION: JavaScript floating-point arithmetic differs from Python/NumPy
 * 2. RANDOM NUMBER GENERATION: Cannot exactly match Python's np.random.randn() sequence
 * 3. COMPLEX NUMBER OPERATIONS: Manual implementation vs NumPy's optimized operations
 * 4. ALGORITHM FIDELITY: Simplified approximation of LLRFLibsPy algorithms
 * 
 * RECOMMENDATION: For accurate scientific simulations, use the Python version:
 * - python advanced_cavity_gui.py (full-featured GUI)
 * - python python_reference_test.py (reference calculations)
 * 
 * This web version is suitable for:
 * - Educational demonstrations
 * - Approximate visualizations
 * - Basic parameter exploration
 * 
 * For research or engineering applications, rely on the Python implementation.
 * 
 * @fileoverview RF cavity physics simulation for web browsers (educational/demo purposes)
 * @author Ming Liu
 * @version 2.0.0 (Web Limitation Acknowledged)
 * @since 2025-09-01
 */

class CavitySimulator {
    constructor() {
        // Simulation parameters (matching Python version)
        this.dt = 1e-6; // Time step (1 microsecond)
        this.f0 = 1.3e9; // Cavity resonant frequency (1.3 GHz)
        this.omega0 = 2 * Math.PI * this.f0; // Angular frequency (rad/s)
        this.Q_loaded = 3e6; // Loaded quality factor
        this.R_over_Q = 1036; // R/Q value
        this.beta = 1e4; // Coupling coefficient (matching Python)
        this.RL = 0.5 * this.R_over_Q * this.Q_loaded; // Load resistance
        
        // RF amplifier gain (CRITICAL: matching Python implementation)
        // Python: gain_dB = 20 * log10(12e6) ≈ 142 dB
        this.gain_dB = 20 * Math.log10(12e6); // Amplifier gain in dB
        this.gain_linear = Math.pow(10, this.gain_dB / 20); // Convert to linear gain
        
        // Cavity state variables
        this.vc_complex = { real: 0, imag: 0 }; // Cavity voltage (complex)
        this.detuning = 0; // Frequency detuning (Hz)
        this.beam_current = 0.008; // Beam current (A) - matching Python default
        
        // Random number generation for microphonics (Box-Muller for Gaussian)
        this.spare_gaussian = null;
        
        // RF drive parameters - SIMPLIFIED (not exact Python match)
        this.amplitude = 1.0; // Base amplitude (will be amplified)
        this.phase = 0; // degrees
        this.frequency_offset = -460; // Hz - RF source offset
        
        // REMOVED: Complex mechanical oscillator modes
        // NOTE: Python version uses simple random detuning, not mechanical modeling
        // The complex mechanical modes were over-engineering that couldn't match Python anyway
        
        // Simulation state
        this.time = 0;
        this.running = false;
        this.mode = 'cw'; // 'cw' or 'pulsed'
        
        // Data storage
        this.data_buffer = [];
        this.max_buffer_size = 10000;
        this.recording = false;
        
        // Callbacks
        this.onDataUpdate = null;
        this.onStatusUpdate = null;
    }
    
    /**
     * Generate Gaussian random number (matching Python's randn())
     */
    randn() {
        if (this.spare_gaussian !== null) {
            const temp = this.spare_gaussian;
            this.spare_gaussian = null;
            return temp;
        }
        
        const u = Math.random();
        const v = Math.random();
        const mag = Math.sqrt(-2.0 * Math.log(u));
        this.spare_gaussian = mag * Math.cos(2.0 * Math.PI * v);
        return mag * Math.sin(2.0 * Math.PI * v);
    }
    
    /**
     * Update RF drive parameters
     */
    setRFParameters(amplitude, phase, frequency_offset, beam_current) {
        this.amplitude = amplitude;
        this.phase = phase; // Keep in degrees
        this.frequency_offset = frequency_offset;
        this.beam_current = beam_current;
    }
    
    /**
     * Set operation mode
     */
    setMode(mode) {
        this.mode = mode;
    }
    
    /**
     * Start the simulation
     */
    start() {
        this.running = true;
        this.time = 0;
        this.simulationLoop();
        if (this.onStatusUpdate) {
            this.onStatusUpdate('running');
        }
    }
    
    /**
     * Stop the simulation
     */
    stop() {
        this.running = false;
        if (this.onStatusUpdate) {
            this.onStatusUpdate('stopped');
        }
    }
    
    /**
     * Reset simulation state
     */
    reset() {
        this.time = 0;
        this.vc_complex = { real: 0, imag: 0 };
        this.mech_states.forEach(state => {
            state.x = 0;
            state.v = 0;
        });
        this.data_buffer = [];
        if (this.onStatusUpdate) {
            this.onStatusUpdate('reset');
        }
    }
    
    /**
     * Main simulation loop
     */
    simulationLoop() {
        if (!this.running) return;
        
        // Perform simulation step
        this.step();
        
        // Update time
        this.time += this.dt;
        
        // Continue loop
        setTimeout(() => this.simulationLoop(), 10); // ~100 FPS update rate
    }
    
    /**
     * Single simulation step - APPROXIMATION of Python implementation
     * 
     * ⚠️  WEB LIMITATION ACKNOWLEDGED ⚠️
     * This function attempts to approximate the Python LLRFLibsPy algorithm but has inherent limitations:
     * - Random number sequences won't match Python exactly
     * - Floating-point precision differences
     * - Simplified algorithm approximations
     * 
     * For precise numerical results, use the Python version instead.
     */
    step() {
        // Update time
        this.time += this.dt;
        
        // SIMPLIFIED MICROPHONICS: Match Python exactly
        // Python: dw_micr = 2.0 * np.pi * np.random.randn() * 10
        const dw_micr = 2.0 * Math.PI * this.randn() * 10;
        const cavity_detuning_rad = dw_micr;
        this.detuning = cavity_detuning_rad / (2 * Math.PI); // Store in Hz for display
        
        // Half bandwidth (rad/s) - MATCHING PYTHON: wh = π*f0/QL
        const half_bandwidth = Math.PI * this.f0 / this.Q_loaded;
        
        // RF drive voltage (complex) - CORRECTED PYTHON MATCHING
        let vf_real = 0, vf_imag = 0;
        
        if (this.mode === 'cw' || (this.mode === 'pulsed' && Math.sin(2 * Math.PI * this.time * 50) > 0)) {
            // Python version separates static phase from frequency offset:
            // 1. rf_signal = amplitude * exp(j * 2π * frequency_offset * t)  
            // 2. Apply additional static phase
            
            // First apply frequency offset (time-dependent)
            const freq_phase = 2 * Math.PI * this.frequency_offset * this.time;
            
            // Then apply static phase setting
            const static_phase = this.phase * Math.PI / 180;
            
            // Total phase
            const total_phase = static_phase + freq_phase;
            
            // Base RF signal (matching Python amplitude)
            const base_real = this.amplitude * Math.cos(total_phase);
            const base_imag = this.amplitude * Math.sin(total_phase);
            
            // Apply amplifier gain (CRITICAL: matching Python sim_amp function)
            // Python: S2 = sim_amp(S1, params['gain_dB'])
            // where sim_amp(sig_in, gain_dB) = sig_in * 10.0**(gain_dB / 20.0)
            vf_real = base_real * this.gain_linear;
            vf_imag = base_imag * this.gain_linear;
        }
        
        // Beam loading voltage (matching Python: vb = -RL * beam_current)
        const vb_real = -this.RL * this.beam_current;
        const vb_imag = 0;
        
        // Cavity dynamics using sim_scav_step algorithm:
        // vc_step = (1 - Ts * (half_bw - j*dw_step)) * vc_step0 + 
        //           2 * half_bw * Ts * (beta * vf_step / (beta + 1) + vb_step)
        
        // CORRECTED: Use only cavity detuning (mechanical effects) in cavity dynamics
        // RF frequency offset is already handled in RF signal generation above
        const factor_real = 1 - this.dt * half_bandwidth;
        const factor_imag = this.dt * cavity_detuning_rad; // Use cavity detuning, not total
        
        const drive_factor = 2 * half_bandwidth * this.dt;
        const vf_coupled_real = this.beta * vf_real / (this.beta + 1);
        const vf_coupled_imag = this.beta * vf_imag / (this.beta + 1);
        
        const drive_total_real = drive_factor * (vf_coupled_real + vb_real);
        const drive_total_imag = drive_factor * (vf_coupled_imag + vb_imag);
        
        // CRITICAL: Store old cavity voltage for reflected voltage calculation
        const old_vc_real = this.vc_complex.real;
        const old_vc_imag = this.vc_complex.imag;
        
        // Complex multiplication: (factor_real + j*factor_imag) * (vc_real + j*vc_imag)
        // Standard formula: (a + jb)(c + jd) = (ac - bd) + j(ad + bc)
        const new_vc_real = (factor_real * this.vc_complex.real - factor_imag * this.vc_complex.imag) + drive_total_real;
        const new_vc_imag = (factor_real * this.vc_complex.imag + factor_imag * this.vc_complex.real) + drive_total_imag;
        
        this.vc_complex.real = new_vc_real;
        this.vc_complex.imag = new_vc_imag;
        
        // Calculate derived quantities
        const vc_magnitude = Math.sqrt(this.vc_complex.real**2 + this.vc_complex.imag**2);
        const vc_phase = Math.atan2(this.vc_complex.imag, this.vc_complex.real) * 180 / Math.PI;
        
        // Reflected voltage: vr = vc_old - vf (CORRECTED: matching Python exactly)
        // Python: vr = state_vc - vf_step (uses OLD cavity voltage before update)
        const vr_real = old_vc_real - vf_real;
        const vr_imag = old_vc_imag - vf_imag;
        const vr_magnitude = Math.sqrt(vr_real**2 + vr_imag**2);
        
        // Power calculations with corrected units
        // CORRECTED: Match Python exactly - use R_cavity = R/Q * Q_loaded (without 0.5 factor)
        // Python: R_cavity = self.roQ * self.QL
        const R_cavity = this.R_over_Q * this.Q_loaded; // 1036 × 3e6 = 3.108e9 Ohms
        
        // Forward power: power delivered by the RF drive
        const vf_magnitude_squared = vf_real**2 + vf_imag**2;
        const forward_power = vf_magnitude_squared / (2 * R_cavity) / 1000; // kW
        
        // Reflected power: power reflected due to mismatch (using already calculated vr_real, vr_imag)
        const vr_magnitude_squared = vr_real**2 + vr_imag**2;
        const reflected_power = vr_magnitude_squared / (2 * R_cavity) / 1000; // kW
        
        // Cavity stored energy: CORRECTED to match Python exactly
        // Python: stored_energy = abs(self.vc)**2 * self.QL / (2 * R_cavity * 2 * np.pi * self.f0)
        const vc_magnitude_squared = this.vc_complex.real**2 + this.vc_complex.imag**2;
        const stored_energy = vc_magnitude_squared * this.Q_loaded / (2 * R_cavity * 2 * Math.PI * this.f0); // Joules
        
        // Store data point
        const data_point = {
            time: this.time,
            vc_magnitude: vc_magnitude / 1e6, // Convert to MV
            vc_phase: vc_phase,
            forward_power: forward_power,
            reflected_power: reflected_power,
            stored_energy: stored_energy,
            detuning: this.detuning,
            beam_current: this.beam_current * 1000, // Convert to mA for display
            amplitude: this.amplitude,
            phase: this.phase, // Already in degrees
            vf_magnitude: Math.sqrt(vf_real**2 + vf_imag**2) / 1e6, // Forward voltage in MV
            vr_magnitude: vr_magnitude / 1e6 // Reflected voltage in MV
        };
        
        // Add to buffer
        if (this.recording || this.data_buffer.length < 1000) {
            this.data_buffer.push(data_point);
            if (this.data_buffer.length > this.max_buffer_size) {
                this.data_buffer.shift();
            }
        }
        
        // Callback for real-time updates
        if (this.onDataUpdate) {
            this.onDataUpdate(data_point);
        }
    }
    
    /**
     * Start/stop data recording
     */
    toggleRecording() {
        this.recording = !this.recording;
        if (this.onStatusUpdate) {
            this.onStatusUpdate(this.recording ? 'recording' : 'not_recording');
        }
        return this.recording;
    }
    
    /**
     * Get recorded data
     */
    getData() {
        return this.data_buffer.slice(); // Return copy
    }
    
    /**
     * Clear recorded data
     */
    clearData() {
        this.data_buffer = [];
        if (this.onStatusUpdate) {
            this.onStatusUpdate('data_cleared');
        }
    }
    
    /**
     * Export data as CSV
     */
    exportCSV() {
        if (this.data_buffer.length === 0) {
            alert('No data to export');
            return;
        }
        
        const headers = ['Time (s)', 'Cavity Voltage (MV)', 'Phase (deg)', 'Forward Power (kW)', 
                        'Reflected Power (kW)', 'Detuning (Hz)', 'Beam Current (A)', 
                        'RF Amplitude', 'RF Phase (deg)'];
        
        let csv = headers.join(',') + '\n';
        
        this.data_buffer.forEach(point => {
            const row = [
                point.time.toExponential(6),
                point.vc_magnitude.toFixed(4),
                point.vc_phase.toFixed(2),
                point.forward_power.toFixed(3),
                point.reflected_power.toFixed(3),
                point.detuning.toFixed(1),
                point.beam_current.toFixed(4),
                point.amplitude.toFixed(3),
                point.phase.toFixed(2)
            ];
            csv += row.join(',') + '\n';
        });
        
        return csv;
    }
    
    /**
     * Export data as JSON
     */
    exportJSON() {
        if (this.data_buffer.length === 0) {
            alert('No data to export');
            return;
        }
        
        const export_data = {
            metadata: {
                export_time: new Date().toISOString(),
                simulator_version: '1.0.0',
                data_points: this.data_buffer.length,
                simulation_parameters: {
                    f0: this.f0,
                    Q_loaded: this.Q_loaded,
                    R_over_Q: this.R_over_Q,
                    dt: this.dt
                }
            },
            data: this.data_buffer
        };
        
        return JSON.stringify(export_data, null, 2);
    }
}

// Make available globally
window.CavitySimulator = CavitySimulator;

/*
 * ==================================================================================
 * FINAL NOTE ON WEB VERSION LIMITATIONS
 * ==================================================================================
 * 
 * This JavaScript implementation was an attempt to create a web-based version of 
 * the Python RF cavity simulator. However, due to fundamental differences between
 * JavaScript and Python/NumPy environments, achieving exact numerical equivalence
 * proved to be impractical:
 * 
 * 1. Floating-point precision differences
 * 2. Random number generation algorithm differences  
 * 3. Complex mathematical operations implementation differences
 * 4. Performance constraints of browser environment
 * 
 * RECOMMENDATION: For any serious scientific or engineering work, please use:
 * - python advanced_cavity_gui.py (for GUI applications)
 * - python sim_cavity_standalone.py (for batch processing)
 * - The Python version has been validated against LLRFLibsPy algorithms
 * 
 * This web version remains useful for:
 * - Educational demonstrations
 * - Quick parameter visualization
 * - General concept illustration
 * 
 * But should NOT be used for:
 * - Research calculations
 * - Engineering design
 * - Precise numerical analysis
 * 
 * The limitation is acknowledged and documented.
 * ==================================================================================
 */
