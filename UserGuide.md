## Step-by-Step Guide for a General User (Using the GUI)

Here's a guide on how a general user would typically use the `TransiScope` GUI to analyze an AVI file, assuming all features are implemented and working.

**Objective:** Load a video file (AVI or multi-page TIFF) of cells, define regions of interest (ROIs) around cells, detect cellular events (e.g., fluorescence changes) within these ROIs over time, and get a normalized event rate.

---

**TransiScope: User Workflow Guide**

**Step 1: Launch the Application**

* Open your terminal or command prompt.
* Activate your Python virtual environment (if you used one for installation).
* Type `transiscope` and press Enter.
* The TransiScope window will open, integrated with the Napari viewer. You should see a "TransiScope Controls" panel docked, likely on the right.

**Step 2: Load Your Video File**

1. In the "TransiScope Controls" panel, under the "1. File Operations" section, click the **"Load File"** button.
2. A file dialog will appear. Navigate to the location of your video file (`.avi` or `.tif`/`.tiff`), select it, and click "Open".
3. **Observe:**
   * The main Napari viewer will display the first frame of your video, converted to greyscale. You can use the slider at the bottom (for the 'T' or time dimension) to scroll through the frames of your video.
   * The "File Info" label in the GUI panel will update with details about your loaded file (name, frame count, FPS, dimensions).
   * The "Activate ROI Drawing", "Clear All ROIs", and "Run Full Analysis" buttons should become enabled.

**Step 3: Set Pixel Size for Physical Unit Calculations**

1. Under the "2. Preprocessing & ROI" section, find the **"Pixel Size"** input field.
2. Enter the physical size of one pixel from your microscope's calibration (e.g., if 1 pixel = 0.16 micrometers, enter `0.160`). The unit is µm/pixel.
   * *This step is crucial for the final normalization to events/second/µm².*

**Step 4: Define Regions of Interest (ROIs) Around Cells**

1. Ensure your video is on a frame where the cells you want to analyze are clearly visible (use the time slider if needed).
2. In the "2. Preprocessing & ROI" section, select your preferred **ROI drawing mode** from the dropdown menu (Rectangle, Ellipse, Polygon, or Freehand Path).
3. **Draw an ROI:**
   * Simply **click and hold the left mouse button**, then drag to draw your region of interest around the cell.
   * Release the mouse button to complete the ROI.
   * The drawn ROI will appear overlaid on your image with a unique number (starting from 1).
   * Each ROI is automatically numbered sequentially (1, 2, 3, etc.) for easy identification on screen and later verification in results.
4. **Draw More ROIs:** 
   * Repeat step 3 for each additional cell you want to analyze.
   * Each new ROI will automatically receive the next sequential number.
5. **ROI Numbering:**
   * ROI numbers are displayed directly on the image viewer for easy reference.
   * These numbers correspond to the ROI IDs in your analysis results, making it simple to match results to specific regions.

**Step 5: (Optional) Manage ROIs**

* **Deleting an ROI:** Select an ROI by clicking on it, then press the `Delete` key to remove it. The remaining ROIs will retain their original numbers.
* **Clear All ROIs:** If you want to start over, click the **"Clear All ROIs"** button. This will remove all drawn ROIs and reset the numbering.

**Step 6: Set Analysis Parameters**

1. Navigate to the "3. Analysis Parameters" section in the GUI panel.
2. For each detection method you want to use, check the corresponding **"Enable..."** checkbox:
   * **Threshold Detection:**
     * If enabling, decide if you want to use a manual threshold or Otsu's automatic method.
     * If manual: Enter a "Threshold Value" (e.g., based on pixel intensity you consider an "event").
     * If Otsu: Check the "Use Otsu" checkbox.
   * **DoG Detection (Difference of Gaussians):**
     * If enabling, set "DoG Sigma 1" (smaller blur), "DoG Sigma 2" (larger blur), and "DoG Min Prominence" (how much a peak must stand out to be considered an event). These parameters tune the sensitivity to events of certain durations/strengths.
   * **Scisson-like Detection:**
     * If enabling, set the "Scisson Penalty" (or other relevant parameters for the specific algorithm). This parameter is often critical and requires careful tuning based on your data.
3. **Post-processing:**
   * Set the **"Min Event Separation"** (in seconds). This helps filter out duplicate detections of the same biological event that might occur very close in time.

**Step 7: Run the Analysis**

1. Once all parameters are set and ROIs are defined, click the large green **"Run Full Analysis"** button (likely at the bottom of the controls panel).
2. **Wait:** The analysis will now run on each ROI using the selected methods. This might take some time depending on the video size, number of ROIs, and complexity of the enabled analyses.
   * The "Log" display area should show progress messages and any warnings or errors encountered during the analysis.

**Step 8: Review Results**

1. After the analysis is complete, a notification will likely appear.
2. The **"Analysis Results" table** in the GUI panel will be populated. Each row typically represents a detected event:
   * **ROI ID:** Which cell the event belongs to.
   * **Type:** Which detection method found it (e.g., "threshold", "dog", "scisson").
   * **Start (s), End (s), Duration (s):** Timing of the event.
   * **Events/s/µm²:** The final normalized event rate for the ROI that this event belongs to. This value will be the same for all events from the same ROI.
   * **Details:** Specific properties of the event (e.g., peak value for DoG).
3. **Interpret:**
   * Examine the event list.
   * The **"Events/s/µm²"** column is the key quantitative output, allowing comparison across different cells or conditions.
   * You might see events from different detection methods. The "Min Event Separation" helps consolidate these if they refer to the same underlying biological event.

**Step 9: Export Results**

* Click the **"Export Results to CSV"** button to save the data from the results table to a CSV file for further statistical analysis or plotting in other software.
* Choose a location and filename for your results file.

**Troubleshooting/Tips for the User:**

* **Read the Log:** The "Log" display is your friend! It will show what the software is doing and any issues it encounters.
* **Parameter Tuning:** Event detection is highly dependent on parameters. You will likely need to experiment with different threshold values, DoG sigmas/prominence, and Scisson penalties to get meaningful results for  *your specific data* . Analyze a small, representative dataset first to optimize parameters.
* **Start Simple:** Try one detection method at a time to understand its behavior before enabling all of them.
* **ROI Quality:** Draw ROIs carefully to accurately delineate your cells. The area of the ROI directly affects the normalized event rate.
