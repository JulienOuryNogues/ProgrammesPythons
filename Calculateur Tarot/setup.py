__author__ = 'Julien'
"""Fichier d'installation de tout fichier .py"""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Tarot Scores",
    version = "1.0",
    description = "Calculateur de points pour jeu de Tarot. 3 à 5 joueurs",
    author="Julien",
    executables = [Executable(script="Calculateur Tarot.py")],
)