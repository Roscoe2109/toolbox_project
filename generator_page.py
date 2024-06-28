import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
import random
import string

def create_generator_frame(app):
    global length_entry, uppercase_var, lowercase_var, special_var, digits_var, password_display, password_history
    generator_frame = ctk.CTkFrame(app, width=1720, height=1080, fg_color="#D3D3D3")
    generator_label = ctk.CTkLabel(generator_frame, text="Générateur", font=("Helvetica", 20), text_color="black")
    generator_label.pack(pady=20)

    options_frame = ctk.CTkFrame(generator_frame, fg_color="#D3D3D3")
    options_frame.pack(pady=10)

    length_label = ctk.CTkLabel(options_frame, text="Nombre de caractères :", font=("Helvetica", 14), text_color="black")
    length_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    length_entry = ctk.CTkEntry(options_frame, width=60)
    length_entry.grid(row=0, column=1, padx=10, pady=5)

    uppercase_var = tk.BooleanVar()
    uppercase_check = ctk.CTkCheckBox(options_frame, text="Majuscules", variable=uppercase_var, text_color="black")
    uppercase_check.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    lowercase_var = tk.BooleanVar()
    lowercase_check = ctk.CTkCheckBox(options_frame, text="Minuscules", variable=lowercase_var, text_color="black")
    lowercase_check.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    special_var = tk.BooleanVar()
    special_check = ctk.CTkCheckBox(options_frame, text="Caractères spéciaux", variable=special_var, text_color="black")
    special_check.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    digits_var = tk.BooleanVar()
    digits_check = ctk.CTkCheckBox(options_frame, text="Chiffres", variable=digits_var, text_color="black")
    digits_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    password_display = ctk.CTkEntry(generator_frame, width=300, state='readonly', text_color="white")
    password_display.pack(pady=10)

    generate_button = ctk.CTkButton(generator_frame, text="Générer", command=generate_password)
    generate_button.pack(pady=10)

    clear_button = ctk.CTkButton(generator_frame, text="Effacer", command=clear_history)
    clear_button.pack(pady=10)

    password_history_label = ctk.CTkLabel(generator_frame, text="Historique des mots de passe générés :", font=("Helvetica", 14), text_color="black")
    password_history_label.pack(pady=(20, 5))

    password_history = scrolledtext.ScrolledText(generator_frame, width=80, height=10, wrap="word")
    password_history.pack(pady=(5, 10))
    password_history.configure(state="disabled")

    return generator_frame

def generate_password():
    length = int(length_entry.get()) if length_entry.get().isdigit() else 12
    characters = ""
    if uppercase_var.get():
        characters += string.ascii_uppercase
    if lowercase_var.get():
        characters += string.ascii_lowercase
    if special_var.get():
        characters += string.punctuation
    if digits_var.get():
        characters += string.digits
    if not characters:
        characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    password_display.configure(state='normal')
    password_display.delete(0, "end")
    password_display.insert(0, password)
    password_display.configure(state='readonly')
    password_history.configure(state='normal')
    password_history.insert("end", password + "\n")
    password_history.see("end")
    password_history.configure(state='disabled')

def clear_history():
    password_history.configure(state='normal')
    password_history.delete(1.0, "end")
    password_history.configure(state='disabled')
