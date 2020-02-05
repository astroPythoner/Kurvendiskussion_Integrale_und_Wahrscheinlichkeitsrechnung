from Grundklassen import Punkt
from Funktion import Funktion

import tkinter as tk
import math

class Sonstiges_Frame(tk.Frame):

    __funktion = None
    punkte=[]

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.update()

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.punkte = []
        if self.__funktion != None:
            if self.__funktion.is_polynomfunktion:
                tk.Label(self, text="Polynomfunktion:").grid(row=0, column=0)
                tk.Label(self, text="f(x) = "+self.__funktion.funktion_polynom_x_ersetzbar).grid(row=1, column=0)
                tk.Label(self, text="Exponenten: "+str([eval(x) for x in self.__funktion.nur_exponenten])).grid(row=2, column=0)
                tk.Label(self, text="Basen:      "+str([eval(x) for x in self.__funktion.nur_basen])).grid(row=3, column=0)
                if self.__funktion.funktion_polynom_x_ersetzbar != self.__funktion.funktion_polynom_aufgefuellt_x_ersetzbar:
                    tk.Label(self, text="mit aufgefüllten Exponenten f(x) = "+self.__funktion.funktion_polynom_aufgefuellt_x_ersetzbar).grid(row=4, column=0)
            elif self.__funktion.is_logarithmus:
                tk.Label(self, text="Logarithmusfunktion").grid(row=0, column=0)
            elif self.__funktion.is_wurzel:
                tk.Label(self, text="Wurzelfunktion").grid(row=0, column=0)
            elif self.__funktion.is_trigonometrisch:
                tk.Label(self, text="trigonometrische Funktion").grid(row=0, column=0)
            elif self.__funktion.is_exponential:
                tk.Label(self, text="Exponentialfunktion").grid(row=0, column=0)
            else:
                tk.Label(self, text="Funktionstyp nicht bekannt").grid(row=0, column=0,sticky=tk.W)
                tk.Label(self, text="   Für eine Vollständige Rechnung gib eine Funktion einer dieser Typen ein:").grid(row=1, column=0,sticky=tk.W)
                tk.Label(self, text="      1. Polynomfunktion: ax'm + bx'n + cx + d").grid(row=2, column=0,sticky=tk.W)
                tk.Label(self, text="      2. Wurzelfunktion: a * (x-b)'(1/2) + c").grid(row=3, column=0,sticky=tk.W)
                tk.Label(self, text="      3. Logarithmusfunktion: a * log(b*(x-c), d) + e").grid(row=4, column=0,sticky=tk.W)
                tk.Label(self, text="      4. Trigonometrische Funktion: a * sin(b*(x-c)) + d").grid(row=5, column=0,sticky=tk.W)
                tk.Label(self, text="      5. Exponentialfunktion: a'x + b'x + c'x").grid(row=6, column=0,sticky=tk.W)
        else:
            tk.Label(self, text="Funktion oben eingeben").grid(row=0, column=0,sticky=tk.W)
            tk.Label(self, text="   Für eine Vollständige Rechnung gib eine Funktion einer dieser Typen ein:").grid(row=1, column=0,sticky=tk.W)
            tk.Label(self, text="      1. Polynomfunktion: ax'm + bx'n + cx + d").grid(row=2, column=0,sticky=tk.W)
            tk.Label(self, text="      2. Wurzelfunktion: a * (x-b)'(1/2) + c").grid(row=3, column=0,sticky=tk.W)
            tk.Label(self, text="      3. Logarithmusfunktion: a * log(b*(x-c), d) + e").grid(row=4, column=0,sticky=tk.W)
            tk.Label(self, text="      4. Trigonometrische Funktion: a * sin(b*(x-c)) + d").grid(row=5, column=0,sticky=tk.W)
            tk.Label(self, text="      5. Exponentialfunktion: a'x + b'x + c'x").grid(row=6, column=0,sticky=tk.W)