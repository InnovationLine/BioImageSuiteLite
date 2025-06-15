# Screenshot Directory

This directory is for storing screenshots used in the example notebooks.

## Recommended Screenshots

For the comprehensive analysis guide, please add the following screenshots:

1. **load_file_button.png** - Shows the "Load File" button location in the File Operations section
2. **pixel_size_setting.png** - Shows where to set pixel size in the Preprocessing section
3. **roi_drawing.png** - Example of drawing ROIs around cells in the viewer
4. **auto_params.png** - Shows the "Auto-set Params from ROI" button and parameter fields
5. **run_analysis.png** - Shows the green "Run Full Analysis" button
6. **summary_plot.png** - Example summary plot showing event rates with error bars

## How to Add Screenshots

1. Take a screenshot of the relevant GUI section
2. Crop to show only the necessary parts
3. Save with the exact filename listed above in this directory
4. In the notebook, uncomment the image reference lines

## Tips for Good Screenshots

- Use consistent window size
- Highlight important buttons/areas with arrows or boxes if needed
- Keep file sizes reasonable (< 500KB per image)
- Use PNG format for best quality
- Show some sample data loaded when possible

## Example Directory Structure

```
examples/
├── comprehensive_analysis_guide.ipynb
├── usage_demo.ipynb
└── images/
    ├── README.md (this file)
    ├── load_file_button.png
    ├── pixel_size_setting.png
    ├── roi_drawing.png
    ├── auto_params.png
    ├── run_analysis.png
    └── summary_plot.png
``` 