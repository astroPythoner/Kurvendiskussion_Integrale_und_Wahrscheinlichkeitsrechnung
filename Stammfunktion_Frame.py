import math
import tkinter as tk

class Stammfunktion_Frame(tk.Frame):

    __funktion = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.update()

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()


    def stammfunktion_bestimmen(self):
        if self.__funktion.is_polinomfunktion:
            pass


    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            self.stammfunktion_bestimmen()
            tk.Label(self, text="Stammfunktion comming soon...").grid(row=0, column=0)
        else:
            tk.Label(self, text="Für Stammfunktion Funktion oben eingeben").grid(row=0, column=0)