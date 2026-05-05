# -*- coding: utf-8 -*-
from typing import List, Tuple, Optional# Vocabulario: A..Z => 0..25, ESPACIO => 26
CHAR_TO_VAL = {chr(ord('A') + i): i for i in range(26)}
CHAR_TO_VAL[' '] = 26# Valor a caracter
VAL_TO_CHAR = {v: k for k, v in CHAR_TO_VAL.items()}

def char_to_val(ch: str) -> int:
    ch = ch.upper()
    if ch in CHAR_TO_VAL:
        return CHAR_TO_VAL[ch]
    raise ValueError(f"Caracter no soportado: {ch}")

def val_to_char(v: int) -> str:
    v %= 27
    return VAL_TO_CHAR[v]

def limpiar_texto(texto: str) -> str:  # Mantener solo A-Z y espacio; convertir a mayÃºsculas
    res = []
    for c in texto:
        if c.upper() >= 'A' and c.upper() <= 'Z':
            res.append(c.upper())
        elif c == ' ':
            res.append(' ')     # ignorar otros caracteres
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
    E0 = calcular_E0(n, m) # Construir la secuencia de caracteres según la permutacion:
    # Primer paso: crear una lista de caracteres en el orden de lectura de posiciones
    chars = []
    for (r, c) in posiciones:
        ch = matriz[r][c]
        if ch is None:
            continue    # Asegurar que chars coincide con el texto filtrado y llenado (ya estÃ¡ filtrado)
        chars.append(ch)     # Aplicar cifrado carÃ¡cter a carÃ¡cter con E0 (no se indica que E0 cambie durante el proceso)
    cifrado = []
    for ch in chars:
        v = char_to_val(ch)
        v2 = (v + E0) % 27
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
    chars = list(texto_cifrado)  # Revertir: v = (v_cifrado - E0) mod 27
    descifrado = []
    for ch in chars:
        v = char_to_val(ch)
        v2 = (v - E0) % 27     # Ahora mapear de vuelta a texto en posiciones originales usando la permutaciÃ³n
        descifrado.append(val_to_char(v2))     # Construimos una matriz n x m con estos chars en el orden de posiciones


    matriz = [[None for _ in range(m)] for _ in range(n)]     # Colocamos en la misma secuencia de posiciones
    for idx, (r, c) in enumerate(posiciones):
        if idx < len(descifrado):
            matriz[r][c] = descifrado[idx]  # Extraemos el texto fila por fila, omitiendo None
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
    return n,m # Ejemplo de uso con el Caso 1 (Hola)

def siguiente_archivo(prefijo, extension=".txt"):
    i = 1
    while True:
        nombre = f"{prefijo}_{i}{extension}"
        try:
            with open(nombre, "r"):
                i += 1
        except FileNotFoundError:
            return nombre

def leer_archivo(nombre):#2. Leer archivo simple
    with open(nombre, "r", encoding="utf-8") as f:
        return f.read()

def guardar_archivo(nombre, contenido,posiciones): # 3. Guardar archivo
    with open(nombre, "w", encoding="utf-8") as f:
        f.write(contenido + "\n")
        f.write(posiciones)

def leer_cifrado(nombre):
    with open(nombre, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    cifrado = lineas[0].strip()
    pos_str = lineas[1].strip()
    posiciones = [(int(p[0]), int(p[1])) for p in pos_str.split('-')]
    return cifrado, posiciones

def extraer_posiciones(historia):
    import re
    nums = list(map(int, re.findall(r'\d', historia)))
    if len(nums) % 2 != 0:
        raise ValueError("Cantidad impar de nÃºmeros")
    return [(nums[i], nums[i+1]) for i in range(0, len(nums), 2)]

def ejemplo_case_1():
    texto = "Hola"
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

def posiciones_a_string(posiciones):
    return '-'.join(f"{r}{c}" for r, c in posiciones)

import json

def cargar_historias(ruta="historias.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def insertar_numeros(historia, posiciones):
    import random
    PALABRAS_RELLENO = ["dos", "tres", "cuatro"]
    numeros = [str(n) for tupla in posiciones for n in tupla]
    partes = historia.split("xxy")
    resultado = partes[0]
    i = 0
    for parte in partes[1:]:
        if i < len(numeros):
            resultado += numeros[i]
            i += 1
        else:
            resultado += random.choice(PALABRAS_RELLENO)
        resultado += parte
    return resultado

def generar_historia(historias, posiciones, nm):
    try: 
        import random
        PALABRAS_RELLENO = ["dos", "tres", "cuatro", "cinco", "seis"]
        claves = sorted(int(k) for k in historias.keys())
        historia_base=""
        clave_usada = None

        for k in claves:
            if nm <= k:
                print(f"miremos K.  {k}")
                print(f"miremos nm : {nm}")
                #historia_base=historias[str(k)][0]
                historia_base=random.choice(historias[str(k)])
                break
        else:
            raise ValueError("NO hay historia aedcuada.")
        print(f"EL conteo de palabras es: {historia_base.count("xxy")}")
        historia_final=insertar_numeros(historia_base, posiciones)
        return historia_final

    except ValueError:
        print("NO hay historia adecuada.")

def leer_cifrado_con_historia(nombre):
    with open(nombre, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    if len(lineas) < 2:
        raise ValueError("El archivo no tiene el formato correcto")
    cifrado = lineas[0].strip()
    historia = "".join(lineas[1:]).strip()  # por si la historia tiene varias lineas
    return cifrado, historia

def extraer_posiciones(historia):
    import re  # 1. sacar todos los digitos
    nums = list(map(int, re.findall(r'\d', historia)))  # 2. validar que sean pares
    if len(nums) % 2 != 0:
        raise ValueError("Cantidad de numeros invalida (debe ser par)")  # 3. agrupar en tuplas
    posiciones = [(nums[i], nums[i+1]) for i in range(0, len(nums), 2)]
    return posiciones

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Cifrar texto desde archivo")
        print("2. Descifrar texto desde archivo")
        print("3. Cifrar + usar historia (posiciones ocultas)")
        print("4. DesCifrar + usar historia (posiciones ocultas)")
        print("5. Salir")
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            texto = leer_archivo("texto_cifrar.txt")
            n,m = calc_tam(texto)   # aqui usas tu funciÃ³n
            cifrado, E0, posiciones = cifrar_texto(texto, n, m)
            pos2=posiciones_a_string(posiciones)
            nombre = siguiente_archivo("cifrado")
            guardar_archivo(nombre, cifrado, pos2)
            print(f"Cifrado guardado en {nombre}")
        elif opcion == "2":
            leer_cif, pos= leer_cifrado("texto_para_decifrar.txt")
            n,m = calc_tam(leer_cif)
            descifrado_n=descifrar_texto(leer_cif,n,m,pos)
            print(f"Texto decifrado_caso 2: {descifrado_n}")
            nombre = siguiente_archivo("des_cifrado")
            guardar_archivo(nombre, descifrado_n, "")

        elif opcion == "3":
            historias=cargar_historias()
            texto = leer_archivo("texto_cifrar.txt")
            n,m = calc_tam(texto)      # aqui usas tu funciÃ³n
            cifrado, E0, posiciones = cifrar_texto(texto, n, m)
            pos2=posiciones_a_string(posiciones)
            nombre = siguiente_archivo("cifrado_Historia")
            nm=n*m
            #print(f"miremos posiciones {posiciones}")
            historia_1=generar_historia(historias, posiciones, nm)
            historia_final=cifrado + "\n " + historia_1
            guardar_archivo(nombre, historia_final, "")
            print(f"Cifrado con historia guardado en {nombre}")
        elif opcion == "4":
            texto_cifradp, historia= leer_cifrado_con_historia("texto_para_decifrar_historia.txt")
            posiciones=extraer_posiciones(historia)
            #print(f"miremos posiciones {posiciones}")
            n,m = calc_tam(texto_cifradp)
            descifrado_n=descifrar_texto(texto_cifradp,n,m,posiciones)
            print(f"Texto descifrado es: {descifrado_n}")
        elif opcion == "5":
            break
        else:
            print("OpciÃ³n invÃ¡lida")

if __name__ == "__main__":# si se desea correr el ejemplo
    menu()
    #ejemplo_case_1()
    #ejemplo_case_2()
