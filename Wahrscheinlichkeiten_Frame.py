import copy
import tkinter as tk
try:
    from threading import Thread
except Exception:
    pass

max_zeilen_tabelle = 500

class Wahrscheinlichkeiten_Frame(tk.Frame):

    wahrscheinlichkeit_werte = None

    def __init__(self, master=None, wahrscheinlichkeit_werte=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.wahrscheinlichkeit_werte = wahrscheinlichkeit_werte
        self.update()

    def update(self):
        for widget in self.winfo_children():
            if not isinstance(widget, tk.Frame):
                widget.destroy()
        self.createLoadingWidgets()
        self.tabellen_frame = tk.Frame(self)
        try:
            t = Thread(target=self.createErgebnisTabelle)
            t.start()
        except NameError:
            tk.Label(self.tabellen_frame,text="Installiere Threading um Berechnung im Hintegrund auszuführen und nicht das ganze Programm anzuhalten",fg="red").grid(row=0,column=self.wahrscheinlichkeit_werte.anz_durchgaenge+4)
            self.createErgebnisTabelle()

    def createLoadingWidgets(self):
        # Ladebildschirm erstellen
        tk.Label(self, text="Rechnet: ").grid(row=0, column=0, sticky=tk.E)
        self.loading_label = tk.Label(self, text="0")
        self.loading_label.grid(row=0, column=1, sticky=tk.W)
        tk.Label(self, text=" von "+str(self.wahrscheinlichkeit_werte.anz_moeglichkeiten**self.wahrscheinlichkeit_werte.anz_durchgaenge)).grid(row=0, column=2, sticky=tk.W)

    def createErgebnisTabelle(self):
        # werte zurücksetzten
        self.num_erg = 0
        self.summe = 0
        # eigentliche Tabelle zeichnen
        self.go_through_baum_ebene(1,[],1)
        # sonstiges drumherum zeichnen
        self.add_first_line()
        self.add_line(0, ["Summe"], self.summe, span=self.wahrscheinlichkeit_werte.anz_durchgaenge)
        total = self.wahrscheinlichkeit_werte.anz_moeglichkeiten**self.wahrscheinlichkeit_werte.anz_durchgaenge
        tk.Label(self.tabellen_frame,text=str(min([500,total]))+" von "+str(total)+" Zeilen dargestellt").grid(row=0,column=self.wahrscheinlichkeit_werte.anz_durchgaenge+3)
        # tabelle in hauptframe nehmen
        self.tabellen_frame.grid(row=0,column=0,columnspan=5,sticky=tk.NW)

    def go_through_baum_ebene(self, durchgang, bisher, chance_bisher):
        # Baum durchgehen und alle möglichlkeiten mit ahrscheinlichkeit berechnen
        for moeglich,chance in zip(self.wahrscheinlichkeit_werte.namen, self.wahrscheinlichkeit_werte.chancen):
            new_bisher = []
            for x in bisher:
                new_bisher.append(x)
            new_bisher.append(moeglich)
            new_chance_bisher = chance_bisher * eval(chance)
            if durchgang < self.wahrscheinlichkeit_werte.anz_durchgaenge:
                self.go_through_baum_ebene(durchgang + 1, new_bisher, new_chance_bisher)
            else:
                self.num_erg += 1
                self.summe += new_chance_bisher
                if self.num_erg <= max_zeilen_tabelle:
                    self.add_line(self.num_erg, new_bisher, new_chance_bisher)
                    if self.num_erg == max_zeilen_tabelle:
                        tk.Label(self.tabellen_frame,text="nur erste "+str(max_zeilen_tabelle)+" Zeilen dargestellt").grid(row=self.num_erg+3,column=0,columnspan=self.wahrscheinlichkeit_werte.anz_durchgaenge+2)
                self.loading_label.config(text=str(self.num_erg))

    def add_line(self, row, zuege, chance, span=1):
        # zeile zu tabelle hinzufügen
        for count, j in enumerate(zuege):
            tk.Label(self.tabellen_frame, text=j).grid(row=row + 2, column=count, columnspan=span, sticky=tk.W)
        tk.Label(self.tabellen_frame, text=chance).grid(row=row + 2, column=self.wahrscheinlichkeit_werte.anz_durchgaenge, sticky=tk.W)
        tk.Label(self.tabellen_frame, text=str(chance * 100) + "%").grid(row=row + 2, column =self.wahrscheinlichkeit_werte.anz_durchgaenge + 1, sticky=tk.W)

    def add_first_line(self):
        # überschriftzeile hinzufügen
        tk.Label(self.tabellen_frame, text="Züge:").grid(row=0, column=0, columnspan = self.wahrscheinlichkeit_werte.anz_durchgaenge, sticky=tk.W)
        tk.Label(self.tabellen_frame, text="Chance:").grid(row=0, column=self.wahrscheinlichkeit_werte.anz_durchgaenge, sticky=tk.W)
        tk.Label(self.tabellen_frame, text="Prozent:").grid(row=0, column=self.wahrscheinlichkeit_werte.anz_durchgaenge+1, sticky=tk.W)