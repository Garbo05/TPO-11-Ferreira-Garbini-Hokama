import tkinter as tk
import random
from tkinter import messagebox

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
    secret_word = random.choice(LISTA_PALABRAS_POSIBLES).upper()  # Selecciona una palabra secreta al azar
    secret_word = remove_accents(secret_word)  # Elimina acentos de la palabra secreta
    intentos = 0  # Inicializa el número de intentos
    intento_bloqueado = False  # Permite realizar intentos
    # Limpia los cuadros de letras
    for i in range(6):
        for j in range(5):
            cuadros_letras[i][j].config(state="normal")
            cuadros_letras[i][j].delete(0, tk.END)  # Limpia las entradas
            cuadros_letras[i][j].config(state="normal", bg="black", fg="white", highlightbackground="gray", highlightthickness=2)  # Restablece el color de fondo
    # Reinicia los colores de las teclas
    for letra, boton in teclas_botones.items():
        boton.config(bg="gray", fg="white")

# Manejar el intento del usuario
def hacer_intento():
    global intentos, intento_bloqueado
    if intento_bloqueado:
        return  # Si el intento está bloqueado, no hace nada
    if intentos < 6:  # Solo permite hasta 6 intentos
        palabra = "".join(cuadros_letras[intentos][i].get().upper() for i in range(5))
        palabra = remove_accents(palabra)  # Elimina acentos de la palabra ingresada
        # Validar la palabra ingresada
        if not validate_guess(palabra) or not validate_palabra(LISTA_PALABRAS_POSIBLES, palabra):
            for i in range(5):
                cuadros_letras[intentos][i].delete(0, tk.END)  # Limpia las entradas
            cuadros_letras[intentos][0].focus()  # Enfoca el primer cuadro
            return
        
        resultado = [''] * 5
        diccionario_secreto = {letra: secret_word.count(letra) for letra in set(secret_word)}  # Cuenta las letras en la palabra secreta
        
        # Comprobar letras correctas (verde)
        for i in range(5):
            if palabra[i] == secret_word[i]:
                resultado[i] = 'green'
                diccionario_secreto[palabra[i]] -= 1  # Reduce el conteo de letras

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
            cuadros_letras[intentos][i].config(state="normal")  # Asegúrate de que el estado sea normal para cambiar color
            cuadros_letras[intentos][i].delete(0, tk.END)
            cuadros_letras[intentos][i].insert(0, palabra[i])
            cuadros_letras[intentos][i].config(bg=resultado[i])  # Establece el color de fondo
            # Evita más interacción (hace que no se pueda editar pero mantiene el color)
            cuadros_letras[intentos][i].bind("<Key>", lambda e: "break")  # Bloquea la entrada de teclas
            cuadros_letras[intentos][i].bind("<Button-1>", lambda e: "break")  # Bloquea clics del ratón
            cuadros_letras[intentos][i].config(takefocus=0)  # Previene el enfoque (no se puede tabular o hacer clic)

        intentos += 1  # Incrementa el número de intentos
        intento_bloqueado = False  # Permite nuevos intentos

        # Verifica si ganó o si se acabaron los intentos
        if palabra == secret_word:
            messagebox.showinfo("¡Felicidades!", f"La palabra secreta era {secret_word}.")
            return exit()
        elif intentos == 6:
            messagebox.showinfo("Fin del juego", f"Se acabaron los intentos. La palabra secreta era {secret_word}.")
            return exit()
        
        cuadros_letras[intentos][0].focus()  # Enfoca el primer cuadro del siguiente intento

# Manejar la entrada de teclado en el grid
def on_key_press(event, letra, intento):
    if event.char.isalpha() and len(event.widget.get()) == 0:  # Solo permite una letra
        event.widget.insert(tk.END, event.char.upper())
        next_widget = event.widget.tk_focusNext()  # Obtiene el siguiente widget
        if next_widget and letra != 4:  # Si no es el último cuadro
            next_widget.focus()  # Mueve el foco al siguiente cuadro
        return "break"
    elif event.keysym == "BackSpace":  # Maneja la tecla de retroceso
        if len(event.widget.get()) == 0:  # Si el cuadro está vacío
            if letra == 0:  # Si es el primer cuadro, no permitir moverse hacia atrás
                return "break"  # Impide cualquier acción si se está en el primer cuadro
            previous_widget = event.widget.tk_focusPrev()
            if previous_widget:
                previous_widget.focus()  # Enfoca el cuadro anterior
                previous_widget.delete(0, tk.END)  # Limpia el cuadro anterior
        else:
            event.widget.delete(0, tk.END)  # Limpia el cuadro actual
    elif event.keysym == 'Return':  # Si se presiona Enter
        hacer_intento()
    if not event.char.isalpha() and event.keysym not in ("BackSpace", "Return"):
        return "break"


# Función para limitar la entrada a un carácter
def validate_char(char):
    return len(char) <= 1

# Salir del programa

def salir_programa():
    return exit()

# Borrar letras en el cuadro actual
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

# Borrar la última letra ingresada
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
vcmd = (ventana.register(validate_char), '%P')  # Valida el número de caracteres

for intento in range(6):
    fila_cuadros = []
    for letra in range(5):
        cuadro = tk.Entry(frame_central, width=3, font=("Arial", 40), justify="center", bg="black", fg="white", relief="solid", highlightbackground="gray", highlightthickness=2,
                          validate="key", validatecommand=vcmd)  # Añade validación
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

# Boton de salida del programa
frame_esquina = tk.Frame(ventana, bg='black')
frame_esquina.grid(row=0,column=0,pady=0, padx=0)

# Botones de "Enviar" y "Borrar"
boton_enviar = tk.Button(frame_teclado, text="Enviar", command=hacer_intento, width=4, height=2, font=("Arial", 18), bg="green", fg="white")
boton_enviar.grid(row=2, column=9, padx=5, pady=5)
boton_borrar = tk.Button(frame_teclado, text="Borrar", command=borrar_virtual, width=4, height=2, font=("Arial", 18), bg="red", fg="white")
boton_borrar.grid(row=1, column=9, padx=5, pady=5)
# Boton de salida del programa
boton_salir = tk.Button(ventana, text="X", command=salir_programa, width=3, height=2, font=("Arial", 18), bg="red", fg="white")
boton_salir.place(x=10, y=10)  # Adjusted to place the button at the top-left corner

# Cargar palabras y comenzar el juego
LISTA_PALABRAS_POSIBLES = cargar_palabras('palabras.txt')
intentos = 0
play_game()
ventana.mainloop()