import random
import simpy
import numpy
import matplotlib.pyplot as plt
import math

#Definimos una semilla por si queremos datos constantes
SEMILLA = 42
#Intervalo de generar carros a Aramberri 40 por minuto, centro en 1.5 y radio de 1.5
LLEGADA_ARAMBERRI = [0.0,3.0]
#Intervalos de generar carros en Rayon 20 por minuto, centro en 3.0 y radio de 3.0
LLEGADA_RAYON_U = [0.0, 6.0]
#Intervalos de generar carros en Rayon 30 por minuto, centro 2.0 en y radio de 2.0
LLEGADA_RAYON_D = [0.0, 4.0]
#Cantidad de autos en promedio por aramberri 40*60*2=4800
ARAMBERRI = 6000#4800
#Cantidad de autos en promedio por rayon (20*60) = 1200 y (30*60) = 1800
#Cantidad total de Rayon = 3000
RAYON_U = 5000 #1200
RAYON_D = 5000 #1800
RAYON_T = 10000 #3000
#Cantidad de autos totales
AutosTotales= 10000 #7800
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
#Definimos las colas para Rayon
COLA_R = 0
MAX_COLA_R = 0

#Definimos arrays de numpy para la cola de A, de R y de T (todos)
Array_Cola_A = numpy.array([])
Array_Cola_R = numpy.array([])
Array_Cola_T = numpy.array([])

#Definimos la cola del momento
Cola_YA = 0
Cola_A = 0
Cola_R = 0

#Definimos arrays para la espera de A, R y T
Array_Espera_A= numpy.array([])
Array_Espera_R= numpy.array([])
Array_Espera_T= numpy.array([])

cola1800 = 0
cola3600 = 0
cola5400 = 0
cola7200 = 0

cola1800A = 0
cola3600A = 0
cola5400A = 0
cola7200A = 0

cola1800R = 0
cola3600R = 0
cola5400R = 0
cola7200R = 0

espera1800 = 0
espera3600 = 0
espera5400 = 0
espera7200 = 0

espera1800A = 0
espera3600A = 0
espera5400A = 0
espera7200A = 0

espera1800R = 0
espera3600R = 0
espera5400R = 0
espera7200R = 0


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
    if env.now < 7200:
        llegada = env.now
        global COLA_A
        global MAX_COLA_A

        global ESPERA_A
        global NOMBRE_A

        global espera_ot
        global espera_n
        global espera_nt
        global espera_d

        global espera_otA
        global espera_nA
        global espera_ntA
        global espera_dA

        global espera_otR
        global espera_nR
        global espera_ntR
        global espera_dR

        global Array_Cola_A
        global Array_Cola_T
        global Cola_YA

        global cola1800
        global cola3600
        global cola5400
        global cola7200

        global cola1800A
        global cola3600A
        global cola5400A
        global cola7200A

        global cola1800R
        global cola3600R
        global cola5400R
        global cola7200R

        global Cola_A

        global Array_Espera_T
        global Array_Espera_A
        global Array_Espera_R

        global espera1800
        global espera3600
        global espera5400
        global espera7200

        global espera1800A
        global espera3600A
        global espera5400A
        global espera7200A

        global espera1800R
        global espera3600R
        global espera5400R
        global espera7200R

        print ('%7.2f'%(env.now)," Llega el carro ", nombre)

        Array_Cola_A = numpy.append(Array_Cola_A,nombre)
        Array_Cola_T = numpy.append(Array_Cola_T,nombre)
        Cola_YA +=1 
        Cola_A +=1 

        #With ejecuta un iterador sin importar si hay excepciones o no
        if id==1 :
            with servidor.request() as req:
                #Hacemos la espera hasta que el semaforo cambie a verde y este de primero

                results = yield req        
                if control:
                    if env.now<7200:
                        yield env.timeout(reaccion)
                        espera = env.now - llegada
                        Array_Espera_A = numpy.append(Array_Espera_A, espera)
                        Array_Espera_T = numpy.append(Array_Espera_T, espera)
                        Cola_YA -=1 
                        Cola_A -=1
                        if env.now == 1800:
                            cola1800 = Cola_YA
                            cola1800R = Cola_R
                            cola1800A = Cola_A

                            espera1800 = numpy.mean(Array_Espera_T)
                            espera1800A = numpy.mean(Array_Espera_A)
                            espera1800R = numpy.mean(Array_Espera_R)
                        if env.now == 3600:
                            cola3600 = Cola_YA
                            cola3600R = Cola_R
                            cola3600A = Cola_A

                            espera3600 = numpy.mean(Array_Espera_T)
                            espera3600A = numpy.mean(Array_Espera_A)
                            espera3600R = numpy.mean(Array_Espera_R)
                        if env.now == 5400:
                            cola5400 = Cola_YA
                            cola5400R = Cola_R
                            cola5400A = Cola_A

                            espera5400 = numpy.mean(Array_Espera_T)
                            espera5400A = numpy.mean(Array_Espera_A)
                            espera5400R = numpy.mean(Array_Espera_R)
                        if env.now == 7200:
                            cola7200 = Cola_YA
                            cola7200R = Cola_R
                            cola7200A = Cola_A
                           
                            espera7200 = numpy.mean(Array_Espera_T)
                            espera7200A = numpy.mean(Array_Espera_A)
                            espera7200R = numpy.mean(Array_Espera_R)

                        print('%7.2f'%(env.now), " Pasa el semaforo el auto: ", nombre)
                        #print("El tiempo es ahora: ", '%7.2f'%(env.now), "menos: ", '%7.2f'%(llegada), "por lo tanto la espera es de: ",'%7.2f'%(espera))

                else:
                    yield env.timeout(semaforo - env.now)
                    if control:
                        '''COLA_A = COLA_A - 1'''
                        if env.now<7200:
                            yield env.timeout(reaccion)
                            espera = env.now - llegada
                            Array_Espera_A = numpy.append(Array_Espera_A, espera)
                            Array_Espera_T = numpy.append(Array_Espera_T, espera)
                            Cola_YA -=1 
                            Cola_A -=1
                            if env.now == 1800:
                                cola1800 = Cola_YA
                                cola1800R = Cola_R
                                cola1800A = Cola_A
    
                                espera1800 = numpy.mean(Array_Espera_T)
                                espera1800A = numpy.mean(Array_Espera_A)
                                espera1800R = numpy.mean(Array_Espera_R)
                            if env.now == 3600:
                                cola3600 = Cola_YA
                                cola3600R = Cola_R
                                cola3600A = Cola_A
    
                                espera3600 = numpy.mean(Array_Espera_T)
                                espera3600A = numpy.mean(Array_Espera_A)
                                espera3600R = numpy.mean(Array_Espera_R)
                            if env.now == 5400:
                                cola5400 = Cola_YA
                                cola5400R = Cola_R
                                cola5400A = Cola_A
    
                                espera5400 = numpy.mean(Array_Espera_T)
                                espera5400A = numpy.mean(Array_Espera_A)
                                espera5400R = numpy.mean(Array_Espera_R)
                            if env.now == 7200:
                                cola7200 = Cola_YA
                                cola7200R = Cola_R
                                cola7200A = Cola_A
                               
                                espera7200 = numpy.mean(Array_Espera_T)
                                espera7200A = numpy.mean(Array_Espera_A)
                                espera7200R = numpy.mean(Array_Espera_R)
    
                            print('%7.2f'%(env.now), " Pasa el semaforo el auto: ", nombre)
                            
        
def autoR (env, nombre, servidor,id):
        #El carro llega y se va cuando esta en verde y es el primero
    if env.now < 7200:
        llegada = env.now

        global COLA_R
        global MAX_COLA_R

        global ESPERA_A
        global NOMBRE_A

        global espera_ot
        global espera_n
        global espera_nt
        global espera_d

        global espera_otA
        global espera_nA
        global espera_ntA
        global espera_dA

        global espera_otR
        global espera_nR
        global espera_ntR
        global espera_dR


        global Array_Cola_R
        global Array_Cola_T
        global Cola_YA

        global cola1800
        global cola3600
        global cola5400
        global cola7200

        global cola1800R
        global cola3600R
        global cola5400R
        global cola7200R

        global cola1800A
        global cola3600A
        global cola5400A
        global cola7200A

        global Cola_R


        global Array_Espera_T
        global Array_Espera_A
        global Array_Espera_R

        global espera1800
        global espera3600
        global espera5400
        global espera7200

        global espera1800A
        global espera3600A
        global espera5400A
        global espera7200A

        global espera1800R
        global espera3600R
        global espera5400R
        global espera7200R

        print ('%7.2f'%(env.now)," Llega el carro ", nombre)
        Array_Cola_R = numpy.append(Array_Cola_R,nombre)
        Array_Cola_T = numpy.append(Array_Cola_T,nombre)
        Cola_YA +=1 
        Cola_R +=1

        if id==2:
            with servidor.request() as req:
                results = yield req        
                if not control:
                    if env.now<7200:
                        yield env.timeout(reaccion)
                        espera = env.now - llegada
                        Array_Espera_R = numpy.append(Array_Espera_R, espera)
                        Array_Espera_T = numpy.append(Array_Espera_T, espera)
                        Cola_YA -=1 
                        Cola_R -=1
                        if env.now == 1800:
                            cola1800 = Cola_YA
                            cola1800R = Cola_R
                            cola1800A = Cola_A

                            espera1800 = numpy.mean(Array_Espera_T)
                            espera1800A = numpy.mean(Array_Espera_A)
                            espera1800R = numpy.mean(Array_Espera_R)
                        if env.now == 3600:
                            cola3600 = Cola_YA
                            cola3600R = Cola_R
                            cola3600A = Cola_A

                            espera3600 = numpy.mean(Array_Espera_T)
                            espera3600A = numpy.mean(Array_Espera_A)
                            espera3600R = numpy.mean(Array_Espera_R)
                        if env.now == 5400:
                            cola5400 = Cola_YA
                            cola5400R = Cola_R
                            cola5400A = Cola_A

                            espera5400 = numpy.mean(Array_Espera_T)
                            espera5400A = numpy.mean(Array_Espera_A)
                            espera5400R = numpy.mean(Array_Espera_R)
                        if env.now == 7200:
                            cola7200 = Cola_YA
                            cola7200R = Cola_R
                            cola7200A = Cola_A
                           
                            espera7200 = numpy.mean(Array_Espera_T)
                            espera7200A = numpy.mean(Array_Espera_A)
                            espera7200R = numpy.mean(Array_Espera_R)

                        print('%7.2f'%(env.now), " Pasa el semaforo el auto: ", nombre)
                        
                else:
                    yield env.timeout(semaforo - env.now)
                    if not control:
                        if env.now<7200:
                            yield env.timeout(reaccion)
                            espera = env.now - llegada
                            Array_Espera_R = numpy.append(Array_Espera_R, espera)
                            Array_Espera_T = numpy.append(Array_Espera_T, espera)
                            Cola_YA -=1 
                            Cola_R -=1
                            if env.now == 1800:
                                cola1800 = Cola_YA
                                cola1800R = Cola_R
                                cola1800A = Cola_A
    
                                espera1800 = numpy.mean(Array_Espera_T)
                                espera1800A = numpy.mean(Array_Espera_A)
                                espera1800R = numpy.mean(Array_Espera_R)
                            if env.now == 3600:
                                cola3600 = Cola_YA
                                cola3600R = Cola_R
                                cola3600A = Cola_A
    
                                espera3600 = numpy.mean(Array_Espera_T)
                                espera3600A = numpy.mean(Array_Espera_A)
                                espera3600R = numpy.mean(Array_Espera_R)
                            if env.now == 5400:
                                cola5400 = Cola_YA
                                cola5400R = Cola_R
                                cola5400A = Cola_A
    
                                espera5400 = numpy.mean(Array_Espera_T)
                                espera5400A = numpy.mean(Array_Espera_A)
                                espera5400R = numpy.mean(Array_Espera_R)
                            if env.now == 7200:
                                cola7200 = Cola_YA
                                cola7200R = Cola_R
                                cola7200A = Cola_A
                               
                                espera7200 = numpy.mean(Array_Espera_T)
                                espera7200A = numpy.mean(Array_Espera_A)
                                espera7200R = numpy.mean(Array_Espera_R)
    
                            print('%7.2f'%(env.now), " Pasa el semaforo el auto: ", nombre)
                            

        
##########################################################################


print('Simulacion semaforo Aramberri y Rayon')
print('Presentado por:')
print('Samir Valencia - 1629607')
print('Cristian Manosalva - 1628397')
print('Esneider Manzano - 1628373')
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
servidor = simpy.Resource(env, capacity=2)
servidor2 = simpy.Resource(env, capacity=2)

env.process(llegadaAramberri (env,ARAMBERRI, servidor))
env.process(llegadaRayonUno (env,RAYON_U, servidor2))
control = True
#Asignamos en segundos las 2 horas de simulacion
promedio = numpy.array([])
while env.now <7200:
        env.run(until=semaforo)
        if control :
            control = False
            semaforo +=rojoAramberri

        else:
            control = True
            semaforo +=verdeAramberri


#Grafica de Numero de Autos en cola segun la hora

horas = numpy.array(["8:30","9:00","9:30","10:00"])
numeroEnColaT= numpy.array([cola1800,cola3600,cola5400,cola7200])
numeroEnColaA= numpy.array([cola1800A,cola3600A,cola5400A,cola7200A])
numeroEnColaR= numpy.array([cola1800R,cola3600R,cola5400R,cola7200R])
plt.plot(horas,numeroEnColaT, color = 'k', linestyle = '-',linewidth = 2, marker = '|', label = 'Autos en cola')

plt.plot(horas,numeroEnColaA, color = 'r', linestyle = ':',linewidth = 2, marker = 'p', label='Autos en cola por Aramberri')

plt.plot(horas,numeroEnColaR, color = 'b', linestyle = '--',linewidth = 2, marker = 'p', label='Autos en cola por Rayon')

plt.xlabel('Horas de corte')
plt.ylabel('Autos en cola')
plt.title("Numero de Autos en cola segun la hora")

plt.tight_layout()
plt.legend()
plt.show()

'''
#Grafica de Segundos promedio de espera de los Autos en cola segun la hora

horas = numpy.array(["8:30","9:00","9:30","10:00"])
promedioEnColaT= numpy.array([espera1800,espera3600,espera5400,espera7200])
promedioEnColaA= numpy.array([espera1800A,espera3600A,espera5400A,espera7200A])
promedioEnColaR= numpy.array([espera1800R,espera3600R,espera5400R,espera7200R])
plt.plot(horas,promedioEnColaT, color = 'k', linestyle = '-',linewidth = 2, marker = '|', label = 'Promedio de tiempo en cola')

plt.plot(horas,promedioEnColaA, color = 'r', linestyle = ':',linewidth = 2, marker = 'p', label='Promedio de tiempo en cola por Aramberri')

plt.plot(horas,promedioEnColaR, color = 'b', linestyle = '--',linewidth = 2, marker = 'p', label='Promedio de tiempo en cola por Rayon')

plt.xlabel('Horas de corte')
plt.ylabel('Segundos en cola')
plt.title("Promedio de segundos en cola por Auto segun la hora")

plt.tight_layout()
plt.legend()
plt.show()
'''
#Histograma
'''

unique, counts = numpy.unique(Array_Espera_T, return_counts=True)
tablafre=numpy.asarray((unique, counts)).T

numMax= numpy.amax(tablafre, axis=0)[0]
numMin= numpy.amin(tablafre, axis=0)[0]
#Se calcula el rango
rango= numMax - numMin
#Se calcula el numero de intervalos
'''
'''
intervs = 1+ (3.322 * math.log(numpy.size(Array_Espera_T)))
intervs = math.ceil(intervs)
Array_Espera_T = numpy.sort(Array_Espera_T)

hist, bin_edges = numpy.histogram(Array_Espera_T, intervs)
plt.hist(Array_Espera_T, bins=bin_edges, range=rango,histtype='bar',color='m',label='Tiempos de espera general')
'''
'''
intervs = 1+ (3.322 * math.log(numpy.size(Array_Espera_A)))
intervs = math.ceil(intervs)
Array_Espera_T = numpy.sort(Array_Espera_A)
hist, bin_edges = numpy.histogram(Array_Espera_A, intervs)
plt.hist(Array_Espera_A, bins=bin_edges, range=rango,histtype='bar',color='g',label='Tiempos de espera Aramberri')
'''
'''
intervs = 1+ (3.322 * math.log(numpy.size(Array_Espera_R)))
intervs = math.ceil(intervs)
Array_Espera_T = numpy.sort(Array_Espera_R)
hist, bin_edges = numpy.histogram(Array_Espera_R, intervs)
plt.hist(Array_Espera_R, bins=bin_edges, range=rango,histtype='bar',color='g',label='Tiempos de espera para Rayon')
'''
'''
plt.xlabel('Tiempo de espera')
plt.ylabel('Cantidad de autos')
plt.title('Histograma tiempo de espera por intervalos')
plt.legend()
plt.show()
'''
