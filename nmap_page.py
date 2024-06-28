import customtkinter as ctk
from tkinter import scrolledtext, filedialog, messagebox
from fpdf import FPDF
import subprocess
import shutil
import os

def create_nmap_frame(app):
    global nmap_frame, ip_entry, result_text
    nmap_frame = ctk.CTkFrame(app, width=1720, height=1080, fg_color="#D3D3D3")
    nmap_label = ctk.CTkLabel(nmap_frame, text="Nmap", font=("Helvetica", 20), text_color="black")
    nmap_label.pack(pady=20)

    ip_label = ctk.CTkLabel(nmap_frame, text="Adresse IP à scanner :", font=("Helvetica", 14), text_color="black")
    ip_label.pack(pady=(20, 5))
    ip_entry = ctk.CTkEntry(nmap_frame, width=300)
    ip_entry.pack(pady=5)

    result_text = scrolledtext.ScrolledText(nmap_frame, width=80, height=20, wrap="word")
    result_text.pack(pady=(20, 10))
    result_text.configure(state="disabled")

    nmap_button_frame = ctk.CTkFrame(nmap_frame, fg_color="#D3D3D3")
    nmap_button_frame.pack(pady=10)
    nmap_launch_button = ctk.CTkButton(nmap_button_frame, text="Scanner", command=run_nmap_scan)
    nmap_launch_button.pack(side="left", padx=(0, 10))
    nmap_pdf_button = ctk.CTkButton(nmap_button_frame, text="Télécharger en PDF", command=save_as_pdf)
    nmap_pdf_button.pack(side="left", padx=(10, 0))

    return nmap_frame

def find_nmap():
    if shutil.which("nmap"):
        return "nmap"
    possible_paths = [
        "C:\\Program Files (x86)\\Nmap\\nmap.exe",
        "C:\\Program Files\\Nmap\\nmap.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def run_nmap_scan():
    ip = ip_entry.get()
    nmap_path = find_nmap()
    if not nmap_path:
        messagebox.showerror("Erreur", "Nmap n'est pas installé ou le chemin n'est pas configuré correctement.")
        return

    if ip:
        result_text.configure(state="normal")
        result_text.delete(1.0, "end")
        try:
            result = subprocess.run([nmap_path, "-sS", ip], capture_output=True, text=True)
            result_text.insert("end", result.stdout)
        except Exception as e:
            result_text.insert("end", f"Erreur : {e}\n")
        result_text.configure(state="disabled")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer une adresse IP valide.")

def save_as_pdf(file_path=None):
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, "Rapport Nmap", ln=True, align='C')
        pdf.set_font("Arial", 'BU', size=14)
        pdf.cell(0, 10, "Résultats", ln=True)
        pdf.set_font("Arial", size=12)
        result_text.configure(state="normal")
        lines = result_text.get(1.0, "end").split("\n")
        result_text.configure(state="disabled")
        for line in lines:
            line_encoded = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, line_encoded)
        pdf.output(file_path)
