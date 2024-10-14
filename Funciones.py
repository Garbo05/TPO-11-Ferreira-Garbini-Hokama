import tkinter as tk
import random
from tkinter import messagebox
from colorama import init

# Inicializa colorama (para la consola, aunque aquí no es relevante en GUI)
init(autoreset=True)

# Cargar palabras desde un archivo .txt
def cargar_palabras(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        palabras = [linea.strip() for linea in f.readlines()]
    return palabras

# Elimina los acentos de una palabra
def remove_accents(word):
    diccionario_tildes = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
    }
    return ''.join(diccionario_tildes.get(letra, letra) for letra in word)

# Verifica que la palabra ingresada sea válida
def validate_guess(word):
    return len(word) == 5 and word.isalpha()

# Verifica si la palabra está en la lista de palabras posibles
def validate_palabra(palabras, word):
    word = remove_accents(word)
    return word in palabras

# Jugar el juego
def play_game():
    global intentos, secret_word, cuadros_letras, teclas_botones, intento_bloqueado
    secret_word = random.choice(LISTA_PALABRAS_POSIBLES).upper()
    secret_word = remove_accents(secret_word)
    intentos = 0
    intento_bloqueado = False
    for i in range(6):
        for j in range(5):
            cuadros_letras[i][j].config(state="normal")
            cuadros_letras[i][j].delete(0, tk.END)  # Limpia las entradas
            cuadros_letras[i][j].config(state="normal", bg="black", fg="white", highlightbackground="gray", highlightthickness=2)  # Reset background color
    # Reiniciar colores de las teclas
    for letra, boton in teclas_botones.items():
        boton.config(bg="gray", fg="white")

def hacer_intento():
    global intentos, intento_bloqueado
    if intento_bloqueado:
        return
    if intentos < 6:
        palabra = "".join(cuadros_letras[intentos][i].get().upper() for i in range(5))
        palabra = remove_accents(palabra)

        # Validar la palabra ingresada
        if not validate_guess(palabra) or not validate_palabra(LISTA_PALABRAS_POSIBLES, palabra):
            for i in range(5):
                cuadros_letras[intentos][i].delete(0, tk.END)  # Limpia las entradas
            cuadros_letras[intentos][0].focus()
            return

        resultado = [''] * 5
        diccionario_secreto = {letra: secret_word.count(letra) for letra in set(secret_word)}

        # Comprobar letras correctas (verde)
        for i in range(5):
            if palabra[i] == secret_word[i]:
                resultado[i] = 'green'
                diccionario_secreto[palabra[i]] -= 1

        # Comprobar letras incorrectas (amarillo y gris)
        for i in range(5):
            if resultado[i] == '':
                if palabra[i] in secret_word and diccionario_secreto[palabra[i]] > 0:
                    resultado[i] = 'yellow'
                    diccionario_secreto[palabra[i]] -= 1
                else:
                    resultado[i] = 'gray'

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
        intento_bloqueado = False
        if palabra == secret_word:
            messagebox.showinfo("¡Felicidades!", f"La palabra secreta era {secret_word}.")
            return
        elif intentos == 6:
            messagebox.showinfo("Fin del juego", f"Se acabaron los intentos. La palabra secreta era {secret_word}.")
            return
        cuadros_letras[intentos][0].focus()

# Manejar la entrada de teclado en el grid
def on_key_press(event, letra, intento):
    if event.char.isalpha() and len(event.widget.get()) == 0:  # Solo permite una letra
        event.widget.insert(tk.END, event.char.upper())
        next_widget = event.widget.tk_focusNext()
        if next_widget and letra != 4:
            next_widget.focus()  # Mover el foco al siguiente cuadro
        return "break"
    elif event.keysym == "BackSpace":
        if len(event.widget.get()) == 0:
            previous_widget = event.widget.tk_focusPrev()
            if previous_widget:
                previous_widget.focus()
                previous_widget.delete(0, tk.END)
        else:
            event.widget.delete(0, tk.END)
    elif event.keysym == 'Return':
        hacer_intento()
    if not event.char.isalpha() and event.keysym not in ("BackSpace", "Return"):
        return "break"

def borrar_letras():
    for i in range(5):
        cuadros_letras[intentos][i].delete(0, tk.END)

# Simulación del teclado virtual
def ingresar_letra(letra):
    global intento_bloqueado
    if intento_bloqueado:
        return

    # Buscar la casilla vacía
    for i in range(5):
        if cuadros_letras[intentos][i].get() == "":
            cuadros_letras[intentos][i].insert(tk.END, letra)
            return

def borrar_virtual():
    global intento_bloqueado
    if intento_bloqueado:
        return

    for i in reversed(range(5)):
        if cuadros_letras[intentos][i].get() != "":
            cuadros_letras[intentos][i].delete(0, tk.END)
            return

# Configuración de la ventana
ventana = tk.Tk()
ventana.attributes("-fullscreen", True)  # Pantalla completa
ventana.config(bg='black')
ventana.title("Stringle")

# Centrar los elementos de la interfaz
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_rowconfigure(0, weight=1)

frame_central = tk.Frame(ventana, bg='black')
frame_central.grid(row=0, column=0, padx=20, pady=20)

# Título del juego
titulo = tk.Label(frame_central, text="LA PALABRA DEL DÍA", font=("Arial", 24), bg="black", fg="white")
titulo.grid(row=0, columnspan=5, pady=(0, 20))

# Crear el grid de cuadros de letras
cuadros_letras = []
for intento in range(6):
    fila_cuadros = []
    for letra in range(5):
        cuadro = tk.Entry(frame_central, width=3, font=("Arial", 40), justify="center", bg="black", fg="white", relief="solid", highlightbackground="gray", highlightthickness=2)
        cuadro.grid(row=intento+1, column=letra, padx=10, pady=10)
        cuadro.bind("<Key>", lambda event, l=letra, i=intento: on_key_press(event, l, i))
        fila_cuadros.append(cuadro)
    cuadros_letras.append(fila_cuadros)

# Crear el teclado virtual
frame_teclado = tk.Frame(frame_central, bg='black')
frame_teclado.grid(row=7, columnspan=5, pady=20)

teclas_botones = {}
letras_teclado = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

# Crear botones del teclado virtual
for fila_index, fila_teclas in enumerate(letras_teclado):
    for col_index, letra in enumerate(fila_teclas):
        boton = tk.Button(frame_teclado, text=letra, command=lambda l=letra: ingresar_letra(l), width=4, height=2,
                        font=("Arial", 18), bg="gray", fg="white")
        boton.grid(row=fila_index, column=col_index, padx=5, pady=5)
        teclas_botones[letra] = boton

# Botones de "Enviar" y "Borrar"
boton_enviar = tk.Button(frame_teclado, text="Enviar", command=hacer_intento, width=4, height=2, font=("Arial", 18), bg="green", fg="white")
boton_enviar.grid(row=2, column=9, padx=5, pady=5)

boton_borrar = tk.Button(frame_teclado, text="Borrar", command=borrar_virtual, width=4, height=2, font=("Arial", 18), bg="red", fg="white")
boton_borrar.grid(row=1, column=9, padx=5, pady=5)

# Cargar palabras y comenzar el juego
LISTA_PALABRAS_POSIBLES = cargar_palabras('palabras.txt')
intentos = 0
play_game()

ventana.mainloop()
