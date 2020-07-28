from Grundklassen import Punkt, Wiederholender_Punkt
from Nullstellen_Frame import nullstellen_berechnen

import tkinter as tk
import math

class Kruemmung_Frame(tk.Frame):

    __funktion = None

    parameter = None

    def __init__(self, master=None,parameter=None, ableitung=None, pdf_writer=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.ableitung = ableitung
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

        pdf = lambda txt: self.pdf_writer.kruemmung_texte.append(txt) if self.pdf_writer is not None else False
        self.punkte = []
        if self.__funktion != None:
            tk.Label(self, text="Krümmung: aus zweiter Ableitung",fg="blue4").grid(row=0, column=0, sticky=tk.W)
            pdf(["calc", "Eventuelle Wendepunkte durch f''(x) = 0:"])
            if len(self.ableitung.funktionen) < 2 or self.ableitung.funktionen[1].funktion == None:
                tk.Label(self, text="Zweite Ableitung f''(x) nicht bekannt",fg="red").grid(row=1, column=0, sticky=tk.W)
                pdf(["noerg", "Zweite Ableitung f''(x) nicht bekannt"])
            else:
                zweite_ableitung = self.ableitung.funktionen[1].funktion
                num_wendepunkt = 0
                tk.Label(self, text="f''(x) = " + zweite_ableitung.funktion_user_kurz).grid(row=1, column=1)
                pdf(["fkt", "f''(x) = " + zweite_ableitung.funktion_user_kurz])
                tk.Label(self, text="Eventuelle Wendepunkte durch f''(x) = 0:",fg="blue2").grid(row=2, column=0, sticky=tk.W)
                nullstellen, row = nullstellen_berechnen(self.parameter,zweite_ableitung, 3, self, pdf_writer=self.pdf_writer.kruemmung_texte)
                tk.Label(self, text="Überprüfen ob Nst Extrempunkte sind durch f'''(nst) ≠ 0:",fg="blue2").grid(row=row + 1, column=0, sticky=tk.W)
                pdf(["calc", "Überprüfen ob Nst Extrempunkte sind durch f'''(nst) ≠ 0:"])
                for nst in nullstellen:
                    if len(self.ableitung.funktionen) > 2 and self.ableitung.funktionen[2].funktion != None:
                        dritte_ableitung = self.ableitung.funktionen[2].funktion
                        tk.Label(self, text="f'''(" + str(nst.x) + ") = " + dritte_ableitung.funktion_user_kurz).grid(row=row + 2, column=1)
                        pdf(["fkt","f'''(" + str(nst.x) + ") = " + dritte_ableitung.funktion_user_kurz])
                        if "x" in dritte_ableitung.funktion_user_x_ersetztbar:
                            tk.Label(self, text="f'''(" + str(nst.x) + ") = " + dritte_ableitung.funktion_x_eingesetzt(nst.x)).grid(row=row + 3, column=1)
                            pdf(["fkt", "f'''(" + str(nst.x) + ") = " + dritte_ableitung.funktion_x_eingesetzt(nst.x)])
                        self.erg = dritte_ableitung.x_einsetzen(nst.x)
                        if self.erg != "nicht definiert":
                            tk.Label(self, text="f'''(" + str(nst.x) + ") = " + str(self.erg)).grid(row=row + 4, column=1)
                            pdf(["fkt", "f'''(" + str(nst.x) + ") = " + str(self.erg)])
                            if self.erg == 0:
                                tk.Label(self, text="Kein Wendepunkt, da f''' = 0 ist.").grid(row=row + 5, column=0, sticky=tk.W)
                                pdf(["fkt", "Kein Wendepunkt, da f''' = 0 ist."])
                            else:
                                num_wendepunkt += 1
                                tk.Label(self, text="Wendepunkt, da f''' ≠ 0").grid(row=row + 5, column=0, sticky=tk.W)
                                pdf(["fkt", "Wendepunkt, da f''' ≠ 0"])
                                if isinstance(nst,Wiederholender_Punkt):
                                    wp = Wiederholender_Punkt(nst.funktion, self.__funktion.x_einsetzen(nst.x), "WP" + str(num_wendepunkt))
                                else:
                                    wp = Punkt(nst.x, self.__funktion.x_einsetzen(nst.x), "WP" + str(num_wendepunkt))
                                tk.Label(self, text="WP" + str(num_wendepunkt) + " = (" + str(round(nst.x, 5)) + "|f(" + str(round(nst.x, 5)) + ")) = " + str(wp),fg="green4").grid(row=row + 6, column=0,sticky=tk.W)
                                pdf(["erg", "WP" + str(num_wendepunkt) + " = (" + str(round(nst.x, 5)) + "|f(" + str(round(nst.x, 5)) + ")) = " + str(wp)])
                                self.punkte.append(wp)
                        else:
                            tk.Label(self, text="f(0) = "+self.erg).grid(row=row + 4, column=1)
                            pdf(["fkt", "f(0) = "+self.erg])
                            tk.Label(self, text="Kein Extrempunkt",fg="green4").grid(row=row + 5, column=0, sticky=tk.W)
                            pdf(["erg", "Kein Extrempunkt"])
                        row = row + 6
                    else:
                        tk.Label(self, text="Dritte Ableitung f'''(x) nicht bekannt",fg="red").grid(row=1, column=0, sticky=tk.W)
                        pdf(["noerg", "Dritte Ableitung f'''(x) nicht bekannt"])
        else:
            tk.Label(self, text="Für Krümmung Funktion oben eingeben").grid(row=0, column=0)