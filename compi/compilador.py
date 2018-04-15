contadorHojas = 1

# Estructura de Nodo
class Node():
    def __init__(self, elemento):
        self.elemento = elemento
        self.izq = None
        self.der = None
        self.hoja = True
        self.numeroHoja = None
        self.anulable = False
        self.primeraPos = []
        self.ultimaPos = []

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

    def nodosHoja(self):
        global contadorHojas

        if self.izq is not None:
            self.izq.nodosHoja()

        if self.der is not None:
            self.der.nodosHoja()

        if self.hoja:
            self.numeroHoja = contadorHojas
            contadorHojas += 1

    def getElemento(self):
        return self.elemento


# Estructura de Arbol
class Arbol():
    def __init__(self, elemento=None):
        if elemento is None:
            self.raiz = None
        else:
            self.raiz = Node(elemento)

    def insertar(self, elemento, pos=0):
        if self.raiz is None:
            self.raiz = Node(elemento)
        else:
            self.raiz.insertar(elemento, pos)

    def recorridoIRD(self):
        if self.raiz is None:
            return ""
        else:
            return self.raiz.ird()

    def buscarHojas(self):
        if self.raiz is None:
            return None
        else:
            return self.raiz.nodosHoja()


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
    print(lista)
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
    listaSimbolos = [".", "|", "*", "+", "?"]
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
    print(listaTokens)
    listaPrioridad = ordenarLista(listaTokens)
    print(listaPrioridad)
    crearArbol(listaPrioridad, arbol)
    print(arbol.recorridoIRD())
    arbol.buscarHojas()
    return arbol


# Pruebas
#print(er("'hola'+('2'|'a') 'a-z'"))
print(er("('a'|'b')*'abb'"))
#print(er("('a'|'b')*'hola'+('a'('a'|'b')+['a'])*"))
#print(er("('a'|'b')('b'|'a')"))
#print(er("'a'+('ab'|'ba')*'cvd''ascd'*('a'*('a'|('b'|'c')*)+)"))