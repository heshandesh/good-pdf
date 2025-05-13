import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([      
    'main.py',
    '--name=GoodPDF',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--add-data=README.md;.',
    '--clean',
    '--noconfirm',
]) 