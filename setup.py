from cx_Freeze import setup ,Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    
    "zip_include_packages": ["tkinter","sqlite3","pandas","os","time","fpdf","datetime","PyPDF2","reportlab.pdfgen","reportlab.lib.pagesizes","io","threading","shutil"],"include_files" :["Base.pdf","Logo.png","README.md","LICENSE.txt"]
}
import sys
base='Win32GUI' if sys.platform=='win32' else none
executable=[Executable(script="Base.py",base=base,icon="Logo.ico",shortcut_name="MediTrack",target_name="MediTrack.exe",shortcut_dir="StartMenuFolder")]
setup(
    name="MediTrack",
    version="0.1",
    description="A user-friendly desktop application for efficiently managing patient records. This system offers secure data storage, streamlined data entry, real-time updates, and robust backup functionality. Export patient information as PDF or Excel files with customizable file paths, ensuring seamless integration into healthcare workflows. Designed with a clean, intuitive interface, this application is ideal for clinics, practitioners, and healthcare administrators seeking a reliable and lightweight patient record management solution.",
    options={"build_exe": build_exe_options},
    executables=executable
    
)