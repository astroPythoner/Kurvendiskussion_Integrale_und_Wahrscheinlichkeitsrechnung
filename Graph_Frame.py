from Grundklassen import Graph

import tkinter as tk

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import math

class Graph_Frame(tk.Frame):

    __funktion = None
    sy = None
    nst = None
    abl = None
    steig = None
    kruem = None
    tanNor = None
    stamfunk = None
    integr = None
    punkt_frames = {sy:"#008800o",nst:"#00CC00o",steig:"#CC2222o",kruem:"#FF22FFo"}
    funktion_frames = [abl,tanNor,stamfunk]
    funktion_frames_aktiv = []
    flächen_frames = [integr]
    flächen_frames_aktiv = []

    graph = Graph("0","blue","blau","f(x)")

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.start_x = tk.IntVar()
        self.start_x.set(-10)
        self.last_start_value = -10
        self.end_x = tk.IntVar()
        self.end_x.set(10)
        self.last_end_value = 10
        self.graph_aktiv = tk.BooleanVar()
        self.graph_aktiv.set(True)
        self.update()

    def add_frames(self,sy,nst,abl,tanNor,steig,kruem,stamfunk,integr):
        self.sy = sy
        self.nst = nst
        self.abl = abl
        self.steig = steig
        self.kruem = kruem
        self.tanNor = tanNor
        self.stamfunk = stamfunk
        self.integr = integr
        self.punkt_frames = {self.sy:"#008800o",self.nst:"#00CC00o",self.steig:"#CC2222o",self.kruem:"#FF22FFo"}
        self.funktion_frames = [self.abl,self.tanNor,self.stamfunk]
        self.funktion_frames_aktiv = []
        for frame in self.funktion_frames:
            try:
                for funktion in frame.funktionen:
                    self.funktion_frames_aktiv.append(tk.BooleanVar())
            except:
                pass
        self.flächen_frames = [self.integr]
        self.flächen_frames_aktiv = []
        for frame in self.funktion_frames:
            try:
                for fläche in frame.flächen:
                    self.flächen_frames_aktiv.append(tk.BooleanVar())
            except:
                pass

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
            self.graph = Graph(self.__funktion,"blue","blau","f(x)")
        self.funktion_frames_aktiv = []
        for frame in self.funktion_frames:
            try:
                for funktion in frame.funktionen:
                    self.funktion_frames_aktiv.append(tk.BooleanVar())
            except:
                pass
        self.flächen_frames = [self.integr]
        self.flächen_frames_aktiv = []
        for frame in self.flächen_frames:
            try:
                for fläche in frame.flächen:
                    self.flächen_frames_aktiv.append(tk.BooleanVar())
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

    def funktion_ausgewählt(self):
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
            self.checkbox_fx = tk.Checkbutton(self, text=self.graph.name+" ("+self.graph.color_name+")",variable=self.graph_aktiv,command=self.funktion_ausgewählt).grid(row=1, column=2, sticky=tk.NW)

            num_funktion = 0
            for frame in self.funktion_frames:
                try:
                    for funktion in frame.funktionen:
                        num_funktion += 1
                        self.checkbox_graph_auswahl = tk.Checkbutton(self, text=funktion.name+" ("+funktion.color_name+")",variable=self.funktion_frames_aktiv[num_funktion-1],command=self.funktion_ausgewählt).grid(row=num_funktion+1,column=2,sticky=tk.NW)
                except:
                    pass
            num_fläche = 0
            for frame in self.flächen_frames:
                try:
                    for fläche in frame.flächen:
                        num_fläche += 1
                        self.checkbox_fläche_auswahl = tk.Checkbutton(self, text=fläche.name + " (" + fläche.color_name + ")", variable=self.flächen_frames_aktiv[num_fläche - 1],command=self.funktion_ausgewählt).grid(row=num_funktion + 1 + num_fläche + 1, column=2, sticky=tk.NW)
                except:
                    pass
            self.punkt_text = tk.Label(self, text="Punkte:").grid(row=1, column=3, sticky=tk.N)
            num_punkt = 0
            for frame in list(self.punkt_frames.keys()):
                try:
                    for punkt in frame.punkte:
                        if punkt.x>=self.start_x.get() and punkt.x<=self.end_x.get():
                            num_punkt += 1
                            self.punkt_label = tk.Label(self, text=punkt.name+": "+str(punkt)).grid(row=num_punkt+1, column=3, sticky=tk.N)
                except:
                    pass
            self.draw_graph(rows=num_funktion+1+num_fläche+1)
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
            plt.plot(self.graph.x_werte[x_start:x_end], self.graph.y_werte[x_start:x_end],lineWidth=2,color=self.graph.color)

        # Achsen zeichnen
        höchster_y_wert = max(self.graph.y_werte[x_start:x_end])
        tiefster_y_wert = min(self.graph.y_werte[x_start:x_end])
        num_funktion = 0
        for frame in self.funktion_frames:
            try:
                for funktion in frame.funktionen:
                    num_funktion += 1
                    if self.funktion_frames_aktiv[num_funktion-1].get():
                       if max(funktion.y_werte[x_start:x_end]) > höchster_y_wert:
                           höchster_y_wert = max(funktion.y_werte[x_start:x_end])
                       if min(funktion.y_werte[x_start:x_end]) < tiefster_y_wert:
                           tiefster_y_wert = min(funktion.y_werte[x_start:x_end])
            except:
                pass
        if höchster_y_wert<0:
            plt.plot([0,0], [0,min(self.graph.y_werte[x_start:x_end])],"black")
        elif tiefster_y_wert>0:
            plt.plot([0, 0], [max(self.graph.y_werte[x_start:x_end]),0], "black")
        else:
            plt.plot([0,0], [höchster_y_wert,tiefster_y_wert],"black")
        plt.text(0,max(self.graph.y_werte[x_start:x_end]), 'Y', ha='center', va='bottom')
        plt.plot([max(self.graph.x_werte[x_start:x_end]),min(self.graph.x_werte[x_start:x_end])], [0,0],"black")
        plt.text(max(self.graph.x_werte[x_start:x_end]), 0, 'X', ha='center', va='bottom')

        # Punkte
        if self.graph_aktiv.get():
            for frame in list(self.punkt_frames.keys()):
                try:
                    for punkt in frame.punkte:
                        if punkt.x>=self.start_x.get() and punkt.x<=self.end_x.get():
                            plt.text(punkt.x, punkt.y, punkt.name, ha='center', va='bottom')
                            plt.scatter(punkt.x,punkt.y, c=self.punkt_frames[frame][:-1], marker=self.punkt_frames[frame][-1:])
                except:
                    pass

        # weitere Funktionen zeichnen (Ableitung,Kruemung)
        num_funktion = 0
        for frame in self.funktion_frames:
            try:
                for funktion in frame.funktionen:
                    num_funktion += 1
                    if self.funktion_frames_aktiv[num_funktion-1].get():
                        plt.plot(funktion.x_werte[x_start:x_end], funktion.y_werte[x_start:x_end], color = funktion.color)
            except:
                pass

        # Flächen
        num_fläche = 0
        for frame in self.flächen_frames:
            try:
                for fläche in frame.flächen:
                    num_fläche += 1
                    if self.flächen_frames_aktiv[num_fläche-1].get():
                        von_x = fläche.von_x * self.graph.genauigkeit + self.graph.max_x * self.graph.genauigkeit
                        bis_x = fläche.bis_x * self.graph.genauigkeit + self.graph.max_x * self.graph.genauigkeit + 1
                        verts = [(fläche.von_x, 0), *zip(self.graph.x_werte[von_x:bis_x], self.graph.y_werte[von_x:bis_x]), (fläche.bis_x, 0)]
                        poly = Polygon(verts, facecolor='0.9', edgecolor='0.6')
                        plt.axes().add_patch(poly)
            except:
                pass

        plot_widget.grid(row=1, column=0, columnspan=2, rowspan=rows)