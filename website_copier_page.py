import customtkinter as ctk
from tkinter import filedialog, messagebox
from fpdf import FPDF
import subprocess
import sys
import os

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywebcopy'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lxml[html_clean]'])
        import pywebcopy
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'installation des dépendances : {e}")
        return None
    return pywebcopy

pywebcopy = install_dependencies()

def create_website_copier_frame(app):
    global website_url_entry, download_directory_entry
    
    website_copier_frame = ctk.CTkFrame(app, width=1720, height=1080, fg_color="#D3D3D3")
    website_copier_label = ctk.CTkLabel(website_copier_frame, text="Website Copier", font=("Helvetica", 20), text_color="black")
    website_copier_label.pack(pady=20)
    
    url_label = ctk.CTkLabel(website_copier_frame, text="URL :", font=("Helvetica", 14), text_color="black")
    url_label.pack(pady=(20, 5))
    website_url_entry = ctk.CTkEntry(website_copier_frame, width=400)
    website_url_entry.pack(pady=5)
    
    download_directory_label = ctk.CTkLabel(website_copier_frame, text="Dossier de destination :", font=("Helvetica", 14), text_color="black")
    download_directory_label.pack(pady=(20, 5))
    download_directory_entry = ctk.CTkEntry(website_copier_frame, width=400)
    download_directory_entry.pack(pady=5)
    
    def select_download_directory():
        directory_path = filedialog.askdirectory()
        download_directory_entry.delete(0, "end")
        download_directory_entry.insert(0, directory_path)
    
    select_directory_button = ctk.CTkButton(website_copier_frame, text="Sélectionner le dossier", command=select_download_directory)
    select_directory_button.pack(pady=10)
    
    button_frame = ctk.CTkFrame(website_copier_frame, fg_color="#D3D3D3")
    button_frame.pack(pady=10)
    
    copier_button = ctk.CTkButton(button_frame, text="Copier", command=run_website_copier)
    copier_button.pack(side="left", padx=10)
    
    pdf_button = ctk.CTkButton(button_frame, text="Télécharger en PDF", command=lambda: save_website_copier_as_pdf("website_copier_report.pdf"))
    pdf_button.pack(side="left", padx=10)
    
    return website_copier_frame

def run_website_copier():
    if pywebcopy is None:
        return
    
    url = website_url_entry.get()
    download_directory = download_directory_entry.get()
    if not url or not download_directory:
        messagebox.showerror("Erreur", "Veuillez fournir une URL et sélectionner un dossier de destination.")
        return

    try:
        pywebcopy.save_website(
            url=url,
            project_folder=download_directory,
            bypass_robots=True,
            debug=True,
            open_in_browser=False
        )
        messagebox.showinfo("Succès", f"Site web {url} copié avec succès dans {download_directory}.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

def save_website_copier_as_pdf(file_path="website_copier_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(0, 10, "Rapport Website Copier", ln=True, align='C')
    pdf.set_font("Arial", 'BU', size=14)
    pdf.cell(0, 10, "Résultats", ln=True)
    pdf.set_font("Arial", size=12)
    url = website_url_entry.get()
    download_directory = download_directory_entry.get()
    content = f"URL : {url}\nDossier de destination : {download_directory}\n"
    pdf.multi_cell(0, 10, content)
    pdf.output(file_path)
