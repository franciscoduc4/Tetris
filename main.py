import tetris
import gamelib
import csv

ALTO_PIXELES = 360
ANCHO_PIXELES = 180
CELDA_PIXELES = 20
ESPERA_DESCENDER = 10

def comando_teclas(ruta_teclas):
    """
    Genera un diccionario donde almacena los movimientos como claves, y las teclas a presionar como valores.
    """
    with open(ruta_teclas) as f_teclas:
        tecla_presionada = {}
        f_teclas_csv = csv.reader(f_teclas, delimiter = '=')   
        for tecla, accion in f_teclas_csv:
            tecla_presionada[accion] = tecla      
    return tecla_presionada

def recuperar_top(ruta):
    """
    Devuelve la tabla de puntajes ya escrita en el archivo, para poder seguir las posiciones del Top 10.
    """

    tabla_puntajes = []
    with open(ruta) as tabla_top:
        for linea in tabla_top:
            linea = linea.rstrip('\n').split(';')
            if len(linea) == 0:
                return tabla_puntajes
            else:
                puntaje, jugador = linea[1], linea[0]
                tabla_puntajes.append((puntaje, jugador))
    return tabla_puntajes

def ingresar_top(puntaje, tabla_puntajes):
    """
    Ingresa el nuevo jugador a la tabla de puntuaciones, dejandola ordenada de mayor a menor.
    """
    
    if len(tabla_puntajes) == 0:
        jugador_n = gamelib.input('Has perdido, ingresar un nickname: ')
        tabla_puntajes.append((puntaje, jugador_n))
        return tabla_puntajes
    
    if len(tabla_puntajes) != 0:
        jugador_n = gamelib.input('Has perdido, ingresar un nickname: ')
        for p, puntos_de_jugador in enumerate(tabla_puntajes):
            if puntaje > int(puntos_de_jugador[0]):
                tabla_puntajes.insert(p, (puntaje, jugador_n))
                break
            else:
                tabla_puntajes.append((puntaje, jugador_n))
                break
        return tabla_puntajes

def puntuaciones_mas_altas(ruta, tabla_puntajes):
    """
    Guarda en un archivo las últimas diez posiciones ordenadas
    de mayor a menor respecto al puntaje.
    """
    with open(ruta, 'w') as tabla_top_10:
        if len(tabla_puntajes) > 10:
           tabla_puntajes = tabla_puntajes[:10]
        for puntos, jugador_n in tabla_puntajes:
            tabla_top_10.write(f'{jugador_n};{puntos}\n')

def dibujar_top_10(ruta):
    """
    Recibe como parámetro el último top 10 guardado y lo grafica en la pantalla.
    """
    gamelib.draw_rectangle(0, 0, ALTO_PIXELES, ANCHO_PIXELES*2, fill='black')
    gamelib.draw_text(f'TOP 10 MEJORES JUGADORES', 180, 30)
    i = 60
    with open(ruta, 'r') as top_10:
        for linea in top_10:
            linea = linea.rstrip('\n').split(';')
            gamelib.draw_text(f'{linea[0]} ----> Puntos: {linea[1]}', 165, i)
            i += 30

def dibujar_grilla(alto_px, ancho_px):
    """
    Dibuja el tablero del tetris.
    """
    for i in range(0, ALTO_PIXELES + 1, CELDA_PIXELES):
        gamelib.draw_line(0, i, ANCHO_PIXELES, i, fill='grey')     
    for j in range(0, ANCHO_PIXELES + 1, CELDA_PIXELES):
        gamelib.draw_line(j, 0, j, ALTO_PIXELES, fill='grey')
    
def dibujar_proxima_pieza(prox_pieza):
    """
    Dibuja la siguiente pieza a ser bienvenida al juego.
    """
    gamelib.draw_text(f'Proxima pieza', 270, 70)
    gamelib.draw_rectangle(210, 90, 330, 220, outline='white', fill='black')
    dibujar_pieza(prox_pieza, 6, 3)
    
def pintar_cuadro(x, y):
    """
    Pinta el cuadro del tamaño de px que esté ocupando la coordenada de la pieza y/o superficie.
    """
    x, y = x * CELDA_PIXELES, y * CELDA_PIXELES
    gamelib.draw_rectangle(0, 0, x, 0, outline='grey', fill='grey')
    gamelib.draw_rectangle(x, y, x + CELDA_PIXELES, y + CELDA_PIXELES, outline='grey', fill='grey')

def dibujar_pieza(pieza, offset_x=0, offset_y=0):
    """
    Dibuja el cuerpo de la pieza con sus respectivas coordenadas.
    """
    for x, y in pieza:
        x, y = x + offset_x, y + offset_y
        pintar_cuadro(x + offset_x, y + offset_y)

def dibujar_puntaje(juego):
    """
    Mantiene actualizado el gráfico del puntaje, por debajo de la siguiente pieza.
    """
    puntaje = tetris.obtener_puntaje(juego)
    gamelib.draw_text(f'Puntos: ', 270, ALTO_PIXELES - (CELDA_PIXELES * 4))
    gamelib.draw_text(f'{puntaje}', 270, ALTO_PIXELES - (CELDA_PIXELES * 2))

def dibujar_superficie(grilla):
    """
    Similar a dibujar_pieza, toma todas las coordenadas que estén ocupadas por la superficie y las pinta.
    """
    for i, fila in enumerate(grilla):
        for j, columna in enumerate(fila):
            if columna == tetris.OCUPADA:
                pintar_cuadro(j, i)

def dibujar_ventana(juego):
    """
    Dibuja todo el contenido grafico del juego actual.
    """
    dibujar_grilla(ALTO_PIXELES, ANCHO_PIXELES)
    dibujar_pieza(tetris.pieza_actual(juego))
    dibujar_superficie(juego[1])
    dibujar_puntaje(juego)

def main():
    
    rotaciones = tetris.rotaciones_pieza('C:/Users/ruso_/OneDrive - fi.uba.ar/Documents/FIUBA/FIUBA/Algoritmos y Programación I/TP2/piezas.txt')
    teclas = comando_teclas('C:/Users/ruso_/OneDrive - fi.uba.ar/Documents/FIUBA/FIUBA/Algoritmos y Programación I/TP2/teclas.txt')

    # Inicializar el estado del juego
    pieza_tetris = tetris.generar_pieza()
    juego_tetris = tetris.crear_juego(pieza_tetris)
    siguiente_pieza = tetris.generar_pieza()
    gamelib.resize(ALTO_PIXELES, ALTO_PIXELES)
    timer_bajar = ESPERA_DESCENDER
    
    while gamelib.loop(fps=30):
        
        gamelib.draw_begin()
        # Dibujar la pantalla
        dibujar_proxima_pieza(siguiente_pieza)
        dibujar_ventana(juego_tetris)
         
        for event in gamelib.get_events():
            if not event:
                break
            
            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
                # Actualizar el juego, según la tecla presionada
               
                if tecla == 'Escape':
                    return
                    
                if tecla in teclas['IZQUIERDA']:
                    juego_tetris = tetris.mover(juego_tetris, tetris.IZQUIERDA)
                                                            
                if tecla in teclas['DERECHA']:
                    juego_tetris = tetris.mover(juego_tetris, tetris.DERECHA)
                                                        
                if tecla in teclas['DESCENDER']:
                    juego_tetris, cambiar_pieza = tetris.avanzar(juego_tetris, siguiente_pieza)
                    if cambiar_pieza == True:
                        siguiente_pieza = tetris.generar_pieza()
                        
                if tecla in teclas['ROTAR']:
                    pieza_tetris = tetris.rotar(juego_tetris, rotaciones)
                    if tetris.esta_en_posicion_valida(juego_tetris[1], pieza_tetris):
                        puntaje = juego_tetris[2]
                        juego_tetris = pieza_tetris, juego_tetris[1], puntaje
                                    
                if tecla in teclas['GUARDAR']:
                    tetris.guardar_partida(juego_tetris, 'ultima-partida.txt')
                                                
                if tecla in teclas['CARGAR']:
                    juego_tetris = tetris.cargar_partida('ultima-partida.txt')
             
        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            juego_tetris, cambiar_pieza = tetris.avanzar(juego_tetris, siguiente_pieza)
            if cambiar_pieza == True:
                siguiente_pieza = tetris.generar_pieza()
            # Descender la pieza automáticamente
        
        if tetris.terminado(juego_tetris):
            break
            
    top_10 = recuperar_top('C:/Users/ruso_/OneDrive - fi.uba.ar/Documents/FIUBA/FIUBA/Algoritmos y Programación I/TP2/puntuaciones.txt')
    puntuaciones_mas_altas('C:/Users/ruso_/OneDrive - fi.uba.ar/Documents/FIUBA/FIUBA/Algoritmos y Programación I/TP2/puntuaciones.txt', ingresar_top(juego_tetris[2], top_10))
    dibujar_top_10('C:/Users/ruso_/OneDrive - fi.uba.ar/Documents/FIUBA/FIUBA/Algoritmos y Programación I/TP2/puntuaciones.txt')
    gamelib.wait(gamelib.EventType.KeyPress)
    
gamelib.init(main)

