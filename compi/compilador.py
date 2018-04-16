contadorHojas = 0
alfabeto = []
hojas = []
siguientePos = []

# Estructura del estado del autómata
class Estado():
    def __init__(self, conjunto, estado, inicial, aceptacion):
        self.conjunto = conjunto
        self.estado = estado
        self.elementos = {}
        self.inicial = inicial
        self.aceptacion = aceptacion

        for x in alfabeto:
            self.elementos[x] = set()

    def insertarMovimiento(self, elemento, movimiento):
        self.elementos[elemento] = movimiento

    def getEstado(self):
        return self.estado

    def getConjunto(self):
        return self.conjunto

    def getMovimiento(self, elemento):
        return self.elementos[elemento]

# Estructura espacial de matriz
class Matriz():
    def __init__(self):
        self.matriz = []
        self.tamaño = 0

    def crearMatriz(self, fila, columna):
        for x in range(fila):
            self.matriz.append([0] * columna)

    def insertarEstado(self, estadoNuevo, estadoOrigen=None, elemento=""):
        if not self.verificarRepetidos(estadoNuevo):
            self.matriz.append(Estado(self.tamaño, estadoNuevo, True if self.tamaño == 0 else False, True if contadorHojas - 1 in estadoNuevo else False))
            if self.tamaño:
                self.movimiento(estadoNuevo, estadoOrigen, elemento)
            self.tamaño += 1
            return True

        if self.tamaño:
            self.movimiento(estadoNuevo, estadoOrigen, elemento)

        return False

    def verificarRepetidos(self, estado):
        for x in self.matriz:
            if x.getEstado() == estado:
                return True
        return False

    def movimiento(self, estadoMovimiento, estadoOrigen, elemento):
        for x in self.matriz:
            if x.getEstado() == estadoOrigen:
                for y in self.matriz:
                    if y.getEstado() == estadoMovimiento:
                        x.insertarMovimiento(elemento, y.getConjunto())

    def imprimirAutomata(self):
        mensaje = ""

        for x in self.matriz:
            mensaje += "Conjunto: %s" % x.getConjunto()
            for y in alfabeto:
                mensaje += " %s: %s" % (y, x.getMovimiento(y))
            mensaje += "\n"

        return mensaje

# Estructura de Nodo
class Node():
    def __init__(self, elemento):
        self.elemento = elemento
        self.izq = None
        self.der = None
        self.hoja = True
        self.numeroHoja = None
        self.anulable = False
        self.primera = set()# Conjunto vacío
        self.ultima = set()# Conjunto vacío

    # Inserta un elemento a la izquierda o derecha del nodo dependiende del la posicion que se le envíe
    # que es la profundidad del arbol
    def insertar(self, elemento, pos=0):
        if pos == 0:
            if self.izq is None:
                if elemento is not None:
                    self.izq = Node(elemento)
            else:
                if elemento is not None:
                    self.der = Node(elemento)

            if elemento is not None:
                self.hoja = False
        else:
            if self.izq is not None and self.der is None:
                self.izq.insertar(elemento, pos-1)
            else:
                self.der.insertar(elemento, pos-1)

    # Hace el recorrido izquierda-raiz-derecha
    def ird(self):
        if self.izq is None:
            tiraIzq = ""
        else:
            tiraIzq = self.izq.ird()

        if self.der is None:
            tiraDer = ""
        else:
            tiraDer = self.der.ird()

        return tiraIzq + " " + self.getElemento() + " " + tiraDer

    # Numera los nodos que sean hoja
    def nodosHoja(self):
        global contadorHojas
        global alfabeto
        global hojas

        if self.izq is not None:
            self.izq.nodosHoja()

        if self.der is not None:
            self.der.nodosHoja()

        if self.hoja:
            self.numeroHoja = contadorHojas
            contadorHojas += 1
            if self.getElemento() != "#":
                if self.getElemento() not in alfabeto:
                    alfabeto.append(self.getElemento())
                hojas.append(self)

    # Marca los elementos necesarios para el algoritmo
    def marcarElementosAFD(self):
        if self.izq is not None:
            self.izq.marcarElementosAFD()

        if self.der is not None:
            self.der.marcarElementosAFD()

        self.anulabilidad()
        self.primeraPos()
        self.ultimaPos()

    # Calcula la anulabilidad
    def anulabilidad(self):
        if self.hoja:
            self.anulable = False
        elif self.getElemento() == "|":
            self.anulable = self.izq.getAnulable() or self.der.getAnulable()
        elif self.getElemento() == ".":
            self.anulable = self.izq.getAnulable() and self.der.getAnulable()
        elif self.getElemento() == "*":
            self.anulable = True
        elif self.getElemento() == "+":
            self.anulable = self.izq.getAnulable()
        elif self.getElemento() == "?":
            self.anulable = True

    # Calcula la primeraPos
    def primeraPos(self):
        if self.hoja:
            self.primera.add(self.getNumeroHoja())
        elif self.getElemento() == "|":
            self.primera = self.izq.getPrimeraPos() | self.der.getPrimeraPos()
        elif self.getElemento() == ".":
            if self.izq.getAnulable():
                self.primera = self.izq.getPrimeraPos() | self.der.getPrimeraPos()
            else:
                self.primera = self.izq.getPrimeraPos()
        elif self.getElemento() == "*":
            self.primera = self.izq.getPrimeraPos()
        elif self.getElemento() == "+":
            self.primera = self.izq.getPrimeraPos()
        elif self.getElemento() == "?":
            self.primera = self.izq.getPrimeraPos()

    # Calcula la ultimaPos
    def ultimaPos(self):
        if self.hoja:
            self.ultima.add(self.getNumeroHoja())
        elif self.getElemento() == "|":
            self.ultima = self.izq.getUltimaPos() | self.der.getUltimaPos()
        elif self.getElemento() == ".":
            if self.der.getAnulable():
                self.ultima = self.izq.getUltimaPos() | self.der.getUltimaPos()
            else:
                self.ultima = self.der.getUltimaPos()
        elif self.getElemento() == "*":
            self.ultima = self.izq.getUltimaPos()
        elif self.getElemento() == "+":
            self.ultima = self.izq.getUltimaPos()
        elif self.getElemento() == "?":
            self.ultima = self.izq.getUltimaPos()

    # Recorre el árbol e ingresa los conjuntos para siguientePos
    def marcarSiguientePos(self):
        global siguientePos

        if self.getElemento() == "*":
            for x in self.getUltimaPos():
                siguientePos[x] = siguientePos[x] | self.getPrimeraPos()
        elif self.getElemento() == ".":
            for x in self.izq.getUltimaPos():
                siguientePos[x] = siguientePos[x] | self.der.getPrimeraPos()

        if self.izq is not None:
            self.izq.marcarSiguientePos()

        if self.der is not None:
            self.der.marcarSiguientePos()

    # Devuelve el elemento del nodo
    def getElemento(self):
        return self.elemento

    # Devuleve la anulabilidad del nodo
    def getAnulable(self):
        return self.anulable

    # Devuelve el número del nodo hoja
    def getNumeroHoja(self):
        return self.numeroHoja

    # Devuelve la primeraPos del nodo
    def getPrimeraPos(self):
        return self.primera

    # Devuelve la ultimaPos del nodo
    def getUltimaPos(self):
        return self.ultima

# Estructura de Arbol
class Arbol():
    def __init__(self, elemento=None):
        if elemento is None:
            self.raiz = None
        else:
            self.raiz = Node(elemento)

    # Inserta un elemento en las profundidad del árbol que posee pos
    def insertar(self, elemento, pos=0):
        if self.raiz is None:
            self.raiz = Node(elemento)
        else:
            self.raiz.insertar(elemento, pos)

    # Inicia el recorrido izquierda-raiz-derecha
    def recorridoIRD(self):
        if self.raiz is None:
            return ""
        else:
            return self.raiz.ird()

    # Inicia el marcado de los nodos hoja
    def buscarHojas(self):
        if self.raiz is None:
            return None
        else:
            self.raiz.nodosHoja()

    # Inicia el algoritmo para marcar la anulabilidad, primeraPos, ultimaPos
    def afd(self):
        global siguientePos
        for x in range(contadorHojas-1):
            siguientePos.append(set())
        automata = Matriz()

        if self.raiz is None:
            return None
        else:
            self.raiz.marcarElementosAFD()
            self.raiz.marcarSiguientePos()

            # Ingresa el valor de la raiz
            automata.insertarEstado(self.raiz.getPrimeraPos())
            return self.afdAux(self.raiz.getPrimeraPos(), automata)

    def afdAux(self, estado, automata):
        estadoNuevo = set()

        for x in alfabeto:
            for y in estado:
                for z in hojas:
                    if z.getNumeroHoja() == y and z.getElemento() == x:
                        estadoNuevo = estadoNuevo | siguientePos[y]
                        break
            copiaEstado = estadoNuevo.copy() # Se hace una copia ya que los conjuntos trabajan con direcciones de
                                             # memoria, y si se limpia el origina, se borran en todos los lugaren en
                                             # donde se haciera una referencia de él
            if automata.insertarEstado(copiaEstado, estado, x):
                self.afdAux(copiaEstado, automata)
            estadoNuevo.clear()

        return automata

# Reprecenta los espacios donde debe haber una concatenación con un "."
def concatenador(lista):
    listaAux = []
    i = 0
    while i != len(lista):
        if lista[i] in "+*":
            if lista[i+1] not in "+*)#]":
                listaAux.append(lista[i])
                listaAux.append(".")
            else:
                listaAux.append(lista[i])
        elif lista[i] not in "+*(#|[":
            if lista[i+1] == "(" or lista[i] == "[" or lista[i+1] not in "+*)|]":
                listaAux.append(lista[i])
                listaAux.append(".")
            else:
                listaAux.append(lista[i])
        else:
            listaAux.append(lista[i])
        i += 1
    return listaAux


# Borra los espacios en blanco y retorna una lista con los tokens
def depurar(cadena):
    lista = []
    i = 0
    while i != len(cadena):
        if cadena[i] == "'":
            lista.append('(')
            i += 1
            while cadena[i] != "'":
                lista.append(cadena[i])
                i += 1
            lista.append(')')
        elif cadena[i] in "+*[]|()":
            lista.append(cadena[i])
        i += 1
    lista.append("#")
    return enlistar(concatenador(lista))


# Vuelve los valores dentro de parentesis y corchetes, una lista en la lista de tokens
def enlistar(lista):
    listaSalida = []
    listaAux = []
    abierto = 0
    i = 0
    pos = []

    for x in lista:
        if x == "(" or x == "[":
            abierto += 1
            pos.append(i)
            i += 1
        elif x == ")" or x == "]":
            if abierto == 1:
                for y in lista[pos.pop()+1:i]:
                    listaAux.append(y)
                lista = lista[i+1:]
                listaSalida.append(listaAux)
                if x == "]":
                    listaSalida.append('?')
                i = 0
                pos.clear()
            elif abierto > 1:
                v = pos.pop()
                for y in lista[v+1:i]:
                    listaAux.append(y)
                lista = lista[:v] + lista[i+1:]
                lista.insert(v, listaAux)
                if x == "]":
                    lista.insert(v+1, '?')
                    i = v + 2
                else:
                    i = v + 1
            abierto -= 1
            listaAux = []
        elif abierto == 0:
            listaSalida.append(x)
            i += 1
        else:
            i += 1
    return listaSalida


# Ordena la lista por prioridad de símbolos
def ordenarLista(lista):
    listaSimbolos = ["|", ".", "*", "+", "?"]
    i = len(lista)-1

    if len(lista) == 1:
        if type(lista[0]) is list:
            return ordenarLista(lista[0])
        else:
            return [lista[0]]
    elif len(lista) > 1:
        for x in listaSimbolos:
            for y in range(i, -1, -1):
                if lista[y] == x:
                    return [lista[y], ordenarLista(lista[:y]), ordenarLista(lista[y+1:])]
    else:
        return [None]


# Crea el árbol sintáctico
def crearArbol(lista, arbol, pos=0):
    if len(lista) == 3:
        arbol.insertar(lista[0], pos-1)
        crearArbol(lista[1], arbol, pos+1)
        crearArbol(lista[2], arbol, pos+1)
    elif len(lista) == 1:
        arbol.insertar(lista[0], pos-1)

# Función inicial
def er(cadena):
    arbol = Arbol()
    listaTokens = depurar(cadena)
    #print(listaTokens)
    listaPrioridad = ordenarLista(listaTokens)
    #print(listaPrioridad)
    crearArbol(listaPrioridad, arbol)
    #print(arbol.recorridoIRD())
    arbol.buscarHojas()
    automata = arbol.afd()
    #print(siguientePos)
    return automata.imprimirAutomata()


# Pruebas
#print(er("'hola'+('2'|'a') 'a-z'"))
#print(er("('a'|'b')*'abb'"))
#print(er("('a'|'b')*'hola'+('a'('a'|'b')+['a'])*"))
#print(er("('a'|'b')('b'|'a')"))
#print(er("'a'+('ab'|'ba')*'cvd''ascd'*('a'*('a'|('b'|'c')*)+)"))