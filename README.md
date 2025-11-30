# TransiScope

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/transiscope.svg)](https://pypi.org/project/transiscope/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17762015.svg)](https://doi.org/10.5281/zenodo.16789347)

**An Interactive Open-Source Platform for Automated Detection and Analysis of Transient Events in Time-Lapse Microscopy**

![1750010543782](image/README/1750010543782.png)

***A screenshot of the main TransiScope interface.***

---

## Overview

TransiScope is a user-friendly desktop application designed for biologists and researchers to analyze time-lapse microscopy data. It simplifies the entire workflow from data import to results export, enabling rapid, reproducible analysis of cellular events.

The tool provides an intuitive graphical user interface (GUI) built on the powerful [Napari](https://napari.org/) viewer, allowing users to perform end-to-end analysis of cellular events.

## Statement of Need

Quantifying transient cellular events—such as calcium transients, vesicle fusion, or fluorescence fluctuations—is fundamental to understanding biological processes. While powerful algorithms for event detection exist (Difference of Gaussians, Otsu thresholding, peak detection), applying them requires either:

- **Programming expertise**: Writing custom scripts in ImageJ/Fiji or Python
- **Manual parameter tuning**: Time-consuming trial-and-error that introduces subjective bias
- **Complex multi-step workflows**: Juggling multiple tools and file formats

Existing bioimage analysis platforms face specific limitations:

- **ImageJ/Fiji** with plugins like TrackMate excel at particle tracking but require complex, multi-step workflows for temporal event detection
- **CellProfiler** is optimized for high-throughput segmentation but not for analyzing rapid intensity-based temporal events within user-defined regions
- **Specialized tools** like ThunderSTORM focus on single-molecule localization, not functional temporal dynamics

**TransiScope bridges this gap** by providing:

1. **Interactive, data-driven parameter optimization**: Analyzes multiple regions of interest (ROIs) to automatically propose optimal detection parameters, eliminating subjective manual tuning
2. **Unified workflow**: Complete analysis from file import to results export within a single, intuitive GUI—no scripting required
3. **Automated normalization**: Event rates normalized by time and ROI area (events/sec/µm²) for direct cross-experiment comparison
4. **Complete transparency**: All parameters and analysis steps automatically logged for reproducibility

TransiScope makes sophisticated event detection accessible to biologists without computational backgrounds, while maintaining the rigor and reproducibility required for quantitative research.

## Key Features

- **Versatile Data Import:** Load time-lapse microscopy data from both `.avi` video files and multi-page `.tif`/`.tiff` image stacks.
- **Interactive ROI Drawing:** Easily draw, manage, and analyze multiple Regions of Interest (ROIs) on your data using Napari's intuitive tools.
- **Advanced Event Detection:** Utilize multiple algorithms for event detection, including:
  - **Threshold-based:** Simple and effective for clear signals.
  - **Difference of Gaussians (DoG):** Robustly detects blob-like features and transient intensity peaks.
  - **Scisson-like (Step Detection):** (In development) For analyzing step-like changes in intensity.
- **Automated Analysis & Export:** Automatically calculate normalized event rates (events/sec/µm²) and export detailed event data and ROI coordinates to CSV for further analysis.
- **Integrated Plotting:** Instantly visualize analysis results with built-in plotting for event rates and intensity traces.

## Installation

We recommend installing BioImageSuiteLite into a dedicated Python virtual environment.

```bash
# First, create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Now, install the package from PyPI
pip install transiscope
```

For the latest development version, you can also install directly from GitHub:

```bash
pip install git+https://github.com/InnovationLine/TransiScope.git
```

## Quick Start

1. **Launch the application:**
   Open your terminal or command prompt (with the virtual environment activated) and run:

   ```bash
   transiscope
   ```
2. **Load Data:**
   Click the **"Load File"** button to open your microscopy data (`.avi` or `.tif`/`.tiff`).
3. **Draw an ROI:**Select your preferred **ROI drawing mode** (Rectangle, Ellipse, Polygon, or Freehand Path) from the dropdown menu in the "Preprocessing & ROI" section, then draw one or more regions around the cells you want to analyze. The interface now provides helpful tooltips for all controls.
4. **Run Analysis:**
   Adjust parameters in the GUI dock widget as needed (e.g., Gaussian sigma, thresholding method). Click the **"Run Analysis"** button to start processing.
5. **Explore Results:**
   View the generated plots for event traces and intensity profiles. Use the **"Save Data"** button to export your quantitative results to a CSV file.

For a detailed reference, see the full [User Guide](./UserGuide.md).

## System Requirements

- Python >= 3.8
- The core dependencies are listed in the `pyproject.toml` file and include:
  - `numpy`
  - `scipy`
  - `opencv-python-headless`
  - `tifffile`
  - `scikit-image`
  - `napari[all]`
  - `shapely`
  - `ruptures`

## How to Cite

If you use TransiScope in your research, please cite it using the metadata below.

## Tutorial: An Interactive Guide

For a hands-on tutorial that walks you through a complete analysis workflow—from loading data to exporting results—please see our comprehensive Jupyter Notebook. This is the best place to start to understand the full capabilities of TransiScope.

<a href="./examples/comprehensive_analysis_guide.ipynb" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Launch-Interactive%20Tutorial-blue?style=for-the-badge&logo=jupyter" alt="Launch Interactive Tutorial" />
</a>

## For Developers

We welcome contributions! To set up a development environment:

### Setting up the Environment

```bash
# Clone the repository
git clone https://github.com/InnovationLine/TransiScope.git
cd TransiScope

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install in editable mode with developer dependencies
pip install -e .
```

### Running the GUI from source

To launch the GUI directly from the source code, run:

```bash
python -m TransiScope.gui_manager
```

For more details on the project structure and architecture, please see our [Architecture Guide](./ARCHITECTURE.md).

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
This license permits free use, modification, and distribution of the software, provided the original copyright and license notice are included in any copies.

## Citation

*TransiScope* is academic software. If you use it in your research, please cite it as follows:

> Dasgupta, Rinki, & Das, Kaushik. (2025). *TransiScope* (Version 1.0.0) \[Software\]. Zenodo. https://doi.org/10.5281/zenodo.17762015
