/**
 * Virtual Cavity RF Simulator - Main Application
 * 
 * Main application logic that connects the simulator engine,
 * chart manager, and user interface elements.
 */

class VirtualCavityApp {
    constructor() {
        try {
            console.log('Creating simulator...');
            this.simulator = new CavitySimulator();
            console.log('Creating chart manager...');
            this.chartManager = new ChartManager();
            
            // UI elements
            this.elements = {};
            this.lastUpdateTime = 0;
            this.updateThrottle = 50; // ms
            
            console.log('Initializing UI...');
            this.initializeUI();
            console.log('Setting up event listeners...');
            this.setupEventListeners();
            console.log('Setting up simulator callbacks...');
            this.setupSimulatorCallbacks();
            
            console.log('Virtual Cavity RF Simulator initialized successfully');
        } catch (error) {
            console.error('Error in VirtualCavityApp constructor:', error);
            throw error;
        }
    }
    
    /**
     * Initialize UI elements
     */
    initializeUI() {
        // Control buttons
        this.elements.startBtn = document.getElementById('startBtn');
        this.elements.stopBtn = document.getElementById('stopBtn');
        this.elements.resetBtn = document.getElementById('resetBtn');
        
        // Parameter sliders
        this.elements.amplitudeSlider = document.getElementById('amplitudeSlider');
        this.elements.phaseSlider = document.getElementById('phaseSlider');
        this.elements.frequencySlider = document.getElementById('frequencySlider');
        this.elements.beamCurrentSlider = document.getElementById('beamCurrentSlider');
        
        // Parameter value displays
        this.elements.amplitudeValue = document.getElementById('amplitudeValue');
        this.elements.phaseValue = document.getElementById('phaseValue');
        this.elements.frequencyValue = document.getElementById('frequencyValue');
        this.elements.beamCurrentValue = document.getElementById('beamCurrentValue');
        
        // Mode selection
        this.elements.cwMode = document.getElementById('cwMode');
        this.elements.pulsedMode = document.getElementById('pulsedMode');
        
        // Data controls
        this.elements.recordBtn = document.getElementById('recordBtn');
        this.elements.exportBtn = document.getElementById('exportBtn');
        this.elements.clearDataBtn = document.getElementById('clearDataBtn');
        
        // Status and displays
        this.elements.statusAlert = document.getElementById('statusAlert');
        this.elements.cavityVoltageDisplay = document.getElementById('cavityVoltageDisplay');
        this.elements.forwardPowerDisplay = document.getElementById('forwardPowerDisplay');
        this.elements.reflectedPowerDisplay = document.getElementById('reflectedPowerDisplay');
        this.elements.detuningDisplay = document.getElementById('detuningDisplay');
        
        // Other controls
        this.elements.autoscaleSwitch = document.getElementById('autoscaleSwitch');
        this.elements.helpBtn = document.getElementById('helpBtn');
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Control buttons
        this.elements.startBtn.addEventListener('click', () => this.startSimulation());
        this.elements.stopBtn.addEventListener('click', () => this.stopSimulation());
        this.elements.resetBtn.addEventListener('click', () => this.resetSimulation());
        
        // Parameter sliders
        this.elements.amplitudeSlider.addEventListener('input', (e) => {
            this.elements.amplitudeValue.textContent = parseFloat(e.target.value).toFixed(2);
            this.updateSimulatorParameters();
        });
        
        this.elements.phaseSlider.addEventListener('input', (e) => {
            this.elements.phaseValue.textContent = e.target.value;
            this.updateSimulatorParameters();
        });
        
        this.elements.frequencySlider.addEventListener('input', (e) => {
            this.elements.frequencyValue.textContent = e.target.value;
            this.updateSimulatorParameters();
        });
        
        this.elements.beamCurrentSlider.addEventListener('input', (e) => {
            this.elements.beamCurrentValue.textContent = parseFloat(e.target.value).toFixed(3);
            this.updateSimulatorParameters();
        });
        
        // Mode selection
        this.elements.cwMode.addEventListener('change', () => {
            if (this.elements.cwMode.checked) {
                this.simulator.setMode('cw');
            }
        });
        
        this.elements.pulsedMode.addEventListener('change', () => {
            if (this.elements.pulsedMode.checked) {
                this.simulator.setMode('pulsed');
            }
        });
        
        // Data controls
        this.elements.recordBtn.addEventListener('click', () => this.toggleRecording());
        this.elements.exportBtn.addEventListener('click', () => this.showExportModal());
        this.elements.clearDataBtn.addEventListener('click', () => this.clearData());
        
        // Autoscale
        this.elements.autoscaleSwitch.addEventListener('change', (e) => {
            this.chartManager.setAutoscale(e.target.checked);
        });
        
        // Help button
        this.elements.helpBtn.addEventListener('click', () => {
            const helpModal = new bootstrap.Modal(document.getElementById('helpModal'));
            helpModal.show();
        });
        
        // Window resize
        window.addEventListener('resize', () => {
            this.chartManager.resizeCharts();
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey) {
                switch(e.key) {
                    case ' ':
                        e.preventDefault();
                        if (this.simulator.running) {
                            this.stopSimulation();
                        } else {
                            this.startSimulation();
                        }
                        break;
                    case 'r':
                        e.preventDefault();
                        this.resetSimulation();
                        break;
                    case 's':
                        e.preventDefault();
                        this.toggleRecording();
                        break;
                }
            }
        });
    }
    
    /**
     * Setup simulator callbacks
     */
    setupSimulatorCallbacks() {
        this.simulator.onDataUpdate = (dataPoint) => {
            // Throttle updates for performance
            const now = Date.now();
            if (now - this.lastUpdateTime > this.updateThrottle) {
                this.updateCharts(dataPoint);
                this.updateDisplays(dataPoint);
                this.lastUpdateTime = now;
            }
        };
        
        this.simulator.onStatusUpdate = (status) => {
            this.updateStatus(status);
        };
    }
    
    /**
     * Start simulation
     */
    startSimulation() {
        this.updateSimulatorParameters();
        this.simulator.start();
        
        this.elements.startBtn.disabled = true;
        this.elements.stopBtn.disabled = false;
        
        this.updateStatus('Simulation running...');
    }
    
    /**
     * Stop simulation
     */
    stopSimulation() {
        this.simulator.stop();
        
        this.elements.startBtn.disabled = false;
        this.elements.stopBtn.disabled = true;
        
        this.updateStatus('Simulation stopped');
    }
    
    /**
     * Reset simulation
     */
    resetSimulation() {
        this.simulator.reset();
        this.chartManager.clearCharts();
        
        this.elements.startBtn.disabled = false;
        this.elements.stopBtn.disabled = true;
        
        this.updateStatus('Simulation reset');
        this.clearDisplays();
    }
    
    /**
     * Update simulator parameters from UI
     */
    updateSimulatorParameters() {
        const amplitude = parseFloat(this.elements.amplitudeSlider.value);
        const phase = parseFloat(this.elements.phaseSlider.value);
        const frequency = parseFloat(this.elements.frequencySlider.value);
        const beamCurrent = parseFloat(this.elements.beamCurrentSlider.value);
        
        this.simulator.setRFParameters(amplitude, phase, frequency, beamCurrent);
    }
    
    /**
     * Update charts with new data
     */
    updateCharts(dataPoint) {
        this.chartManager.updateCharts(dataPoint);
    }
    
    /**
     * Update parameter displays
     */
    updateDisplays(dataPoint) {
        this.elements.cavityVoltageDisplay.textContent = `${dataPoint.vc_magnitude.toFixed(3)} MV`;
        this.elements.forwardPowerDisplay.textContent = `${dataPoint.forward_power.toFixed(1)} kW`;
        this.elements.reflectedPowerDisplay.textContent = `${dataPoint.reflected_power.toFixed(1)} kW`;
        this.elements.detuningDisplay.textContent = `${dataPoint.detuning.toFixed(1)} Hz`;
        
        // Add visual feedback for data updates
        [this.elements.cavityVoltageDisplay, this.elements.forwardPowerDisplay, 
         this.elements.reflectedPowerDisplay, this.elements.detuningDisplay].forEach(element => {
            element.parentElement.classList.add('data-update');
            setTimeout(() => element.parentElement.classList.remove('data-update'), 300);
        });
    }
    
    /**
     * Clear parameter displays
     */
    clearDisplays() {
        this.elements.cavityVoltageDisplay.textContent = '0.0 MV';
        this.elements.forwardPowerDisplay.textContent = '0.0 kW';
        this.elements.reflectedPowerDisplay.textContent = '0.0 kW';
        this.elements.detuningDisplay.textContent = '0.0 Hz';
    }
    
    /**
     * Update status message
     */
    updateStatus(status) {
        let message = '';
        let alertClass = 'alert-info';
        
        switch(status) {
            case 'running':
                message = '<i class="fas fa-play-circle text-success"></i> Simulation running';
                alertClass = 'alert-success';
                break;
            case 'stopped':
                message = '<i class="fas fa-stop-circle text-danger"></i> Simulation stopped';
                alertClass = 'alert-warning';
                break;
            case 'reset':
                message = '<i class="fas fa-redo text-info"></i> Simulation reset';
                alertClass = 'alert-info';
                break;
            case 'recording':
                message = '<i class="fas fa-record-vinyl text-danger"></i> Recording data...';
                alertClass = 'alert-danger';
                break;
            case 'not_recording':
                message = '<i class="fas fa-stop text-secondary"></i> Recording stopped';
                alertClass = 'alert-secondary';
                break;
            case 'data_cleared':
                message = '<i class="fas fa-trash text-info"></i> Data cleared';
                alertClass = 'alert-info';
                break;
            default:
                message = `<i class="fas fa-info-circle"></i> ${status}`;
        }
        
        this.elements.statusAlert.className = `alert ${alertClass} small`;
        this.elements.statusAlert.innerHTML = message;
    }
    
    /**
     * Toggle data recording
     */
    toggleRecording() {
        const isRecording = this.simulator.toggleRecording();
        
        if (isRecording) {
            this.elements.recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
            this.elements.recordBtn.className = 'btn btn-danger btn-sm';
        } else {
            this.elements.recordBtn.innerHTML = '<i class="fas fa-record-vinyl"></i> Start Recording';
            this.elements.recordBtn.className = 'btn btn-outline-primary btn-sm';
        }
    }
    
    /**
     * Clear all data
     */
    clearData() {
        if (confirm('Are you sure you want to clear all recorded data?')) {
            this.simulator.clearData();
            this.chartManager.clearCharts();
            this.updateStatus('All data cleared');
        }
    }
    
    /**
     * Show export modal
     */
    showExportModal() {
        const data = this.simulator.getData();
        if (data.length === 0) {
            alert('No data to export. Start simulation and recording first.');
            return;
        }
        
        // Create modal content
        const modalHTML = `
            <div class="modal fade" id="exportModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Export Data</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>Export ${data.length} data points in your preferred format:</p>
                            <div class="d-grid gap-2">
                                <button class="btn btn-primary" onclick="app.exportData('csv')">
                                    <i class="fas fa-file-csv"></i> Export as CSV
                                </button>
                                <button class="btn btn-outline-primary" onclick="app.exportData('json')">
                                    <i class="fas fa-file-code"></i> Export as JSON
                                </button>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if present
        const existingModal = document.getElementById('exportModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add modal to DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Show modal
        const exportModal = new bootstrap.Modal(document.getElementById('exportModal'));
        exportModal.show();
    }
    
    /**
     * Export data in specified format
     */
    exportData(format) {
        let data, filename, mimeType;
        
        if (format === 'csv') {
            data = this.simulator.exportCSV();
            filename = `cavity_simulation_${new Date().toISOString().split('T')[0]}.csv`;
            mimeType = 'text/csv';
        } else if (format === 'json') {
            data = this.simulator.exportJSON();
            filename = `cavity_simulation_${new Date().toISOString().split('T')[0]}.json`;
            mimeType = 'application/json';
        }
        
        if (data) {
            this.downloadFile(data, filename, mimeType);
            
            // Close modal
            const exportModal = bootstrap.Modal.getInstance(document.getElementById('exportModal'));
            exportModal.hide();
            
            this.updateStatus(`Data exported as ${format.toUpperCase()}`);
        }
    }
    
    /**
     * Download file helper
     */
    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        URL.revokeObjectURL(url);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    try {
        console.log('Initializing Virtual Cavity App...');
        window.app = new VirtualCavityApp();
        console.log('App initialized successfully');
        
        // Show welcome message
        setTimeout(() => {
            window.app.updateStatus('Ready to start simulation');
        }, 1000);
    } catch (error) {
        console.error('Failed to initialize app:', error);
        
        // Show error message to user
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger position-fixed top-0 start-50 translate-middle-x mt-3';
        errorDiv.style.zIndex = '9999';
        errorDiv.innerHTML = `
            <h6>Initialization Error</h6>
            <p>Failed to load the simulator. Please check the browser console for details.</p>
            <small>Error: ${error.message}</small>
        `;
        document.body.appendChild(errorDiv);
    }
});

// Handle page visibility change to pause/resume simulation
document.addEventListener('visibilitychange', () => {
    if (window.app && window.app.simulator.running) {
        if (document.hidden) {
            // Page is hidden, could pause simulation for performance
            console.log('Page hidden - simulation continues');
        } else {
            // Page is visible again
            console.log('Page visible - simulation active');
        }
    }
});
