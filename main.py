def InitMatriz(CantidadFilas, CantidadColumnas):
    contador = 0
    NuevaMatriz = []
    for y in range(CantidadFilas):
        nuevafila = []
        for x in range(CantidadColumnas):
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

def editar_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0

    for i in range(filas):
        for j in range(columnas):
            actual = matriz[i][j]
            nuevo_valor = input(f"Elemento en [{i}][{j}] (actual: '{actual}'): ")
            if nuevo_valor.strip() != "":
                matriz[i][j] = nuevo_valor

def ImprimirMatriz(matriz):
    for fila in matriz:
        print(fila)


matriz = InitMatriz(3, 3)

ImprimirMatriz(matriz)

editar_matriz(matriz)

print("\nMatriz actualizada:")
ImprimirMatriz(matriz) 