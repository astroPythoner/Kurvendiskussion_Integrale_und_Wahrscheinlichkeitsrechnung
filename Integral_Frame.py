from Grundklassen import Flaeche, Punkt, Wiederholender_Punkt
from Funktion import vorzeichen_str

import tkinter as tk
import math

class Integral_Frame(tk.Frame):

    __funktion = None
    stammfunktion = None
    differenz_stammfunktion = None
    nullstellen = None
    einstellungsframe = None
    achte_auf_nullstellen = None
    zwischen_graphen = None

    def __init__(self, master=None, stammfunktion=None, differenz_stammfunktion=None, nullstellen=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.flaechen = [Flaeche(0.9,0.6,"hellgrau","Integral")]
        self.x_start = tk.IntVar()
        self.x_start.set(-1)
        self.last_x_start_wert = -1
        self.x_ende = tk.IntVar()
        self.x_ende.set(1)
        self.last_x_ende_wert = 1
        self.update()
        self.stammfunktion = stammfunktion
        self.differenz_stammfunktion = differenz_stammfunktion
        self.nullstellen = nullstellen
        self.achte_auf_nullstellen = False
        self.zwischen_graphen = False

    def update(self, neu_funktion = None, second_funktion=None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def start_x_changed(self,wert=None):
        if wert != self.last_x_start_wert:
            self.last_x_start_wert = wert
            self.flaechen[0].von_x = self.x_start.get()
            self.createWidgets()
            if self.x_start.get() >= self.x_ende.get():
                self.x_ende.set(self.x_start.get()+1)

    def end_x_changed(self,wert=None):
        if wert != self.last_x_ende_wert:
            self.last_x_ende_wert = wert
            self.flaechen[0].bis_x = self.x_ende.get()
            self.createWidgets()
            if self.x_ende.get() <= self.x_start.get():
                self.x_start.set(self.x_ende.get()-1)

    def achte_nst_changed(self):
        self.achte_auf_nullstellen = not self.achte_auf_nullstellen
        self.createWidgets()

    def zwischen_graphen_changed(self):
        self.zwischen_graphen = not self.zwischen_graphen
        self.createWidgets()

    def integral_berechnen(self):
        if self.zwischen_graphen and len(self.differenz_stammfunktion.funktionen) >= 1:
            stammfunktion = self.differenz_stammfunktion.funktionen[1].funktion
        elif self.zwischen_graphen == False and len(self.stammfunktion.funktionen) >= 1:
            stammfunktion = self.stammfunktion.funktionen[0].funktion
        else:
            tk.Label(self, text="Keine Stammfunktion gefunden").grid(row=2, column=1)
            return
        tk.Label(self, text="Stammfunktion: "+stammfunktion.funktion_user_kurz).grid(row=2, column=1)
        tk.Label(self, text="1. Beide Werte in Stammfunktion einsetzen:").grid(row=3, column=0,sticky=tk.W,columnspan=2)
        erster_wert = stammfunktion.x_einsetzen(self.x_start.get())
        zweiter_wert = stammfunktion.x_einsetzen(self.x_ende.get())
        tk.Label(self, text="F("+str(self.x_start.get())+") = "+str(erster_wert)).grid(row=4, column=1, sticky=tk.W)
        tk.Label(self, text="F("+str(self.x_ende.get())+") = "+str(zweiter_wert)).grid(row=5, column=1, sticky=tk.W)
        if erster_wert == "nicht definiert" or zweiter_wert == "nicht definiert":
            tk.Label(self, text="Kein Ergebnis, da eine nicht definiert Zahl in Ergebnissen").grid(row=6, column=0, sticky=tk.W, columnspan=2)
        elif (self.nullstellen != None and self.zwischen_graphen == False) or (self.differenz_stammfunktion != None and self.zwischen_graphen):
            # nach Nullstellen der Funktion zwischen den beiden Punkten suchen
            nullstellen_dazwischen = []
            if self.zwischen_graphen:
                nst = self.differenz_stammfunktion.punkte
            else:
                nst = self.nullstellen.punkte
            for punkt in nst:
                if isinstance(punkt,Wiederholender_Punkt):
                    wieder_punkte = punkt.get_koordinaten_from_to(self.x_start.get(),self.x_ende.get())
                    for wieder_punkt in wieder_punkte:
                        nullstellen_dazwischen.append(Punkt(wieder_punkt[0],wieder_punkt[1],"nst"))
                else:
                    if self.x_start.get() < punkt.x < self.x_ende.get():
                        nullstellen_dazwischen.append(punkt)
            if len(nullstellen_dazwischen) >= 1 and self.achte_auf_nullstellen:
                tk.Label(self, text="!! ACHTUNG Wenn nicht gefundene Nullstellen zwischen den Punkten liegen werden die Flächen unter dem Graph negativ gesehen und im Ergebnis abgezogen").grid(row=6,column=0,sticky=tk.W,columnspan=2)
                tk.Label(self, text="2. Nullstellen zwischen Werten finden").grid(row=7,column=0,sticky=tk.W,columnspan=2)
                nst_text = "Nulstellen: "
                for punkt in nullstellen_dazwischen:
                    nst_text += str(punkt)+", "
                nst_text = nst_text[:-2]
                tk.Label(self, text=nst_text).grid(row=8, column=1,sticky=tk.W)
                tk.Label(self, text="3. Auch Nullstellen einsetzten").grid(row=9, column=0, sticky=tk.W,columnspan=2)
                werte_nullstellen = []
                for count,punkt in enumerate(nullstellen_dazwischen):
                    wert = stammfunktion.x_einsetzen(punkt.x)
                    werte_nullstellen.append(wert)
                    tk.Label(self, text="F(" + str(punkt.x) + ") = " + str(wert)).grid(row=10+count,column=1,sticky=tk.W)
                row = 10+count
                werte_nullstellen.insert(0,erster_wert)
                werte_nullstellen.insert(len(werte_nullstellen),zweiter_wert)
                if "nicht definiert" in werte_nullstellen:
                    tk.Label(self, text="Ergebnis kann nicht berechnet werden, da eine nicht definiert Zahl in Ergebnissen").grid(row=7, column=0, sticky=tk.W, columnspan=2)
                else:
                    # Differenzen berechnen
                    tk.Label(self, text="3. Differenz zwischen den errechneten Werten finden:").grid(row=row+1, column=0, sticky=tk.W,columnspan=2)
                    ergbnis_teile = []
                    for punkt_num in range(len(werte_nullstellen)-1):
                        erg = abs(werte_nullstellen[punkt_num+1] - werte_nullstellen[punkt_num])
                        ergbnis_teile.append(erg)
                        tk.Label(self, text="| " + " "+ str(werte_nullstellen[punkt_num+1]) + " " + vorzeichen_str(-werte_nullstellen[punkt_num])  + " | = " + str(erg)).grid(row=row+2+punkt_num, column=1, sticky=tk.W)
                    row = row+2+punkt_num
                    tk.Label(self,text="4. Ergebnisse zusammenzählen:").grid(row=row + 1, column=0, sticky=tk.W, columnspan=2)
                    tk.Label(self, text="Fläche = "+str(math.fsum(ergbnis_teile))).grid(row=row+2, column=1, sticky=tk.W)
            else:
                # Differenz berechnen
                tk.Label(self, text="2. Differenz der beiden Werte finden:").grid(row=7, column=0, sticky=tk.W, columnspan=2)
                erg = abs(zweiter_wert - erster_wert)
                tk.Label(self, text="| " + str(zweiter_wert) + " " + vorzeichen_str(-erster_wert) + " | = " + str(erg)).grid(row=7, column=1, sticky=tk.W)

    def createWidgets(self):
        for widget in self.winfo_children():
            if not isinstance(widget,tk.Frame):
                widget.destroy()

        if self.einstellungsframe is None:
            self.einstellungsframe = tk.Frame(self)
            self.x_start_regler = tk.Scale(self.einstellungsframe, from_=-100, to=99, orient=tk.HORIZONTAL, variable=self.x_start)
            self.x_start_regler.config(command=self.start_x_changed)
            self.x_start_regler.grid(row=0, column=0, sticky=tk.NSEW)
            self.x_start_spinbox = tk.Spinbox(self.einstellungsframe, from_=-100, to=99, textvariable=self.x_start)
            self.x_start_spinbox.config(command=self.start_x_changed)
            self.x_start_spinbox.grid(row=0, column=1, sticky=tk.S+tk.W)
            self.x_ende_regler = tk.Scale(self.einstellungsframe, from_=-99, to=100, orient=tk.HORIZONTAL, variable=self.x_ende)
            self.x_ende_regler.config(command=self.end_x_changed)
            self.x_ende_regler.grid(row=1, column=0, sticky=tk.NSEW)
            self.x_ende_spinbox = tk.Spinbox(self.einstellungsframe, from_=-99, to=100, textvariable=self.x_ende)
            self.x_ende_spinbox.config(command=self.end_x_changed)
            self.x_ende_spinbox.grid(row=1, column=1, sticky=tk.S+tk.W)
            self.achte_nst_button = tk.Checkbutton(self.einstellungsframe, text="Nullstellen beachten und Fläche unter x-Achse positiv sehen", command=self.achte_nst_changed)
            self.achte_nst_button.grid(row=2, column=0)
            self.zwichen_grpahen_button = tk.Checkbutton(self.einstellungsframe, text="Fläche zwischen Funktionen berechnen", command=self.zwischen_graphen_changed)
            self.zwichen_grpahen_button.grid(row=3, column=0)
            self.einstellungsframe.columnconfigure(0,minsize=400)
            self.einstellungsframe.grid(row=0, column=0, sticky=tk.W)

        if self.__funktion is not None:
            if self.stammfunktion is None or len(self.stammfunktion.funktionen) == 0 or self.stammfunktion.funktionen[0].funktion is None:
                tk.Label(self, text="Keine Stammfunktion gefunden").grid(row=1, column=0)
            else:
                self.integral_berechnen()
        else:
            tk.Label(self, text="Für Integrale Funktion oben eingeben").grid(row=1, column=0)