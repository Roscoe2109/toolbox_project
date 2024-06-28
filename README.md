# Projet master 1 - Création toolbox


Le projet Toolbox Hacking est une application développé dans le cadre mon projet de fin de première année de master. Cette boîte à outils centralise et automatise des outils de sécurités couramment utilisés pour faciliter les tests d'intrusion. Celle-ci permet également de générer des rapports détaillés pour chaque test.

## Fonctionnalités

- Scan de Ports (Nmap): Détecte les ports ouverts sur un réseau ou un ordinateur afin d'identifier les services disponibles et potentiellement vulnérables
- Bruteforce SSH: Réalise une attaque visant à deviner les identifiants de connexion SSH via de nombreuses combinaisons stockées dans un dictionnaire
- Générateur de Mots de Passe: Outil pour créer des mots de passe aléatoires et sécurisés
- Exfiltration de Données: Attaque visant à extraire des données sensibles ou confidentielles d’un système vers un emplacement externe
- Website Copier: Outil qui permet le téléchargement et la copie du contenu d'un site web entier pour une utilisation hors ligne ou pour l'analyser

## Technologies Utilisées

- Langage de Programmation: Python
- Interface Utilisateur: CustomTkinter
- Connexions SSH: Paramiko
- Website Copier: PyWebCopy
- Génération de Rapports: FPDF
- Fusion de PDF: PyPDF2

## Installation du projet

### Cloner le répôt :

```
git clone https://github.com/Roscoe2109/toolbox_project.git
```

### Exécuter le projet :

L'ensemble des dépendances nécessaires sont téléchargées lors de l'exécution du script : 
```
cd toolbox_project
python main.py
```
