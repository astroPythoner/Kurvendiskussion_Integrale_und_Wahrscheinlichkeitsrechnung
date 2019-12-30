from Funktion import Funktion, vorzeichen_str
from Grundklassen import Graph

import math
import tkinter as tk

class TangenteNormale_Frame(tk.Frame):

    __funktion = None
    funktionen = []

    def __init__(self, ableitung, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.update()
        self.ableitung = ableitung
        self.x_wert = tk.IntVar()
        self.last_wert = 0

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def scrollbar_bewegt(self,wert=None):
        if wert != self.last_wert:
            self.last_wert = wert
            self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            self.funktionen = []
            self.x_regler = tk.Scale(self, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.x_wert)
            self.x_regler.config(command=self.scrollbar_bewegt)
            self.x_regler.grid(row = 0,column = 0, sticky=tk.NSEW)
            self.spinbox = tk.Spinbox(self, from_=-100, to=100, textvariable=self.x_wert)
            self.spinbox.config(command=self.scrollbar_bewegt)
            self.spinbox.grid(row=0, column=1,sticky=tk.W)
            tk.Label(self, text=str(self.x_wert.get())+" in Gleichungen einsetzten").grid(row=1, column=0,sticky=tk.W)
            tk.Label(self, text="f("+str(self.x_wert.get())+") = "+self.__funktion.funktion_x_eingesetzt(self.x_wert.get())).grid(row=2, column=1)
            try:
                erg_normale_funktion = self.__funktion.x_einsetzen(self.x_wert.get())
                if isinstance(erg_normale_funktion, complex):
                    erg_normale_funktion = "nicht definiert"
            except:
                erg_normale_funktion = "nicht definiert"
            tk.Label(self, text="f("+str(self.x_wert.get())+") = "+str(erg_normale_funktion)).grid(row=3, column=1)
            if len(self.ableitung.funktionen) > 0 and self.ableitung.funktionen[0].funktion != None:
                ableitung = self.ableitung.funktionen[0].funktion
                tk.Label(self, text="f'(" + str(self.x_wert.get()) + ") = " + ableitung.funktion_x_eingesetzt(self.x_wert.get())).grid(row=4, column=1)
                try:
                    erg_ableitung = ableitung.x_einsetzen(self.x_wert.get())
                    if isinstance(erg_ableitung, complex):
                        erg_normale_funktion = "nicht definiert"
                except:
                    erg_ableitung = "nicht definiert"
                tk.Label(self, text="f'(" + str(self.x_wert.get()) + ") = " + str(erg_ableitung)).grid(row=5, column=1)
            else:
                tk.Label(self, text="f'(x) nicht bekannt").grid(row=4,column=1)
                erg_ableitung = "nicht definiert"
            tk.Label(self, text="Tangente nach Formel t(x) = f'(x0)*(x-x0)+f(x0):").grid(row=6, column=0,sticky=tk.W)
            tk.Label(self, text="Normale nach Formel n(x) = (-1/f'(x0))*(x-x0)+f(x0):").grid(row=8, column=0, sticky=tk.W)
            if erg_ableitung != "nicht definiert" and erg_normale_funktion != "nicht definiert":
                # normalengleichung gzusammenbasteln
                funktionsterm = ""
                if erg_ableitung != 0:
                    funktionsterm += str(erg_ableitung)
                    if self.x_wert.get()!= 0:
                        funktionsterm += " * (x"+vorzeichen_str(self.x_wert.get())+") "
                    else:
                        funktionsterm += " * x "
                if erg_normale_funktion != 0:
                    funktionsterm += vorzeichen_str(erg_normale_funktion)
                if funktionsterm == "":
                    funktionsterm = "0"
                t = Funktion(funktionsterm)
                graph_t = Graph(t,"#FFBB00","dunkelgelb","t(x)")
                self.funktionen.append(graph_t)
                tk.Label(self, text="t(x) = "+t.funktion_user_kurz).grid(row=7, column=1)
                # tangentengleichung zusammenbasteln
                if erg_ableitung != 0:
                    funktionsterm = ""
                    if erg_ableitung < 0:
                        funktionsterm += "(1/"+str(erg_ableitung*-1)+")"
                    elif erg_ableitung == 1:
                        funktionsterm += "-1"
                    else:
                        funktionsterm += "(-1/"+str(erg_ableitung)+")"
                    if self.x_wert.get() != 0:
                        funktionsterm += " * (x" + vorzeichen_str(self.x_wert.get()) + ") "
                    else:
                        funktionsterm += " * x "
                    if erg_normale_funktion != 0:
                        funktionsterm += vorzeichen_str(erg_normale_funktion)
                    if funktionsterm == "":
                        funktionsterm = "0"
                    n = Funktion(funktionsterm)
                    graph_n = Graph(n,"#FFCC33","hellgelb","n(x)")
                    self.funktionen.append(graph_n)
                    tk.Label(self, text="n(x) = " + n.funktion_user_kurz).grid(row=9, column=1)
                else:
                    tk.Label(self, text="Fehler durch Null teilen -> keine Normalengleichung").grid(row=9, column=1)
            else:
                tk.Label(self, text="Tangentengleichung kann nicht bestimmt werden").grid(row=7, column=1)
                tk.Label(self, text="Normalengleichung kann nicht bestimmt werden").grid(row=9, column=1)
        else:
            tk.Label(self, text="Für Tangente und Normale Funktion oben eingeben").grid(row=0, column=0)