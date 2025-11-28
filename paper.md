---
title: 'TransiScope: An Interactive Platform for Automated Detection and Analysis of Transient Events in Time-Lapse Microscopy'
tags:
  - Python
  - microscopy
  - image analysis
  - event detection
  - calcium imaging
  - fluorescence microscopy
  - napari
authors:
  - name: Rinki Dasgupta
    orcid: 0000-0000-0000-0000
    affiliation: "1, 2"
  - name: Kaushik Das
    corresponding: true
    orcid: 0000-0000-0000-0000
    affiliation: 3
affiliations:
 - name: Department of Psychiatry and Neuroscience, Dell Medical Center, University of Texas at Austin, Austin, TX, 78701, USA
   index: 1
 - name: Department of Biology, Texas Woman's University, Denton, TX, 76204, USA
   index: 2
 - name: Department of Computer Applications, National Institute of Technology Jharkhand, Jamshedpur, 831014, India
   index: 3
date: 28 November 2025
bibliography: paper.bib
---

# Summary

Quantifying transient cellular events—such as calcium transients, vesicle exocytosis, and fluorescence fluctuations—is fundamental to understanding biological processes at the cellular level. `TransiScope` is an open-source, user-friendly desktop application built on Python and the Napari viewer that streamlines the complete workflow of detecting and analyzing such events in time-lapse microscopy data. The software provides an intuitive graphical interface that eliminates the need for programming expertise, while offering advanced features including interactive region-of-interest (ROI) management, data-driven parameter optimization, and multiple event detection algorithms (Difference of Gaussians, Otsu thresholding, step detection). Key innovations include automated parameter estimation from user-selected ROIs, complete algorithmic transparency through automated logging, and normalized quantification (events/sec/µm²) that enables direct comparison across experiments. TransiScope fills a critical usability gap in bioimage analysis, making sophisticated temporal event detection accessible to biologists without computational backgrounds.

# Statement of Need

Analyzing dynamic cellular processes from time-lapse microscopy requires detecting and quantifying transient events—discrete, short-lived changes in fluorescence intensity that represent biological phenomena such as neurotransmitter release, calcium signaling, or vesicle fusion [@Pelet2012; @Hummer2017]. While powerful algorithms for event detection exist, including Difference of Gaussians (DoG) filtering [@Yuan2014], Otsu thresholding [@Cao2019], and peak detection methods, applying these techniques currently requires either significant programming expertise or navigating complex, multi-step workflows that introduce subjective bias through manual parameter tuning [@OBrien2016; @Savage2023].

Existing bioimage analysis platforms face specific limitations for temporal event analysis:

- **ImageJ/Fiji** [@Schindelin2012] with plugins like TrackMate [@Cayuela2023] excel at particle tracking and segmentation but require complex, multi-step workflows for temporal event detection within user-defined regions
- **CellProfiler** [@Carpenter2006] is optimized for high-throughput segmentation-based analysis but not for analyzing rapid intensity-based temporal events  
- **Specialized tools** like ThunderSTORM [@Ovesny2014] focus on single-molecule localization microscopy, not functional temporal dynamics

This landscape reveals a critical usability gap: **no existing tool provides a unified, user-friendly workflow for biologists to perform robust temporal event analysis without coding skills.**

`TransiScope` addresses this gap through four key innovations:

1. **Interactive, data-driven parameter optimization**: Users draw multiple ROIs over representative cellular regions, and the software automatically analyzes their averaged intensity traces to propose optimal detection parameters. This eliminates subjective manual tuning while adapting to the specific signal characteristics of each dataset [@Held2013].

2. **Unified workflow in a single GUI**: Complete analysis from file import (AVI, TIFF) through ROI drawing, event detection, and results export occurs within one intuitive interface built on Napari [@Chiu2022]—no scripting, macro programming, or file format conversions required.

3. **Automated normalization for cross-experiment comparison**: Event rates are automatically normalized by both time and ROI area (events/sec/µm²), accounting for variations in acquisition duration and region size that would otherwise confound biological interpretation.

4. **Complete algorithmic transparency and reproducibility**: All parameters, detection thresholds, and processing steps are automatically logged with timestamps, ensuring that analyses are fully reproducible and scientifically auditable [@Dudda2025].

By making sophisticated event detection accessible while maintaining scientific rigor, `TransiScope` empowers a broader community of researchers to perform quantitative temporal analysis of cellular dynamics. The software is particularly valuable for laboratories studying neurotransmission, calcium signaling, exocytosis, and other rapid cellular processes where manual analysis is prohibitively time-consuming and prone to observer bias.

# Software Description

## Architecture

`TransiScope` follows a modular architecture with three logical layers:

- **User Interface Layer**: Built on Napari, providing interactive image display, ROI drawing tools (rectangle, ellipse, polygon, freehand), and a comprehensive control panel for parameter configuration
- **Application Logic Layer**: Pure Python modules handling file I/O (`io_operations.py`), ROI management and intensity extraction (`roi_handler.py`), event detection algorithms (`analysis_processor.py`), and logging (`utilities.py`)
- **External Libraries**: Leverages established open-source tools including NumPy [@Harris2020], SciPy [@Virtanen2020], scikit-image [@VanDerWalt2014], OpenCV [@Bradski2000], and Shapely for computational tasks

## Key Features

### Data Import and Preprocessing
- Supports `.avi` video files and multi-page `.tif`/`.tiff` image stacks
- Automatic conversion of color videos to greyscale
- Microscope calibration input (pixel size in µm) for physical unit calculations

### Interactive ROI Management
- Multiple drawing modes (rectangle, ellipse, polygon, freehand path) via Napari's shapes layer
- Real-time visualization of ROIs overlaid on time-lapse data
- ROI area calculation using Shapely for accurate normalization

### Event Detection Algorithms

**Difference of Gaussians (DoG)**: Detects blob-like features by subtracting two Gaussian-blurred versions of the intensity trace, with parameters σ₁ (narrow filter), σ₂ (broad filter), and minimum prominence threshold. The algorithm identifies local maxima in the DoG-filtered signal that exceed the prominence criterion.

**Threshold-based Detection**: Identifies events when intensity exceeds a threshold, using either manual thresholds or automatic Otsu's method [@Jumiawi2022] that analyzes the intensity distribution to establish an objective cutoff.

**Step Detection (Scisson-like)**: Under development; intended for analyzing step-like intensity changes using change-point detection methods from the Ruptures library.

### Automated Parameter Optimization

The "Auto-set Parameters" feature implements a data-driven workflow:

1. User draws multiple ROIs over representative active regions
2. Software calculates the mean intensity trace across all ROIs
3. Peak detection (via `scipy.signal.find_peaks`) identifies the most prominent peak
4. Peak width at half-maximum (FWHM) is converted to optimal σ₁ = FWHM / 2.355
5. Broader kernel set to σ₂ = 1.6 × σ₁ following Marr-Hildreth convention
6. Prominence threshold set to 25% of maximum peak prominence

All calculations are logged, ensuring full transparency and reproducibility.

### Post-Processing and Normalization

- **Temporal filtering**: Consolidates closely-spaced detections using a minimum separation parameter (e.g., 1-4 seconds), preventing double-counting of single biological events
- **Normalization**: Final event counts divided by video duration (seconds) and ROI area (µm²) to yield standardized rates for cross-experiment comparison

### Results Export
- Detailed CSV output with event timing, type, ROI ID, and normalized rates
- Metadata headers include analysis timestamp and parameters
- UTF-8-SIG encoding ensures proper rendering of special characters (µm)

## Quality Assurance

The software has been validated using publicly available microscopy datasets [@Hummer2017; @Hummer2020], demonstrating:

- **High specificity**: Background ROIs correctly identify zero events (no false positives)
- **Biological sensitivity**: High-K⁺ stimulation datasets show expected 2.5-3× increase in event rates compared to unstimulated conditions  
- **Objectivity**: Automated Otsu thresholding eliminates false positives that arise with manual thresholding
- **Parameter robustness**: Systematic variation of temporal filtering parameters (min_sep) shows expected and interpretable effects on event counts

# Example Usage

A typical workflow proceeds as follows:

1. **Launch application**: `transiscope` from command line
2. **Load data**: Click "Load File" and select `.avi` or `.tiff` file
3. **Set calibration**: Enter pixel size (e.g., 0.16 µm/pixel) for accurate area calculations
4. **Draw ROIs**: Select drawing mode and outline cellular regions of interest
5. **Optimize parameters**: Click "Auto-set Parameters" to derive optimal settings from ROI intensity traces
6. **Run analysis**: Click "Run Analysis" to detect events across all ROIs
7. **Review results**: Examine results table showing event timing and normalized rates
8. **Export**: Save results to CSV for statistical analysis or plotting

A comprehensive Jupyter notebook tutorial is included in the `examples/` directory, providing step-by-step guidance with sample data.

# Acknowledgements

We thank the authors of the publicly available microscopy datasets used for validation [@Hummer2017; @Hummer2020]. This work leverages the open-source scientific Python ecosystem, particularly Napari, NumPy, SciPy, and scikit-image. Development was conducted as an independent open-source initiative without dedicated institutional funding.

# References

