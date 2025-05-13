# Good PDF

A lightweight PDF viewer with built-in attachment support. View PDFs, extract attachments, and navigate pages with ease.

## Features

- 📄 **PDF Viewing**: Open and view PDF files with smooth navigation
- 📎 **Attachment Support**: View and extract PDF attachments (embedded files and annotations)
- 🔍 **Zoom Controls**: Adjust view with zoom in/out and fit-to-page options
- 📱 **Modern Interface**: Clean and intuitive PyQt6-based GUI
- 🚀 **Fast Performance**: Built with PyMuPDF for efficient PDF handling

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Building Executable

### Prerequisites
- Python 3.7+
- PyInstaller (included in requirements.txt)
- (Optional) UPX for smaller executable size

### Version Management
1. Open `version.py` and update the version number:
```python
VERSION = "1.0.0"  # Change this to your desired version
```
2. The version format should be: `MAJOR.MINOR.PATCH`
   - MAJOR: Big changes (e.g., 2.0.0)
   - MINOR: New features (e.g., 1.1.0)
   - PATCH: Bug fixes (e.g., 1.0.1)

### Build Steps
1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
python build.py
```

3. Find your executable:
- Location: `dist/GoodPDF-v{VERSION}.exe`
- Example: `dist/GoodPDF-v1.0.0.exe`

### Note
- The executable size is around 80MB (normal for PyQt6 applications)
- This is a single-file executable with all dependencies included
- No installation required - just run the .exe file

## Requirements

- Python 3.7+
- PyQt6
- PyMuPDF
- PyInstaller (for building executable)

## Usage

1. **Opening PDFs**:
   - Click "Open" or use File > Open
   - Navigate to your PDF file

2. **Viewing Attachments**:
   - Click "Attachments" to view embedded files
   - Select an attachment to extract or open

3. **Navigation**:
   - Use arrow buttons to move between pages
   - Enter page number to jump to specific page

4. **Zoom Controls**:
   - Use "+" and "-" buttons to zoom
   - Click "Fit" to fit page to window
   - Click "Fill" to fill window with page

## Development

To modify or enhance the application:

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Test thoroughly
5. Update version in `version.py`
6. Build new executable

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 