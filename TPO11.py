import tkinter as tk
from Functions import create_window, load_words
import datetime

current_time = datetime.datetime.now()

# Cargar la lista de palabras desde el archivo
POSSIBLE_WORDS_LIST = load_words('words.txt')

# Número máximo de intentos
MAX_ATTEMPTS = 6

# Crear la ventana de instrucciones como la ventana principal
window_instructions = tk.Tk()
window_instructions.attributes("-fullscreen", True)  # Pantalla completa
if current_time.hour >= 20 or current_time.hour < 6:
    window_instructions.config(bg="black")
else:
    window_instructions.config(bg="white")
window_instructions.title("Instrucciones")

# Función para mostrar las instrucciones con un ejemplo gráfico


def show_instructions():
    if current_time.hour >= 20 or current_time.hour < 6:
        central_frame = tk.Frame(window_instructions, bg='black')
    else:
        central_frame = tk.Frame(window_instructions, bg='white')
    central_frame.grid(row=0, column=0, padx=20, pady=20)

    # Asegurar que el contenido del frame central se centre
    window_instructions.grid_rowconfigure(0, weight=1)
    window_instructions.grid_columnconfigure(0, weight=1)

    # Título "STRINGLE" centrado
    if current_time.hour >= 20 or current_time.hour < 6:
        title = tk.Label(
            central_frame, text="Bienvenido a STRINGLE!", font=("Arial", 24),
            bg="black", fg="white", anchor="center", justify='center'
            )
    else:
        title = tk.Label(
            central_frame, text="Bienvenido a STRINGLE!", font=("Arial", 24),
            bg="white", fg="black", anchor="center", justify='center'
            )
    title.grid(row=0, columnspan=5, pady=(0, 20))

    # Texto explicativo de las instrucciones centrado
    instructions_text = (
        "El juego consiste en adivinar una palabra de 5 letters, \n"
        "para ello cuentas con 6 intentos. Después de cada \n"
        "intento se te informará qué letters se encuentran en \n"
        "la palabra. Si se encuentra alguna letter en la posición \n"
        "correcta se marcará en color VERDE. \n"
        "Las que formen parte de la palabra, pero están en la \n"
        "posición incorrecta, se mostrarán en color \n"
        "AMARILLO. Las que no estén dentro de la palabra se \n"
        "mostrarán en color GRIS. \n"
        "Los resultados se verían así: \n"
    )
    if current_time.hour >= 20 or current_time.hour < 6:
        instructions_label = tk.Label(
            central_frame, text=instructions_text,
            bg="black", fg="white", font=("Arial", 14), justify="center"
            )
    else:
        instructions_label = tk.Label(
            central_frame, text=instructions_text,
            bg="white", fg="black", font=("Arial", 14), justify="center"
            )
    instructions_label.grid(row=1, columnspan=5, pady=(0, 20))

    # Ejemplo de colores
    examples = [
        (['T', 'O', 'R', 'N', 'O'],
            ['gray', 'gray', 'gray', 'gray', 'gray']),
        (['A', 'C', 'E', 'R', 'O'],
            ['#FCD12A', '#FCD12A', 'gray', 'gray', 'gray']),
        (['C', 'A', 'R', 'T', 'A'],
            ['green', 'green', 'green', 'green', 'green'])
    ]

    # Crear el ejemplo gráfico centrado
    for i, (word, colors) in enumerate(examples):
        for j, (letter, color) in enumerate(zip(word, colors)):
            frame = tk.Entry(
                central_frame, width=3, font=("Arial", 40), justify="center",
                fg="white", relief="solid", highlightbackground="gray",
                highlightthickness=2, disabledbackground=color,
                disabledforeground="white"
                )
            frame.insert(0, letter)
            frame.config(state="disabled")
            frame.grid(row=i + 2, column=j, padx=10, pady=10)

    # Botón para empezar el juego centrado
    start_game_btn = tk.Button(
        central_frame, text="Empezar Juego",
        command=start_game_handler,
        bg="green", fg="white", font=("Arial", 18)
        )
    start_game_btn.grid(row=5, columnspan=5, pady=20, sticky="n")


# Definir una función para manejar el evento del botón
def start_game_handler():
    window_instructions.destroy()
    start_game()


# Función para iniciar el juego (llama a la interfaz del archivo Funciones.py)
def start_game():
    create_window()


# Mostrar las instrucciones antes de comenzar el juego
show_instructions()


# Mantener la ventana de instrucciones abierta
window_instructions.mainloop()
