import random
import re

#FUNCIONES

def verify_guess(word):
    if word == "":
        word = input("Ingrese una palabra. ")
    elif len(word) != 5:
        word = input("Ingrese una palabra de 5 letras. ") 
    elif word.isdigit() == True:
        word = input("Ingrese una palabra válida. ")

#PROGRAMA PRINCIPAL

lista = ["arbol","amigo","cajon","clase","boton"]

print("BIENVENIDO A STRINGLE\nEl juego consiste en...")
palabra = input(" ")

hola = verify_guess(palabra)