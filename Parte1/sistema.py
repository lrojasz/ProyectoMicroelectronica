# Importar micro_ucr_hash
from micro_ucr_hash import micro_ucr_hash

"""
Clase sistema
Toma como entradas un bloque de 16 bits, y el parámetro de DEBUG para imprimir datos de depuración. Devuelve el hash de 3 bytes correspondiente a la entrada.
"""
class sistema:
    """
    Función __init__
    Método de inicialización para un sistema donde se pasan 12 bytes, un target y se declara el parámetro de DEBUG (todos tienen valores por defecto)
    """
    def __init__(self,bytes = [0x61, 0x69, 0x63, 0x70, 0x21, 0x00, 0x00, 0x03, 0x17, 0x08, 0x00, 0xf3],target = 10,DEBUG = False):
        # Declarar atributos bytes, target y DEBUG basado en parámetros dados, o los valores por defecto
        self.bytes = tuple(bytes)
        self.target = target
        self.DEBUG = DEBUG
        self.done = False
        self.__micro_ucr_hash = micro_ucr_hash()
        # DEBUG: imprimir nuevos parámetros y actualizar el debug de micro_ucr_hash
        if (DEBUG):
            print("\nDeclarando nuevo sistema en modo DEBUG.\nBytes:",[hex(x) for x in self.bytes])
            (self.__micro_ucr_hash).toggleDEBUG(DEBUG)
        # NO se busca el nonce hasta "la señal de inicio" startSignal
    """
    Función updateBytes
    Método que permite actualizar el valor de bytes
    """
    def updateBytes(self,bytes):
        self.bytes = tuple(bytes)
        self.done = False
    """
    Función updateTarget
    Método que permite actualizar el target
    """
    def updateTarget(self,target):
        self.target = target
        self.done = False
    """
    Función toggleDEBUG
    Método que permite actualizar el valor de DEBUG tanto del sistema como el módulo micro_ucr_hash interno
    """
    def toggleDEBUG(self,DEBUG):
        if(DEBUG):
            print("\nsistema en modo DEBUG.")
        else:
            print("\nsistema saliendo de modo DEBUG.")
        self.DEBUG = DEBUG
        (self.__micro_ucr_hash).toggleDEBUG(DEBUG)
        self.done = False
    """
    Función startSignal
    Método que permite pasar la señal de inicio y buscar el nonce. Devuelve las salidas del sistema.
    """
    def startSignal(self):
        self.__findNonce()
        return tuple(self.nonce), self.done
    """
    Función __findNonce
    Método que usa los 12 bytes indicados y hace un nonce válido que permite crear una salida en micro_ucr_hash cuyos primeros dos bytes sean menores a un target.
    """
    def __findNonce(self):
        # Inicializar valores necesarios para encontrar el nonce
        self.__setUp()
        # Iterar por los diferentes valores de nonce, actualizando el micro_ucr_hash en cada iteracion. Cuando se terminó, se levanta "terminado"
        self.__iterate()
        self.done = True
        # DEBUG: Al obtener un nonce válido se imprime ese valor, el target y el hash correspondiente
        if(self.DEBUG):
            print("Hash válido:",[hex(x) for x in self.hash])
            print("Nonce válido:",[hex(x) for x in self.nonce])
    """
    Función __setUp
    Método privado que inicializa atributos privados que van a ser necesarios para los cálculos de findNonce
    """
    def __setUp(self):
        # Declarar variables de nonce, validNonce y done
        self.nonce = [0x0, 0x0, 0x0, 0x0]
        self.__validNonce = False
        self.done = False
        # Imprimir primer nonce (todo 0s)
        if (self.DEBUG):
            print("Primer nonce determinado:",[hex(x) for x in self.nonce])
        # Actualizar micro_ucr_hash con nonce actual
        self.hash = (self.__micro_ucr_hash).update(self.bytes + tuple(self.nonce))
    """
    Función __nextNonce
    Método privado que obtiene el próximo nonce a probar (según método del contador)
    """
    def __nextNonce(self):
        # No es valido, revisar próximo nonce
        self.nonce[3] += 1
        # Revisar condición de rebase para todos los nonce
        for x in reversed(range(0,4)):
            # Caso especial, es el último nonce posible :(
            if (self.nonce[x] > 0xff) & (x == 0):
                self.nonce[x] = self.nonce[x] & 0xff
            # No es el último nonce posible, condicion de 'rebase'
            elif (self.nonce[x] > 0xff):
                self.nonce[x] = self.nonce[x] & 0xff
                self.nonce[x-1] += 1
        # Imprimir nuevo nonce
        if (self.DEBUG):
            print("Nuevo nonce determinado:",[hex(x) for x in self.nonce])
    """
    Función __iterate
    Método privado que itera por diferentes valores de nonce hasta que se obtiene uno válido, según el target
    """
    def __iterate(self):
        # Mientras no se encuentre nonce válido, aplicar micro_ucr_hash, revisar y si es necesario nonce++
        while (self.__validNonce == False):
            # Usar micro_ucr_hash para obtener el nuevo hash
            self.hash = (self.__micro_ucr_hash).update(self.bytes + tuple(self.nonce))
            # Si el hash es válido
            if ( (self.hash[0] <= self.target) & (self.hash[1] <= self.target) ):
                # DEBUG: Imprimir que se obtuvo un nonce válido
                if (self.DEBUG):
                    print("Nonce válido obtenido")
                # Condición de salida
                self.__validNonce = True
            # Si el hash no es válido
            else :
                # DEBUG: Imprimir que se obtuvo un nonce inválido
                if (self.DEBUG):
                    print("Nonce inválido")
                # Obtener nuevo nonce
                self.__nextNonce()
        # DEBUG: Imprimir "valid check" al salir de la iteración
        if (self.DEBUG):
            print ("Target:",self.target)
            print ("Prueba de validez:", hex(self.hash[0]),"y", hex(self.hash[1]),"<",self.target)
    