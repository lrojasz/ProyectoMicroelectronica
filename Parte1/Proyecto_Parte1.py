# Importar librerias
import time
import sys

"""
Función micro_ucr_hash
Toma como entradas un bloque de 16 bits, un target, y el parámetro de DEBUG para imprimir datos de depuración. Devuelve el hash de 3 bytes correspondiente a la entrada.
"""
def micro_ucr_hash(bloque, target, DEBUG):
    # DEBUG: Imprimir bloque que entra a micro_ucr_hash
    if (DEBUG):
        print("Bloque que entra a micro_ucr_hash:", [hex(x) for x in bloque] )
    # Paso 2: inicializar 32 variables W (tamaño un byte)
    W = []
    for i in range(0,32):
        if (i <= 15):
            W.append(bloque[i])
        else:
            W.append(W[i-3] | W [i-9] ^ W[i-14])
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
        # Iteraciones 0-15
        if (i <= 15):
            k = 0x99
            x = a ^ b
        # Iteraciones 16-31
        else: 
            k = 0xa1
            x = a | b
        # Actualizar a, b y c
        a = b ^ c
        b = c << 4
        c = x + k + W[i]
        # Revisar overflow
        while(a > 0xff):
            a -= 256
        while(b > 0xff):
            b -= 256
        while(c > 0xff):
            c -= 256
        # Última iteración
        if (i == 31):
            H[0] = H[0] + a
            H[1] = H[1] + b
            H[2] = H[2] + c
        while(H[0] > 0xff):
            H[0] -= 256
        while(H[1] > 0xff):
            H[1] -= 256
        while(H[2] > 0xff):
            H[2] -= 256
        # DEBUG: Imprimir a, b y c internos
        if (DEBUG):
            print("a, b, c:", hex(a), hex(b), hex(c))
    # DEBUG: Imprimir Hash resultante
    if (DEBUG):
        print("Hash pre-retorno:", [hex(x) for x in H] )
    # Retornar
    return H

"""
Declaración de variables
"""
# Declarar 12 bytes iniciales t el nonce de 4 para pasar a micro_ucr_hash
bytes = (0x39, 0x7d, 0x9f, 0x2f, 0x40, 0xca, 0x9e, 0x6c, 0x6b, 0x1f, 0x33, 0x24)
nonce = (0xfd, 0xed, 0x87, 0x3c)
# Declarar target
target = 0x10

"""
Llamar micro_ucr_hash y medir tiempo de recorrido
"""
# Correr micro_ucr_hash (se envía bytes + nonce como entrada)
print("Datos de entrada:",[hex(x) for x in (bytes+nonce)])
t1 = time.time()
Hash = micro_ucr_hash(bytes+nonce, target, True)
t2 = time.time()
t3 = t2 - t1
# Imprimir hash resultante y tiempo de ejecución
print("Hash resultante:", [hex(x) for x in Hash] )
print("Tiempo de ejecución:",t3)
