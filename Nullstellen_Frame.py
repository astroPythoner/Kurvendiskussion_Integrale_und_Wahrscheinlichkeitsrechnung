from Grundklassen import Punkt, Wiederholender_Punkt
from Funktion import Funktion, polynom_to_str, n_mal_x_plus_m_to_string, vorzeichen_str

import tkinter as tk
import math
try:
    import sympy
except Exception:
    pass

def nullstellen_berechnen(parameter, funktion, row, frame, num_nullstellen_bisher=0, print_nullstellen=True):
    tk.Label(frame, text="0 = " + funktion.funktion_user_kurz).grid(row=row, column=1)
    punkte = []
    if not "x" in funktion.funktion_user_x_ersetztbar:
        if funktion.x_einsetzen(0) == 0:
            tk.Label(frame, text="Ist immer null -> unendlich viele Nullstellen",fg="green4").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
        else:
            tk.Label(frame, text="Ist nie null -> keine Nullstelle",fg="green4").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
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
                    tk.Label(frame, text="Keine Nullstelle",fg="green4").grid(row=row + 3, column=0, sticky=tk.W)
                else:
                    punkte.append(Punkt(0, 0, "Nst"))
                    if print_nullstellen:
                        tk.Label(frame, text="Nst = " + str(punkte[0]),fg="green4").grid(row=row + 2, column=0, sticky=tk.W)
            else:
                punkte.append(Punkt(0, 0, "Nst"))
                if print_nullstellen:
                    tk.Label(frame, text="Nst = " + str(punkte[0]),fg="green4").grid(row=row + 2, column=0, sticky=tk.W)
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
            if eval(m) != 0:
                if funktion.funktion_user_kurz[0] != "x":
                    tk.Label(frame, text="| /(" + m + ")").grid(row=row + 1, column=2, sticky=tk.W)
                    n_durch_m = eval(funktion.funktion_to_computer_readable("-(" + n + ")/(" + m + ")"))
                tk.Label(frame, text=str(n_durch_m) + " = x'" + str(b)).grid(row=row + 2, column=1)
                doppel_erg_durch_wurzel = False
                if b != 1:
                    tk.Label(frame, text="| √").grid(row=row + 2, column=2)
                    tk.Label(frame, text=str(b) + "√(" + str(n_durch_m) + ") = x").grid(row=row + 3, column=1)
                    if n_durch_m < 0 and b % 2 == 0:
                        erg = None
                    else:
                        if b % 2 == 0:
                            doppel_erg_durch_wurzel = True
                        b = b / 1.0
                        erg = n_durch_m ** (1 / b)
                else:
                    erg = n_durch_m
                if erg != None and not isinstance(erg, complex):
                    if doppel_erg_durch_wurzel:
                        punkte.append(Punkt(erg, 0, "Nst" + str(num_nullstellen_bisher + 1)))
                        punkte.append(Punkt(-erg, 0, "Nst" + str(num_nullstellen_bisher + 2)))
                        if print_nullstellen:
                            tk.Label(frame, text="Nst" + str(num_nullstellen_bisher + 1) + " = " + str(punkte[0]),fg="green4").grid(row=row + 4, column=0, sticky=tk.W)
                            tk.Label(frame, text="Nst" + str(num_nullstellen_bisher + 2) + " = " + str(punkte[1]),fg="green4").grid(row=row + 5, column=0, sticky=tk.W)
                    else:
                        punkte.append(Punkt(erg, 0, "Nst" + str(num_nullstellen_bisher + 1)))
                        if print_nullstellen:
                            tk.Label(frame, text="Nst" + str(num_nullstellen_bisher + 1) + " = " + str(punkte[0]),fg="green4").grid(row=row + 4, column=0, sticky=tk.W)
                else:
                    tk.Label(frame, text="nicht definiert = x").grid(row=row + 4, column=1)
                    tk.Label(frame, text="Keine Nullstelle",fg="green4").grid(row=row + 5, column=0)
                row = row + 5
            else:
                tk.Label(frame, text="Keine Nullstelle",fg="green4").grid(row=row + 1, column=0)
        # x ausklammern (0=mx'b+nx'c -> 0=x'c*(mx'(b-c)+n) -> SVN)
        elif len(exponenten) == 2:
            b = max(nur_expos)
            c = min(nur_expos)
            m = nur_basen[nur_expos.index(b)]
            n = nur_basen[nur_expos.index(c)]
            b_minus_c = eval(funktion.funktion_to_computer_readable("("+str(b)+")-(" + str(c) + ")"))
            tk.Label(frame, text="x'"+c+" ausklammern",fg="blue2").grid(row=row + 1, column=1)
            tk.Label(frame, text="0 = (x'"+str(c)+") * ("+str(m)+"x'"+str(b_minus_c)+" + "+str(n)+")").grid(row=row + 2, column=1)
            tk.Label(frame, text="Satz vom Nullprodukt",fg="blue2").grid(row=row + 3, column=1)
            if eval(c) <= 0:
                tk.Label(frame, text="x1 = 0 ist keine Nullstelle",fg="green4").grid(row=row + 4, column=1)
            else:
                tk.Label(frame, text="x1 = 0").grid(row=row + 4, column=1)
                punkte.append(Punkt(0, 0, "Nst"+str(num_nullstellen_bisher+1)))
                if print_nullstellen:
                    tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+1)+" = " + str(punkte[0]),fg="green4").grid(row=row + 5, column=0, sticky=tk.W)
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
                    if print_nullstellen:
                        tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+2)+" = " + str(punkte[1]),fg="green4").grid(row=row + 4, column=0, sticky=tk.W)
                        tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+3)+" = " + str(punkte[2]),fg="green4").grid(row=row + 5, column=0, sticky=tk.W)
                else:
                    punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+2)))
                    if print_nullstellen:
                        tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+2)+" = " + str(punkte[1]),fg="green4").grid(row=row + 4, column=0, sticky=tk.W)
            else:
                tk.Label(frame, text="nicht definiert = x").grid(row=row + 4, column=1)
                tk.Label(frame, text="Keine weitere Nullstelle",fg="green4").grid(row=row + 5, column=0)
            row = row + 5
        # Mitternachtsformel
        elif len(exponenten) == 3 and "0" in nur_expos and "1" in nur_expos and "2" in nur_expos:
                a = eval(nur_basen[nur_expos.index("2")])
                b = eval(nur_basen[nur_expos.index("1")])
                c = eval(nur_basen[nur_expos.index("0")])
                tk.Label(frame, text="Mitternachtsfomel nach (-b±√(b'2-4ac))/2a)  a = "+str(a)+",  b = "+str(b)+",  c = "+str(c),fg="blue2").grid(row=row+1, column=1)
                diskriminante = b**2-4*a*c
                if diskriminante < 0:
                    tk.Label(frame, text="negative Wurzel -> Keine Nullstelle").grid(row=row + 2, column=1)
                else:
                    erg = (-b+(diskriminante**(1/2)))/(2*a)
                    if diskriminante == 0:
                        punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+1)))
                        if print_nullstellen:
                            tk.Label(frame, text="x = "+str(erg)).grid(row=row + 2, column=1)
                            tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+1)+" = " + str(punkte[0]),fg="green4").grid(row=row + 3, column=0, sticky=tk.W)
                    else:
                        erg2 = (-b - (diskriminante ** (1 / 2))) / (2 * a)
                        punkte.append(Punkt(erg, 0, "Nst"+str(num_nullstellen_bisher+1)))
                        punkte.append(Punkt(erg2, 0, "Nst"+str(num_nullstellen_bisher+2)))
                        if print_nullstellen:
                            tk.Label(frame, text="x1 = "+str(erg)+"  x2 = "+str(erg2)).grid(row=row + 2, column=1)
                            tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+1)+" = " + str(punkte[0]),fg="green4").grid(row=row + 3, column=0, sticky=tk.W)
                            tk.Label(frame, text="Nst"+str(num_nullstellen_bisher+2)+" = " + str(punkte[1]),fg="green4").grid(row=row + 4, column=0, sticky=tk.W)
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
                tk.Label(frame, text=polynom_to_str(1,smallest_expo_fuer_ausklammern)+" ausklammern",fg="blue2").grid(row=row + 1, column=1)
                funktion_ausgeklammert = ""
                for exponent in exponenten:
                    funktion_ausgeklammert += polynom_to_str(exponent[0],eval(exponent[1])-smallest_expo_fuer_ausklammern)
                restliche_funktion = Funktion(parameter, funktion_ausgeklammert)
                tk.Label(frame, text=polynom_to_str(1,smallest_expo_fuer_ausklammern)+" * ("+funktion_ausgeklammert+")").grid(row=row + 2, column=1)
                tk.Label(frame, text="Satz vom Nullprodukt x = 0, restliche Funktion: "+restliche_funktion.funktion_user_kurz,fg="blue2").grid(row=row + 3, column=1)
                punkte.append(Punkt(0, 0, "Nst" + str(num_nullstellen_bisher + 1)))
                if print_nullstellen:
                    tk.Label(frame, text="Nst" + str(num_nullstellen_bisher + 1) + " = (0|0)",fg="green4").grid(row=row + 4, column=0, sticky=tk.W)
                weitere_punkte, row2 = nullstellen_berechnen(parameter, restliche_funktion, row + 5, frame, num_nullstellen_bisher + 1, print_nullstellen)
                row = row2
                for punkt in weitere_punkte:
                    punkte.append(punkt)
            # Polynomdivision
            else:
                tk.Label(frame, text="Polynomdivision",fg="blue2").grid(row=row + 1, column=1)
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
                    row=row+3
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
                    if print_nullstellen:
                        tk.Label(frame, text="geratene Nullstelle passt: Nst"+str(num_nullstellen_bisher+1)+" = "+str(punkte[0])).grid(row=row, column=0,sticky=tk.W)
                    uebrige_funktion = Funktion(parameter, uebriger_funktionsterm)
                    tk.Label(frame, text="Restliche Funtkion: " + uebrige_funktion.funktion_user_kurz).grid(row=row+1, column=1)
                    weitere_punkte, row2 = nullstellen_berechnen(parameter, uebrige_funktion, row + 2, frame, num_nullstellen_bisher + 1, print_nullstellen)
                    row=row2
                    for punkt in weitere_punkte:
                        punkte.append(punkt)
    elif funktion.is_trigonometrisch:
        links = 0
        if funktion.trigonometrisch_d != 0:
            links = -funktion.trigonometrisch_d
            tk.Label(frame, text="| "+vorzeichen_str(links)).grid(row=row, column=2)
            tk.Label(frame, text=str(links)+" = " + str(funktion.trigonometrisch_a) + " * "+ funktion.trigonometrische_funktion + "(" + n_mal_x_plus_m_to_string(funktion.trigonometrisch_b, -funktion.trigonometrisch_c) + ")").grid(row=row+1, column=1)
            row = row+1
        if funktion.trigonometrisch_a != 1:
            links = links/funktion.trigonometrisch_a
            tk.Label(frame, text="| /"+str(funktion.trigonometrisch_a)).grid(row=row, column=2)
            tk.Label(frame, text=str(links)+" = " +funktion.trigonometrische_funktion + "(" + n_mal_x_plus_m_to_string(funktion.trigonometrisch_b, -funktion.trigonometrisch_c) + ")").grid(row=row+1, column=1)
            row = row+1
        try:
            links = eval("math.a" + funktion.trigonometrische_funktion + "(" + str(links) + ")")
        except Exception:
            tk.Label(frame, text="keine Nullstelle",fg="green4").grid(row=row+1, column=1)
            return punkte,row+1
        links_merken1 = -links
        tk.Label(frame, text="| a"+funktion.trigonometrische_funktion).grid(row=row, column=2)
        tk.Label(frame, text=str(links) + " = "+n_mal_x_plus_m_to_string(funktion.trigonometrisch_b, -funktion.trigonometrisch_c)).grid(row=row+1, column=1)
        row = row+1
        links_merken2 = links
        if funktion.trigonometrisch_b != 1:
            links = links/funktion.trigonometrisch_b
            links_merken2 = links
            tk.Label(frame, text="| /"+str(funktion.trigonometrisch_b)).grid(row=row, column=2)
            tk.Label(frame, text=str(links)+" = "+"x"+vorzeichen_str(funktion.trigonometrisch_c)).grid(row=row+1, column=1)
            row = row+1
        if funktion.trigonometrisch_c != 0:
            links = links+funktion.trigonometrisch_c
            tk.Label(frame, text="| "+vorzeichen_str(funktion.trigonometrisch_c)).grid(row=row, column=2)
            tk.Label(frame, text=str(links)+" = x").grid(row=row+1, column=1)
            row = row+1
        teiler = funktion.trigonometrisch_b/2
        punkte.append(Wiederholender_Punkt(Funktion(parameter, str(links) + "+(x*pi)/" + str(teiler)), 0, "Nst1"))
        if print_nullstellen:
            tk.Label(frame, text="Nst1 = " + str(punkte[0]),fg="green4").grid(row=row + 1, column=0, sticky=tk.W)
        if funktion.trigonometrische_funktion == "cos":
            tk.Label(frame, text=str(-links_merken2) + " = " + "x" + vorzeichen_str(funktion.trigonometrisch_c)).grid(row=row + 2, column=1)
            row = row + 2
            if funktion.trigonometrisch_c != 0:
                tk.Label(frame, text="| " + vorzeichen_str(funktion.trigonometrisch_c)).grid(row=row, column=2)
                tk.Label(frame, text=str(-links_merken2+funktion.trigonometrisch_c) + " = x").grid(row=row + 1, column=1)
                row = row + 1
            punkte.append(Wiederholender_Punkt(Funktion(parameter, str(-links_merken2 + funktion.trigonometrisch_c) + "+pi/" + str(teiler) + "+(x*pi)/" + str(teiler)), 0, "Nst2"))
        else:
            tk.Label(frame, text=str(links_merken1) + " + pi = " + n_mal_x_plus_m_to_string(funktion.trigonometrisch_b, -funktion.trigonometrisch_c)).grid(row=row + 2, column=1)
            links_merken1 = links_merken1 + math.pi
            row = row+2
            if funktion.trigonometrisch_b != 1:
                links_merken1 = links_merken1/ funktion.trigonometrisch_b
                tk.Label(frame, text="| /" + str(funktion.trigonometrisch_b)).grid(row=row, column=2)
                tk.Label(frame, text=str(links_merken1) + " = " + "x" + vorzeichen_str(funktion.trigonometrisch_c)).grid(row=row + 1, column=1)
                row = row + 1
            if funktion.trigonometrisch_c != 0:
                links_merken1 = links_merken1 + funktion.trigonometrisch_c
                tk.Label(frame, text="| " + vorzeichen_str(funktion.trigonometrisch_c)).grid(row=row, column=2)
                tk.Label(frame, text=str(links_merken1) + " = x").grid(row=row + 1, column=1)
                row = row + 1
            punkte.append(Wiederholender_Punkt(Funktion(parameter, str(links_merken1) + "+(x*pi)/" + str(teiler)), 0, "Nst2"))
        if print_nullstellen:
            tk.Label(frame, text="Nst2 = " + str(punkte[1]),fg="green4").grid(row=row + 1, column=0, sticky=tk.W)
        row = row + 1
    else:
        if not ("sin" in funktion.funktion_user_x_ersetztbar or "cos" in funktion.funktion_user_x_ersetztbar or "tan" in funktion.funktion_user_x_ersetztbar):
            could_be_solved = True
            try:
                solution = sympy.solveset(funktion.funktion_sympy_readable,sympy.Symbol('x'))
                ergebnisse = []
                if solution.is_empty:
                    tk.Label(frame, text="Keine Nullstellen gefunden",fg="green4").grid(row=row + 1, column=0, columnspan=2, sticky=tk.W)
                else:
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
                        if print_nullstellen:
                            tk.Label(frame, text="Nst" + str(num_nullstellen_bisher + 1 + count) + " = " + str(punkte[-1]),fg="green4").grid(row=row + 1 + count, column=0, sticky=tk.W)
            except Exception:
                could_be_solved = False
            if not could_be_solved:
                tk.Label(frame, text="Nullstellen konnten nicht gefunden werden",fg="red").grid(row=row+1, column=0,columnspan=2, sticky=tk.W)
            row = row + 1
        else:
            tk.Label(frame, text="Trigonometrische Funktion kann auch unendlich viele Nullstellen haben",fg="green4").grid(row=row+1, column=0,columnspan=2, sticky=tk.W)
            row = row + 1
    return punkte,row


class Nullstellen_Frame(tk.Frame):

    __funktion = None
    punkte = []

    parameter = None

    def __init__(self, master=None,parameter=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.NSEW)
        self.parameter = parameter
        self.update()

    def update(self, neu_funktion = None, second_funktion=None):
        if neu_funktion is not None:
            self.__funktion = neu_funktion
        self.createWidgets()

    def createWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        if self.__funktion != None:
            tk.Label(self, text="Nullstellen ermittlen durch f(x) = 0:",fg="blue4").grid(row=0, column=0, columnspan=2,sticky=tk.W)
            punkte,row = nullstellen_berechnen(self.parameter,self.__funktion,1,self)
            unterschiedliche_x_werte = []
            for count,punkt in enumerate(punkte):
                if isinstance(punkt,Punkt):
                    if punkt.x not in unterschiedliche_x_werte:
                        unterschiedliche_x_werte.append(punkt.x)
                    else:
                        del punkte[count]
            self.punkte = sorted(punkte)
        else:
            tk.Label(self, text="Fuer Nullstellenberechnung Funktion oben eingeben").grid(row=0, column=0)