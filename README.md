# README: Installation and Usage Guide for MediTrack

---

# **MediTrack: Patient Record Management Application**
MediTrack is a desktop application designed to efficiently manage patient records. It provides secure data storage, real-time updates, and features for exporting data in various formats. The application is ideal for healthcare professionals, clinics, and administrators.

---

## **Features**
- Add, update, and manage patient records seamlessly.
- Export data as PDF or Excel files with customizable paths.
- Automatic hourly backup of database files.
- Cross-platform compatibility for Windows and macOS.
- User-friendly interface with robust data management tools.

---

## **System Requirements**
### For Windows:
- OS: Windows 7 or later (64-bit recommended)
- Python 3.8 or later
- Required Libraries: Listed in `requirements.txt`

### For macOS:
- OS: macOS High Sierra (10.13) or later
- Python 3.8 or later
- Required Libraries: Listed in `requirements.txt`

---

## **Installation Guide**
### For Precompiled Executable:
#### Windows:
1. Download the latest MediTrack `.exe` file from the [release page](https://github.com/Asmodeus14/MediTrack/releases).
2. Double-click the downloaded file to run the application.

#### macOS:
1. Download the MediTrack `.app` bundle from the [release page](https://github.com/Asmodeus14/MediTrack/releases).
2. Move the `.app` file to the `/Applications` folder.
3. Double-click to launch MediTrack.

### For Source Code:
1. Clone the repository or download the source code.
   ```bash
   git clone https://github.com/Asmodeus14/MediTrack.git
   cd MediTrack
   ```

2. Install required dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application.
   ```bash
   python Base.py
   ```

---

## **Building the Executable**
If you want to create your own executable using **cx_Freeze**, follow these steps:

1. Ensure `cx_Freeze` is installed:
   ```bash
   pip install cx_Freeze
   ```

2. Modify the `setup.py` file if necessary for your platform.

3. Build the application:
   ```bash
   python setup.py build
   ```

4. The executable will be generated in the `build` folder.

---

## **Directory Structure**
- **Base.py**: Main application script.
- **README.md**: This installation guide.
- **LICENSE.txt**: Licensing information.
- **Logo.png**: Application logo.
- **Backup Folder**: Automatically created to store backups.
- **setup.py**: Build script for creating executables.

---

## **Usage Instructions**
1. Launch the application.
2. Use the **Add Patient** tab to input patient information.
3. View all patients in the **Patient List** section.
4. Use the **Export** buttons to save records as PDF or Excel files.
5. Backup files are automatically saved hourly in the `Backup` folder.

---

## **Support**
If you encounter issues, please contact:
- **Email**: singhabhay3145@gmail.com
- **GitHub Issues**: [Submit an Issue](https://github.com/Asmodeus14/MediTrack/issues/new)

Thank you for using MediTrack!

