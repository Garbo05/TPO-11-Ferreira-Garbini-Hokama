import emoji
import tkinter as tk
import random
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

# Cargar palabras desde un archivo .txt
def cargar_palabras(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        palabras = [linea.strip() for linea in f.readlines()]
    return palabras

# Elimina los acentos de una palabra
def remove_accents(word):
    diccionario_tildes = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U'
    }
    resultado = ""
    for letra in word:
        resultado += diccionario_tildes.get(letra, letra)
    return resultado

# Verifica que la palabra ingresada sea válida
def validate_guess(word):
    return len(word) == 5 and word.isalpha()

# Verifica si la palabra está en la lista de palabras posibles
def validate_palabra(palabras, word):
    word = remove_accents(word)
    return word in palabras

# Jugar el juego
def play_game():
    global intentos, secret_word, cuadros_letras
    secret_word = random.choice(LISTA_PALABRAS_POSIBLES).upper()
    secret_word = remove_accents(secret_word)
    intentos = 0
    for i in range(6):
        for j in range(5):
            cuadros_letras[i][j].delete(0, tk.END)  # Limpia las entradas

# Manejar el intento del usuario
def hacer_intento(event=None):
    global intentos
    if intentos < 6:
        palabra = "".join(cuadros_letras[intentos][i].get().upper() for i in range(5))
        palabra = remove_accents(palabra)
        
        # Mensajes de depuración
        print("Palabra ingresada:", palabra)

        # Validar la palabra ingresada
        if not validate_guess(palabra) or not validate_palabra(LISTA_PALABRAS_POSIBLES, palabra):
            print("Por favor ingrese una palabra válida de 5 letras que esté en la lista.")
            # Resetear las letras ingresadas
            for i in range(5):
                cuadros_letras[intentos][i].delete(0, tk.END)  # Limpia las entradas
            return
        
        resultado = [''] * 5
        diccionario_secreto = {letra: secret_word.count(letra) for letra in set(secret_word)}
        
        # Comprobar letras correctas (verde)
        for i in range(5):
            if palabra[i] == secret_word[i]:
                resultado[i] = 'green'
                diccionario_secreto[palabra[i]] -= 1
        
        # Comprobar letras incorrectas (amarillo y rojo)
        for i in range(5):
            if resultado[i] == '':
                if palabra[i] in secret_word and diccionario_secreto[palabra[i]] > 0:
                    resultado[i] = 'yellow'
                    diccionario_secreto[palabra[i]] -= 1
                else:
                    resultado[i] = 'red'
        
        # Actualizar la interfaz
        for i in range(5):
            cuadros_letras[intentos][i].delete(0, tk.END)
            cuadros_letras[intentos][i].insert(0, palabra[i])
            cuadros_letras[intentos][i].config(bg=resultado[i])
        
        intentos += 1
        
        if palabra == secret_word:
            print(f"¡Felicidades! La palabra secreta era {secret_word}.")
            return
        elif intentos == 6:
            print(f"Se acabaron los intentos. La palabra secreta era {secret_word}.")

def on_key_press(event):
    if event.char.isalpha() and len(event.widget.get()) == 0:  # Solo permite una letra si el cuadro está vacío
        event.widget.insert(tk.END, event.char)
        next_widget = event.widget.tk_focusNext()  # Obtiene el siguiente widget
        if next_widget:
            next_widget.focus()  # Cambia el foco al siguiente cuadro
        return "break"  # Evita que el evento se propague y cause duplicación
    elif event.keysym == 'space':  # Confirmar intento con espacio
        hacer_intento()

# Configuración de la ventana
ventana = tk.Tk()
ventana.config(width=300, height=200)
ventana.title("Stringle")
cuadros_letras = []
for intento in range(6):  # 6 filas para intentos
    fila_cuadros = []
    for letra in range(5):  # 5 columnas para letras
        cuadro = tk.Entry(ventana, width=2, font=("Arial", 24))
        cuadro.grid(row=intento, column=letra, padx=5, pady=5)
        cuadro.bind("<Key>", on_key_press)  # Bind para manejar la entrada de teclado
        fila_cuadros.append(cuadro)
    cuadros_letras.append(fila_cuadros)

# Cargar palabras y comenzar el juego
LISTA_PALABRAS_POSIBLES = cargar_palabras('palabras.txt')
intentos = 0
play_game()
ventana.mainloop()