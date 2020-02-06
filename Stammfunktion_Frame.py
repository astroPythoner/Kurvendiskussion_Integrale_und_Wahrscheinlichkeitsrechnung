from Grundklassen import Graph
from Funktion import Funktion, vorzeichen_str, bruch_kuerzen, polynom_to_str

import tkinter as tk
import math
try:
    import sympy
except Exception:
    pass

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
                    zaehler, nenner = bruch_kuerzen(eval(polynom[0]), eval(polynom[1])+1)
                    if nenner == 1:
                        stammfunktion_kurz += polynom_to_str(zaehler, eval(polynom[1])+1)
                    else:
                        stammfunktion_kurz += polynom_to_str("("+str(zaehler)+"/"+str(nenner)+")",eval(polynom[1])+1)
            stammfunk.set_funktion(stammfunktion_kurz)
            tk.Label(self, text="F(x) = "+stammfunktion_lang).grid(row=2, column=1)
            tk.Label(self, text="F(x) = "+stammfunk.funktion_user_kurz).grid(row=3, column=1)
        else:
            could_be_solved = True
            try:
                loesung = sympy.integrate(self.__funktion.funktion_computer_readable, sympy.Symbol('x'))
                stammfunk = Funktion()
                funktion_erkannt = stammfunk.set_funktion(sympy.printing.sstr(loesung).replace("**", "'"))
                if funktion_erkannt:
                    tk.Label(self, text="F(x) = " + stammfunk.funktion_user_kurz).grid(row=1, column=1)
                else:
                    could_be_solved = False
                    tk.Label(self, text="Vielleicht hilft das: "+sympy.printing.sstr(loesung).replace("**", "'")).grid(row=2, column=0, columnspan=2, sticky=tk.W)
            except Exception:
                could_be_solved = False
            if not could_be_solved:
                tk.Label(self, text="Stammfunktion konnte nicht erstellt werden").grid(row=1, column=0, columnspan=2, sticky=tk.W)
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