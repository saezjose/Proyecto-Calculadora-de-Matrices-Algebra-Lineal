import tkinter as tk
from fractions import Fraction
from PIL import Image, ImageTk
from tkinter import Label



# ============================ FUNCIONES MATEMÁTICAS ============================
def sumar_matrices(Matriz_A, Matriz_B):
    if len(Matriz_A) != len(Matriz_B) or len(Matriz_A[0]) != len(Matriz_B[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")

    resultado = []
    for i in range(len(Matriz_A)):
        fila = []
        for j in range(len(Matriz_A[0])):
            suma = Matriz_A[i][j] + Matriz_B[i][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado

def restar_matrices(Matriz_A, Matriz_B):
    if len(Matriz_A) != len(Matriz_B) or len(Matriz_A[0]) != len(Matriz_B[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")

    resultado = []
    for i in range(len(Matriz_A)):
        fila = []
        for j in range(len(Matriz_A[0])):
            suma = Matriz_A[i][j] - Matriz_B[i][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado

def multiplicar_matrices(Matriz_A, Matriz_B):
    if len(Matriz_A[0]) != len(Matriz_B):
        raise ValueError("No se pueden multiplicar: columnas de A ≠ filas de B")

    filas_A = len(Matriz_A)
    columnas_B = len(Matriz_B[0])
    columnas_A = len(Matriz_A[0])
    
    resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_B):
            for k in range(columnas_A):
                resultado[i][j] += Matriz_A[i][k] * Matriz_B[k][j]
    return resultado

def determinante(matriz):
    n = len(matriz)
    if any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada")

    if n == 1:
        return matriz[0][0]

    if n == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    det = 0
    for col in range(n):
        signo = (-1) ** col
        cofactor = matriz[0][col]
        matrizreducida = submatriz(matriz, 0, col)
        det += signo * cofactor * determinante(matrizreducida)
    return det

def submatriz(matriz, fila_excluir, col_excluir):
    matrizreducida = []
    for i in range(len(matriz)):
        if i == fila_excluir:
            continue
        fila = []
        for j in range(len(matriz[i])):
            if j == col_excluir:
                continue
            fila.append(matriz[i][j])
        matrizreducida.append(fila)
    return matrizreducida


def matriz_inversa_gauss_jordan(matriz):
    n = len(matriz)

    if not matriz or any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada y no vacía")
    augmented = []
    for i in range(n):
        row = [Fraction(str(matriz[i][j])) for j in range(n)]
        for j in range(n):
            row.append(Fraction(1.0) if i == j else Fraction(0.0))
        augmented.append(row)

    for i in range(n):
        pivot = augmented[i][i]
        if pivot == 0:
            raise ValueError("Matriz no invertible (pivote cero)")
        for j in range(2 * n):
            augmented[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(2 * n):
                    augmented[k][j] -= factor * augmented[i][j]

    inversa = []
    for i in range(n):
        inversa.append(augmented[i][n:])

    return inversa


def factorizacion_LU(matriz):
    n = len(matriz)
    
    # Crear matrices L y U inicializadas con ceros
    L = [[0 for _ in range(n)] for _ in range(n)]
    U = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            U[i][j] = matriz[i][j]
        
        for j in range(i, n):
            if i == j:
                L[i][i] = 1 
            else:
                L[j][i] = matriz[j][i] / U[i][i]

        # Realizar eliminación de Gauss para ajustar la matriz U
        for j in range(i + 1, n):
            for k in range(i + 1, n):
                matriz[j][k] -= L[j][i] * U[i][k]

    return L, U


# ============================ INTERFAZ GRÁFICA ============================
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
        resultado = sumar_matrices(A, B)
        mostrar_resultado("Suma A+B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_restar():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    try:
        resultado = restar_matrices(A, B)
        mostrar_resultado("Resta A-B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_multiplicar():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    try:
        resultado = multiplicar_matrices(A, B)
        mostrar_resultado("Multiplicación A×B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_inversa():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)

    resultado = ""

    # Intentar inversa de A
    try:
        inversa_A = matriz_inversa_gauss_jordan(A)
        resultado += "Inversa de A:\n" + matriz_a_string(inversa_A) + "\n\n"
    except Exception as e:
        resultado += f"Inversa de A: Error - {str(e)}\n\n"

    # Intentar inversa de B
    try:
        inversa_B = matriz_inversa_gauss_jordan(B)
        resultado += "Inversa de B:\n" + matriz_a_string(inversa_B)
    except Exception as e:
        resultado += f"Inversa de B: Error - {str(e)}"

    mostrar_resultado(resultado)


def operacion_determinante():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    try:
        det_A = determinante(A)
        det_B = determinante(B)
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
        L, U = factorizacion_LU(A_copia)
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

