from TransiScope import io_operations
from TransiScope import utilities
import numpy as np
import os

logger = utilities.setup_logging()

# Create a dummy AVI for testing if needed (or use an existing one)
# --- (You might need to copy the create_dummy_avi function here or make it importable) ---
def create_dummy_avi(filename='data/manual_sample.avi', frames=10, width=32, height=32, fps=5):
    import cv2
    # ... (rest of the dummy AVI creation code from the notebook example) ...
    # Ensure 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    # ...
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    if not out.isOpened():
        print(f"Error: Could not open video writer for {filename}")
        return None
    for i in range(frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.circle(frame, (width//2, height//2), i+1, (0, (i*10)%255, 0), -1)
        out.write(frame)
    out.release()
    print(f"Created dummy AVI: {filename}")
    return filename

dummy_avi_path = create_dummy_avi()
# ---

if dummy_avi_path:
    print(f"Attempting to load: {dummy_avi_path}")
    frames, metadata = io_operations.load_avi(dummy_avi_path)

    if frames:
        print("AVI Loaded successfully!")
        print(f"Metadata: {metadata}")
        
        grey_stack = io_operations.convert_to_greyscale_stack(frames)
        if grey_stack is not None:
            print(f"Greyscale stack shape: {grey_stack.shape}")
            
            output_tiff_path = 'data/manual_output.tif'
            io_operations.save_to_multitiff(grey_stack, output_tiff_path, metadata)
            print(f"Saved to {output_tiff_path}")
        else:
            print("Failed to convert to greyscale.")
    else:
        print(f"Failed to load AVI: {dummy_avi_path}")
else:
    print("Failed to create dummy AVI for testing.")