import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, filedialog
from fpdf import FPDF

def create_nmap_frame(app):
    global ip_entry, result_text
    nmap_frame = ctk.CTkFrame(app, width=1720, height=1080, fg_color="#D3D3D3")
    nmap_label = ctk.CTkLabel(nmap_frame, text="Nmap", font=("Helvetica", 20), text_color="black")
    nmap_label.pack(pady=20)

    def validate_ip_entry(char):
        return char.isdigit() or char == "."

    vcmd = (nmap_frame.register(validate_ip_entry), "%S")
    ip_label = ctk.CTkLabel(nmap_frame, text="Adresse IP à scanner", font=("Helvetica", 14), text_color="black")
    ip_label.pack(pady=(20, 5))

    ip_entry = ctk.CTkEntry(nmap_frame, width=300, validate="key", validatecommand=vcmd)
    ip_entry.pack(pady=5)

    result_text = scrolledtext.ScrolledText(nmap_frame, width=80, height=20, wrap=tk.WORD)
    result_text.pack(pady=(20, 10))
    result_text.configure(state="disabled")

    button_frame = ctk.CTkFrame(nmap_frame, fg_color="#D3D3D3")
    button_frame.pack(pady=10)
    scan_button = ctk.CTkButton(button_frame, text="Scanner", command=lambda: run_nmap(ip_entry.get()))
    scan_button.pack(side="left", padx=(0, 10))
    pdf_button = ctk.CTkButton(button_frame, text="Télécharger en PDF", command=save_as_pdf)
    pdf_button.pack(side="left", padx=(10, 0))

    return nmap_frame

def run_nmap(ip_address):
    if ip_address:
        result_text.configure(state="normal")
        result_text.delete(1.0, "end")
        try:
            process = subprocess.Popen(
                ["nmap", "-sS", ip_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in iter(process.stdout.readline, ''):
                result_text.insert("end", line)
                result_text.see("end")
                result_text.update_idletasks()
            process.stdout.close()
            process.wait()
        except Exception as e:
            result_text.insert("end", f"Error: {e}")
        result_text.configure(state="disabled")

def get_fake_cve_info(port):
    cve_info = {
        "80": ["CVE-2021-1234", "CVE-2021-5678"],
        "443": ["CVE-2020-1234", "CVE-2019-5678"],
        "22": ["CVE-2018-1234", "CVE-2017-5678"],
        "21": ["CVE-2016-1234", "CVE-2015-5678"],
        "25": ["CVE-2014-1234", "CVE-2013-5678"],
        "110": ["CVE-2012-1234", "CVE-2011-5678"],
        "143": ["CVE-2010-1234", "CVE-2009-5678"],
    }
    return cve_info.get(port, [])

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
        scanning_info = f"Adresse IP scannée : {ip_entry.get()}\n\n"
        pdf.multi_cell(0, 10, scanning_info)
        ports_info = ""
        cve_info = ""
        for line in lines:
            if "open" in line or "closed" in line or "filtered" in line:
                line_encoded = line.encode('latin-1', 'replace').decode('latin-1')
                ports_info += line_encoded + "\n"
                port = line.split("/")[0]
                cve_list = get_fake_cve_info(port)
                if cve_list:
                    cve_info += f"\nPort {port} :\n"
                    for cve in cve_list:
                        cve_info += f"- {cve}\n"
        pdf.multi_cell(0, 10, ports_info)
        if cve_info:
            pdf.set_font("Arial", 'BU', size=14)
            pdf.cell(0, 10, "\nInformations sur les CVE", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, cve_info)
        pdf.output(file_path)
