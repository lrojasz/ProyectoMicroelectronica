# Importar librerias
import time
import sys

"""
Función micro_ucr_hash
Toma como entradas un bloque de 16 bits, y el parámetro de DEBUG para imprimir datos de depuración. Devuelve el hash de 3 bytes correspondiente a la entrada.
"""
def micro_ucr_hash(bloque, DEBUG):
    # DEBUG: Imprimir bloque que entra a micro_ucr_hash
    if (DEBUG):
        print("Bloque que entra a micro_ucr_hash:", [hex(x) for x in bloque] )
    # Paso 2: inicializar 32 variables W (tamaño un byte)
    W = []
    for i in range(0,32):
        if (i <= 15):
            W.append(bloque[i])
        else:
            W.append((W[i-3] | W [i-9] ^ W[i-14]) & 0xff)
    # DEBUG: Imprimir 32 variables (lista)
    if (DEBUG):
        print("Lista de 32 variables:", [hex(x) for x in W])
    # Paso 3: Inicializar tres variables: H[0] = 0x01, H[1] = 0x89, H[2] = 0xfe
    H = [0x01, 0x89, 0xfe]
    a = H[0]
    b = H[1]
    c = H[2]
    # Paso 4: Iterar 32 veces sacando k y x.  
    for i in range(0,32):
        # Iteraciones 0-16
        if (i <= 16):
            k = 0x99
            x = ( a ^ b ) & 0xff
        # Iteraciones 17-31
        else: 
            k = 0xa1
            x = ( a | b) & 0xff
        # Actualizar a, b y c
        a = (b ^ c ) & 0xff
        b = (c << 4) & 0xff
        c = (x + k + W[i]) & 0xff
        # Última iteración
        if (i == 31):
            H[0] = (H[0] + a) & 0xff
            H[1] = (H[1] + b) & 0xff
            H[2] = (H[2] + c) & 0xff
        # DEBUG: Imprimir a, b y c internos
        if (DEBUG):
            print("a, b, c:", hex(a), hex(b), hex(c))
    # DEBUG: Imprimir Hash resultante
    if (DEBUG):
        print("Hash pre-retorno:", [hex(x) for x in H] )
    # Retornar
    return H


"""
Función sistema
Toma como entradas 12 bytes y hace un nonce válido que permite crear una salida en micro_ucr_hash cuyos primeros dos bytes sean menores a un target.
"""
def sistema(bytes, target, DEBUG):
    # Declarar variables locales
    nonce = [0x0, 0x0, 0x0, 0x0]
    validNonce = False
    if (DEBUG):
        print("Primer nonce determinado:",[hex(x) for x in nonce])
    # Mientras no se encuentre nonce válido, aplicar micro_ucr_hash, revisar y si es necesario nonce++
    while (validNonce == False):
        # Llamar micro_ucr_hash
        H = micro_ucr_hash(bytes+nonce,DEBUG)
        # Revisar H
        if ( (H[0] <= target) & (H[1] <= target) ):
            # Es valido, toca retornar
            if (DEBUG):
                print("Nonce válido obtenido")
            validNonce = True
            return H, nonce
        elif (DEBUG):
            print("Nonce inválido")
        # No es valido, revisar próximo nonce
        nonce[3] += 1
        # Revisar condición de rebase para todos los nonce
        for x in reversed(range(0,4)):
            # Caso especial, es el último nonce posible :(
            if (nonce[x] > 0xff) & (x == 0):
                nonce[x] = nonce[x] & 0xff
            # No es el último nonce posible, condicion de 'rebase'
            elif (nonce[x] > 0xff):
                nonce[x] = nonce[x] & 0xff
                nonce[x-1] += 1
        # Imprimir nuevo nonce
        if (DEBUG):
            print("Nuevo nonce determinado:",[hex(x) for x in nonce])
    # Se salió del while, retornar nonce y H
    return H, nonce

"""
Declaración de variables
"""
# Declarar 12 bytes iniciales t el nonce de 4 para pasar a micro_ucr_hash
"""
bytes = (0x39, 0x7d, 0x9f, 0x2f, 0x40, 0xca, 0x9e, 0x6c, 0x6b, 0x1f, 0x33, 0x24)
nonce = (0xfd, 0xed, 0x87, 0x3c)
bytes = (0xed, 0x18, 0xbe, 0x0f, 0x98, 0x4a, 0xe0, 0xe2, 0xe3, 0x12, 0x8e, 0xfe)
nonce = (0x0f, 0xa2, 0x34, 0x91)
"""
bytes = [0x61, 0x69, 0x63, 0x70, 0x21, 0x00, 0x00, 0x03, 0x17, 0x08, 0x00, 0xf3]
nonce1 = [0x00, 0x00, 0x07, 0x12]
# Declarar target
target = 10

"""
Llamar micro_ucr_hash y medir tiempo de recorrido
"""
# Correr micro_ucr_hash (se envía bytes + nonce como entrada)
print("Datos de entrada:",[hex(x) for x in (bytes+nonce1)])
t1 = time.time()
Hash1 = micro_ucr_hash(bytes+nonce1, False)
t2 = time.time()
t3 = t2 - t1
# Imprimir hash resultante y tiempo de ejecución
print("Hash resultante:", [hex(x) for x in Hash1] )
print("Tiempo de ejecución:",t3)

"""
Llamar sistema y medir tiempo de recorrido
"""
# Correr sistema (se envía bytes y el target)
print("\nDatos de entrada:",[hex(x) for x in (bytes)])
t1 = time.time()
Hash, nonce = sistema(bytes, target, False)
t2 = time.time()
t3 = t2 - t1
# Imprimir hash resultante, nonce resultante y tiempo de ejecución
print("Hash resultante:", [hex(x) for x in Hash] )
print("Nonce resultante:", [hex(x) for x in nonce] )
print("Tiempo de ejecución:",t3)
