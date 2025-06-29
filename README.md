# BioImageSuiteLite

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/bioimagesuitelite.svg)](https://pypi.org/project/bioimagesuitelite/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15686106.svg)](https://doi.org/10.5281/zenodo.15686106)

**An Interactive Open-Source Platform for Automated Detection and Analysis of Transient Events in Time-Lapse Microscopy**

![1750010543782](image/README/1750010543782.png)

***A screenshot of the main BioImageSuiteLite interface.***

---

## Overview

BioImageSuiteLite is a user-friendly desktop application designed for biologists and researchers to analyze time-lapse microscopy data. It simplifies the entire workflow from data import to results export, enabling rapid, reproducible analysis of cellular events.

The tool provides an intuitive graphical user interface (GUI) built on the powerful [Napari](https://napari.org/) viewer, allowing users to perform end-to-end analysis of cellular events.

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
pip install bioimagesuitelite
```

For the latest development version, you can also install directly from GitHub:

```bash
pip install git+https://github.com/InnovationLine/BioImageSuiteLite.git
```

## Quick Start

1. **Launch the application:**
   Open your terminal or command prompt (with the virtual environment activated) and run:
   ```bash
   bioimagesuitelite
   ```
2. **Load Data:**
   Click the **"Load File"** button to open your microscopy data (`.avi` or `.tif`/`.tiff`).
3. **Draw an ROI:**
   Select the **Polygon tool** from the Napari layer controls (top left) and draw one or more regions around the cells you want to analyze.
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

If you use BioImageSuiteLite in your research, please cite it using the metadata below.

## Tutorial: An Interactive Guide

For a hands-on tutorial that walks you through a complete analysis workflow—from loading data to exporting results—please see our comprehensive Jupyter Notebook. This is the best place to start to understand the full capabilities of BioImageSuiteLite.

<a href="./examples/comprehensive_analysis_guide.ipynb" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Launch-Interactive%20Tutorial-blue?style=for-the-badge&logo=jupyter" alt="Launch Interactive Tutorial" />
</a>

## For Developers

We welcome contributions! To set up a development environment:

### Setting up the Environment

```bash
# Clone the repository
git clone https://github.com/InnovationLine/BioImageSuiteLite.git
cd BioImageSuiteLite

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install in editable mode with developer dependencies
pip install -e .
```

### Running the GUI from source

To launch the GUI directly from the source code, run:

```bash
python -m BioImageSuiteLite.gui_manager
```

For more details on the project structure and architecture, please see our [Architecture Guide](./ARCHITECTURE.md).

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
This license permits free use, modification, and distribution of the software, provided the original copyright and license notice are included in any copies.

## Citation

*BioImageSuiteLite* is academic software. If you use it in your research, please cite it as follows:

> Dasgupta, Rinki, & Das, Kaushik. (2025). *BioImageSuiteLite* (Version 0.1.3) \[Software\]. Zenodo. https://doi.org/10.5281/zenodo.15686106
