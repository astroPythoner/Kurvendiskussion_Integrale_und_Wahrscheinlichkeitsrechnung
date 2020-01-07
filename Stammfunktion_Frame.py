import math
import tkinter as tk
from Funktion import Funktion, vorzeichen_str, polynom_to_str, bruch_kürzen
from Grundklassen import Graph


class Stammfunktion_Frame(tk.Frame):

    __funktion = None
    funktionen = []

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.update()

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
            self.funktionen = []
        self.createWidgets()


    def stammfunktion_bestimmen(self):
        stammfunk = Funktion()
        if not "x" in self.__funktion.funktion_user_kurz:
            stammfunk.set_funktion(str(eval(self.__funktion.funktion_user_kurz))+"*x")
            tk.Label(self, text="Kein x enthalten: f(x) = a -> F(x) = a*x").grid(row=1, column=1)
            tk.Label(self, text="F(x) = "+stammfunk.funktion_user_kurz).grid(row=2, column=1)
        elif self.__funktion.is_polynomfunktion:
            tk.Label(self, text="Polynomfunktion aufleiten nach Formel a*x'b -> (a/(b+1))*x'(b+1)").grid(row=1, column=0,sticky=tk.W,columnspan=2)
            stammfunktion_kurz = ""
            stammfunktion_lang = ""
            for polynom in self.__funktion.exponenten_array:
                if eval(polynom[1]) == -1:
                    stammfunktion_kurz += vorzeichen_str(str(eval(polynom[0]))+"*ln(x)")
                    stammfunktion_lang += vorzeichen_str(str(eval(polynom[0]))+"*ln(x)")
                else:
                    stammfunktion_lang += " + ("+str(eval(polynom[0]))+"/("+str(eval(polynom[1]))+"+1))*x'("+str(eval(polynom[1]))+"+1)"
                    zähler, nenner = bruch_kürzen(eval(polynom[0]), eval(polynom[1])+1)
                    if nenner == 1:
                        stammfunktion_kurz += polynom_to_str(zähler, eval(polynom[1])+1)
                    else:
                        stammfunktion_kurz += polynom_to_str("("+str(zähler)+"/"+str(nenner)+")",eval(polynom[1])+1)
            stammfunk.set_funktion(stammfunktion_kurz)
            tk.Label(self, text="F(x) = "+stammfunktion_lang).grid(row=2, column=1)
            tk.Label(self, text="F(x) = "+stammfunk.funktion_user_kurz).grid(row=3, column=1)
        else:
            tk.Label(self, text="Stammfunktion von nicht polynomfunktionen comming soon ...").grid(row=1, column=0,sticky=tk.W,columnspan=2)
            return
        tk.Label(self, text="Stammfunktion: F(x) = " + stammfunk.funktion_user_kurz).grid(row=4, column=0, sticky=tk.W, columnspan=2)
        self.funktionen = [Graph(stammfunk, "#443344", "grau", "F(x)")]

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        if self.__funktion != None:
            tk.Label(self, text="f(x) = "+self.__funktion.funktion_user_kurz).grid(row=0, column=1)
            self.stammfunktion_bestimmen()
        else:
            tk.Label(self, text="Für Stammfunktion Funktion oben eingeben").grid(row=0, column=0)