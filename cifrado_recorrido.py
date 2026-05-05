# -*- coding: utf-8 -*-
from typing import List, Tuple, Optional

# Vocabulario: A..Z => 0..25, ESPACIO => 26
CHAR_TO_VAL = {chr(ord('A') + i): i for i in range(26)}
CHAR_TO_VAL[' '] = 26
# Valor a caracter
VAL_TO_CHAR = {v: k for k, v in CHAR_TO_VAL.items()}

def char_to_val(ch: str) -> int:
    ch = ch.upper()
    if ch in CHAR_TO_VAL:
        return CHAR_TO_VAL[ch]
    raise ValueError(f"Caracter no soportado: {ch}")

def val_to_char(v: int) -> str:
    v %= 27
    return VAL_TO_CHAR[v]

def limpiar_texto(texto: str) -> str:
    # Mantener solo A-Z y espacio; convertir a mayÃºsculas
    res = []
    for c in texto:
        if c.upper() >= 'A' and c.upper() <= 'Z':
            res.append(c.upper())
        elif c == ' ':
            res.append(' ')
        # ignorar otros caracteres
    return ''.join(res)

def construir_matriz(texto: str, n: int, m: int) -> Tuple[List[List[Optional[str]]], List[Tuple[int,int]]]:
    """
    Crea una matriz n x m y llena con los caracteres del texto (izquierda a derecha, fila por fila).
    Las celdas no usadas quedan como None.
    Devuelve la matriz y la lista de posiciones usadas (en orden de llenado).
    """
    texto = limpiar_texto(texto)
    total = n * m
    filled = texto[:total]  # recorta si es necesario
    matriz = [[None for _ in range(m)] for _ in range(n)]
    pos = []
    idx = 0
    for i in range(n):
        for j in range(m):
            if idx < len(filled):
                matriz[i][j] = filled[idx]
                pos.append((i, j))
                idx += 1
            else:
                matriz[i][j] = None
    return matriz, pos

def permutacion_de_reordenamiento(matriz: List[List[Optional[str]]]) -> List[Tuple[int,int]]:
    import random
    """
    Genera la lista de posiciones de la matriz en el orden de lectura/ reordenamiento.
    Tomando fila por fila (izq->der, arriba->abajo) las celdas no vacÃ­as, se devuelve
    la secuencia de posiciones (fila, columna).
    """
    n = len(matriz)
    m = len(matriz)
    positions = []
    for i in range(n):
        for j in range(m):
            if matriz[i][j] is not None:
                positions.append((i, j))
    random.shuffle(positions)
    return positions

def calcular_E0(n: int, m: int) -> int:
    """
    E0 = (sum de filas) * (sum de columnas) * m * n
    Donde sum de filas = 0+1+...+(n-1) = n*(n-1)/2
    y sum de columnas = 0+1+...+(m-1) = m*(m-1)/2
    DespuÃ©s:
    E0 mod 27; si == 0 => E0 += 1
    """
    sum_filas = n * (n - 1) // 2
    sum_cols = m * (m - 1) // 2
    E0 = sum_filas * sum_cols * m * n
    if E0 % 27 == 0:
        E0 += 1
    return E0

def texto_a_indices(texto: str) -> List[int]:
    return [char_to_val(c) for c in texto]

def indices_a_texto(indices: List[int]) -> str:
    return ''.join(val_to_char(v) for v in indices)

def cifrar_texto(texto: str, n: int, m: int) -> Tuple[str, int, List[Tuple[int,int]]]:
    """
    Cifra el texto usando el algoritmo descrito.
    Devuelve: texto_cifrado, E0 utilizado, lista de posiciones de reordenamiento.
    """
    matriz, _ = construir_matriz(texto, n, m)
    posiciones = permutacion_de_reordenamiento(matriz)  # orden de llenado de caracteres vÃ¡lidos
    E0 = calcular_E0(n, m)
    #print(f"EL valir de E0 ES: {E0}")
    # Construir la secuencia de caracteres según la permutacion:
    # Primer paso: crear una lista de caracteres en el orden de lectura de posiciones
    chars = []
    for (r, c) in posiciones:
        ch = matriz[r][c]
        if ch is None:
            continue
        chars.append(ch)
    # Asegurar que chars coincide con el texto filtrado y llenado (ya estÃ¡ filtrado)
    # Aplicar cifrado carÃ¡cter a carÃ¡cter con E0 (no se indica que E0 cambie durante el proceso)
    cifrado = []
    for ch in chars:
        v = char_to_val(ch)
        #print(f"Veamos como cifra el texto, el caracter es: {v}")
        v2 = (v + E0) % 27
        #print(f"Veamos el resultado de v+E0 MOD 27: {v2}")
        cifrado.append(val_to_char(v2))
    texto_cifrado = ''.join(cifrado)

    return texto_cifrado, E0, posiciones

def descifrar_texto(texto_cifrado: str, n: int, m: int, posiciones: List[Tuple[int,int]]) -> str:
    """
    Descifra el texto cifrado, asumiendo la clave E0 calculada con la misma n,m.
    Requiere la lista de posiciones usadas para reconstruir el orden original.
    Devuelve el texto descifrado en el orden original de la matriz (sin reconstrucciÃ³n final).
    """
    E0 = calcular_E0(n, m)
    chars = list(texto_cifrado)
    # Revertir: v = (v_cifrado - E0) mod 27
    descifrado = []
    for ch in chars:
        v = char_to_val(ch)
        v2 = (v - E0) % 27
        descifrado.append(val_to_char(v2))
    # Ahora mapear de vuelta a texto en posiciones originales usando la permutaciÃ³n
    # Construimos una matriz n x m con estos chars en el orden de posiciones
    matriz = [[None for _ in range(m)] for _ in range(n)]
    # Colocamos en la misma secuencia de posiciones
    for idx, (r, c) in enumerate(posiciones):
        if idx < len(descifrado):
            matriz[r][c] = descifrado[idx]
    # Extraemos el texto fila por fila, omitiendo None
    texto_descifrado = []
    for i in range(n):
        for j in range(m):
            ch = matriz[i][j]
            if ch is not None:
                texto_descifrado.append(ch)
    return ''.join(texto_descifrado)


def calc_tam(texto:str):
    n,m=2,2
    texto=texto.upper()
    contador=0
    for c in texto:
        if('A' <= c<= 'Z') or c ==' ':
            contador+=1

    alto = False
    nn=False
    mm=False
    while not alto:
        if(n*m>=contador):
            alto=True
        else:
            if(not nn):
                n+=1
                nn=True
            if(not mm):
                m+=1
                mm=True
            else:
                nn= False
                mm=False

    #print(f"Revisemos la long de cont: {contador}")
    return n,m
# Ejemplo de uso con el Caso 1 (Hola)
def ejemplo_case_1():
    texto = "Hola"
    #n, m = 2,2  # tal como en el ejemplo
    n,m = calc_tam(texto)
    texto_cifrado, E0, posiciones = cifrar_texto(texto, n, m)
    print("Texto cifrado_1:", texto_cifrado)
    print("E0:", E0)
    print("Posiciones de permutacion_1:", posiciones)
    descifrado = descifrar_texto(texto_cifrado, n, m, posiciones)
    print("Descifrado (texto segun matriz):_1", descifrado)
    texto2="Hola mundo"
    n,m = calc_tam(texto2)
    texto_cifrado2, E0, posiciones = cifrar_texto(texto2, n, m)
    print("Texto cifrado_2:", texto_cifrado2)
    print("E0_2:", E0)
    print("Posiciones de permutacion_2:", posiciones)
    descifrado = descifrar_texto(texto_cifrado2, n, m, posiciones)
    print("Descifrado (texto segun matriz):_2", descifrado)

def ejemplo_case_2():
    texto_cifrado="EPLS"
    posiciones=[(1, 1), (1, 0), (0, 0), (0, 1)]
    n,m = calc_tam(texto_cifrado)
    print("Se calculara el decifrado de una frase cifrada.")
    descifrado_n=descifrar_texto(texto_cifrado,n,m,posiciones)
    print(f"Texto decifrado_caso 2: {descifrado_n}")



# si se desea correr el ejemplo
if __name__ == "__main__":
    ejemplo_case_1()
    ejemplo_case_2()

