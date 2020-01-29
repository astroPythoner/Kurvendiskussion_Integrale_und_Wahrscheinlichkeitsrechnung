from random import randint,choice,randrange,uniform,random
from Funktion import Funktion, polynom_to_str, vorzeichen_str
import tkinter as tk


def fakultaet(n):
    if n == 0:
        return 1
    erg = 1
    for x in range(1,n+1):
        erg *= x
    return erg

def alle_kombis_addieren(zahlen,laenge_kombis):
    if laenge_kombis == 1:
        erg = 0
        for i in range(len(zahlen) - laenge_kombis + 1):
            erg += zahlen[i]
    else:
        erg = 0
        for i in range(len(zahlen)-laenge_kombis+1):
            j = alle_kombis_addieren(zahlen[i+1:],laenge_kombis-1)
            erg += zahlen[i]*j
    return erg

class Random_Funtkionen:

    with_polynomfunktion = True
    with_wurzelfunktion = False
    with_exponentialfunktion = False
    with_logarithmischefunktion = False
    with_trigonometrischefunktion = False

    poly_min_nst = -5  # Nullstellen zwischen
    poly_max_nst = 5
    poly_min_expo = 1  # höchster expo zwischen
    poly_max_expo = 4
    poly_ganzzahlige_nst = True # Nullstellen ganzzahlig

    trigo_vorgeg_trigo = "None"  # "None","sin","cos","tan"
    trigo_with_x_streck = True  # Streckungen und Stauchungen
    trigo_with_y_streck = True
    trigo_with_x_versch = True
    trigo_with_y_versch = True

    logar_vorgeg_log = "None"  # "None","ln","log10"
    logar_with_x_versch = True  # Streckung und Stauchung
    logar_with_y_versch = True
    logar_spiegelung = "negativ a" # "negativ a" (Spiegeln durch negative Zahl vor log), "0 < basis < 1" (Spiegeln durch basis zwischen 1 und 0), "None" (keine Spiegelung)

    def get_random_polynomfunktion(self):
        ### Funtion vom Typ ax'3+bx'2+cx+d mit unterschiedlich hohen Exponenten ###
        if self.poly_min_expo == self.poly_max_expo:
            hoechster_expo = self.poly_min_expo
        else:
            hoechster_expo = randint(self.poly_min_expo,self.poly_max_expo)
        if self.poly_ganzzahlige_nst:
            nullstellen = []
            for x in range(hoechster_expo):
                if self.poly_min_nst == self.poly_max_nst:
                    nullstellen.append(self.poly_min_nst)
                else:
                    nullstellen.append(randint(self.poly_min_nst,self.poly_max_nst))
            return_funktion = "x'"+str(hoechster_expo)
            for expo in range(hoechster_expo):
                current_exponent = hoechster_expo-expo-1
                vor_faktor = alle_kombis_addieren(nullstellen,expo+1)
                return_funktion += polynom_to_str(vor_faktor,current_exponent)
        else:
            return_funktion = ""
            for expo in range(hoechster_expo,-1,-1):
                return_funktion += polynom_to_str(randint(-50,50), expo)
        return Funktion(return_funktion)

    def get_random_wurzelfunktion(self):
        ### Funtion vom Typ a(x−b)'(1/2)+c ###
        return Funktion("3*x'(1/3)")

    def get_random_exponentialfunktion(self):
        return Funktion("5'x")

    def get_random_logarithmischefunktion(self):
        ### Funtion vom Typ a*log(x+b,c)+d auch als ln oder 10log ###
        if self.logar_spiegelung != "None":
            if self.logar_spiegelung == "negativ a":
                a = round(uniform(-1, -10), 1)
            else:
                a = round(uniform(1, 10),1)
        else:
            a = 1
        if self.logar_vorgeg_log == "None":
            if self.logar_spiegelung == "0 < basis < 1":
                c = round(random(), 2)
            else:
                c = round(uniform(2, 10), 1)
        if self.trigo_with_x_versch:
            b = round(uniform(-5,5),1)
        else:
            b = 0
        if self.trigo_with_y_versch:
            d = randint(-20,20)
        else:
            d = 0
        funktion = ""
        if a == -1:
            funktion += "-"
        elif a != 1:
            funktion += str(a)+"*"
        if self.logar_vorgeg_log == "ln":
            funktion += "ln(x"
        elif self.logar_vorgeg_log == "log10":
            funktion += "log10(x"
        else:
            funktion += "log(x"
        if b != 0:
            funktion += vorzeichen_str(b)
        if self.logar_vorgeg_log == "None":
            funktion += ","+str(c)
        funktion += ")"
        if d != 0:
            funktion += vorzeichen_str(d)
        return Funktion(funktion)

    def get_random_trigonometrischefunktion(self):
        ### Funtion vom Typ a*sin((x-b)*c)+d mit sin cos oder tan ###
        trigonometrie = choice(["sin","cos","tan"])
        if self.trigo_vorgeg_trigo in ["sin","cos","tan"]:
            trigonometrie = self.trigo_vorgeg_trigo
        if self.trigo_with_y_streck:
            a = round(uniform(-10, 10),1)
            while a == 0:
                a = round(uniform(-10,10),1)
        else:
            a = 1
        if self.trigo_with_x_streck:
            b = randint(-8, 8)
            while b == 0:
                b = randint(-8,8)
        else:
            b = 1
        if self.trigo_with_x_versch:
            c = round(uniform(-5,5),1)
        else:
            c = 0
        if self.trigo_with_y_versch:
            d = randint(-20,20)
        else:
            d = 0
        return_funktion = ""
        if a != 1:
            return_funktion += str(a)+"*"
        return_funktion += trigonometrie+"("
        if b != 1:
            return_funktion += str(b)+"*("
        return_funktion += "x"
        if c != 0:
            return_funktion += vorzeichen_str(c)
        if b != 1:
            return_funktion += ")"
        return_funktion += ")"
        if d != 0:
            return_funktion += vorzeichen_str(d)
        return Funktion(return_funktion)

    def get_random_funktion(self):
        moegliche_funktionstypen = []
        if self.with_polynomfunktion:
            moegliche_funktionstypen.append(self.get_random_polynomfunktion)
        if self.with_wurzelfunktion:
            moegliche_funktionstypen.append(self.get_random_wurzelfunktion)
        if self.with_exponentialfunktion:
            moegliche_funktionstypen.append(self.get_random_exponentialfunktion)
        if self.with_logarithmischefunktion:
            moegliche_funktionstypen.append(self.get_random_logarithmischefunktion)
        if self.with_trigonometrischefunktion:
            moegliche_funktionstypen.append(self.get_random_trigonometrischefunktion)
        if len(moegliche_funktionstypen) > 0:
            return choice(moegliche_funktionstypen)()
        else:
            return None


class Remote_Settings(tk.Toplevel):

    def __init__(self, parent, random_funktionen):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.ran_fun = random_funktionen

        self.title("Zufallsfunktion einstellen")
        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=7, pady=7)
        self.buttonbox()
        self.grab_set()

        self.initial_focus = self
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        self.with_poly = tk.BooleanVar()
        self.with_poly.set(self.ran_fun.with_polynomfunktion)
        tk.Checkbutton(master,text="Polynomfunktion",variable=self.with_poly,onvalue=True,offvalue=False).grid(row=0,column=0, sticky=tk.W)
        self.ganze_nst = tk.BooleanVar()
        self.ganze_nst.set(self.ran_fun.poly_ganzzahlige_nst)
        tk.Checkbutton(master, text="Ganzzahlige Nullstellen zwischen:", variable=self.ganze_nst, onvalue=True, offvalue=False).grid(row=1, column=1, sticky=tk.W)
        self.min_nst = tk.IntVar()
        self.min_nst.set(self.ran_fun.poly_min_nst)
        tk.Scale(master, variable=self.min_nst, from_=-50, to=50, orient=tk.HORIZONTAL).grid(row=1, column=2, sticky=tk.W)
        self.max_nst = tk.IntVar()
        self.max_nst.set(self.ran_fun.poly_max_nst)
        tk.Scale(master, variable=self.max_nst, from_=-50, to=50, orient=tk.HORIZONTAL).grid(row=1, column=3, sticky=tk.W)
        tk.Label(master, text="Hoechster Exponent zwischen:").grid(row=2, column=1, sticky=tk.W)
        self.min_expo = tk.IntVar()
        self.min_expo.set(self.ran_fun.poly_min_expo)
        tk.Scale(master, variable=self.min_expo, from_=1, to=5, orient=tk.HORIZONTAL).grid(row=2, column=2, sticky=tk.W)
        self.max_expo = tk.IntVar()
        self.max_expo.set(self.ran_fun.poly_max_expo)
        tk.Scale(master, variable=self.max_expo, from_=1, to=5, orient=tk.HORIZONTAL).grid(row=2, column=3, sticky=tk.W)
        self.with_wurz = tk.BooleanVar()
        self.with_wurz.set(self.ran_fun.with_wurzelfunktion)
        tk.Checkbutton(master, text="Wurzelfunktion", variable=self.with_wurz, onvalue=True, offvalue=False).grid(row=5, column=0, sticky=tk.W)
        self.with_expon = tk.BooleanVar()
        self.with_expon.set(self.ran_fun.with_exponentialfunktion)
        tk.Checkbutton(master, text="Exponentialfunktion", variable=self.with_expon, onvalue=True, offvalue=False).grid(row=10, column=0, sticky=tk.W)
        self.with_log = tk.BooleanVar()
        self.with_log.set(self.ran_fun.with_logarithmischefunktion)
        tk.Checkbutton(master, text="Logarithmische Funktion", variable=self.with_log, onvalue=True, offvalue=False).grid(row=15, column=0, sticky=tk.W)
        self.with_trig = tk.BooleanVar()
        self.vorgeg_log = tk.StringVar()
        self.vorgeg_log.set(self.ran_fun.logar_vorgeg_log)
        tk.Radiobutton(master, text="ln", variable=self.vorgeg_log, value="ln").grid(row=16, column=1, sticky=tk.W)
        tk.Radiobutton(master, text="log10", variable=self.vorgeg_log, value="log10").grid(row=16, column=2, sticky=tk.W)
        tk.Radiobutton(master, text="log", variable=self.vorgeg_log, value="None").grid(row=16, column=3, sticky=tk.W)
        self.log_spiegelung = tk.StringVar()
        self.log_spiegelung.set(self.ran_fun.logar_spiegelung)
        tk.Radiobutton(master, text="keine Spiegelung", variable=self.log_spiegelung, value="None").grid(row=17, column=1, sticky=tk.W)
        tk.Radiobutton(master, text="negativer Vorfaktor", variable=self.log_spiegelung, value="negativ a").grid(row=17, column=2, sticky=tk.W)
        tk.Radiobutton(master, text="Basis < 0", variable=self.log_spiegelung, value="0 < basis < 1").grid(row=17, column=3, sticky=tk.W)
        self.log_x_versch = tk.BooleanVar()
        self.log_x_versch.set(self.ran_fun.logar_with_x_versch)
        tk.Checkbutton(master, text="X-Verschiebung", variable=self.log_x_versch, onvalue=True, offvalue=False).grid(row=18, column=1, sticky=tk.W, columnspan=2)
        self.log_y_versch = tk.BooleanVar()
        self.log_y_versch.set(self.ran_fun.logar_with_y_versch)
        tk.Checkbutton(master, text="Y-Verschiebung", variable=self.log_y_versch, onvalue=True, offvalue=False).grid(row=18, column=3, sticky=tk.W, columnspan=2)
        self.with_trig.set(self.ran_fun.with_trigonometrischefunktion)
        tk.Checkbutton(master, text="Trigonometrische Funktion", variable=self.with_trig, onvalue=True, offvalue=False).grid(row=20, column=0, sticky=tk.W)
        self.vorgeg_trigo = tk.StringVar()
        self.vorgeg_trigo.set(self.ran_fun.trigo_vorgeg_trigo)
        tk.Radiobutton(master, text="sin", variable=self.vorgeg_trigo, value="sin").grid(row=21, column=1, sticky=tk.W)
        tk.Radiobutton(master, text="cos", variable=self.vorgeg_trigo, value="cos").grid(row=21, column=2, sticky=tk.W)
        tk.Radiobutton(master, text="tan", variable=self.vorgeg_trigo, value="tan").grid(row=21, column=3, sticky=tk.W)
        tk.Radiobutton(master, text="zufaellig", variable=self.vorgeg_trigo, value="None").grid(row=21, column=4, sticky=tk.W)
        self.x_streck = tk.BooleanVar()
        self.x_streck.set(self.ran_fun.trigo_with_x_streck)
        tk.Checkbutton(master, text="X-Streckung", variable=self.x_streck, onvalue=True, offvalue=False).grid(row=22, column=1, sticky=tk.W, columnspan=2)
        self.y_streck = tk.BooleanVar()
        self.y_streck.set(self.ran_fun.trigo_with_y_streck)
        tk.Checkbutton(master, text="Y-Streckung", variable=self.y_streck, onvalue=True, offvalue=False).grid(row=22, column=3, sticky=tk.W, columnspan=2)
        self.x_versch = tk.BooleanVar()
        self.x_versch.set(self.ran_fun.trigo_with_x_versch)
        tk.Checkbutton(master, text="X-Verschiebung", variable=self.x_versch, onvalue=True, offvalue=False).grid(row=23, column=1, sticky=tk.W, columnspan=2)
        self.y_versch = tk.BooleanVar()
        self.y_versch.set(self.ran_fun.trigo_with_y_versch)
        tk.Checkbutton(master, text="Y-Verschiebung", variable=self.y_versch, onvalue=True, offvalue=False).grid(row=23, column=3, sticky=tk.W, columnspan=2)

    def buttonbox(self):
        box = tk.Frame(self)

        fertig = tk.Button(box, text="fertig", command=self.react)
        fertig.pack(side=tk.LEFT, padx=7, pady=7)

        box.pack()

    def react(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def apply(self):
        self.ran_fun.with_polynomfunktion = self.with_poly.get()
        self.ran_fun.poly_ganzzahlige_nst = self.ganze_nst.get()
        self.ran_fun.poly_min_nst = self.min_nst.get()
        self.ran_fun.poly_max_nst = self.max_nst.get()
        self.ran_fun.poly_min_expo = self.min_expo.get()
        self.ran_fun.poly_max_expo = self.max_expo.get()
        self.ran_fun.with_polynomfunktion = self.with_poly.get()
        self.ran_fun.with_polynomfunktion = self.with_poly.get()
        self.ran_fun.with_wurzelfunktion = self.with_wurz.get()
        self.ran_fun.with_exponentialfunktion = self.with_expon.get()
        self.ran_fun.with_logarithmischefunktion = self.with_log.get()
        self.ran_fun.logar_vorgeg_log = self.vorgeg_log.get()
        self.ran_fun.logar_with_x_versch = self.log_x_versch.get()
        self.ran_fun.logar_with_y_versch = self.log_y_versch.get()
        self.ran_fun.logar_spiegelung = self.log_spiegelung.get()
        self.ran_fun.with_trigonometrischefunktion = self.with_trig.get()
        self.ran_fun.trigo_with_x_streck = self.x_streck.get()
        self.ran_fun.trigo_with_y_streck = self.y_streck.get()
        self.ran_fun.trigo_with_x_versch = self.x_versch.get()
        self.ran_fun.trigo_with_y_versch = self.y_versch.get()