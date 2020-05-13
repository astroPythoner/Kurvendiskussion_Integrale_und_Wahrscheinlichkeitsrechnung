import tkinter as tk
import math

class GlobalesVerhalten_Frame(tk.Frame):

    __funktion = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.update()

    def update(self, neu_funktion = None, second_funktion=None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            tk.Label(self, text="Globales Verhalten: " + self.__funktion.funktion_polynom_x_ersetzbar,fg="blue4").grid(row=0, column=0,sticky=tk.W)
            if not "x" in self.__funktion.funktion_user_x_ersetztbar:
                wert = self.__funktion.x_einsetzen(0)
                tk.Label(self, text="lim x->∞ = " + str(wert),fg="green4").grid(row=1, column=1)
                tk.Label(self, text="lim x->-∞ = " + str(wert),fg="green4").grid(row=2, column=1)
            elif self.__funktion.is_polynomfunktion:
                geht_gegen_array_plus_unendlich = []
                geht_gegen_array_minus_unendlich = []
                for i in self.__funktion.exponenten_array:
                    exponent = eval(self.__funktion.funktion_to_computer_readable(i[1]))
                    basis = eval(self.__funktion.funktion_to_computer_readable(i[0]))
                    if exponent > 0:
                        if basis > 0:
                            geht_gegen_array_plus_unendlich.append("+∞")
                            if exponent % 2 == 0:
                                geht_gegen_array_minus_unendlich.append("+∞")
                            else:
                                geht_gegen_array_minus_unendlich.append("-∞")
                        elif basis < 0:
                            geht_gegen_array_plus_unendlich.append("-∞")
                            if exponent % 2 == 0:
                                geht_gegen_array_minus_unendlich.append("-∞")
                            else:
                                geht_gegen_array_minus_unendlich.append("+∞")
                        else:
                            geht_gegen_array_plus_unendlich.append("+0")
                            geht_gegen_array_minus_unendlich.append("+0")
                    elif exponent < 0:
                        if basis > 0:
                            geht_gegen_array_plus_unendlich.append("+0")
                            if exponent%2 == 0:
                                geht_gegen_array_minus_unendlich.append("+0")
                            else:
                                geht_gegen_array_minus_unendlich.append("-0")
                        elif basis < 0:
                            geht_gegen_array_plus_unendlich.append("-0")
                            if exponent%2 == 0:
                                geht_gegen_array_minus_unendlich.append("-0")
                            else:
                                geht_gegen_array_minus_unendlich.append("+0")
                        else:
                            geht_gegen_array_plus_unendlich.append("+0")
                            geht_gegen_array_minus_unendlich.append("+0")
                    else:
                        if str(basis)[0] == "-":
                            geht_gegen_array_plus_unendlich.append(str(basis))
                            geht_gegen_array_minus_unendlich.append(str(basis))
                        else:
                            geht_gegen_array_plus_unendlich.append("+"+str(basis))
                            geht_gegen_array_minus_unendlich.append("+"+str(basis))
                geht_gegen_funktion_plus_unendlich = ""
                geht_gegen_funktion_minus_unendlich = ""
                for i in range(len(geht_gegen_array_plus_unendlich)):
                    geht_gegen_funktion_plus_unendlich += geht_gegen_array_plus_unendlich[i]
                    geht_gegen_funktion_minus_unendlich += geht_gegen_array_minus_unendlich[i]
                tk.Label(self, text="lim x->∞ = " + geht_gegen_funktion_plus_unendlich).grid(row=1, column=0)
                tk.Label(self, text="lim x->-∞ = " + geht_gegen_funktion_minus_unendlich).grid(row=3, column=0)
                if len(geht_gegen_funktion_plus_unendlich) > 2:
                    if "∞" in geht_gegen_funktion_plus_unendlich:
                        tk.Label(self, text="lim x->∞ = " + geht_gegen_funktion_plus_unendlich[:2],fg="green4").grid(row=2, column=0)
                    else:
                        tk.Label(self, text="lim x->∞ = " + str(eval(geht_gegen_funktion_plus_unendlich)),fg="green4").grid(row=2,column=0)
                if len(geht_gegen_funktion_minus_unendlich) > 2:
                    if "∞" in geht_gegen_funktion_minus_unendlich:
                        tk.Label(self, text="lim x->-∞ = " + geht_gegen_funktion_minus_unendlich[:2],fg="green4").grid(row=4,column=0)
                    else:
                        tk.Label(self, text="lim x->-∞ = " + str(eval(geht_gegen_funktion_minus_unendlich)),fg="green4").grid(row=4,column=0)
            elif self.__funktion.is_trigonometrisch:
                tk.Label(self, text="Trigonometrische Funktion konvegiert nicht",fg="blue4").grid(row=1, column=1,sticky = tk.W)
                tk.Label(self, text="Wertemenge:",fg="blue2").grid(row=2, column=1,sticky = tk.W)
                if self.__funktion.trigonometrische_funktion == "tan":
                    tk.Label(self, text="W = {-∞;∞}",fg="green4").grid(row=3, column=1)
                else:
                    tk.Label(self, text="W = {−a + d;a + d}").grid(row=3, column=1)
                    wert1 = self.__funktion.trigonometrisch_a + self.__funktion.trigonometrisch_d
                    wert2 = -self.__funktion.trigonometrisch_a + self.__funktion.trigonometrisch_d
                    min_wert = min([wert1,wert2])
                    max_wert = max([wert1,wert2])
                    tk.Label(self, text="W = {"+str(min_wert)+";"+str(max_wert)+"}",fg="green4").grid(row=4, column=1)
            elif self.__funktion.is_wurzel:
                if self.__funktion.wurzel_b == 0 or self.__funktion.wurzel_a == 0:
                    tk.Label(self, text="lim x->∞ = 0",fg="green4").grid(row=1, column=0)
                    tk.Label(self, text="lim x->-∞ = 0",fg="green4").grid(row=2, column=0)
                elif self.__funktion.wurzel_b < 0:
                    tk.Label(self, text="lim x->∞ = in Wurzelfunktionen lassen sich keine negativen Werte einsetzen (durch negativen Vorfakter in der Wurzel wird aus positiv negativ)",fg="green4").grid(row=1, column=0)
                    if self.__funktion.wurzel_a < 0:
                        tk.Label(self, text="lim x->-∞ = -∞",fg="green4").grid(row=2, column=0)
                    elif self.__funktion.wurzel_a > 0:
                        tk.Label(self, text="lim x->-∞ = ∞",fg="green4").grid(row=2, column=0)
                elif self.__funktion.wurzel_b > 0:
                    tk.Label(self, text="lim x->-∞ = in Wurzelfunktionen lassen sich keine negativen Werte einsetzen",fg="green4").grid(row=2, column=0)
                    if self.__funktion.wurzel_a < 0:
                        tk.Label(self, text="lim x->-∞ = -∞",fg="green4").grid(row=1, column=0)
                    elif self.__funktion.wurzel_a > 0:
                        tk.Label(self, text="lim x->-∞ = ∞",fg="green4").grid(row=1, column=0)
            else:
                tk.Label(self, text="Globales Verhalten konnte nicht ermittelt werden",fg="red").grid(row=1, column=0,sticky=tk.W)
        else:
            tk.Label(self, text="Für Berechnung des globalen Verhaltens Funktion oben eingeben").grid(row=0, column=0)