from Grundklassen import Graph
from Funktion import Funktion

import tkinter as tk
import math

class Ableitung_Frame(tk.Frame):

    __funktion = None
    funktionen = []

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
            self.funktionen = []
            erste_ableitung,row_1 = self.ableiten(self.__funktion, 1, 0)
            if erste_ableitung != None:
                self.funktionen.append(Graph(erste_ableitung, "#990000","dunkelrot", "f'(x)"))
                zweite_ableitung, row_2 = self.ableiten(erste_ableitung, 2, row_1)
                if zweite_ableitung != None:
                    self.funktionen.append(Graph(zweite_ableitung, "#CC0000", "rot", "f''(x)"))
                    dritte_ableitung, row_3 = self.ableiten(zweite_ableitung, 3, row_2)
                    if dritte_ableitung != None:
                        self.funktionen.append(Graph(dritte_ableitung, "#FF0000","hellrot", "f'''(x)"))
        else:
            self.funktion_text = tk.Label(self, text="Für Ableitungen Funktion oben eingeben")
            self.funktion_text.grid(row=0, column=0)

    def ableiten(self,davor_abgeleitete_funktion,num_ableitung,row):
        ableitungsfunktion = None
        funktionsname = "f"
        for i in range(num_ableitung):
            funktionsname += "'"
        funktionsname_davor = funktionsname[:-1]+"(x)"
        funktionsname += "(x)"
        tk.Label(self, text=str(num_ableitung)+". Ableitung:").grid(row=row+1, column=0, columnspan=2, sticky=tk.W)
        tk.Label(self, text=funktionsname_davor+" = " + davor_abgeleitete_funktion.funktion_user_x_ersetztbar).grid(row=row+2, column=1)
        row = row+2
        if not "x" in davor_abgeleitete_funktion.funktion_user_x_ersetztbar:
            ableitungsfunktion = "0"
            tk.Label(self, text="Kein x enthalten:").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
            tk.Label(self, text=funktionsname+" = " + ableitungsfunktion).grid(row=row + 2, column=1)
            tk.Label(self, text=str(num_ableitung) + ". Ableitung: " + funktionsname + " = " + ableitungsfunktion).grid(row=row + 3, column=0, sticky=tk.W)
            row = row+3
        elif davor_abgeleitete_funktion.is_polinomfunktion:
            exponenten = davor_abgeleitete_funktion.exponenten_array
            tk.Label(self, text="In Exponentialform bringen:").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
            tk.Label(self, text=funktionsname_davor+" = " + davor_abgeleitete_funktion.funktion_exponential_x_ersetzbar).grid(row=row + 2,column=1)
            tk.Label(self, text="Ableiten nach Regel ax'b -> (a*b)*x'(b-1):").grid(row=row + 3, column=0, columnspan=2,sticky=tk.W)
            row = row + 3
            neue_exponenten = []
            neue_exponenten_kurz = []
            for exponent in exponenten:
                neue_exponenten.append(["(" + exponent[0] + "*" + exponent[1] + ")", "(" + exponent[1] + "-1)"])
                basis_wert = eval(davor_abgeleitete_funktion.funktion_to_computer_readable(self.__funktion.funktion_verschönern("((" + exponent[0] + ")*" + exponent[1] + ")")))
                if basis_wert >= 0:
                    basis_wert = "+" + str(basis_wert)
                else:
                    basis_wert = str(basis_wert)
                expo_wert = eval(self.__funktion.funktion_to_computer_readable(self.__funktion.funktion_verschönern("((" + exponent[1] + ")-1)")))
                if expo_wert < 0:
                    expo_wert = "(" + str(expo_wert) + ")"
                else:
                    expo_wert = str(expo_wert)
                neue_exponenten_kurz.append([basis_wert, expo_wert])
            expos_zu_funktion = ""
            expos_kurz_funktion = ""
            expos_ganz_kurz_funktion = ""
            for exponent_neu in neue_exponenten:
                expos_zu_funktion += exponent_neu[0] + "*x'" + exponent_neu[1]
            for exponent_kurz_neu in neue_exponenten_kurz:
                expos_kurz_funktion += str(exponent_kurz_neu[0]) + "*x'" + str(exponent_kurz_neu[1])
                if exponent_kurz_neu[0] == "+1" or exponent_kurz_neu[0] == "+1.0":
                    if exponent_kurz_neu[1] == "1" or exponent_kurz_neu[1] == "1.0":
                        expos_ganz_kurz_funktion += "+x"
                    elif exponent_kurz_neu[1] == "0" or exponent_kurz_neu[1] == "0.0":
                        expos_ganz_kurz_funktion += "+1"
                    else:
                        expos_ganz_kurz_funktion += "+x'" + str(exponent_kurz_neu[1])
                elif exponent_kurz_neu[0] == "+0" or exponent_kurz_neu[0] == "+0.0":
                    pass
                else:
                    if exponent_kurz_neu[1] == "1" or exponent_kurz_neu[1] == "1.0":
                        expos_ganz_kurz_funktion += str(exponent_kurz_neu[0]) + "*x"
                    elif exponent_kurz_neu[1] == "0" or exponent_kurz_neu[1] == "0.0":
                        expos_ganz_kurz_funktion += str(exponent_kurz_neu[0])
                    else:
                        expos_ganz_kurz_funktion += str(exponent_kurz_neu[0]) + "*x'" + str(exponent_kurz_neu[1])
            expos_zu_funktion = self.__funktion.funktion_verschönern(expos_zu_funktion)
            expos_kurz_funktion = self.__funktion.funktion_verschönern(expos_kurz_funktion)
            expos_ganz_kurz_funktion = self.__funktion.funktion_verschönern(expos_ganz_kurz_funktion)
            tk.Label(self, text=funktionsname+" = " + expos_zu_funktion).grid(row=row + 1, column=1)
            tk.Label(self, text=funktionsname+" = " + expos_kurz_funktion).grid(row=row + 2, column=1)
            tk.Label(self, text=funktionsname+" = " + expos_ganz_kurz_funktion).grid(row=row + 3, column=1)
            ableitungsfunktion = expos_ganz_kurz_funktion
            tk.Label(self, text=str(num_ableitung)+". Ableitung: "+funktionsname+" = " + ableitungsfunktion).grid(row=row + 4, column=0,sticky=tk.W)
            row = row+4
        else:
            tk.Label(self, text="Ableitung von nicht Polinomfunktionen comming soon").grid(row=row+1, column=0,columnspan=2,sticky=tk.W)
            row = row+1

        if ableitungsfunktion != None:
            f = Funktion()
            f.set_funktion(ableitungsfunktion)
            return f,row
        else:
            return None,row