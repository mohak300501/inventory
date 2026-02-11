# Fire Extinguisher Predictive Maintenance Software

This project is a modern, interactive desktop application for managing and analyzing fire extinguisher maintenance and reliability. It features:
- A beautiful, responsive PyQt5 GUI
- Easy entry and management of fire extinguisher and failure data
- Predictive maintenance calculations and due date highlighting
- Bar and pie chart visualizations
- PDF export of extinguisher data (A4 landscape)
- Modern UI/UX with theming, tooltips, and accessibility
- Editable comboboxes for custom data entry

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