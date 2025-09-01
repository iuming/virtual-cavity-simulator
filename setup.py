#!/usr/bin/env python3
"""
Setup script for Virtual Cavity RF Simulator

Project: Virtual Cavity RF Simulator
Author: Ming Liu (mliu@ihep.ac.cn)
Institution: Institute of High Energy Physics, Chinese Academy of Sciences
Created: 2025-09-01
Version: 1.0.0
"""

from setuptools import setup, find_packages
import os

# Read long description from README
def read_long_description():
    """Read the long description from README.md"""
    here = os.path.abspath(os.path.dirname(__file__))
    try:
        with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Virtual Cavity RF Simulator - A comprehensive RF cavity simulation platform"

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt"""
    here = os.path.abspath(os.path.dirname(__file__))
    try:
        with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return ['numpy>=1.19.0', 'matplotlib>=3.3.0']

# Package metadata
setup(
    name="virtual-cavity-simulator",
    version="1.0.0",
    author="Ming Liu",
    author_email="mliu@ihep.ac.cn",
    description="A comprehensive RF cavity simulation platform with advanced GUI",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/iuming/virtual-cavity-simulator",
    project_urls={
        "Bug Reports": "https://github.com/iuming/virtual-cavity-simulator/issues",
        "Source": "https://github.com/iuming/virtual-cavity-simulator",
        "Documentation": "https://github.com/iuming/virtual-cavity-simulator/docs",
    },
    
    # Package configuration
    packages=find_packages(),
    include_package_data=True,
    
    # Dependencies
    install_requires=read_requirements(),
    python_requires=">=3.7",
    
    # Entry points for command-line scripts
    entry_points={
        'console_scripts': [
            'virtual-cavity-gui=launch_gui:main',
            'virtual-cavity-sim=sim_cavity_standalone:main',
        ],
    },
    
    # Package data
    package_data={
        '': ['*.txt', '*.md', '*.yml', '*.yaml'],
    },
    
    # Classification
    classifiers=[
        # Development status
        "Development Status :: 5 - Production/Stable",
        
        # Intended audience
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        
        # Topic
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Programming language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        
        # Operating system
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        
        # Environment
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        
        # Natural language
        "Natural Language :: English",
        
        # Interface
        "User Interface :: Desktop",
    ],
    
    # Keywords for discovery
    keywords=[
        "rf-cavity", "accelerator-physics", "simulation", "gui", "llrf",
        "superconducting-cavity", "beam-dynamics", "control-systems",
        "scientific-computing", "visualization", "real-time", "physics"
    ],
    
    # Additional metadata
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'black>=21.0.0',
            'isort>=5.9.0',
            'flake8>=3.9.0',
            'mypy>=0.910',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=0.5.0',
        ],
        'jupyter': [
            'jupyter>=1.0.0',
            'ipywidgets>=7.6.0',
        ],
    },
    
    # ZIP safe
    zip_safe=False,
)
