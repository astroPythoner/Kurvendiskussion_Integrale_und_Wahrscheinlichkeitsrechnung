import tkinter as tk

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import math

class Graph_Frame(tk.Frame):

    __funktion = None
    x_cor = [0]
    y_cor = [0]
    sy = None
    nst = None
    steig = None
    kruem = None
    punkt_frames = {sy:"ro",nst:"go",steig:"yo",kruem:"lo"}

    # max_x ist maximaler x_wert in positive und negative x_richtung, genauegkeit ist die 'abtastrate' also bei 10 zumbeispiel in zehntel schritten   Tipp: max_x*genauigkeit sollten nicht über 10000 liegen da sonst Berechnungen lange dauern
    max_x = 100
    genauigkeit = 10

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.start_x = tk.IntVar()
        self.start_x.set(-10)
        self.last_start_value = -10
        self.end_x = tk.IntVar()
        self.end_x.set(10)
        self.last_end_value = 10
        self.update()

    def add_frames(self,sy,nst,steig,kruem):
        self.sy = sy
        self.nst = nst
        self.steig = steig
        self.kruem = kruem
        self.punkt_frames = {self.sy:"ro",self.nst:"go",self.steig:"yo",self.kruem:"lo"}

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.x_cor = []
        for i in range(-(self.max_x*self.genauigkeit), (self.max_x*self.genauigkeit)):
            self.x_cor.append(i/self.genauigkeit)
        self.y_cor = []
        for x in self.x_cor:
            if self.__funktion is not None:
                try:
                    funktionswert_an_i = eval(self.__funktion.funktion_computer_readable)
                    if isinstance(funktionswert_an_i,complex):
                        funktionswert_an_i = 0
                except Exception:
                    funktionswert_an_i = 0
            else:
                funktionswert_an_i = 0
            self.y_cor.append(funktionswert_an_i)
        self.createWidgets()

    def bereich_update(self,value):
        value = int(value)
        if value < 0 and self.last_start_value != value:
            self.last_start_value = value
            self.draw_graph()
        if value > 0 and self.last_end_value != value:
            self.last_end_value = value
            self.draw_graph()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            self.start_x_regler = tk.Scale(self, from_=-self.max_x, to=-1, orient=tk.HORIZONTAL, variable = self.start_x)
            self.start_x_regler.config(command=self.bereich_update)
            self.start_x_regler.grid(row=0,column=0, sticky=tk.NSEW)
            self.end_x_regler = tk.Scale(self, from_=1, to=self.max_x, orient=tk.HORIZONTAL, variable = self.end_x, command=self.bereich_update)
            self.end_x_regler.grid(row=0, column=1, sticky=tk.NSEW)

        else:
            self.funktion_text = tk.Label(self, text="Für Graph zeichnen Funktion oben eingeben")
            self.funktion_text.grid(row=0, column=0, sticky=tk.W)
        self.draw_graph()

    def draw_graph(self):
        plt.clf()
        fig = plt.figure(1)

        canvas = FigureCanvasTkAgg(fig, self)
        plot_widget = canvas.get_tk_widget()

        # Funktion zeichnen
        x_start = self.start_x.get()*self.genauigkeit+self.max_x*self.genauigkeit
        x_end = self.end_x.get()*self.genauigkeit+self.max_x*self.genauigkeit+1
        plt.plot(self.x_cor[x_start:x_end], self.y_cor[x_start:x_end])

        # Achsen zeichnen
        if max(self.y_cor[x_start:x_end])<0:
            plt.plot([0,0], [0,min(self.y_cor[x_start:x_end])],"black")
        elif min(self.y_cor[x_start:x_end])>0:
            plt.plot([0, 0], [max(self.y_cor[x_start:x_end]),0], "black")
        else:
            plt.plot([0,0], [max(self.y_cor[x_start:x_end]),min(self.y_cor[x_start:x_end])],"black")
        plt.text(0,max(self.y_cor[x_start:x_end]), 'Y', ha='center', va='bottom')
        plt.plot([max(self.x_cor[x_start:x_end]),min(self.x_cor[x_start:x_end])], [0,0],"black")
        plt.text(max(self.x_cor[x_start:x_end]), 0, 'X', ha='center', va='bottom')

        # Punkt
        for frame in list(self.punkt_frames.keys()):
            try:
                for punkt in frame.punkte:
                    plt.text(punkt[0], punkt[1], 'Sy', ha='center', va='bottom')
                    plt.plot([punkt[1]], [punkt[1]], self.punkt_frames[frame])
            except:
                pass

        plot_widget.grid(row=0, column=0)


        plot_widget.grid(row=1, column=0, columnspan=2)