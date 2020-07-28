from Grundklassen import Punkt, Wiederholender_Punkt, Graph
from Funktion import Funktion
from Nullstellen_Frame import nullstellen_berechnen
from Stammfunktion_Frame import make_stammfunktion

import tkinter as tk
import math
try:
    import sympy
except Exception:
    pass

class Sonstiges_Frame(tk.Frame):

    __funktion = None
    __second_funktion = None
    parameter = None
    punkte = []
    funktionen = []

    funktion_not_erkannt_reasons = {}

    def __init__(self, master=None,debug=False, parameter=None, pdf_writer=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.debug = debug
        self.parameter = parameter
        self.pdf_writer = pdf_writer
        self.update()

    def update(self, neu_funktion = None, second_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
            if second_funktion != None:
                self.__second_funktion = second_funktion
        self.createWidgets()

    def add_funktion_not_erkannt_reason(self,funktionstyp,reason):
        self.funktion_not_erkannt_reasons[funktionstyp] = reason

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.punkte = []
        self.funktionen = []
        if self.__funktion != None:
            ## Erste Funktion
            if self.__funktion.is_polynomfunktion:
                tk.Label(self, text="Polynomfunktion:").grid(row=0, column=0)
                tk.Label(self, text="f(x) = "+self.__funktion.funktion_polynom_x_ersetzbar).grid(row=1, column=0)
                tk.Label(self, text="Exponenten: "+str([eval(x) for x in self.__funktion.nur_exponenten])).grid(row=2, column=0)
                tk.Label(self, text="Basen: "+str([eval(x) for x in self.__funktion.nur_basen])).grid(row=3, column=0)
                if self.__funktion.funktion_polynom_x_ersetzbar != self.__funktion.funktion_polynom_aufgefuellt_x_ersetzbar:
                    tk.Label(self, text="mit aufgefüllten Exponenten f(x) = "+self.__funktion.funktion_polynom_aufgefuellt_x_ersetzbar).grid(row=4, column=0)
            elif self.__funktion.is_logarithmus:
                tk.Label(self, text="Logarithmusfunktion").grid(row=0, column=0)
            elif self.__funktion.is_wurzel:
                tk.Label(self, text="Wurzelfunktion ("+self.__funktion.funktion_wurzel_x_ersetzbar+")").grid(row=0, column=0)
                tk.Label(self, text="f(x) = " + self.__funktion.funktion_wurzel_x_ersetzbar).grid(row=1,column=0)
                tk.Label(self, text="a * sqrt(b(x-c)) + d:   a = " + str(self.__funktion.wurzel_a) + ", b = " + str(self.__funktion.wurzel_b) + ", c = " + str(self.__funktion.wurzel_c) + ", d = " + str(self.__funktion.wurzel_d)).grid(row=2,column=0)
            elif self.__funktion.is_trigonometrisch:
                tk.Label(self, text="trigonometrische Funktion ("+self.__funktion.trigonometrische_funktion+")").grid(row=0, column=0)
                tk.Label(self, text="f(x) = " + self.__funktion.funktion_trigonometrisch_x_ersetzbar).grid(row=1, column=0)
                tk.Label(self, text="a * "+self.__funktion.trigonometrische_funktion+"(b(x-c)) + d:   a = "+str(self.__funktion.trigonometrisch_a)+", b = "+str(self.__funktion.trigonometrisch_b)+", c = "+str(self.__funktion.trigonometrisch_c)+", d = "+str(self.__funktion.trigonometrisch_d)).grid(row=2, column=0)
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
            if self.__funktion.has_parameter:
                tk.Label(self, text="Funktion mit Paramter").grid(row=9, column=0)

            ## zweite Funktion -> Differenzfunktion u. Schnittpunkte
            if self.__second_funktion.funktion_user_kurz != "0" and self.__second_funktion.funktion_user_kurz != "":
                pdf = lambda txt: self.pdf_writer.differenz_funktion_texte.append(txt) if self.pdf_writer is not None else False
                tk.Label(self, text="").grid(row=7, column=0,sticky=tk.W)
                tk.Label(self, text="Zweite Funktion: g(x) = "+self.__second_funktion.funktion_user_kurz).grid(row=8, column=0, sticky=tk.W)
                # Differenzfunktion
                tk.Label(self, text="Differenzfunktion:",fg="blue4").grid(row=9, column=0, sticky=tk.E)
                tk.Label(self, text="d(x) = f(x) - g(x)",fg="blue2").grid(row=9, column=1, sticky=tk.W)
                pdf(["fkt","d(x) = f(x) - g(x)"])
                try:
                    simplified = sympy.simplify("("+self.__funktion.funktion_sympy_readable+") - ("+self.__second_funktion.funktion_sympy_readable+")")
                    differenzfunktion = Funktion(self.parameter)
                    could_be_simplified = differenzfunktion.set_funktion(sympy.printing.sstr(simplified).replace("**", "'"))
                except Exception:
                    could_be_simplified = False
                    differenzfunktion = Funktion(self.parameter)
                    could_be_simplified = differenzfunktion.set_funktion("("+self.__funktion.funktion_user_kurz+") - ("+self.__second_funktion.funktion_user_kurz+")")
                if could_be_simplified:
                    tk.Label(self, text="d(x) = (" + self.__funktion.funktion_user_kurz + ") - (" + self.__second_funktion.funktion_user_kurz + ")").grid(row=10, column=1, sticky=tk.W)
                    pdf(["fkt", "d(x) = (" + self.__funktion.funktion_user_kurz + ") - (" + self.__second_funktion.funktion_user_kurz + ")"])
                    tk.Label(self, text="d(x) = "+differenzfunktion.funktion_user_kurz,fg="green4").grid(row=11, column=1, sticky=tk.W)
                    pdf(["fkt", "d(x) = "+differenzfunktion.funktion_user_kurz])
                else:
                    tk.Label(self, text="d(x) = (" + self.__funktion.funktion_user_kurz + ") - (" + self.__second_funktion.funktion_user_kurz + ")",fg="green4").grid(row=10, column=1, sticky=tk.W)
                    pdf(["fkt", "d(x) = (" + self.__funktion.funktion_user_kurz + ") - (" + self.__second_funktion.funktion_user_kurz + ")"])
                self.funktionen.append(Graph(differenzfunktion, "#00C9C9", "hellblau", "d(x)"))
                # Schnittpunkte
                pdf = lambda txt: self.pdf_writer.nullstellen_differenz_funktion_texte.append(txt) if self.pdf_writer is not None else False
                tk.Label(self, text="Schnittpunkte:",fg="blue4").grid(row=12, column=0, sticky=tk.E)
                tk.Label(self, text="d(x) = 0",fg="blue2").grid(row=12, column=1)
                pdf(["fkt","d(x) = 0"])
                punkte,row = nullstellen_berechnen(self.parameter,differenzfunktion,13,self,print_nullstellen=False,pdf_writer=self.pdf_writer.nullstellen_differenz_funktion_texte)
                for count,punkt in enumerate(punkte):
                    y_wert = self.__funktion.x_einsetzen(punkt.x)
                    if isinstance(punkt,Punkt):
                        p = Punkt(punkt.x,y_wert,"Sp"+str(count+1))
                    else:
                        p = Wiederholender_Punkt(punkt.funktion,y_wert,"Sp"+str(count+1))
                    self.punkte.append(p)
                    tk.Label(self, text="Sp"+str(count+1)+" = ("+str(punkt.x)+" | f("+str(punkt.x)+")) = "+str(p),fg="green4").grid(row=row+count+1, column=1)
                    pdf(["erg", "Sp"+str(count+1)+" = ("+str(punkt.x)+" | f("+str(punkt.x)+")) = "+str(p)])
                # Stammfunktion der Differenzfunktion
                pdf = lambda txt: self.pdf_writer.stammfunktion_differenzfunktion_texte.append(txt) if self.pdf_writer is not None else False
                row = row+len(punkte)+1
                tk.Label(self, text="Stammfunktion der Differenzfunktion:",fg="blue4").grid(row=row, column=0, sticky=tk.E)
                stammfunk,row = make_stammfunktion(self.parameter, differenzfunktion, row, self, "D(x)",print_stammfunktion=False,pdf_writer=self.pdf_writer.stammfunktion_differenzfunktion_texte)
                if stammfunk is not None:
                    tk.Label(self, text="Stammfunktion: D(x) = " + stammfunk.funktion_user_kurz,fg="green4").grid(row=row + 5, column=1)
                    pdf(["erg","Stammfunktion: D(x) = " + stammfunk.funktion_user_kurz])
                    self.funktionen.append(Graph(stammfunk, "#00FFFF", "hellblau", "D(x)"))

            ## Debug
            if self.debug:
                tk.Label(self, text="Debug:").grid(row=row+10, column=0, sticky=tk.W)
                tk.Label(self, text="   kurz: " + self.__funktion.funktion_user_kurz).grid(row=row+11, column=0, sticky=tk.W)
                tk.Label(self, text="   x erstetzbar: " + self.__funktion.funktion_user_x_ersetztbar).grid(row=row+12, column=0, sticky=tk.W)
                tk.Label(self, text="   computer: " + self.__funktion.funktion_computer_readable).grid(row=row+13, column=0, sticky=tk.W)
                tk.Label(self, text="   sympy: " + self.__funktion.funktion_sympy_readable).grid(row=row+14, column=0, sticky=tk.W)
                tk.Label(self, text="Gründe für nicht erkannte Funktionen: ").grid(row=row+15, column=0, sticky=tk.W)
                for count, reason in enumerate(self.funktion_not_erkannt_reasons):
                    tk.Label(self, text="   " + reason + " : " + self.funktion_not_erkannt_reasons[reason]).grid(row=row+16 + count, column=0, sticky=tk.W)
                self.funktion_not_erkannt_reasons = {}
        ## keine Funktion eigegeben
        else:
            tk.Label(self, text="Funktion oben eingeben").grid(row=0, column=0,sticky=tk.W)
            tk.Label(self, text="   Für eine Vollständige Rechnung gib eine Funktion einer dieser Typen ein:").grid(row=1, column=0,sticky=tk.W)
            tk.Label(self, text="      1. Polynomfunktion: ax'm + bx'n + cx + d").grid(row=2, column=0,sticky=tk.W)
            tk.Label(self, text="      2. Wurzelfunktion: a * (x-b)'(1/2) + c").grid(row=3, column=0,sticky=tk.W)
            tk.Label(self, text="      3. Logarithmusfunktion: a * log(b*(x-c), d) + e").grid(row=4, column=0,sticky=tk.W)
            tk.Label(self, text="      4. Trigonometrische Funktion: a * sin(b*(x-c)) + d").grid(row=5, column=0,sticky=tk.W)
            tk.Label(self, text="      5. Exponentialfunktion: a'x + b'x + c'x").grid(row=6, column=0,sticky=tk.W)