import random
import simpy
import numpy
import matplotlib.pyplot as plt

#Definimos una semilla por si queremos datos constantes
SEMILLA = 42
#Intervalo de generar carros a Aramberri 40 por minuto, centro en 1.5 y radio de 1.5
LLEGADA_ARAMBERRI = [0.0,3.0]
#Intervalos de generar carros en Rayon 20 por minuto, centro en 3.0 y radio de 3.0
LLEGADA_RAYON_U = [0.0, 6.0]
#Intervalos de generar carros en Rayon 30 por minuto, centro 2.0 en y radio de 2.0
LLEGADA_RAYON_D = [0.0, 4.0]
#Cantidad de autos en promedio por aramberri 40*60*2=4800
ARAMBERRI = 4800
#Cantidad de autos en promedio por rayon (20*60) = 1200 y (30*60) = 1800
#Cantidad total de Rayon = 3000
RAYON_U = 1200
RAYON_D = 1800
RAYON_T = 3000
#Cantidad de autos totales
AutosTotales= 7800
#Tiempos del semaforo
control = True
verdeAramberri = 40
rojoAramberri = 30

semaforo = verdeAramberri

#Tiempo de reaccion para avanzar(no solamente el primer carro sino para todos)
reaccion = 2
#Definimos las colas para Aramberri
COLA_A = 0
MAX_COLA_A = 0
NOMBRE_A = numpy.array([])
ESPERA_A = numpy.array([])
#Definimos las colas para Rayon
COLA_R = 0
MAX_COLA_R = 0
COLA_REAL_R = numpy.array([])
ESPERA_R = numpy.array([])


def llegadaAramberri(env, numero, server):
        for i in range(numero):
                a= auto(env, 'Auto Aramberri %02d'%i, server,1)
                env.process(a)
                tiempo_llegada = random.uniform(LLEGADA_ARAMBERRI[0],LLEGADA_ARAMBERRI[1])
                yield env.timeout(tiempo_llegada)#Retorna un objeto iterable 

def llegadaRayonUno(env, numero, server):
        for i in range(numero):
                #Este primer if controla la llegada de 8 a 9 por Rayon
                if env.now < 3600:
                        a= autoR(env, 'Auto Rayon de 8 a 9 %02d'%i, server,2)
                        env.process(a)
                        tiempo_llegada = random.uniform(LLEGADA_RAYON_U[0],LLEGADA_RAYON_U[1])
                        yield env.timeout(tiempo_llegada)#Retorna un objeto iterable 
                #Este primer if controla la llegada de 9 a 10 por Rayon
                if env.now >= 3600:
                        a= autoR(env, 'Auto Rayon de 9 a 10 %02d'%i, server,2)
                        env.process(a)
                        tiempo_llegada = random.uniform(LLEGADA_RAYON_D[0],LLEGADA_RAYON_D[1])
                        yield env.timeout(tiempo_llegada)#Retorna un objeto iterable 




##########################################################################

def auto (env, nombre, servidor,id):
        #El carro llega y se va cuando esta en verde y es el primero
        llegada = env.now
        #print ('%7.2f'%(env.now)," Llega el carro ", nombre)
        global COLA_A
        global MAX_COLA_A
        global ESPERA_A
        global NOMBRE_A
        #Atendemos a los carros (retorno del yield)
        #With ejecuta un iterador sin importar si hay excepciones o no
        if id==1:
            with servidor.request() as req:
                #Hacemos la espera hasta que el semaforo cambie a verde y este de primero
                COLA_A +=1
                if COLA_A > MAX_COLA_A:
                        MAX_COLA_A = COLA_A
                results = yield req        
                if control:
                    COLA_A = COLA_A - 1
                    espera = env.now - llegada
                    ESPERA_A = numpy.append(ESPERA_A,espera)
                    NOMBRE_A = numpy.append(NOMBRE_A,nombre)
            
                    #print('%7.2f'%(env.now), " El auto ", nombre, " espera a pasar el semaforo ", espera)
                    yield env.timeout(reaccion)
                    #print('%7.2f'%(env.now), " Pasa el semaforo el auto: ", nombre)

                else:
                    yield env.timeout(semaforo - env.now)
                    #print ("AHORA CONTROL ES ", control)
                    if control:
                        COLA_A = COLA_A - 1
                        espera = env.now - llegada
                        ESPERA_A = numpy.append(ESPERA_A,espera)
                        NOMBRE_A = numpy.append(NOMBRE_A,nombre)

                        #print('%7.2f'%(env.now), " El auto ", nombre, " espera a pasar el semaforo ", espera)
                        yield env.timeout(reaccion)
                        #print('%7.2f'%(env.now), " Pasa el semaforo el auto: ", nombre)

        
def autoR (env, nombre, servidor,id):
        #El carro llega y se va cuando esta en verde y es el primero
        llegada = env.now
        #print ('%7.2f'%(env.now)," Llega el carro ", nombre)
        global COLA_R
        global MAX_COLA_R
        global ESPERA_R
        global NOMBRE_R

        #Atendemos a los carros (retorno del yield)
        #With ejecuta un iterador sin importar si hay excepciones o no
        if id==2:
            with servidor.request() as req:
                #Hacemos la espera hasta que el semaforo cambie a verde y este de primero
                COLA_R +=1
                if COLA_R > MAX_COLA_R:
                        MAX_COLA_R = COLA_R
                results = yield req        
                if not control:
                    COLA_R = COLA_R - 1
                    espera = env.now - llegada
                    ESPERA_R = numpy.append(ESPERA_R,espera)
                    NOMBRE_R = numpy.append(NOMBRE_A,nombre)

                    #print('%7.2f'%(env.now), " El auto ", nombre, " espera a pasar el semaforo ", espera)
                    yield env.timeout(reaccion)
                    #print('%7.2f'%(env.now), " Pasa el semaforo el auto: ", nombre)

                else:
                    yield env.timeout(semaforo - env.now)
                    #print ("AHORA CONTROL ES ", control)
                    if not control:
                        COLA_R = COLA_R - 1
                        espera = env.now - llegada
                        ESPERA_R = numpy.append(ESPERA_R,espera)
                        NOMBRE_R = numpy.append(NOMBRE_A,nombre)

                        #print('%7.2f'%(env.now), " El auto ", nombre, " espera a pasar el semaforo ", espera)
                        yield env.timeout(reaccion)
                        #print('%7.2f'%(env.now), " Pasa el semaforo el auto: ", nombre)

        
##########################################################################


print('Simulacion semaforo Aramberri y Rayon')
#Asignamos a random una semilla fija para tener resultados 
#constante si no asignamos una semilla, generamos resultados 
#diferentes en cada ejecucion de la simulacion

random.seed(SEMILLA)

#Definimos un nuevo ambiente de simulacion utilizando
#la libreria simpy
env = simpy.Environment()
#env2 = simpy.Environment()
#Definimos un servidor con una capacidad de 1
#La capacidad de 1 significara que un solo auto puede 
#seguir adelante en el semaforo
servidor = simpy.Resource(env, capacity=1)
servidor2 = simpy.Resource(env, capacity=1)

env.process(llegadaAramberri (env,ARAMBERRI, servidor))
env.process(llegadaRayonUno (env,RAYON_U, servidor2))
control = True
#Asignamos en segundos las 2 horas de simulacion
while env.now < 7200:
        env.run(until=semaforo)
        if control :
            control = False
            semaforo +=rojoAramberri

        else:
            control = True
            semaforo +=verdeAramberri
plt.plot(NOMBRE_A,ESPERA_A)
plt.show()
plt.plot(NOMBRE_R,ESPERA_R)
plt.show()

print("ahora se deberia mostrar la grafica")
