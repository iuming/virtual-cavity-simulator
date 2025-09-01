/**
 * Virtual Cavity RF Simulator - Chart Management
 * 
 * Handles all chart creation, updates, and data visualization
 * using Chart.js for real-time plotting.
 */

class ChartManager {
    constructor() {
        this.charts = {};
        this.dataBufferSize = 500; // Number of points to display
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
        this.createMainChart();
        this.createVoltageChart();
        this.createReflectedChart();
    }
    
    /**
     * Create main real-time chart
     */
    createMainChart() {
        const ctx = document.getElementById('mainChart').getContext('2d');
        
        this.charts.main = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Cavity Voltage (MV)',
                        data: [],
                        borderColor: this.colors.primary,
                        backgroundColor: this.colors.primary + '20',
                        tension: 0.1,
                        pointRadius: 0,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Detuning (Hz)',
                        data: [],
                        borderColor: this.colors.info,
                        backgroundColor: this.colors.info + '20',
                        tension: 0.1,
                        pointRadius: 0,
                        yAxisID: 'y1'
                    },
                    {
                        label: 'Forward Power (kW)',
                        data: [],
                        borderColor: this.colors.success,
                        backgroundColor: this.colors.success + '20',
                        tension: 0.1,
                        pointRadius: 0,
                        yAxisID: 'y2'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Real-time Cavity Response'
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    x: {
                        type: 'linear',
                        title: {
                            display: true,
                            text: 'Time (s)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(4);
                            }
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Cavity Voltage (MV)',
                            color: this.colors.primary
                        },
                        ticks: {
                            color: this.colors.primary
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Detuning (Hz)',
                            color: this.colors.info
                        },
                        ticks: {
                            color: this.colors.info
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    },
                    y2: {
                        type: 'linear',
                        display: false,
                        position: 'right'
                    }
                }
            }
        });
    }
    
    /**
     * Create voltage magnitude and phase chart
     */
    createVoltageChart() {
        const ctx = document.getElementById('voltageChart').getContext('2d');
        
        this.charts.voltage = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Magnitude (MV)',
                        data: [],
                        borderColor: this.colors.primary,
                        backgroundColor: this.colors.primary + '20',
                        tension: 0.1,
                        pointRadius: 0,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Phase (deg)',
                        data: [],
                        borderColor: this.colors.warning,
                        backgroundColor: this.colors.warning + '20',
                        tension: 0.1,
                        pointRadius: 0,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    x: {
                        type: 'linear',
                        title: {
                            display: true,
                            text: 'Time (s)'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Magnitude (MV)',
                            color: this.colors.primary
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Phase (deg)',
                            color: this.colors.warning
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Create reflected power chart
     */
    createReflectedChart() {
        const ctx = document.getElementById('reflectedChart').getContext('2d');
        
        this.charts.reflected = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Reflected Power (kW)',
                        data: [],
                        borderColor: this.colors.danger,
                        backgroundColor: this.colors.danger + '20',
                        tension: 0.1,
                        pointRadius: 0,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    x: {
                        type: 'linear',
                        title: {
                            display: true,
                            text: 'Time (s)'
                        }
                    },
                    y: {
                        type: 'linear',
                        title: {
                            display: true,
                            text: 'Power (kW)'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    /**
     * Update all charts with new data point
     */
    updateCharts(dataPoint) {
        const timePoint = { x: dataPoint.time, y: dataPoint.vc_magnitude };
        const detuningPoint = { x: dataPoint.time, y: dataPoint.detuning };
        const forwardPowerPoint = { x: dataPoint.time, y: dataPoint.forward_power };
        const phasePoint = { x: dataPoint.time, y: dataPoint.vc_phase };
        const reflectedPoint = { x: dataPoint.time, y: dataPoint.reflected_power };
        
        // Update main chart
        this.addDataPoint(this.charts.main, 0, timePoint);
        this.addDataPoint(this.charts.main, 1, detuningPoint);
        this.addDataPoint(this.charts.main, 2, forwardPowerPoint);
        
        // Update voltage chart
        this.addDataPoint(this.charts.voltage, 0, timePoint);
        this.addDataPoint(this.charts.voltage, 1, phasePoint);
        
        // Update reflected power chart
        this.addDataPoint(this.charts.reflected, 0, reflectedPoint);
        
        // Update chart displays
        this.charts.main.update('none');
        this.charts.voltage.update('none');
        this.charts.reflected.update('none');
    }
    
    /**
     * Add data point to specific dataset
     */
    addDataPoint(chart, datasetIndex, point) {
        const dataset = chart.data.datasets[datasetIndex];
        dataset.data.push(point);
        
        // Limit buffer size
        if (dataset.data.length > this.dataBufferSize) {
            dataset.data.shift();
        }
    }
    
    /**
     * Clear all chart data
     */
    clearCharts() {
        Object.values(this.charts).forEach(chart => {
            chart.data.datasets.forEach(dataset => {
                dataset.data = [];
            });
            chart.update();
        });
    }
    
    /**
     * Set autoscale for all charts
     */
    setAutoscale(enabled) {
        Object.values(this.charts).forEach(chart => {
            Object.keys(chart.options.scales).forEach(scaleKey => {
                if (scaleKey !== 'x') {
                    if (enabled) {
                        delete chart.options.scales[scaleKey].min;
                        delete chart.options.scales[scaleKey].max;
                    }
                }
            });
            chart.update();
        });
    }
    
    /**
     * Update chart time range
     */
    updateTimeRange(minTime, maxTime) {
        Object.values(this.charts).forEach(chart => {
            chart.options.scales.x.min = minTime;
            chart.options.scales.x.max = maxTime;
            chart.update('none');
        });
    }
    
    /**
     * Resize charts (useful for responsive layouts)
     */
    resizeCharts() {
        Object.values(this.charts).forEach(chart => {
            chart.resize();
        });
    }
    
    /**
     * Get chart screenshot as base64 image
     */
    getChartImage(chartName) {
        if (this.charts[chartName]) {
            return this.charts[chartName].toBase64Image();
        }
        return null;
    }
    
    /**
     * Set chart theme (light/dark)
     */
    setTheme(theme) {
        const gridColor = theme === 'dark' ? '#444' : '#e0e0e0';
        const textColor = theme === 'dark' ? '#fff' : '#333';
        
        Object.values(this.charts).forEach(chart => {
            // Update grid colors
            Object.keys(chart.options.scales).forEach(scaleKey => {
                chart.options.scales[scaleKey].grid.color = gridColor;
                chart.options.scales[scaleKey].ticks.color = textColor;
                if (chart.options.scales[scaleKey].title) {
                    chart.options.scales[scaleKey].title.color = textColor;
                }
            });
            
            // Update plugins
            if (chart.options.plugins.title) {
                chart.options.plugins.title.color = textColor;
            }
            if (chart.options.plugins.legend) {
                chart.options.plugins.legend.labels.color = textColor;
            }
            
            chart.update();
        });
    }
}

// Make available globally
window.ChartManager = ChartManager;
