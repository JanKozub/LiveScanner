# Live Scanner Project

## Overview

This project is a simple screenshot software that implements a functionality of drawing on the screenshot by moving a pen in front of a camera.

## 1. app.py
This is the main application file that integrates all the services. It likely serves as the entry point of the project and manages the initialization and execution of the various services.

Key Components:

- Initialization of GUI utilities.
- Integration with the scanner service.
- Integration with the screenshot service.
- Main execution flow.

## 2. guiUtils.py
This file contains utility functions and classes related to GUI operations. These utilities are essential for interacting with the graphical user interface, providing necessary abstractions and helper functions.

Key Components:

- GUI component initialization.
- Event handling.
- Helper functions for GUI interactions.

## 3. scannerservice.py
This file implements the scanner service which is responsible for scanning operations. It includes functionalities for initiating scans, processing scanned data, and managing scanning-related tasks.

Key Components:

- Scanner initialization.
- Scan execution.
- Data processing from scans.
- Error handling for scanning operations.

## 4. screenshotService.py
This file provides functionalities to capture screenshots. It includes methods for taking screenshots, saving them, and potentially manipulating the captured images.

Key Components:

- Screenshot capture.
- Image saving.
- Image processing (if applicable).