from Grundklassen import Graph
from Funktion import Funktion, vorzeichen_str, bruch_kuerzen, n_mal_x_plus_m_to_string, polynom_to_str

import tkinter as tk
from tkinter import font
from tkinter import ttk
import math
try:
    import sympy
except Exception:
    pass

class Stammfunktion_Frame(tk.Frame):

    __funktion = None
    funktionen = []

    parameter = None

    def __init__(self, master=None,parameter=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.parameter = parameter
        self.update()

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
            self.funktionen = []
        self.createWidgets()

    def stammfunktion_bestimmen(self):
        stammfunk = Funktion(self.parameter)
        if not "x" in self.__funktion.funktion_user_kurz:
            stammfunk.set_funktion(str(self.__funktion.x_einsetzen(0))+"*x")
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
        elif self.__funktion.is_trigonometrisch and self.__funktion.trigonometrische_funktion != "tan":
            stammfunktion_ende = ""
            row = 0
            if self.__funktion.trigonometrisch_d != 0:
                tk.Label(self, text=" konstante Zahl mit x erweitern").grid(row=0, column=2,sticky = tk.W)
                tk.Label(self, text="F(x) = " +self.__funktion.funktion_trigonometrisch_x_ersetzbar+"x").grid(row=1, column=1)
                stammfunktion_ende = vorzeichen_str(self.__funktion.trigonometrisch_d,mitleerzeichen=True)+"x"
                row = 1
            if self.__funktion.trigonometrische_funktion == "sin":
                tk.Label(self, text=" Kettenregel sin(v(x)) -> -cos(v(x)) / v'(x)").grid(row=row, column=2, sticky=tk.W)
                tk.Label(self, text="F(x) = " + str(self.__funktion.trigonometrisch_a) + " * -cos(" + n_mal_x_plus_m_to_string(self.__funktion.trigonometrisch_b, -self.__funktion.trigonometrisch_c) + ") / "+str(self.__funktion.trigonometrisch_b)+" "+stammfunktion_ende).grid(row=row+1, column=1)
                stammfunk = Funktion(self.parameter,str(-self.__funktion.trigonometrisch_a/self.__funktion.trigonometrisch_b)+" * cos("+n_mal_x_plus_m_to_string(self.__funktion.trigonometrisch_b, -self.__funktion.trigonometrisch_c)+") "+stammfunktion_ende)
            elif self.__funktion.trigonometrische_funktion == "cos":
                tk.Label(self, text=" Kettenregel cos(v(x)) -> sin(v(x)) / v'(x)").grid(row=row, column=2, sticky=tk.W)
                tk.Label(self, text="F(x) = " + str(self.__funktion.trigonometrisch_a) + " * sin(" + n_mal_x_plus_m_to_string(self.__funktion.trigonometrisch_b, -self.__funktion.trigonometrisch_c) + ") / "+str(self.__funktion.trigonometrisch_b)+" "+stammfunktion_ende).grid(row=row+1, column=1)
                stammfunk = Funktion(self.parameter,str(self.__funktion.trigonometrisch_a/self.__funktion.trigonometrisch_b)+" * sin("+n_mal_x_plus_m_to_string(self.__funktion.trigonometrisch_b, -self.__funktion.trigonometrisch_c)+") "+stammfunktion_ende)
            tk.Label(self, text="F(x) = "+stammfunk.funktion_user_kurz).grid(row=row+2, column=1)
        else:
            could_be_solved = True
            try:
                loesung = sympy.integrate(self.__funktion.funktion_sympy_readable, sympy.Symbol('x'))
                stammfunk = Funktion(self.parameter)
                funktion_erkannt = stammfunk.set_funktion(sympy.printing.sstr(loesung).replace("**", "'"))
                if funktion_erkannt:
                    tk.Label(self, text="F(x) = " + stammfunk.funktion_user_kurz).grid(row=1, column=1)
                else:
                    my_font = font.Font(family="Courier New")
                    style = ttk.Style()
                    style.configure("Fixed.TLabel", font=my_font)
                    could_be_solved = False
                    tk.Label(self, text="Vielleicht hilft das: "+sympy.sstr(loesung).replace("**", "'")).grid(row=2, column=0, columnspan=2, sticky=tk.W)
                    [ttk.Label(self, text=line, style="Fixed.TLabel").grid(row=count+3, column=0, columnspan=2, sticky=tk.W) for count,line in enumerate(sympy.pretty(loesung).split("\n"))]
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