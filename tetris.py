import random
import pickle
OCUPADA = 1
VACIA = 0
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T
)

def rotaciones_pieza(ruta):
    """
    Guarda la rotacion de cada pieza, siendo cada pieza una clave y cada rotacion un valor
    en un diccionario y lo devuelve.
    """
    
    with open(ruta) as f_piezas:
        rotaciones = {}
        piezas = ('CUBO', 'Z', 'S', 'I', 'L', '-L', 'T')
        
        for j, linea in enumerate(f_piezas):
            linea = linea.rstrip('\n').split(' ')
            for i, pieza in enumerate(piezas):
                if j == i:
                    rotaciones[pieza] = list(linea)  
    
    for pieza, rotacion in rotaciones.items():
        for i, e in enumerate(rotacion):
            rotaciones[pieza][i] = tuple(tuple(int(x2) for x2 in x1.split(',')) for x1 in e.split(';'))
    return rotaciones

def guardar_partida(juego, ruta):
    """
    Guarda la partida escribiendo sobre el archivo el ultimo estado de juego.
    """
    with open(ruta, 'wb') as partida:
        pickle.dump(juego, partida) 

def cargar_partida(ruta):
    """
    Obtiene la ruta y continua el juego con el estado que fue guardado.
    """
    with open(ruta, 'rb') as partida_guardada:
        estado_de_juego = pickle.load(partida_guardada)
    return estado_de_juego

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El rotacion retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    if pieza == None:
        return random.choice(PIEZAS)
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
    posicion_inicial = pieza
 
    nueva_posicion = []
    
    for x, y in posicion_inicial:
        (coord_x, coord_y) = ((dx + x), (dy + y))
        pos_nueva = (coord_x, coord_y)
        nueva_posicion.append(pos_nueva)
    return tuple(nueva_posicion)

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
    pieza = trasladar_pieza(pieza_inicial, ANCHO_JUEGO//2, 0)
    grilla_tetris = []
    puntaje = 0
    
    for f in range(ALTO_JUEGO):
        grilla_tetris.append([])
        for c in range(ANCHO_JUEGO):
            grilla_tetris[f].append(0)

    return pieza, grilla_tetris, puntaje

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return (ANCHO_JUEGO, ALTO_JUEGO)

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """    
    pieza, grilla_tetris, puntaje = juego

    return pieza

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    _, grilla_tetris, _ = juego
    
    return grilla_tetris[y][x] == OCUPADA
       
def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """ 
    pieza, grilla_tetris, puntaje = juego
    pieza_movida = trasladar_pieza(pieza, direccion, 0)

    if not esta_en_posicion_valida(grilla_tetris, pieza_movida):
        return juego
    return pieza_movida, grilla_tetris, puntaje

def rotar(juego, rotaciones):
    """
    Recibe un estado de juego, ordena, y devuelve la pieza rotada en su posicion original.
    """
    pieza, grilla_tetris, puntaje = juego
    pieza_ordenada = ordenar_por_coordenadas(pieza)
    pos_1_x, pos_1_y = pieza_ordenada[0][0], pieza_ordenada[0][1]
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -pos_1_x, -pos_1_y)
    rotacion_siguiente = buscar_rotacion(pieza_en_origen)
    
    return trasladar_pieza(rotacion_siguiente, pos_1_x, pos_1_y)

def ordenar_por_coordenadas(pieza):
    """
    Ordena la pieza segun sus coordenadas, donde pos_1 resulta aquella que tiene menor valor de x y menor valor de y.
    """
    return tuple(sorted(pieza))

def obtener_sig_rotacion(pieza, tipo_pieza):
    """
    Recibe una tupla con las coordenadas de la pieza, su tipo, y devuelve el numero de la siguiente rotacion para piezas
    con cuatro rotaciones.
    """
    rotaciones = rotaciones_pieza('C:/Users/ruso_/OneDrive - fi.uba.ar/Documents/FIUBA/FIUBA/Algoritmos y Programación I/TP2/piezas.txt')
    i = 0
    num = 4
    while i < num:
        if pieza == rotaciones[tipo_pieza][i]:
            num = i
        i+= 1
    return num

def buscar_rotacion(pieza):
    """
    Busca la siguiente rotacion a la pieza dada y devuelve la pieza rotada.
    """
    rotaciones = rotaciones_pieza('C:/Users/ruso_/OneDrive - fi.uba.ar/Documents/FIUBA/FIUBA/Algoritmos y Programación I/TP2/piezas.txt')

    if pieza in rotaciones['CUBO']:
        return pieza 
    
    elif pieza in rotaciones['Z']:
        return rotaciones['Z'][1] if (pieza == rotaciones['Z'][0]) else rotaciones['Z'][0]

    elif pieza in rotaciones['S']:
        return rotaciones['S'][1] if (pieza == rotaciones['S'][0]) else rotaciones['S'][0]

    elif pieza in rotaciones['I']:
        return rotaciones['I'][1] if (pieza == rotaciones['I'][0]) else rotaciones['I'][0]
    
    elif pieza in rotaciones['L']:
        num = obtener_sig_rotacion(pieza, 'L')
        return rotaciones['L'][0] if (num == 3) else rotaciones['L'][num+1]

    elif pieza in rotaciones['-L']:
        num = obtener_sig_rotacion(pieza, '-L')
        return rotaciones['-L'][0] if (num == 3) else rotaciones['-L'][num+1]
 
    elif pieza in rotaciones['T']:
        num = obtener_sig_rotacion(pieza, 'T')
        return rotaciones['T'][0] if (num == 3) else rotaciones['T'][num+1]

def esta_en_posicion_valida(grilla_tetris, pieza):
    """
     Devuelve True si la pieza_actual esta en una posicion valida, devuelve False si ocurre lo contrario
    """
    for x, y in pieza:
        if (0 > x or x > ANCHO_JUEGO-1) or (0 > y or y > ALTO_JUEGO-1) or grilla_tetris[y][x] == OCUPADA:
            return False
    return True

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer rotacion
    es el nuevo estado del juego y el segundo rotacion es un booleano que indica
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
    el parámetro siguiente_pieza. El rotacion del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    pieza, grilla_tetris, puntaje = juego
    cambiar_pieza = True
    trasladada = trasladar_pieza(pieza, 0, 1)

    if terminado(juego):
        return juego, True
    
    if esta_en_posicion_valida(grilla_tetris, trasladada):
        nuevo_estado_juego = trasladada, grilla_tetris, puntaje
        return nuevo_estado_juego, False
    else:
        for pos_x, pos_y in pieza:
            grilla_tetris[pos_y][pos_x] = OCUPADA

        grilla_tetris, puntaje = eliminar_lineas_completas(grilla_tetris, puntaje)
  
        return (trasladar_pieza(siguiente_pieza, ANCHO_JUEGO//2, 0), grilla_tetris, puntaje), cambiar_pieza
      
def eliminar_lineas_completas(grilla_tetris, puntaje):
    """
    Verifica que las lineas de la grilla esten completas, en caso afirmativo las emilina
    y agrega una nueva fila vacia al comienzo, caso contrario devuelve el mismo
    estado de juego.
    """
   
    fila_llena = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    grilla_nueva = []
    
    for i in range(ALTO_JUEGO):
        if grilla_tetris[i] == fila_llena:
            fila_vacia = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            grilla_nueva.insert(0, fila_vacia)
            puntaje += 100
        else:
            grilla_nueva.insert(i, grilla_tetris[i])
            puntaje += 0
    return grilla_nueva, puntaje

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """         
    pieza, grilla_tetris, _ = juego
    if not esta_en_posicion_valida(grilla_tetris, pieza):
        return True
    return False

def obtener_puntaje(juego):
    """
    Recibe un estado de juego, y devuelve su puntaje actual.
    """
    _, _, puntaje = juego
    return puntaje


