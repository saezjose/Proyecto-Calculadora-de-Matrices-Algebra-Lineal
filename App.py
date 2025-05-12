import main
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Label
from fractions import Fraction

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
imagen_redimensionada = imagen_original.resize((350, 150))
imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

label_imagen = Label(root, image=imagen_tk)
label_imagen.image = imagen_tk
label_imagen.place(x=460, y=220)

# Resultado
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

# Matrices
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

# Obtener matriz segura
def obtener_matriz(entradas):
    matriz = []
    for fila in entradas:
        fila_valores = []
        for entrada in fila:
            valor = entrada.get().strip()  # Eliminamos espacios al principio/final
            if valor == '':
                fila_valores.append(None)
            else:
                try:
                    # Aceptar valores como 1/2, -3, 5 etc.
                    fraccion = Fraction(valor)
                    fila_valores.append(fraccion)
                except (ValueError, ZeroDivisionError):
                    mostrar_resultado(
                        f"Error: '{valor}' no es válido.\nUsa solo números enteros o fracciones como '3/4' o '-2'."
                    )
                    return None
        matriz.append(fila_valores)

    if not any(any(x is not None for x in fila) for fila in matriz):
        mostrar_resultado("Error: Ingresa al menos un número en la matriz.")
        return None

    matriz = [fila for fila in matriz if any(x is not None for x in fila)]
    if not matriz or not matriz[0]:
        return []

    columnas_validas = [i for i in range(len(matriz[0])) if any(fila[i] is not None for fila in matriz)]
    matriz = [[fila[i] for i in columnas_validas] for fila in matriz]

    return matriz

def limpiar_entradas():
    for fila in entradas_A + entradas_B:
        for entrada in fila:
            entrada.delete(0, tk.END)

def matriz_a_string(matriz):
    return '\n'.join(['\t'.join(['' if x is None else str(x) for x in fila]) for fila in matriz])

# Botones
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
    if A is None or B is None: return
    try:
        resultado = main.sumar_matrices(A, B)
        mostrar_resultado("Suma A+B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_restar():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    if A is None or B is None: return
    try:
        resultado = main.restar_matrices(A, B)
        mostrar_resultado("Resta A-B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_multiplicar():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    if A is None or B is None: return
    try:
        resultado = main.multiplicar_matrices(A, B)
        mostrar_resultado("Multiplicación A×B:\n" + matriz_a_string(resultado))
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_inversa():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    if A is None or B is None: return

    resultado = ""

    try:
        inversa_A = main.matriz_inversa_gauss_jordan(A)
        resultado += "Inversa de A:\n" + matriz_a_string(inversa_A) + "\n\n"
    except Exception as e:
        resultado += f"Inversa de A: Error - {str(e)}\n\n"

    try:
        inversa_B = main.matriz_inversa_gauss_jordan(B)
        resultado += "Inversa de B:\n" + matriz_a_string(inversa_B)
    except Exception as e:
        resultado += f"Inversa de B: Error - {str(e)}"

    mostrar_resultado(resultado)

def operacion_determinante():
    A = obtener_matriz(entradas_A)
    B = obtener_matriz(entradas_B)
    if A is None or B is None: return
    try:
        det_A = main.determinante(A)
        det_B = main.determinante(B)
        resultado = f"Determinante de A: {det_A}\nDeterminante de B: {det_B}"
        mostrar_resultado(resultado)
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

def operacion_LU():
    A = obtener_matriz(entradas_A)
    if A is None: return
    try:
        import copy
        A_copia = copy.deepcopy(A)
        L, U = main.factorizacion_LU(A_copia)
        texto = "Factorización LU de A:\n\nMatriz L:\n" + matriz_a_string(L) + "\n\nMatriz U:\n" + matriz_a_string(U)
        mostrar_resultado(texto)
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

# Crear botones
crear_boton("LU de A", operacion_LU).grid(row=2, column=1, padx=5, pady=5)
crear_boton("Sumar", operacion_sumar, COLOR_BOTON_OPERACION).grid(row=0, column=0, padx=5, pady=5)
crear_boton("Restar", operacion_restar, COLOR_BOTON_OPERACION).grid(row=0, column=1, padx=5, pady=5)
crear_boton("Multiplicar", operacion_multiplicar).grid(row=1, column=0, padx=5, pady=5)
crear_boton("Inversa ", operacion_inversa).grid(row=1, column=1, padx=5, pady=5)
crear_boton("Determinante ", operacion_determinante).grid(row=2, column=0, padx=5, pady=5)
crear_boton("Limpiar Entradas", limpiar_entradas, "#888888").grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.geometry("850x450")
root.mainloop()
