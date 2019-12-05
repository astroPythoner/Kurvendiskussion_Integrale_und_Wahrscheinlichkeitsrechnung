# Programm das nach Eingabe eines Funktionsterms alle Punkte zur Kurvendiskussion automatisch berechnet

# Copyright 2019

import tkinter as tk
from tkinter import ttk

import SchnittpunktYAchse_Frame
import Ableitung_Frame
import Nullstellen_Frame
import GlobalesVerhalten_Frame
import Steigung_Frame
import Kruemmung_Frame
import Symmetrie_Frame
import Graph_Frame

import Funktion

root = None

DEBUG = True

class MainWindow(tk.Frame):

    funktion = Funktion.Funktion()
    frames = []

    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.createWidgets()

    def funktion_übernehmen_button_pressed(self):
        passt = self.funktion.set_funktion(self.eingabe.get())
        if passt==True:
            for frame in self.frames:
                frame.update(self.funktion)
            self.eingabe_passt.config(text="Funktion passt")
            if DEBUG:
                text = self.eingabe.get()+"\n = "+self.funktion.funktion_user_x_ersetztbar+"\n = "+self.funktion.funktion_user_kurz+"\n = "+self.funktion.funktion_computer_readable
                if self.funktion.is_exponential:
                    text += "\n Exponenten: "+str(self.funktion.exponenten_array)
                    text += "\n = " + str(self.funktion.funktion_exponential_x_ersetzbar)
                    text += "\n = " + str(self.funktion.funktion_exponential_computer_readable)
                else:
                    text += "\n keine Exponentialgleichung"
                self.debug.config(text=text)
        elif passt == "unverändert":
            self.eingabe_passt.config(text="Funktion nicht verändert")
        else:
            self.eingabe_passt.config(text="Funktion fehlerhaft")

    def createWidgets(self):

        #Eingabefeld
        self.formlezeichen_info = tk.Label(self, text="plus: +\nminus: -\nmal: *\ngeteilt: /\nhochzahlen: '\npi,e, c,g\nsin,cos,tan,arcsin,...")
        self.formlezeichen_info.grid(row=0, column=0, sticky=tk.W)
        self.eingabe_info = tk.Label(self,text="Hier Funktion eingeben: f(x)=")
        self.eingabe_info.grid(row=0, column=1, sticky=tk.E)
        self.eingabe = tk.Entry(self)
        self.eingabe.grid(row=0,column=2, sticky=tk.EW)
        self.eingabe_button = tk.Button(self, text="übernehmen",command=self.funktion_übernehmen_button_pressed)
        self.eingabe_button.grid(row=0, column=3, sticky=tk.W)
        self.eingabe_passt = tk.Label(self, text="")
        self.eingabe_passt.grid(row=0, column=4, sticky=tk.W)
        if DEBUG:
            self.debug = tk.Label(self, text="")
            self.debug.grid(row=1, column=0,columnspan=5)

        #Note-Book zur Auswsahl der Kurvendiskussionsthemen
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
        self.pane.add(self.Ableitung_Frame, text="Ableitung", padding=0)
        self.Steigung_Frame = Steigung_Frame.Steigung_Frame()
        self.frames.append(self.Steigung_Frame)
        self.pane.add(self.Steigung_Frame, text="Steigung", padding=0)
        self.Krümmung_Frame = Kruemmung_Frame.Krümmung_Frame()
        self.frames.append(self.Krümmung_Frame)
        self.pane.add(self.Krümmung_Frame, text="Krümmung", padding=0)
        self.Symmetrie_Frame = Symmetrie_Frame.Symmetrie_Frame()
        self.frames.append(self.Symmetrie_Frame)
        self.pane.add(self.Symmetrie_Frame, text="Symmetrie", padding=0)

        self.Graph_Frame.add_frames(self.schnittpunktYAchse_Frame,self.Nullsetllen_Frame,self.Steigung_Frame,self.Krümmung_Frame)
        self.frames.append(self.Graph_Frame)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Kurvendiskussion")
    root.resizable(0,0)
    app = MainWindow(master=root)
    app.mainloop()
    print("shutting down")
    root.destroy()