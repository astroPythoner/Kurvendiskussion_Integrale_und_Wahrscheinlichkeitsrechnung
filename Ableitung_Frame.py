from Grundklassen import Graph
from Funktion import Funktion, n_mal_x_plus_m_to_string, polynom_array_to_str, vorzeichen_str

import tkinter as tk
import math
try:
    import sympy
except Exception:
    pass

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
            if isinstance(erste_ableitung, Funktion):
                self.funktionen.append(Graph(erste_ableitung, "#990000","dunkelrot", "f'(x)"))
                zweite_ableitung, row_2 = self.ableiten(erste_ableitung, 2, row_1)
                if isinstance(zweite_ableitung, Funktion):
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
            ableitungsfunktion = Funktion("0")
            tk.Label(self, text="Kein x enthalten:").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
            tk.Label(self, text=funktionsname+" = 0").grid(row=row + 2, column=1)
            tk.Label(self, text=str(num_ableitung) + ". Ableitung: " + funktionsname + " = 0").grid(row=row + 3, column=0, sticky=tk.W)
            row = row+3
        elif davor_abgeleitete_funktion.is_polynomfunktion:
            exponenten = davor_abgeleitete_funktion.exponenten_array
            tk.Label(self, text="In Exponentialform bringen:").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
            tk.Label(self, text=funktionsname_davor+" = " + davor_abgeleitete_funktion.funktion_polynom_x_ersetzbar).grid(row=row + 2,column=1)
            tk.Label(self, text="Ableiten nach Regel ax'b -> (a*b)*x'(b-1):").grid(row=row + 3, column=0, columnspan=2,sticky=tk.W)
            row = row + 3
            neue_exponenten = []
            neue_exponenten_kurz = []
            for exponent in exponenten:
                neue_exponenten.append(["(" + exponent[0] + "*" + exponent[1] + ")", "(" + exponent[1] + "-1)"])
                basis_wert = eval(davor_abgeleitete_funktion.funktion_to_computer_readable(self.__funktion.funktion_verschoenern("((" + exponent[0] + ")*" + exponent[1] + ")")))
                expo_wert = eval(self.__funktion.funktion_to_computer_readable(self.__funktion.funktion_verschoenern("((" + exponent[1] + ")-1)")))
                neue_exponenten_kurz.append([basis_wert, expo_wert])
            poly_funktion = ""
            poly_funktion_kurz = ""
            for poly_num in range(0,len(neue_exponenten)):
                poly_funktion += vorzeichen_str(neue_exponenten[poly_num][0] + "*x'" + neue_exponenten[poly_num][1],True)
                poly_funktion_kurz += polynom_array_to_str(neue_exponenten_kurz[poly_num])
            ableitungsfunktion = Funktion(poly_funktion_kurz)
            tk.Label(self, text=funktionsname+" = " + poly_funktion).grid(row=row + 1, column=1)
            tk.Label(self, text=funktionsname+" = " + ableitungsfunktion.funktion_user_kurz).grid(row=row + 2, column=1)
            tk.Label(self, text=str(num_ableitung)+". Ableitung: "+funktionsname+" = " + ableitungsfunktion.funktion_user_kurz).grid(row=row + 3, column=0,sticky=tk.W)
            row = row+3
        elif davor_abgeleitete_funktion.is_trigonometrisch:
            if davor_abgeleitete_funktion.trigonometrisch_d != 0:
                tk.Label(self, text=" konstante Zahl fällt weg, da kein x enthalten").grid(row=row, column=2,sticky = tk.W)
                tk.Label(self, text=funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a) + " * " + davor_abgeleitete_funktion.trigonometrische_funktion + "(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")").grid(row=row+1, column=1)
                row = row + 1
            if davor_abgeleitete_funktion.trigonometrische_funktion == "cos":
                tk.Label(self, text="Nach Kettenregel "+davor_abgeleitete_funktion.trigonometrische_funktion+"(u(x)) -> -sin(u(x)) * u'(x), Vorfaktor bleibt erhalten").grid(row=row+1, column=1)
                tk.Label(self, text=funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a)+" * -sin(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ") * " + str(davor_abgeleitete_funktion.trigonometrisch_b)).grid(row=row+2, column=1)
                ableitungsfunktion = Funktion(str(-1*davor_abgeleitete_funktion.trigonometrisch_a*davor_abgeleitete_funktion.trigonometrisch_b)+" * sin(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")")
            elif davor_abgeleitete_funktion.trigonometrische_funktion == "sin":
                tk.Label(self,text="Nach Kettenregel " + davor_abgeleitete_funktion.trigonometrische_funktion + "(u(x)) -> cos(u(x)) * u'(x), Vorfaktor bleibt erhalten").grid(row=row + 1, column=1)
                tk.Label(self, text=funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a) + " * cos(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ") * " + str(davor_abgeleitete_funktion.trigonometrisch_b)).grid(row=row + 2, column=1)
                ableitungsfunktion = Funktion(str(davor_abgeleitete_funktion.trigonometrisch_a * davor_abgeleitete_funktion.trigonometrisch_b) + " * cos(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")")
            elif davor_abgeleitete_funktion.trigonometrische_funktion == "tan":
                tk.Label(self, text=" tan() -> 1/cos()² mit Kettenregel tan(v(x)) -> v'(x)/(cos(x)²").grid(row=row, column=2, sticky=tk.W)
                tk.Label(self, text="F(x) = " + str(self.__funktion.trigonometrisch_a) + " * " + str(self.__funktion.trigonometrisch_b) + " / cos(" + n_mal_x_plus_m_to_string(self.__funktion.trigonometrisch_b,-self.__funktion.trigonometrisch_c) + ")'2").grid(row=row + 1, column=1)
                ableitungsfunktion = Funktion(str(davor_abgeleitete_funktion.trigonometrisch_a * davor_abgeleitete_funktion.trigonometrisch_b) + " / cos(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")'2")
            tk.Label(self, text=funktionsname+" = " + ableitungsfunktion.funktion_user_kurz).grid(row=row + 3, column=1)
            row = row+3
        else:
            could_be_solved = True
            try:
                loesung = sympy.diff(davor_abgeleitete_funktion.funktion_sympy_readable, sympy.Symbol('x'), 1)
                ableitungsfunktion = Funktion()
                funktion_erkannt = ableitungsfunktion.set_funktion(sympy.printing.sstr(loesung).replace("**", "'"))
                if funktion_erkannt:
                    tk.Label(self, text=funktionsname+"= " + ableitungsfunktion.funktion_user_kurz).grid(row=row+1, column=1)
                    tk.Label(self, text=str(num_ableitung) + ". Ableitung: " + funktionsname + " = " + ableitungsfunktion.funktion_user_kurz).grid(row=row + 2, column=0, sticky=tk.W)
                    row = row+2
                else:
                    could_be_solved = False
                    tk.Label(self, text="Vielleicht hilft das: " + sympy.sstr(loesung).replace("**", "'")).grid(row=row+2, column=0, columnspan=2, sticky=tk.W)
            except Exception:
                could_be_solved = False
            if not could_be_solved:
                ableitungsfunktion = None
                tk.Label(self, text="Ableitung konnte nicht erstellt werden").grid(row=row+1, column=0, columnspan=2, sticky=tk.W)
                row = row + 2
        if ableitungsfunktion != None:
            return ableitungsfunktion,row
        else:
            return None,row