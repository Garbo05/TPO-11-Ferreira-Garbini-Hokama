import tkinter as tk
import random
from colorama import init

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
            cuadros_letras[i][j].config(state="normal")
            cuadros_letras[i][j].delete(0, tk.END)  # Limpia las entradas
            cuadros_letras[i][j].config(state="normal", bg="white")  # Reset background color

def hacer_intento(event=None):
    global intentos
    if intentos < 6:
        palabra = "".join(cuadros_letras[intentos][i].get().upper() for i in range(5))
        palabra = remove_accents(palabra)

        print("Palabra ingresada:", palabra)  # Mensajes de depuración

        # Validar la palabra ingresada
        if not validate_guess(palabra) or not validate_palabra(LISTA_PALABRAS_POSIBLES, palabra):
            print("Por favor ingrese una palabra válida de 5 letras que esté en la lista.")
            # Resetear las letras ingresadas
            for i in range(5):
                cuadros_letras[intentos][i].delete(0, tk.END)  # Limpia las entradas
            
            # Move focus back to the first input box of the current attempt
            cuadros_letras[intentos][0].focus()
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

        # Actualizar la interfaz con los colores
        for i in range(5):
            cuadros_letras[intentos][i].config(state="normal")  # Ensure state is normal to change color
            cuadros_letras[intentos][i].delete(0, tk.END)
            cuadros_letras[intentos][i].insert(0, palabra[i])
            cuadros_letras[intentos][i].config(bg=resultado[i])  # Set the background color

            # Prevent further interaction (make uneditable but leave color intact)
            cuadros_letras[intentos][i].bind("<Key>", lambda e: "break")  # Block key input
            cuadros_letras[intentos][i].bind("<Button-1>", lambda e: "break")  # Block mouse clicks
            cuadros_letras[intentos][i].config(takefocus=0)  # Prevent focus (can't tab or click into)

        intentos += 1

        if palabra == secret_word:
            print(f"¡Felicidades! La palabra secreta era {secret_word}.")
            return
        elif intentos == 6:
            print(f"Se acabaron los intentos. La palabra secreta era {secret_word}.")
            return

        # Move focus to the next row of entries after entering a guess
        cuadros_letras[intentos][0].focus()  # Focus on the first box of the next row


def on_key_press(event, letra, intento):
    # Handle letter input
    if event.char.isalpha() and len(event.widget.get()) == 0:  # Only allow a letter if the box is empty
        event.widget.insert(tk.END, event.char)
        next_widget = event.widget.tk_focusNext()  # Get the next widget (next input box)
        if next_widget and letra != 4:
            next_widget.focus()  # Move the focus to the next box
        return "break"  # Stop further event propagation to prevent duplication

    # Handle Backspace
    elif event.keysym == "BackSpace":
        if len(event.widget.get()) == 0:  # If the current box is empty, go to the previous one
            previous_widget = event.widget.tk_focusPrev()  # Get the previous widget
            if previous_widget:
                previous_widget.focus()  # Move the focus to the previous box
                previous_widget.delete(0, tk.END)  # Delete its content
        else:
            event.widget.delete(0, tk.END)  # If the current box has a letter, delete it

    # Handle Enter key
    elif event.keysym == 'Return':  # Confirm word attempt with Enter key
        hacer_intento()

    # Block any non-alphabetic input
    if not event.char.isalpha() and event.keysym not in ("BackSpace", "Return"):
        return "break"  # Prevent non-alphabetic input


def on_key_press_new(event, letra, intento):
    # Handle letter input
    if event.char.isalpha() and len(event.widget.get()) == 0:  # Only allow a letter if the box is empty
        event.widget.insert(tk.END, event.char)
        next_widget = event.widget.tk_focusNext()  # Get the next widget (next input box)
        if next_widget and letra != 4:
            next_widget.focus()  # Move the focus to the next box
        return "break"  # Stop further event propagation to prevent duplication

    # Handle Backspace on the first box (do nothing)
    elif event.keysym == "BackSpace":
        if event.widget == cuadros_letras[intento][0]:  # Prevent going back if at the first position
            return "break"
        else:
            event.widget.delete(0, tk.END)

    # Handle Enter key
    elif event.keysym == 'Return':  # Confirm word attempt with Enter key
        hacer_intento()

    # Block any non-alphabetic input
    if not event.char.isalpha() and event.keysym not in ("BackSpace", "Return"):
        return "break"  # Prevent non-alphabetic input


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
        
        if letra != 0:
            cuadro.bind("<Key>", lambda event, l=letra, i=intento: on_key_press(event, l, i))  # Bind para manejar la entrada de teclado
        else:
            cuadro.bind("<Key>", lambda event, l=letra, i=intento: on_key_press_new(event, l, i))  # Bind para manejar la entrada de teclado
        
        fila_cuadros.append(cuadro)
    cuadros_letras.append(fila_cuadros)

# Cargar palabras y comenzar el juego
LISTA_PALABRAS_POSIBLES = cargar_palabras('palabras.txt')
intentos = 0
play_game()
ventana.mainloop()