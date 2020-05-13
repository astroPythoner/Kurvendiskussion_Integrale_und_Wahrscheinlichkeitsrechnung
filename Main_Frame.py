# Kurvendiskussion in tkinter:
# Programm das nach Eingabe eines Funktionsterms eine vollständige Kurvendiskussion erstellt
# mit weiteren Features wie Funktionszufallsgenerator oder Flächen/Integral Rechnung

# Copyright 2019-2020

import tkinter as tk
from tkinter import ttk
from tkinter import font

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

import Baumdiagramm_Frame
import Wahrscheinlichkeiten_Frame

import Grundklassen
import RandomFunktion
import Funktion

root = None

DEBUG = False


class MainWindow(tk.Frame):

    parameter = None
    funktion = None
    kurven_diskussion_frames = []
    kurven_diskussion_head_frames = []
    wahrscheinlichkeit_werte = None
    wahrscheinlichkeit_frames = []
    wahrscheinlichkeit_head_frames = []

    funktionsrandom = RandomFunktion.Random_Funktionen(parameter)

    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.parameter = Grundklassen.Parameter(self)
        self.funktion = Funktion.Funktion(self.parameter, "0")
        self.second_funktion = Funktion.Funktion(self.parameter, "0")
        self.wahrscheinlichkeit_werte = Grundklassen.Wahrscheinlichkeitsrechnung_werte()
        self.createWidgets()
        self.funktion_random_erstellen_button_pressed()

    def funktion_uebernehmen_button_pressed(self):
        passt = self.funktion.set_funktion(self.eingabe.get())

        if passt==True:
            if self.funktion.has_parameter or self.second_funktion.has_parameter:
                self.parameter_scale.configure(state=tk.NORMAL)
                self.parameter_move.configure(state=tk.NORMAL)
                self.parameter_stop.configure(state=tk.NORMAL)
            else:
                self.parameter_scale.configure(state=tk.DISABLED)
                self.parameter_move.configure(state=tk.DISABLED)
                self.parameter_stop.configure(state=tk.DISABLED)

            for frame in self.kurven_diskussion_frames:
                frame.update(self.funktion,self.second_funktion)
            for head_frame in self.kurven_diskussion_head_frames:
                head_frame.canvas.delete(tk.ALL)
                head_frame.canvas.create_window((0, 0), window=head_frame.frame, anchor="nw")
                head_frame.canvas.configure(yscrollcommand=head_frame.y_scrollbar.set, xscrollcommand=head_frame.x_scrollbar.set)

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
            elif self.funktion.has_parameter:
                text = "Paramterfunktion: "+self.funktion.funktion_user_kurz
            else:
                text = "Funktionstyp nicht bekannt: "+self.funktion.funktion_user_kurz
            self.funktion_info_text.config(text=text)

        elif passt == "unverändert":
            self.eingabe_passt.config(text="Funktion nicht verändert")
        else:
            self.eingabe_passt.config(text="Funktion fehlerhaft")
    def second_funktion_uebernehmen_button_pressed(self):
        if self.second_funktion_eingabe.get() == "":
            self.second_funktion.set_funktion("0")
            passt = True
        else:
            passt = self.second_funktion.set_funktion(self.second_funktion_eingabe.get())

        if passt == True:
            if self.funktion.has_parameter or self.second_funktion.has_parameter:
                self.parameter_scale.configure(state=tk.NORMAL)
                self.parameter_move.configure(state=tk.NORMAL)
                self.parameter_stop.configure(state=tk.NORMAL)
            else:
                self.parameter_scale.configure(state=tk.DISABLED)
                self.parameter_move.configure(state=tk.DISABLED)
                self.parameter_stop.configure(state=tk.DISABLED)

            for frame in self.kurven_diskussion_frames:
                frame.update(self.funktion,self.second_funktion)
            for head_frame in self.kurven_diskussion_head_frames:
                head_frame.canvas.delete(tk.ALL)
                head_frame.canvas.create_window((0, 0), window=head_frame.frame, anchor="nw")
                head_frame.canvas.configure(yscrollcommand=head_frame.y_scrollbar.set, xscrollcommand=head_frame.x_scrollbar.set)

            if self.second_funktion.funktion_user_kurz == "0":
                self.second_funktion_eingabe_passt.config(text="keine zweite Funktion")
            else:
                self.second_funktion_eingabe_passt.config(text="Funktion passt")

        elif passt == "unverändert":
            self.second_funktion_eingabe_passt.config(text="Funktion nicht verändert")
        else:
            self.second_funktion_eingabe_passt.config(text="Funktion fehlerhaft")
    def funktion_random_erstellen_button_pressed(self):
        self.eingabe.delete(0,tk.END)
        random_funktion = self.funktionsrandom.get_random_funktion()
        if isinstance(random_funktion, Funktion.Funktion):
            self.eingabe.insert(0, random_funktion.funktion_user_x_ersetztbar)
            self.eingabe_passt.config(text="Zufallsfunktion hinzugefügt")

    def change_parameter_value(self,cause):
        self.parameter.set_wert(self.parameter_scale.get())
        self.funktion_uebernehmen_button_pressed()
    def start_parameter_moving(self):
        self.parameter.start()
    def stop_parameter_moving(self):
        self.parameter.stop()
    def make_parameter_settings(self):
        Grundklassen.Parameter_Settings(self, self.parameter)
        self.parameter_scale.config(from_=self.parameter.min_wert, to=self.parameter.max_wert)

    def anz_moeglichkeiten_changed(self):
        self.wahrscheinlichkeit_werte.set_werte(anz_moeglichkeiten=self.moeglichkeiten.get())
        for widget in self.wahrscheinlichkeitsrechnungFrame.winfo_children():
            if not isinstance(widget, tk.Frame):
                if not isinstance(widget, ttk.Notebook):
                    widget.destroy()
        self.updateWahrscheinlichkeitsrechnungWidgets(self.wahrscheinlichkeitsrechnungFrame)
    def wahrscheinlichkeitswerte_uebernehmen_button_pressed(self):
        self.wahrscheinlichkeit_werte.set_werte(self.durchgaenge.get(),self.moeglichkeiten.get(),self.zuruecklegen.get(),self.get_names(),self.get_chances())
        for widget in self.wahrscheinlichkeitsrechnungFrame.winfo_children():
            if not isinstance(widget, tk.Frame):
                if not isinstance(widget, ttk.Notebook):
                    widget.destroy()
        self.createWahrscheinlichkeitsrechnungWidgets(self.wahrscheinlichkeitsrechnungFrame)
    def reset_names_button_pressed(self):
        for count,x in enumerate(self.moeglichk_name_entrys):
            x.delete(0,tk.END)
            x.insert(0, str(count+1))
    def reset_chance_button_pressed(self):
        for x in self.moeglichk_chance_entrys:
            x.delete(0,tk.END)
            x.insert(0, "1/" + str(self.wahrscheinlichkeit_werte.anz_moeglichkeiten))
    def get_names(self):
        return [x.get() for x in self.moeglichk_name_entrys]
    def get_chances(self):
        return [x.get() for x in self.moeglichk_chance_entrys]


    def createWidgets(self):
        self.head_pane = ttk.Notebook(self)
        self.head_pane.grid(row=4, column=0, columnspan=7, sticky=tk.NSEW)

        self.kurvendiskussionFrame = tk.Frame(width=1300)
        self.createKurvendiskussionWidgets(self.kurvendiskussionFrame)
        self.head_pane.add(self.kurvendiskussionFrame, text="Kurvendiskussion", padding=0)

        self.wahrscheinlichkeitsrechnungFrame = tk.Frame(width=1300)
        self.createWahrscheinlichkeitsrechnungWidgets(self.wahrscheinlichkeitsrechnungFrame)
        self.head_pane.add(self.wahrscheinlichkeitsrechnungFrame, text="Wahrscheinlichkeitsrechnung", padding=0)

    def createKurvendiskussionWidgets(self,frame):
        #Eingabefeld
        self.formlezeichen_info = tk.Label(frame,text="plus: +\nminus: -\nmal: *\ngeteilt: /\nhochzahlen: '\nKommazahlen: 1.5\nkonstanten: pi,e\nsin(), cos(), tan(), arcsin(),...\nlog(wert,basis), log10(), ln()\n√: sqrt() oder wurzel()")
        self.formlezeichen_info.grid(row=0, column=0, sticky=tk.W, rowspan=2)
        self.eingabe_info = tk.Label(frame,text="Hier Funktion eingeben: ƒ(x)=")
        self.eingabe_info.grid(row=0, column=1, sticky=tk.E)
        self.eingabe = tk.Entry(frame)
        self.eingabe.grid(row=0,column=2, sticky=tk.EW)
        self.eingabe_button = tk.Button(frame, text="übernehmen",command=self.funktion_uebernehmen_button_pressed)
        self.eingabe_button.grid(row=0, column=3, sticky=tk.W)
        self.random_funktion_button = tk.Button(frame, text="zufällige Funktion", command=self.funktion_random_erstellen_button_pressed)
        self.random_funktion_button.grid(row=1, column=3, sticky=tk.NW)
        self.random_einstellungen = tk.Button(frame, text="Zufallsfunktion Einstellungen", command=lambda *args: RandomFunktion.Remote_Settings(self, self.funktionsrandom))
        self.random_einstellungen.grid(row=1, column=4, columnspan=3, sticky=tk.NW)
        self.eingabe_passt = tk.Label(frame, text="")
        self.eingabe_passt.grid(row=0, column=4, columnspan=3, sticky=tk.W)
        self.funktion_info_text = tk.Label(frame, text="")
        self.funktion_info_text.grid(row=1, column=1, columnspan=2)
        self.parameter_text = tk.Label(frame, text="Parameter k:")
        self.parameter_text.grid(row=2, column=0, sticky=tk.E)
        self.parameter_scale = tk.Scale(frame, from_=self.parameter.min_wert, to=self.parameter.max_wert, orient=tk.HORIZONTAL, resolution=0.1, command=self.change_parameter_value)
        self.parameter_scale.grid(row=2, column=1, columnspan=3,sticky=tk.EW)
        self.parameter_move = tk.Button(frame, text="►", command=self.start_parameter_moving)
        self.parameter_move.grid(row=2, column=4, sticky=tk.E)
        self.parameter_stop = tk.Button(frame, text="█", command=self.stop_parameter_moving)
        self.parameter_stop.grid(row=2, column=5, sticky=tk.W)
        self.parameter_settings = tk.Button(frame, text="Einstellungen Parameter", command=self.make_parameter_settings)
        self.parameter_settings.grid(row=2, column=6, sticky=tk.W)
        self.second_funktion_text = tk.Label(frame, text="Zweite Funktion: g(x)=")
        self.second_funktion_text.grid(row=3, column=1, sticky=tk.E)
        self.second_funktion_eingabe = tk.Entry(frame)
        self.second_funktion_eingabe.grid(row=3, column=2, sticky=tk.EW)
        self.second_funktion_ubernehmen = tk.Button(frame, text="übernehmen", command=self.second_funktion_uebernehmen_button_pressed)
        self.second_funktion_ubernehmen.grid(row=3, column=3, sticky=tk.W)
        self.second_funktion_eingabe_passt = tk.Label(frame, text="")
        self.second_funktion_eingabe_passt.grid(row=3, column=4, columnspan=3, sticky=tk.W)

        #Notebook zur Auswsahl der Kurvendiskussionsthemen
        self.kurvendiskussion_pane = ttk.Notebook(frame,width=1300,height=570)
        self.kurvendiskussion_pane.grid(row=4, column=0, columnspan=7, sticky=tk.NSEW)

        self.Graph_Frame = ScrollableFrame(frame,Graph_Frame.Graph_Frame,self.parameter)
        self.kurvendiskussion_pane.add(self.Graph_Frame.head_frame, text="Graph", padding=0)

        self.schnittpunktYAchse_head_frame = ScrollableFrame(frame,SchnittpunktYAchse_Frame.SchnittpunktYAchse_Frame)
        self.schnittpunktYAchse_Frame = self.schnittpunktYAchse_head_frame.frame
        self.kurven_diskussion_frames.append(self.schnittpunktYAchse_Frame)
        self.kurven_diskussion_head_frames.append(self.schnittpunktYAchse_head_frame)
        self.kurvendiskussion_pane.add(self.schnittpunktYAchse_head_frame.head_frame, text="Schnittpunkt Y Achse", padding=0)

        self.nullstellen_head_frame = ScrollableFrame(frame,Nullstellen_Frame.Nullstellen_Frame,self.parameter)
        self.Nullstellen_Frame = self.nullstellen_head_frame.frame
        self.kurven_diskussion_frames.append(self.Nullstellen_Frame)
        self.kurven_diskussion_head_frames.append(self.nullstellen_head_frame)
        self.kurvendiskussion_pane.add(self.nullstellen_head_frame.head_frame, text="Nullstellen", padding=0)

        self.globalsverhalten_head_frame = ScrollableFrame(frame,GlobalesVerhalten_Frame.GlobalesVerhalten_Frame)
        self.GlobalesVerhalten_Frame = self.globalsverhalten_head_frame.frame
        self.kurven_diskussion_frames.append(self.GlobalesVerhalten_Frame)
        self.kurven_diskussion_head_frames.append(self.globalsverhalten_head_frame)
        self.kurvendiskussion_pane.add(self.globalsverhalten_head_frame.head_frame, text="Globales Verhalten", padding=0)

        self.ablteitung_head_frame = ScrollableFrame(frame,Ableitung_Frame.Ableitung_Frame,self.parameter)
        self.Ableitung_Frame = self.ablteitung_head_frame.frame
        self.kurven_diskussion_frames.append(self.Ableitung_Frame)
        self.kurven_diskussion_head_frames.append(self.ablteitung_head_frame)
        self.kurvendiskussion_pane.add(self.ablteitung_head_frame.head_frame, text="Ableitung", padding=0)

        self.tangentenormale_head_frame = ScrollableFrame(frame,TangenteNormale_Frame.TangenteNormale_Frame,self.parameter,self.Ableitung_Frame)
        self.TangenteNormale_Frame = self.tangentenormale_head_frame.frame
        self.kurven_diskussion_frames.append(self.TangenteNormale_Frame)
        self.kurven_diskussion_head_frames.append(self.tangentenormale_head_frame)
        self.kurvendiskussion_pane.add(self.tangentenormale_head_frame.head_frame, text="Normale/Tangente", padding=0)

        self.steigung_head_frame = ScrollableFrame(frame,Steigung_Frame.Steigung_Frame,self.parameter,self.Ableitung_Frame)
        self.Steigung_Frame = self.steigung_head_frame.frame
        self.kurven_diskussion_frames.append(self.Steigung_Frame)
        self.kurven_diskussion_head_frames.append(self.steigung_head_frame)
        self.kurvendiskussion_pane.add(self.steigung_head_frame.head_frame, text="Steigung", padding=0)

        self.kruemmung_head_frame = ScrollableFrame(frame,Kruemmung_Frame.Kruemmung_Frame,self.parameter,self.Ableitung_Frame)
        self.Kruemmung_Frame = self.kruemmung_head_frame.frame
        self.kurven_diskussion_frames.append(self.Kruemmung_Frame)
        self.kurven_diskussion_head_frames.append(self.kruemmung_head_frame)
        self.kurvendiskussion_pane.add(self.kruemmung_head_frame.head_frame, text="Krümmung", padding=0)

        self.stammfunktion_head_frame = ScrollableFrame(frame,Stammfunktion_Frame.Stammfunktion_Frame,self.parameter)
        self.Stammfunktion_Frame = self.stammfunktion_head_frame.frame
        self.kurven_diskussion_frames.append(self.Stammfunktion_Frame)
        self.kurven_diskussion_head_frames.append(self.stammfunktion_head_frame)
        self.kurvendiskussion_pane.add(self.stammfunktion_head_frame.head_frame, text="Stammfunktion", padding=0)

        self.sonstiges_head_frame = ScrollableFrame(frame, Sonstiges_Frame.Sonstiges_Frame, DEBUG)
        self.Sonstige_Frame = self.sonstiges_head_frame.frame

        self.integrale_head_frame = ScrollableFrame(frame,Integral_Frame.Integral_Frame,self.Stammfunktion_Frame,self.Sonstige_Frame,self.Nullstellen_Frame,self.Graph_Frame.frame,self.parameter)
        self.Integrale_Frame = self.integrale_head_frame.frame
        self.kurven_diskussion_frames.append(self.Integrale_Frame)
        self.kurven_diskussion_head_frames.append(self.integrale_head_frame)
        self.kurvendiskussion_pane.add(self.integrale_head_frame.head_frame, text="Integral", padding=0)

        self.kurven_diskussion_frames.append(self.Sonstige_Frame)
        self.kurven_diskussion_head_frames.append(self.sonstiges_head_frame)
        self.kurvendiskussion_pane.add(self.sonstiges_head_frame.head_frame, text="Sonstiges", padding=0)

        self.kurven_diskussion_frames.append(self.Graph_Frame.frame)
        self.kurven_diskussion_head_frames.append(self.Graph_Frame)

        self.funktion.add_debug_sonstiges_frame(self.Sonstige_Frame)
        self.Graph_Frame.frame.add_frames(self.schnittpunktYAchse_Frame, self.Nullstellen_Frame, self.Ableitung_Frame, self.TangenteNormale_Frame, self.Steigung_Frame, self.Kruemmung_Frame, self.Stammfunktion_Frame, self.Integrale_Frame, self.Sonstige_Frame)

    def updateWahrscheinlichkeitsrechnungWidgets(self,frame):
        rechts = self.wahrscheinlichkeit_werte.anz_moeglichkeiten + 2
        mitte = int(rechts / 2)
        # Eingabefeld
        self.durchgaenge = tk.IntVar()
        self.durchgaenge.set(self.wahrscheinlichkeit_werte.anz_durchgaenge)
        self.durchgaenge_info = tk.Label(frame, text="Durchgänge:")
        self.durchgaenge_info.grid(row=0, column=0, sticky=tk.E, columnspan=mitte)
        self.durchgaenge_spinbox = tk.Spinbox(frame, from_=1, to=50, textvariable=self.durchgaenge)
        self.durchgaenge_spinbox.grid(row=0, column=mitte, sticky=tk.W, columnspan=mitte)
        self.moeglichkeiten = tk.IntVar()
        self.moeglichkeiten.set(self.wahrscheinlichkeit_werte.anz_moeglichkeiten)
        self.moeglichkeiten_info = tk.Label(frame, text="Anzahl Möglichkeiten:")
        self.moeglichkeiten_info.grid(row=1, column=0, sticky=tk.E, columnspan=mitte)
        self.moeglichkeiten_spinbox = tk.Spinbox(frame, from_=1, to=20, textvariable=self.moeglichkeiten, command=self.anz_moeglichkeiten_changed)
        self.moeglichkeiten_spinbox.grid(row=1, column=mitte, sticky=tk.W, columnspan=mitte)
        self.zuruecklegen = tk.BooleanVar()
        self.zuruecklegen.set(self.wahrscheinlichkeit_werte.zuruecklegen)
        self.mit_zuruecklegen_radiobutton = tk.Radiobutton(frame, text="Mit zurücklegen", variable=self.zuruecklegen, value=True)
        self.mit_zuruecklegen_radiobutton.grid(row=2, column=0, columnspan=mitte)
        self.ohne_zuruecklegen_radiobutton = tk.Radiobutton(frame, text="Ohne zurücklegen", variable=self.zuruecklegen, value=False)
        self.ohne_zuruecklegen_radiobutton.grid(row=2, column=mitte + 1, columnspan=mitte)
        self.moeglichk_info = tk.Label(frame, text="Möglichkeiten:")
        self.moeglichk_info.grid(row=3, column=0, sticky=tk.W, columnspan=rechts)
        self.moeglichk_name_info = tk.Label(frame, text="Name:")
        self.moeglichk_name_info.grid(row=4, column=0, sticky=tk.E)
        self.moeglichk_chance_info = tk.Label(frame, text="Chance:")
        self.moeglichk_chance_info.grid(row=5, column=0, sticky=tk.E)
        self.moeglichk_name_entrys = []
        self.moeglichk_chance_entrys = []
        for count,moeglichkeit in enumerate(range(self.wahrscheinlichkeit_werte.anz_moeglichkeiten)):
            entry_name = tk.Entry(frame, width=4)
            if count < len(self.wahrscheinlichkeit_werte.namen):
                entry_name.insert(0, self.wahrscheinlichkeit_werte.namen[count])
            else:
                entry_name.insert(0, count+1)
                self.wahrscheinlichkeit_werte.append_name(count+1)
            entry_name.grid(row=4, column=moeglichkeit + 1)
            self.moeglichk_name_entrys.append(entry_name)
            entry_chance = tk.Entry(frame, width=4)
            if count < len(self.wahrscheinlichkeit_werte.chancen):
                entry_chance.insert(0, self.wahrscheinlichkeit_werte.chancen[count])
            else:
                entry_chance.insert(0, "1/" + str(self.wahrscheinlichkeit_werte.anz_moeglichkeiten))
                self.wahrscheinlichkeit_werte.append_chance("1/" + str(self.wahrscheinlichkeit_werte.anz_moeglichkeiten))
            entry_chance.grid(row=5, column=moeglichkeit + 1)
            self.moeglichk_chance_entrys.append(entry_chance)
        self.moeglichk_name_reset_button = tk.Button(frame, text="durchnummerieren", command=self.reset_names_button_pressed)
        self.moeglichk_name_reset_button.grid(row=4, column=self.wahrscheinlichkeit_werte.anz_moeglichkeiten + 2)
        self.moeglichk_chance_reset_button = tk.Button(frame, text="gleichmäßig", command=self.reset_chance_button_pressed)
        self.moeglichk_chance_reset_button.grid(row=5, column=self.wahrscheinlichkeit_werte.anz_moeglichkeiten + 2)
        self.uebernehmen_button = tk.Button(frame, text="übernehmen", command=self.wahrscheinlichkeitswerte_uebernehmen_button_pressed)
        self.uebernehmen_button.grid(row=6, column=0, columnspan=rechts+1)

        self.wahrscheinlichkeit_pane.grid(row=7, column=0, columnspan=self.wahrscheinlichkeit_werte.anz_moeglichkeiten + 3, sticky=tk.NSEW)

        tk.Label(frame,text="Die Wahrscheinlichkeitsrechnung befindet sich noch in der Entwicklung, einige Features funktionieren noch nicht und es können Stabilitätsprobleme auftreten",fg="red").grid(row=8,column=0,columnspan=self.wahrscheinlichkeit_werte.anz_moeglichkeiten + 3, sticky=tk.W)

    def createWahrscheinlichkeitsrechnungWidgets(self,frame):
        # Notebook
        self.wahrscheinlichkeit_pane = ttk.Notebook(frame,width=1300,height=550)
        self.wahrscheinlichkeit_pane.grid(row=7, column=0, sticky=tk.NSEW)

        self.baumdiagramm_head_frame = ScrollableFrame(frame, Baumdiagramm_Frame.Baumdiagramm_Frame,self.wahrscheinlichkeit_werte)

        self.wahrscheinlichkeiten_head_frame = ScrollableFrame(frame, Wahrscheinlichkeiten_Frame.Wahrscheinlichkeiten_Frame, self.wahrscheinlichkeit_werte)

        self.updateWahrscheinlichkeitsrechnungWidgets(frame)

        # Notebook
        self.wahrscheinlichkeit_pane.add(self.wahrscheinlichkeiten_head_frame.head_frame, text="Wahrscheinlichkeiten", padding=0)
        self.wahrscheinlichkeit_pane.add(self.baumdiagramm_head_frame.head_frame, text="Baumdiagramm", padding=0)

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
    root.title("Kurvendiskussion - version: 2.6.0 - dev0.1.0")
    root.resizable(0,0)
    app = MainWindow(master=root)
    app.mainloop()
    print("shutting down")
    root.destroy()