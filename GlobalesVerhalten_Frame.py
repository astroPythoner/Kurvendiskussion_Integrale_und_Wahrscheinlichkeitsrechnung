import tkinter as tk

class GlobalesVerhalten_Frame(tk.Frame):

    __funktion = None

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
            tk.Label(self, text="Globales Verhalten: " + self.__funktion.funktion_exponential_x_ersetzbar).grid(row=0, column=0,sticky=tk.W)
            if not "x" in self.__funktion.funktion_user_x_ersetztbar:
                wert = eval(self.__funktion.funktion_computer_readable)
                tk.Label(self, text="lim x->∞ = " + str(wert)).grid(row=1, column=1)
                tk.Label(self, text="lim x->-∞ = " + str(wert)).grid(row=2, column=1)
            elif self.__funktion.is_polinomfunktion:
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
                        if basis >= 0:
                            geht_gegen_array_plus_unendlich.append("+"+str(basis))
                            geht_gegen_array_minus_unendlich.append("+"+str(basis))
                        else:
                            geht_gegen_array_plus_unendlich.append(str(basis))
                            geht_gegen_array_minus_unendlich.append(str(basis))
                geht_gegen_funktion_plus_unendlich = ""
                geht_gegen_funktion_minus_unendlich = ""
                for i in range(len(geht_gegen_array_plus_unendlich)):
                    geht_gegen_funktion_plus_unendlich += geht_gegen_array_plus_unendlich[i]
                    geht_gegen_funktion_minus_unendlich += geht_gegen_array_minus_unendlich[i]
                tk.Label(self, text="lim x->∞ = " + geht_gegen_funktion_plus_unendlich).grid(row=1, column=0)
                tk.Label(self, text="lim x->-∞ = " + geht_gegen_funktion_minus_unendlich).grid(row=3, column=0)
                if len(geht_gegen_funktion_plus_unendlich) > 2:
                    if "∞" in geht_gegen_funktion_plus_unendlich:
                        tk.Label(self, text="lim x->∞ = " + geht_gegen_funktion_plus_unendlich[:2]).grid(row=2, column=0)
                    else:
                        tk.Label(self, text="lim x->∞ = " + str(eval(geht_gegen_funktion_plus_unendlich))).grid(row=2,column=0)
                if len(geht_gegen_funktion_minus_unendlich) > 2:
                    if "∞" in geht_gegen_funktion_minus_unendlich:
                        tk.Label(self, text="lim x->-∞ = " + geht_gegen_funktion_minus_unendlich[:2]).grid(row=4,column=0)
                    else:
                        tk.Label(self, text="lim x->-∞ = " + str(eval(geht_gegen_funktion_minus_unendlich))).grid(row=4,column=0)
            else:
                tk.Label(self, text="Globales Verhalten für nicht Polinomfunktionen comming soon..." + self.__funktion.funktion_user_kurz).grid(row=1, column=0,sticky=tk.W)
        else:
            tk.Label(self, text="Für Berechnung des globalen Verhaltens Funktion oben eingeben").grid(row=0, column=0)