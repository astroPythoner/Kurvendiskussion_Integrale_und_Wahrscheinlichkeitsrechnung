from Grundklassen import Graph, Punkt, Wiederholender_Punkt
import Funktion

import tkinter as tk

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import math

def smallest_in_array(array):
    smallest = None
    for i in array:
        if i is not None:
            smallest = i
            break
    if smallest == None:
        return None #no value in arrray
    for i in array:
        if i is not None and i < smallest:
            smallest = i
    return smallest

def biggest_in_array(array):
    biggest = None
    for i in array:
        if i is not None:
            biggest = i
            break
    if biggest == None:
        return None  # no value in arrray
    for i in array:
        if i is not None and i > biggest:
            biggest = i
    return biggest

class Graph_Frame(tk.Frame):

    __funktion = None
    __second_funktion = None
    sy = None
    nst = None
    abl = None
    steig = None
    kruem = None
    tanNor = None
    stamfunk = None
    integr = None
    sonst = None
    punkt_frames = {sy:"#008800o",nst:"#00CC00o",steig:"#CC2222o",kruem:"#FF22FFo",sonst:"#000033o"}
    funktion_frames = [abl,tanNor,stamfunk,sonst,integr]
    funktion_frames_aktiv = []
    flaechen_frames = [integr]
    flaechen_frames_aktiv = []
    aktiv = {"f(x)":True,"f'(x)":False,"f''(x)":False,"f'''(x)":False,"t(x)":False,"n(x)":False,"F(x)":False,"Integral":False}

    graph = None
    parameter = None

    def __init__(self, master=None,parameter=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.NSEW)
        self.start_x = tk.IntVar()
        self.start_x.set(-10)
        self.last_start_value = -10
        self.end_x = tk.IntVar()
        self.end_x.set(10)
        self.last_end_value = 10
        self.graph_aktiv = tk.BooleanVar()
        self.graph_aktiv.set(True)
        self.second_graph_aktiv = tk.BooleanVar()
        self.second_graph_aktiv.set(True)
        self.parameter = parameter
        self.graph = Graph(Funktion.Funktion(self.parameter,"0"),"blue","blau","f(x)")
        self.update()

    def add_frames(self,sy,nst,abl,tanNor,steig,kruem,stamfunk,integr,sonst):
        self.sy = sy
        self.nst = nst
        self.abl = abl
        self.steig = steig
        self.kruem = kruem
        self.tanNor = tanNor
        self.stamfunk = stamfunk
        self.integr = integr
        self.sonst = sonst
        self.punkt_frames = {self.sy:"#008800o",self.nst:"#00CC00o",self.steig:"#CC2222o",self.kruem:"#FF22FFo",self.sonst:"#000033o"}
        self.funktion_frames = [self.abl,self.tanNor,self.stamfunk,self.sonst,self.integr]
        self.funktion_frames_aktiv = []
        for frame in self.funktion_frames:
            try:
                for funktion in frame.funktionen:
                    self.funktion_frames_aktiv.append(tk.BooleanVar())
            except:
                pass
        self.flaechen_frames = [self.integr]
        self.flaechen_frames_aktiv = []
        for frame in self.funktion_frames:
            try:
                for flaeche in frame.flaechen:
                    self.flaechen_frames_aktiv.append(tk.BooleanVar())
            except:
                pass

    def update(self, neu_funktion = None, second_funktion=None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
            self.graph = Graph(self.__funktion, "blue", "blau", "f(x)")

            self.__second_funktion = None
            self.second_graph = None
            if second_funktion is not None:
                if second_funktion.funktion_user_kurz != "0" and second_funktion.funktion_user_kurz != "":
                    self.__second_funktion = second_funktion
                    self.second_graph = Graph(self.__second_funktion, "#008888", "blaugrau", "g(x)")

        self.funktion_frames_aktiv = []
        for frame in self.funktion_frames:
            try:
                for funktion in frame.funktionen:
                    var = tk.BooleanVar()
                    for ding in self.aktiv:
                        if funktion.name == ding:
                            var.set(self.aktiv[ding])
                    self.funktion_frames_aktiv.append(var)
            except:
                pass
        self.flaechen_frames = [self.integr]
        self.flaechen_frames_aktiv = []
        for frame in self.flaechen_frames:
            try:
                for flaeche in frame.flaechen:
                    var = tk.BooleanVar()
                    for ding in self.aktiv:
                        if flaeche.name == ding:
                            var.set(self.aktiv[ding])
                    self.flaechen_frames_aktiv.append(var)
            except:
                pass
        self.createWidgets()

    def bereich_update(self,value):
        value = int(value)
        if value < 0 and self.last_start_value != value:
            self.last_start_value = value
            self.createWidgets()
        if value > 0 and self.last_end_value != value:
            self.last_end_value = value
            self.createWidgets()

    def funktion_ausgewaehlt(self,funktion):
        if funktion in self.aktiv:
            self.aktiv[funktion] = not self.aktiv[funktion]
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            self.start_x_regler = tk.Scale(self, from_=-self.graph.max_x, to=-1, orient=tk.HORIZONTAL, variable = self.start_x)
            self.start_x_regler.config(command=self.bereich_update)
            self.start_x_regler.grid(row=0,column=0, sticky=tk.NSEW)
            self.end_x_regler = tk.Scale(self, from_=1, to=self.graph.max_x, orient=tk.HORIZONTAL, variable = self.end_x, command=self.bereich_update)
            self.end_x_regler.grid(row=0, column=1, sticky=tk.NSEW)
            self.checkbox_fx = tk.Checkbutton(self, text=self.graph.name+" ("+self.graph.color_name+")",variable=self.graph_aktiv,command=lambda: self.funktion_ausgewaehlt("f(x)")).grid(row=1, column=2, sticky=tk.NW)
            if self.__second_funktion is not None and self.second_graph is not None:
                self.checkbox_fx2 = tk.Checkbutton(self, text=self.second_graph.name + " (" + self.second_graph.color_name + ")", variable=self.second_graph_aktiv, command=lambda: self.funktion_ausgewaehlt("g(x)")).grid(row=2, column=2, sticky=tk.NW)
                add = 2
            else:
                add = 1

            num_funktion = 0
            for frame in self.funktion_frames:
                try:
                    for funktion in frame.funktionen:
                        num_funktion += 1
                        if funktion.name == "Mittelwert":
                            self.checkbox_graph_auswahl = tk.Checkbutton(self, text=funktion.name+" ("+funktion.color_name+")",variable=self.funktion_frames_aktiv[num_funktion-1],command=lambda a = funktion.name: self.funktion_ausgewaehlt(a)).grid(row=num_funktion+add+1,column=2,sticky=tk.NW)
                        else:
                            self.checkbox_graph_auswahl = tk.Checkbutton(self, text=funktion.name+" ("+funktion.color_name+")",variable=self.funktion_frames_aktiv[num_funktion-1],command=lambda a = funktion.name: self.funktion_ausgewaehlt(a)).grid(row=num_funktion+add,column=2,sticky=tk.NW)
                except:
                    pass
            num_flaeche = 0
            for frame in self.flaechen_frames:
                try:
                    for flaeche in frame.flaechen:
                        num_flaeche += 1
                        self.checkbox_flaeche_auswahl = tk.Checkbutton(self, text=flaeche.name + " (" + flaeche.color_name + ")", variable=self.flaechen_frames_aktiv[num_flaeche - 1],command=lambda a = flaeche.name: self.funktion_ausgewaehlt(a)).grid(row=num_funktion + add + num_flaeche + 1, column=2, sticky=tk.NW)
                except:
                    pass
            self.punkt_text = tk.Label(self, text="Punkte:").grid(row=1, column=3, sticky=tk.N)
            num_punkt = 0
            for frame in list(self.punkt_frames.keys()):
                try:
                    for punkt in frame.punkte:
                        num_punkt += 1
                        self.punkt_label = tk.Label(self, text=punkt.name+": "+str(punkt)).grid(row=num_punkt+1, column=3, sticky=tk.N)
                except:
                    pass

            self.draw_graph(rows=num_funktion+1+num_flaeche+1)
        else:
            self.funktion_text = tk.Label(self, text="Für Graph zeichnen Funktion oben eingeben")
            self.funktion_text.grid(row=0, column=0, sticky=tk.W)

    def draw_graph(self,rows=10):
        plt.clf()
        fig = plt.figure(1)

        canvas = FigureCanvasTkAgg(fig, self)
        plot_widget = canvas.get_tk_widget()

        x_start = self.start_x.get()*self.graph.genauigkeit+self.graph.max_x*self.graph.genauigkeit
        x_end = self.end_x.get()*self.graph.genauigkeit+self.graph.max_x*self.graph.genauigkeit+1

        # Funktion zeichnen
        if self.graph_aktiv.get():
            x_werte = []
            y_werte = []
            for count in range(x_end-x_start):
                wert = self.graph.y_werte[count+x_start]
                if wert is not None:
                    y_werte.append(wert)
                    x_werte.append(self.graph.x_werte[count+x_start])
                elif x_werte != [] and y_werte != []:
                    plt.plot(x_werte, y_werte,lineWidth=2,color=self.graph.color)
                    x_werte = []
                    y_werte = []
            if x_werte != [] and y_werte != []:
                plt.plot(x_werte, y_werte, lineWidth=2, color=self.graph.color)
        if self.second_graph_aktiv.get() and self.second_graph is not None:
            x_werte = []
            y_werte = []
            for count in range(x_end-x_start):
                wert = self.second_graph.y_werte[count+x_start]
                if wert is not None:
                    y_werte.append(wert)
                    x_werte.append(self.second_graph.x_werte[count+x_start])
                elif x_werte != [] and y_werte != []:
                    plt.plot(x_werte, y_werte,lineWidth=2,color=self.second_graph.color)
                    x_werte = []
                    y_werte = []
            if x_werte != [] and y_werte != []:
                plt.plot(x_werte, y_werte, lineWidth=2, color=self.second_graph.color)

        # Achsen zeichnen
        hoechster_y_wert = biggest_in_array(self.graph.y_werte[x_start:x_end])
        tiefster_y_wert = smallest_in_array(self.graph.y_werte[x_start:x_end])
        if self.second_graph_aktiv.get() and self.second_graph is not None:
            high = biggest_in_array(self.second_graph.y_werte[x_start:x_end])
            if high > hoechster_y_wert:
                hoechster_y_wert = high
            low = smallest_in_array(self.second_graph.y_werte[x_start:x_end])
            if low < tiefster_y_wert:
                tiefster_y_wert = low
        num_funktion = 0
        for frame in self.funktion_frames:
            try:
                for funktion in frame.funktionen:
                    num_funktion += 1
                    if self.funktion_frames_aktiv[num_funktion-1].get():
                       if biggest_in_array(funktion.y_werte[x_start:x_end]) > hoechster_y_wert:
                           hoechster_y_wert = biggest_in_array(funktion.y_werte[x_start:x_end])
                       if smallest_in_array(funktion.y_werte[x_start:x_end]) < tiefster_y_wert:
                           tiefster_y_wert = smallest_in_array(funktion.y_werte[x_start:x_end])
            except:
                pass
        # y-Achse
        if hoechster_y_wert == None or tiefster_y_wert == None:
            plt.plot([0,0], [-1,1], "black")
            plt.text(0, 1, 'Y', ha='center', va='bottom')
        else:
            if hoechster_y_wert<0:
                plt.plot([0,0], [0,smallest_in_array(self.graph.y_werte[x_start:x_end])],"black")
            elif tiefster_y_wert>0:
                plt.plot([0, 0], [biggest_in_array(self.graph.y_werte[x_start:x_end]),0], "black")
            else:
                plt.plot([0,0], [hoechster_y_wert,tiefster_y_wert],"black")
            plt.text(0,hoechster_y_wert, 'Y', ha='center', va='bottom')
        # x-Achse
        plt.plot([biggest_in_array(self.graph.x_werte[x_start:x_end]),smallest_in_array(self.graph.x_werte[x_start:x_end])], [0,0],"black")
        plt.text(biggest_in_array(self.graph.x_werte[x_start:x_end]), 0, 'X', ha='center', va='bottom')

        # Punkte
        if self.graph_aktiv.get():
            for frame in list(self.punkt_frames.keys()):
                try:
                    for punkt in frame.punkte:
                        if isinstance(punkt,Punkt):
                            if punkt.x>=self.start_x.get() and punkt.x<=self.end_x.get():
                                plt.text(punkt.x, punkt.y, punkt.name, ha='center', va='bottom')
                                plt.scatter(punkt.x,punkt.y, c=self.punkt_frames[frame][:-1], marker=self.punkt_frames[frame][-1:])
                        else:
                            for p in punkt.get_koordinaten_from_to(self.start_x.get(),self.end_x.get()):
                                plt.text(punkt.x, punkt.y, punkt.name, ha='center', va='bottom')
                                plt.scatter(p[0], p[1], c=self.punkt_frames[frame][:-1], marker=self.punkt_frames[frame][-1:])
                except:
                    pass

        # weitere Funktionen zeichnen (Ableitung,Kruemung,...)
        num_funktion = 0
        for frame in self.funktion_frames:
            try:
                for funktion in frame.funktionen:
                    num_funktion += 1
                    if self.funktion_frames_aktiv[num_funktion - 1].get():
                        x_werte = []
                        y_werte = []
                        for count in range(x_end - x_start):
                            wert = funktion.y_werte[count + x_start]
                            if wert is not None:
                                y_werte.append(wert)
                                x_werte.append(funktion.x_werte[count + x_start])
                            elif x_werte != [] and y_werte != []:
                                plt.plot(x_werte, y_werte, lineWidth=2, color=funktion.color)
                                x_werte = []
                                y_werte = []
                        if x_werte != [] and y_werte != []:
                            plt.plot(x_werte, y_werte, lineWidth=2, color=funktion.color)
            except:
                pass

        # Flaechen
        num_flaeche = 0
        for frame in self.flaechen_frames:
            try:
                for flaeche in frame.flaechen:
                    num_flaeche += 1
                    if self.flaechen_frames_aktiv[num_flaeche-1].get():
                        von_x = flaeche.von_x * self.graph.genauigkeit + self.graph.max_x * self.graph.genauigkeit
                        bis_x = flaeche.bis_x * self.graph.genauigkeit + self.graph.max_x * self.graph.genauigkeit + 1
                        if frame.zwischen_graphen:
                            matplotlib.pyplot.fill_between(self.graph.x_werte[von_x:bis_x],self.graph.y_werte[von_x:bis_x],self.second_graph.y_werte[von_x:bis_x], facecolor='0.9', edgecolor='0.6')
                        else:
                            verts = [(flaeche.von_x, 0), *zip(self.graph.x_werte[von_x:bis_x], self.graph.y_werte[von_x:bis_x]), (flaeche.bis_x, 0)]
                            poly = Polygon(verts, facecolor='0.9', edgecolor='0.6')
                            plt.axes().add_patch(poly)
            except:
                pass

        plot_widget.grid(row=1, column=0, columnspan=2, rowspan=rows)