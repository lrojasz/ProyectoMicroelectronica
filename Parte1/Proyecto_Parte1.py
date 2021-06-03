# Importar librerias generales
import time
import sys
# Importar módulos
from sistema import sistema
from sistema_des import sistema_des

"""
Función Main
Función que contiene todo el código del main. Hace un nuevo sistema, con ciertos valores de bytes predeterminados, y obtiene las salidas correspondientes.
"""
def main():
    # Declaración de variables
    bytes = [0x61, 0x69, 0x63, 0x70, 0x21, 0x00, 0x00, 0x03, 0x17, 0x08, 0x00, 0xf3]
    target = 10
    DEBUG = False
    """
    Sistema optimizado en área
    """
    print("\nSistema optimizado en área:\n")
    # Crear nuevo sistema con los parámetros indicados
    system = sistema(bytes,target,DEBUG)
    # Imprimir información de entrada
    print("Bytes ingresados: ", [hex(x) for x in bytes])
    print("Target: ", target)
    # Enviar señal de inicio y obtener salidas del sistema
    print("Señal de Inicio")
    start_time = time.time()
    nonce, terminado = system.startSignal()
    end_time = time.time()
    # Imprimir salidas
    print("\nTermiando:", terminado)
    print("Nonce:", [hex(x) for x in nonce])
    # Imprimir tiempo de ejecución
    print("Tiempo de ejecución:",(end_time-start_time))
    """
    Sistema optimizado en desempeño
    """
    print("\n\nSistema optimizado en desempeño:\n")
    # Crear nuevo sistema con los parámetros indicados
    system_des = sistema_des(bytes,target,DEBUG)
    # Imprimir información de entrada
    print("Bytes ingresados: ", [hex(x) for x in bytes])
    print("Target: ", target)
    # Enviar señal de inicio y obtener salidas del sistema
    print("Señal de Inicio")
    start_time = time.time()
    nonce, terminado = system_des.startSignal()
    end_time = time.time()
    # Imprimir salidas
    print("\nTermiando:", terminado)
    print("Nonce:", [hex(x) for x in nonce])
    # Imprimir tiempo de ejecución
    print("Tiempo de ejecución:",(end_time-start_time))
"""
Se llama a la función main
"""
main()