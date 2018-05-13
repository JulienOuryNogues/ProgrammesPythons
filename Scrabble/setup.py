__author__ = 'Julien'
"""Fichier d'installation de tout fichier .py"""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Scrabble",
    version = "2.0",
    description = "Jeu de Scrabble. Un joueur. Langues disponibles : Français, anglais, allemand, italien, espagnol",
    author="Julien",
    executables = [Executable(script="Jeu de Scrabble.py")],
)