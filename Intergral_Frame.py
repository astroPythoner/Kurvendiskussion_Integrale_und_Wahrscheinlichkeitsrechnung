import math
import tkinter as tk

from Grundklassen import Fläche

class Intergral_Frame(tk.Frame):

    __funktion = None
    stammfunktion = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.flächen = [Fläche(0.9,0.6,"blaugrau","Intergral")]
        self.x_start = tk.IntVar()
        self.x_start.set(-1)
        self.last_x_start_wert = -1
        self.x_ende = tk.IntVar()
        self.x_ende.set(1)
        self.last_x_ende_wert = 1
        self.update()

    def add_stammfunktion(self,stammfunktion):
        self.stammfunktion = stammfunktion

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def start_x_changed(self,wert=None):
        if wert != self.last_x_start_wert:
            self.last_x_start_wert = wert
            self.flächen[0].von_x = self.x_start.get()
            self.createWidgets()
            if self.x_start.get() >= self.x_ende.get():
                self.x_ende.set(self.x_start.get()+1)

    def end_x_changed(self,wert=None):
        if wert != self.last_x_ende_wert:
            self.last_x_ende_wert = wert
            self.flächen[0].bis_x = self.x_ende.get()
            self.createWidgets()
            if self.x_ende.get() <= self.x_start.get():
                self.x_start.set(self.x_ende.get()-1)

    def intergral_berechnen(self):
        stammfunktion = self.stammfunktion.funktionen[0].funktion
        tk.Label(self, text="Stammfunktion: "+stammfunktion.funktion_user_kurz).grid(row=2, column=1)
        tk.Label(self, text="1. Beide Werte in Stammfunktion einsetzen:").grid(row=3, column=0,sticky=tk.W,columnspan=2)
        erster_wert = stammfunktion.x_einsetzen(self.x_start.get())
        zweiter_wert = stammfunktion.x_einsetzen(self.x_ende.get())
        tk.Label(self, text="F("+str(self.x_start.get())+") = "+str(erster_wert)).grid(row=4, column=1, sticky=tk.W)
        tk.Label(self, text="F("+str(self.x_ende.get())+") = "+str(zweiter_wert)).grid(row=5, column=1, sticky=tk.W)
        tk.Label(self, text="2. Differenz der beiden Werte finden:").grid(row=6, column=0, sticky=tk.W, columnspan=2)
        erg = abs(erster_wert-zweiter_wert)
        tk.Label(self, text="| "+str(erster_wert)+" - "+str(zweiter_wert)+" | = "+str(erg)).grid(row=7, column=1)

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            self.x_start_regler = tk.Scale(self, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.x_start)
            self.x_start_regler.config(command=self.start_x_changed)
            self.x_start_regler.grid(row=0, column=0, sticky=tk.NSEW)
            self.x_start_spinbox = tk.Spinbox(self, from_=-100, to=100, textvariable=self.x_start)
            self.x_start_spinbox.config(command=self.start_x_changed)
            self.x_start_spinbox.grid(row=0, column=1, sticky=tk.W)
            self.x_ende_regler = tk.Scale(self, from_=-100, to=100, orient=tk.HORIZONTAL, variable=self.x_ende)
            self.x_ende_regler.config(command=self.end_x_changed)
            self.x_ende_regler.grid(row=1, column=0, sticky=tk.NSEW)
            self.x_ende_spinbox = tk.Spinbox(self, from_=-100, to=100, textvariable=self.x_ende)
            self.x_ende_spinbox.config(command=self.end_x_changed)
            self.x_ende_spinbox.grid(row=1, column=1, sticky=tk.W)
            if self.stammfunktion == None or len(self.stammfunktion.funktionen) == 0 or self.stammfunktion.funktionen[0].funktion == None:
                tk.Label(self, text="Keine Stammfunktion gefunden").grid(row=2, column=0)
            else:
                self.intergral_berechnen()
        else:
            tk.Label(self, text="Für Intergrale Funktion oben eingeben").grid(row=0, column=0)