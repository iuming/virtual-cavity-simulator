# Virtual Cavity RF Simulator - Web Version

🌐 **Live Demo**: [https://iuming.github.io/virtual-cavity-simulator/](https://iuming.github.io/virtual-cavity-simulator/)

## Overview

This is a web-based version of the Virtual Cavity RF Simulator that runs entirely in your browser. It provides real-time RF cavity simulation with an interactive graphical interface, making it accessible without requiring Python installation.

## Features

### 🎛️ Real-time Control Interface
- **Amplitude Control**: Adjustable RF drive amplitude (0.0 - 2.0)
- **Phase Control**: RF phase adjustment (-180° to +180°)
- **Frequency Offset**: Detuning control (±2000 Hz)
- **Beam Current**: Variable beam loading (0 - 20 mA)
- **Operation Modes**: CW and Pulsed modes

### 📊 Interactive Visualization
- **Multi-curve Display**: Real-time plotting with Chart.js
- **Cavity Voltage**: Magnitude and phase monitoring
- **Power Analysis**: Forward and reflected power tracking
- **Detuning Display**: Frequency offset visualization
- **Responsive Design**: Works on desktop, tablet, and mobile

### 💾 Data Management
- **Real-time Recording**: Start/stop data recording
- **Export Options**: CSV and JSON format export
- **Data Buffer**: 10,000+ data points capacity
- **Clear Function**: Reset all recorded data

## Technology Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Charts**: Chart.js for real-time plotting
- **Physics Engine**: Custom JavaScript RF cavity simulation
- **Icons**: Font Awesome
- **Responsive Framework**: Bootstrap Grid System

## Physics Implementation

The web version implements a simplified but accurate RF cavity model:

### Cavity Dynamics
```javascript
// Cavity voltage differential equation
dVc/dt = -j*ω_detuning*Vc - (ω0/2Q)*Vc + (ω0/2)*V_drive - (ω0/2)*I_beam*R/Q
```

### Key Parameters
- **Resonant Frequency**: 1.3 GHz
- **Quality Factor**: 3×10⁶ (loaded)
- **R/Q**: 1036 Ω
- **Time Step**: 1 μs
- **Mechanical Modes**: 5 microphonic resonances

### Microphonics Simulation
The simulator includes 5 mechanical resonance modes:
- 280 Hz, 341 Hz, 460 Hz, 487 Hz, 618 Hz
- Each with realistic Q factors and coupling

## Usage Instructions

### Getting Started
1. **Open the Web App**: Visit the live demo link
2. **Start Simulation**: Click "Start Simulation" button
3. **Adjust Parameters**: Use sliders to change RF parameters
4. **Monitor Response**: Watch real-time plots and displays

### Data Recording
1. **Start Recording**: Click "Start Recording" to save data
2. **Export Data**: Use "Export Data" for CSV/JSON download
3. **Clear Data**: Reset all recorded data when needed

### Keyboard Shortcuts
- **Ctrl + Space**: Start/Stop simulation
- **Ctrl + R**: Reset simulation
- **Ctrl + S**: Toggle recording

## File Structure

```
web/
├── index.html          # Main application page
├── css/
│   └── style.css      # Custom styles
├── js/
│   ├── simulator.js   # RF cavity physics engine
│   ├── charts.js      # Chart management
│   └── main.js        # Main application logic
└── README.md          # This file
```

## Comparison with Desktop Version

| Feature | Web Version | Desktop Version |
|---------|-------------|-----------------|
| Installation | None required | Python + dependencies |
| Platform | Any modern browser | Windows, Linux, macOS |
| Performance | Good (JavaScript) | Excellent (Python/NumPy) |
| Physics Accuracy | Simplified but realistic | Full LLRFLibsPy implementation |
| Data Export | CSV, JSON | CSV, JSON, MATLAB |
| Real-time Plot | Chart.js | Matplotlib |
| Mobile Support | Yes | No |

## Browser Compatibility

- **Chrome**: 90+ ✅
- **Firefox**: 88+ ✅
- **Safari**: 14+ ✅
- **Edge**: 90+ ✅
- **Mobile Browsers**: iOS Safari 14+, Chrome Mobile 90+ ✅

## Performance Notes

- **Update Rate**: ~100 FPS visualization
- **Data Points**: 500 points displayed, 10,000 stored
- **Memory Usage**: <50MB typical
- **CPU Usage**: Low (optimized JavaScript)

## Development

To run locally:

```bash
# Clone repository
git clone https://github.com/iuming/virtual-cavity-simulator.git
cd virtual-cavity-simulator/web

# Serve locally (Python)
python -m http.server 8000

# Or use any static file server
# Then open http://localhost:8000
```

## Future Enhancements

- [ ] Parameter scanning automation
- [ ] Advanced microphonics models
- [ ] FFT spectrum analysis
- [ ] Multi-cavity simulation
- [ ] Custom cavity parameter input
- [ ] Dark mode theme
- [ ] Touch gestures for mobile
- [ ] WebGL acceleration for higher performance

## Contributing

Contributions are welcome! Please see the main repository's [Contributing Guidelines](../CONTRIBUTING.md).

## License

MIT License - see [LICENSE](../LICENSE) file for details.

## Author

**Ming Liu**
- Email: mliu@ihep.ac.cn
- Institution: Institute of High Energy Physics, Chinese Academy of Sciences
- ORCID: [0000-0001-6239-1180](https://orcid.org/0000-0001-6239-1180)

---

💡 **Tip**: For production research or high-precision simulations, consider using the full desktop version with LLRFLibsPy for maximum accuracy and performance.
