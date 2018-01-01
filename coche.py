# -*- coding: utf-8 -*-
#Sergio Alonso
#Helio Fernandez Abad
from __future__ import print_function
import random

def iniciarPuntuaciones(puntuaciones):  #Este metodo se encarga de leer, si existe, el fichero de puntuaciones y pone dichas puntuaciones en la lista.
    '''PRE:si hay un fichero de puntuaciones esta correctamente escrito'''
    i=0
    try:
        f=open("puntuaciones.txt","r")
        while i<len(puntuaciones):
            linea=f.readline()
            if not linea: break
            puntuaciones[i]=int(linea)
            i+=1
        f.close()
    except(IOError):
        None
    finally:return None
def guardarPuntuaciones(puntuaciones):  #Tiene como funcion guardar el contenido de la lista de puntuaciones en el fichero que contiene a las mismas.
    f=open("puntuaciones.txt","w")
    for i in range(len(puntuaciones)):   
        f.write(str(puntuaciones[i]))
        f.write("\n")
    f.close()
    return None
def generarPuntuaciones(numniveles):    #Este metodo se encarga de, si no hay puntuaciones previas, poner el valor de la puntuacion de cada nivel en -1, para asi indicar que el nivel no se ha completado.
    i=0
    puntuaciones=[]
    while i<numniveles:
        puntuaciones.append(-1)
        i+=1
    return puntuaciones
def actualizar(puntuaciones,nivel,pasos):   #Este es el metodo responsable de sustituir las puntuaciones almacenadas en el fichero, por las obtenidas durante la sesion de juego si y solo si, estas son puntuaciones mejores que las presentes en el fichero.
    if puntuaciones[nivel]==-1: puntuaciones[nivel]=pasos
    else:
        if puntuaciones[nivel]>pasos: puntuaciones[nivel]=pasos
    return None
def cargarNivel(nivel): #Este metodo se sirve del parametro nivel, obtenido en el selector de niveles, para devolver unicamente la informacion relativa al nivel que el usuario desea jugar.
    i,j=0,1
    infoNivel=[]
    try:
        f=open("niveles.txt","r")
        infoNivel=f.readlines()
        while i<nivel:
            j+=int(infoNivel[j])+1
            i+=1
        numcoches=int(infoNivel[j])
        infoNivel=infoNivel[j+1:j+1+numcoches]
        infoNivel=[Coche(infoNivel[i],i==0) for i in range(len(infoNivel))]
        f.close()
    except(IOError):
        print ("No se encontro el archivo de niveles")
        raise
    finally:return infoNivel
def comprobarMovimiento(coche,infoNivel,direccion): #Este es el metodo encargado de comprobar si el movimiento que el usuario intenta hacer es posible o no.
    if coche.orient=="H":
        y=coche.y
        if direccion==1:
            x=coche.x+coche.len
        else: x=coche.x-1
    else:
        x=coche.x
        if direccion==1:
            y=coche.y+coche.len
        else: y=coche.y-1
    if x==7 and y==3: return True
    if x<=0 or y<=0 or x>=7 or y>=7: return False
    i=0
    while i<len(infoNivel):
        if not infoNivel[i].casillaLibre(x,y): return False
        i+=1
    return True


img_2H=["data/ElATV(H).png","data/Elfalsoprofeta(elmartir)(H).png","data/Elmesias(H).png","data/JayLeno(H).png"]
img_2V=["data/ElATV(V).png","data/Elfalsoprofeta(elmartir)(V).png","data/Elmesias(V).png","data/JayLeno(V).png"]
img_3H=["data/Elangel(H).png","data/Elprincipe(H).png","data/Elrey(H).png"]
img_3V=["data/Elangel(V).png","data/Elprincipe(V).png","data/Elrey(V).png"]

class Coche:    #Aqui queda definida la clase coche.
    def __init__(self,info,first=False):    #Constructor de la clase Coche info es la informacion de cada coche en el formato de l fichero niveles.txt
        self.orient =info[0]
        self.x=int(info[1])
        self.y=int(info[2])
        self.len=int(info[3])
        if first:
            self.img="data/Eldios(H).png"
        else:
            if self.len==2:
                if self.orient=="H":
                    self.img=img_2H[random.randint(0, len(img_2H)-1)]
                else:
                    self.img=img_2V[random.randint(0, len(img_2V)-1)]
            else:
                if self.orient=="H":
                    self.img=img_3H[random.randint(0, len(img_3H)-1)]
                else:
                    self.img=img_3V[random.randint(0, len(img_3V)-1)]
        return None
    def move(self,direccion):   #Mueve el objeto coche en lña direccion indicada
        if self.orient=="H": self.x+=direccion
        else:self.y+=direccion
        return None
    def casillaLibre(self,x,y): #compruba si alguna de las casillas ocupadas por el coche es la casilla x,y
        cx,cy=self.x,self.y
        i=0
        while i<self.len: 
            if x==cx and y==cy:return False
            if self.orient=="H":cx+=1
            else:cy+=1
            i+=1
        return True   

        
        
    