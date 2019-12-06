from Funktion import Funktion
from Grundklassen import Punkt
from Nullstellen_Frame import nullstellen_berechnen

import tkinter as tk
import math

class Krümmung_Frame(tk.Frame):

    __funktion = None

    def __init__(self, ableitung, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.update()
        self.ableitung = ableitung

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            tk.Label(self, text="Krümmung: aus zweiter Ableitung").grid(row=0, column=0, sticky=tk.W)
            if len(self.ableitung.funktionen) > 1:
                zweite_ableitung = Funktion()
                zweite_ableitung.set_funktion(self.ableitung.funktionen[1].funktion.funktion_user_x_ersetztbar)
                self.punkte = []
                num_wendepunkt = 0
                if zweite_ableitung != None:
                    tk.Label(self, text="f''(x) = " + zweite_ableitung.funktion_user_kurz).grid(row=1, column=1)
                else:
                    tk.Label(self, text="Ableitung f''(x) nicht bekannt").grid(row=1, column=0)
                if zweite_ableitung != None:
                    tk.Label(self, text="Eventuelle Wendepunkte durch f''(x) = 0:").grid(row=2, column=0, sticky=tk.W)
                    nullstellen, row = nullstellen_berechnen(zweite_ableitung, 3, self)
                    tk.Label(self, text="Überprüfen ob Nst Extrempunkte sind durch f'''(nst) ≠ 0:").grid(row=row + 1, column=0, sticky=tk.W)
                    for nst in nullstellen:
                        if len(self.ableitung.funktionen) > 2 and self.ableitung.funktionen[2] != None:
                            zweite_ableitung = Funktion()
                            zweite_ableitung.set_funktion(self.ableitung.funktionen[2].funktion.funktion_user_x_ersetztbar)
                            tk.Label(self, text="f'''(" + str(nst.x) + ") = " + zweite_ableitung.funktion_user_kurz).grid(row=row + 2, column=1)
                            if "x" in zweite_ableitung.funktion_user_x_ersetztbar:
                                tk.Label(self, text="f'''(" + str(nst.x) + ") = " + zweite_ableitung.funktion_user_x_ersetztbar.replace("x", str(nst.x))).grid(row=row + 3, column=1)
                            try:
                                self.erg = eval(zweite_ableitung.funktion_computer_readable.replace("x", "(" + str(nst.x) + ")"))
                                if isinstance(self.erg, complex):
                                    self.erg = None
                            except:
                                self.erg = None
                            if self.erg != None:
                                tk.Label(self, text="f'''(" + str(nst.x) + ") = " + str(self.erg)).grid(row=row + 4, column=1)
                                if self.erg == 0:
                                    tk.Label(self, text="Kein Wendepunkt, da f''' 0 ist.").grid(row=row + 5, column=0, sticky=tk.W)
                                else:
                                    num_wendepunkt += 1
                                    tk.Label(self, text="Wendepunkt, da f''' ≠ 0").grid(row=row + 5, column=0, sticky=tk.W)
                                    wp = Punkt(nst.x, eval(self.__funktion.funktion_computer_readable.replace("x", "(" + str(nst.x) + ")")), "WP" + str(num_wendepunkt))
                                    tk.Label(self, text="WP" + str(num_wendepunkt) + " = (" + str(round(nst.x, 3)) + "|f(" + str(round(nst.x, 3)) + ")) = " + str(wp)).grid(row=row + 6, column=0,sticky=tk.W)
                                    self.punkte.append(wp)
                            else:
                                tk.Label(self, text="f(0) = nicht definiert").grid(row=row + 4, column=1)
                                tk.Label(self, text="Kein Extrempunkt").grid(row=row + 5, column=0, sticky=tk.W)
                            row = row + 6
                        else:
                            pass
        else:
            tk.Label(self, text="Für Krümmung Funktion oben eingeben").grid(row=0, column=0)