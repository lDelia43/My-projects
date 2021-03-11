import random
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6


def leer_piezas(nombre_archivo="piezas.txt"):
    """
    Lee el archivo indicado (por defecto `piezas.txt`) y devuelve un diccionario
    con las rotaciones anteriores como clave y las siguientes como valor(en caso de ser la ultima rotacion
    tiene como valor la primer posicion)
    """
    diccionario_piezas = dict()

    with open(nombre_archivo) as piezas:
        lista_posciones_en_origen = list()
        for nro_linea, linea in enumerate(piezas):
            if linea == '\n':
                continue

            lista_linea = list()

            for rotacion in linea.split():
                lista_rot = list()

                if rotacion == '#':
                    break

                for coord in rotacion.split(';'):
                    l = list()
                    for pos in coord.split(','):
                        l.append(int(pos))
                    lista_rot.append(tuple(l))
                    
                lista_linea.append(tuple(lista_rot))
            lista_linea = tuple(lista_linea)

            if nro_linea == 0:
                diccionario_piezas[lista_linea[-1]] = lista_linea[-1]

            elif  1 <= nro_linea <= 3:
                diccionario_piezas[lista_linea[len(lista_linea) - 1]] = lista_linea[0]
                diccionario_piezas[lista_linea[0]] = lista_linea[len(lista_linea) - 1]

            elif 4 <= nro_linea <= 6:
                diccionario_piezas[lista_linea[len(lista_linea) - 1]] = lista_linea[0]
                contador = 0

                while contador < len(lista_linea) - 1:
                    diccionario_piezas[lista_linea[contador]] = lista_linea[contador + 1]
                    contador += 1
            lista_posciones_en_origen.append(lista_linea[0])
            
    return diccionario_piezas, lista_posciones_en_origen

rotacion , PIEZAS = leer_piezas()





def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    if pieza == None:
        return PIEZAS[random.randrange(len(PIEZAS))]
    return PIEZAS[pieza]


def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_trasladada = ()
    for elemento in pieza:
        pieza_trasladada += (elemento[0] + dx, elemento[1] + dy),
    return pieza_trasladada



def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    pieza_centrada = trasladar_pieza(pieza_inicial, ANCHO_JUEGO//2, 0)
    grilla = []
    for _ in range(ALTO_JUEGO):
        grilla.append([0]* ANCHO_JUEGO)
    dimensiones = (len(grilla[5]), len(grilla))
    score = 0
    juego = [grilla, pieza_centrada, dimensiones, score]
    return juego


def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return juego[2]

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return juego[1]

    

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return juego[0][y][x] == 1

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    ancho = dimensiones(juego)[0]
    pieza_trasladada = trasladar_pieza(pieza_actual(juego), direccion, 0)
    for x,y in pieza_trasladada:
        if x >= ancho or x < 0 or hay_superficie(juego, x, y):
            return juego
    juego[1] = pieza_trasladada
    return juego


def rotar(juego, rotaciones = rotacion):
    ancho, alto = dimensiones(juego)
    pieza_actual = juego[1]
    pieza_ordenada = sorted(pieza_actual)
    primer_posicion = pieza_ordenada[0]
    x, y = primer_posicion
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -x, -y)
    siguiente_rotacion = rotaciones[pieza_en_origen]
    pieza_trasladada = trasladar_pieza(siguiente_rotacion, x, y)
    for x , y in pieza_trasladada:
        if y == alto or x >= ancho or x < 0 or hay_superficie(juego, x, y):
            return pieza_actual
    return pieza_trasladada

            
def guardar_partida(juego, ruta = 'partida.txt'):
    """
    Guarda el ultimo estado del juego
    """
    with open(ruta, 'w') as partida:

        grilla = juego[0]
        pieza_actual = juego[1]
        ancho, alto = juego[2]
        puntaje = juego[3]

        partida.write("%s\n" % str(puntaje))
        partida.write("%s\n" % f"{str(ancho)},{str(alto)}")

        for fila in grilla:
            partida.write( "%s\n" % fila)

        for x , y  in pieza_actual:
            partida.write(f"{str(x)},{str(y)};")


def cargar_partida(ruta = "partida.txt"):
    """
    Carga la ultima partida guardada del juego y devuelve el estado del juego tal cual fue guardado
    """
    grilla = list()
    contador = 0
    dimension_cargada = tuple()
    pieza_actual = list()
    with open(ruta) as partida_guardada:


        puntaje_guardado = partida_guardada.readline().rstrip("\n") # cargo el puntaje del juego


        for numero_linea, linea in enumerate(partida_guardada):
            lista = list()


            if numero_linea == 0: # cargo las dimensiones 
                ancho, alto = linea.rstrip("\n").split(",")
                dimension_cargada = (int(ancho), int(alto))
                    

                    
            elif 0 < numero_linea < (dimension_cargada[1] + 1): # cargo la grilla 
                for pos_grilla in linea:
                    if pos_grilla.isdigit():
                        lista.append(int(pos_grilla))
                grilla.append(lista)

            
            elif numero_linea == (dimension_cargada[1] + 1): # cargo la pieza_actual
                for coordenada in linea.split(";"):   
                    l = list()      
                    if coordenada == "":
                        continue
                    for numero in coordenada.split(","):
                        l.append(int(numero))
                    pieza_actual.append(tuple(l))
        
        pieza_actual = tuple(pieza_actual)


    return grilla, pieza_actual, dimension_cargada, int(puntaje_guardado)




def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    grilla = juego[0]
    pieza_trasladada = trasladar_pieza(pieza_actual(juego), 0, 1)
    ancho, alto = dimensiones(juego)
    score = juego[3]

    if terminado(juego):
        return juego, False
    
    
    
    for r,w in pieza_trasladada:
        if w == alto or hay_superficie(juego, r, w):
            for x,y in pieza_actual(juego):
                grilla[y][x] = 1
            score += 50
            juego[3] = score
            eliminar_fila(juego)
            juego[1] = trasladar_pieza(siguiente_pieza, ancho//2, 0)
            return juego, True

    for _,z in pieza_trasladada: 
        if z < alto:
            juego[1] = pieza_trasladada
            return juego, False
    


def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    pieza_terminado = pieza_actual(juego)
    for x, y in pieza_terminado:
        if hay_superficie(juego, x, y):
            return True
    return False




def eliminar_fila(juego):
    """
    Elimina las filas completas de la grilla y baja una posición a las demás
    """
    superficie = juego[0]
    ancho = dimensiones(juego)[0]
    for fila in range(len(superficie)):
        if 0 in superficie[fila]:
            continue
        superficie.remove(superficie[fila])
        superficie.insert(0, [0]* ancho)
        juego[3] += 100



                    



