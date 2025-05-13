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
    text_ecuaciones.delete("1.0", tk.END)

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

    resultado = ""

    if A:
        try:
            inversa_A = main.matriz_inversa_gauss_jordan(A)
            resultado += "Inversa de A:\n" + matriz_a_string(inversa_A) + "\n\n"
        except Exception as e:
            resultado += f"Inversa de A: Error - {str(e)}\n\n"

    if B:
        try:
            inversa_B = main.matriz_inversa_gauss_jordan(B)
            resultado += "Inversa de B:\n" + matriz_a_string(inversa_B)
        except Exception as e:
            resultado += f"Inversa de B: Error - {str(e)}"

    if not A and not B:
        mostrar_resultado("Error: Ingresa al menos una matriz para calcular la inversa.")
        return

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

# Label para ecuaciones
label_ecuaciones = tk.Label(frame_botones, text="Ecuaciones (una por línea, hasta 4 incógnitas: X Y Z W):", bg=COLOR_FONDO, font=FUENTE)
label_ecuaciones.grid(row=4, column=0, columnspan=2, pady=(10, 0))

# Text widget para ingresar ecuaciones
text_ecuaciones = tk.Text(frame_botones, height=6, width=50, font=FUENTE)
text_ecuaciones.grid(row=5, column=0, columnspan=2, pady=5)

def parsear_ecuaciones(texto):
    import re
    lineas = texto.strip().split('\n')
    if len(lineas) == 0 or len(lineas) > 4:
        raise ValueError("Ingresa entre 1 y 4 ecuaciones.")
    
    # Variables permitidas en orden
    variables_permitidas = ['x', 'y', 'z', 'w']
    
    # Detectar variables usadas en las ecuaciones (solo x,y,z,w)
    variables_usadas = []
    for var in variables_permitidas:
        # Use regex to find variable as a letter possibly preceded by + or - and optional spaces, case-insensitive
        pattern_var = re.compile(re.escape(var), re.IGNORECASE)
        if any(pattern_var.search(linea) for linea in lineas):
            variables_usadas.append(var)
    
    if len(variables_usadas) == 0:
        raise ValueError("No se detectaron variables válidas (X, Y, Z, W).")
    if len(variables_usadas) > 4:
        raise ValueError("Solo se permiten hasta 4 variables (X, Y, Z, W).")
    if len(lineas) != len(variables_usadas):
        raise ValueError("El número de ecuaciones debe ser igual al número de variables detectadas.")
    
    coeficientes = []
    terminos = []

    for linea in lineas:
        # Separar términos y término independiente
        if '=' not in linea:
            raise ValueError("Cada ecuación debe contener un signo '='.")
        izquierda, derecha = linea.split('=')
        derecha = derecha.strip()
        izquierda = izquierda.strip()

        coef = [0] * len(variables_usadas)

        # Buscar coeficientes para cada variable usada
        for i, var in enumerate(variables_usadas):
            pattern = re.compile(r'([+-]?\s*\d*\/?\d*)\s*' + re.escape(var), re.IGNORECASE)
            matches = pattern.findall(izquierda)
            total_coef = 0
            for match in matches:
                coef_str = match.replace(' ', '')
                if coef_str in ['', '+', '-']:
                    coef_str += '1'
                try:
                    total_coef += float(Fraction(coef_str))
                except Exception:
                    raise ValueError(f"Coeficiente inválido: {coef_str}")
            coef[i] = total_coef

        # Detectar términos constantes en el lado izquierdo (sin variables)
        # Remover términos con variables para encontrar constantes
        izquierda_sin_vars = izquierda
        for var in variables_usadas:
            izquierda_sin_vars = re.sub(r'([+-]?\s*\d*\/?\d*)\s*' + re.escape(var), '', izquierda_sin_vars, flags=re.IGNORECASE)
        # Buscar constantes en izquierda_sin_vars
        constantes = re.findall(r'([+-]?\s*\d+\/?\d*)', izquierda_sin_vars)
        suma_constantes = 0
        for c in constantes:
            c_str = c.replace(' ', '')
            try:
                suma_constantes += float(Fraction(c_str))
            except Exception:
                raise ValueError(f"Término constante inválido: {c_str}")

        # Ajustar término independiente moviendo constantes al lado derecho con signo opuesto
        try:
            terminos.append(float(Fraction(derecha)) - suma_constantes)
        except Exception:
            raise ValueError(f"Término independiente inválido: {derecha}")

        coeficientes.append(coef)

    return coeficientes, terminos, variables_usadas

def resolver_sistema():
    texto = text_ecuaciones.get("1.0", tk.END)
    try:
        coef, term, variables_usadas = parsear_ecuaciones(texto)
        solucion = main.gauss_jordan_sistema(coef, term)
        resultado = "Solución:\n"
        for i, val in enumerate(solucion):
            resultado += f"{variables_usadas[i]} = {val}\n"
        mostrar_resultado(resultado)
    except Exception as e:
        mostrar_resultado(f"Error: {str(e)}")

crear_boton("Resolver Sistema", resolver_sistema, "#4CAF50").grid(row=6, column=0, columnspan=2, pady=10)

root.geometry("850x650")
root.mainloop()
