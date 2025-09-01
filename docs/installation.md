# Installation Guide

This guide provides detailed instructions for installing the Virtual Cavity RF Simulator on different platforms.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, Ubuntu 18.04+, macOS 10.14+
- **Python**: 3.7 or higher
- **Memory**: 4 GB RAM minimum, 8 GB recommended
- **Storage**: 1 GB free disk space
- **Display**: 1024x768 minimum resolution

### Recommended Requirements
- **Python**: 3.9 or higher
- **Memory**: 16 GB RAM or more
- **Storage**: 5 GB free disk space for data and outputs
- **Display**: 1920x1080 or higher resolution

## Installation Methods

### Method 1: pip Installation (Recommended)

```bash
# Install from PyPI (when published)
pip install virtual-cavity-simulator

# Or install with development dependencies
pip install virtual-cavity-simulator[dev]
```

### Method 2: Source Installation

```bash
# Clone the repository
git clone https://github.com/iuming/virtual-cavity-simulator.git
cd virtual-cavity-simulator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Method 3: Conda Installation

```bash
# Create conda environment
conda create -n cavity-sim python=3.9
conda activate cavity-sim

# Install dependencies
conda install numpy matplotlib
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Platform-Specific Instructions

### Windows Installation

#### Prerequisites
1. **Python Installation**:
   - Download Python 3.9+ from [python.org](https://www.python.org/)
   - Ensure "Add to PATH" is checked during installation
   - Verify installation: `python --version`

2. **Git (Optional)**:
   - Download from [git-scm.com](https://git-scm.com/)
   - Or use GitHub Desktop

3. **Microsoft C++ Build Tools** (if needed):
   - Download from [Microsoft](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Required for some scientific packages

#### Installation Steps
```powershell
# Open PowerShell as Administrator
# Clone repository
git clone https://github.com/iuming/virtual-cavity-simulator.git
cd virtual-cavity-simulator

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Test installation
python launch_gui.py
```

#### Common Windows Issues
- **DLL Errors**: Install Microsoft Visual C++ Redistributable
- **Permission Errors**: Run PowerShell as Administrator
- **Path Issues**: Ensure Python is in system PATH

### Linux Installation (Ubuntu/Debian)

#### Prerequisites
```bash
# Update package list
sudo apt update

# Install Python and development tools
sudo apt install python3 python3-pip python3-venv python3-dev
sudo apt install git build-essential

# Install GUI dependencies
sudo apt install python3-tk
```

#### Installation Steps
```bash
# Clone repository
git clone https://github.com/iuming/virtual-cavity-simulator.git
cd virtual-cavity-simulator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Test installation
python launch_gui.py
```

#### Common Linux Issues
- **GUI Issues**: Install `python3-tk` package
- **Permission Errors**: Use `sudo` for system packages
- **Display Issues**: Set `DISPLAY` environment variable

### macOS Installation

#### Prerequisites
1. **Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```

2. **Homebrew** (recommended):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Python**:
   ```bash
   brew install python
   ```

#### Installation Steps
```bash
# Clone repository
git clone https://github.com/iuming/virtual-cavity-simulator.git
cd virtual-cavity-simulator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test installation
python launch_gui.py
```

#### Common macOS Issues
- **tkinter Issues**: Install Python via Homebrew
- **Certificate Errors**: Update certificates or use `--trusted-host`
- **Permission Issues**: Use appropriate file permissions

## LLRFLibsPy Installation

The simulator requires LLRFLibsPy for RF simulation functionality.

### Installation from Source
```bash
# Clone LLRFLibsPy repository
git clone https://github.com/aaqiao/LLRFLibsPy.git
cd LLRFLibsPy

# Install dependencies
pip install -r requirements.txt

# Install LLRFLibsPy
pip install -e .
```

### Verification
```python
# Test LLRFLibsPy installation
python -c "from llrflibs.rf_sim import cav_ss_mech; print('LLRFLibsPy OK')"
```

## Dependency Management

### Core Dependencies
- **numpy**: Numerical computing foundation
- **matplotlib**: Plotting and visualization
- **scipy**: Scientific computing (indirect dependency)
- **tkinter**: GUI framework (usually included with Python)

### Optional Dependencies
- **jupyter**: For example notebooks
- **pytest**: For running tests
- **sphinx**: For building documentation

### Managing Dependencies
```bash
# List installed packages
pip list

# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade numpy

# Update all packages
pip install --upgrade -r requirements.txt
```

## Virtual Environment Setup

### Why Use Virtual Environments?
- Isolate project dependencies
- Avoid conflicts between projects
- Ensure reproducible installations
- Easy cleanup and management

### Creating Virtual Environments
```bash
# Using venv (built-in)
python -m venv cavity-sim-env
source cavity-sim-env/bin/activate  # Linux/macOS
cavity-sim-env\Scripts\activate     # Windows

# Using conda
conda create -n cavity-sim python=3.9
conda activate cavity-sim

# Using virtualenv
pip install virtualenv
virtualenv cavity-sim-env
source cavity-sim-env/bin/activate
```

## Verification and Testing

### Quick Verification
```bash
# Test Python installation
python --version

# Test package imports
python -c "import numpy, matplotlib, tkinter; print('Dependencies OK')"

# Test LLRFLibsPy
python -c "from llrflibs.rf_sim import cav_ss_mech; print('LLRFLibsPy OK')"

# Launch GUI test
python launch_gui.py
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=.

# Run specific test
python -m pytest tests/test_simulation.py
```

## Troubleshooting

### Common Installation Issues

#### ImportError: No module named 'tkinter'
**Solution**:
- Windows: Reinstall Python with tkinter option checked
- Linux: `sudo apt install python3-tk`
- macOS: `brew install python-tk`

#### ImportError: No module named 'llrflibs'
**Solution**:
- Install LLRFLibsPy following the instructions above
- Verify installation path and PYTHONPATH

#### GUI doesn't start / Display issues
**Solution**:
- Linux: Set `DISPLAY` environment variable
- Windows: Update graphics drivers
- macOS: Install Python via Homebrew

#### Permission denied errors
**Solution**:
- Use virtual environments
- Don't use `sudo` with pip
- Check file permissions

#### Compilation errors during installation
**Solution**:
- Windows: Install Microsoft C++ Build Tools
- Linux: Install `build-essential` package
- macOS: Install Xcode Command Line Tools

### Getting Help

If you encounter issues:

1. **Check the logs**: Look for error messages in terminal output
2. **Search issues**: Check [GitHub Issues](https://github.com/iuming/virtual-cavity-simulator/issues)
3. **Create issue**: Report new bugs with system information
4. **Contact support**: Email mliu@ihep.ac.cn for assistance

### System Information
When reporting issues, include:

```bash
# System information
python --version
pip --version
python -c "import platform; print(platform.platform())"

# Package versions
pip list | grep -E "(numpy|matplotlib|scipy)"

# Environment details
echo $PYTHONPATH
which python
```

## Performance Optimization

### Recommended Settings
- Use SSD storage for better I/O performance
- Allocate sufficient RAM (8GB+ recommended)
- Close unnecessary applications during simulation
- Use virtual environments to minimize conflicts

### Monitoring Performance
```python
# Monitor memory usage
import psutil
print(f"Memory usage: {psutil.virtual_memory().percent}%")

# Monitor CPU usage
import time
start_time = time.time()
# ... run simulation ...
elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time:.2f} seconds")
```

## Next Steps

After successful installation:

1. **Read the User Guide**: `docs/user_guide.md`
2. **Try Examples**: Check `examples/` directory
3. **Run Tests**: Verify functionality with test suite
4. **Explore Features**: Start with basic simulation and explore advanced features

For detailed usage instructions, see the [User Guide](user_guide.md).
