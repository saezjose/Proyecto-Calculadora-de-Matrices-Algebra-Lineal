def InitMatriz(CantidadFilas, CantidadColumnas):
    contador = 0
    NuevaMatriz = []
    for i in range(CantidadFilas):
        nuevafila = []
        for j in range(CantidadColumnas):
            letra = letra_por_indice(contador)
            nuevafila.append(letra)
            contador+=1
        NuevaMatriz.append(nuevafila)
    return NuevaMatriz

def letra_por_indice(n):
    resultado = ''
    while n >= 0:
        resultado = chr(n % 26 + ord('A')) + resultado
        n = n // 26 - 1
    return resultado

def ImprimirMatriz(matriz):
    for i in range(len(matriz)):
        print(matriz[i])
    print("\n")

def editar_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0

    for i in range(filas):
        for j in range(columnas):
            actual = matriz[i][j]
            while True:
                entrada = input(f"Elemento en [{i+1}][{j+1}] (actual: '{actual}'): ").strip()
                if entrada == "":
                    # Mantener el valor actual
                    break
                try:
                    nuevo_valor = float(entrada)
                    matriz[i][j] = nuevo_valor
                    break
                except ValueError:
                    print("Entrada inválida. Solo se permiten números reales.")


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
        raise ValueError("No se pueden multiplicar: columnas de Matriz_A ≠ filas de Matriz_B")

    filas_A = len(Matriz_A)
    columnas_B = len(Matriz_B[0])
    columnas_A = len(Matriz_A[0])
    
    #matriz tamaño M x R
    resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]

    # Realizamos la multiplicación
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



Matriz_A = InitMatriz(3, 3)
Matriz_B = InitMatriz(3, 3)

editar_matriz(Matriz_A)
editar_matriz(Matriz_B)

print("\nMatriz actualizada:")
ImprimirMatriz(Matriz_A) 
ImprimirMatriz(Matriz_B) 

suma = sumar_matrices(Matriz_A, Matriz_B)
resta = restar_matrices(Matriz_A,Matriz_B)
multiplicacion = multiplicar_matrices(Matriz_A, Matriz_B)
determinant = determinante(Matriz_A)

ImprimirMatriz(suma)
ImprimirMatriz(resta)
ImprimirMatriz(multiplicacion)
print(determinant)