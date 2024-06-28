import customtkinter as ctk
from tkinter import scrolledtext, filedialog, messagebox
from fpdf import FPDF
import random
import string

def create_generator_frame(app):
    global generator_frame, history_textbox, password_length_entry, use_uppercase, use_lowercase, use_special, use_digits, password_display
    generator_frame = ctk.CTkFrame(app, width=1720, height=1080, fg_color="#D3D3D3")
    generator_label = ctk.CTkLabel(generator_frame, text="Générateur de Mots de Passe", font=("Helvetica", 20), text_color="black")
    generator_label.pack(pady=20)

    # Nombre de caractères
    length_label = ctk.CTkLabel(generator_frame, text="Nombre de caractères :", font=("Helvetica", 14), text_color="black")
    length_label.pack(pady=(20, 5))
    password_length_entry = ctk.CTkEntry(generator_frame, width=50)
    password_length_entry.pack(pady=5)

    # Options de génération
    use_uppercase = ctk.CTkCheckBox(generator_frame, text="Majuscules", text_color="black")
    use_uppercase.pack(pady=5)
    use_lowercase = ctk.CTkCheckBox(generator_frame, text="Minuscules", text_color="black")
    use_lowercase.pack(pady=5)
    use_special = ctk.CTkCheckBox(generator_frame, text="Caractères spéciaux", text_color="black")
    use_special.pack(pady=5)
    use_digits = ctk.CTkCheckBox(generator_frame, text="Chiffres", text_color="black")
    use_digits.pack(pady=5)

    # Bouton de génération
    generate_button = ctk.CTkButton(generator_frame, text="Générer", command=generate_password)
    generate_button.pack(pady=20)

    # Zone d'affichage du mot de passe généré
    password_display = ctk.CTkEntry(generator_frame, width=300)
    password_display.pack(pady=10)
    password_display.configure(state="readonly")

    # Bouton d'effacement de l'historique
    clear_button = ctk.CTkButton(generator_frame, text="Effacer", command=clear_history)
    clear_button.pack(pady=10)

    # Zone d'affichage pour l'historique
    history_label = ctk.CTkLabel(generator_frame, text="Historique des mots de passe générés :", font=("Helvetica", 14), text_color="black")
    history_label.pack(pady=(20, 5))
    history_textbox = scrolledtext.ScrolledText(generator_frame, width=80, height=10, wrap="word")
    history_textbox.pack(pady=(5, 20))
    history_textbox.configure(state="disabled")

    return generator_frame

def generate_password():
    length = int(password_length_entry.get())
    characters = ""
    if use_uppercase.get():
        characters += string.ascii_uppercase
    if use_lowercase.get():
        characters += string.ascii_lowercase
    if use_special.get():
        characters += string.punctuation
    if use_digits.get():
        characters += string.digits

    if not characters:
        messagebox.showerror("Erreur", "Veuillez sélectionner au moins une option de caractères.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_display.configure(state="normal")
    password_display.delete(0, 'end')
    password_display.insert(0, password)
    password_display.configure(state="readonly")

    history_textbox.configure(state="normal")
    history_textbox.insert('end', password + '\n')
    history_textbox.configure(state="disabled")

def clear_history():
    global history_textbox
    history_textbox.configure(state="normal")
    history_textbox.delete(1.0, "end")
    history_textbox.configure(state="disabled")

def save_generator_as_pdf(file_path=None):
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, "Rapport Générateur de Mots de Passe", ln=True, align='C')
        pdf.set_font("Arial", 'BU', size=14)
        pdf.cell(0, 10, "Historique des mots de passe générés", ln=True)
        pdf.set_font("Arial", size=12)
        history_textbox.configure(state="normal")
        lines = history_textbox.get(1.0, "end").split("\n")
        history_textbox.configure(state="disabled")
        for line in lines:
            line_encoded = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, line_encoded)
        pdf.output(file_path)
