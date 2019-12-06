from Grundklassen import Punkt

import tkinter as tk
import math


def nullstellen_berechnen(funktion, row, frame):
    tk.Label(frame, text="0 = " + funktion.funktion_user_kurz).grid(row=row, column=1)
    punkte = []
    if not "x" in funktion.funktion_user_x_ersetztbar:
        if eval(funktion.funktion_computer_readable) == 0:
            tk.Label(frame, text="Ist immer null -> unendlich viele Nullstellen").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
        else:
            tk.Label(frame, text="Ist nie null -> keine Nullstelle").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
        row = row + 1
    elif funktion.is_polinomfunktion:
        exponenten = funktion.exponenten_array
        nur_expos = funktion.nur_exponenten
        nur_basen = funktion.nur_basen
        # x=0 (0=mx'b -> x=0)
        if len(exponenten) == 1:
            if funktion.funktion_user_kurz[0] != "x":
                tk.Label(frame, text="| /(" + nur_basen[0] + ")").grid(row=row, column=2, sticky=tk.W)
                tk.Label(frame, text="0 = x'" + nur_expos[0]).grid(row=row + 1, column=1)
                row += 1
            tk.Label(frame, text="| √").grid(row=row, column=2)
            tk.Label(frame, text=nur_expos[0] + "√0 = x").grid(row=row + 1, column=1)
            if eval(funktion.funktion_to_computer_readable(nur_expos[0])) < 0:
                tk.Label(frame, text="nicht definiert = x").grid(row=row + 2, column=1)
                tk.Label(frame, text="Keine Nullstelle").grid(row=row + 3, column=0, sticky=tk.W)
            else:
                punkte.append(Punkt(0, 0, "Nst"))
                tk.Label(frame, text="Nst = " + str(punkte[0])).grid(row=row + 2, column=0, sticky=tk.W)
            row = row + 3
        # wurzel ziehen (0=mx'b+n -> -n/m=x'b -> x=b√(-n/m))
        elif len(exponenten) == 2 and '0' in nur_expos:
            if nur_expos[0] == "0":
                n = nur_basen[0]
                m = nur_basen[1]
                b = eval(funktion.funktion_to_computer_readable(nur_expos[1]))
            else:
                n = nur_basen[1]
                m = nur_basen[0]
                b = eval(funktion.funktion_to_computer_readable(nur_expos[0]))
            minus_n = eval(funktion.funktion_to_computer_readable("-(" + n + ")"))
            tk.Label(frame, text="| " + str(minus_n)).grid(row=row, column=2, sticky=tk.W)
            tk.Label(frame, text=str(minus_n) + " = " + m + "x'" + str(b)).grid(row=row + 1, column=1)
            n_durch_m = eval(funktion.funktion_to_computer_readable("-(" + n + ")"))
            if funktion.funktion_user_kurz[0] != "x":
                tk.Label(frame, text="| /(" + m + ")").grid(row=row + 1, column=2, sticky=tk.W)
                n_durch_m = eval(funktion.funktion_to_computer_readable("-(" + n + ")/(" + (m) + ")"))
            tk.Label(frame, text=str(n_durch_m) + " = x'" + str(b)).grid(row=row + 2, column=1)
            doppel_erg_durch_wurzel = False
            if b != 1:
                tk.Label(frame, text="| √").grid(row=row + 2, column=2)
                tk.Label(frame, text=str(b) + "√(" + str(n_durch_m) + ") = x").grid(row=row + 3, column=1)
                if n_durch_m < 0 and b % 2 == 0:
                    erg = None
                else:
                    if b%2 == 0:
                        doppel_erg_durch_wurzel = True
                    b = b / 1.0
                    erg = n_durch_m ** (1 / b)
            else:
                erg = n_durch_m
            if erg != None and not isinstance(erg, complex):
                if doppel_erg_durch_wurzel:
                    punkte.append(Punkt(erg, 0, "Nst1"))
                    punkte.append(Punkt(-erg, 0, "Nst2"))
                    tk.Label(frame, text="Nst1 = " + str(punkte[0])).grid(row=row + 4, column=0, sticky=tk.W)
                    tk.Label(frame, text="Nst2 = " + str(punkte[1])).grid(row=row + 5, column=0, sticky=tk.W)
                else:
                    punkte.append(Punkt(erg, 0, "Nst"))
                    tk.Label(frame, text="Nst = " + str(punkte[0])).grid(row=row + 4, column=0, sticky=tk.W)
            else:
                tk.Label(frame, text="nicht definiert = x").grid(row=row + 4, column=1)
                tk.Label(frame, text="Keine Nullstelle").grid(row=row + 5, column=0)
            row = row + 5
        # x ausklammern (0=mx'b+nx'c -> 0=x'c*(mx'(b-c)+n) -> SVN)
        elif len(exponenten) == 2:
            b = max(nur_expos)
            c = min(nur_expos)
            m = nur_basen[nur_expos.index(b)]
            n = nur_basen[nur_expos.index(c)]
            b_minus_c = eval(funktion.funktion_to_computer_readable("("+str(b)+")-(" + str(c) + ")"))
            tk.Label(frame, text="x'"+c+" ausklammern").grid(row=row + 1, column=1)
            tk.Label(frame, text="0 = (x'"+str(c)+") * ("+str(m)+"x'"+str(b_minus_c)+" + "+str(n)+")").grid(row=row + 2, column=1)
            tk.Label(frame, text="Satz vom Nullprodukt").grid(row=row + 3, column=1)
            if eval(c) <= 0:
                tk.Label(frame, text="x1 = 0 ist keine Nullstelle").grid(row=row + 4, column=1)
            else:
                tk.Label(frame, text="x1 = 0").grid(row=row + 4, column=1)
                punkte.append(Punkt(0, 0, "Nst1"))
                tk.Label(frame, text="Nst1 = " + str(punkte[0])).grid(row=row + 5, column=0, sticky=tk.W)
                tk.Label(frame, text="x2 = "+str(m)+"x'"+str(b_minus_c)+" + "+str(n)).grid(row=row+6, column=1)
            row = row+6
            minus_n = eval(funktion.funktion_to_computer_readable("-(" + n + ")"))
            tk.Label(frame, text="| " + str(minus_n)).grid(row=row, column=2, sticky=tk.W)
            tk.Label(frame, text=str(minus_n) + " = " + str(m) + "x'" + str(b_minus_c)).grid(row=row + 1, column=1)
            tk.Label(frame, text="| /(" + m + ")").grid(row=row + 1, column=2, sticky=tk.W)
            n_durch_m = eval(funktion.funktion_to_computer_readable("(" + str(minus_n) + ")/(" + str(m) + ")"))
            tk.Label(frame, text=str(n_durch_m) + " = x'" + str(b_minus_c)).grid(row=row + 2, column=1)
            doppel_erg_durch_wurzel = False
            if b_minus_c != 1:
                tk.Label(frame, text="| √").grid(row=row + 2, column=2)
                tk.Label(frame, text=str(b_minus_c) + "√(" + str(n_durch_m) + ") = x").grid(row=row + 3, column=1)
                if n_durch_m < 0 and b_minus_c % 2 == 0:
                    erg = None
                else:
                    if b_minus_c % 2 == 0:
                        doppel_erg_durch_wurzel = True
                    b_minus_c = b_minus_c / 1.0
                    erg = n_durch_m ** (1 / b_minus_c)
            else:
                erg = n_durch_m
            if erg != None and not isinstance(erg, complex):
                if doppel_erg_durch_wurzel:
                    punkte.append(Punkt(erg, 0, "Nst1"))
                    punkte.append(Punkt(-erg, 0, "Nst2"))
                    tk.Label(frame, text="Nst2 = " + str(punkte[0])).grid(row=row + 4, column=0, sticky=tk.W)
                    tk.Label(frame, text="Nst3 = " + str(punkte[1])).grid(row=row + 5, column=0, sticky=tk.W)
                else:
                    punkte.append(Punkt(erg, 0, "Nst"))
                    tk.Label(frame, text="Nst2 = " + str(punkte[0])).grid(row=row + 4, column=0, sticky=tk.W)
            else:
                tk.Label(frame, text="nicht definiert = x").grid(row=row + 4, column=1)
                tk.Label(frame, text="Keine weitere Nullstelle").grid(row=row + 5, column=0)
            row = row + 5
        elif len(exponenten) == 3:  # evntl.Mitternachtsformel oder Poldi
            if "0" in nur_expos and "1" in nur_expos and "2" in nur_expos:
                a = eval(nur_basen[nur_expos.index("2")])
                b = eval(nur_basen[nur_expos.index("1")])
                c = eval(nur_basen[nur_expos.index("0")])
                tk.Label(frame, text="Mitternachtsfomel nach (-b±√(b'2-4ac))/2a)  a = "+str(a)+",  b = "+str(b)+",  c = "+str(c)).grid(row=row+1, column=1)
                diskriminante = b**2-4*a*c
                if diskriminante < 0:
                    tk.Label(frame, text="negative Wurzel -> Keine Nullstelle").grid(row=row + 2, column=1)
                else:
                    erg = (-b+(diskriminante**(1/2)))/(2*a)
                    if diskriminante == 0:
                        punkte.append(Punkt(erg, 0, "Nst1"))
                        tk.Label(frame, text="x = "+str(erg)).grid(row=row + 2, column=1)
                    else:
                        erg2 = (-b - (diskriminante ** (1 / 2))) / (2 * a)
                        punkte.append(Punkt(erg, 0, "Nst1"))
                        punkte.append(Punkt(erg2, 0, "Nst2"))
                        tk.Label(frame, text="x1 = "+str(erg)+"  x2 = "+str(erg2)).grid(row=row + 2, column=1)
                        tk.Label(frame, text="Nst1 = " + str(punkte[0])).grid(row=row + 3, column=0, sticky=tk.W)
                        tk.Label(frame, text="Nst2 = " + str(punkte[1])).grid(row=row + 4, column=0, sticky=tk.W)
                row = row+4
            else:
                tk.Label(frame, text="Poldi").grid(row=row+1, column=1)
            row = row + 1
        else:  # Poldi
            tk.Label(frame, text="Poldi").grid(row=row + 1, column=1)
            row = row+1
    else:
        tk.Label(frame, text="Nullstellen von nicht Polinomfunktionen comming soon").grid(row=row+1, column=0,columnspan=2, sticky=tk.W)
        row = row + 1
    return punkte,row

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
            tk.Label(self, text="Nullstellen ermittlen durch f(x) = 0:").grid(row=0, column=0, columnspan=2,sticky=tk.W)
            punkte,row = nullstellen_berechnen(self.__funktion,1,self)
            self.punkte = punkte
        else:
            tk.Label(self, text="Für Nullstellenberechnung Funktion oben eingeben").grid(row=0, column=0)