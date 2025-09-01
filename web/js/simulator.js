/**
 * Virtual Cavity RF Simulator - Core Simulation Engine
 * 
 * This module implements the RF cavity physics simulation
 * using JavaScript for real-time web-based operation.
 */

class CavitySimulator {
    constructor() {
        // Simulation parameters
        this.dt = 1e-6; // Time step (1 microsecond)
        this.f0 = 1.3e9; // Cavity resonant frequency (1.3 GHz)
        this.Q_loaded = 3e6; // Loaded quality factor
        this.R_over_Q = 1036; // R/Q value
        this.beta = 1.0; // Coupling coefficient
        
        // Cavity state variables
        this.vc_complex = { real: 0, imag: 0 }; // Cavity voltage (complex)
        this.detuning = 0; // Frequency detuning (Hz)
        this.beam_current = 0.01; // Beam current (A)
        
        // RF drive parameters
        this.amplitude = 1.0;
        this.phase = 0; // degrees
        this.frequency_offset = 0; // Hz
        
        // Mechanical resonances (microphonics)
        this.mechanical_modes = [
            { freq: 280, Q: 100, amplitude: 1e-8 },
            { freq: 341, Q: 150, amplitude: 0.8e-8 },
            { freq: 460, Q: 200, amplitude: 1.2e-8 },
            { freq: 487, Q: 180, amplitude: 0.6e-8 },
            { freq: 618, Q: 250, amplitude: 0.9e-8 }
        ];
        
        // Initialize mechanical oscillators
        this.mech_states = this.mechanical_modes.map(mode => ({
            x: 0,
            v: 0,
            omega: 2 * Math.PI * mode.freq,
            gamma: mode.omega / (2 * mode.Q),
            amplitude: mode.amplitude
        }));
        
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
     * Update RF drive parameters
     */
    setRFParameters(amplitude, phase, frequency_offset, beam_current) {
        this.amplitude = amplitude;
        this.phase = phase * Math.PI / 180; // Convert to radians
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
     * Single simulation step
     */
    step() {
        // Update mechanical resonances (microphonics)
        let total_mechanical_detuning = 0;
        this.mech_states.forEach((state, i) => {
            const mode = this.mechanical_modes[i];
            
            // Simple driven harmonic oscillator
            const force = mode.amplitude * Math.sin(state.omega * this.time);
            const acc = -state.omega * state.omega * state.x - 2 * state.gamma * state.v + force;
            
            state.v += acc * this.dt;
            state.x += state.v * this.dt;
            
            // Convert mechanical displacement to frequency shift
            total_mechanical_detuning += state.x * 1e6; // Scale factor
        });
        
        // Total detuning including manual offset and microphonics
        this.detuning = this.frequency_offset + total_mechanical_detuning;
        
        // Calculate cavity dynamics
        const omega_0 = 2 * Math.PI * this.f0;
        const omega_detuned = omega_0 + 2 * Math.PI * this.detuning;
        const omega_L = 2 * Math.PI * this.f0; // RF frequency
        
        // Half bandwidth
        const half_bandwidth = omega_0 / (2 * this.Q_loaded);
        
        // RF drive voltage (complex)
        let v_drive_real = 0, v_drive_imag = 0;
        
        if (this.mode === 'cw' || (this.mode === 'pulsed' && Math.sin(2 * Math.PI * this.time * 50) > 0)) {
            v_drive_real = this.amplitude * Math.cos(omega_L * this.time + this.phase);
            v_drive_imag = this.amplitude * Math.sin(omega_L * this.time + this.phase);
        }
        
        // Beam loading (simplified)
        const beam_loading_real = -this.beam_current * this.R_over_Q * 0.5;
        const beam_loading_imag = 0;
        
        // Cavity differential equation (in rotating frame)
        // dVc/dt = -j*ω_detuning*Vc - (ω0/2Q)*Vc + (ω0/2)*V_drive - (ω0/2)*I_beam*R/Q
        
        const detuning_term_real = -this.detuning * 2 * Math.PI * this.vc_complex.imag;
        const detuning_term_imag = this.detuning * 2 * Math.PI * this.vc_complex.real;
        
        const damping_real = -half_bandwidth * this.vc_complex.real;
        const damping_imag = -half_bandwidth * this.vc_complex.imag;
        
        const drive_real = half_bandwidth * v_drive_real;
        const drive_imag = half_bandwidth * v_drive_imag;
        
        const beam_real = half_bandwidth * beam_loading_real;
        const beam_imag = half_bandwidth * beam_loading_imag;
        
        // Update cavity voltage
        const dVc_real = detuning_term_real + damping_real + drive_real + beam_real;
        const dVc_imag = detuning_term_imag + damping_imag + drive_imag + beam_imag;
        
        this.vc_complex.real += dVc_real * this.dt;
        this.vc_complex.imag += dVc_imag * this.dt;
        
        // Calculate derived quantities
        const vc_magnitude = Math.sqrt(this.vc_complex.real**2 + this.vc_complex.imag**2);
        const vc_phase = Math.atan2(this.vc_complex.imag, this.vc_complex.real) * 180 / Math.PI;
        
        // Forward and reflected power calculation
        const forward_power = this.amplitude**2 * 1000; // kW (simplified)
        const reflected_power = Math.abs(this.detuning) * 0.1; // kW (simplified)
        
        // Store data point
        const data_point = {
            time: this.time,
            vc_magnitude: vc_magnitude / 1e6, // Convert to MV
            vc_phase: vc_phase,
            forward_power: forward_power,
            reflected_power: reflected_power,
            detuning: this.detuning,
            beam_current: this.beam_current,
            amplitude: this.amplitude,
            phase: this.phase * 180 / Math.PI
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
