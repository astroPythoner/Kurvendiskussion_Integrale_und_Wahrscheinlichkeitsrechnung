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
            tk.Label(self, text="Globales Verhalten:" + self.__funktion.funktion_user_kurz).grid(row=0, column=0,sticky=tk.W)
            if not "x" in self.__funktion.funktion_user_x_ersetztbar:
                wert = eval(self.__funktion.funktion_computer_readable)
                tk.Label(self, text="lim x->∞ = " + str(wert)).grid(row=0, column=0, sticky=tk.W)
                tk.Label(self, text="lim x->-∞ = " + str(wert)).grid(row=0, column=0, sticky=tk.W)
            elif self.__funktion.is_polinomfunktion:
                pass
            else:
                tk.Label(self, text="Globales Verhalten für nicht Polinomfunktionen comming soon..." + self.__funktion.funktion_user_kurz).grid(row=1, column=0,sticky=tk.W)
        else:
            tk.Label(self, text="Für Berechnung des globalen Verhaltens Funktion oben eingeben").grid(row=0, column=0)