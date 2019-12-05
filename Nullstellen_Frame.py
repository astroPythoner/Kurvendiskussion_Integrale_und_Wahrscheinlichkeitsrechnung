from Punkt import Punkt

import tkinter as tk
import math

class Nullstellen_Frame(tk.Frame):

    __funktion = None
    punkte = []

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

        if self.__funktion != None:
            tk.Label(self, text="Nullstellen ermittlen durch f(x) = 0:").grid(row=0, column=0, columnspan=2, sticky=tk.W)
            tk.Label(self, text="0 = " + self.__funktion.funktion_user_kurz).grid(row=1, column=1)
            row = 1
            if self.__funktion.is_exponential:
                exponenten = self.__funktion.exponenten_array
                nur_expos = self.__funktion.nur_exponenten
                nur_basen = self.__funktion.nur_basen
                if len(exponenten) == 1: #x=0 (0=mx'b -> x=0)
                    self.punkte.append(Punkt(0,0,"Nst"))
                    if self.__funktion.funktion_user_kurz[0] != "x":
                        tk.Label(self, text="| /("+nur_basen[0]+")").grid(row=row, column=2)
                        tk.Label(self, text="0 = x'"+nur_expos[0]).grid(row=row+1, column=1)
                        row += 1
                    tk.Label(self, text="| √").grid(row=row, column=2)
                    tk.Label(self, text=nur_expos[0]+"√0 = x").grid(row=row+1, column=1)
                    tk.Label(self, text="Nst = "+str(self.punkte[0])).grid(row=row+2, column=0)
                if len(exponenten) == 2 and '0' in exponenten:   #lineare Funktion - wurzel ziehen (0=mx'b+n -> -n/m=x'b -> x=b√(-n/m))
                    tk.Label(self, text="0 = ").grid(row=1, column=1)
                    self.punkte.append([0, 0])
            else:
                tk.Label(self, text="Nullstellen von nicht Exponentialfunktionen comming soon").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        else:
            tk.Label(self, text="Für Nullstellenberechnung Funktion oben eingeben").grid(row=0, column=0)