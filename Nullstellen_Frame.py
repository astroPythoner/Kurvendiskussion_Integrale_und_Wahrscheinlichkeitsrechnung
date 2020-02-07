from Grundklassen import Punkt
from Funktion import Funktion, polynom_to_str, vorzeichen_str

import tkinter as tk
import math
try:
    import sympy
except Exception:
    pass

def nullstellen_berechnen(funktion, row, frame, num_nullstellen_bisher=0):
    tk.Label(frame, text="0 = " + funktion.funktion_user_kurz).grid(row=row, column=1)
    punkte = []
    if not "x" in funktion.funktion_user_x_ersetztbar:
        if eval(funktion.funktion_computer_readable) == 0:
            tk.Label(frame, text="Ist immer null -> unendlich viele Nullstellen").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
        else:
            tk.Label(frame, text="Ist nie null -> keine Nullstelle").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
        row = row + 1
    elif funktion.is_polynomfunktion:
        exponenten = funktion.exponenten_array
        nur_expos = funktion.nur_exponenten
        nur_basen = funktion.nur_basen
        needs_polynomdivision = False
        # x=0 (0=mx'b -> x=0)
        if len(exponenten) == 1:
            if eval(funktion.nur_basen[0]) != 1:
                tk.Label(frame, text="| /(" + nur_basen[0] + ")").grid(row=row, column=2, sticky=tk.W)
                tk.Label(frame, text="0 = x'" + nur_expos[0]).grid(row=row + 1, column=1)
                row += 1
            if eval(funktion.nur_exponenten[0]) != 1:
                tk.Label(frame, text="| √").grid(row=row, column=2)
                tk.Label(frame, text=nur_expos[0] + "√0 = x").grid(row=row + 1, column=1)
                if eval(funktion.funktion_to_computer_readable(nur_expos[0])) <= 0:
                    tk.Label(frame, text="nicht definiert = x").grid(row=row + 2, column=1)
                    tk.Label(frame, text="Keine Nullstelle").grid(row=row + 3, column=0, sticky=tk.W)
                else:
                    punkte.append(Punkt(0, 0, "Nst"))
                    tk.Label(frame, text="Nst = " + str(punkte[0])).grid(row=row + 2, column=0, sticky=tk.W)
            else:
                punkte.append(Punkt(0, 0, "Nst"))
                tk.Label(frame, text="Nst = " + str(punkte[0])).grid(row=row + 2, column=0, sticky=tk.W)
            row = row + 3
        # wurzel ziehen (0=mx'b+n -> -n/m=x'b -> x=b√(-n/m))
        elif len(exponenten) == 2 and '0' in nur_expos:
            if nur_expos[0] == "0":
                n = nur_basen[0]
                m = nur_basen[1]
                b = eval(funktion.funktion_to_computer_readable(nur_expos[1]))
            else:
                n = nur_basen[1]
                m = nur_basen[0]
                b = eval(funktion.funktion_to_computer_readable(nur_expos[0]))
            minus_n = eval(funktion.funktion_to_computer_readable("-(" + n + ")"))
            tk.Label(frame, text="| " + str(minus_n)).grid(row=row, column=2, sticky=tk.W)
            tk.Label(frame, text=str(minus_n) + " = " + m + "x'" + str(b)).grid(row=row + 1, column=1)
            n_durch_m = eval(funktion.funktion_to_computer_readable("-(" + n + ")"))
            if funktion.funktion_user_kurz[0] != "x":
                tk.Label(frame, text="| /(" + m + ")").grid(row=row + 1, column=2, sticky=tk.W)
                n_durch_m = eval(funktion.funktion_to_computer_readable("-(" + n + ")/(" + (m) + ")"))
            tk.Label(frame, text=str(n_durch_m) + " = x'" + str(b)).grid(row=row + 2, column=1)
            doppel_erg_durch_wurzel = False
            if b != 1:
                tk.Label(frame, text="| √").grid(row=row + 2, column=2)
                tk.Label(frame, text=str(b) + "√(" + str(n_durch_m) + ") = x").grid(row=row + 3, column=1)
                if n_durch_m < 0 and b % 2 == 0:
                    erg = None
                else:
                    if b%2 == 0:
                        doppel_erg_durch_wurzel = True
                    b = b / 1.0
                    erg = n_durch_m ** (1 / b)
            else:
                erg = n_durch_m
            if erg != None and not isinstance(erg, complex):
                if doppel_erg_durch_wurzel:
                    punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+1)))
                    punkte.append(Punkt(-erg, 0, "Nst"+str(num_nullstellen_bisher+2)))
                    tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+1)+" = " + str(punkte[0])).grid(row=row + 4, column=0, sticky=tk.W)
                    tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+2)+" = " + str(punkte[1])).grid(row=row + 5, column=0, sticky=tk.W)
                else:
                    punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+1)))
                    tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+1)+" = " + str(punkte[0])).grid(row=row + 4, column=0, sticky=tk.W)
            else:
                tk.Label(frame, text="nicht definiert = x").grid(row=row + 4, column=1)
                tk.Label(frame, text="Keine Nullstelle").grid(row=row + 5, column=0)
            row = row + 5
        # x ausklammern (0=mx'b+nx'c -> 0=x'c*(mx'(b-c)+n) -> SVN)
        elif len(exponenten) == 2:
            b = max(nur_expos)
            c = min(nur_expos)
            m = nur_basen[nur_expos.index(b)]
            n = nur_basen[nur_expos.index(c)]
            b_minus_c = eval(funktion.funktion_to_computer_readable("("+str(b)+")-(" + str(c) + ")"))
            tk.Label(frame, text="x'"+c+" ausklammern").grid(row=row + 1, column=1)
            tk.Label(frame, text="0 = (x'"+str(c)+") * ("+str(m)+"x'"+str(b_minus_c)+" + "+str(n)+")").grid(row=row + 2, column=1)
            tk.Label(frame, text="Satz vom Nullprodukt").grid(row=row + 3, column=1)
            if eval(c) <= 0:
                tk.Label(frame, text="x1 = 0 ist keine Nullstelle").grid(row=row + 4, column=1)
            else:
                tk.Label(frame, text="x1 = 0").grid(row=row + 4, column=1)
                punkte.append(Punkt(0, 0, "Nst"+str(num_nullstellen_bisher+1)))
                tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+1)+" = " + str(punkte[0])).grid(row=row + 5, column=0, sticky=tk.W)
            tk.Label(frame, text="x2 = "+str(m)+"x'"+str(b_minus_c)+" + "+str(n)).grid(row=row+6, column=1)
            row = row+6
            minus_n = eval(funktion.funktion_to_computer_readable("-(" + n + ")"))
            tk.Label(frame, text="| " + str(minus_n)).grid(row=row, column=2, sticky=tk.W)
            tk.Label(frame, text=str(minus_n) + " = " + str(m) + "x'" + str(b_minus_c)).grid(row=row + 1, column=1)
            tk.Label(frame, text="| /(" + m + ")").grid(row=row + 1, column=2, sticky=tk.W)
            n_durch_m = eval(funktion.funktion_to_computer_readable("(" + str(minus_n) + ")/(" + str(m) + ")"))
            tk.Label(frame, text=str(n_durch_m) + " = x'" + str(b_minus_c)).grid(row=row + 2, column=1)
            doppel_erg_durch_wurzel = False
            if b_minus_c != 1:
                tk.Label(frame, text="| √").grid(row=row + 2, column=2)
                tk.Label(frame, text=str(b_minus_c) + "√(" + str(n_durch_m) + ") = x").grid(row=row + 3, column=1)
                if n_durch_m < 0 and b_minus_c % 2 == 0:
                    erg = None
                else:
                    if b_minus_c % 2 == 0:
                        doppel_erg_durch_wurzel = True
                    b_minus_c = b_minus_c / 1.0
                    erg = n_durch_m ** (1 / b_minus_c)
            else:
                erg = n_durch_m
            if erg != None and not isinstance(erg, complex):
                if doppel_erg_durch_wurzel:
                    punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+2)))
                    punkte.append(Punkt(-erg, 0, "Nst"+str(num_nullstellen_bisher+3)))
                    tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+2)+" = " + str(punkte[1])).grid(row=row + 4, column=0, sticky=tk.W)
                    tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+3)+" = " + str(punkte[2])).grid(row=row + 5, column=0, sticky=tk.W)
                else:
                    punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+2)))
                    tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+2)+" = " + str(punkte[1])).grid(row=row + 4, column=0, sticky=tk.W)
            else:
                tk.Label(frame, text="nicht definiert = x").grid(row=row + 4, column=1)
                tk.Label(frame, text="Keine weitere Nullstelle").grid(row=row + 5, column=0)
            row = row + 5
        # Mitternachtsformel
        elif len(exponenten) == 3 and "0" in nur_expos and "1" in nur_expos and "2" in nur_expos:
                a = eval(nur_basen[nur_expos.index("2")])
                b = eval(nur_basen[nur_expos.index("1")])
                c = eval(nur_basen[nur_expos.index("0")])
                tk.Label(frame, text="Mitternachtsfomel nach (-b±√(b'2-4ac))/2a)  a = "+str(a)+",  b = "+str(b)+",  c = "+str(c)).grid(row=row+1, column=1)
                diskriminante = b**2-4*a*c
                if diskriminante < 0:
                    tk.Label(frame, text="negative Wurzel -> Keine Nullstelle").grid(row=row + 2, column=1)
                else:
                    erg = (-b+(diskriminante**(1/2)))/(2*a)
                    if diskriminante == 0:
                        punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+1)))
                        tk.Label(frame, text="x = "+str(erg)).grid(row=row + 2, column=1)
                        tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+1)+" = " + str(punkte[0])).grid(row=row + 3, column=0, sticky=tk.W)
                    else:
                        erg2 = (-b - (diskriminante ** (1 / 2))) / (2 * a)
                        punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+1)))
                        punkte.append(Punkt(erg2, 0, "Nst"+str(num_nullstellen_bisher+2)))
                        tk.Label(frame, text="x1 = "+str(erg)+"  x2 = "+str(erg2)).grid(row=row + 2, column=1)
                        tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+1)+" = " + str(punkte[0])).grid(row=row + 3, column=0, sticky=tk.W)
                        tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+2)+" = " + str(punkte[1])).grid(row=row + 4, column=0, sticky=tk.W)
                row = row+4
        # entweder noch x ausklammern oder direkt Polynomndivision
        else:
            smallest_expo_fuer_ausklammern = eval(nur_expos[0])
            for exponent in nur_expos:
                if int(eval(exponent)) != eval(exponent) or eval(exponent) <= 0:
                    needs_polynomdivision = True
                elif smallest_expo_fuer_ausklammern > eval(exponent):
                    smallest_expo_fuer_ausklammern = eval(exponent)
            # ausklammern
            if not needs_polynomdivision:
                tk.Label(frame, text=polynom_to_str(1,smallest_expo_fuer_ausklammern)+" ausklammern").grid(row=row + 1, column=1)
                funktion_ausgeklammert = ""
                for exponent in exponenten:
                    funktion_ausgeklammert += polynom_to_str(exponent[0],eval(exponent[1])-smallest_expo_fuer_ausklammern)
                restliche_funktion = Funktion(funktion_ausgeklammert)
                tk.Label(frame, text=polynom_to_str(1,smallest_expo_fuer_ausklammern)+" * ("+funktion_ausgeklammert+")").grid(row=row + 2, column=1)
                tk.Label(frame, text="Satz vom Nullprodukt x = 0, restliche Funktion: "+restliche_funktion.funktion_user_kurz).grid(row=row + 3, column=1)
                punkte.append(Punkt(0, 0, "Nst" + str(num_nullstellen_bisher + 1)))
                tk.Label(frame, text="Nst" + str(num_nullstellen_bisher + 1) + " = (0|0)").grid(row=row + 4, column=0, sticky=tk.W)
                weitere_punkte, row2 = nullstellen_berechnen(restliche_funktion, row+5, frame, num_nullstellen_bisher + 1)
                row = row2
                for punkt in weitere_punkte:
                    punkte.append(punkt)
            # Polynomdivision
            else:
                tk.Label(frame, text="Polynomdivision").grid(row=row + 1, column=1)
                tk.Label(frame, text="Ausgeschreibene polynomfunktion: "+funktion.funktion_polynom_aufgefuellt_x_ersetzbar).grid(row=row + 2, column=1)
                geratene_nullstelle = None
                epsilon = 0.001
                x = 0
                try:
                    if -epsilon <= eval(funktion.funktion_polynom_aufgefuellt_computer_readable) <= epsilon:
                        geratene_nullstelle = 0
                except:
                    pass
                if geratene_nullstelle == None:
                    for x in range(-100, 100):
                        try:
                            if -epsilon <= eval(funktion.funktion_polynom_aufgefuellt_computer_readable) <= epsilon:
                                geratene_nullstelle = x
                        except:
                            pass
                if geratene_nullstelle == None:
                    x = -100
                    while x <= 100:
                        try:
                            if -epsilon <= eval(funktion.funktion_polynom_aufgefuellt_computer_readable) <= epsilon:
                                geratene_nullstelle = x
                        except:
                            pass
                        x += 0.05
                        x = round(x,2)
                if geratene_nullstelle == None:
                    for x in funktion.nur_basen:
                        try:
                            x = eval(funktion.funktion_to_computer_readable(funktion.funktion_verschoenern(x)))
                            if -epsilon <= eval(funktion.funktion_polynom_aufgefuellt_computer_readable) <= epsilon:
                                geratene_nullstelle = x
                        except:
                            pass
                        try:
                            x = -x
                            if -epsilon <= eval(funktion.funktion_polynom_aufgefuellt_computer_readable) <= epsilon:
                                geratene_nullstelle = x
                        except:
                            pass
                if geratene_nullstelle == None:
                    tk.Label(frame, text="geratene Nullstelle: keine Nullstelle gefunden").grid(row=row + 3, column=1)
                else:
                    tk.Label(frame, text="geratene Nullstelle: x = " + str(geratene_nullstelle)+" -> ").grid(row=row + 3, column=1)
                    row = row+3
                    num_expos = 0
                    uebriger_funktionsterm = ""
                    # polynomdivision
                    for expo_und_basis in funktion.exponenten_aufgefuellt_array:
                        expo_teil = expo_und_basis[0] + "*x'" + expo_und_basis[1]
                        expo_mit_x = "*x'" + expo_und_basis[1]
                        basis = eval(expo_und_basis[0])
                        tk.Label(frame, text=expo_teil).grid(row=row, column=num_expos*2+3)
                        if num_expos == 0:
                            letzte_basis = eval(expo_und_basis[0])
                            tk.Label(frame, text=expo_teil).grid(row=row+1, column=3)
                            tk.Label(frame, text=")").grid(row=row+1, column=6)
                            tk.Label(frame, text="-(").grid(row=row+1, column=2)
                            tk.Label(frame, text=vorzeichen_str(letzte_basis) + expo_mit_x).grid(row=row + 2, column=5)
                        elif num_expos == 1:
                            letzte_basis = letzte_basis* (-geratene_nullstelle)
                            tk.Label(frame, text=vorzeichen_str(letzte_basis)+expo_mit_x).grid(row=row+1, column=5)
                            letzte_basis = basis-letzte_basis
                            tk.Label(frame, text=vorzeichen_str(letzte_basis)+expo_mit_x).grid(row=row+2, column=5)
                            tk.Label(frame, text=vorzeichen_str(letzte_basis)+expo_mit_x).grid(row=row+3, column=5)
                        elif num_expos > 1:
                            tk.Label(frame, text=expo_teil).grid(row=row+(num_expos-1)*2, column=num_expos*2+3)
                            letzte_basis = letzte_basis* (-geratene_nullstelle)
                            tk.Label(frame, text=vorzeichen_str(letzte_basis)+expo_mit_x).grid(row=row+(num_expos-1)*2+1, column=num_expos*2+3)
                            if num_expos == len(funktion.exponenten_aufgefuellt_array)-1:
                                tk.Label(frame, text="+0").grid(row=row+(num_expos-1)*2+2, column=num_expos*2+3)
                            else:
                                letzte_basis = basis - letzte_basis
                                tk.Label(frame, text=vorzeichen_str(letzte_basis)+expo_mit_x).grid(row=row+(num_expos-1)*2+2, column=num_expos*2+3)
                                tk.Label(frame, text=vorzeichen_str(letzte_basis)+expo_mit_x).grid(row=row+(num_expos-1)*2+3, column=num_expos*2+3)
                                if num_expos == len(funktion.exponenten_aufgefuellt_array)-2:
                                    tk.Label(frame, text="0").grid(row=row+(num_expos-1)*2+4, column=num_expos*2+3)
                            tk.Label(frame, text="-(").grid(row=row+1+(num_expos-1)*2, column=num_expos*2)
                            tk.Label(frame, text=")").grid(row=row+1+(num_expos-1)*2, column=num_expos*2+4)
                        # Endfunktion erweitern
                        if num_expos != len(funktion.exponenten_aufgefuellt_array)-1:
                            exponent_fuer_uebrige_funktion = eval(expo_und_basis[1]) - 1
                            tk.Label(frame, text=vorzeichen_str(letzte_basis) + "*x'" + str(exponent_fuer_uebrige_funktion)).grid(row=row, column=len(funktion.exponenten_aufgefuellt_array) * 2 + num_expos + 4)
                            uebriger_funktionsterm += polynom_to_str(letzte_basis,exponent_fuer_uebrige_funktion)
                        num_expos += 1
                    tk.Label(frame, text= " / (x"+vorzeichen_str(geratene_nullstelle*-1)+") = ").grid(row=row, column=num_expos*2+3)
                    row = row+(len(funktion.exponenten_aufgefuellt_array))*2+4
                    punkte.append(Punkt(geratene_nullstelle,0,"Nst"+str(num_nullstellen_bisher+1)))
                    tk.Label(frame, text="geratene Nullstelle passt: Nst"+str(num_nullstellen_bisher+1)+" = "+str(punkte[0])).grid(row=row, column=0,sticky=tk.W)
                    uebrige_funktion = Funktion(uebriger_funktionsterm)
                    tk.Label(frame, text="Restliche Funtkion: " + uebrige_funktion.funktion_user_kurz).grid(row=row+1, column=1)
                    weitere_punkte, row2 = nullstellen_berechnen(uebrige_funktion,row+2,frame,num_nullstellen_bisher+1)
                    row=row2
                    for punkt in weitere_punkte:
                        punkte.append(punkt)
    else:
        could_be_solved = True
        try:
            solution = sympy.solveset(funktion.funktion_sympy_readable,sympy.Symbol('x'))
            ergebnisse = []
            if solution.is_empty:
                tk.Label(frame, text="Keine Nullstellen gefunden").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
            for loesung in list(solution):
                loesung = sympy.pretty(loesung)
                if isinstance(loesung,str):
                    try:
                        loesung = float(eval(loesung))
                        if int(loesung) == loesung:
                            loesung = int(loesung)
                    except Exception:
                        pass
                if isinstance(loesung,int) or isinstance(loesung,float):
                    ergebnisse.append(loesung)
                else:
                    could_be_solved = False
            if could_be_solved:
                for count,erg in enumerate(ergebnisse):
                    punkte.append(Punkt(erg, 0, "Nst" + str(num_nullstellen_bisher + 1 + count)))
                    tk.Label(frame, text="Nst" + str(num_nullstellen_bisher + 1 + count) + " = " + str(punkte[-1])).grid(row=row + 1 + count, column=0, sticky=tk.W)
        except Exception as e:
            print(e)
            could_be_solved = False
        if not could_be_solved:
            tk.Label(frame, text="Nullstellen konnten nicht gefunden werden").grid(row=row+1, column=0,columnspan=2, sticky=tk.W)
        row = row + 1
    return punkte,row


class Nullstellen_Frame(tk.Frame):

    __funktion = None
    punkte = []

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
            tk.Label(self, text="Nullstellen ermittlen durch f(x) = 0:").grid(row=0, column=0, columnspan=2,sticky=tk.W)
            punkte,row = nullstellen_berechnen(self.__funktion,1,self)
            unterschiedliche_x_werte = []
            for count,punkt in enumerate(punkte):
                if punkt.x not in unterschiedliche_x_werte:
                    unterschiedliche_x_werte.append(punkt.x)
                else:
                    del punkte[count]
            self.punkte = sorted(punkte)
        else:
            tk.Label(self, text="Fuer Nullstellenberechnung Funktion oben eingeben").grid(row=0, column=0)


if __name__ == '__main__':
    funk = "+ 1*x**2 - 2*x**1 + 8*x**0 + 40*x**(-1)"
    print(eval(funk.replace("x", "(-2)")))
