__author__ = 'Julien'
"""Fichier d'installation de tout fichier .py"""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Morpion - Tic Tac Toe",
    version = "1.0",
    description = "Jeu de Morpion. Un ou deux joueurs",
    author="Julien",
    executables = [Executable(script="Jeu de Morpion.py")],
)