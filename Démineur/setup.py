__author__ = 'Julien'
"""Fichier d'installation de tout fichier .py"""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Démineur",
    version = "1.0",
    description = "Jeu de Démineur. Un Joueur",
    author="Julien",
    executables = [Executable(script="Démineur.py")],
)