'''
Importar bibliotecas
'''
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt

'''
Declarar variables locales
'''
# Variables generales
archivo = 'system.def'
count = 0
DEBUG = True
# Strings a utilizar
temp = ""
coordenadas = ""
basura = "" 
xMax = ""
# Arreglo de listas
componentes = []
metales = []

'''
Lectura de archivo
'''
# Mensaje de inicio, caso DEBUG
if (DEBUG):
    print("\n\tDENSIDAD DE CELDAS:\n\n")
# Usando readline(), leer archivo línea por línea
file = open(archivo, 'r')

# Iterar 'infinitamente' (hasta que el archivo termine, se sale con break)
EOF = False
SOC = False
SON = False
while EOF == False:
    # Incrementar contador de líneas de archivo
    count += 1
    # Obtener próxima línea
    line = file.readline()

    # Sacar xMax
    if 'DIEAREA' in line:
        # Sacar x máximo
        basura,temp = line.split(' ) ( ',1)
        xMax,basura = temp.split(' ',1)
        xMax = xMax.replace(" ","")
        # DEBUG: Imprimir mensaje y línea
        if (DEBUG): 
            print ('\n[ ',xMax,']\tx máximo encontrado\n')
    # Analizar si se llegó a "FIXED"
    elif 'SPECIALNETS' in line:
        # DEBUG: Imprimir mensaje y línea
        if (DEBUG): 
            print ('\nMetales especiales encontrados, terminar análisis\n')
        # Declarar EOF (no importa el resto del archivo)
        EOF = True
    # Analizar si se llegó a "FIXED"
    elif 'NETS' in line:
        # DEBUG: Imprimir mensaje y línea
        if (DEBUG): 
            print ('\nMetales encontrados, iniciando análisis\n')
        # Declarar EOF (no importa el resto del archivo)
        SON = True
    # Analizar la línea a ver si se finalizó la parte de componentes
    elif 'END COMPONENTS' in line:
        # DEBUG: Imprimir mensaje y línea
        if (DEBUG): 
            print("Línea{}: {}".format(count, line.strip()))
            print ('\nFin de COMPONENTS\n')
        # Declarar SOC=False (no hay componentes a partir de esto)
        SOC = False
    # Analizar la línea a ver si es la parte de componentes    
    elif 'COMPONENTS' in line: 
        # DEBUG: Imprimir mensaje y línea
        if (DEBUG):
            print ('\nInicio de COMPONENTS\n')
            print("Línea{}: {}".format(count, line.strip()))
        # Declarar SOC 'start of components', para empezar a analizar el próximo ciclo 
        SOC = True
    # Caso de un componente, si no es FILL, analizarlo
    elif SOC and not('FILL' in line) :
        # Separar la parte en paréntesis
        basura,coordenadas = line.split("( ")
        coordenadas,temp = coordenadas.split(" )")
        # Dividir coordenadas en x,y
        x,y = coordenadas.split(" ")
        # DEBUG: Imprimir x,y con la línea correspondiente
        if (DEBUG):
            print("[ x: ",x,"\ty: ",y,"]\t", "Línea{}: {}".format(count, line.strip()),)
        # Meter a lista de listas, para posteriormente hacer el heatmap
        componentes.append([int(x),int(y)])


    # Caso de vias de metal4, tiene que haber iniciado NETS, no se toman SPECIAL NETS
    # tomar NETS, NO tomar SPECIAL NETS
    # significa 'llega hasta el final'
    elif SON and ('NEW metal4' in line):
        # Reemplazar cualquier * por xMáximo (no importa si es 'y', no se va a analizar)
        line = line.replace("*", xMax)
        # Separar la parte en paréntesis, y obtener x1
        basura,coordenadas = line.split("metal4 ( ")
        x1,basura = coordenadas.split(" ",1)
        # Sacar coordenadas y obtener x2, eliminando cualquier coordenada extra
        coordenadas,temp = coordenadas.split(') (',1)
        x2,basura = temp.split(")",1)
        x2 = x2.replace(" ","")
        # DEBUG: Imprimir línea de componentes válido
        if (DEBUG):
            print("[ x1: ",x1,"\tx2: ",x2,"]\t", "Línea{}: {}".format(count, line.strip()))
        # Meter a lista de listas, para posteriormente hacer el heatmap
        metales.append([int(x1),int(x2)])

    # Línea vacía, EOF
    if not line:
        EOF = True

# Cerrar archivo
file.close()


'''
Código para formar Heatmap:
'''
# DEBUG: Imprimir arreglos de componentes y metales
if (DEBUG):
    print("\nCOMPONENTES:\n",componentes)
    print("\nMETALES:\n",metales)
# HACER AQUÍ LOGICA QUE LO HACE FUNCIONAR!!!!!!

'''
Plotear Heatmap:
'''
componentMap = sns.heatmap(np.array(componentes)) # actualizar .np
figure = componentMap.get_figure() 
figure.savefig('componentMap.png', dpi=400)
metalMap = sns.heatmap(np.array(metales)) # actualizar .np
figure = componentMap.get_figure() 
figure.savefig('metalsMap.png', dpi=400)

