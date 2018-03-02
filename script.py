INICIOX = 0
INICIOY = 1
FINX = 2
FINY = 3
TIMESTART = 4
TIMEEND = 5
ASIGNADO = 6
X = 0
Y = 1
ENTRANSITO = 2
TOINICIO = 3
DESTINO = 4
HISTORIAL = 5
IZQUIERDA = -1
ABAJO = -1
NADA = 0
DERECHA = 1
ARRIBA = 1

with open("./b_should_be_easy.in", "r") as content:
      lines = content.read().rstrip().split("\n")

lines = [i.split(" ") for i in lines]

rows = int(lines[0][0])
columns = int(lines[0][1])
vehicles = int(lines[0][2])
rides = int(lines[0][3])
bonus = int(lines[0][4])
steps = int(lines[0][5])
currentTime = 0

viajes = []
for idx, description in enumerate(lines):
    if idx == 0:
        continue

    viajes.append([int(j) for j in description] + [False])

coches = []
for i in range(vehicles):
    coches.append([0, 0, False, False, [], []])


def nextComute(viajes, maxsteps, currentTime):
    minTime = steps
    nextComutes = []
    for idx, transit in enumerate(viajes):
        if not transit[ASIGNADO]:
            if transit[TIMESTART] < currentTime: # TODO aun podria llegar
                transit[ASIGNADO] = True
                # nextComutes.append(transit)
            if (transit[TIMESTART] - currentTime) < minTime:
                minTime = transit[TIMESTART] - currentTime
                nextComutes = [transit]
            elif (transit[TIMESTART] - currentTime) == minTime:
                minTime = transit[TIMESTART] - currentTime
                nextComutes.append(transit)
    return nextComutes


def moverHaciaDestino(car, allTransits, currentTime):
    if car[X] < car[DESTINO][X]:
        car[X] += DERECHA
    elif car[X] < car[DESTINO][X]:
        car[X] += IZQUIERDA
    else:
        if car[Y] < car[DESTINO][Y]:
            car[Y] += ARRIBA
        elif car[Y] < car[DESTINO][Y]:
            car[Y] += ABAJO
        else:
            if car[TOINICIO]:
                if allTransits[car[HISTORIAL][-1]][TIMESTART] != currentTime:
                    car[TOINICIO] = False
                    car[DESTINO] = [allTransits[car[HISTORIAL][-1]][FINX], allTransits[car[HISTORIAL][-1]][FINY]]
                    moverHaciaDestino(car, allTransits, currentTime)
            else:
                car[ENTRANSITO] = False


def dist(viaje, coche):
    return viaje[INICIOX] - coche[X] + viaje[INICIOY] - coche[Y]


def assignCarToTransit(transits, ociosos, maxDist, allTransits):
    #print("Asignando", transits, ociosos)
    for transit in transits:
        #print("Asignando transito", transit)
        if (transit[FINX] - transit[INICIOX] + transit[FINY] - transit[INICIOY]) > (transit[TIMEEND] - transit[TIMESTART]):
            transit[ASIGNADO] = True
            #print("FUCK", transit[FINX] - transit[INICIOX] + transit[FINY] - transit[INICIOY], transit[TIMEEND] - transit[TIMESTART])
            continue
        minDist = maxDist
        myCar = None
        for coche in ociosos:
            if not coche[ENTRANSITO] and dist(transit, coche) < minDist:
                myCar = coche
        if not myCar:
            continue
        #print("El coche", myCar)
        transit[ASIGNADO] = True
        myCar[ENTRANSITO] = True
        myCar[TOINICIO] = True
        myCar[DESTINO] = [transit[INICIOX], transit[INICIOY]]
        myCar[HISTORIAL].append(allTransits.index(transit))


# #print(rows, columns, vehicles, rides, bonus, steps, viajes, coches)
#print("Viajes:", viajes)
#print("Coches:", coches)

while(steps > currentTime):
    print("Voy a dar un paso:", currentTime)
    algunoOcioso = True
    while algunoOcioso:
        #print("Hay ociosos")
        ociosos = []
        for coche in coches:
            if not coche[ENTRANSITO]:
                ociosos.append(coche)
        #print("Y son:", ociosos)
        if not ociosos:
            algunoOcioso = False
            continue
        #print("Sigo en el bucle")
        candidates = nextComute(viajes, steps, currentTime)
        if not candidates:
            break
        #print("Proximos viajes", candidates)
        assignCarToTransit(candidates, ociosos, columns + rows, viajes)

    for coche in coches:
        if coche[ENTRANSITO]:
            moverHaciaDestino(coche, viajes, currentTime)

    # print("Viajes:", viajes)
    # print("Coches:", coches)

    currentTime += 1


salida = open("./output.txt", "w")
for coche in coches:
    # print(len(coche[HISTORIAL]), coche[HISTORIAL])
    line = str(len(coche[HISTORIAL]))
    for viaje in coche[HISTORIAL]:
        line += " " + str(viaje)
    salida.write(line + "\n")

salida.close()
