import subprocess
import sys
import os
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from nmap_page import save_as_pdf as save_nmap_as_pdf
from bruteforce_ssh_page import save_bruteforce_as_pdf
from exfiltration_page import save_exfiltration_as_pdf
from generator_page import save_generator_as_pdf
from website_copier_page import save_website_copier_as_pdf

# Fonction pour installer un package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Fonction pour générer le rapport global
def generate_global_report():
    nmap_pdf = "nmap_report.pdf"
    bruteforce_pdf = "bruteforce_report.pdf"
    exfiltration_pdf = "exfiltration_report.pdf"
    generator_pdf = "generator_report.pdf"
    website_copier_pdf = "website_copier_report.pdf"

    save_nmap_as_pdf(nmap_pdf)
    save_bruteforce_as_pdf(bruteforce_pdf)
    save_exfiltration_as_pdf(exfiltration_pdf)
    save_generator_as_pdf(generator_pdf)
    save_website_copier_as_pdf(website_copier_pdf)

    global_report_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if global_report_path:
        writer = PdfWriter()

        for pdf_path in [nmap_pdf, bruteforce_pdf, exfiltration_pdf, generator_pdf, website_copier_pdf]:
            if os.path.exists(pdf_path):
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    writer.add_page(page)
                os.remove(pdf_path)
            else:
                print(f"Le fichier {pdf_path} n'existe pas et ne peut pas être ajouté au rapport global.")

        with open(global_report_path, "wb") as out_file:
            writer.write(out_file)
