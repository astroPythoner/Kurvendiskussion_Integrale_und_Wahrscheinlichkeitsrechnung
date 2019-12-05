from Grundklassen import Punkt

import tkinter as tk
import math


def nullstellen_berechnen(funktion, row, frame):
    tk.Label(frame, text="0 = " + funktion.funktion_user_kurz).grid(row=row, column=1)
    punkte = []
    if funktion.is_exponential:
        exponenten = funktion.exponenten_array
        nur_expos = funktion.nur_exponenten
        nur_basen = funktion.nur_basen
        if len(exponenten) == 1:  # x=0 (0=mx'b -> x=0)
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
        elif len(exponenten) == 2 and '0' in nur_expos:  # lineare Funktion - wurzel ziehen (0=mx'b+n -> -n/m=x'b -> x=b√(-n/m))
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
        elif len(exponenten) == 2:  # lineare Funktion - wurzel ziehen (0=mx'b+nx'c -> 0=x'c*(mx'(b-c)+n) -> SVN)
            tk.Label(frame, text="x ausklammern").grid(row=row + 1, column=1, sticky=tk.W)
            row = row + 1
        elif len(exponenten) == 3:  # evntl.Mitternachtsformel oder Poldi
            tk.Label(frame, text="evntl mit Mitternachtsfomel lösbar ansonsten Poldi").grid(row=1, column=1)
            row = row + 1
        else:  # Poldi
            tk.Label(frame, text="Poldi").grid(row=row + 1, column=1)
            row = row+1
    else:
        tk.Label(frame, text="Nullstellen von nicht Exponentialfunktionen comming soon").grid(row=row+1, column=0,columnspan=2, sticky=tk.W)
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
            punkte = nullstellen_berechnen(self.__funktion,1,self)
            self.punkte = punkte
        else:
            tk.Label(self, text="Für Nullstellenberechnung Funktion oben eingeben").grid(row=0, column=0)