from Grundklassen import Punkt

import tkinter as tk
import math

class SchnittpunktYAchse_Frame(tk.Frame):

    __funktion = None
    punkte = []

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.update()

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
            self.punkte = []
            self.erg = self.__funktion.x_einsetzen(0)
            if self.erg != "nicht definiert":
                self.punkte.append(Punkt(0,self.erg,"Sy"))
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            tk.Label(self, text="Schnittpunkt mit Y-Achse ermittlen durch x = 0:").grid(row=0,column=0,columnspan=2,sticky=tk.W)
            tk.Label(self, text="f(x) = " + self.__funktion.funktion_user_kurz).grid(row=1, column=1)
            tk.Label(self, text="f(0) = " + self.__funktion.funktion_x_eingesetzt(0)).grid(row=2, column=1)
            if self.erg != "nicht definiert":
                tk.Label(self, text="f(0) = "+str(self.erg)).grid(row=3, column=1)
                tk.Label(self, text="Sy = "+str(self.punkte[0])).grid(row=4, column=0,sticky=tk.W)
            else:
                tk.Label(self, text="f(0) = nicht definiert").grid(row=3, column=1)
                tk.Label(self, text="Kein Schnittpunkt mit Y-Achse").grid(row=4, column=0, sticky=tk.W)
        else:
            tk.Label(self, text="Für Schnittpunktberechnung Funktion oben eingeben").grid(row=0, column=0)