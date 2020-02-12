from Grundklassen import Punkt, Wiederholender_Punkt
from Funktion import Funktion
from Nullstellen_Frame import nullstellen_berechnen

import tkinter as tk
import math

class Steigung_Frame(tk.Frame):

    __funktion = None
    punkte=[]

    parameter = None

    def __init__(self, master=None,parameter=None, ableitung=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.ableitung = ableitung
        self.parameter = parameter
        self.update()

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.punkte = []
        if self.__funktion != None:
            tk.Label(self, text="Steigung: aus erster Ableitung").grid(row=0,column=0,sticky=tk.W)
            if len(self.ableitung.funktionen) < 1 or self.ableitung.funktionen[0].funktion == None:
                tk.Label(self, text="Ableitung f'(x) nicht bekannt").grid(row=1, column=0)
            else:
                ableitung = self.ableitung.funktionen[0].funktion
                num_hochpunkt = 0
                num_tiefpunkte = 0
                tk.Label(self, text="f'(x) = " + ableitung.funktion_user_kurz).grid(row=1, column=1)
                tk.Label(self, text="Eventuelle Extrempunkte durch f'(x) = 0:").grid(row=2, column=0, sticky=tk.W)
                nullstellen,row = nullstellen_berechnen(self.parameter,ableitung,3,self)
                if len(nullstellen) >= 1:
                    tk.Label(self, text="Überprüfen ob Nst Extrempunkte sind durch f''(nst) ≠ 0:").grid(row=row+1, column=0, sticky=tk.W)
                for nst in nullstellen:
                    if len(self.ableitung.funktionen) > 1 and self.ableitung.funktionen[1].funktion != None:
                        zweite_ableitung = self.ableitung.funktionen[1].funktion
                        tk.Label(self, text="f''("+str(nst.x)+") = " + zweite_ableitung.funktion_user_kurz).grid(row=row+2, column=1)
                        if "x" in zweite_ableitung.funktion_user_x_ersetztbar:
                            tk.Label(self, text="f''("+str(nst.x)+") = " + zweite_ableitung.funktion_x_eingesetzt(nst.x)).grid(row=row+3, column=1)
                        self.erg = zweite_ableitung.x_einsetzen(nst.x)
                        if self.erg != "nicht definiert":
                            tk.Label(self, text="f''("+str(nst.x)+") = " + str(self.erg)).grid(row=row+4, column=1)
                            if self.erg < 0:
                                num_hochpunkt += 1
                                tk.Label(self, text="Hochpunkt, da f'' < 0").grid(row=row+5, column=0, sticky=tk.W)
                                if isinstance(nst,Wiederholender_Punkt):
                                    hp = Wiederholender_Punkt(nst.funktion,self.__funktion.x_einsetzen(nst.x),"HP"+str(num_hochpunkt))
                                else:
                                    hp = Punkt(nst.x,self.__funktion.x_einsetzen(nst.x),"HP"+str(num_hochpunkt))
                                tk.Label(self, text="HP"+str(num_hochpunkt)+" = ("+str(round(nst.x,3))+"|f("+str(round(nst.x,3))+")) = "+str(hp)).grid(row=row + 6, column=0, sticky=tk.W)
                                self.punkte.append(hp)
                            elif self.erg == 0:
                                tk.Label(self, text="Kein Extrempunkt, da f'' 0 ist.").grid(row=row+5, column=0, sticky=tk.W)
                            else:
                                num_tiefpunkte += 1
                                tk.Label(self, text="Tiefpunkt, da f'' > 0").grid(row=row+5, column=0, sticky=tk.W)
                                if isinstance(nst,Wiederholender_Punkt):
                                    tp = Wiederholender_Punkt(nst.funktion,self.__funktion.x_einsetzen(nst.x),"TP"+str(num_tiefpunkte))
                                else:
                                    tp = Punkt(nst.x,self.__funktion.x_einsetzen(nst.x),"TP"+str(num_tiefpunkte))
                                tk.Label(self, text="TP"+str(num_tiefpunkte)+" = ("+str(round(nst.x,3))+"|f("+str(round(nst.x,3))+")) = "+str(tp)).grid(row=row + 6, column=0, sticky=tk.W)
                                self.punkte.append(tp)
                        else:
                            tk.Label(self, text="f(0) = "+self.erg).grid(row=row+4, column=1)
                            tk.Label(self, text="Kein Extrempunkt").grid(row=row+5, column=0, sticky=tk.W)
                        row = row + 6
                    else:
                        tk.Label(self, text="Zweite Ableitung f''(x) nicht bekannt").grid(row=1, column=0, sticky=tk.W)
        else:
            tk.Label(self, text="Für Steigung Funktion oben eingeben").grid(row=0, column=0)