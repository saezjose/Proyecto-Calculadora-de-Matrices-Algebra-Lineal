import main
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Label

COLOR_FONDO = "#dcdcdc"
COLOR_PANEL = "#f4f4f4"
COLOR_BOTON = "#666666"
COLOR_BOTON_OPERACION = "#ff704d"
FUENTE = ("Helvetica", 10)

root = tk.Tk()
root.title("Calculadora de Matrices")
root.configure(bg=COLOR_FONDO)
root.resizable(False, False)


imagen_original = Image.open("Calculadora.png")
imagen_redimensionada = imagen_original.resize((350, 150))  # tamaño deseado
imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

# Crear un Label con la imagen
label_imagen = Label(root, image=imagen_tk)
label_imagen.image = imagen_tk  # guardar una referencia
label_imagen.place(x=460, y=220)

# Componentes de la interfaz
frame_resultado = tk.Frame(root, bg=COLOR_PANEL, relief="solid", bd=1)
frame_resultado.place(x=460, y=20, width=355, height=180)

resultado_texto = tk.Text(
    frame_resultado, height=10, width=40, bg=COLOR_PANEL,
    fg="#000000", font=("Courier New", 10), bd=0
)
resultado_texto.pack(expand=True, fill="both")

def mostrar_resultado(texto):
    resultado_texto.delete("1.0", tk.END)
    resultado_texto.insert(tk.END, texto)

# Matrices A y B
frame_matrices = tk.Frame(root, bg=COLOR_FONDO)
frame_matrices.place(x=20, y=20)

FILAS, COLUMNAS = 4, 4
entradas_A, entradas_B = [], []

tk.Label(frame_matrices, text="Matriz A", bg=COLOR_FONDO, font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=5)
tk.Label(frame_matrices, text="Matriz B", bg=COLOR_FONDO, font=("Helvetica", 12, "bold")).grid(row=0, column=4, columnspan=3, pady=5)

for i in range(FILAS):
    fila_A, fila_B = [], []
    for j in range(COLUMNAS):
        eA = tk.Entry(frame_matrices, width=5, justify="center", font=FUENTE)
        eA.grid(row=i+1, column=j, padx=4, pady=3)
        fila_A.append(eA)

        eB = tk.Entry(frame_matrices, width=5, justify="center", font=FUENTE)
        eB.grid(row=i+1, column=j+6, padx=4, pady=3)
        fila_B.append(eB)
    entradas_A.append(fila_A)
    entradas_B.append(fila_B)

# Funciones de operaciones
def obtener_matriz(entradas):
    matriz = []
    for fila in entradas:
        fila_valores = []
        for entrada in fila:
            valor = entrada.get()
            if valor == '':
                fila_valores.append(None)
            else:
                fila_valores.append(float(valor))
        matriz.append(fila_valores)

    # Eliminar filas vacías
    matriz = [fila for fila in matriz if any(x is not None for x in fila)]

    # Determinar columnas no vacías
    if matriz:
        columnas_validas = [i for i in range(len(matriz[0])) if any(fila[i] is not None for fila in matriz)]
        matriz = [[fila[i] for i in columnas_validas] for fila in matriz]

    return matriz

def matriz_a_string(matriz):
    return '\n'.join(['\t'.join(['' if x is None else str(round(x, 2)) for x in fila]) for fila in matriz])

# Botones de operaciones
frame_botones = tk.Frame(root, bg=COLOR_FONDO)
frame_botones.place(x=15, y=210)

def crear_boton(texto, comando, color=COLOR_BOTON):
    return tk.Button(
        frame_botones, text=texto, width=23, height=2,
        bg=color, fg="white", font=FUENTE, command=comando
    )

def operacion_sumar():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    try:
        resultado = main.sumar_matrices(A, B)
        mostrar_resultado("Suma A+B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_restar():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    try:
        resultado = main.restar_matrices(A, B)
        mostrar_resultado("Resta A-B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_multiplicar():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    try:
        resultado = main.multiplicar_matrices(A, B)
        mostrar_resultado("Multiplicación A×B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_inversa():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)

    resultado = ""

    # Intentar inversa de A
    try:
        inversa_A = main.matriz_inversa_gauss_jordan(A)
        resultado += "Inversa de A:\n" + matriz_a_string(inversa_A) + "\n\n"
    except Exception as e:
        resultado += f"Inversa de A: Error - {str(e)}\n\n"

    # Intentar inversa de B
    try:
        inversa_B = main.matriz_inversa_gauss_jordan(B)
        resultado += "Inversa de B:\n" + matriz_a_string(inversa_B)
    except Exception as e:
        resultado += f"Inversa de B: Error - {str(e)}"

    mostrar_resultado(resultado)


def operacion_determinante():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    try:
        det_A = main.determinante(A)
        det_B = main.determinante(B)
        resultado = f"Determinante de A: {det_A:.2f}\nDeterminante de B: {det_B:.2f}"
        mostrar_resultado(resultado)
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_LU():
    A = obtener_matriz(entradas_A)
    try:
        # Hacer una copia de A para no modificarla
        import copy
        A_copia = copy.deepcopy(A)
        L, U = main.factorizacion_LU(A_copia)
        texto = "Factorización LU de A:\n\nMatriz L:\n" + matriz_a_string(L) + "\n\nMatriz U:\n" + matriz_a_string(U)
        mostrar_resultado(texto)
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")


crear_boton("LU de A", operacion_LU).grid(row=2, column=1, padx=5, pady=5)
crear_boton("Sumar", operacion_sumar, COLOR_BOTON_OPERACION).grid(row=0, column=0, padx=5, pady=5)
crear_boton("Restar", operacion_restar, COLOR_BOTON_OPERACION).grid(row=0, column=1, padx=5, pady=5)
crear_boton("Multiplicar", operacion_multiplicar).grid(row=1, column=0, padx=5, pady=5)
crear_boton("Inversa ", operacion_inversa).grid(row=1, column=1, padx=5, pady=5)
crear_boton("Determinante ", operacion_determinante).grid(row=2, column=0, padx=5, pady=5)

root.geometry("850x400")
root.mainloop()

