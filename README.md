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

To create a standalone executable:

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
python build.py
```

The executable will be created in the `dist` folder as `GoodPDF.exe`

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
5. Build new executable

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 