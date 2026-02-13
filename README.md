# Inventory Management Software

This project is a modern, interactive desktop application for managing inventory. It features:
- A beautiful, responsive PyQt5 GUI
- Easy creation and management of daily inventory tables.
- Add new items and sites dynamically.
- Automatic calculation of totals.
- Data is saved in CSV format for easy access and portability.
- Export inventory tables to PDF.
- Modern UI/UX with theming, and accessibility.

## Usage

### Try a Compiled App
Check the `dist` directory for a pre-built executable for your operating system. Simply run the executable to launch the app.

> **Note:** To run the compiled executable, you must have `DRDO-logo.png`, `DRDO-logo.ico` and `style.qss` in the same folder as the executable.

### If No Compiled App Works
If you cannot run any of the provided executables, you can build your own:

1. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip3 install -r requirements.txt
   ```
2. **Build the app for your OS:**
   ```bash
   # For linux
   pyinstaller --onefile --windowed --icon=DRDO-logo.png inventory.py

   # For windows
   pyinstaller --onefile --windowed --icon=DRDO-logo.ico inventory.py
   ```
   The executable will be created in the `dist` directory.

3. **Run the app:**
   ```bash
   ./dist/fire  # or fire.exe on Windows
   ```
   > **Note:** Make sure `DRDO-logo.png`, `DRDO-logo.ico` and `style.qss` are in the same folder as the executable.

## Author
```
Author: Mohak Ketan Patil
GitHub: mohak300501
``` 