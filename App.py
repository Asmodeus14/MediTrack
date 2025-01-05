"""
MediTrack - Patient Management System
=====================================

Description:
------------
MediTrack is a user-friendly desktop application designed to manage patient information efficiently. 
This system offers features such as secure data storage, real-time updates, streamlined data entry, 
and robust backup functionality. Users can export patient records in PDF or Excel formats, 
providing a seamless solution for healthcare workflows.

Features:
---------
- Add, view, and manage patient records with ease.
- Export data to PDF and Excel formats.
- Real-time search and highlighting for patient records.
- Automated database backups to ensure data security.
- Printing support for individual or all patient records.

Usage:
------
Run this script to launch the application. Ensure that the required dependencies are installed. 
The application GUI is intuitive and designed for both novice and advanced users.

License:
--------
This software is provided "AS IS" under the terms of the LICENSE.txt file included in this project.

Dependencies:
-------------
- tkinter: GUI framework for Python
- sqlite3: Lightweight database management
- pandas: Data manipulation and analysis
- fpdf: PDF generation
- PyPDF2: PDF reading and writing
- reportlab: Advanced PDF generation

Author:
-------
Abhay Singh
"""



import tkinter as tk
from tkinter import ttk, messagebox,PhotoImage
import sqlite3
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import time
import shutil
import threading

# Database Setup
def initialize_database():
    conn = sqlite3.connect("patient_app.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        contact TEXT,
        Address TEXT,
        Date TEXT
        )
    """)

def backup_database():
    backup_folder="Backup"
    while True:
        # Ensure the folder exists
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)  # Create the folder if it doesn't exist
            
            
        backup_file = os.path.join(backup_folder, "patients_backup.db")
        try:
            shutil.copy("patients.db", backup_file)
            
        except Exception as e:
            continue
            
        time.sleep(3600) 



# Add Patient
def add_patient(event):
    name = entry_name.get()
    age = entry_age.get()
    gender = combo_gender.get()
    contact = entry_contact.get()
    Address = text_Address.get("1.0", tk.END)
    
    
    date = datetime.now().strftime("%d-%m-%Y--%H:%M:%S")
    
    if not name:
        messagebox.showerror("Input Error", "Patient name is required!")
        return
    conn = sqlite3.connect("patient_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, age, gender, contact,Date,Address ) VALUES (?, ?, ?, ?, ?, ?)",(name, age, gender, contact, Address, date ))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Patient added successfully!")
    clear_patient_form()
    load_patients()

# Clear Patient Form
def clear_patient_form():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    combo_gender.set("")
    entry_contact.delete(0, tk.END)
    text_Address.delete("1.0", tk.END)


    
    
  

# Load Patients
def load_patients():
    tree_patients.delete(*tree_patients.get_children())
    conn = sqlite3.connect("patient_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, gender, contact ,Address,Date  FROM patients")
    for row in cursor.fetchall():
        tree_patients.insert("", tk.END, values=row)
    conn.close()

# Export to PDF
def export_to_pdf():
    save_folder="PDF"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    conn = sqlite3.connect("patient_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    
    if not patients:
        messagebox.showinfo("No Data", "No patient data to export!")
        return
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Patient Database", ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="ID | Name | Age | Gender | Contact | Address | Date-Time", ln=True)
    for patient in patients:
        pdf.cell(200, 10, txt=f"{patient[0]} | {patient[1]} | {patient[2]} | {patient[3]} | {patient[4]} | {patient[5]} |{patient[6]}", ln=True)
    
    save_path = os.path.join(save_folder,"Paitent_database.pdf")
    if save_path:
        pdf.output(save_path)
        messagebox.showinfo("Success", f"PDF saved to {save_path}")



# Export to Excel
def export_to_excel():
    conn = sqlite3.connect("patient_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    save_folder="Excel"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        
    if not patients:
        messagebox.showinfo("No Data", "No patient data to export!")
        return
    
    save_path = os.path.join(save_folder,"Patient_data.xlsx")
    if save_path:
        df = pd.DataFrame(patients, columns=["ID", "Name", "Age", "Gender", "Contact", "Address","Date"])
        df.to_excel(save_path, index=False)
        messagebox.showinfo("Success", f"Excel file saved to {save_path}")

# Print Data
def print_data():
    answer =messagebox.askokcancel("Print Confirmation","This will print the whole sheet")
    if answer is True:
        conn = sqlite3.connect("patient_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        conn.close()
        
        
        
        if not patients:
            messagebox.showinfo("No Data", "No patient data to print!")
            return
        
        with open("temp_print.txt", "w") as file:
            for patient in patients:
                file.write(f"ID:{patient[0]}\n  Name: {patient[1]}        Age: {patient[2]}-{patient[3]}\n  Contact: {patient[4]}{" "*6}Date: {patient[6]}\n  Address: {patient[5]} ")
        
        os.system("notepad /p temp_print.txt")
        os.remove("temp_print.txt")
    else:
        messagebox.showwarning("Print Confirmation","Process was interrupted")
        
# Print specific Data Print
    
def Specific_data_print(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No patient selected.")
        return

    text = tree.item(selected_item, "values")
    
    output_pdf_path=f"{text[1]}.pdf"
    
    reader = PdfReader("Base.pdf")
    writer = PdfWriter()

    
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(165, 620, "Patient Name:")
    c.setFont("Helvetica", 12)
    c.drawString(250, 620,text[1])
    c.setFont("Helvetica-Bold", 12)
    c.drawString(320, 620, "Age:")
    c.setFont("Helvetica", 12)
    c.drawString(350, 620, text[2])
    c.setFont("Helvetica-Bold", 12)
    c.drawString(370, 620, "Sex:")
    c.setFont("Helvetica", 12)
    c.drawString(400, 620, text[3])
    c.setFont("Helvetica-Bold",12)
    c.drawString(450,620,"Contact:")
    c.setFont("Helvetica",12)
    c.drawString(500,620,text[4])
    c.setFont("Helvetica-Bold", 12)
    c.drawString(440, 640, "Date:")
    c.setFont("Helvetica", 12)
    c.drawString(470, 640, text[6])
    c.drawString(165,600,"Address:")
    c.setFont("Helvetica",12)
    Address=text[5]
    c.drawString(220,600,Address.replace("\n","")) 
    c.save()

    
    packet.seek(0)
    new_pdf = PdfReader(packet)

    
    for i, page in enumerate(reader.pages):
        if i == 0:
            page.merge_page(new_pdf.pages[0])  
        writer.add_page(page)

    
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)
    
    time.sleep(2)
    os.startfile(f"{text[1]}.pdf")
    time.sleep(5)
    os.remove(f"{text[1]}.pdf")
    
    
   
   
    
# Search patients
def search_patients(search_entry, tree):
    
    query = search_entry.get().lower()
    state=False  
    for item in tree.get_children():
        if query =="":
            break
        
        tree.item(item, tags=())  

        
        values = tree.item(item, "values")
        
        
        if query in values[0].lower() or query in values[1].lower():  
            tree.item(item, tags=("highlight",))
            state=True
            
    
    if state is True:
        tree.tag_configure("highlight", background="yellow")
    else:
        messagebox.showerror("Search","Patient not found. Try finding manually if the patient knows the Date and ID.")
        tree.tag_configure("highlight", background="white")

def deselect_tree_item(event):
    item=tree_patients.focus()
    if item :
        tree_patients.selection_remove(item)                    
         



# GUI Setup
def main():
    initialize_database()
    global entry_name, entry_age, combo_gender, entry_contact, text_Address
    global tree_patients
    
    
    backup_thread = threading.Thread(target=backup_database, daemon=True)
    backup_thread.start()
    
    root = tk.Tk()
    
    img=PhotoImage(file=r'Logo.png')
    root.iconphoto(True,img)
    root.title("Patient Information and Record Management App")
    root.state("zoomed")
    
    
    
    frame_form = ttk.LabelFrame(root, text="Add Patient")
    frame_form.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(frame_form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    entry_name = ttk.Entry(frame_form)
    entry_name.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frame_form, text="Age:").grid(row=0, column=3, padx=5, pady=5)
    entry_age = ttk.Entry(frame_form)
    entry_age.grid(row=0, column=4, padx=5, pady=5)
    
    ttk.Label(frame_form, text="Gender:").grid(row=1, column=0, padx=5, pady=5)
    combo_gender = ttk.Combobox(frame_form, values=["Male", "Female", "Other"])
    combo_gender.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(frame_form, text="Contact:").grid(row=1, column=3, padx=5, pady=5)
    entry_contact = ttk.Entry(frame_form)
    entry_contact.grid(row=1, column=4, padx=5, pady=5)
    
    ttk.Label(frame_form, text="Address:").grid(row=4, column=1, padx=5, pady=5)
    text_Address = tk.Text(frame_form, height=5, width=40)
    text_Address.grid(row=4, column=2, padx=5, pady=5)
    
    
    
    
    ttk.Button(frame_form, text="Add Patient", command=add_patient).grid(row=5, column=3, columnspan=2, pady=10)
    root.bind("<Return>",add_patient)
    root.bind("<Button-3>", deselect_tree_item)
    
    # Search bar
    search_frame = tk.Frame(root)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    search_button = tk.Button(search_frame, text="Search", command=lambda: search_patients(search_entry, tree_patients))
    search_button.grid(row=0, column=2, padx=5, pady=5)
    
    # Frame List
    
    frame_patient_list = ttk.LabelFrame(root, text="Patient List")
    frame_patient_list.pack(fill="both", expand=True, padx=10, pady=5)
    
    tree_patients = ttk.Treeview(frame_patient_list, columns=("ID", "Name", "Age", "Gender", "Contact","Date","Adress"), show="headings")
    tree_patients.heading("ID", text="ID",anchor="center")
    tree_patients.heading("Name", text="Name",anchor="center")
    tree_patients.heading("Age", text="Age",anchor="center")
    tree_patients.heading("Gender", text="Gender",anchor="center")
    tree_patients.heading("Contact", text="Contact",anchor="center")
    tree_patients.heading("Date", text="Date",anchor="center")
    tree_patients.heading("Adress", text="Address",anchor="center")
    
    
    tree_patients.column("ID",anchor="center")
    tree_patients.column("Name",anchor="center")
    tree_patients.column("Age",anchor="center")
    tree_patients.column("Gender",anchor="center")
    tree_patients.column("Contact",anchor="center")
    tree_patients.column("Date",anchor="center")
    tree_patients.column("Address",anchor="w")
    
    
    scrollbar = ttk.Scrollbar(frame_patient_list, orient="vertical", command=tree_patients.yview)
    tree_patients.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    
    tree_patients.pack(fill="both", expand=True)
    
    frame_buttons = ttk.Frame(root)
    frame_buttons.pack(fill="x", pady=5)
    ttk.Button(frame_buttons, text="Export to PDF", command=export_to_pdf).pack(side="left", padx=5)
    ttk.Button(frame_buttons, text="Export to Excel", command=export_to_excel).pack(side="left", padx=5)
    ttk.Button(frame_buttons, text="Print All Records", command=print_data).pack(side="left", padx=5)
    ttk.Button(frame_buttons, text="Print Selected Record", command=lambda :Specific_data_print(tree_patients)).pack(side="left", padx=5)
    
    
    
    load_patients()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
