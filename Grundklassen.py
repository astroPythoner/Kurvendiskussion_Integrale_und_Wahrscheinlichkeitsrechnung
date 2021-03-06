import math
import threading
from time import sleep
import tkinter as tk
from PDF_writer import create_pdf

class Punkt:
    __slots__ = ('x','y','name')

    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name

    def get_koordinaten_array(self):
        return [self.x,self.y]

    def get_koordinaten_einzeln(self):
        return self.x, self.y

    def __repr__(self):
        return "("+str(round(self.x,5))+" | "+str(round(self.y,5))+")"

    def __cmp__(self, other):
        return self.x > other.x
    def __lt__(self, other):
        return self.x < other.x
    def __gt__(self, other):
        return self.x > other.x


class Wiederholender_Punkt:
    # Punkte vom Aufbau {a*k+b, k ∈ Z}
    # nur ganz Zahlen und nur lineare Funktionen

    __slots__ = ('funktion', 'x','y', 'name','steigend')

    def __init__(self, funktion, y, name):
        self.funktion = funktion
        self.y = y
        self.x = self.funktion.x_einsetzen(0)
        self.name = name
        wert1 = self.funktion.x_einsetzen(0)
        wert2 = self.funktion.x_einsetzen(1)
        if wert1 < wert2:
            self.steigend = True  # steigend
        elif wert1 > wert2:
            self.steigend = False # fallend
        else:
            self.steigend = None  # nicht erlaubt nur lineare Funktionen

    def get__kte_koordinate_array(self,k):
        wert = self.funktion.x_einsetzen(k)
        return [wert, self.y]

    def get_kte_koordinate_einzeln(self,k):
        wert = self.funktion.x_einsetzen(k)
        return wert, self.y

    def get_koordinaten_from_to(self,from_value,to_value):
        einsetzten = 0
        wert = self.funktion.x_einsetzen(einsetzten)
        if wert > from_value and self.steigend or wert < from_value and not self.steigend:
            merken = -1
        elif wert < from_value and self.steigend or wert > from_value and not self.steigend:
            merken = 1
        if wert != from_value:
            while True:
                einsetzten += merken
                if self.funktion.x_einsetzen(einsetzten) == from_value:
                    break
                if wert < from_value and self.funktion.x_einsetzen(einsetzten) > from_value:
                    break
                elif wert > from_value and self.funktion.x_einsetzen(einsetzten) < from_value:
                    break
                else:
                    wert = self.funktion.x_einsetzen(einsetzten)
        k_from = einsetzten
        einsetzten = 0
        wert = self.funktion.x_einsetzen(einsetzten)
        if wert > to_value and self.steigend or wert < to_value and not self.steigend:
            merken = -1
        elif wert < to_value and self.steigend or wert > to_value and not self.steigend:
            merken = 1
        if wert != to_value:
            while True:
                einsetzten += merken
                if self.funktion.x_einsetzen(einsetzten) == to_value:
                    break
                if wert < to_value and self.funktion.x_einsetzen(einsetzten) > to_value:
                    break
                elif wert > to_value and self.funktion.x_einsetzen(einsetzten) < to_value:
                    break
                else:
                    wert = self.funktion.x_einsetzen(einsetzten)
        k_to = einsetzten
        punkte = []
        for k in range(min([k_to,k_from]),max([k_to,k_from])+1):
            wert = self.funktion.x_einsetzen(k)
            if wert > from_value and wert < to_value:
                punkte.append([wert, self.y])
        return punkte

    def get_koordinaten_array(self):
        return [self.x,self.y]

    def get_koordinaten_einzeln(self):
        return self.x, self.y

    def __repr__(self):
        return "{"+self.funktion.funktion_user_kurz.replace("x","k")+", k ∈ Z}"

    def __cmp__(self, other):
        return self.x > other.x
    def __lt__(self, other):
        return self.x < other.x
    def __gt__(self, other):
        return self.x > other.x


class Graph:
    funktion = ""
    color = "red"
    color_name = "rot"
    name = ""
    x_werte = []
    y_werte = []

    # max_x ist maximaler x_wert in positive und negative x_richtung, genauegkeit ist die 'abtastrate' also bei 10 zumbeispiel in zehntel schritten   Tipp: max_x*genauigkeit sollten nicht über 10000 liegen da sonst Berechnungen lange dauern
    max_x = 100
    genauigkeit = 10

    def __init__(self,funktion,color,color_name,name):
        self.color = color
        self.color_name = color_name
        self.name = name
        self.neu_funktion(funktion)

    def neu_funktion(self,funktion):
        self.funktion = funktion
        self.x_werte = []
        for i in range(-(self.max_x * self.genauigkeit), (self.max_x * self.genauigkeit)):
            self.x_werte.append(i / self.genauigkeit)
        self.y_werte = []
        for x in self.x_werte:
            if funktion is not None:
                funktionswert_an_i = funktion.x_einsetzen(x)
                if funktionswert_an_i == "nicht definiert":
                    funktionswert_an_i = None
            else:
                funktionswert_an_i = None
            self.y_werte.append(funktionswert_an_i)


class Flaeche:
    face_color = "red"
    edge_color = "red"
    color_name = "rot"
    name = ""
    von_x = -1
    bis_x = 1

    def __init__(self,facecolor,edge_color,color_name,name):
        self.face_color = facecolor
        self.edge_color = edge_color
        self.color_name = color_name
        self.name = name


class Parameter(threading.Thread):
    wert = 0
    min_wert = -10
    max_wert = 10
    schrittweite = 0.5
    speed = 1.5

    __rising = True
    __moving = False
    __main_frame = None

    def __init__(self,main_frame):
        threading.Thread.__init__(self)
        self.__main_frame = main_frame

    def set_wert(self,wert):
        if self.min_wert <= wert <= self.max_wert:
            self.wert = round(wert,2)

    def run(self):
        self.__moving = True
        while self.__moving:
            if self.__rising:
                self.wert += self.schrittweite
            else:
                self.wert -= self.schrittweite
            self.wert = round(self.wert,2)
            if self.max_wert <= self.wert:
                self.wert = self.max_wert
                self.__rising = False
            elif self.min_wert >= self.wert:
                self.wert = self.min_wert
                self.__rising = True
            self.__main_frame.parameter_scale.set(self.wert)
            sleep(self.speed)
        threading.Thread.__init__(self)

    def stop(self):
        self.__moving = False

class Parameter_Settings(tk.Toplevel):

    schrittweiten = [0.05,0.1,0.2,0.25,0.5,0.75,1,1.5,2,2.5,5,7.5,10,15,20,25]
    speeds = [0.5,0.6,0.75,0.8,1,1.25,1.5,2,2.5,3,4,5,7.5,10]

    def __init__(self, parent, parameter):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.parameter = parameter

        self.title("Parameter einstellen")
        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        self.body(body)
        body.pack(padx=7, pady=7)
        self.initial_focus = body
        self.buttonbox()
        self.grab_set()
        self.initial_focus = self
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        tk.Label(master,text="Parameter Mindest- und Maximalwert").grid(row=0,column=0, columnspan=len(self.schrittweiten),sticky = tk.W)
        self.scale_1 = tk.Scale(master,from_=-50, to=50, orient=tk.HORIZONTAL)
        self.scale_1.grid(row=1,column=0, columnspan=len(self.schrittweiten),sticky = tk.EW)
        self.scale_1.set(self.parameter.min_wert)
        self.scale_2 = tk.Scale(master,from_=-50, to=50, orient=tk.HORIZONTAL)
        self.scale_2.grid(row=2, column=0, columnspan=len(self.schrittweiten),sticky = tk.EW)
        self.scale_2.set(self.parameter.max_wert)
        tk.Label(master,text="Schrittweite").grid(row=3,column=0, columnspan=len(self.schrittweiten),sticky = tk.W)
        self.schrittweite = tk.IntVar()
        if self.parameter.schrittweite in self.schrittweiten:
            self.schrittweite.set(self.schrittweiten.index(self.parameter.schrittweite))
        for count,schrittweite in enumerate(self.schrittweiten):
            tk.Radiobutton(master,text=str(schrittweite),variable=self.schrittweite,value=count).grid(row=4,column=count)
        tk.Label(master, text="Geschwindigkeit (Wartezeit nach Fertigstellung der Rechnung in Sekunden)").grid(row=5, column=0, columnspan=len(self.schrittweiten), sticky=tk.W)
        self.speed = tk.IntVar()
        if self.parameter.speed in self.speeds:
            self.speed.set(self.speeds.index(self.parameter.speed))
        for count, speed in enumerate(self.speeds):
            tk.Radiobutton(master, text=str(speed), variable=self.speed, value=count).grid(row=6,column=count)

    def buttonbox(self):
        box = tk.Frame(self)
        fertig = tk.Button(box, text="fertig", command=self.react)
        fertig.pack(side=tk.LEFT, padx=7, pady=7)
        box.pack()

    def react(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def apply(self):
        self.parameter.min_wert = min([self.scale_1.get(),self.scale_2.get()])
        self.parameter.max_wert = max([self.scale_1.get(),self.scale_2.get()])
        self.parameter.schrittweite = self.schrittweiten[self.schrittweite.get()]
        self.parameter.speed = self.speeds[self.speed.get()]


class PDF_Creator():
    funktion = ""
    second_funktion = ""

    draw_image = True
    draw_schnittpunkt_y_achse = True
    schnittpunkt_y_achse_texte = []
    draw_nullstellen = True
    nullstellen_texte = []
    draw_globales_verhalten = True
    globales_verhalten_texte = []
    draw_differenz_funktion = True
    differenz_funktion_texte = []
    draw_nullstellen_differenz_funktion = True
    nullstellen_differenz_funktion_texte = []
    draw_stammfunktion_differenzfunktion = True
    stammfunktion_differenzfunktion_texte = []
    draw_ableitung = True
    ableitung_texte = []
    draw_normale = True
    normale_texte = []
    draw_tangente = True
    tangente_texte = []
    draw_steigung = True
    steigung_texte = []
    draw_kruemmung = True
    kruemmung_texte = []
    draw_stammfunktion = True
    stammfunktion_texte = []
    draw_integral = True
    integral_texte = []

    def create_pdf(self,file_name,master,graph_frame):
        pdf = self
        class Loading_screen(tk.Toplevel):
            def __init__(self):
                tk.Toplevel.__init__(self, master)
                self.transient(master)
                self.title("Rechnung exportieren")
                tk.Label(self,text="Die Rechnung wird exporiert, dies kann einen Moment dauern").grid(row=0,column=0)
                self.update()
                self.initial_focus = self
                self.initial_focus.focus_set()
                graph_frame.export_image("image.png")
                create_pdf(file_name, pdf)
                self.withdraw()
                self.update_idletasks()
                master.focus_set()
                self.destroy()
        Loading_screen()

    def reset(self):
        self.schnittpunkt_y_achse_texte = []
        self.nullstellen_texte = []
        self.globales_verhalten_texte = []
        self.differenz_funktion_texte = []
        self.nullstellen_differenz_funktion_texte = []
        self.stammfunktion_differenzfunktion_texte = []
        self.ableitung_texte = []
        self.normale_texte = []
        self.tangente_texte = []
        self.steigung_texte = []
        self.kruemmung_texte = []
        self.stammfunktion_texte = []
        self.integral_texte = []

    def __getitem__(self, item):
        if item == 0: return self.draw_image
        if item == 1: return self.draw_schnittpunkt_y_achse
        if item == 2: return self.draw_nullstellen
        if item == 3: return self.draw_globales_verhalten
        if item == 4: return self.draw_differenz_funktion
        if item == 5: return self.draw_nullstellen_differenz_funktion
        if item == 6: return self.draw_stammfunktion_differenzfunktion
        if item == 7: return self.draw_ableitung
        if item == 8: return self.draw_normale
        if item == 9: return self.draw_tangente
        if item ==10: return self.draw_steigung
        if item ==11: return self.draw_kruemmung
        if item ==12: return self.draw_stammfunktion
        if item ==13: return self.draw_integral

class PDF_Settings(tk.Toplevel):

    def __init__(self, parent, creator:PDF_Creator):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.creator = creator
        self.vars = [tk.BooleanVar(value=creator[x]) for x in range(14)]

        self.title("PDF erstellen")
        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        self.body(body)
        body.pack(padx=7, pady=7)
        self.initial_focus = body
        self.buttonbox()
        self.grab_set()
        self.initial_focus = self
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        tk.Label(master,text="Inhalt des PDFs").grid(row=0,column=0, columnspan=2,sticky = tk.W)
        tk.Checkbutton(master, text="Graph",                                                            variable=self.vars[0]).grid(row=1,column=1,sticky = tk.W)
        tk.Checkbutton(master, text="Schnittpunkt mit der Y-Achse",                                     variable=self.vars[1]).grid(row=2, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Nullstellen",                                                      variable=self.vars[2]).grid(row=3, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Globales Verhalten",                                               variable=self.vars[3]).grid(row=4, column=1, sticky=tk.W)
        if self.creator.second_funktion != "":
            tk.Checkbutton(master, text="Differenzfunktion",                                                variable=self.vars[4]).grid(row=5, column=1, sticky=tk.W)
            tk.Checkbutton(master, text="Nullstellen der Differenzfunktion (Schnittpunkte der Funktionen)", variable=self.vars[5]).grid(row=6, column=1, sticky=tk.W)
            tk.Checkbutton(master, text="Stammfunktion der Differenzfunktion",                              variable=self.vars[6]).grid(row=7, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Ableitungen",                                                      variable=self.vars[7]).grid(row=8, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Normale",                                                          variable=self.vars[8]).grid(row=9, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Tangente",                                                         variable=self.vars[9]).grid(row=10, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Steigung (Extrempunkte)",                                          variable=self.vars[10]).grid(row=11, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Krümmung (Wendepunkte)",                                           variable=self.vars[11]).grid(row=12, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Stammfunktion",                                                    variable=self.vars[12]).grid(row=13, column=1, sticky=tk.W)
        tk.Checkbutton(master, text="Integral",                                                         variable=self.vars[13]).grid(row=14, column=1, sticky=tk.W)

    def buttonbox(self):
        box = tk.Frame(self)
        fertig = tk.Button(box, text="erstellen", command=self.react)
        fertig.pack(side=tk.LEFT, padx=7, pady=7)
        box.pack()

    def react(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def apply(self):
        self.creator.draw_image = self.vars[0].get()
        self.creator.draw_schnittpunkt_y_achse = self.vars[1].get()
        self.creator.draw_nullstellen = self.vars[2].get()
        self.creator.draw_globales_verhalten = self.vars[3].get()
        self.creator.draw_differenz_funktion = self.vars[4].get()
        self.creator.draw_nullstellen_differenz_funktion = self.vars[5].get()
        self.creator.draw_stammfunktion_differenzfunktion = self.vars[6].get()
        self.creator.draw_ableitung = self.vars[7].get()
        self.creator.draw_normale = self.vars[8].get()
        self.creator.draw_tangente = self.vars[9].get()
        self.creator.draw_steigung = self.vars[10].get()
        self.creator.draw_kruemmung = self.vars[11].get()
        self.creator.draw_stammfunktion = self.vars[12].get()
        self.creator.draw_integral = self.vars[13].get()


class Wahrscheinlichkeitsrechnung_werte():
    anz_durchgaenge = 1
    anz_moeglichkeiten = 1
    zuruecklegen = True
    namen = ["1"]
    chancen = ["1"]

    moeglich = True
    chancen_gleich = False

    def set_werte(self,anz_durchgaenge=None,anz_moeglichkeiten=None,zuruecklegen=None,namen=None,chancen=None):
        if anz_durchgaenge != None:
            self.anz_durchgaenge = anz_durchgaenge
        if anz_moeglichkeiten != None:
            self.anz_moeglichkeiten = anz_moeglichkeiten
        if zuruecklegen != None:
            self.zuruecklegen = zuruecklegen
        if namen != None:
            self.namen = namen
        if chancen != None:
            self.chancen=chancen
            self.chancen_gleich = True
            for chance in self.chancen:
                if chance != self.chancen[0]:
                    self.chancen_gleich = False
        self.moeglich = self.check_moeglich()

    def check_moeglich(self):
        summe = 0
        for chance in self.chancen:
            summe += eval(chance)
        if round(summe,6) != 1:
            return False
        if len(self.namen) != self.anz_moeglichkeiten:
            return False
        if len(self.chancen) != self.anz_moeglichkeiten:
            return False
        if not self.zuruecklegen and self.anz_moeglichkeiten<self.anz_durchgaenge:
            return False
        return True

    def append_name(self,name):
        self.namen.append(name)
    def append_chance(self, chance):
        self.chancen.append(chance)