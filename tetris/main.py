import os.path
from os import path
import gamelib
import tetris
import csv
ESPERA_DESCENDER = 8

def acciones_teclas(ruta = "teclas.txt"):
    acciones = {}
    with open("teclas.txt") as teclas:
        for linea in teclas:

            if linea != "\n":
                clave, valor = linea.strip().split('=')
                acciones[clave.strip()] = valor.strip()
    return acciones



def juego_dibujar(juego, siguiente_pieza):
    gamelib.draw_text("TETRIS",410,30, size = 25)
    dibujar_lineas_horizontales(0,30,270,30)
    dibujar_lineas_verticales(30,0,30,540)
    mostrar_puntuacion(juego)
    mostrar_superficie_consolidada(juego)
    mostrar_pieza_actual(juego)
    mostar_siguiente_pieza_cuadro()
    mostrar_siguiente_pieza(siguiente_pieza)


def main():
    # Inicializar el estado del juego
    juego = tetris.crear_juego(tetris.generar_pieza())
    gamelib.resize(540, 540)
    timer_bajar = ESPERA_DESCENDER
    siguiente_pieza = tetris.generar_pieza()
    mapeado_teclas = acciones_teclas()

    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        # Dibujar la pantalla
        juego_dibujar(juego, siguiente_pieza)
        gamelib.draw_end()
        

        if tetris.terminado(juego):
            break

        for event in gamelib.get_events():

            if not event:
                break

            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
                
                # Actualizar el juego, según la tecla presionada
                if tecla in mapeado_teclas: #Si el jugador oprime las teclas "a","d","w","s","g","c","esc" se realizara una accion determinada para esa tecla
                    movimiento = mapeado_teclas.get(tecla)

                    if movimiento == "DERECHA" or movimiento == "IZQUIERDA":
                        der_izq = Direccion(movimiento)
                        tetris.mover(juego, der_izq.determinar_direccion())

                    if movimiento == "DESCENDER":
                        _, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
                        if cambiar_pieza:
                            siguiente_pieza = tetris.generar_pieza()

                    if movimiento == "GUARDAR":
                        tetris.guardar_partida(juego, "partida.txt")

                    if movimiento == "CARGAR":
                        if path.exists("partida.txt"):
                            grilla, pieza_actual, dimensiones, puntaje = tetris.cargar_partida("partida.txt")
                            juego[0] = grilla
                            juego[1] = pieza_actual
                            juego[2] = dimensiones
                            juego[3] = puntaje
                        else:
                            tetris.guardar_partida(juego, "partida.txt")

                    if movimiento == "SALIR":
                        return
                    
                    if movimiento == "ROTAR":
                        juego[1] = tetris.rotar(juego)


                

        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            # Descender la pieza automáticamente
            _, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
            if cambiar_pieza:
                siguiente_pieza = tetris.generar_pieza()

    puntuacion_lograda = juego[3]
    lista_puntuacion = puntuacion(puntuacion_lograda)
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        mostrar_lista_de_puntajes(lista_puntuacion)
        gamelib.draw_end()
        for event in gamelib.get_events():
            if event.type == gamelib.EventType.KeyPress and event.key == 'Escape':
                return
            



def dibujar_lineas_horizontales(x1,y1,x2,y2):
    """
    Dibuja las lineas horizontales de mi grilla
    """
    while y1 and y2 != 570:
        gamelib.draw_line(x1, y1, x2, y2, fill='grey', width=2)
        y1 += 30
        y2 += 30

def dibujar_lineas_verticales(x1,y1,x2,y2):
    """
    Dibuja las lineas verticales de mi grilla
    """
    while x1 and x2 != 300:
        gamelib.draw_line(x1, y1, x2, y2, fill='grey', width=2)
        x1 += 30
        x2 += 30

def mostrar_superficie_consolidada(juego):
    """
    Dibuja la superficie consolidada
    """
    grilla = juego[0]
    for y,fila in enumerate(grilla):
        for x,columna in enumerate(fila):
            if columna == 1:
                gamelib.draw_rectangle(5+x*30,5+y*30,25+x*30,25+y*30)

def mostrar_siguiente_pieza(siguiente_pieza):
    """
    Muestra la sieguiente_pieza en pantalla
    """
    for x,y in siguiente_pieza:
        gamelib.draw_rectangle(320+x*30,125+y*30,340+x*30,145+y*30, outline = "white" , fill= "grey")


def mostrar_pieza_actual(juego):
    """
    Dibuja la ubicación de la pieza actual
    """
    pieza_actual = juego[1]
    for x,y in pieza_actual:
        gamelib.draw_rectangle(5+x*30,5+y*30,25+x*30,25+y*30)


def mostar_siguiente_pieza_cuadro():
    """
    Dibuja el cuadro de la siguiente_pieza
    """
    gamelib.draw_text("NEXT PIECE",360,100)
    gamelib.draw_line(300, 110, 420, 110, fill='grey', width=2)
    gamelib.draw_line(300, 110, 300, 250, fill='grey', width=2)
    gamelib.draw_line(300, 250, 420, 250, fill='grey', width=2)
    gamelib.draw_line(420, 110, 420, 250, fill='grey', width=2)

def mostrar_lista_de_puntajes(lista):
    """
    Muestra la tabla de puntajes
    """
    y = 0
    for nombre, puntaje in lista:
        y += 50
        gamelib.draw_text(f"{nombre} realizo {puntaje} puntos", 270, y )

def mostrar_puntuacion(juego):
    """
    Dibuja el cuadro donde ira ubicado el score
    """
    score = juego[3]
    gamelib.draw_text(f"{score}",360,425)
    gamelib.draw_text("SCORE",360,400)
    gamelib.draw_line(330, 410, 390, 410, fill='grey', width=2)
    gamelib.draw_line(330, 410, 330, 435, fill='grey', width=2)
    gamelib.draw_line(330, 435, 390, 435, fill='grey', width=2)
    gamelib.draw_line(390, 410, 390, 435, fill='grey', width=2)

class Direccion:
    def __init__(self, direccion):
        """
        Inicializa la direccion
        """
        self.direccion = direccion
    
    def determinar_direccion(self):
        """
        Determina la direccion, si es derecha devuelve 1 y si es izquierda devuelve -1
        """
        if self.direccion == "DERECHA":
            self.direccion = 1
            return self.direccion
        if self.direccion == "IZQUIERDA":
            self.direccion = -1
            return self.direccion


def puntuacion(puntuacion_jugador):
    """
    Recibe la puntuacion del jugador, le pide al usuario que ingrese su nombre y lo guarda en un archivo de texto
    """
    lista_puntuaciones = list()
    nombre = gamelib.input("Ingrese su nombre de usuario")

    if not nombre :
        nombre = "N/N"

    try:
        with open("puntuaciones.txt")as puntuaciones_cargadas:
            puntuaciones_anteriores = csv.reader(puntuaciones_cargadas)
            for puntaje in puntuaciones_anteriores:
                lista_puntuaciones.append(puntaje)
    except FileNotFoundError:
        pass

    lista_puntuaciones.append([nombre,puntuacion_jugador])
    lista_puntuaciones = sorted(lista_puntuaciones, key=lambda puntos:int(puntos[1])) # Ordena la lista por puntos

    if len(lista_puntuaciones) == 11:
        lista_puntuaciones.pop(0)

    with open("puntuaciones.txt","w")as puntuaciones:
        for nombre, puntuacion in lista_puntuaciones:
            puntuaciones.write("%s\n" % f"{nombre},{puntuacion}")
    lista_puntuaciones.reverse()
    return lista_puntuaciones




gamelib.init(main)
