import math

class Punkt():
    x = 0
    y = 0
    name = ""

    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name

    def get_koordinaten_array(self):
        return [self.x,self.y]

    def get_koordinaten_einzeln(self):
        return self.x, self.y

    def __str__(self):
        return "("+str(round(self.x,5))+" | "+str(round(self.y,5))+")"


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
        self.funktion = funktion
        self.color = color
        self.color_name = color_name
        self.name = name
        self.neu_funktion(funktion)

    def neu_funktion(self,funktion):
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


class Fläche():
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