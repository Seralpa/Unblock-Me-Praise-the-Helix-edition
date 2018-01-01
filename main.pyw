#!/usr/bin/python
# -*- coding: UTF-8 -*-

#Sergio Alonso Pascual
#Helio Fernandez Abad
import gtk
from coche import *
offset=25
class App(gtk.Builder):
    def __init__(self):
        super(App,self).__init__()
        self.add_from_file("data/unblock_me.glade")
        
        self.connect_signals(self)
        
        self.menu_principal = self.get_object("Menu_principal")
        self.seleccion_niveles = self.get_object("Seleccion_niveles")
        self.juego=self.get_object("Ventana Tablero")
        self.victoria=self.get_object("Victoria")
        
        button_seleccionar_nivel=self.get_object("Seleccionar nivel")
        button_seleccionar_nivel.connect("clicked",self.jugar)
        
        self.menu_principal.show_all()
        
        self.tabla_niveles=self.get_object("table1").get_children()
        self.tablero=self.get_object("fixed1")
        
        self.puntuaciones=generarPuntuaciones(numniveles)
        iniciarPuntuaciones(self.puntuaciones)
        #self.nivel=0
        #self.infonivel=[]
        self.coches=[]
        self.arrastrando=False
        self.x0=0
        self.y0=0
        self.car_name=0
        #self.movimientos=0
    def salir(self,widget,data=None):   #pide una confirmacion para salir del juego cuando intentas cerrar una de las ventanas del juego o pulsas el boton "salir"
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_YES_NO,flags=gtk.DIALOG_MODAL,message_format="¿Estas seguro de que quieres salir?")
        response = dialog.run()
        if response == gtk.RESPONSE_YES:
            gtk.main_quit()
        else:
            dialog.destroy()
            return True
    def jugar(self,widget,data=None):   #muestra la ventana de seleccion de nivel
        for i in range(len(self.tabla_niveles)):
            if self.puntuaciones[i]!=-1:
                label="Nivel "+str(i+1)+": completado en "+str(self.puntuaciones[i])+" movimientos"
                self.tabla_niveles[i].connect("clicked",self.jugar_nivel)
            elif i==0 or self.puntuaciones[i-1]!=-1:
                label="Nivel "+str(i+1)+": no completado"
                self.tabla_niveles[i].connect("clicked",self.jugar_nivel)
            else:
                label="Nivel "+str(i+1)+": BLOQUEADO"
            self.tabla_niveles[i].set_label(label)
        self.victoria.hide()
        self.juego.hide()
        self.menu_principal.hide()
        self.seleccion_niveles.show_all()
        return None
    def reiniciar_estadisticas(self,widget,data=None):  #pide una doble confirmacion para resetear las puntuaciones
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_YES_NO,flags=gtk.DIALOG_MODAL,message_format="¿Estas seguro de que quieres borrar las puntuaciones?")
        response = dialog.run()
        if response == gtk.RESPONSE_YES:
            dialog.destroy()
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_YES_NO,flags=gtk.DIALOG_MODAL,message_format="Esto las eliminara para siempre (mucho tiempo)")
            response = dialog.run()
            if response == gtk.RESPONSE_YES:
                self.puntuaciones=generarPuntuaciones(numniveles)  
                guardarPuntuaciones(self.puntuaciones)
                self.seleccion_niveles = self.get_object("Seleccion_niveles")
                dialog.destroy()
            else:
                dialog.destroy()
        else:
            dialog.destroy()
        return None
    def jugar_nivel(self,widget,data=None): #se ocupa de dibujar los "coches en el tablero de juego y dibujar el mismo
        for i in range(len(self.tabla_niveles)):
            if self.tabla_niveles[i]==widget:
                self.nivel=i
        self.infonivel=cargarNivel(self.nivel)
        self.seleccion_niveles.hide()
        for i in self.coches:
            i.destroy()
        for i in range(len(self.infonivel)):
            car=gtk.EventBox()
            imagen=gtk.Image()
            imagen.set_from_file(self.infonivel[i].img)
            
            car.add(imagen)
            self.tablero.put(car,100*(self.infonivel[i].x-1)+offset,100*(self.infonivel[i].y-1)+offset)         
            car.set_events(gtk.gdk.BUTTON_PRESS_MASK |     #@UndefinedVariable
                           gtk.gdk.BUTTON_RELEASE_MASK |  #@UndefinedVariable
                           gtk.gdk.POINTER_MOTION_MASK)   #@UndefinedVariable
            car.connect("button_press_event", self.pulsacion)
            car.connect("button_release_event", self.evento_soltar)
            car.connect("motion_notify_event", self.evento_arrastrar)
        self.coches=self.tablero.get_children()
        del self.coches[0]
        label_nivel=self.get_object("Nivel jugando")
        label_nivel.set_label("Nivel que se esta jugando: "+str(self.nivel+1))
        label_record=self.get_object("label1")
        if self.puntuaciones[self.nivel]==-1:
            record="---"
        else:
            record=str(self.puntuaciones[self.nivel])
        label_record.set_label("Record actual: "+record)
        self.movimientos=0
        label_movimientos=self.get_object("Etiqueta 2")
        label_movimientos.set_label("Nº de movimientos: "+str(self.movimientos))
        
        self.validate_undo=False
        
        self.juego.show_all()
        return None
    def pulsacion(self, widget, event, data=None):  #detecta cuando se esta pulsando un "coche"
        # Para distinguir arrastrar de mover el ratón:
        self.arrastrando = True
        self.x0 = int(event.x_root)
        self.y0 = int(event.y_root)
        for i in range(len(self.coches)):
            if self.coches[i]==widget:
                self.car_name=i
                break
        self.prevX=self.infonivel[self.car_name].x
        self.prevY=self.infonivel[self.car_name].y
        self.validate_undo=True
        return gtk.TRUE
    def evento_arrastrar(self, widget, event, data=None):   #se ocupa del movimiento de los "coches"
        # Para no confundir arrastrar con sólo mover el ratón:
        if not self.arrastrando:
            return gtk.FALSE
        
        dx = int(event.x_root) - self.x0
        dy = int(event.y_root) - self.y0
        direccion=0
        if self.infonivel[self.car_name].orient=="H":
            if dx<0: 
                direccion=-1
            elif dx>0: 
                direccion=1
            if comprobarMovimiento(self.infonivel[self.car_name],self.infonivel,direccion):
                self.tablero.move(widget,(self.infonivel[self.car_name].x-1)*100+offset+dx,(self.infonivel[self.car_name].y-1)*100+offset)
                if abs(dx)>=100:
                    self.infonivel[self.car_name].move(direccion)
                    self.x0=int(event.x_root)
                    self.tablero.move(widget,(self.infonivel[self.car_name].x-1)*100+offset,(self.infonivel[self.car_name].y-1)*100+offset)
        else:
            if dy<0: 
                direccion=-1
            elif dy>0: 
                direccion=1
            if comprobarMovimiento(self.infonivel[self.car_name],self.infonivel,direccion):
                self.tablero.move(widget,(self.infonivel[self.car_name].x-1)*100+offset,(self.infonivel[self.car_name].y-1)*100+dy+offset)
                if abs(dy)>=100:
                    self.infonivel[self.car_name].move(direccion)
                    self.y0=int(event.y_root)
                    self.tablero.move(widget,(self.infonivel[self.car_name].x-1)*100+offset,(self.infonivel[self.car_name].y-1)*100+offset)
        return gtk.TRUE
    def evento_soltar(self, widget, event, data=None):  #ajusta la posicion final del "coche" y detecta si seha ganado la partida
        self.arrastrando = False
        # Desplazamiento final:
        x=self.tablero.child_get_property(widget,"x")-offset
        y=self.tablero.child_get_property(widget,"y")-offset
        if self.infonivel[self.car_name].orient=="H":
            if x//100+1<self.infonivel[self.car_name].x:
                if x%100<50:
                    if comprobarMovimiento(self.infonivel[self.car_name],self.infonivel,-1):
                        self.infonivel[self.car_name].move(-1)
            else:
                if x%100>=50:
                    if comprobarMovimiento(self.infonivel[self.car_name],self.infonivel,1):
                        self.infonivel[self.car_name].move(1)
        else:
            if y//100+1<self.infonivel[self.car_name].y:
                if y%100<50:
                    if comprobarMovimiento(self.infonivel[self.car_name],self.infonivel,-1):
                        self.infonivel[self.car_name].move(-1)
            else:
                if y%100>=50:
                    if comprobarMovimiento(self.infonivel[self.car_name],self.infonivel,1):
                        self.infonivel[self.car_name].move(1)
        self.tablero.move(widget,(self.infonivel[self.car_name].x-1)*100+offset,(self.infonivel[self.car_name].y-1)*100+offset)
        self.movimientos+=1
        label_movimientos=self.get_object("Etiqueta 2")
        label_movimientos.set_label("Nº de movimientos: "+str(self.movimientos))
        if self.infonivel[0].x==6:
            actualizar(self.puntuaciones,self.nivel,self.movimientos)
            guardarPuntuaciones(self.puntuaciones)
            label_nivel_completado=self.get_object("Etiqueta 7")
            label_nivel_completado.set_label("Nivel completado: "+str(self.nivel+1))
            label_movimientos=self.get_object("Etiqueta 8")
            label_movimientos.set_label("Nº de movimientos: "+str(self.movimientos))
            label_record=self.get_object("Etiqueta 9")
            label_record.set_label("Record del nivel: "+str(self.puntuaciones[self.nivel]))
            label_coches=self.get_object("Etiqueta 10")
            label_coches.set_label("Nº de coches: "+str(len(self.infonivel)))
            for i in self.coches:
                i.destroy()
            self.juego.hide()
            self.victoria.show_all()
        return gtk.TRUE 
    def mostrar_menu_principal(self,widget,data=None):  #muestra el menu principal
        self.juego.hide()
        self.seleccion_niveles.hide()
        self.victoria.hide()
        self.menu_principal.show_all()
        return None
    def reiniciar_nivel(self,widget,data=None): #elimina los "coches" que hay en ese momento y vuelve a cargar los del nivel en la posicion inicial reiniciando los movimientos
        for i in self.coches:
            i.destroy()
        self.infonivel=cargarNivel(self.nivel)
        for i in range(len(self.infonivel)):
            car=gtk.EventBox()
            imagen=gtk.Image()
            imagen.set_from_file(self.infonivel[i].img)
            
            car.add(imagen)
            self.tablero.put(car,100*(self.infonivel[i].x-1)+offset,100*(self.infonivel[i].y-1)+offset)         
            car.set_events(gtk.gdk.BUTTON_PRESS_MASK |     #@UndefinedVariable
                           gtk.gdk.BUTTON_RELEASE_MASK |  #@UndefinedVariable
                           gtk.gdk.POINTER_MOTION_MASK)   #@UndefinedVariable
            car.connect("button_press_event", self.pulsacion)
            car.connect("button_release_event", self.evento_soltar)
            car.connect("motion_notify_event", self.evento_arrastrar)
        self.juego.show_all()
        self.coches=self.tablero.get_children()
        del self.coches[0]
        self.movimientos=0
        label_movimientos=self.get_object("Etiqueta 2")
        label_movimientos.set_label("Nº de movimientos: "+str(self.movimientos))
        self.validate_undo=False
    def siguiente_nivel(self,widget,data=None): #carga el tablero del siguiente nivel
        if self.nivel+1==20:
            self.victoria.hide()
            self.juego.show_all()
            return None
        self.victoria.hide()
        self.nivel+=1
        self.infonivel=cargarNivel(self.nivel)
        for i in range(len(self.infonivel)):
            car=gtk.EventBox()
            imagen=gtk.Image()
            imagen.set_from_file(self.infonivel[i].img)
            
            car.add(imagen)
            self.tablero.put(car,100*(self.infonivel[i].x-1)+offset,100*(self.infonivel[i].y-1)+offset)         
            car.set_events(gtk.gdk.BUTTON_PRESS_MASK |     #@UndefinedVariable
                           gtk.gdk.BUTTON_RELEASE_MASK |  #@UndefinedVariable
                           gtk.gdk.POINTER_MOTION_MASK)   #@UndefinedVariable
            car.connect("button_press_event", self.pulsacion)
            car.connect("button_release_event", self.evento_soltar)
            car.connect("motion_notify_event", self.evento_arrastrar)
        self.juego.show_all()
        self.coches=self.tablero.get_children()
        del self.coches[0]
        self.movimientos=0
        self.validate_undo=False
        label_nivel=self.get_object("Nivel jugando")
        label_nivel.set_label("Nivel que se esta jugando: "+str(self.nivel+1))
        label_movimientos=self.get_object("Etiqueta 2")
        label_movimientos.set_label("Nº de movimientos: "+str(self.movimientos))
        label_record=self.get_object("label1")
        if self.puntuaciones[self.nivel]==-1:
            record="---"
        else:
            record=str(self.puntuaciones[self.nivel])
        label_record.set_label("Record actual: "+record)
        return None
    def deshacer(self,widget,data=None):
        if not self.validate_undo:
            return None
        self.infonivel[self.car_name].x=self.prevX
        self.infonivel[self.car_name].y=self.prevY
        self.tablero.move(self.coches[self.car_name],(self.prevX-1)*100+offset,(self.prevY-1)*100+offset)
        self.movimientos-=1
        label_movimientos=self.get_object("Etiqueta 2")
        label_movimientos.set_label("Nº de movimientos: "+str(self.movimientos))
        self.validate_undo=False
        return None
try:
    fniveles=open("niveles.txt","r")
    numniveles=int(fniveles.readline())
    fniveles.close()
except(IOError):
    print("No se encontro el fichero de niveles")
    raise 
unblock_me_Helix_edition=App()
gtk.main()















