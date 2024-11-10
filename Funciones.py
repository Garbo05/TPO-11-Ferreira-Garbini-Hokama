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
    return ''.join(accents_dictionary.get(letra, letra) for letra in word)


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

    # Limpia los cuadros de letras
    for i in range(6):
        for j in range(5):
            letters_frames[i][j].config(state="normal")
            letters_frames[i][j].delete(0, tk.END)
            if current_time.hour >= 20 or current_time.hour < 6:
                letters_frames[i][j].config(
                    state="normal", bg="black",
                    fg="white", highlightbackground="gray",
                    highlightthickness=2
                    )  # Restablece el color de fondo
            else:
                letters_frames[i][j].config(
                    state="normal", bg="white",
                    fg="black", highlightbackground="gray",
                    highlightthickness=2
                    )  # Restablece el color de fondo
    # Reinicia los colores de las teclas
    for letra, boton in letters_button.items():
        boton.config(bg="gray", fg="white")


# Manejar el intento del usuario
def hacer_intento():
    global attempts, secret_word, letters_frames
    global letters_button, attempt_block
    if attempt_block:
        return  # Si el intento está bloqueado, no hace nada
    if attempts < 6:  # Solo permite hasta 6 intentos
        palabra = "".join(
            letters_frames[attempts][i].get().upper() for i in range(5)
            )
        palabra = remove_accents(palabra)
        # Validar la palabra ingresada
        if not validate_guess(palabra) or not validate_word(
                                            LIST_POSSIBLE_WORDS, palabra
                                            ):
            for i in range(5):
                letters_frames[attempts][i].delete(0, tk.END)
            letters_frames[attempts][0].focus()  # Enfoca el primer cuadro
            return
        resultado = [''] * 5
        diccionario_secreto = {
            letra: secret_word.count(letra) for letra in set(secret_word)
            }
        # Comprobar letras correctas (verde)
        for i in range(5):
            if palabra[i] == secret_word[i]:
                resultado[i] = 'green'
                diccionario_secreto[palabra[i]] -= 1
        # Comprobar letras incorrectas (amarillo y gris)
        for i in range(5):
            if resultado[i] == '':
                if palabra[i] in secret_word and \
                        diccionario_secreto[palabra[i]] > 0:
                    resultado[i] = '#FCD12A'
                    diccionario_secreto[palabra[i]] -= 1
                else:
                    resultado[i] = 'gray'

        # Actualizar la interfaz con los colores
        for i in range(5):
            letters_frames[attempts][i].config(state="normal")
            letters_frames[attempts][i].delete(0, tk.END)
            letters_frames[attempts][i].insert(0, palabra[i])
            letters_frames[attempts][i].config(bg=resultado[i])
            letters_frames[attempts][i].bind("<Key>", lambda e: "break")
            letters_frames[attempts][i].bind("<Button-1>", lambda e: "break")
            letters_frames[attempts][i].config(takefocus=0)
        attempts += 1  # Incrementa el número de intentos
        attempt_block = False  # Permite nuevos intentos
        # Verifica si ganó o si se acabaron los intentos
        if palabra == secret_word:
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
def on_key_press(event, letra, intento):
    # Verificar si el intento corresponde al intento actual
    if intento != attempts:
        return "break"  # Ignorar la entrada si no es el intento actual

    if event.char.isalpha():
        event.widget.delete(0, tk.END)  # Borrar el contenido actual
        event.widget.insert(0, event.char.upper())  # Insertar nuevo carácter
        next_widget = event.widget.tk_focusNext()
        if next_widget and letra != 4:
            next_widget.focus()
        return "break"
    elif event.keysym == "BackSpace":
        if len(event.widget.get()) == 0:
            if letra != 0:  # Verificar si NO es el primer casillero
                previous_widget = event.widget.tk_focusPrev()
                if previous_widget:
                    previous_widget.focus()
                    previous_widget.delete(0, tk.END)
        else:
            event.widget.delete(0, tk.END)
    elif event.keysym == 'Return':
        hacer_intento()
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


def salir_programa():
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
            font=("Arial", 24), bg="black", fg="white"
            )
    else:
        titulo = tk.Label(
            frame_central, text="LA PALABRA DEL DÍA",
            font=("Arial", 24), bg="white", fg="black"
            )
    titulo.grid(row=0, columnspan=5, pady=(0, 20))

    # Crear el grid de cuadros de letras (intentos)
    letters_frames = []
    for intento in range(6):
        fila_cuadros = []
        for letra in range(5):
            if current_time.hour >= 20 or current_time.hour < 6:
                cuadro = tk.Entry(
                    frame_central, font=("Arial", 16), width=3,
                    justify="center", bg="black", fg="white",
                    highlightbackground="gray", highlightthickness=2
                    )
            else:
                cuadro = tk.Entry(
                    frame_central, font=("Arial", 16), width=3,
                    justify="center", bg="white", fg="black",
                    highlightbackground="gray", highlightthickness=2
                    )
            cuadro.grid(row=intento+1, column=letra, padx=5, pady=5)
            cuadro.bind(
                "<Key>", lambda event, letra=letra,
                intento=intento: on_key_press(event, letra, intento)
                )  # Manejar la entrada del teclado
            fila_cuadros.append(cuadro)
        letters_frames.append(fila_cuadros)

    # Crear teclado virtual (teclas)
    if current_time.hour >= 20 or current_time.hour < 6:
        frame_teclado = tk.Frame(window, bg='black')
    else:
        frame_teclado = tk.Frame(window, bg='white')
    frame_teclado.grid(row=1, column=0, pady=20)

    letras_fila1 = "QWERTYUIOP"
    letras_fila2 = "ASDFGHJKLÑ"
    letras_fila3 = "ZXCVBNM"

    letters_button = {}  # Para almacenar los botones
    for fila, letras in enumerate([letras_fila1, letras_fila2, letras_fila3]):
        for columna, letra in enumerate(letras):
            boton = tk.Button(
                frame_teclado, text=letra, font=("Arial", 14),
                width=4, height=2, bg="gray", fg="white",
                command=lambda letter=letra: ingresar_letra(letter)
                )
            boton.grid(row=fila, column=columna, padx=5, pady=5)
            letters_button[letra] = boton

    # Botones de "Enviar" y "Borrar"
    boton_enviar = tk.Button(
        frame_teclado, text="Enviar",
        command=hacer_intento, width=4, height=2,
        font=("Arial", 18), bg="green", fg="white")
    boton_enviar.grid(row=2, column=9, padx=5, pady=5)
    boton_borrar = tk.Button(
        frame_teclado, text="Borrar", command=borrar_virtual,
        width=4, height=2, font=("Arial", 18), bg="red", fg="white"
        )
    boton_borrar.grid(row=1, column=9, padx=5, pady=5)

    # Boton de salida del programa
    boton_salir = tk.Button(
        window, text="X", command=salir_programa, width=3,
        height=2, font=("Arial", 18), bg="red", fg="white"
        )
    boton_salir.place(x=10, y=10)

    # Botón para reiniciar el juego
    boton_jugar = tk.Button(
        window, text="Jugar de nuevo", font=("Arial", 18), 
        width=14, height=2, bg="green", fg="white",  
        command=reset_game)
    boton_jugar.grid(row=2, column=0, pady=20)

    # Cargar las palabras del archivo .txt
    LIST_POSSIBLE_WORDS = charge_words("words.txt")
    # Iniciar el juego
    play_game()

    # Mostrar la ventana
    window.mainloop()


# Ingresar letra desde el teclado virtual
def ingresar_letra(letra):
    widget_actual = letters_frames[attempts][0].focus_get()
    widget_actual.delete(0, tk.END)  # Borrar el contenido actual
    widget_actual.insert(0, letra.upper())  # Insertar el nuevo carácter
    next_widget = widget_actual.tk_focusNext()
    if next_widget:
        next_widget.focus()
