"""
Clase micro_ucr_hash
Toma como entradas un bloque de 16 bits, y el parámetro de DEBUG para imprimir datos de depuración. Devuelve el hash de 3 bytes correspondiente a la entrada.
"""
class micro_ucr_hash:
    """
    Función __init__
    Método de inicialización para un micro_ucr_hash donde se pasa un bloque y se declara el parámetro de DEBUG (tienen valores por defecto)
    """
    def __init__(self, DEBUG = False, bloque = [0x61, 0x69, 0x63, 0x70, 0x21, 0x00, 0x00, 0x03, 0x17, 0x08, 0x00, 0xf3, 0x00, 0x00, 0x07, 0x12]):
        # Declarar atributo DEBUG basado en parámetros dados, o los valores por defecto
        self.bloque = (tuple(bloque))
        self.DEBUG = DEBUG
        # DEBUG: imprimir nuevos parámetros
        if (DEBUG):
            print("\nDeclarando nuevo micro_ucr_hash en modo DEBUG.\nBloque:",[hex(x) for x in self.bloque])
        # Llamar a getHash para obtener el hash correcto.
        self.__getHash()
    """
    Función toggleDEBUG
    Método que permite actualizar el valor de DEBUG
    """
    def toggleDEBUG(self,DEBUG):
        if(DEBUG):
            print("\nmicro_ucr_hash en modo DEBUG.")
        else:
            print("\nmicro_ucr_hash saliendo de modo DEBUG.")
        self.DEBUG = DEBUG
    """
    Función update
    Este método actualiza el valor del bloque y consiguientemente obtiene un nuevo hash. Se retorna el nuevo valor de hash.
    """
    def update(self,bloque):
        # Se busca actualizar el valor del bloque que se está pasando
        self.bloque = tuple(bloque)
        # DEBUG: imprimir nuevos parámetros
        if (self.DEBUG):
            print("\nNuevo bloque:",[hex(x) for x in self.bloque])
        # Por lo tanto, se requiere calcular un nuevo hash
        self.__getHash()
        # Retornar nuevo valor de hash
        return self.hash
    """
    Función __getHash
    Método privado que obtiene el hash resultante del bloque que se pasa como parámetro 
    """
    def __getHash(self):
        # DEBUG: Imprimir bloque que entra a micro_ucr_hash
        if (self.DEBUG):
            print("\nObteniendo hash resultante con getHash()")
        # Declarar atributos privados para el cálculo del hash
        self.__setUp()
        # Iterar 32 veces para obtener una función hash válida
        H = self.__iterate()
        # DEBUG: Imprimir Hash resultante
        if (self.DEBUG):
            print("Guardando hash resultante:", [hex(x) for x in H] )
        # Guardar el H como un tuple (no modificable) en self.hash
        self.hash = tuple(H)
    """
    Función __setUp
    Método privado que inicializa atributos privados
    """
    def __setUp(self):
        # Inicializar las 32 variables W
        self.__getW()
        # Inicializar los valores de a, b y c
        self.__a = 0x01
        self.__b = 0x89
        self.__c = 0xfe
    """
    Función __getW
    Método privado que obtiene las 32 variables W que se necesitan para realizar cálculos
    """
    def __getW(self):
        # Inicializar 32 variables W (tamaño un byte)
        W = []
        for i in range(0,15):
            if (i <= 15):
                W.append(self.bloque[i])
            else:
                W.append((W[i-3] | W [i-9] ^ W[i-14]) & 0xff)
        for i in range(15,32):
            if (i <= 15):
                W.append(self.bloque[i])
            else:
                W.append((W[i-3] | W [i-9] ^ W[i-14]) & 0xff)
        # DEBUG: Imprimir 32 variables (lista)
        if (self.DEBUG):
            print("Lista de 32 variables:", [hex(x) for x in W])
        # Declarar W como tupla y almacenar
        self.__W = tuple(W)
    """
    Función __updateKX
    Método privado que actualiza los valores de k y x dependiendo de a, b y el número de iteraciones
    """
    def __updateKX(self,i):
        # Iteraciones 0-16
        if (i <= 16):
            self.__k = 0x99
            self.__x = ( self.__a ^ self.__b ) & 0xff
        # Iteraciones 17-31
        else: 
            self.__k = 0xa1
            self.__x = ( self.__a | self.__b) & 0xff
    """
    Función __updateABC
    Método privado que actualiza los valores de a, b y c dependiendo de k, x y del número de iteraciones
    """
    def __updateABC(self,i):
        # Actualizar los valores de a, b y c
        self.__a = (self.__b ^ self.__c ) & 0xff
        self.__b = (self.__c << 4) & 0xff
        self.__c = (self.__x + self.__k + self.__W[i]) & 0xff
        # DEBUG: Imprimir a, b y c internos
        if (self.DEBUG):
            print("Iteración #", i, "  \ta, b, c:", hex(self.__a), hex(self.__b), hex(self.__c))
    """
    Función __iterate
    Método privado que indica lo que tiene que suceder en las 32 iteraciones necesarias para obtener el hash
    """
    def __iterate(self):
        # Inicializar tres variables H
        H = [0x01, 0x89, 0xfe]
        # Iterar 32 veces
        # Construcción de hash 
        for i in range(0,15):
            # Actualizar los valores de k,x y después a,b,c
            self.__updateKX(i)
            self.__updateABC(i)
        for i in range(15,32):
            # Actualizar los valores de k,x y después a,b,c
            self.__updateKX(i)
            self.__updateABC(i)
            # Última iteración
            if (i == 31):
                H[0] = (H[0] + self.__a) & 0xff
                H[1] = (H[1] + self.__b) & 0xff
                H[2] = (H[2] + self.__c) & 0xff
        # Cuando ya se terminó de iterar, se devuelve el valor del hash
        return H