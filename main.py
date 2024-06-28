import subprocess
import sys

# Fonction pour installer un package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Liste des packages requis
required_packages = [
    "customtkinter", "paramiko", "pywebcopy", "fpdf", "pypdf2"
]

# Vérifier et installer les packages requis
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install_package(package)

# Importer les modules après l'installation
import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import customtkinter as ctk

from nmap_page import create_nmap_frame, run_nmap, save_as_pdf
from bruteforce_ssh_page import create_bruteforce_frame, run_bruteforce, save_bruteforce_as_pdf
from generator_page import create_generator_frame, generate_password, clear_history, save_generator_as_pdf
from exfiltration_page import create_exfiltration_frame, run_exfiltration, save_exfiltration_as_pdf
from website_copier_page import create_website_copier_frame, run_website_copier, save_website_copier_as_pdf
from utils import generate_global_report

# Initialiser l'application principale
app = ctk.CTk()
app.attributes("-fullscreen", False)  # Désactiver le mode plein écran
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}")  # Adapter la taille de la fenêtre à l'écran
app.title("Toolbox Hacking - Projet d'étude 2024")
app.configure(bg="#D3D3D3")  # Définir la couleur de fond globale en gris clair

current_frame = None

# Fonction pour gérer l'animation du menu
def toggle_menu():
    if menu_frame.winfo_ismapped():
        animate_menu("close")
    else:
        animate_menu("open")

# Fonction pour animer le menu
def animate_menu(action):
    current_width = menu_frame.winfo_width()
    new_width = 200 if action == "open" else 0
    increment = 10 if action == "open" else -10

    def expand():
        nonlocal current_width
        current_width += increment
        menu_frame.configure(width=current_width)
        if (action == "open" and current_width < new_width) or (action == "close" and current_width > new_width):
            app.after(10, expand)
        else:
            if action == "close":
                menu_frame.pack_forget()
                if current_frame:
                    current_frame.pack(fill="both", expand=True)
                else:
                    welcome_label.pack(fill="both", expand=True)

    if action == "open":
        if current_frame:
            current_frame.pack_forget()
        else:
            welcome_label.pack_forget()
        menu_frame.pack(side="left", fill="y")
        expand()
    else:
        expand()

# Fonction pour afficher la page d'accueil
def show_home():
    global current_frame
    hide_all_frames()
    welcome_label.pack(fill="both", expand=True)
    current_frame = None

# Fonction pour masquer tous les cadres et afficher le cadre donné
def show_frame(frame):
    global current_frame
    hide_all_frames()
    frame.pack(fill="both", expand=True)
    current_frame = frame

# Créer le bouton du menu burger
burger_button = ctk.CTkButton(app, text="☰", command=toggle_menu, width=30)
burger_button.pack(side="left", anchor="nw", padx=(10, 10), pady=10)  # Ajout d'un espace entre le bouton menu et le bouton accueil

# Créer le bouton d'accueil
home_button = ctk.CTkButton(app, text="Accueil", command=show_home, width=60)
home_button.pack(side="left", anchor="nw", padx=(0, 10), pady=10)

# Créer le bouton de rapport global
global_report_button = ctk.CTkButton(app, text="Générer rapport global", command=generate_global_report, width=160)
global_report_button.pack(side="left", anchor="nw", padx=(10, 10), pady=10)

# Créer le cadre du menu
menu_frame = ctk.CTkFrame(app, width=0, height=1080, fg_color="#333333")  # Gris foncé pour le menu
menu_frame.pack_propagate(False)  # Empêcher le cadre de redimensionner automatiquement

# Fonction pour masquer tous les frames
def hide_all_frames():
    nmap_frame.pack_forget()
    bruteforce_frame.pack_forget()
    generator_frame.pack_forget()
    exfiltration_frame.pack_forget()
    website_copier_frame.pack_forget()
    welcome_label.pack_forget()

# Créer les frames pour chaque page
nmap_frame = create_nmap_frame(app)
bruteforce_frame = create_bruteforce_frame(app)
generator_frame = create_generator_frame(app)
exfiltration_frame = create_exfiltration_frame(app)
website_copier_frame = create_website_copier_frame(app)

# Ajouter des boutons de menu
nmap_button = ctk.CTkButton(menu_frame, text="Nmap", command=lambda: show_frame(nmap_frame))
nmap_button.pack(pady=10)

bruteforce_button = ctk.CTkButton(menu_frame, text="Bruteforce SSH", command=lambda: show_frame(bruteforce_frame))
bruteforce_button.pack(pady=10)

generator_button = ctk.CTkButton(menu_frame, text="Générateur", command=lambda: show_frame(generator_frame))
generator_button.pack(pady=10)

exfiltration_button = ctk.CTkButton(menu_frame, text="Exfiltration de données", command=lambda: show_frame(exfiltration_frame))
exfiltration_button.pack(pady=10)

website_copier_button = ctk.CTkButton(menu_frame, text="Website Copier", command=lambda: show_frame(website_copier_frame))
website_copier_button.pack(pady=10)

# Créer le label de bienvenue
welcome_label = ctk.CTkLabel(app, text="Bienvenue dans le projet Toolbox Hacking - 2024", font=("Helvetica", 20))
welcome_label.pack(fill="both", expand=True)

# Masquer le menu au démarrage
menu_frame.pack_forget()

# Démarrer l'application
app.mainloop()
