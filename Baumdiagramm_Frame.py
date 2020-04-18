import tkinter as tk

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Baumdiagramm_Frame(tk.Frame):

    wahrscheinlichkeit_werte = None

    def __init__(self, master=None, wahrscheinlichkeit_werte=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.NSEW)
        self.wahrscheinlichkeit_werte = wahrscheinlichkeit_werte
        self.update()

    def update(self):
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.draw_graph()

    def draw_graph(self):
        durchgaenge = self.wahrscheinlichkeit_werte.anz_durchgaenge
        moeglichkeiten = self.wahrscheinlichkeit_werte.anz_moeglichkeiten

        if (durchgaenge in {1:20,2:10,3:5,4:3,5:2,6:2} and {1:20,2:10,3:5,4:3,5:2,6:2}[durchgaenge] >= moeglichkeiten) or (moeglichkeiten == 1 and durchgaenge <= 25):
            plt.clf()
            fig = plt.figure(1)

            canvas = FigureCanvasTkAgg(fig, self)
            plot_widget = canvas.get_tk_widget()

            plt.axis('off')

            plt.text(0, 0, "start", ha='center', va='bottom')
            plt.scatter(0, 0)
            self.draw_baum_ebene(durchgaenge,moeglichkeiten,1,0,self.wahrscheinlichkeit_werte.namen, plt)

            plot_widget.grid(row=0, column=0, sticky=tk.NSEW)

    def draw_baum_ebene(self,durchgaenge,moeglichkeiten,durchgang,pos,namen, plt):
        breite = moeglichkeiten ** durchgaenge
        for moeglich in range(moeglichkeiten):
            x = pos + breite * ((moeglich * 2 + 1) / (moeglichkeiten * 2)) - breite/2
            plt.plot([pos,x],[-durchgang+1,-durchgang],color='black')
            plt.text(x, -durchgang+0.1, namen[moeglich], ha='center', va='bottom')
            plt.scatter(x, -durchgang,color='black')
            if durchgang+1 <= self.wahrscheinlichkeit_werte.anz_durchgaenge:
                if self.wahrscheinlichkeit_werte.zuruecklegen:
                    self.draw_baum_ebene(durchgaenge - 1, moeglichkeiten, durchgang + 1,x,namen, plt)
                else:
                    neue_namen = []
                    for count,n in enumerate(namen):
                        if count != moeglich:
                            neue_namen.append(namen)
                    self.draw_baum_ebene(durchgaenge-1,moeglichkeiten-1,durchgang+1,x,namen, plt)