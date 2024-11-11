import tkinter as tk
import random
from tkinter import messagebox
import importlib
import Funciones
import datetime

# Variables globales
letters_frames = []
letters_button = {}
attempts = 0
attempt_block = False
LIST_POSSIBLE_WORDS = []
current_time = datetime.datetime.now()

# Función para reiniciar el módulo Funciones y el juego


def reset_game():
    global window
    window.destroy()
    importlib.reload(Funciones)  # Recarga todo el módulo Funciones
    Funciones.create_window()  # Reinicia la ventana principal del juego


# Cargar palabras desde un archivo .txt

def charge_words(file):
    with open(file, 'r', encoding='utf-8') as f:
        # Lee las palabras y devuelve la lista sin modificación
        return [linea.strip().upper() for linea in f.readlines()]


# Elimina los acentos de una palabra
def remove_accents(word):
    accents_dictionary = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
    }
    return ''.join(accents_dictionary.get(letter, letter) for letter in word)


# Verifica que la palabra ingresada sea válida
def validate_guess(word):
    return len(word) == 5 and word.isalpha()


# Verifica si la palabra está en la lista de palabras posibles
def validate_word(palabras, word):
    word = remove_accents(word)
    return word in palabras


# Jugar el juego
def play_game():
    global attempts, secret_word, letters_frames
    global letters_button, attempt_block, LIST_POSSIBLE_WORDS
    secret_word = random.choice(LIST_POSSIBLE_WORDS).upper()
    secret_word = remove_accents(secret_word)  # Elimina acentos
    attempts = 0  # Inicializa el número de intentos
    attempt_block = False  # Permite realizar intentos

# Función para bloquear la entrada del teclado
def block_keyboard(event):
    return "break"

# Función para bloquear clics
def block_click(event):
    return "break"


# Manejar el intento del usuario
def make_attempt():
    global attempts, secret_word, letters_frames
    global letters_button, attempt_block
    if attempt_block:
        return  # Si el intento está bloqueado, no hace nada
    if attempts < 6:  # Solo permite hasta 6 intentos
        word = "".join(
            letters_frames[attempts][i].get().upper() for i in range(5)
            )
        word = remove_accents(word)
        # Validar la palabra ingresada
        if not validate_guess(word) or not validate_word(
                                            LIST_POSSIBLE_WORDS, word
                                            ):
            for i in range(5):
                letters_frames[attempts][i].delete(0, tk.END)
            letters_frames[attempts][0].focus()  # Enfoca el primer cuadro
            return
        result = [''] * 5
        diccionario_secreto = {
            letter: secret_word.count(letter) for letter in set(secret_word)
            }
        # Comprobar letras correctas (verde)
        for i in range(5):
            if word[i] == secret_word[i]:
                result[i] = 'green'
                diccionario_secreto[word[i]] -= 1
        # Comprobar letras incorrectas (amarillo y gris)
        for i in range(5):
            if result[i] == '':
                if word[i] in secret_word and \
                        diccionario_secreto[word[i]] > 0:
                    result[i] = '#FCD12A'
                    diccionario_secreto[word[i]] -= 1
                else:
                    result[i] = 'gray'

        # Actualizar la interfaz con los colores
        for i in range(5):
            letters_frames[attempts][i].config(state="normal")
            letters_frames[attempts][i].delete(0, tk.END)
            letters_frames[attempts][i].insert(0, word[i])
            letters_frames[attempts][i].config(bg=result[i])
            letters_frames[attempts][i].bind("<Key>", block_keyboard)
            letters_frames[attempts][i].bind("<Button-1>", block_click)
            letters_frames[attempts][i].config(takefocus=0)
        attempts += 1  # Incrementa el número de intentos
        attempt_block = False  # Permite nuevos intentos
        # Verifica si ganó o si se acabaron los intentos
        if word == secret_word:
            messagebox.showinfo("¡Felicidades!",
                                f"La palabra secreta era {secret_word}."
                                )
            return
        elif attempts == 6:
            messagebox.showinfo("Fin del juego",
                                "Se acabaron los intentos."
                                f"La palabra secreta era {secret_word}."
                                )
            return
        letters_frames[attempts][0].focus()


# Botón para borrar la letra actual o la anterior
def borrar_letra():
    for i in range(4, -1, -1):
        if letters_frames[attempts][i].get():
            letters_frames[attempts][i].delete(0, tk.END)
            letters_frames[attempts][i].focus()
            break


# Manejar la entrada de teclado en el grid
def on_key_press(event, letter, guess):
    # Verificar si el intento corresponde al guess actual
    if guess != attempts:
        return "break"  # Ignorar la entrada si no es el intento actual

    if event.char.isalpha():
        event.widget.delete(0, tk.END)  # Borrar el contenido actual
        event.widget.insert(0, event.char.upper())  # Insertar nuevo carácter
        next_widget = event.widget.tk_focusNext()
        if next_widget and letter != 4:
            next_widget.focus()
        return "break"
    elif event.keysym == "BackSpace":
        if len(event.widget.get()) == 0:
            if letter != 0:  # Verificar si NO es el primer casillero
                previous_widget = event.widget.tk_focusPrev()
                if previous_widget:
                    previous_widget.focus()
                    previous_widget.delete(0, tk.END)
        else:
            event.widget.delete(0, tk.END)
    elif event.keysym == 'Return':
        make_attempt()
    if not event.char.isalpha() and \
            event.keysym not in ("BackSpace", "Return"):
        return "break"


# Borrar la última letra ingresada
def borrar_virtual():
    global attempt_block
    if attempt_block:
        return
    for i in reversed(range(5)):
        if letters_frames[attempts][i].get() != "":
            letters_frames[attempts][i].delete(0, tk.END)
            return


def exit_game():
    return exit()


def create_window():
    global window, letters_frames, letters_button, LIST_POSSIBLE_WORDS
    window = tk.Tk()
    window.attributes("-fullscreen", True)  # Pantalla completa
    if current_time.hour >= 20 or current_time.hour < 6:
        window.config(bg='black')
    else:
        window.config(bg='white')
    window.title("Stringle")

    # Centrar los elementos de la interfaz
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    if current_time.hour >= 20 or current_time.hour < 6:
        frame_central = tk.Frame(window, bg='black')
    else:
        frame_central = tk.Frame(window, bg='white')
    frame_central.grid(row=0, column=0, padx=20, pady=20)

    # Título del juego
    if current_time.hour >= 20 or current_time.hour < 6:
        titulo = tk.Label(
            frame_central, text="LA PALABRA DEL DÍA",
            font=("Arial", 36), bg="black", fg="white"
            )
    else:
        titulo = tk.Label(
            frame_central, text="LA PALABRA DEL DÍA",
            font=("Arial", 36), bg="white", fg="black"
            )
    titulo.grid(row=0, columnspan=5, pady=(0, 20))

    # Crear el grid de cuadros de letras (intentos)
    letters_frames = []
    for guess in range(6):
        fila_cuadros = []
        for letter in range(5):
            if current_time.hour >= 20 or current_time.hour < 6:
                cuadro = tk.Entry(
                    frame_central, font=("Arial", 24), width=4,
                    justify="center", bg="black", fg="white",
                    highlightbackground="gray", highlightthickness=2
                    )
            else:
                cuadro = tk.Entry(
                    frame_central, font=("Arial", 24), width=4,
                    justify="center", bg="white", fg="black",
                    highlightbackground="gray", highlightthickness=2
                    )
            cuadro.grid(row=guess+1, column=letter, padx=10, pady=10)
            cuadro.bind(
                "<Key>", lambda event, letter=letter,
                guess=guess: on_key_press(event, letter, guess)  
                        ) # Manejar la entrada del teclado
            fila_cuadros.append(cuadro)
        letters_frames.append(fila_cuadros)

    # Crear teclado virtual (teclas)
    if current_time.hour >= 20 or current_time.hour < 6:
        frame_teclado = tk.Frame(window, bg='black')
    else:
        frame_teclado = tk.Frame(window, bg='white')
    frame_teclado.grid(row=1, column=0, pady=20)

    letters_row1 = "QWERTYUIOP"
    letters_row2 = "ASDFGHJKLÑ"
    letters_row3 = "ZXCVBNM"

    letters_button = {}  # Para almacenar los botones
    for fila, letras in enumerate([letters_row1, letters_row2, letters_row3]):
        for columna, letter in enumerate(letras):
            boton = tk.Button(
                frame_teclado, text=letter, font=("Arial", 14),
                width=4, height=2, bg="gray", fg="white",
                command=lambda letter=letter: enter_letter(letter)
                )
            boton.grid(row=fila, column=columna, padx=5, pady=5)
            letters_button[letter] = boton

    # Botones de "Enviar" y "Borrar"
    send_button = tk.Button(
        frame_teclado, text="Enviar",
        command=make_attempt, width=4, height=2,
        font=("Arial", 18), bg="green", fg="white")
    send_button.grid(row=2, column=9, padx=5, pady=5)
    delete_button = tk.Button(
        frame_teclado, text="Borrar", command=borrar_virtual,
        width=4, height=2, font=("Arial", 18), bg="red", fg="white"
        )
    delete_button.grid(row=1, column=9, padx=5, pady=5)

    # Boton de salida del programa
    exit_button = tk.Button(
        window, text="X", command=exit_game, width=3,
        height=2, font=("Arial", 18), bg="red", fg="white"
        )
    exit_button.place(x=10, y=10)

    # Botón para reiniciar el juego
    play_button = tk.Button(
        window, text="Jugar de nuevo", font=("Arial", 18),
        width=14, height=2, bg="green", fg="white",
        command=reset_game)
    play_button.grid(row=2, column=0, pady=20)

    # Cargar las palabras del archivo .txt
    LIST_POSSIBLE_WORDS = charge_words("words.txt")
    # Iniciar el juego
    play_game()

    # Mostrar la ventana
    window.mainloop()


# Ingresar letra desde el teclado virtual
def enter_letter(letter):
    widget_actual = letters_frames[attempts][0].focus_get()
    widget_actual.delete(0, tk.END)  # Borrar el contenido actual
    widget_actual.insert(0, letter.upper())  # Insertar el nuevo carácter
    next_widget = widget_actual.tk_focusNext()
    if next_widget:
        next_widget.focus()
