import random
import re
from colorama import Fore, init

#FUNCIONES

def print_variables(a):
    print(a)

def verify_guess(word):
    while word.isalpha() == False:
            word = input("La palabra no puede contener numeros. Ingrese una palabra válida. ")
    while word == "":
        word = input("No se ingreso ninguna palabra. Ingrese una palabra. ")
    while len(word) != 5:
        word = input("Longitud incorrecta. Ingrese una palabra de 5 letras. ") 
    return word
    

#PROGRAMA PRINCIPAL

LISTA_PALABRAS_POSIBLES = ["ARBOL","AMIGO","CAJON","CLASE","BOTON"]
print_variables(LISTA_PALABRAS_POSIBLES)
palabra_secreta = LISTA_PALABRAS_POSIBLES[random.randint(0,len(LISTA_PALABRAS_POSIBLES)-1)]
print_variables(palabra_secreta)
INTENTOS_MAXIMO = 6
#Inicializacion de la ista en la que se van a agregar las letras que se encuenten en la palabra  




print("BIENVENIDO A STRINGLE\nEl juego consiste en adivinar una palabra de 5 letras, para ello contas con 6 intentos, despues de cada intento se te informara que letras estan en la palabra y se encuentran en la posicion correcta y cuales forman parte de la palabra, pero estan en la posicion incorrecta")

for intentos in range (1, INTENTOS_MAXIMO+1):
    palabra = input(f"INTENTO N° {intentos}\nIngrese una palabra de 5 letras:  ")
    palabra = verify_guess(palabra)
    palabra.upper()
    print_variables(palabra)
    resultado=[]
    for i in range (len(palabra)):
        if palabra[i]==palabra_secreta[i]:
            #letra_verde=Fore.GREEN+palabra[i]
            resultado.append(Fore.GREEN+palabra[i])
        elif palabra[i] in palabra_secreta:
            #letra_amarilla=Fore.YELLOW+palabra[i]
            resultado.append(Fore.YELLOW+palabra[i])
        else:
            # letra_roja=Fore.RED+palabra[i]
            resultado.append(letra_roja=Fore.RED+palabra[i])
    print(resultado)
if palabra==palabra_secreta:
    print(f"La palabra secreta era {palabra}. Felicidades")
else:
    print(f"Mala suerte, se agotaron tus {INTENTOS_MAXIMO} intentos, la palabra secreta era {palabra_secreta}.")                           

#print(Fore.GREEN + palabra)