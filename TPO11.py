import tkinter as tk
from Funciones import crear_ventana, cargar_palabras  # Importar la función para crear la ventana del juego

# Cargar la lista de palabras desde el archivo
LISTA_PALABRAS_POSIBLES = cargar_palabras('palabras.txt')

# Número máximo de intentos
INTENTOS_MAXIMO = 6

# Crear la ventana de instrucciones como la ventana principal
instrucciones_ventana = tk.Tk()  # Usamos Tk() en vez de Toplevel para evitar ventana en blanco
instrucciones_ventana.attributes("-fullscreen", True)  # Pantalla completa
instrucciones_ventana.config(bg="black")
instrucciones_ventana.title("Instrucciones")

# Función para mostrar las instrucciones con un ejemplo gráfico
def mostrar_instrucciones():
    frame_central = tk.Frame(instrucciones_ventana, bg='black')
    frame_central.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    # Asegurar que el contenido del frame central se centre
    instrucciones_ventana.grid_rowconfigure(0, weight=1)
    instrucciones_ventana.grid_columnconfigure(0, weight=1)
    
    # Título "LA PALABRA DEL DÍA" centrado
    titulo = tk.Label(frame_central, text="LA PALABRA DEL DÍA", font=("Arial", 24), bg="black", fg="white", anchor="center")
    titulo.grid(row=0, columnspan=5, pady=(0, 20))

    # Texto explicativo de las instrucciones centrado
    instrucciones_texto = (
        "El juego consiste en adivinar una palabra de 5 letras, \n"
        "para ello cuentas con 6 intentos. Después de cada \n"
        "intento se te informará qué letras se encuentran en \n"
        "la palabra. Si se encuentra alguna letra en la posición \n"
        "correcta se marcará en color VERDE. \n"
        "Las que formen parte de la palabra, pero están en la \n"
        "posición incorrecta, se mostrarán en color \n"
        "AMARILLO. Las que no estén dentro de la palabra se \n"
        "mostrarán en color ROJO. \n"
        "Los resultados se verían así: \n"
    )
    instrucciones_label = tk.Label(frame_central, text=instrucciones_texto, bg="black", fg="white", font=("Arial", 14), justify="left")
    instrucciones_label.grid(row=1, columnspan=5, pady=(0, 20), sticky="w")  # Sticky w (west) para que se alinee correctamente

    ejemplos = [
        (['T', 'O', 'R', 'N', 'O'], ['gray', 'gray', 'gray', 'gray', 'gray']),  # Ninguna letra pertenece
        (['A', 'C', 'E', 'R', 'O'], ['#FCD12A', '#FCD12A', 'gray', 'gray', 'gray']),  # Alguna letra en posición incorrecta
        (['C', 'A', 'R', 'T', 'A'], ['green', 'green', 'green', 'green', 'green'])  # Todo correcto
    ]

    # Crear el ejemplo gráfico centrado
    for i, (palabra, colores) in enumerate(ejemplos):
        for j, (letra, color) in enumerate(zip(palabra, colores)):
            cuadro = tk.Entry(frame_central, width=3, font=("Arial", 40), justify="center", bg=color, fg="white", relief="solid", highlightbackground="gray", highlightthickness=2)
            cuadro.insert(0, letra)
            cuadro.grid(row=i + 2, column=j, padx=10, pady=10)

    # Botón para empezar el juego centrado
    empezar_juego_btn = tk.Button(frame_central, text="Empezar Juego", command=lambda: [instrucciones_ventana.destroy(), iniciar_juego()], bg="green", fg="white", font=("Arial", 18))
    empezar_juego_btn.grid(row=5, columnspan=5, pady=20, sticky="n")

# Función para iniciar el juego (llama a la interfaz del archivo Funciones.py)
def iniciar_juego():
    crear_ventana()  # Llama a la función que crea la ventana principal del juego

# Mostrar las instrucciones antes de comenzar el juego
mostrar_instrucciones()

# Mantener la ventana de instrucciones abierta
instrucciones_ventana.mainloop()
