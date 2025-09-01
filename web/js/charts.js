/**
 * Virtual Cavity RF Simulator - Chart Management System
 * 
 * @fileoverview Comprehensive chart management for RF cavity simulation visualization
 * @author Ming Liu
 * @version 2.0.0
 * @since 2025-09-01
 * 
 * @description This module handles all chart creation, updates, and data visualization
 * using Chart.js for real-time plotting with separate charts for each parameter.
 * Features include:
 * - Independent charts for voltage, power, detuning, and beam parameters
 * - Real-time data updates with configurable buffer sizes
 * - Dual-axis support for related but different-scale parameters
 * - Automatic chart scaling and legend management
 * 
 * @requires Chart.js v3.x or higher
 * @requires chartjs-adapter-date-fns for time scale support
 */

class ChartManager {
    constructor() {
        this.charts = {};
        this.dataBufferSize = 300; // Number of points to display
        this.updateInterval = 100; // ms
        
        // Color scheme
        this.colors = {
            primary: '#667eea',
            secondary: '#764ba2',
            success: '#28a745',
            warning: '#ffc107',
            danger: '#dc3545',
            info: '#17a2b8'
        };
        
        this.initializeCharts();
    }
    
    /**
     * Initialize all charts
     */
    initializeCharts() {
        // Check if DOM elements exist before creating charts
        const voltageChartElement = document.getElementById('voltageChart');
        const powerChartElement = document.getElementById('powerChart');
        const detuningChartElement = document.getElementById('detuningChart');
        const beamChartElement = document.getElementById('beamChart');
        
        // Create charts only if corresponding DOM elements exist
        if (voltageChartElement) {
            this.createVoltageChart();
        } else {
            console.warn('voltageChart element not found - voltage chart will not be available');
        }
        
        if (powerChartElement) {
            this.createPowerChart();
        } else {
            console.warn('powerChart element not found - power chart will not be available');
        }
        
        if (detuningChartElement) {
            this.createDetuningChart();
        } else {
            console.warn('detuningChart element not found - detuning chart will not be available');
        }
        
        if (beamChartElement) {
            this.createBeamChart();
        } else {
            console.warn('beamChart element not found - beam chart will not be available');
        }
        
        console.log('Charts initialized:', Object.keys(this.charts));
    }
    
    /**
     * Create voltage chart (magnitude and phase)
     */
    createVoltageChart() {
        const ctx = document.getElementById('voltageChart');
        if (!ctx) {
            console.error('voltageChart element not found');
            return;
        }
        
        this.charts.voltage = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Voltage Magnitude (MV)',
                        data: [],
                        borderColor: this.colors.primary,
                        backgroundColor: this.colors.primary + '20',
                        tension: 0.1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Voltage Phase (°)',
                        data: [],
                        borderColor: this.colors.secondary,
                        backgroundColor: this.colors.secondary + '20',
                        tension: 0.1,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Time (μs)'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Voltage Magnitude (MV)',
                            color: this.colors.primary
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Phase (°)',
                            color: this.colors.secondary
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                },
                animation: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }
    
    /**
     * Create power chart (forward and reflected)
     */
    createPowerChart() {
        const ctx = document.getElementById('powerChart');
        if (!ctx) {
            console.error('powerChart element not found');
            return;
        }
        
        this.charts.power = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Forward Power (kW)',
                        data: [],
                        borderColor: this.colors.success,
                        backgroundColor: this.colors.success + '20',
                        tension: 0.1
                    },
                    {
                        label: 'Reflected Power (kW)',
                        data: [],
                        borderColor: this.colors.danger,
                        backgroundColor: this.colors.danger + '20',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Time (μs)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Power (kW)'
                        },
                        beginAtZero: true
                    }
                },
                animation: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }
    
    /**
     * Create detuning chart
     */
    createDetuningChart() {
        const ctx = document.getElementById('detuningChart');
        if (!ctx) {
            console.error('detuningChart element not found');
            return;
        }
        
        this.charts.detuning = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Detuning Frequency (Hz)',
                        data: [],
                        borderColor: this.colors.info,
                        backgroundColor: this.colors.info + '20',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Time (μs)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Detuning (Hz)'
                        }
                    }
                },
                animation: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }
    
    /**
     * Create beam current and stored energy chart
     */
    createBeamChart() {
        const ctx = document.getElementById('beamChart');
        if (!ctx) {
            console.error('beamChart element not found');
            return;
        }
        
        this.charts.beam = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Beam Current (mA)',
                        data: [],
                        borderColor: this.colors.success,
                        backgroundColor: this.colors.success + '20',
                        tension: 0.1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Stored Energy (J)',
                        data: [],
                        borderColor: this.colors.warning,
                        backgroundColor: this.colors.warning + '20',
                        tension: 0.1,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Time (μs)'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Beam Current (mA)',
                            color: this.colors.success
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Stored Energy (J)',
                            color: this.colors.warning
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                },
                animation: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }
    
    /**
     * Update all charts with new data
     */
    updateCharts(dataPoint) {
        const time_us = dataPoint.time * 1e6; // Convert to microseconds
        
        // Update voltage chart
        if (this.charts.voltage) {
            this.charts.voltage.data.datasets[0].data.push({
                x: time_us,
                y: dataPoint.vc_magnitude
            });
            this.charts.voltage.data.datasets[1].data.push({
                x: time_us,
                y: dataPoint.vc_phase
            });
            
            // Limit data points
            if (this.charts.voltage.data.datasets[0].data.length > this.dataBufferSize) {
                this.charts.voltage.data.datasets[0].data.shift();
                this.charts.voltage.data.datasets[1].data.shift();
            }
            
            this.charts.voltage.update('none');
        }
        
        // Update power chart
        if (this.charts.power) {
            this.charts.power.data.datasets[0].data.push({
                x: time_us,
                y: dataPoint.forward_power
            });
            this.charts.power.data.datasets[1].data.push({
                x: time_us,
                y: dataPoint.reflected_power
            });
            
            // Limit data points
            if (this.charts.power.data.datasets[0].data.length > this.dataBufferSize) {
                this.charts.power.data.datasets[0].data.shift();
                this.charts.power.data.datasets[1].data.shift();
            }
            
            this.charts.power.update('none');
        }
        
        // Update detuning chart
        if (this.charts.detuning) {
            this.charts.detuning.data.datasets[0].data.push({
                x: time_us,
                y: dataPoint.detuning
            });
            
            // Limit data points
            if (this.charts.detuning.data.datasets[0].data.length > this.dataBufferSize) {
                this.charts.detuning.data.datasets[0].data.shift();
            }
            
            this.charts.detuning.update('none');
        }
        
        // Update beam chart
        if (this.charts.beam) {
            this.charts.beam.data.datasets[0].data.push({
                x: time_us,
                y: dataPoint.beam_current
            });
            this.charts.beam.data.datasets[1].data.push({
                x: time_us,
                y: dataPoint.stored_energy
            });
            
            // Limit data points
            if (this.charts.beam.data.datasets[0].data.length > this.dataBufferSize) {
                this.charts.beam.data.datasets[0].data.shift();
                this.charts.beam.data.datasets[1].data.shift();
            }
            
            this.charts.beam.update('none');
        }
    }
    
    /**
     * Clear all charts
     */
    clearCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.data && chart.data.datasets) {
                chart.data.datasets.forEach(dataset => {
                    dataset.data = [];
                });
                chart.update();
            }
        });
    }
    
    /**
     * Resize all charts (needed for responsive layout)
     */
    resizeCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.resize === 'function') {
                chart.resize();
            }
        });
    }
    
    /**
     * Destroy all charts
     */
    destroy() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
        this.charts = {};
    }
}
