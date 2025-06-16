# BioImageSuiteLite - Architecture

This document provides a high-level overview of the software architecture for BioImageSuiteLite. It is intended for developers who wish to contribute to the project.

## Core Components

The application is divided into three logical layers:

1.  **User Interface Layer:** Built with `napari` and `PyQt5`. This layer is responsible for all visual elements, user interaction, and event handling.
2.  **Application Logic Layer:** Pure Python modules that handle the core scientific and data processing tasks.
3.  **External Libraries:** The underlying open-source libraries that provide the foundational tools for image processing, numerical analysis, and data handling.

## Architecture Diagram

The diagram below illustrates the relationships and data flow between the major components of the application.

```mermaid
graph TD
    subgraph UserInterface[User Interface Layer]
        NapariCore[Napari Viewer & Event Loop]
        GUI_Controls["BioImageSuiteLiteGUI Dock Widget (gui_manager.py)"]
        LogDisplayWidget["QTextEdit for Logs (in GUI_Controls)"]
        ROI_ShapesLayer[Napari Shapes Layer for ROIs]
    end

    subgraph ApplicationLogic[Application Logic Layer]
        IO_Module["IO Operations (io_operations.py)"]
        ROI_Module["ROI Handler (roi_handler.py)"]
        Analysis_Module["Analysis Processor (analysis_processor.py)"]
        Utils_Module["Utilities (utilities.py)"]
    end

    subgraph ExternalLibraries[External Libraries & Backend]
        OpenCV["OpenCV (cv2)"]
        Tifffile[Tifffile]
        ScikitImage[Scikit-Image]
        NumPy[NumPy]
        SciPy[SciPy]
        Shapely["Shapely (for ROI area)"]
        Ruptures["Ruptures (for Scisson-like)"]
        PythonLogging[Python Logging System]
    end

    %% UI Interactions
    NapariCore --> GUI_Controls{Manages/Displays};
    GUI_Controls -- Interacts with/Manages --> ROI_ShapesLayer;
    GUI_Controls -- Triggers Actions in --> IO_Module;
    GUI_Controls -- Triggers Actions in --> Analysis_Module;
    GUI_Controls -- Uses Config from --> ROI_Module;
    GUI_Controls -- Displays Image Data from --> NapariCore;  

    %% Logging Flow
    Utils_Module -- Configures --> PythonLogging;
    IO_Module -- Sends Logs to --> PythonLogging;
    Analysis_Module -- Sends Logs to --> PythonLogging;
    ROI_Module -- Sends Logs to --> PythonLogging;
    GUI_Controls -- Sends Logs to --> PythonLogging;
    PythonLogging -- "QtLogHandler (via GUI_Controls)" --> LogDisplayWidget;

    %% Application Logic Dependencies
    IO_Module -- Uses --> OpenCV;
    IO_Module -- Uses --> Tifffile;
    IO_Module -- Uses --> NumPy;

    ROI_Module -- Uses --> NumPy;
    ROI_Module -- Uses --> Shapely;

    Analysis_Module -- Uses --> NumPy;
    Analysis_Module -- Uses --> SciPy;
    Analysis_Module -- Uses --> ScikitImage;
    Analysis_Module -- Uses --> Ruptures;
    Analysis_Module -- Processes data from --> ROI_Module;
  

    %% Data Flow (Conceptual)
    IO_Module -- Provides Image Data & Metadata --> GUI_Controls;
    GUI_Controls -- Image Data Displayed in --> NapariCore;
    ROI_ShapesLayer -- Defines Regions on Image Data in --> NapariCore;
    ROI_ShapesLayer -- Vertex Data sent to --> ROI_Module;
    ROI_Module -- Provides ROI Masks & Intensity Traces to --> Analysis_Module;
    Analysis_Module -- Generates Event Data --> GUI_Controls;

    %% Style
    classDef ui fill:#D6EAF8,stroke:#5DADE2,stroke-width:2px;
    classDef appLogic fill:#D1F2EB,stroke:#48C9B0,stroke-width:2px;
    classDef extLib fill:#FCF3CF,stroke:#F7DC6F,stroke-width:2px;

    class UserInterface,NapariCore,GUI_Controls,LogDisplayWidget,ROI_ShapesLayer ui;
    class ApplicationLogic,IO_Module,ROI_Module,Analysis_Module,Utils_Module appLogic;
    class ExternalLibraries,OpenCV,Tifffile,ScikitImage,NumPy,SciPy,Shapely,Ruptures,PythonLogging extLib;
```

### Explanation of Layers

*   **User Interface Layer:**
    *   **Napari Viewer & Event Loop:** The core engine from Napari that handles image display, windowing, and the main event processing.
    *   **BioImageSuiteLiteGUI Dock Widget:** The custom Qt widget (`gui_manager.py`) containing all buttons, input fields, and results tables, which is docked into the Napari viewer.
    *   **Napari Shapes Layer for ROIs:** A specialized Napari layer used for drawing and managing Regions of Interest directly on the image.

*   **Application Logic Layer:** These are the core, non-visual Python modules.
    *   **IO Operations (`io_operations.py`):** Handles loading media files and data export.
    *   **ROI Handler (`roi_handler.py`):** Manages ROI data (vertices, masks, area calculations) and extracts intensity traces.
    *   **Analysis Processor (`analysis_processor.py`):** Contains the scientific algorithms for event detection (threshold, DoG, Scisson-like), filtering, and normalization.

*   **External Libraries & Backend:**
    *   These are the third-party libraries your application relies on for specific tasks like image reading, numerical operations, and scientific calculations. 