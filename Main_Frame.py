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
import Sonstiges_Frame

import RandomFunktion
import Funktion

root = None

DEBUG = True

class MainWindow(tk.Frame):

    funktion = Funktion.Funktion()
    frames = []
    head_frames = []

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
            for head_frame in self.head_frames:
                head_frame.canvas.delete(tk.ALL)
                head_frame.canvas.create_window((0, 0), window=head_frame.frame, anchor="nw")
                head_frame.canvas.configure(yscrollcommand=head_frame.y_scrollbar.set, xscrollcommand=head_frame.x_scrollbar.set)

            self.Graph_Frame.update(self.funktion)
            self.eingabe_passt.config(text="Funktion passt")
            if self.funktion.is_polynomfunktion:
                text = "Polynomfunktion: " + self.funktion.funktion_polynom_x_ersetzbar
            elif self.funktion.is_wurzel:
                text = "Wurzelfunktion: " + self.funktion.funktion_wurzel_x_ersetzbar
            elif self.funktion.is_logarithmus:
                text = "Logarithmusfunktion: " + self.funktion.funktion_logarithmus_x_ersetzbar
            elif self.funktion.is_trigonometrisch:
                text = "Trigonometrische Funktion: " + self.funktion.funktion_trigonometrisch_x_ersetzbar
            elif self.funktion.is_exponential:
                text = "Exponentialfunktion: " + self.funktion.funktion_exponential_x_ersetzbar
            else:
                text = "Funktionstyp nicht bekannt"
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

        self.schnittpunktYAchse_head_frame = ScrollableFrame(self,SchnittpunktYAchse_Frame.SchnittpunktYAchse_Frame)
        self.schnittpunktYAchse_Frame = self.schnittpunktYAchse_head_frame.frame
        self.frames.append(self.schnittpunktYAchse_Frame)
        self.head_frames.append(self.schnittpunktYAchse_head_frame)
        self.pane.add(self.schnittpunktYAchse_head_frame.head_frame, text="Schnittpunkt Y Achse", padding=0)

        self.nullstellen_head_frame = ScrollableFrame(self,Nullstellen_Frame.Nullstellen_Frame)
        self.Nullstellen_Frame = self.nullstellen_head_frame.frame
        self.frames.append(self.Nullstellen_Frame)
        self.head_frames.append(self.nullstellen_head_frame)
        self.pane.add(self.nullstellen_head_frame.head_frame, text="Nullstellen", padding=0)

        self.globalsverhalten_head_frame = ScrollableFrame(self,GlobalesVerhalten_Frame.GlobalesVerhalten_Frame)
        self.GlobalesVerhalten_Frame = self.globalsverhalten_head_frame.frame
        self.frames.append(self.GlobalesVerhalten_Frame)
        self.head_frames.append(self.globalsverhalten_head_frame)
        self.pane.add(self.globalsverhalten_head_frame.head_frame, text="Globales Verhalten", padding=0)

        self.ablteitung_head_frame = ScrollableFrame(self,Ableitung_Frame.Ableitung_Frame)
        self.Ableitung_Frame = self.ablteitung_head_frame.frame
        self.frames.append(self.Ableitung_Frame)
        self.head_frames.append(self.ablteitung_head_frame)
        self.pane.add(self.ablteitung_head_frame.head_frame, text="Ableitung", padding=0)

        self.tangentenormale_head_frame = ScrollableFrame(self,TangenteNormale_Frame.TangenteNormale_Frame,self.Ableitung_Frame)
        self.TangenteNormale_Frame = self.tangentenormale_head_frame.frame
        self.frames.append(self.TangenteNormale_Frame)
        self.head_frames.append(self.tangentenormale_head_frame)
        self.pane.add(self.tangentenormale_head_frame.head_frame, text="Normale/Tangente", padding=0)

        self.steigung_head_frame = ScrollableFrame(self,Steigung_Frame.Steigung_Frame,self.Ableitung_Frame)
        self.Steigung_Frame = self.steigung_head_frame.frame
        self.frames.append(self.Steigung_Frame)
        self.head_frames.append(self.steigung_head_frame)
        self.pane.add(self.steigung_head_frame.head_frame, text="Steigung", padding=0)

        self.kruemmung_head_frame = ScrollableFrame(self,Kruemmung_Frame.Kruemmung_Frame,self.Ableitung_Frame)
        self.Kruemmung_Frame = self.kruemmung_head_frame.frame
        self.frames.append(self.Kruemmung_Frame)
        self.head_frames.append(self.kruemmung_head_frame)
        self.pane.add(self.kruemmung_head_frame.head_frame, text="Krümmung", padding=0)

        self.stammfunktion_head_frame = ScrollableFrame(self,Stammfunktion_Frame.Stammfunktion_Frame)
        self.Stammfunktion_Frame = self.stammfunktion_head_frame.frame
        self.frames.append(self.Stammfunktion_Frame)
        self.head_frames.append(self.stammfunktion_head_frame)
        self.pane.add(self.stammfunktion_head_frame.head_frame, text="Stammfunktion", padding=0)

        self.integrale_head_frame = ScrollableFrame(self,Integral_Frame.Integral_Frame,self.Stammfunktion_Frame,self.Nullstellen_Frame)
        self.Integrale_Frame = self.integrale_head_frame.frame
        self.frames.append(self.Integrale_Frame)
        self.head_frames.append(self.integrale_head_frame)
        self.pane.add(self.integrale_head_frame.head_frame, text="Integral", padding=0)

        self.sonstiges_head_frame = ScrollableFrame(self,Sonstiges_Frame.Sonstiges_Frame,DEBUG)
        self.Sonstige_Frame = self.sonstiges_head_frame.frame
        self.frames.append(self.Sonstige_Frame)
        self.head_frames.append(self.sonstiges_head_frame)
        self.pane.add(self.sonstiges_head_frame.head_frame, text="Sonstiges", padding=0)

        self.funktion.add_debug_sonstiges_frame(self.Sonstige_Frame)
        self.Graph_Frame.add_frames(self.schnittpunktYAchse_Frame, self.Nullstellen_Frame, self.Ableitung_Frame, self.TangenteNormale_Frame, self.Steigung_Frame, self.Kruemmung_Frame, self.Stammfunktion_Frame, self.Integrale_Frame)


class ScrollableFrame():
    def __init__(self,master,frame,*args):
        self.master = master
        self.head_frame = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.head_frame)
        self.y_scrollbar = ttk.Scrollbar(self.head_frame, orient="vertical", command=self.canvas.yview)
        self.x_scrollbar = ttk.Scrollbar(self.head_frame, orient="horizontal", command=self.canvas.xview)
        self.frame = frame(self.canvas,*args)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")
        self.x_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

    def update(self):
        self.head_frame.destroy()
        self.head_frame = tk.Frame(self.master)
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.head_frame)
        self.y_scrollbar = ttk.Scrollbar(self.head_frame, orient="vertical", command=self.canvas.yview)
        self.x_scrollbar = ttk.Scrollbar(self.head_frame, orient="horizontal", command=self.canvas.xview)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")
        self.x_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Kurvendiskussion - v2.1.0")
    root.resizable(0,0)
    app = MainWindow(master=root)
    app.mainloop()
    print("shutting down")
    root.destroy()