import tkinter as tk
import random
from tkinter import messagebox
import importlib
import Funciones
import datetime

# Variables globales
cuadros_letras = []
teclas_botones = {}
intentos = 0
intento_bloqueado = False
LISTA_PALABRAS_POSIBLES = []
hora_actual = datetime.datetime.now()

# Función para reiniciar el módulo Funciones y el juego
def resetear_juego():
    global ventana
    ventana.destroy()
    importlib.reload(Funciones)  # Recarga todo el módulo Funciones
    Funciones.crear_ventana()  # Reinicia la ventana principal del juego


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
    global intentos, secret_word, cuadros_letras
    global teclas_botones, intento_bloqueado, LISTA_PALABRAS_POSIBLES
    secret_word = random.choice(LISTA_PALABRAS_POSIBLES).upper()
    secret_word = remove_accents(secret_word)  # Elimina acentos
    intentos = 0  # Inicializa el número de intentos
    intento_bloqueado = False  # Permite realizar intentos

    # Limpia los cuadros de letras
    for i in range(6):
        for j in range(5):
            cuadros_letras[i][j].config(state="normal")
            cuadros_letras[i][j].delete(0, tk.END)
            if hora_actual.hour >= 20 or hora_actual.hour < 6:
                cuadros_letras[i][j].config(
                    state="normal", bg="black",
                    fg="white", highlightbackground="gray", highlightthickness=2
                    )  # Restablece el color de fondo
            else:
                cuadros_letras[i][j].config(
                    state="normal", bg="white",
                    fg="black", highlightbackground="gray", highlightthickness=2
                    )  # Restablece el color de fondo
    # Reinicia los colores de las teclas
    for letra, boton in teclas_botones.items():
        boton.config(bg="gray", fg="white")


# Manejar el intento del usuario
def hacer_intento():
    global intentos, secret_word, cuadros_letras
    global teclas_botones, intento_bloqueado
    if intento_bloqueado:
        return  # Si el intento está bloqueado, no hace nada
    if intentos < 6:  # Solo permite hasta 6 intentos
        palabra = "".join(
            cuadros_letras[intentos][i].get().upper() for i in range(5)
            )
        palabra = remove_accents(palabra)
        # Validar la palabra ingresada
        if not validate_guess(palabra) or not validate_palabra(
                                            LISTA_PALABRAS_POSIBLES, palabra
                                            ):
            for i in range(5):
                cuadros_letras[intentos][i].delete(0, tk.END)
            cuadros_letras[intentos][0].focus()  # Enfoca el primer cuadro
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
            cuadros_letras[intentos][i].config(state="normal")
            cuadros_letras[intentos][i].delete(0, tk.END)
            cuadros_letras[intentos][i].insert(0, palabra[i])
            cuadros_letras[intentos][i].config(bg=resultado[i])
            cuadros_letras[intentos][i].bind("<Key>", lambda e: "break")
            cuadros_letras[intentos][i].bind("<Button-1>", lambda e: "break")
            cuadros_letras[intentos][i].config(takefocus=0)
        intentos += 1  # Incrementa el número de intentos
        intento_bloqueado = False  # Permite nuevos intentos
        # Verifica si ganó o si se acabaron los intentos
        if palabra == secret_word:
            messagebox.showinfo("¡Felicidades!", f"La palabra secreta era {secret_word}.")
            return
        elif intentos == 6:
            messagebox.showinfo("Fin del juego", f"Se acabaron los intentos. La palabra secreta era {secret_word}.")
            return
        cuadros_letras[intentos][0].focus()


# Botón para borrar la letra actual o la anterior
def borrar_letra():
    for i in range(4, -1, -1):
        if cuadros_letras[intentos][i].get():
            cuadros_letras[intentos][i].delete(0, tk.END)
            cuadros_letras[intentos][i].focus()
            break


# Manejar la entrada de teclado en el grid
def on_key_press(event, letra, intento):
    # Verificar si el intento corresponde al intento actual
    if intento != intentos:
        return 'break'  # Ignorar la entrada si no es el intento actual
    
    if event.char.isalpha() and len(event.widget.get()) == 0:
        event.widget.insert(tk.END, event.char.upper())
        next_widget = event.widget.tk_focusNext()
        if next_widget and letra != 4:  # Si no es el último cuadro
            next_widget.focus()  # Mueve el foco al siguiente cuadro
        return "break"
    elif event.keysym == "BackSpace":  # Maneja la tecla de retroceso
        if len(event.widget.get()) == 0:  # Si el cuadro está vacío
            if letra != 0:
                previous_widget = event.widget.tk_focusPrev()
                if previous_widget:
                    previous_widget.focus()  # Enfoca el cuadro anterior
                    previous_widget.delete(0, tk.END)  # Limpia el cuadro anterior
        else:
            event.widget.delete(0, tk.END)  # Limpia el cuadro actual
    elif event.keysym == 'Return':  # Si se presiona Enter
        hacer_intento()
    if not event.char.isalpha() and \
            event.keysym not in ("BackSpace", "Return"):
        return "break"


# Borrar la última letra ingresada
def borrar_virtual():
    global intento_bloqueado
    if intento_bloqueado:
        return
    for i in reversed(range(5)):
        if cuadros_letras[intentos][i].get() != "":
            cuadros_letras[intentos][i].delete(0, tk.END)
            return


def salir_programa():
    return exit()


def crear_ventana():
    global ventana, cuadros_letras, teclas_botones, LISTA_PALABRAS_POSIBLES
    ventana = tk.Tk()
    ventana.attributes("-fullscreen", True)  # Pantalla completa
    if hora_actual.hour >= 20 or hora_actual.hour < 6:
        ventana.config(bg='black')
    else:
        ventana.config(bg='white')
    ventana.title("Stringle")

    # Centrar los elementos de la interfaz
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(0, weight=1)
    if hora_actual.hour >= 20 or hora_actual.hour < 6:
        frame_central = tk.Frame(ventana, bg='black')
    else:
        frame_central = tk.Frame(ventana, bg='white')
    frame_central.grid(row=0, column=0, padx=20, pady=20)

    # Título del juego
    if hora_actual.hour >= 20 or hora_actual.hour < 6:
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
    cuadros_letras = []
    for intento in range(6):
        fila_cuadros = []
        for letra in range(5):
            if hora_actual.hour >= 20 or hora_actual.hour < 6:
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
        cuadros_letras.append(fila_cuadros)

    # Crear teclado virtual (teclas)
    if hora_actual.hour >= 20 or hora_actual.hour < 6:
        frame_teclado = tk.Frame(ventana, bg='black')
    else:
        frame_teclado = tk.Frame(ventana, bg='white')
    frame_teclado.grid(row=1, column=0, pady=20)


    letras_fila1 = "QWERTYUIOP"
    letras_fila2 = "ASDFGHJKLÑ"
    letras_fila3 = "ZXCVBNM"

    teclas_botones = {}  # Para almacenar los botones
    for fila, letras in enumerate([letras_fila1, letras_fila2, letras_fila3]):
        for columna, letra in enumerate(letras):
            boton = tk.Button(
                frame_teclado, text=letra, font=("Arial", 14),
                width=4, height=2, bg="gray", fg="white",
                command=lambda l=letra: ingresar_letra(l)
                )
            boton.grid(row=fila, column=columna, padx=5, pady=5)
            teclas_botones[letra] = boton

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
        ventana, text="X", command=salir_programa, width=3,
        height=2, font=("Arial", 18), bg="red", fg="white"
        )
    boton_salir.place(x=10, y=10)

    # Botón para reiniciar el juego
    boton_jugar = tk.Button(
        ventana, text="Jugar de nuevo", font=("Arial", 14),
        width=10, height=2, bg="green", fg="white",
        command=resetear_juego)
    boton_jugar.grid(row=2, column=0, pady=20)

    # Cargar las palabras del archivo .txt
    LISTA_PALABRAS_POSIBLES = cargar_palabras("palabras.txt")
    # Iniciar el juego
    play_game()

    # Mostrar la ventana
    ventana.mainloop()


# Ingresar letra desde el teclado virtual
def ingresar_letra(letra):
    widget_actual = cuadros_letras[intentos][0].focus_get()
    widget_actual.insert(tk.END, letra.upper())
    next_widget = widget_actual.tk_focusNext()
    if next_widget:
        next_widget.focus()
