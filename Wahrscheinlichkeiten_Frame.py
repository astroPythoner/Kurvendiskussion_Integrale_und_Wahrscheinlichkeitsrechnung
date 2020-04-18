import copy
import tkinter as tk

class Wahrscheinlichkeiten_Frame(tk.Frame):

    wahrscheinlichkeit_werte = None

    def __init__(self, master=None, wahrscheinlichkeit_werte=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.wahrscheinlichkeit_werte = wahrscheinlichkeit_werte
        self.update()

    def update(self):
        self.erg = []
        if self.wahrscheinlichkeit_werte.chancen_gleich:
            chance = eval(self.wahrscheinlichkeit_werte.chancen[0]) ** self.wahrscheinlichkeit_werte.anz_durchgaenge
            print(chance)
            self.go_through_baum_ebene_ergebnis_bekannt(self.wahrscheinlichkeit_werte.anz_durchgaenge,1,self.wahrscheinlichkeit_werte.namen,[],chance)
        elif self.wahrscheinlichkeit_werte.anz_moeglichkeiten ** self.wahrscheinlichkeit_werte.anz_durchgaenge < 650:
            self.go_through_baum_ebene(self.wahrscheinlichkeit_werte.anz_durchgaenge,1,self.wahrscheinlichkeit_werte.namen,self.wahrscheinlichkeit_werte.chancen,[],1)
        self.createWidgets()

    def go_through_baum_ebene_ergebnis_bekannt(self,max_durchgaenge, durchgang, moeglichkeiten_namen, bisher, erg):
        for moeglich in moeglichkeiten_namen:
            new_bisher = []
            for x in bisher:
                new_bisher.append(x)
            new_bisher.append(moeglich)
            if durchgang < max_durchgaenge:
                self.go_through_baum_ebene_ergebnis_bekannt(max_durchgaenge, durchgang + 1, moeglichkeiten_namen, new_bisher, erg)
            else:
                self.erg.append([new_bisher,erg])

    def go_through_baum_ebene(self,max_durchgaenge, durchgang, moeglichkeiten_namen, moeglichkeiten_chancen, bisher, chance_bisher):
        for moeglich in moeglichkeiten_namen:
            new_bisher = []
            for x in bisher:
                new_bisher.append(x)
            new_bisher.append(moeglich)
            new_chance_bisher = chance_bisher * eval(moeglichkeiten_chancen[moeglichkeiten_namen.index(moeglich)])
            if durchgang < max_durchgaenge:
                self.go_through_baum_ebene(max_durchgaenge, durchgang + 1, moeglichkeiten_namen, moeglichkeiten_chancen, new_bisher, new_chance_bisher)
            else:
                self.erg.append([new_bisher,new_chance_bisher])

    def createWidgets(self):
        for widget in self.winfo_children():
            if not isinstance(widget,tk.Frame):
                widget.destroy()

        summe = 0
        tk.Label(self, text="Züge:").grid(row=0, column=0, columnspan = self.wahrscheinlichkeit_werte.anz_durchgaenge, sticky=tk.W)
        tk.Label(self, text="Chance:").grid(row=0, column=self.wahrscheinlichkeit_werte.anz_durchgaenge, sticky=tk.W)
        tk.Label(self, text="Prozent:").grid(row=0, column=self.wahrscheinlichkeit_werte.anz_durchgaenge+1, sticky=tk.W)
        for count1,i in enumerate(self.erg):
            for count2,j in enumerate(i[0]):
                tk.Label(self,text=j).grid(row=count1+2,column=count2,sticky=tk.W)
            tk.Label(self, text=i[1]).grid(row=count1+2, column=len(i[0]),sticky=tk.W)
            tk.Label(self, text=str(i[1]*100)+"%").grid(row=count1+2, column=len(i[0])+1,sticky=tk.W)
            summe += i[1]
        tk.Label(self, text="Summe").grid(row=1, column=0, columnspan=self.wahrscheinlichkeit_werte.anz_durchgaenge, sticky=tk.W)
        tk.Label(self, text=summe).grid(row=1, column=self.wahrscheinlichkeit_werte.anz_durchgaenge, sticky=tk.W)
        tk.Label(self, text=str(summe)+"%").grid(row=1, column=self.wahrscheinlichkeit_werte.anz_durchgaenge + 1, sticky=tk.W)
        tk.Label(self, text=str(len(self.erg))+" Zeilen geladen").grid(row=0, column=self.wahrscheinlichkeit_werte.anz_durchgaenge + 2, sticky=tk.W)