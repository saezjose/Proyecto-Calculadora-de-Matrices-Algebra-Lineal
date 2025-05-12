from fractions import Fraction

def verificar_matriz_valida(matriz):
    """Verifica si la matriz está completa (sin celdas vacías)."""
    for fila in matriz:
        if None in fila:  # Si hay valores vacíos
            return False
    return True

def convertir_a_fracciones(matriz):
    return [[Fraction(str(elem)) for elem in fila] for fila in matriz]


def sumar_matrices(Matriz_A, Matriz_B):

    if not verificar_matriz_valida(Matriz_A) or not verificar_matriz_valida(Matriz_B):
        raise ValueError("Algunas celdas de las matrices están vacías. Por favor, ingresa todos los valores.")
    
    if len(Matriz_A) != len(Matriz_B) or len(Matriz_A[0]) != len(Matriz_B[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")
    
    Matriz_A = convertir_a_fracciones(Matriz_A)
    Matriz_B = convertir_a_fracciones(Matriz_B)

    resultado = []
    for i in range(len(Matriz_A)):
        fila = []
        for j in range(len(Matriz_A[0])):
            suma = Matriz_A[i][j] + Matriz_B[i][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado

def restar_matrices(Matriz_A, Matriz_B):

    if not verificar_matriz_valida(Matriz_A) or not verificar_matriz_valida(Matriz_B):
        raise ValueError("Algunas celdas de las matrices está vacías. Por favor, ingresa todos los valores.")

    if len(Matriz_A) != len(Matriz_B) or len(Matriz_A[0]) != len(Matriz_B[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")
    
    Matriz_A = convertir_a_fracciones(Matriz_A)
    Matriz_B = convertir_a_fracciones(Matriz_B)

    resultado = []
    for i in range(len(Matriz_A)):
        fila = []
        for j in range(len(Matriz_A[0])):
            suma = Matriz_A[i][j] - Matriz_B[i][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado

def multiplicar_matrices(Matriz_A, Matriz_B):

    if not verificar_matriz_valida(Matriz_A) or not verificar_matriz_valida(Matriz_B):
        raise ValueError("Algunas celdas de las matrices está vacías. Por favor, ingresa todos los valores.")

    if len(Matriz_A[0]) != len(Matriz_B):
        raise ValueError("No se pueden multiplicar: columnas de A ≠ filas de B")
   
    Matriz_A = convertir_a_fracciones(Matriz_A)
    Matriz_B = convertir_a_fracciones(Matriz_B)

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
    if not verificar_matriz_valida(matriz):
        raise ValueError("Algunas celdas de las matrices están vacías. Por favor, ingresa todos los valores.")

    n = len(matriz)
    if any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada")

    # Convertir todos los elementos a fracción
    matriz = convertir_a_fracciones(matriz)

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

    if not verificar_matriz_valida(matriz):
        raise ValueError("Algunas celdas de las matrices están vacías. Por favor, ingresa todos los valores.")

    if not matriz or any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada y no vacía")
    
    matriz = convertir_a_fracciones(matriz)    
    
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
    if not verificar_matriz_valida(matriz):
        raise ValueError("Algunas celdas de las matrices están vacías. Por favor, ingresa todos los valores.")

    if not matriz or any(len(fila) != len(matriz) for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada y no vacía")

    n = len(matriz)

    matriz = convertir_a_fracciones(matriz)  
    
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

def gauss_jordan_sistema(coeficientes, terminos_independientes):
    from copy import deepcopy
    n = len(coeficientes)
    if any(len(fila) != n for fila in coeficientes):
        raise ValueError("La matriz de coeficientes debe ser cuadrada")

    coeficientes = convertir_a_fracciones(coeficientes)
    terminos_independientes = [Fraction(str(x)) for x in terminos_independientes]

    # Crear matriz aumentada
    augmented = [coeficientes[i] + [terminos_independientes[i]] for i in range(n)]

    for i in range(n):
        # Buscar pivote
        pivot = augmented[i][i]
        if pivot == 0:
            # Buscar fila para intercambiar
            for r in range(i+1, n):
                if augmented[r][i] != 0:
                    augmented[i], augmented[r] = augmented[r], augmented[i]
                    pivot = augmented[i][i]
                    break
            else:
                raise ValueError("El sistema no tiene solución única (pivote cero)")

        # Normalizar fila pivote
        for j in range(i, n+1):
            augmented[i][j] /= pivot

        # Eliminar otras filas
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(i, n+1):
                    augmented[k][j] -= factor * augmented[i][j]

    # Extraer soluciones
    solucion = [augmented[i][n] for i in range(n)]
    return solucion
