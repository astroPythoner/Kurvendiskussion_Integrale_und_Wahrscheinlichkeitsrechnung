import math

class Punkt():
    __slots__ = ('x','y','name')

    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name

    def get_koordinaten_array(self):
        return [self.x,self.y]

    def get_koordinaten_einzeln(self):
        return self.x, self.y

    def __repr__(self):
        return "("+str(round(self.x,5))+" | "+str(round(self.y,5))+")"

    def __cmp__(self, other):
        return self.x > other.x
    def __lt__(self, other):
        return self.x < other.x
    def __gt__(self, other):
        return self.x > other.x


class Wiederholender_Punkt():
    # Punkte vom Aufbau {a*k+b, k ∈ Z}
    # nur ganz Zahlen und nur lineare Funktionen

    __slots__ = ('funktion', 'x','y', 'name','steigend')

    def __init__(self, funktion, y, name):
        self.funktion = funktion
        self.y = y
        self.x = self.funktion.x_einsetzen(0)
        self.name = name
        wert1 = self.funktion.x_einsetzen(0)
        wert2 = self.funktion.x_einsetzen(1)
        if wert1 < wert2:
            self.steigend = True  # steigend
        elif wert1 > wert2:
            self.steigend = False # fallend
        else:
            self.steigend = None  # nicht erlaubt nur lineare Funktionen

    def get__kte_koordinate_array(self,k):
        wert = self.funktion.x_einsetzen(k)
        return [wert, self.y]

    def get_kte_koordinate_einzeln(self,k):
        wert = self.funktion.x_einsetzen(k)
        return wert, self.y

    def get_koordinaten_from_to(self,from_value,to_value):
        einsetzten = 0
        wert = self.funktion.x_einsetzen(einsetzten)
        if wert > from_value and self.steigend or wert < from_value and not self.steigend:
            merken = -1
        elif wert < from_value and self.steigend or wert > from_value and not self.steigend:
            merken = 1
        if wert != from_value:
            while True:
                einsetzten += merken
                if self.funktion.x_einsetzen(einsetzten) == from_value:
                    break
                if wert < from_value and self.funktion.x_einsetzen(einsetzten) > from_value:
                    break
                elif wert > from_value and self.funktion.x_einsetzen(einsetzten) < from_value:
                    break
                else:
                    wert = self.funktion.x_einsetzen(einsetzten)
        k_from = einsetzten
        einsetzten = 0
        wert = self.funktion.x_einsetzen(einsetzten)
        if wert > to_value and self.steigend or wert < to_value and not self.steigend:
            merken = -1
        elif wert < to_value and self.steigend or wert > to_value and not self.steigend:
            merken = 1
        if wert != to_value:
            while True:
                einsetzten += merken
                if self.funktion.x_einsetzen(einsetzten) == to_value:
                    break
                if wert < to_value and self.funktion.x_einsetzen(einsetzten) > to_value:
                    break
                elif wert > to_value and self.funktion.x_einsetzen(einsetzten) < to_value:
                    break
                else:
                    wert = self.funktion.x_einsetzen(einsetzten)
        k_to = einsetzten
        punkte = []
        for k in range(min([k_to,k_from]),max([k_to,k_from])+1):
            wert = self.funktion.x_einsetzen(k)
            if wert > from_value and wert < to_value:
                punkte.append([wert, self.y])
        return punkte

    def get_koordinaten_array(self):
        return [self.x,self.y]

    def get_koordinaten_einzeln(self):
        return self.x, self.y

    def __repr__(self):
        return "{"+self.funktion.funktion_user_kurz.replace("x","k")+", k ∈ Z}"

    def __cmp__(self, other):
        return self.x > other.x
    def __lt__(self, other):
        return self.x < other.x
    def __gt__(self, other):
        return self.x > other.x


class Graph():
    funktion = ""
    color = "red"
    color_name = "rot"
    name = ""
    x_werte = []
    y_werte = []

    # max_x ist maximaler x_wert in positive und negative x_richtung, genauegkeit ist die 'abtastrate' also bei 10 zumbeispiel in zehntel schritten   Tipp: max_x*genauigkeit sollten nicht über 10000 liegen da sonst Berechnungen lange dauern
    max_x = 100
    genauigkeit = 10

    def __init__(self,funktion,color,color_name,name):
        self.color = color
        self.color_name = color_name
        self.name = name
        self.neu_funktion(funktion)

    def neu_funktion(self,funktion):
        self.funktion = funktion
        self.x_werte = []
        for i in range(-(self.max_x * self.genauigkeit), (self.max_x * self.genauigkeit)):
            self.x_werte.append(i / self.genauigkeit)
        self.y_werte = []
        for x in self.x_werte:
            if funktion is not None:
                try:
                    if x < 0:
                        x_str = "(" + str(x) + ")"
                    else:
                        x_str = str(x)
                    funktionswert_an_i = eval(funktion.funktion_computer_readable.replace("x", x_str))
                    if isinstance(funktionswert_an_i, complex):
                        funktionswert_an_i = 0
                except Exception:
                    funktionswert_an_i = 0
            else:
                funktionswert_an_i = 0
            self.y_werte.append(funktionswert_an_i)


class Flaeche():
    face_color = "red"
    edge_color = "red"
    color_name = "rot"
    name = ""
    von_x = -1
    bis_x = 1

    def __init__(self,facecolor,edge_color,color_name,name):
        self.face_color = facecolor
        self.edge_color = edge_color
        self.color_name = color_name
        self.name = name


if __name__ == '__main__':
    from Funktion import Funktion
    punkt = Wiederholender_Punkt(Funktion("2*x"),0,"Nst")
    print(punkt.get_koordinaten_from_to(-10,10))