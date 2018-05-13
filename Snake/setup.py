__author__ = 'Julien'
"""Fichier d'installation de tout fichier .py"""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Snake",
    version = "1.0",
    description = "Jeu de Snake. Un joueur",
    author="Julien",
    executables = [Executable(script="Snake.py")],
)