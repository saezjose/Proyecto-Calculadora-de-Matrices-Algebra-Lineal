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


def sumar_matrices(matriz1, matriz2):
    if len(matriz1) != len(matriz2) or len(matriz1[0]) != len(matriz2[0]):
        raise ValueError("Las matrices deben tener las mismas dimensiones")

    resultado = []
    for i in range(len(matriz1)):
        fila = []
        for j in range(len(matriz1[0])):
            suma = matriz1[i][j] + matriz2[i][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado


matriz = InitMatriz(3, 3)
matriz1 = InitMatriz(3, 3)

editar_matriz(matriz)
editar_matriz(matriz1)

print("\nMatriz actualizada:")
ImprimirMatriz(matriz) 
ImprimirMatriz(matriz1) 

suma = sumar_matrices(matriz, matriz1)

ImprimirMatriz(suma)