# Virtual Cavity RF Simulator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)]()
[![Website](https://img.shields.io/badge/website-online-brightgreen.svg)](https://iuming.github.io/virtual-cavity-simulator/)

## ⚠️ Important Usage Guidelines

### 🐍 Python Version (Recommended for Scientific Applications)
- **Use for**: Research, engineering calculations, precise simulations
- **Accuracy**: Full numerical precision with validated LLRFLibsPy algorithms
- **Command**: `python advanced_cavity_gui.py`

### 🌐 Web Version (Educational/Demo Purposes Only)
- **Use for**: Educational demonstrations, basic visualization, parameter exploration
- **⚠️ Limitations**: Approximate results only - not suitable for scientific calculations
- **Note**: JavaScript implementation has inherent numerical precision limitations

---

🌐 **Project Website**: [https://iuming.github.io/virtual-cavity-simulator/](https://iuming.github.io/virtual-cavity-simulator/)

🚀 **Web Demo**: [Try the live web version](https://iuming.github.io/virtual-cavity-simulator/simulator.html) - No installation required!

A comprehensive **Radio Frequency (RF) cavity simulation platform** with advanced graphical user interface for accelerator physics applications. Available both as a desktop Python application and a web-based simulator that runs in your browser.

## 🌟 Features

### 🎛️ Real-time Multi-Parameter Control
- **Amplitude Control**: 0.0-2.0 range with precision sliders
- **Phase Control**: -180° to +180° real-time phase adjustment
- **Frequency Offset**: ±2000Hz detuning control
- **Beam Current**: 0-0.02A beam loading simulation
- **Mode Switching**: CW/Pulsed operation modes

### 📊 Multi-Curve Dynamic Visualization
- **Cavity Voltage**: Real-time magnitude and phase monitoring
- **Reflected Power**: Forward/reflected power analysis
- **Detuning**: Frequency offset tracking
- **Mechanical Modes**: 5-mode microphonics simulation
- **Response Curves**: Parameter sweep visualization

### 🔍 Advanced Data Analysis
- **Data Recording**: Start/stop recording with timestamp
- **Export Formats**: CSV and JSON data export
- **Historical Playback**: Data replay and analysis
- **Large Dataset**: 10,000+ data points buffer

### 🧪 Parameter Scanning
- **Multi-Parameter**: Amplitude/Phase/Frequency/Current scanning
- **Custom Ranges**: User-defined scan parameters
- **Response Analysis**: 20-point automatic response curves
- **Progress Tracking**: Real-time scan progress display

## 🚀 Quick Start

### 🌐 Web Version (Recommended for Quick Testing)

**No installation required!** Try the simulator directly in your browser:

👉 **[Launch Web Simulator](https://iuming.github.io/virtual-cavity-simulator/simulator.html)**

Features:
- Runs on any modern browser (desktop/mobile)
- Real-time RF cavity simulation
- Interactive parameter control
- Data export (CSV/JSON)
- Responsive design

### 🖥️ Desktop Version (Full Features)

For advanced research and maximum accuracy:

### Prerequisites

```bash
# Python 3.7 or higher
python --version

# Required packages
pip install numpy matplotlib tkinter
```

### Installation

```bash
# Clone the repository
git clone https://github.com/iuming/virtual-cavity-simulator.git
cd virtual-cavity-simulator

# Install dependencies
pip install -r requirements.txt

# Install LLRFLibsPy (required)
# Follow LLRFLibsPy installation instructions
```

### Launch the Simulator

```bash
# Start the GUI application
python launch_gui.py

# Or run standalone simulation
python sim_cavity_standalone.py
```

## 📖 Usage Guide

### Basic Operation

1. **Start Simulation**: Click "Start" to begin real-time simulation
2. **Parameter Control**: Use sliders to adjust RF parameters
3. **Data Recording**: Click "Start Recording" to save data
4. **Parameter Scanning**: Select parameter and range for automatic scanning
5. **Export Data**: Save results in CSV or JSON format

### Advanced Features

- **Resonance Analysis**: Set frequency offset to -460Hz for resonance observation
- **Transient Response**: Switch to pulsed mode for transient analysis
- **Linear Region**: Scan amplitude parameters to analyze linear operation
- **Beam Loading**: Adjust beam current to observe loading effects

## 🏗️ Technical Architecture

### Core Components

- **RF Source Module**: Signal generation and modulation
- **Cavity Dynamics**: State-space cavity model with mechanical coupling
- **Visualization Engine**: Real-time multi-plot display system
- **Data Management**: Recording, storage, and export functionality

### Simulation Parameters

- **Time Resolution**: 1 μs time steps
- **Cavity Frequency**: 1.3 GHz (configurable)
- **Quality Factor**: 3×10⁶ (loaded)
- **Mechanical Modes**: 5 modes (280, 341, 460, 487, 618 Hz)
- **Beam Parameters**: Variable current 0-20 mA

## 📁 Project Structure

```
virtual-cavity-simulator/
├── advanced_cavity_gui.py     # Main GUI application
├── sim_cavity_standalone.py   # Standalone simulation
├── launch_gui.py              # Application launcher
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── LICENSE                    # MIT license
├── docs/                      # Documentation
│   ├── installation.md        # Installation guide
│   ├── user_guide.md          # User manual
│   └── api_reference.md       # API documentation
├── examples/                  # Example scripts
│   ├── basic_simulation.py    # Basic usage example
│   └── parameter_sweep.py     # Parameter scanning example
└── tests/                     # Unit tests
    ├── test_simulation.py     # Simulation tests
    └── test_gui.py            # GUI tests
```

## 🔬 Scientific Applications

### Accelerator Physics
- **Cavity Design**: RF cavity parameter optimization
- **Control System**: LLRF control algorithm development
- **Microphonics**: Mechanical vibration analysis
- **Beam Loading**: Beam-cavity interaction studies

### Research Areas
- **Superconducting Cavities**: SRF cavity dynamics
- **Linear Accelerators**: LINAC RF system design
- **Free Electron Lasers**: FEL RF control systems
- **Storage Rings**: Synchrotron RF cavity analysis

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/iuming/virtual-cavity-simulator.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📊 Performance

- **Real-time Performance**: 1000+ simulations/second
- **Memory Usage**: <100MB for typical operations
- **Data Capacity**: 10,000+ data points with smooth visualization
- **Platform Support**: Windows, Linux, macOS

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [User Manual](docs/user_guide.md)
- [API Reference](docs/api_reference.md)
- [Examples](examples/)

## 🐛 Known Issues

- **Windows Installation**: Some dependencies may require Microsoft C++ Build Tools
- **Matrix Conditioning**: Scipy warnings for ill-conditioned matrices (non-critical)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ming Liu**
- Email: mliu@ihep.ac.cn
- Institution: Institute of High Energy Physics, Chinese Academy of Sciences
- ORCID: [0000-0001-6239-1180](https://orcid.org/0000-0001-6239-1180)

## 🙏 Acknowledgments

- **LLRFLibsPy Team**: For the excellent RF simulation framework
- **IHEP**: For supporting this research and development
- **Community**: For feedback and contributions

## 📈 Citation

If you use this software in your research, please cite:

```bibtex
@software{liu2025virtualcavity,
  title={Virtual Cavity RF Simulator},
  author={Liu, Ming},
  year={2025},
  institution={Institute of High Energy Physics, Chinese Academy of Sciences},
  url={https://github.com/iuming/virtual-cavity-simulator}
}
```

## 🔗 Related Projects

- [LLRFLibsPy](https://github.com/aaqiao/LLRFLibsPy) - Low-Level RF Library for Python
- [pythonSoftIOC](https://github.com/dls-controls/pythonSoftIOC) - Python Soft IOC Framework

---

⭐ **Star this repository** if you find it useful!

📧 **Contact**: For questions or support, please email mliu@ihep.ac.cn
