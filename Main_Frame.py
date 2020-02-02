# Programm das nach Eingabe eines Funktionsterms alle Punkte zur Kurvendiskussion automatisch berechnet

# Copyright 2019

import tkinter as tk
from tkinter import ttk
from random import randint

import SchnittpunktYAchse_Frame
import Ableitung_Frame
import Nullstellen_Frame
import GlobalesVerhalten_Frame
import Steigung_Frame
import Kruemmung_Frame
import Graph_Frame
import TangenteNormale_Frame
import Stammfunktion_Frame
import Integral_Frame

import RandomFunktion
import Funktion

root = None

DEBUG = False

class MainWindow(tk.Frame):

    funktion = Funktion.Funktion()
    frames = []

    funktionsrandom = RandomFunktion.Random_Funtkionen()

    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.createWidgets()
        self.funktion_random_erstellen_button_pressed()

    def funktion_uebernehmen_button_pressed(self):
        passt = self.funktion.set_funktion(self.eingabe.get())
        if passt==True:
            for frame in self.frames:
                frame.update(self.funktion)
            self.Graph_Frame.update(self.funktion)
            self.eingabe_passt.config(text="Funktion passt")
            if DEBUG:
                text = "Debug: "+self.eingabe.get()+"\n = "+self.funktion.funktion_user_x_ersetztbar+"\n = "+self.funktion.funktion_user_kurz+"\n = "+self.funktion.funktion_computer_readable
                if self.funktion.is_polynomfunktion:
                    text += "\n Exponenten: "+str(self.funktion.exponenten_array)
                    text += "\n = " + str(self.funktion.funktion_polynom_x_ersetzbar)
                    text += "\n = " + str(self.funktion.funktion_polynom_computer_readable)
                else:
                    text += "\n keine Exponentialgleichung"
            else:
                if self.funktion.is_polynomfunktion:
                    text = "Polynomfunktion: "+self.funktion.funktion_user_kurz
                else:
                    text = self.funktion.funktion_user_kurz + "\nTipp: gebe eine Polynomfunktion ein (z.B.: 4x'3 + 2x'2 + 9x)"
            self.funktion_info_text.config(text=text)
        elif passt == "unverändert":
            self.eingabe_passt.config(text="Funktion nicht verändert")
        else:
            self.eingabe_passt.config(text="Funktion fehlerhaft")

    def funktion_random_erstellen_button_pressed(self):
        self.eingabe.delete(0,tk.END)
        random_funktion = self.funktionsrandom.get_random_funktion()
        if isinstance(random_funktion, Funktion.Funktion):
            self.eingabe.insert(0, random_funktion.funktion_user_x_ersetztbar)
            self.eingabe_passt.config(text="Zufallsfunktion hinzugefügt")

    def createWidgets(self):

        #Eingabefeld
        self.formlezeichen_info = tk.Label(self,text="plus: +\nminus: -\nmal: *\ngeteilt: /\nhochzahlen: '\nKommazahlen: 1.5\nkonstanten: pi,e\nsin(), cos(), tan(), arcsin(),...\nlog(wert,basis), log10(), ln()")
        self.formlezeichen_info.grid(row=0, column=0, sticky=tk.W, rowspan=2)
        self.eingabe_info = tk.Label(self,text="Hier Funktion eingeben: f(x)=")
        self.eingabe_info.grid(row=0, column=1, sticky=tk.E)
        self.eingabe = tk.Entry(self)
        self.eingabe.grid(row=0,column=2, sticky=tk.EW)
        self.eingabe_button = tk.Button(self, text="übernehmen",command=self.funktion_uebernehmen_button_pressed)
        self.eingabe_button.grid(row=0, column=3, sticky=tk.W)
        self.random_funktion_button = tk.Button(self, text="zufällige Funktion", command=self.funktion_random_erstellen_button_pressed)
        self.random_funktion_button.grid(row=1, column=3, sticky=tk.NW)
        self.random_einstellungen = tk.Button(self, text="Zufallsfunktion Einstellungen", command=lambda *args: RandomFunktion.Remote_Settings(self, self.funktionsrandom))
        self.random_einstellungen.grid(row=1, column=4, sticky=tk.NW)
        self.eingabe_passt = tk.Label(self, text="")
        self.eingabe_passt.grid(row=0, column=4, sticky=tk.W)
        self.funktion_info_text = tk.Label(self, text="")
        self.funktion_info_text.grid(row=1, column=1, columnspan=2)

        #Notebook zur Auswsahl der Kurvendiskussionsthemen
        self.pane = ttk.Notebook(self)
        self.pane.grid(row=2,column=0,columnspan=5,sticky=tk.NSEW)

        self.Graph_Frame = Graph_Frame.Graph_Frame()
        self.pane.add(self.Graph_Frame, text="Graph", padding=0)
        self.schnittpunktYAchse_Frame = SchnittpunktYAchse_Frame.SchnittpunktYAchse_Frame()
        self.frames.append(self.schnittpunktYAchse_Frame)
        self.pane.add(self.schnittpunktYAchse_Frame, text="Schnittpunkt Y Achse", padding=0)
        self.Nullsetllen_Frame = Nullstellen_Frame.Nullstellen_Frame()
        self.frames.append(self.Nullsetllen_Frame)
        self.pane.add(self.Nullsetllen_Frame, text="Nullstellen", padding=0)
        self.GlobalesVerhalten_Frame = GlobalesVerhalten_Frame.GlobalesVerhalten_Frame()
        self.frames.append(self.GlobalesVerhalten_Frame)
        self.pane.add(self.GlobalesVerhalten_Frame, text="Globales Verhalten", padding=0)
        self.Ableitung_Frame = Ableitung_Frame.Ableitung_Frame()
        self.frames.append(self.Ableitung_Frame)
        self.TangenteNormale_Frame = TangenteNormale_Frame.TangenteNormale_Frame(self.Ableitung_Frame)
        self.frames.append(self.TangenteNormale_Frame)
        self.pane.add(self.TangenteNormale_Frame, text="Normale/Tangente", padding=0)
        self.pane.add(self.Ableitung_Frame, text="Ableitung", padding=0)
        self.Steigung_Frame = Steigung_Frame.Steigung_Frame(self.Ableitung_Frame)
        self.frames.append(self.Steigung_Frame)
        self.pane.add(self.Steigung_Frame, text="Steigung", padding=0)
        self.Kruemmung_Frame = Kruemmung_Frame.Kruemmung_Frame(self.Ableitung_Frame)
        self.frames.append(self.Kruemmung_Frame)
        self.pane.add(self.Kruemmung_Frame, text="Krümmung", padding=0)
        self.Stammfunktion_Frame = Stammfunktion_Frame.Stammfunktion_Frame()
        self.frames.append(self.Stammfunktion_Frame)
        self.pane.add(self.Stammfunktion_Frame, text="Stammfunktion", padding=0)
        self.Integrale_Frame = Integral_Frame.Integral_Frame(self.Stammfunktion_Frame,self.Nullsetllen_Frame)
        self.frames.append(self.Integrale_Frame)
        self.pane.add(self.Integrale_Frame, text="Integral", padding=0)

        self.Graph_Frame.add_frames(self.schnittpunktYAchse_Frame,self.Nullsetllen_Frame,self.Ableitung_Frame,self.TangenteNormale_Frame,self.Steigung_Frame,self.Kruemmung_Frame,self.Stammfunktion_Frame,self.Integrale_Frame)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Kurvendiskussion - v1.2.1")
    root.resizable(0,0)
    app = MainWindow(master=root)
    app.mainloop()
    print("shutting down")
    root.destroy()