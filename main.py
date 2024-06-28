import subprocess
import sys
import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import customtkinter as ctk

from nmap_page import create_nmap_frame, run_nmap, save_as_pdf
from bruteforce_ssh_page import create_bruteforce_frame, run_bruteforce, save_bruteforce_as_pdf
from generator_page import create_generator_frame, generate_password, clear_history
from exfiltration_page import create_exfiltration_frame, run_exfiltration, save_exfiltration_as_pdf
from website_copier_page import create_website_copier_frame, run_website_copier, save_website_copier_as_pdf
from utils import install_package, generate_global_report

def check_and_install_packages():
    required_packages = [
        "customtkinter", "paramiko", "pywebcopy", "fpdf", "pypdf2"
    ]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            install_package(package)

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

check_and_install_packages()

app = ctk.CTk()
app.attributes("-fullscreen", False)
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}")
app.title("Toolbox Hacking - Projet d'étude 2024")
app.configure(bg="#D3D3D3")

current_frame = None

def toggle_menu():
    if menu_frame.winfo_ismapped():
        animate_menu("close")
    else:
        animate_menu("open")

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

def show_home():
    global current_frame
    hide_all_frames()
    welcome_label.pack(fill="both", expand=True)
    current_frame = None

def show_frame(frame):
    global current_frame
    hide_all_frames()
    frame.pack(fill="both", expand=True)
    current_frame = frame

burger_button = ctk.CTkButton(app, text="☰", command=toggle_menu, width=30)
burger_button.pack(side="left", anchor="nw", padx=(10, 10), pady=10)  # Ajout d'un espace entre le bouton menu et le bouton accueil

home_button = ctk.CTkButton(app, text="Accueil", command=show_home, width=60)
home_button.pack(side="left", anchor="nw", padx=(0, 10), pady=10)

global_report_button = ctk.CTkButton(app, text="Générer rapport global", command=generate_global_report, width=160)
global_report_button.pack(side="left", anchor="nw", padx=(10, 10), pady=10)

menu_frame = ctk.CTkFrame(app, width=0, height=1080, fg_color="#333333")
menu_frame.pack_propagate(False)

def hide_all_frames():
    nmap_frame.pack_forget()
    bruteforce_frame.pack_forget()
    generator_frame.pack_forget()
    exfiltration_frame.pack_forget()
    website_copier_frame.pack_forget()
    welcome_label.pack_forget()

nmap_frame = create_nmap_frame(app)
bruteforce_frame = create_bruteforce_frame(app)
generator_frame = create_generator_frame(app)
exfiltration_frame = create_exfiltration_frame(app)
website_copier_frame = create_website_copier_frame(app)

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

welcome_label = ctk.CTkLabel(app, text="Bienvenue dans le projet Toolbox Hacking - 2024", font=("Helvetica", 20))
welcome_label.pack(fill="both", expand=True)

menu_frame.pack_forget()

app.mainloop()
