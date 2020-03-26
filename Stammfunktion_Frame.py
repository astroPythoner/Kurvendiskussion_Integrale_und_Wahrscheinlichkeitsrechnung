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


def make_stammfunktion(parameter,funktion,row,frame,name,print_stammfunktion=True):
    tk.Label(frame, text="f(x) = "+funktion.funktion_user_x_ersetztbar).grid(row=row, column=1)
    stammfunk = Funktion(parameter)
    if not "x" in funktion.funktion_user_kurz:
        stammfunk.set_funktion(str(funktion.x_einsetzen(0))+"*x")
        tk.Label(frame, text="Kein x enthalten: f(x) = a -> F(x) = a*x").grid(row=row+1, column=1)
        tk.Label(frame, text=name+" = "+stammfunk.funktion_user_kurz).grid(row=row+2, column=1)
    elif funktion.is_polynomfunktion:
        tk.Label(frame, text="Polynomfunktion aufleiten nach Formel a*x'b -> (a/(b+1))*x'(b+1)").grid(row=row+1, column=1,sticky=tk.W,columnspan=2)
        stammfunktion_kurz = ""
        stammfunktion_lang = ""
        for polynom in funktion.exponenten_array:
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
        tk.Label(frame, text=name+" = "+stammfunktion_lang).grid(row=row+2, column=1)
        tk.Label(frame, text=name+" = "+stammfunk.funktion_user_kurz).grid(row=row+3, column=1)
    elif funktion.is_trigonometrisch and funktion.trigonometrische_funktion != "tan":
        stammfunktion_ende = ""
        row_add = 0
        if funktion.trigonometrisch_d != 0:
            tk.Label(frame, text=" konstante Zahl mit x erweitern").grid(row=row+0, column=2,sticky = tk.W)
            tk.Label(frame, text=name+" = " + funktion.funktion_trigonometrisch_x_ersetzbar+"x").grid(row=row+1, column=1)
            stammfunktion_ende = vorzeichen_str(funktion.trigonometrisch_d,mitleerzeichen=True)+"x"
            row_add = 1
        if funktion.trigonometrische_funktion == "sin":
            tk.Label(frame, text=" Kettenregel sin(v(x)) -> -cos(v(x)) / v'(x)").grid(row=row+row_add, column=2, sticky=tk.W)
            tk.Label(frame, text=name+" = " + str(funktion.trigonometrisch_a) + " * -cos(" + n_mal_x_plus_m_to_string(funktion.trigonometrisch_b, -funktion.trigonometrisch_c) + ") / "+str(funktion.trigonometrisch_b)+" "+stammfunktion_ende).grid(row=row+row_add+1, column=1)
            stammfunk = Funktion(frame.parameter,str(-funktion.trigonometrisch_a/funktion.trigonometrisch_b)+" * cos("+n_mal_x_plus_m_to_string(funktion.trigonometrisch_b, -funktion.trigonometrisch_c)+") "+stammfunktion_ende)
        elif funktion.trigonometrische_funktion == "cos":
            tk.Label(frame, text=" Kettenregel cos(v(x)) -> sin(v(x)) / v'(x)").grid(row=row+row_add, column=2, sticky=tk.W)
            tk.Label(frame, text=name+" = " + str(funktion.trigonometrisch_a) + " * sin(" + n_mal_x_plus_m_to_string(funktion.trigonometrisch_b, -funktion.trigonometrisch_c) + ") / "+str(funktion.trigonometrisch_b)+" "+stammfunktion_ende).grid(row=row+row_add+1, column=1)
            stammfunk = Funktion(parameter,str(funktion.trigonometrisch_a/funktion.trigonometrisch_b)+" * sin("+n_mal_x_plus_m_to_string(funktion.trigonometrisch_b, -funktion.trigonometrisch_c)+") "+stammfunktion_ende)
        tk.Label(frame, text=name+" = "+stammfunk.funktion_user_kurz).grid(row=row+row_add+2, column=1)
    elif funktion.is_wurzel:
        stammfunktion_ende = ""
        row_add = 0
        if funktion.wurzel_d != 0:
            tk.Label(frame, text=" konstante Zahl mit x erweitern").grid(row=row+0, column=2,sticky = tk.W)
            tk.Label(frame, text=name+" = " +funktion.funktion_wurzel_x_ersetzbar+"x").grid(row=row+1, column=1)
            stammfunktion_ende = vorzeichen_str(funktion.wurzel_d,mitleerzeichen=True)+"*x"
            row_add = 1
        tk.Label(frame, text=" Kettenregel sqrt(v(x)) -> (2/3)*v(x)'(3/2) / v'(x)").grid(row=row+row_add, column=2, sticky=tk.W)
        tk.Label(frame, text=name+" = "+str(funktion.wurzel_a)+"* (2/3)*("+n_mal_x_plus_m_to_string(funktion.wurzel_b,-funktion.wurzel_c)+")'(3/2) / "+str(funktion.wurzel_b)+" "+stammfunktion_ende).grid(row=row+row+1, column=1,sticky=tk.W)
        bruch = bruch_kuerzen(2*funktion.wurzel_a,3*funktion.wurzel_b)
        if bruch[1] != 1:
            stammfunk = Funktion(parameter,"("+str(bruch[0])+"*("+n_mal_x_plus_m_to_string(funktion.wurzel_b,-funktion.wurzel_c)+")'(3/2) ) /"+str(bruch[1])+stammfunktion_ende)
        else:
            stammfunk = Funktion(parameter,str(bruch[0])+"*(" + n_mal_x_plus_m_to_string(funktion.wurzel_b,-funktion.wurzel_c) + ")'(3/2)" + stammfunktion_ende)
    else:
        could_be_solved = True
        try:
            loesung = sympy.integrate(funktion.funktion_sympy_readable, sympy.Symbol('x'))
            stammfunk = Funktion(parameter)
            funktion_erkannt = stammfunk.set_funktion(sympy.printing.sstr(loesung).replace("**", "'"))
            if funktion_erkannt:
                tk.Label(frame, text=name+" = " + stammfunk.funktion_user_kurz).grid(row=row+1, column=1)
            else:
                my_font = font.Font(family="Courier New")
                style = ttk.Style()
                style.configure("Fixed.TLabel", font=my_font)
                could_be_solved = False
                tk.Label(frame, text="Vielleicht hilft das: "+sympy.sstr(loesung).replace("**", "'")).grid(row=row+2, column=0, columnspan=2, sticky=tk.W)
                [ttk.Label(frame, text=line, style="Fixed.TLabel").grid(row=row+count+3, column=0, columnspan=2, sticky=tk.W) for count,line in enumerate(sympy.pretty(loesung).split("\n"))]
        except Exception:
            could_be_solved = False
        if not could_be_solved:
            tk.Label(frame, text="Stammfunktion konnte nicht erstellt werden").grid(row=row+1, column=0, columnspan=2, sticky=tk.W)
            return None,None
    if print_stammfunktion:
        tk.Label(frame, text="Stammfunktion: "+name+" = " + stammfunk.funktion_user_kurz).grid(row=row+4, column=0, sticky=tk.W, columnspan=2)
    return stammfunk,row+5

class Stammfunktion_Frame(tk.Frame):

    __funktion = None
    funktionen = []

    parameter = None

    def __init__(self, master=None,parameter=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.parameter = parameter
        self.update()

    def update(self, neu_funktion = None, second_funktion=None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
            self.funktionen = []
        self.createWidgets()

    def stammfunktion_bestimmen(self):
        stammfunk,row = make_stammfunktion(self.parameter,self.__funktion,0,self,"F(x)")
        if stammfunk is not None:
            self.funktionen = [Graph(stammfunk, "#443344", "grau", "F(x)")]

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        if self.__funktion != None:
            tk.Label(self, text="f(x) = "+self.__funktion.funktion_user_kurz).grid(row=0, column=1)
            self.stammfunktion_bestimmen()
        else:
            tk.Label(self, text="Für Stammfunktion Funktion oben eingeben").grid(row=0, column=0)