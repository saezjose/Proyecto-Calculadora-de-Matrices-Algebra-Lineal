from fractions import Fraction

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
