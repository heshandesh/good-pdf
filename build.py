import PyInstaller.__main__
import os
from version import VERSION

# Create executable name with version
EXE_NAME = f"GoodPDF-v{VERSION}"

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Run PyInstaller
PyInstaller.__main__.run([
    'main.py',
    f'--name={EXE_NAME}',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--add-data=README.md;.',
    '--clean',
    '--noconfirm'
])

print(f"\nBuild complete! Executable created as: {EXE_NAME}.exe")
print("You can find it in the 'dist' folder.") 