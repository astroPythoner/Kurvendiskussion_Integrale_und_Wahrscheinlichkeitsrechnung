import math
import tkinter as tk

from Grundklassen import Fläche

class Intergral_Frame(tk.Frame):

    __funktion = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.flächen = [Fläche(0.9,0.6,"blaugrau","Intergral")]
        self.x_start = tk.IntVar()
        self.last_x_start_wert = 0
        self.x_ende = tk.IntVar()
        self.last_x_ende_wert = 0
        self.update()

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def start_x_changed(self,wert=None):
        if wert != self.last_x_start_wert:
            self.last_x_start_wert = wert
            self.flächen[0].von_x = self.x_start.get()
            self.createWidgets()
            if self.x_start.get() > self.x_ende.get():
                self.x_ende.set(self.x_start.get())

    def end_x_changed(self,wert=None):
        if wert != self.last_x_ende_wert:
            self.last_x_ende_wert = wert
            self.flächen[0].bis_x = self.x_ende.get()
            self.createWidgets()
            if self.x_ende.get() < self.x_start.get():
                self.x_start.set(self.x_ende.get())

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
            tk.Label(self, text="Intergrale comming soon...").grid(row=2, column=0)
        else:
            tk.Label(self, text="Für Intergrale Funktion oben eingeben").grid(row=0, column=0)