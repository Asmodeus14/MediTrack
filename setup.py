from cx_Freeze import setup, Executable
import sys

# Dependencies and included files
build_exe_options = {
    "zip_include_packages": [
        "tkinter", "sqlite3", "pandas", "os", "time", "fpdf", "datetime",
        "PyPDF2", "reportlab.pdfgen", "reportlab.lib.pagesizes", "io", "threading", "shutil"
    ],
    "include_files": ["Base.pdf", "Logo.png", "README.md", "LICENSE.txt","Logo.icns","requirements.txt"],
}

# Determine base for GUI applications
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Suppresses the console window for Windows GUI apps
elif sys.platform == "darwin":
    base = None  # For macOS, typically no base is required for GUI apps

# Define executables
executables = [
    Executable(
        script="App.py",
        base=base,
        icon="Logo.ico" if sys.platform == "win32" else "Logo.icns",  # Use .ico for Windows and .icns for macOS
        shortcut_name="MediTrack",
        target_name="MediTrack.exe" if sys.platform == "win32" else "MediTrack",
        shortcut_dir="StartMenuFolder" if sys.platform == "win32" else None,
    )
]

# Setup configuration
setup(
    name="MediTrack",
    version="0.1",
    description=(
        "A user-friendly desktop application for efficiently managing patient records. "
        "This system offers secure data storage, streamlined data entry, real-time updates, "
        "and robust backup functionality. Export patient information as PDF or Excel files "
        "with customizable file paths, ensuring seamless integration into healthcare workflows. "
        "Designed with a clean, intuitive interface, this application is ideal for clinics, "
        "practitioners, and healthcare administrators seeking a reliable and lightweight "
        "patient record management solution."
    ),
    options={"build_exe": build_exe_options},
    executables=executables,
)
