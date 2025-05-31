import napari
# from typing import Optional, Dict, List, Any
from napari.layers import Image as NapariImageLayer, Shapes as NapariShapesLayer
from napari.utils.notifications import show_info, show_error, show_warning
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
                            QSpinBox, QDoubleSpinBox, QGroupBox, QFormLayout,
                            QCheckBox, QLineEdit, QScrollArea, QTableWidget, QTableWidgetItem,
                            QHeaderView, QSplitter, QTextEdit, QDialog)
from qtpy.QtCore import Qt
import numpy as np
from napari.layers.shapes.shapes import Mode as NapariShapesMode
import logging

# Matplotlib imports for plotting
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# We can use plt for simple plot configurations if needed, but direct Figure/Axes is often cleaner for embedding
# import matplotlib.pyplot as plt

from . import io_operations
from . import roi_handler
from . import analysis_processor
from . import utilities

# Setup logging for the GUI
logger = utilities.setup_logging() # Use the app-specific logger

class BioImageSuiteLiteGUI:
    def __init__(self, viewer: napari.Viewer):
        self.viewer = viewer
        self.viewer.title = "BioImageSuiteLite v0.1"
        
        # --- Internal State ---
        self.raw_frames: Optional[List[np.ndarray]] = None
        self.greyscale_stack: Optional[np.ndarray] = None # T, H, W
        self.current_image_layer: Optional[NapariImageLayer] = None
        self.shapes_layer: Optional[NapariShapesLayer] = None
        self.roi_manager: Optional[roi_handler.ROIManager] = None
        self.metadata: Dict[str, Any] = {}
        self.pixel_size_um: float = 1.0 # Default, user should set this
        self.all_detected_events: List[analysis_processor.Event] = []
        self.roi_summary_stats: Dict[Any, Dict[str, float]] = {} # For storing rate and SE per ROI


        # --- Main Widget ---
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setMinimumWidth(350) # Give some space for controls

        # Create a splitter for controls and results
        splitter = QSplitter(Qt.Vertical)

        # --- Controls Area (Scrollable) ---
        controls_scroll = QScrollArea()
        controls_scroll.setWidgetResizable(True)
        self.controls_widget = QWidget()
        controls_layout = QVBoxLayout(self.controls_widget)
        controls_scroll.setWidget(self.controls_widget)
        
        # == File Operations Group ==
        file_group = QGroupBox("1. File Operations")
        file_layout = QFormLayout(file_group)
        self.btn_load_avi = QPushButton("Load .avi File")
        self.btn_load_avi.clicked.connect(self._load_avi_action)
        self.lbl_file_info = QLabel("No file loaded.")
        self.lbl_file_info.setWordWrap(True)
        self.btn_save_tiff = QPushButton("Save as Multi-TIFF")
        self.btn_save_tiff.clicked.connect(self._save_tiff_action)
        self.btn_save_tiff.setEnabled(False)
        file_layout.addRow(self.btn_load_avi)
        file_layout.addRow(self.lbl_file_info)
        file_layout.addRow(self.btn_save_tiff)
        controls_layout.addWidget(file_group)

        # == Preprocessing Group ==
        preproc_group = QGroupBox("2. Preprocessing & ROI")
        preproc_layout = QFormLayout(preproc_group)
        self.pixel_size_input = QDoubleSpinBox()
        self.pixel_size_input.setSuffix(" µm/pixel")
        self.pixel_size_input.setDecimals(3)
        self.pixel_size_input.setMinimum(0.001)
        self.pixel_size_input.setMaximum(100.0)
        self.pixel_size_input.setValue(0.16) # Common example value
        self.pixel_size_input.valueChanged.connect(self._update_pixel_size)
        preproc_layout.addRow("Pixel Size:", self.pixel_size_input)
        
        self.btn_add_roi_mode = QPushButton("Activate ROI Drawing")
        self.btn_add_roi_mode.setCheckable(True)
        self.btn_add_roi_mode.clicked.connect(self._toggle_roi_drawing_mode)
        self.btn_add_roi_mode.setEnabled(False)
        preproc_layout.addRow(self.btn_add_roi_mode)
        
        self.btn_clear_rois = QPushButton("Clear All ROIs")
        self.btn_clear_rois.clicked.connect(self._clear_all_rois)
        self.btn_clear_rois.setEnabled(False)
        preproc_layout.addRow(self.btn_clear_rois)
        controls_layout.addWidget(preproc_group)

        # == Analysis Parameters Group ==
        analysis_group = QGroupBox("3. Analysis Parameters")
        analysis_form_layout = QFormLayout(analysis_group)

        # Thresholding
        self.cb_enable_threshold = QCheckBox("Enable Threshold Detection")
        self.threshold_value_input = QDoubleSpinBox()
        self.threshold_value_input.setRange(0, 65535) # Assuming up to 16-bit
        self.threshold_value_input.setValue(100)
        self.cb_use_otsu = QCheckBox("Use Otsu")
        self.cb_use_otsu.stateChanged.connect(lambda state: self.threshold_value_input.setEnabled(not state))
        analysis_form_layout.addRow(self.cb_enable_threshold)
        analysis_form_layout.addRow("Threshold Value:", self.threshold_value_input)
        analysis_form_layout.addRow(self.cb_use_otsu)

        # DoG
        self.cb_enable_dog = QCheckBox("Enable DoG Detection")
        self.dog_sigma1_input = QDoubleSpinBox()
        self.dog_sigma1_input.setRange(0.1, 100.0)
        self.dog_sigma1_input.setValue(1.0)
        self.dog_sigma1_input.setSingleStep(0.1)
        self.dog_sigma2_input = QDoubleSpinBox()
        self.dog_sigma2_input.setRange(0.2, 100.0)
        self.dog_sigma2_input.setValue(2.0)
        self.dog_sigma2_input.setSingleStep(0.1)
        self.dog_prominence_input = QDoubleSpinBox()
        self.dog_prominence_input.setRange(0.0, 1000.0)
        self.dog_prominence_input.setValue(5.0) # Needs tuning
        self.dog_prominence_input.setToolTip("Min prominence for DoG peaks. Set to 0 to use dynamic threshold.")
        analysis_form_layout.addRow(self.cb_enable_dog)
        analysis_form_layout.addRow("DoG Sigma 1:", self.dog_sigma1_input)
        analysis_form_layout.addRow("DoG Sigma 2:", self.dog_sigma2_input)
        analysis_form_layout.addRow("DoG Min Prominence:", self.dog_prominence_input)

        # Scisson-like (Stub)
        self.cb_enable_scisson = QCheckBox("Enable Scisson-like (Stub)")
        self.scisson_penalty_input = QDoubleSpinBox() # Example param
        self.scisson_penalty_input.setRange(0.1, 10000.0)
        self.scisson_penalty_input.setValue(10.0) # Needs heavy tuning
        self.scisson_penalty_input.setToolTip("Penalty for Scisson-like (e.g., Pelt). Highly sensitive.")
        analysis_form_layout.addRow(self.cb_enable_scisson)
        analysis_form_layout.addRow("Scisson Penalty (approx):", self.scisson_penalty_input)

        # Post-processing
        self.min_event_separation_input = QDoubleSpinBox()
        self.min_event_separation_input.setSuffix(" s")
        self.min_event_separation_input.setRange(0.0, 60.0)
        self.min_event_separation_input.setValue(0.5)
        analysis_form_layout.addRow("Min Event Separation:", self.min_event_separation_input)
        
        controls_layout.addWidget(analysis_group)

        # == Run Analysis Button ==
        self.btn_run_analysis = QPushButton("Run Full Analysis")
        self.btn_run_analysis.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 6px; }")
        self.btn_run_analysis.clicked.connect(self._run_full_analysis)
        self.btn_run_analysis.setEnabled(False)
        controls_layout.addWidget(self.btn_run_analysis)

        self.btn_show_summary_plot = QPushButton("Show Summary Plot")
        self.btn_show_summary_plot.clicked.connect(self._show_summary_plot_action)
        self.btn_show_summary_plot.setEnabled(False) # Disabled until analysis results are available
        controls_layout.addWidget(self.btn_show_summary_plot)

        controls_layout.addStretch() # Pushes buttons to bottom of its section
        # If you wanted the run analysis button at the very bottom, move addStretch above it
        # and then add the summary plot button. For now, placing both before stretch.

        splitter.addWidget(controls_scroll) # Add controls area to splitter

        # --- Results Area ---
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)
        results_widget.setMinimumHeight(200) # Ensure results area is visible

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(7) # ROI ID, Event Type, Start (s), End (s), Duration (s), Norm. Rate, Props
        self.results_table.setHorizontalHeaderLabels(["ROI ID", "Type", "Start (s)", "End (s)", "Duration (s)", "Events/s/µm²", "Details"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers) # Read-only
        results_layout.addWidget(QLabel("Analysis Results:"))
        results_layout.addWidget(self.results_table)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        results_layout.addWidget(QLabel("Log:"))
        results_layout.addWidget(self.log_display)
        # Custom log handler to pipe logs to QTextEdit
        self.log_handler = QtLogHandler(self.log_display)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(self.log_handler) # Add to root logger
        logging.getLogger().setLevel(logging.INFO) # Ensure root logger level is appropriate


        splitter.addWidget(results_widget) # Add results area to splitter
        splitter.setSizes([int(self.viewer.window.qt_viewer.height() * 0.6), int(self.viewer.window.qt_viewer.height() * 0.4)]) # Initial sizes

        self.main_layout.addWidget(splitter)
        self.viewer.window.add_dock_widget(self.main_widget, name="BioImageSuiteLite Controls", area='right')
        
        self._update_pixel_size() # Initialize pixel size

    def _update_pixel_size(self):
        self.pixel_size_um = self.pixel_size_input.value()
        show_info(f"Pixel size set to {self.pixel_size_um:.3f} µm/pixel.")
        # If ROIs exist, their physical area might need recalculation
        if self.roi_manager:
            for roi_obj in self.roi_manager.get_all_rois():
                roi_obj.set_area_physical(self.pixel_size_um)


    def _load_avi_action(self):
        file_path, _ = QFileDialog.getOpenFileName(self.main_widget, "Open AVI File", "", "AVI Files (*.avi)")
        if not file_path:
            return

        self.raw_frames, self.metadata = io_operations.load_avi(file_path)

        if self.raw_frames and self.metadata:
            self.lbl_file_info.setText(
                f"Loaded: {file_path.split('/')[-1]}\n"
                f"Frames: {self.metadata['frame_count']}, "
                f"FPS: {self.metadata['fps']:.2f}, "
                f"Size: {self.metadata['height']}x{self.metadata['width']}"
            )
            
            # Convert to greyscale immediately for display and analysis
            self.greyscale_stack = io_operations.convert_to_greyscale_stack(self.raw_frames)
            if self.greyscale_stack is None:
                show_error("Failed to convert AVI to greyscale stack.")
                self.btn_save_tiff.setEnabled(False)
                self.btn_add_roi_mode.setEnabled(False)
                self.btn_run_analysis.setEnabled(False)
                return

            # Clear previous layers
            if self.current_image_layer and self.current_image_layer in self.viewer.layers:
                self.viewer.layers.remove(self.current_image_layer)
            if self.shapes_layer and self.shapes_layer in self.viewer.layers:
                self.viewer.layers.remove(self.shapes_layer)
            
            self.current_image_layer = self.viewer.add_image(
                self.greyscale_stack,
                name=f"Greyscale_{file_path.split('/')[-1]}",
                metadata=self.metadata
            )
            self.viewer.dims.current_step = (0,0,0) # Show first frame
            self.viewer.reset_view()

            # Initialize ROI Manager with correct image shape (T, H, W)
            self.roi_manager = roi_handler.ROIManager(self.greyscale_stack.shape)
            self._setup_shapes_layer()

            self.btn_save_tiff.setEnabled(True)
            self.btn_add_roi_mode.setEnabled(True)
            self.btn_clear_rois.setEnabled(True)
            self.btn_run_analysis.setEnabled(True) # Enable once image is loaded
            show_info("AVI loaded and converted to greyscale.")
        else:
            show_error(f"Failed to load AVI: {file_path}")
            self.lbl_file_info.setText("Failed to load AVI.")
            self.btn_save_tiff.setEnabled(False)
            self.btn_add_roi_mode.setEnabled(False)
            self.btn_run_analysis.setEnabled(False)

    def _save_tiff_action(self):
        if self.greyscale_stack is None:
            show_warning("No greyscale image data to save.")
            return

        output_path, _ = QFileDialog.getSaveFileName(self.main_widget, "Save Multi-Page TIFF", "", "TIFF Files (*.tif *.tiff)")
        if not output_path:
            return

        success = io_operations.save_to_multitiff(self.greyscale_stack, output_path, self.metadata)
        if success:
            show_info(f"Greyscale stack saved to {output_path}")
        else:
            show_error(f"Failed to save TIFF to {output_path}")

    def _setup_shapes_layer(self):
        if self.shapes_layer and self.shapes_layer in self.viewer.layers:
            self.viewer.layers.remove(self.shapes_layer)
        
        self.shapes_layer = self.viewer.add_shapes(
            name='ROIs',
            ndim=self.greyscale_stack.ndim -1, # ROIs are 2D on each T-slice
            face_color='transparent',
            edge_color='red',
            edge_width=2
        )
        self.shapes_layer.mode = 'add_polygon' # Default mode
        # Connect event for when new shape is drawn
        self.shapes_layer.events.data.connect(self._on_roi_added_or_changed)
        self.shapes_layer.mouse_drag_callbacks.append(self._on_roi_interaction)
        # Could connect to self.shapes_layer.events.set_data for changes too
        self.btn_add_roi_mode.setChecked(False) # Reset button
        self._toggle_roi_drawing_mode() # To set initial mode based on unchecked

    def _on_roi_interaction(self, layer, event):
        # This callback is triggered during drag, useful for live updates or vertex move detection
        # For simplicity, we rely on the 'data' event for when a shape is finalized or selected and modified.
        # Check if a shape is selected and being modified
        if layer.mode in ['direct', 'select', 'vertex_insert', 'vertex_remove'] and len(layer.selected_data) > 0:
            # This is tricky as data event might not fire until modification is complete.
            # Napari's event model for shapes is complex.
            # For now, we rely on the `data` event which fires after most changes.
            pass
        yield # Let napari handle the event

    def _on_roi_added_or_changed(self, event):
        """Callback when shapes data changes (add, remove, modify)."""
        if not self.roi_manager or not self.shapes_layer:
            logger.debug("ROI manager or shapes layer not ready.")
            return       

        raw_action = getattr(event, 'action', None)
        # Convert the action to a lowercase string. If it's an enum, str() will often give 'Enum.MEMBER'.
        # If it's already a string, it will just be a string.
        action_str = ''
        if raw_action is not None:
            action_str = str(raw_action).lower()
            if '.' in action_str: # Handles cases like 'ActionType.ADDED' -> 'added'
                action_str = action_str.split('.')[-1]

        logger.debug(f"Shapes layer data event: raw_action='{raw_action}', processed_action_str='{action_str}', current_mode='{self.shapes_layer.mode}'")


        # Use lowercase string for comparison
        if action_str == 'added': # Napari often uses 'added' or 'add'
            added_indices = getattr(event, 'data_indices', tuple())
            if not added_indices:
                logger.debug("Action 'added', but no data_indices in event.")
                return

            current_shapes_data = getattr(event, 'value', self.shapes_layer.data) # Get the most recent data

            for new_shape_idx in added_indices:
                if new_shape_idx == -1: 
                    new_shape_idx = len(current_shapes_data) - 1

                if not (0 <= new_shape_idx < len(current_shapes_data)):
                    logger.warning(f"Invalid new_shape_idx {new_shape_idx} from event.")
                    continue

                new_shape_data = current_shapes_data[new_shape_idx]
                logger.debug(f"Processing 'added' shape at index {new_shape_idx}, data: {new_shape_data}")

                if len(new_shape_data) < 3:
                    show_warning(f"Shape at index {new_shape_idx} is too small (<3 vertices). Not added to ROIManager. User can delete manually from Napari.")
                    continue 

                vertices_for_roi = new_shape_data

                already_managed = False
                for existing_roi in self.roi_manager.get_all_rois():
                    if existing_roi.vertices.shape == vertices_for_roi.shape and \
                       np.array_equal(existing_roi.vertices, vertices_for_roi):
                        logger.debug(f"Shape at index {new_shape_idx} already managed. Skipping.")
                        already_managed = True
                        break
                if already_managed:
                    continue

                added_roi = self.roi_manager.add_roi(vertices_for_roi)
                if added_roi:
                    added_roi.set_area_physical(self.pixel_size_um)
                    show_info(f"ROI {added_roi.id} added (Area: {added_roi.area_pixels:.1f} px, {added_roi.area_sq_um or 0:.2f} µm²).")

                    # Property update attempt (simplified, may need more robust handling)
                    try:
                        props = self.shapes_layer.properties
                        new_prop_entry = {'roi_manager_id': added_roi.id, 'name': f'ROI_{added_roi.id}'}
                        if isinstance(props, dict): # Properties as dict of lists
                            for key, value_list in new_prop_entry.items():
                                if key not in props:
                                    props[key] = [None] * len(current_shapes_data)
                                elif len(props[key]) < len(current_shapes_data): # Pad if necessary
                                    props[key].extend([None] * (len(current_shapes_data) - len(props[key])))
                                props[key][new_shape_idx] = value_list # Assuming value_list is not a list here but the value itself
                            self.shapes_layer.properties = props
                        elif isinstance(props, list): # Properties as list of dicts
                            if new_shape_idx < len(props):
                                props[new_shape_idx].update(new_prop_entry)
                            elif new_shape_idx == len(props):
                                props.append(new_prop_entry)
                            self.shapes_layer.properties = props
                        self.shapes_layer.refresh_colors()
                    except Exception as e_prop:
                        logger.warning(f"Could not update Napari shape properties: {e_prop}")
                else:
                    show_warning(f"ROIManager failed to add shape from index {new_shape_idx}. Shape remains in Napari.")

        elif action_str == 'removed': # Napari often uses 'removed' or 'remove'
            removed_indices = getattr(event, 'data_indices', tuple())
            logger.info(f"Napari shapes removed at indices: {removed_indices}. ROIManager not auto-updated in this version.")
            # Implement removal from self.roi_manager if you have a robust way to map napari indices/IDs to your ROI IDs

        elif action_str == 'changed': # Napari often uses 'changed' or 'changing'
            changed_indices = getattr(event, 'data_indices', tuple())
            logger.info(f"Napari shapes changed at indices: {changed_indices}. ROIManager not auto-updated in this version.")
            # Implement update logic in self.roi_manager (e.g., re-calculate area, intensity trace if vertices changed)


    def _toggle_roi_drawing_mode(self):
        if not self.shapes_layer:
            self.btn_add_roi_mode.setChecked(False)
            return

        if self.btn_add_roi_mode.isChecked():
            # Before changing mode, ensure any active drawing is finalized or cancelled.
            # Napari's _finish_drawing is usually called on double-click or mode change.
            # If the layer is in an inconsistent state, changing mode can be problematic.
            # The previous fix to _on_roi_added_or_changed should prevent that state.
            
            logger.debug("Activating ROI drawing mode (add_polygon).")
            self.shapes_layer.mode = NapariShapesMode.ADD_POLYGON
            self.btn_add_roi_mode.setText("Finish ROI Drawing")            
            show_info("ROI drawing mode: ON. Draw polygons. Double-click or Esc to finish a polygon.")
            # Set default properties for the next shape to be drawn (if you want to link)
            # self.shapes_layer.current_properties = {'internal_id': self.roi_manager.next_roi_id}
        else:
            logger.debug("Deactivating ROI drawing mode (select).")
            # If currently drawing a shape, changing mode will typically finalize or discard it.
            # Napari handles this by calling _finish_drawing internally.
            # If _finish_drawing had issues before, this could also show them.            
            self.shapes_layer.mode = NapariShapesMode.SELECT
            self.btn_add_roi_mode.setText("Activate ROI Drawing")
            show_info("ROI drawing mode: OFF. Shapes layer in select mode.")

    def _clear_all_rois(self):
        if self.shapes_layer:
            self.shapes_layer.data = [] # Clear from napari
            self.shapes_layer.refresh()
        if self.roi_manager:
            self.roi_manager.rois = {} # Clear from our manager
            self.roi_manager.next_roi_id = 1
        show_info("All ROIs cleared.")
        if self.btn_add_roi_mode.isChecked(): # If it was in drawing mode
            self._toggle_roi_drawing_mode() # Toggle to turn it off and update text


    def _run_full_analysis(self):
        if self.greyscale_stack is None or self.roi_manager is None or not self.roi_manager.get_all_rois():
            show_warning("Please load data and define at least one ROI before running analysis.")
            self.btn_show_summary_plot.setEnabled(False) # Ensure plot button is disabled
            return
        
        if self.metadata['fps'] <= 0:
            show_error("FPS is zero or invalid. Cannot perform time-based analysis.")
            self.btn_show_summary_plot.setEnabled(False) # Ensure plot button is disabled
            return

        logger.info("--- Starting Full Analysis ---")
        self.results_table.setRowCount(0) # Clear previous results
        self.all_detected_events = []
        self.roi_summary_stats.clear() # Clear previous summary stats
        self.btn_show_summary_plot.setEnabled(False) # Disable during analysis
        
        fps = self.metadata['fps']
        total_frames = self.greyscale_stack.shape[0]
        observation_duration_seconds = total_frames / fps

        rois_to_analyze = self.roi_manager.get_all_rois()

        for roi_obj in rois_to_analyze:
            logger.info(f"Analyzing ROI ID: {roi_obj.id}, Area: {roi_obj.area_pixels:.1f} px, {roi_obj.area_sq_um or 0:.2f} µm²")
            if roi_obj.area_sq_um is None or roi_obj.area_sq_um <= 0:
                logger.warning(f"ROI {roi_obj.id} has zero or uncalculated physical area. Skipping normalization for this ROI.")
                # Continue to detection, but normalization will be 0 or NaN
            
            intensity_trace = roi_obj.get_mean_intensity_trace(self.greyscale_stack)
            if intensity_trace is None:
                logger.error(f"Could not get intensity trace for ROI {roi_obj.id}. Skipping analysis for this ROI.")
                continue

            roi_events: List[analysis_processor.Event] = []
            # 1. Threshold Detection
            if self.cb_enable_threshold.isChecked():
                thresh_val = self.threshold_value_input.value() if not self.cb_use_otsu.isChecked() else None
                use_otsu_flag = self.cb_use_otsu.isChecked()
                try:
                    ev = analysis_processor.detect_events_threshold(
                        intensity_trace, fps, roi_obj.id,
                        threshold_value=thresh_val, use_otsu=use_otsu_flag
                    )
                    roi_events.extend(ev)
                except Exception as e:
                    logger.error(f"Error in threshold detection for ROI {roi_obj.id}: {e}")


            # 2. DoG Detection
            if self.cb_enable_dog.isChecked():
                s1 = self.dog_sigma1_input.value()
                s2 = self.dog_sigma2_input.value()
                prom = self.dog_prominence_input.value()
                min_prom = prom if prom > 0 else None # Use None if 0 to trigger dynamic threshold
                try:
                    ev = analysis_processor.detect_events_dog(
                        intensity_trace, fps, roi_obj.id,
                        sigma1=s1, sigma2=s2, min_prominence=min_prom
                    )
                    roi_events.extend(ev)
                except Exception as e:
                    logger.error(f"Error in DoG detection for ROI {roi_obj.id}: {e}")
            
            # 3. Scisson-like Detection (Stub)
            if self.cb_enable_scisson.isChecked():
                # This is a stub, replace with actual implementation
                penalty = self.scisson_penalty_input.value()
                try:
                    ev = analysis_processor.detect_events_scisson_like_stub(
                        intensity_trace, fps, roi_obj.id, penalty_value=penalty
                    ) # Add params
                    roi_events.extend(ev)
                except Exception as e:
                    logger.error(f"Error in Scisson-like detection for ROI {roi_obj.id}: {e}")

            # 4. Filter Duplicates for this ROI
            min_sep = self.min_event_separation_input.value()
            filtered_roi_events = analysis_processor.filter_duplicate_events(roi_events, min_sep)
            self.all_detected_events.extend(filtered_roi_events)

            # 5. Normalize and Display Results for this ROI
            num_filtered_events_roi = len(filtered_roi_events)
            
            normalized_rate = 0.0
            se_rate = 0.0 # Standard Error of the rate

            if roi_obj.area_sq_um and roi_obj.area_sq_um > 0 and observation_duration_seconds > 0:
                 normalized_rate = analysis_processor.normalize_event_rate(
                    num_filtered_events_roi,
                    observation_duration_seconds,
                    roi_obj.area_sq_um
                )
                 if num_filtered_events_roi > 0:
                    se_rate = np.sqrt(num_filtered_events_roi) / (observation_duration_seconds * roi_obj.area_sq_um)
            else:
                logger.warning(f"ROI {roi_obj.id}: Cannot normalize rate or calculate SE due to zero/invalid area ({roi_obj.area_sq_um} µm²) or duration.")

            self.roi_summary_stats[roi_obj.id] = {'rate': normalized_rate, 'se': se_rate}

            logger.info(f"ROI {roi_obj.id}: Total detected (raw) = {len(roi_events)}, Filtered = {num_filtered_events_roi}, Norm. Rate = {normalized_rate:.4e} ± {se_rate:.2e}")

            for event_obj in filtered_roi_events:
                row_pos = self.results_table.rowCount()
                self.results_table.insertRow(row_pos)
                self.results_table.setItem(row_pos, 0, QTableWidgetItem(str(event_obj.roi_id)))
                self.results_table.setItem(row_pos, 1, QTableWidgetItem(event_obj.event_type))
                self.results_table.setItem(row_pos, 2, QTableWidgetItem(f"{event_obj.start_time:.2f}"))
                self.results_table.setItem(row_pos, 3, QTableWidgetItem(f"{event_obj.end_time:.2f}"))
                self.results_table.setItem(row_pos, 4, QTableWidgetItem(f"{event_obj.duration:.2f}"))
                self.results_table.setItem(row_pos, 5, QTableWidgetItem(f"{normalized_rate:.3e}"))
                
                prop_str = ", ".join([f"{k}:{v:.2f}" if isinstance(v, float) else f"{k}:{v}" for k,v in event_obj.properties.items()])
                self.results_table.setItem(row_pos, 6, QTableWidgetItem(prop_str))
        
        if not self.all_detected_events:
            show_info("Analysis complete. No events found with current settings.")
            self.btn_show_summary_plot.setEnabled(False)
        else:
            show_info(f"Analysis complete. Total {len(self.all_detected_events)} unique events found across all ROIs.")
            self.btn_show_summary_plot.setEnabled(True) # Enable if events were found
        logger.info("--- Full Analysis Finished ---")

    def _show_summary_plot_action(self):
        if not self.all_detected_events:
            show_warning("No analysis results available to plot. Please run analysis first.")
            return
        
        if not self.roi_summary_stats:
            show_warning("ROI summary statistics are not available. Please re-run analysis.")
            return

        logger.info("Generating summary plot with standard errors...")

        # Extract data for plotting from self.roi_summary_stats
        roi_ids_sorted = sorted(self.roi_summary_stats.keys(), key=lambda x: int(x) if isinstance(x, int) or x.isdigit() else str(x))
        rates_sorted = [self.roi_summary_stats[rid]['rate'] for rid in roi_ids_sorted]
        se_sorted = [self.roi_summary_stats[rid]['se'] for rid in roi_ids_sorted]

        # Create a new dialog to host the plot
        plot_dialog = QDialog(self.main_widget) # Parent to the main widget
        plot_dialog.setWindowTitle("ROI Analysis Summary Plot (Rate ± SE)")
        plot_dialog.setMinimumSize(700, 500) # Adjusted size for better SE display
        dialog_layout = QVBoxLayout(plot_dialog)

        # Matplotlib Figure and Canvas
        fig = Figure(figsize=(8, 6), dpi=100) # Adjusted figure size
        ax = fig.add_subplot(111)

        bar_positions = np.arange(len(roi_ids_sorted))
        bars = ax.bar(bar_positions, rates_sorted, yerr=se_sorted, 
                        align='center', alpha=0.7, capsize=5, # capsize for error bar caps
                        error_kw={'ecolor': 'black', 'elinewidth':1.5})

        ax.set_xticks(bar_positions)
        ax.set_xticklabels([str(rid) for rid in roi_ids_sorted]) # Ensure ROI IDs are strings for labels
        ax.set_xlabel("ROI ID")
        ax.set_ylabel("Normalized Event Rate (Events/s/µm²)")
        ax.set_title("Summary of Normalized Event Rates per ROI (± Standard Error)")
        ax.yaxis.grid(True, linestyle='--', alpha=0.7) # Add horizontal grid for better readability
        fig.tight_layout()

        # Add text labels on top of each bar (Rate ± SE)
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            se_val = se_sorted[i]
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + se_val * 0.1, # Position text slightly above error bar
                      f'{yval:.2e} \n± {se_val:.1e}', va='bottom', ha='center', fontsize=8) # Smaller font for two lines

        canvas = FigureCanvas(fig)
        dialog_layout.addWidget(canvas)

        close_button = QPushButton("Close")
        close_button.clicked.connect(plot_dialog.accept)
        dialog_layout.addWidget(close_button)

        plot_dialog.setLayout(dialog_layout)
        plot_dialog.exec_()

        logger.info("Summary plot with standard errors displayed.")


# For piping logs to QTextEdit
class QtLogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.widget = text_widget
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)        
        self.widget.append(msg)
        self.widget.verticalScrollBar().setValue(self.widget.verticalScrollBar().maximum()) # Auto-scroll


def main():
    """Main function to launch the Napari viewer with the plugin."""
    utilities.setup_logging(level=logging.INFO) # Ensure logging is set up at least once globally
    try:
        viewer = napari.Viewer()
        gui = BioImageSuiteLiteGUI(viewer) # The GUI class will add its widget
        napari.run()
    except Exception as e:
        # This is a last resort catch for critical startup errors.
        # Individual operations should have their own error handling.
        logger.critical(f"Critical error launching BioImageSuiteLite: {e}", exc_info=True)
        # Optionally show a system-level error dialog if possible outside Napari context
        # from qtpy.QtWidgets import QMessageBox
        # app = napari.qt.get_app() # Get or create a QApplication
        # if app: # Check if QApplication exists
        #    QMessageBox.critical(None, "Application Error", f"A critical error occurred: {e}")


if __name__ == '__main__':
    # This allows running the GUI directly for development,
    # but `bioimagesuitelite` script is preferred after installation.
    main()