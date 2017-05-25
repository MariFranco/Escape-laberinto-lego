#!/usr/bin/env python3
import ev3dev as ev3
from ev3dev.ev3 import *
import time
from time import sleep

#Inicializando las componentes
motorD = Motor('outA')
motorI = Motor('outD')
sensorDistancia = UltrasonicSensor()
sensorColor = ColorSensor()
sensorColor.mode='COL-COLOR'
lcd = Screen()
lcd.update()


#Valores enteros para determinar los movimientos
grados = 380
paso = 720
velocidad = 400
tiempo = 2
orientacion = 1
bool_orientacion = 1
filas = 10
columnas = filas
#Defino la matriz
matriz = []
for i in range(filas):
    matriz.append([])
    for j in range(columnas):
        matriz[i].append(0)
    #fin for
#fin for
#estado actual
actualX = 0
actualY = 0
#esperar a que el calor del color sea el que necesitamos
matriz[0][0] = 1
ok = 1
while(ok == 1):
    if(sensorColor.value() == 6 or sensorColor.value() == 1):
        ok = 0
#fin while
if(ok == 0):
    #entra al laberinto
    while(sensorColor.value() != 2 and (actualX < filas -1 and actualY < columnas -1 and actualX > -1 and actualY > -1)):
        #si hay un muro
        sleep(tiempo)
        if(sensorDistancia.value() <= 200):
            #Evaluamos la orientación que llevaba
            if(orientacion == 1):
                orientacion = orientacion + 1
                if(actualY + 1 <= filas -1):
                 matriz[actualX][actualY + 1] = -1
                #fin if
                #Ahora se procede a rotar a la izquierda
                motorD.run_to_rel_pos(position_sp = grados, speed_sp = velocidad, stop_action="hold")
                motorI.run_to_rel_pos(position_sp = -grados, speed_sp = velocidad, stop_action="hold")
                sleep(tiempo)
            #fin if
            elif(orientacion == 2):
                orientacion = orientacion + 1
                #rotar 180 grados por la Derecha
                motorD.run_to_rel_pos(position_sp=-2*grados, speed_sp=velocidad, stop_action="hold")
                motorI.run_to_rel_pos(position_sp=2*grados, speed_sp=velocidad, stop_action="hold")
                sleep(tiempo)
                #fin else
                if(actualX - 1 >= 0):
                    matriz[actualX - 1][actualY] = -1
                #fin if
            #fin if
            elif(orientacion == 3):
                orientacion = orientacion + 1
                # Rotar a la derecha
                motorD.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
                motorI.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
                sleep(tiempo)
                if(actualX + 1 <= filas - 1):
                    matriz[actualX + 1][actualY] = -1
            #fin if
            elif(orientacion == 4):
                orientacion = 1
                #Rotar hacia la derecha
                motorD.run_to_rel_pos(position_sp=-2*grados, speed_sp=velocidad, stop_action="hold")
                motorI.run_to_rel_pos(position_sp=2*grados, speed_sp=velocidad, stop_action="hold")
                sleep(tiempo)
                if(actualY - 1 >= 0):
                    matriz[actualX][actualY] = -1
                #fin if
            #fin if


        #fin if
        else:
            aprovado = 0
            if(orientacion == 1):
                if(actualY + 1 <= filas - 1):
                    actualY = actualY + 1
                    aprovado = 1
                    matriz[actualX][actualY] = 1
                #fin if
                sleep(tiempo)
            #fin if
            elif(orientacion == 2):
                if(actualX - 1 >= 0):
                    actualX = actualX - 1
                    aprovado = 1
                    matriz[actualX][actualY] = 1
                #fin if
                sleep(tiempo)
            #fin if
            elif(orientacion == 3):
                if(actualX + 1 <= columnas - 1):
                    actualX = actualX + 1
                    aprovado = 1
                    matriz[actualX][actualY] = 1
                #fin if
                sleep(tiempo)
            #fin if
            elif(orientacion == 4):
                if(actualY - 1 >= 0):
                    actualY = actualY - 1
                    aprovado = 1
                    matriz[actualX][actualY] = 1
                #fin if
                sleep(tiempo)
            #fin if
            #avanzar 1 paso
            if(aprovado == 1):
                motorD.run_to_rel_pos(position_sp = paso, speed_sp = velocidad, stop_action = "hold")
                motorI.run_to_rel_pos(position_sp = paso, speed_sp = velocidad, stop_action = "hold")
            #fin if
        #fin else
    #fin while

#fin if
#Si llego a la meta, este estado tendrá un valor de 100
if(sensorColor.value() == 2):
    matriz[actualX][actualY] = 100
#imprimimos la matriz
for i in range(filas):
    print(matriz[i])

sleep(5)

posicion = [0] * 2
orientacion = 3
dire = 0
tiempo = 3

while (matriz[posicion[0]][posicion[1]] != 100):
    sleep(tiempo)
    print("(" + str(posicion[0]) + "," + str(posicion[1]) + ")")
    if (posicion[0] == 0):
        if (posicion[1] == 0):

            if (matriz[posicion[0]][posicion[1] + 1] == 1 or matriz[posicion[0]][posicion[1] + 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0
                posicion[1] = posicion[1] + 1

                dire = 3  # derecha como está en la matriz xd
            elif (matriz[posicion[0] + 1][posicion[1]] == 1 or matriz[posicion[0] + 1][posicion[1]] == 100):
                matriz[posicion[0]][posicion[1]] = 0
                posicion[0] = posicion[0] + 1
                dire = 4  # abajo como está en la matriz xd

        # fin del if
        elif (posicion[1] == filas - 1):
            if (matriz[posicion[0] + 1][posicion[1]] == 1 or matriz[posicion[0] + 1][posicion[1]] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[0] = posicion[0] + 1
                dire = 4
            elif (matriz[posicion[0]][posicion[1] - 1] == 1 or matriz[posicion[0]][posicion[1] - 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[1] = posicion[1] - 1
                dire = 2
        # fin del elif
        else:
            if (matriz[posicion[0] + 1][posicion[1]] == 1 or matriz[posicion[0] + 1][posicion[1]] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[0] = posicion[0] + 1
                dire = 4
            elif (matriz[posicion[0]][posicion[1] - 1] == 1 or matriz[posicion[0]][posicion[1] - 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[1] = posicion[1] - 1
                dire = 2
            elif (matriz[posicion[0]][posicion[1] + 1] == 1 or matriz[posicion[0]][posicion[1] + 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[1] = posicion[1] + 1
                dire = 3
                # fin del else
    # fin del if
    elif (posicion[0] == filas - 1):
        if (posicion[1] == 0):
            if (matriz[posicion[0]][posicion[1] + 1] == 1 or matriz[posicion[0]][posicion[1] + 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[1] = posicion[1] + 1
                dire = 3
            elif (matriz[posicion[0] - 1][posicion[1]] == 1 or matriz[posicion[0]][posicion[1] - 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[0] = posicion[0] - 1
                dire = 1
        # fin del if
        elif (posicion[1] == filas - 1):
            if (matriz[posicion[0] - 1][posicion[1]] == 1 or matriz[posicion[0] - 1][posicion[1]] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[0] = posicion[0] - 1
                dire = 1
            elif (matriz[posicion[0]][posicion[1] - 1] == 1 or matriz[posicion[0]][posicion[1] - 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[1] = posicion[1] - 1
                dire = 2
        # fin del elif
        else:
            if (matriz[posicion[0] - 1][posicion[1]] == 1 or matriz[posicion[0] - 1][posicion[1]] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[0] = posicion[0] - 1
                dire = 1
            elif (matriz[posicion[0]][posicion[1] - 1] == 1 or matriz[posicion[0]][posicion[1] - 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[1] = posicion[1] - 1
                dire = 2
            elif (matriz[posicion[0]][posicion[1] + 1] == 1 or matriz[posicion[0]][posicion[1] + 1] == 100):
                matriz[posicion[0]][posicion[1]] = 0

                posicion[1] = posicion[1] + 1
                dire = 3
                # fin del else
                # fin del elif
    elif (posicion[1] == 0):
        if (matriz[posicion[0] - 1][posicion[1]] == 1 or matriz[posicion[0] - 1][posicion[1]] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[0] = posicion[0] - 1
            dire = 1
        elif (matriz[posicion[0] + 1][posicion[1]] == 1 or matriz[posicion[0] + 1][posicion[1]] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[0] = posicion[0] + 1
            dire = 4
        elif (matriz[posicion[0]][posicion[1] + 1] == 1 or matriz[posicion[0]][posicion[1] + 1] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[1] = posicion[1] + 1
            dire = 3
    # fin del elif
    elif (posicion[1] == filas - 1):
        if (matriz[posicion[0] - 1][posicion[1]] == 1 or matriz[posicion[0] - 1][posicion[1]] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[0] = posicion[0] - 1
            dire = 1
        elif (matriz[posicion[0] + 1][posicion[1]] == 1 or matriz[posicion[0] + 1][posicion[1]] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[0] = posicion[0] + 1
            dire = 4
        elif (matriz[posicion[0]][posicion[1] - 1] == 1 or matriz[posicion[0]][posicion[1] - 1] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[1] = posicion[1] - 1
            dire = 2
    # fin del elif
    else:
        if (matriz[posicion[0] - 1][posicion[1]] == 1 or matriz[posicion[0] - 1][posicion[1]] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[0] = posicion[0] - 1
            dire = 1
        elif (matriz[posicion[0] + 1][posicion[1]] == 1 or matriz[posicion[0] + 1][posicion[1]] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[0] = posicion[0] + 1
            dire = 4
        elif (matriz[posicion[0]][posicion[1] - 1] == 1 or matriz[posicion[0]][posicion[1] - 1] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[1] = posicion[1] - 1
            dire = 2
        elif (matriz[posicion[0]][posicion[1] + 1] == 1 or matriz[posicion[0]][posicion[1] + 1] == 100):
            matriz[posicion[0]][posicion[1]] = 0

            posicion[1] = posicion[1] + 1
            dire = 3
    # fin del else
    print("(" + str(posicion[0]) + "," + str(posicion[1]) + ")")
    # rota a la pocision adecuada
    if ((orientacion == 1 and dire == 2)):
        # Ahora se procede a rotar a la izquierda
        motorD.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if
    elif ((orientacion == 2 and dire == 4)):
        # Ahora se procede a rotar a la izquierda
        motorD.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if
    elif ((orientacion == 4 and dire == 3)):
        # Ahora se procede a rotar a la izquierda
        motorD.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if
    elif ((orientacion == 3 and dire == 1)):
        # Ahora se procede a rotar a la izquierda
        motorD.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if
    elif ((orientacion == 1 and dire == 2)):
        # Ahora se procede a rotar a la izquierda
        motorD.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if
    elif ((orientacion == 2 and dire == 4)):
        # Ahora se procede a rotar a la izquierda
        motorD.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if
    elif ((orientacion == 4 and dire == 3)):
        # Ahora se procede a rotar a la izquierda
        motorD.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if
    elif ((orientacion == 3 and dire == 1)):
        # Ahora se procede a rotar a la izquierda
        motorD.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if

    elif ((orientacion == 1 and dire == 3)):
        # Rotar hacia la derecha
        motorD.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

        # fin else
    # fin if
    elif ((orientacion == 3 and dire == 4)):
        # Rotar hacia la derecha
        motorD.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

        # fin else
    # fin if
    elif ((orientacion == 4 and dire == 2)):
        # Rotar hacia la derecha
        motorD.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

        # fin else
    # fin if
    elif ((orientacion == 2 and dire == 1)):
        # Rotar hacia la derecha
        motorD.run_to_rel_pos(position_sp=-grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

        # fin else
    # fin if
    elif (orientacion == dire):
        print("Mariana te amo")
    else:
        # rotar 180 grados por la Derecha
        motorD.run_to_rel_pos(position_sp=-2 * grados, speed_sp=velocidad, stop_action="hold")
        motorI.run_to_rel_pos(position_sp=2 * grados, speed_sp=velocidad, stop_action="hold")
        sleep(tiempo)

    # fin if
    motorD.run_to_rel_pos(position_sp=paso, speed_sp=velocidad, stop_action="hold")
    motorI.run_to_rel_pos(position_sp=paso, speed_sp=velocidad, stop_action="hold")
    sleep(tiempo)

    print (str(orientacion) + " - " + str(dire))
    orientacion = dire
# fin del while
print("FIN DEL PROGRAMA")