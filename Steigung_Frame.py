import tkinter as tk

class Steigung_Frame(tk.Frame):

    __funktion = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.update()

    def update(self, neu_funktion = None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            self.funktion_text = tk.Label(self, text="Steigung comming soon..."+self.__funktion.funktion_user_kurz)
            self.funktion_text.grid(row=0,column=0)
        else:
            self.funktion_text = tk.Label(self, text="Für Tabelle der Steigung Funktion oben eingeben")
            self.funktion_text.grid(row=0, column=0)