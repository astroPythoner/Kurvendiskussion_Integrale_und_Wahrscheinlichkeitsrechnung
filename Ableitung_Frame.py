from Grundklassen import Graph
from Funktion import Funktion, n_mal_x_plus_m_to_string, polynom_array_to_str, vorzeichen_str, bruch_kuerzen

import tkinter as tk
from tkinter import font
from tkinter import ttk
import math
try:
    import sympy
except Exception:
    pass

class Ableitung_Frame(tk.Frame):

    __funktion = None
    funktionen = []

    parameter = None

    def __init__(self, master=None,parameter=None, pdf_writer=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.parameter = parameter
        self.pdf_writer = pdf_writer
        self.update()

    def update(self, neu_funktion = None, second_funktion=None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            self.funktionen = []
            erste_ableitung,row_1 = self.ableiten(self.__funktion, 1, 0,pdf_writer=self.pdf_writer.ableitung_texte)
            if isinstance(erste_ableitung, Funktion):
                self.funktionen.append(Graph(erste_ableitung, "#990000","dunkelrot", "f'(x)"))
                zweite_ableitung, row_2 = self.ableiten(erste_ableitung, 2, row_1,pdf_writer=self.pdf_writer.ableitung_texte)
                if isinstance(zweite_ableitung, Funktion):
                    self.funktionen.append(Graph(zweite_ableitung, "#CC0000", "rot", "f''(x)"))
                    dritte_ableitung, row_3 = self.ableiten(zweite_ableitung, 3, row_2,pdf_writer=self.pdf_writer.ableitung_texte)
                    if dritte_ableitung != None:
                        self.funktionen.append(Graph(dritte_ableitung, "#FF0000","hellrot", "f'''(x)"))
        else:
            self.funktion_text = tk.Label(self, text="Für Ableitungen Funktion oben eingeben")
            self.funktion_text.grid(row=0, column=0)

    def ableiten(self,davor_abgeleitete_funktion,num_ableitung,row,pdf_writer):
        pdf = lambda txt: pdf_writer.append(txt) if pdf_writer is not None else False
        ableitungsfunktion = None
        funktionsname = "f"
        for i in range(num_ableitung):
            funktionsname += "'"
        funktionsname_davor = funktionsname[:-1]+"(x)"
        funktionsname += "(x)"
        tk.Label(self, text=str(num_ableitung)+". Ableitung:",fg="blue4").grid(row=row+1, column=0, columnspan=2, sticky=tk.W)
        pdf(["title",str(num_ableitung)+". Ableitung:"])
        tk.Label(self, text=funktionsname_davor+" = " + davor_abgeleitete_funktion.funktion_user_x_ersetztbar).grid(row=row+2, column=1)
        row = row+2
        if not "x" in davor_abgeleitete_funktion.funktion_user_x_ersetztbar:
            ableitungsfunktion = Funktion(self.parameter,"0")
            tk.Label(self, text="Kein x enthalten:",fg="blue2").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
            pdf(["calc", "Kein x enthalten:"])
            tk.Label(self, text=funktionsname+" = 0").grid(row=row + 2, column=1)
            pdf(["fkt", funktionsname+" = 0"])
            tk.Label(self, text=str(num_ableitung) + ". Ableitung: " + funktionsname + " = 0",fg="green4").grid(row=row + 3, column=0, sticky=tk.W)
            pdf(["erg", str(num_ableitung) + ". Ableitung: " + funktionsname + " = 0"])
            row = row+3
        elif davor_abgeleitete_funktion.is_polynomfunktion:
            exponenten = davor_abgeleitete_funktion.exponenten_array
            tk.Label(self, text="In Exponentialform bringen:",fg="blue2").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
            pdf(["calc", "In Exponentialform bringen:"])
            tk.Label(self, text=funktionsname_davor+" = " + davor_abgeleitete_funktion.funktion_polynom_x_ersetzbar).grid(row=row + 2,column=1)
            pdf(["fkt", funktionsname_davor+" = " + davor_abgeleitete_funktion.funktion_polynom_x_ersetzbar])
            tk.Label(self, text="Ableiten nach Regel ax'b -> (a*b)*x'(b-1):",fg="blue2").grid(row=row + 3, column=0, columnspan=2,sticky=tk.W)
            pdf(["calc", "Ableiten nach Regel ax'b -> (a*b)*x'(b-1):"])
            row = row + 3
            neue_exponenten = []
            neue_exponenten_kurz = []
            for exponent in exponenten:
                neue_exponenten.append(["(" + exponent[0] + "*" + exponent[1] + ")", "(" + exponent[1] + "-1)"])
                p = self.parameter.wert
                basis_wert = eval(davor_abgeleitete_funktion.funktion_to_computer_readable(self.__funktion.funktion_verschoenern("((" + exponent[0] + ")*" + exponent[1] + ")")))
                expo_wert = eval(self.__funktion.funktion_to_computer_readable(self.__funktion.funktion_verschoenern("((" + exponent[1] + ")-1)")))
                neue_exponenten_kurz.append([basis_wert, expo_wert])
            poly_funktion = ""
            poly_funktion_kurz = ""
            for poly_num in range(0,len(neue_exponenten)):
                poly_funktion += vorzeichen_str(neue_exponenten[poly_num][0] + "*x'" + neue_exponenten[poly_num][1],True)
                poly_funktion_kurz += polynom_array_to_str(neue_exponenten_kurz[poly_num])
            ableitungsfunktion = Funktion(self.parameter,poly_funktion_kurz)
            tk.Label(self, text=funktionsname+" = " + poly_funktion).grid(row=row + 1, column=1)
            pdf(["fkt", funktionsname+" = " + poly_funktion])
            tk.Label(self, text=funktionsname+" = " + ableitungsfunktion.funktion_user_kurz).grid(row=row + 2, column=1)
            pdf(["fkt", funktionsname+" = " + ableitungsfunktion.funktion_user_kurz])
            tk.Label(self, text=str(num_ableitung)+". Ableitung: "+funktionsname+" = " + ableitungsfunktion.funktion_user_kurz,fg="green4").grid(row=row + 3, column=0,sticky=tk.W)
            pdf(["erg", str(num_ableitung)+". Ableitung: "+funktionsname+" = " + ableitungsfunktion.funktion_user_kurz])
            row = row+3
        elif davor_abgeleitete_funktion.is_trigonometrisch:
            if davor_abgeleitete_funktion.trigonometrisch_d != 0:
                tk.Label(self, text=" konstante Zahl fällt weg, da kein x enthalten",fg="blue2").grid(row=row, column=2,sticky = tk.W)
                pdf(["calc", "konstante Zahl fällt weg, da kein x enthalten"])
                tk.Label(self, text=funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a) + " * " + davor_abgeleitete_funktion.trigonometrische_funktion + "(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")").grid(row=row+1, column=1)
                pdf(["fkt", funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a) + " * " + davor_abgeleitete_funktion.trigonometrische_funktion + "(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")"])
                row = row + 1
            if davor_abgeleitete_funktion.trigonometrische_funktion == "cos":
                tk.Label(self, text="Nach Kettenregel "+davor_abgeleitete_funktion.trigonometrische_funktion+"(u(x)) -> -sin(u(x)) * u'(x), Vorfaktor bleibt erhalten",fg="blue2").grid(row=row+1, column=1)
                pdf(["calc", "Nach Kettenregel "+davor_abgeleitete_funktion.trigonometrische_funktion+"(u(x)) -> -sin(u(x)) * u'(x), Vorfaktor bleibt erhalten"])
                tk.Label(self, text=funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a)+" * -sin(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ") * " + str(davor_abgeleitete_funktion.trigonometrisch_b)).grid(row=row+2, column=1)
                pdf(["fkt", funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a)+" * -sin(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ") * " + str(davor_abgeleitete_funktion.trigonometrisch_b)])
                ableitungsfunktion = Funktion(self.parameter,str(-1*davor_abgeleitete_funktion.trigonometrisch_a*davor_abgeleitete_funktion.trigonometrisch_b)+" * sin(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")")
            elif davor_abgeleitete_funktion.trigonometrische_funktion == "sin":
                tk.Label(self,text="Nach Kettenregel " + davor_abgeleitete_funktion.trigonometrische_funktion + "(u(x)) -> cos(u(x)) * u'(x), Vorfaktor bleibt erhalten",fg="blue2").grid(row=row + 1, column=1)
                pdf(["calc", "Nach Kettenregel " + davor_abgeleitete_funktion.trigonometrische_funktion + "(u(x)) -> cos(u(x)) * u'(x), Vorfaktor bleibt erhalten"])
                tk.Label(self, text=funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a) + " * cos(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ") * " + str(davor_abgeleitete_funktion.trigonometrisch_b)).grid(row=row + 2, column=1)
                pdf(["fkt", funktionsname+" = " + str(davor_abgeleitete_funktion.trigonometrisch_a) + " * cos(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ") * " + str(davor_abgeleitete_funktion.trigonometrisch_b)])
                ableitungsfunktion = Funktion(self.parameter,str(davor_abgeleitete_funktion.trigonometrisch_a * davor_abgeleitete_funktion.trigonometrisch_b) + " * cos(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")")
            elif davor_abgeleitete_funktion.trigonometrische_funktion == "tan":
                tk.Label(self, text=" tan() -> 1/cos()² mit Kettenregel tan(v(x)) -> v'(x)/(cos(x)²",fg="blue2").grid(row=row, column=2, sticky=tk.W)
                pdf(["calc", "tan() -> 1/cos()² mit Kettenregel tan(v(x)) -> v'(x)/(cos(x)²"])
                tk.Label(self, text="F(x) = " + str(self.__funktion.trigonometrisch_a) + " * " + str(self.__funktion.trigonometrisch_b) + " / cos(" + n_mal_x_plus_m_to_string(self.__funktion.trigonometrisch_b,-self.__funktion.trigonometrisch_c) + ")'2").grid(row=row + 1, column=1)
                pdf(["fkt", "F(x) = " + str(self.__funktion.trigonometrisch_a) + " * " + str(self.__funktion.trigonometrisch_b) + " / cos(" + n_mal_x_plus_m_to_string(self.__funktion.trigonometrisch_b,-self.__funktion.trigonometrisch_c) + ")'2"])
                ableitungsfunktion = Funktion(self.parameter,str(davor_abgeleitete_funktion.trigonometrisch_a * davor_abgeleitete_funktion.trigonometrisch_b) + " / cos(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.trigonometrisch_b, -davor_abgeleitete_funktion.trigonometrisch_c) + ")'2")
            tk.Label(self, text=funktionsname+" = " + ableitungsfunktion.funktion_user_kurz).grid(row=row + 3, column=1)
            pdf(["fkt", funktionsname+" = " + ableitungsfunktion.funktion_user_kurz])
            tk.Label(self, text=str(num_ableitung)+". Ableitung: "+funktionsname+" = " + ableitungsfunktion.funktion_user_kurz,fg="green4").grid(row=row + 4, column=0,sticky=tk.W)
            pdf(["erg", str(num_ableitung)+". Ableitung: "+funktionsname+" = " + ableitungsfunktion.funktion_user_kurz])
            row = row+4
        elif davor_abgeleitete_funktion.is_wurzel:
            if davor_abgeleitete_funktion.wurzel_d != 0:
                tk.Label(self, text=" konstante Zahl fällt weg, da kein x enthalten",fg="blue2").grid(row=row, column=2,sticky = tk.W)
                pdf(["calc", "konstante Zahl fällt weg, da kein x enthalten"])
                tk.Label(self, text=funktionsname+" = " + str(davor_abgeleitete_funktion.wurzel_a) + " * sqrt(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.wurzel_b, -davor_abgeleitete_funktion.wurzel_c) + ")").grid(row=row+1, column=1)
                pdf(["fkt", funktionsname+" = " + str(davor_abgeleitete_funktion.wurzel_a) + " * sqrt(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.wurzel_b, -davor_abgeleitete_funktion.wurzel_c) + ")"])
                row = row+1
            tk.Label(self, text=" Wurzel lösen nach √x -> 1/(2√x)",fg="blue2").grid(row=row, column=2, sticky=tk.W)
            pdf(["calc", "Wurzel lösen nach √x -> 1/(2√x)"])
            tk.Label(self, text=funktionsname + " = " + str(davor_abgeleitete_funktion.wurzel_a) + " * 1/(2*sqrt(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.wurzel_b,-davor_abgeleitete_funktion.wurzel_c) + "))").grid(row=row, column=1)
            pdf(["fkt", funktionsname + " = " + str(davor_abgeleitete_funktion.wurzel_a) + " * 1/(2*sqrt(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.wurzel_b,-davor_abgeleitete_funktion.wurzel_c) + "))"])
            tk.Label(self, text=" Nach Kettenregel auch innere Funktion ableiten und multiplizieren",fg="blue2").grid(row=row+1, column=2, sticky=tk.W)
            pdf(["calc", "Nach Kettenregel auch innere Funktion ableiten und multiplizieren"])
            tk.Label(self, text=funktionsname + " = " + str(davor_abgeleitete_funktion.wurzel_a) + " * 1/(2*sqrt(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.wurzel_b,-davor_abgeleitete_funktion.wurzel_c) + ")) * "+str(davor_abgeleitete_funktion.wurzel_b)).grid(row=row+1, column=1)
            pdf(["fkt", funktionsname + " = " + str(davor_abgeleitete_funktion.wurzel_a) + " * 1/(2*sqrt(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.wurzel_b,-davor_abgeleitete_funktion.wurzel_c) + ")) * "+str(davor_abgeleitete_funktion.wurzel_b)])
            bruch = bruch_kuerzen(davor_abgeleitete_funktion.wurzel_a*davor_abgeleitete_funktion.wurzel_b,2)
            ableitungsfunktion = Funktion(self.parameter,str(bruch[0]) + "/(" + str(bruch[1]) + "*sqrt(" + n_mal_x_plus_m_to_string(davor_abgeleitete_funktion.wurzel_b,-davor_abgeleitete_funktion.wurzel_c) + "))")
            tk.Label(self, text=funktionsname + " = " + ableitungsfunktion.funktion_user_kurz).grid(row=row+2, column=1)
            pdf(["fkt", funktionsname + " = " + ableitungsfunktion.funktion_user_kurz])
            tk.Label(self, text=str(num_ableitung)+". Ableitung: "+funktionsname+" = " + ableitungsfunktion.funktion_user_kurz,fg="green4").grid(row=row + 3, column=0,sticky=tk.W)
            pdf(["erg", str(num_ableitung)+". Ableitung: "+funktionsname+" = " + ableitungsfunktion.funktion_user_kurz])
            row = row+3
        else:
            could_be_solved = True
            try:
                loesung = sympy.diff(davor_abgeleitete_funktion.funktion_sympy_readable, sympy.Symbol('x'), 1)
                ableitungsfunktion = Funktion(self.parameter)
                funktion_erkannt = ableitungsfunktion.set_funktion(sympy.printing.sstr(loesung).replace("**", "'"))
                if funktion_erkannt:
                    tk.Label(self, text=funktionsname+"= " + ableitungsfunktion.funktion_user_kurz).grid(row=row+1, column=1)
                    pdf(["fkt", funktionsname+"= " + ableitungsfunktion.funktion_user_kurz])
                    tk.Label(self, text=str(num_ableitung) + ". Ableitung: " + funktionsname + " = " + ableitungsfunktion.funktion_user_kurz,fg="green4").grid(row=row + 2, column=0, sticky=tk.W)
                    pdf(["erg", str(num_ableitung) + ". Ableitung: " + funktionsname + " = " + ableitungsfunktion.funktion_user_kurz])
                    row = row+2
                else:
                    my_font = font.Font(family="Courier New")
                    style = ttk.Style()
                    style.configure("Fixed.TLabel", font=my_font)
                    could_be_solved = False
                    tk.Label(self, text="Vielleicht hilft das: " + sympy.sstr(loesung).replace("**", "'")).grid(row=2, column=0, columnspan=2, sticky=tk.W)
                    [ttk.Label(self, text=line, style="Fixed.TLabel").grid(row=count + 3, column=0, columnspan=2, sticky=tk.W) for count, line in enumerate(sympy.pretty(loesung).split("\n"))]
            except Exception:
                could_be_solved = False
            if not could_be_solved:
                ableitungsfunktion = None
                tk.Label(self, text="Ableitung konnte nicht erstellt werden",fg="red").grid(row=row+1, column=0, columnspan=2, sticky=tk.W)
                pdf(["noerg", "Ableitung konnte nicht erstellt werden"])
                row = row + 3
        if ableitungsfunktion != None:
            return ableitungsfunktion,row
        else:
            return None,row