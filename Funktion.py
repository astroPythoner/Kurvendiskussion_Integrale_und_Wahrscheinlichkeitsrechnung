import math


def vorzeichen_str(wert,mitleerzeichen=False):
    if isinstance(wert,int) or isinstance(wert,float):
        if wert < 0:
            if mitleerzeichen:
                return "- "+str(wert*-1)
            else:
                return str(wert)
        else:
            if mitleerzeichen:
                return "+ " + str(wert)
            else:
                return "+"+str(wert)
    elif isinstance(wert,str):
        if wert[0] in ["+","-","/","*"]:
            if mitleerzeichen:
                if wert[1] != " ":
                    return wert[0]+" "+wert[1:]
                else:
                    return wert
            else:
                return wert
        else:
            if mitleerzeichen:
                return "+ "+wert
            else:
                return "+"+wert

def polynom_to_str(basis,expo):
    # Basis und Exponent in richtige From bringen
    if isinstance(expo,str):
        if expo[0] == "+":
            expo = expo[1:]
        int_expo = eval(expo)
    else:
        int_expo = expo
    if isinstance(basis,str):
        if basis[0] == "+":
            basis = basis[1:]
        int_basis = eval(basis)
    else:
        int_basis = basis
        basis = str(basis)
    # Hier Exponent und Basis zusammenbasteln
    if int_basis == 0:
        return ""
    if int_expo == 0:
        return vorzeichen_str(basis)
    elif int_expo == 1:
        if int_basis == 1:
            return "+x"
        elif int_basis == -1:
            return "-x"
        else:
            return vorzeichen_str(basis+"*x")
    elif int_expo < 0:
        if int_basis == 1:
            return "+x'("+vorzeichen_str(expo)+")"
        elif int_basis == -1:
            return "-x'("+vorzeichen_str(expo)+")"
        else:
            return vorzeichen_str(basis+"*x'("+vorzeichen_str(expo)+")")
    else:
        if int_basis == 1:
            return "+x'"+str(expo)
        elif int_basis == -1:
            return "-x'"+str(expo)
        else:
            if isinstance(expo,str) and not expo.isnumeric():
                return vorzeichen_str(basis + "*x'(" + expo+")")
            elif isinstance(expo,str) and expo.isnumeric() and int_expo<0:
                return vorzeichen_str(basis + "*x'(" + expo+")")
            elif isinstance(expo,str) and expo.isnumeric():
                return vorzeichen_str(basis+"*x'"+expo)
            elif int_expo < 0:
                return vorzeichen_str(basis + "*x'(" + str(int_expo)) + ")"
            else:
                return vorzeichen_str(basis + "*x'" + str(int_expo))

def polynom_array_to_str(array):
    return polynom_to_str(array[0],array[1])

def groesster_teiler(a,b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def bruch_kuerzen(zaehler,teiler):
    if teiler == 0:
        return zaehler,teiler
    ggt = groesster_teiler(zaehler,teiler)
    return int(zaehler/ggt), int(teiler/ggt)

def check_funktionen_gleich(funktion1,funktion2):
    if isinstance(funktion1,Funktion):
        funktion1 = funktion1.funktion_computer_readable
    else:
        funktion1 = Funktion.funktion_to_computer_readable(1,funktion1)
    if isinstance(funktion2,Funktion):
        funktion2 = funktion2.funktion_computer_readable
    else:
        funktion2 = Funktion.funktion_to_computer_readable(1,funktion2)
    if funktion1 == funktion2:
        return True
    for x in range(-30, 30):
        try:
            if eval(funktion1.replace("x","("+str(x)+")")) != eval(funktion2.replace("x","("+str(x)+")")):
                return False
        except Exception:
            return False
    for x in [math.pi, math.pi / 2, math.pi / 3, math.e, math.e/2]:
        try:
            if eval(funktion1.replace("x",str(x))) != eval(funktion2.replace("x",str(x))):
                return False
        except Exception:
            return False
    return True

def get_n_m_from_n_mal_x_plus_m(funktion):
    if isinstance(funktion,str):
        funktion = Funktion(funktion)
    # checks through n(x+m) and return n,m
    if "x" in funktion.funktion_user_x_ersetztbar:
        funktion_array = []
        funktion_array.extend(funktion.funktion_user_x_ersetztbar)
        offene_klammern = 0
        index = funktion_array.index("x") + 1
        m = ""
        while index < len(funktion_array):
            letter = funktion_array[index]
            m += letter
            if letter == "(":
                offene_klammern += 1
            elif letter == ")":
                offene_klammern -= 1
                if offene_klammern < 0:
                    m = m[:-1]
                    break
                if offene_klammern == 0:
                    break
            index += 1
        if m == "":
            m = "0"
        offene_klammern = 0
        index = funktion_array.index("x") - 1
        geklammert = False
        if funktion_array[index] == "(":
            index -= 1
            geklammert = True
        n = ""
        while index >= 0:
            letter = funktion_array[index]
            n += letter
            if letter == ")":
                offene_klammern += 1
            elif letter == "(":
                offene_klammern -= 1
                if offene_klammern < 0:
                    n = n[:-1]
                    break
            index -= 1
        n = n[::-1]
        if n == "":
            n = "1"
        if n == "-":
            n = "-1"
        if n == "+":
            n = "+1"
        if n.endswith("*"):
            n = n[:-1]
        if not geklammert:
            m = "("+m+")/("+n+")"
        # check if n and m are correct
        if "x" in n or "x" in m:
            return False,False
        if not check_funktionen_gleich(funktion,str(eval(n))+"*(x"+vorzeichen_str(eval(m))+")"):
            return False,False
        return n,m
    return False,False

class Funktion():

    funktion_user_kurz = ""
    funktion_user_x_ersetztbar = ""
    funktion_computer_readable = ""
    funktion_sympy_readable = ""

    is_polynomfunktion = False             # Typ: ax'3 + bx'2 + cx + d + ...
    funktion_polynom_x_ersetzbar = ""
    funktion_polynom_computer_readable = ""
    exponenten_array = []
    nur_exponenten = []
    nur_basen = []
    funktion_polynom_aufgefuellt_x_ersetzbar = ""
    funktion_polynom_aufgefuellt_computer_readable = ""
    exponenten_aufgefuellt_array = []
    nur_exponenten_aufgefuellt = []
    nur_basen_aufgefuellt = []

    is_wurzel = False                      # Typ: a(x-b)'(1/2) + d
    funktion_wurzel_x_ersetzbar = ""
    funktion_wurzel_computer_readable = ""
    wurzel_a = 0
    wurzel_b = 0
    wurzel_c = 0

    is_logarithmus = False                 # Typ: a * log(b(x-c), d) + e
    funktion_logarithmus_x_ersetzbar = ""
    funktion_logarithmus_computer_readable = ""
    logarithmus_a = 0
    logarithmus_b = 0
    logarithmus_c = 0
    logarithmus_d = 0
    logarithmus_e = 0

    is_trigonometrisch = False             # Typ: a * sin(b(x-c)) + d
    funktion_trigonometrisch_x_ersetzbar = ""
    funktion_trigonometrisch_computer_readable = ""
    trigonometrische_funktion = "" #sin,cos or tan
    trigonometrisch_a = 0
    trigonometrisch_b = 0
    trigonometrisch_c = 0
    trigonometrisch_d = 0

    is_exponential = False                # Typ: a'x+b'x+c'x
    funktion_exponential_x_ersetzbar = ""
    funktion_exponential_computer_readable = ""

    # Um zu sehen warum Funktionstyp nicht erkannt wurde
    debug_sonstiges = False

    def __init__(self,funktion=None):
        if funktion != None:
            self.set_funktion(funktion)

    def __str__(self):
        if self.is_polynomfunktion:
            return "Polynomfunktion: " + self.funktion_user_kurz
        elif self.is_wurzel:
            return "Wurzelfunktion: " + self.funktion_user_kurz
        elif self.is_logarithmus:
            return "Logarithmusfunktion: " + self.funktion_user_kurz
        elif self.is_trigonometrisch:
            return "Trigonometrische Funktion: " + self.funktion_user_kurz
        elif self.is_exponential:
            return "Exponentialfunktion: " + self.funktion_user_kurz
        else:
            return "Funktion: "+self.funktion_user_kurz

    def add_debug_sonstiges_frame(self,sonstiges_frame):
        self.debug_sonstiges = sonstiges_frame

    def funktion_verschoenern(self,funktion):
        # ganz ausschreiben  (3x -> 3*x)
        funktion = funktion.replace("^", "'")
        funktion = funktion.replace("asin", "arcsin")
        funktion = funktion.replace("acos", "arccos")
        funktion = funktion.replace("atan", "arctan")
        funktion_array = []
        funktion_array.extend(funktion)
        count = 0
        while count < len(funktion_array):
            letter = funktion_array[count]
            letter_davor = None
            if count > 0:
                letter_davor = funktion_array[count-1]
            letter_danach = None
            if count < len(funktion_array)-1:
                letter_danach = funktion_array[count+1]
            if letter == "x":
                if letter_davor != None and letter_davor == " ":
                    del funktion_array[count - 1]
                    count -= 1
                if letter_danach != None and letter_danach == " ":
                    del funktion_array[count + 1]
                if letter_davor != None and (letter_davor.isnumeric() or letter_davor==")" or letter_davor=="i" or letter_davor=="e" or letter_davor == "x"):
                    funktion_array.insert(count, "*")
                    count -= 1
                if letter_danach != None and (letter_danach.isnumeric() or letter_danach == "(" or letter_danach=="p" or letter_danach=="e" or letter_danach == "x" or letter_danach == "s" or letter_danach == "c" or letter_danach == "t" or letter_danach == "a"):
                    funktion_array.insert(count+1, "*")
            elif letter == " ":
                if letter_danach != None and letter_danach == " ":
                    del funktion_array[count+1]
                    count -= 1
            elif letter in ["+","-","*","/","'"]:
                if letter == "*" or letter == "/" or letter == "'":
                    if letter_davor != None and letter_davor == " ":
                        del funktion_array[count-1]
                        count -= 1
                    if letter_danach != None and letter_danach == " ":
                        del funktion_array[count+1]
                else:
                    if letter_davor != None and letter_davor != " ":
                        funktion_array.insert(count, " ")
                        count -= 1
                    if letter_danach != None and letter_danach != " ":
                        funktion_array.insert(count + 1, " ")
            count += 1
        return "".join(i for i in funktion_array)

    def funktion_to_computer_readable(self,funktion):
        funktion = funktion.replace("e","math.e")
        funktion = funktion.replace("pi", "math.pi")
        funktion_array = []
        funktion_array.extend(funktion)
        for count,letter in enumerate(funktion_array):
            if letter == "'" or letter == "":
                funktion_array[count] = "**"
        letter_num = 0
        while letter_num < len(funktion_array):
            if (funktion_array[letter_num:letter_num+3] == ["s","i","n"] or funktion_array[letter_num:letter_num+3] == ["c","o","s"] or funktion_array[letter_num:letter_num+3] == ["t","a","n"]) and (letter_num<=3 or (letter_num>3 and funktion_array[letter_num-3:letter_num] != ["a","r","c"])):
                funktion_array.insert(letter_num,"math.")
                letter_num += 1
            if (funktion_array[letter_num:letter_num+3] == ["s","i","n"] or funktion_array[letter_num:letter_num+3] == ["c","o","s"] or funktion_array[letter_num:letter_num+3] == ["t","a","n"]) and (letter_num>3 and funktion_array[letter_num-3:letter_num] == ["a","r","c"]):
                funktion_array[letter_num - 1] = "a"
                funktion_array[letter_num - 2] = "."
                funktion_array[letter_num - 3] = "math"
            letter_num += 1
        funktion = "".join(i for i in funktion_array)
        funktion = funktion.replace("log", "math.log")
        funktion = funktion.replace("ln", "math.log1p")
        return funktion

    def funktion_to_sympy_readable(self,funktion):
        funktion = funktion.replace("e","e")
        funktion = funktion.replace("pi", "pi")
        funktion_array = []
        funktion_array.extend(funktion)
        for count,letter in enumerate(funktion_array):
            if letter == "'" or letter == "":
                funktion_array[count] = "**"
        funktion = "".join(i for i in funktion_array)
        funktion = funktion.replace("log", "log")
        funktion = funktion.replace("ln", "ln")
        return funktion

    def funktion_to_user_kurz(self,funktion):
        funktion_array = []
        funktion_array.extend(funktion)
        count = 0
        while count < len(funktion_array):
            letter = funktion_array[count]
            letter_davor = None
            if count > 0:
                letter_davor = funktion_array[count-1]
            letter_danach = None
            if count < len(funktion_array)-1:
                letter_danach = funktion_array[count+1]
            if letter == "*":
                if letter_davor != None and (letter_davor.isnumeric()):
                    del funktion_array[count]
                if letter_danach != None and (letter_danach.isnumeric()):
                    del funktion_array[count]
            count+= 1
        return "".join(i for i in funktion_array)

    def __exponenten_zusammenfuehren_und_sortieren(self,exponenten_mit_basis):
        gekuerzte_exponenten = []
        gekuerzte_basen = []
        # ausrechnen
        for count,exponent_mis_basis in enumerate(exponenten_mit_basis):
            gekuerzte_exponenten.append(str(eval(self.funktion_to_computer_readable(self.funktion_verschoenern(exponent_mis_basis[1])))))
            wert = eval(self.funktion_to_computer_readable(self.funktion_verschoenern(exponent_mis_basis[0])))
            if wert > 0:
                gekuerzte_basen.append("+"+str(wert))
            else:
                gekuerzte_basen.append(str(wert))
        # zusammenfuehren
        count1=0
        count2=0
        while count1 < len(gekuerzte_exponenten):
            expo1 = gekuerzte_exponenten[count1]
            while count2 < len(gekuerzte_exponenten):
                expo2 = gekuerzte_exponenten[count2]
                if count1 != count2 and expo1 == expo2:
                    wert = int(gekuerzte_basen[count1])+int(gekuerzte_basen[count2])
                    if wert > 0:
                        gekuerzte_basen[count1] = "+" + str(wert)
                    else:
                        gekuerzte_basen[count1] = str(wert)
                    del gekuerzte_exponenten[count2]
                    del gekuerzte_basen[count2]
                count2 += 1
            count1 += 1
        exponenten_mit_basis = []
        for x in range(len(gekuerzte_exponenten)):
            exponenten_mit_basis.append([gekuerzte_basen[x],gekuerzte_exponenten[x]])
        # sortieren
        switched_something = True
        while switched_something:
            switched_something = False
            for j in range(len(exponenten_mit_basis)-1):
                if eval(exponenten_mit_basis[j+1][1]) > eval(exponenten_mit_basis[j][1]):
                    switched_something = True
                    exponenten_mit_basis[j], exponenten_mit_basis[j + 1] = exponenten_mit_basis[j + 1], exponenten_mit_basis[j]
        return exponenten_mit_basis

    def __sortierte_exponenten_auffuellen(self, exponenten_sortiert_mit_basis):
        return_array = []
        for expo_num in range(len(exponenten_sortiert_mit_basis)-1):
            expo = int(eval(exponenten_sortiert_mit_basis[expo_num][1]))
            return_array.append(exponenten_sortiert_mit_basis[expo_num])
            for x in range(expo-1,int(eval(exponenten_sortiert_mit_basis[expo_num+1][1])),-1):
                return_array.append(["+0",str(x)])
        return_array.append(exponenten_sortiert_mit_basis[-1])
        if eval(exponenten_sortiert_mit_basis[-1][1]) > 0:
            for x in range(int(eval(exponenten_sortiert_mit_basis[-1][1])-1), -1, -1):
                return_array.append(["+0", str(x)])
        switched_something = True
        while switched_something:
            switched_something = False
            for j in range(len(return_array) - 1):
                if eval(return_array[j + 1][1]) > eval(return_array[j][1]):
                    switched_something = True
                    return_array[j], return_array[j + 1] = return_array[j + 1], return_array[j]
        return return_array

    def __set_values_after_set_funktion_polynom(self,funktion):
        exponenten, expo_funktion = self.__check_funktion_polynom_funktion_and_convert(funktion)
        if exponenten == False or exponenten == None:
            self.is_polynomfunktion = False
            if self.debug_sonstiges != False:
                self.debug_sonstiges.add_funktion_not_erkannt_reason("Polynomfunktion",expo_funktion)
            self.funktion_polynom_x_ersetzbar = ""
            self.funktion_polynom_computer_readable = ""
            self.exponenten_array = []
            self.nur_exponenten = []
            self.nur_basen = []
            self.funktion_polynom_aufgefuellt_x_ersetzbar = ""
            self.funktion_polynom_aufgefuellt_computer_readable = ""
            self.exponenten_aufgefuellt_array = []
            self.nur_exponenten_aufgefuellt = []
            self.nur_basen_aufgefuellt = []
        else:
            self.is_polynomfunktion = True
            self.exponenten_array = exponenten
            for exponent in self.exponenten_array:
                self.nur_exponenten.append(exponent[1])
                self.nur_basen.append(exponent[0])
            self.funktion_polynom_x_ersetzbar = self.funktion_verschoenern(expo_funktion)
            self.funktion_polynom_computer_readable = self.funktion_to_computer_readable(self.funktion_polynom_x_ersetzbar)
            self.exponenten_aufgefuellt_array = self.__sortierte_exponenten_auffuellen(exponenten)
            funktion = ""
            for exponent in self.exponenten_aufgefuellt_array:
                self.nur_exponenten_aufgefuellt.append(exponent[1])
                self.nur_basen_aufgefuellt.append(exponent[0])
                if eval(exponent[1]) < 0:
                    funktion += exponent[0] + "*x'(" + exponent[1] + ")"
                else:
                    funktion += exponent[0] + "*x'" + exponent[1]
            self.funktion_polynom_aufgefuellt_x_ersetzbar = self.funktion_verschoenern(funktion)
            self.funktion_polynom_aufgefuellt_computer_readable = self.funktion_to_computer_readable(self.funktion_polynom_x_ersetzbar)

    def __check_funktion_polynom_funktion_and_convert(self,funktion):
        funktion = funktion.replace(" ","")
        if funktion[0] != "+" and funktion[0] != "-":
            funktion = "+"+funktion
        exponenten = []
        if "x" in funktion:
            count = 0
            num_plus_or_minus_since_last_expo = 0
            count_last_plus_or_minus = 0
            klammern_offen = 0
            while count < len(funktion):
                char = funktion[count]
                if char == "(":
                    klammern_offen += 1
                if char == ")":
                    klammern_offen -= 1
                if (char == "+" or char == "-" or count == len(funktion)-1) and klammern_offen == 0:
                    num_plus_or_minus_since_last_expo += 1
                    if num_plus_or_minus_since_last_expo%2==0:
                        try:
                            end = count
                            if count == len(funktion)-1:
                                end = count +1
                            wert = eval(self.funktion_to_computer_readable(funktion[count_last_plus_or_minus:end]))
                            if isinstance(wert,int):
                                if wert >= 0:
                                    exponenten.append(["+"+str(wert), "0"])
                                else:
                                    exponenten.append([str(wert), "0"])
                            else:
                                exponenten.append(["+("+funktion[count_last_plus_or_minus:end]+")", "0"])
                        except:
                            pass
                    else:
                        count_last_plus_or_minus = count
                if char == "x":
                    im_bruch = False
                    basis_gedreht = []
                    geoeffnete_klammern = 0
                    char_vor_x_count = count-1
                    while char_vor_x_count >= 0 and geoeffnete_klammern >= 0:
                        char_vor_x = funktion[char_vor_x_count]
                        if char_vor_x == ")":
                            geoeffnete_klammern += 1
                        if char_vor_x == "(":
                            geoeffnete_klammern -= 1
                            if geoeffnete_klammern < 0 and char_vor_x_count > 0:
                                if funktion[char_vor_x_count - 1] == "+":
                                    basis_gedreht.append("+")
                                    break
                                elif funktion[char_vor_x_count - 1] == "-":
                                    basis_gedreht.append("-")
                                    break
                                else:
                                    return False, "ausklammern"
                            elif char_vor_x_count == 0:
                                basis_gedreht.append("+")
                                break
                        if (char_vor_x == "+" or char_vor_x == "-") and geoeffnete_klammern == 0:
                            basis_gedreht.append(char_vor_x)
                            break
                        basis_gedreht.append(char_vor_x)
                        char_vor_x_count -= 1
                    if 'x' in basis_gedreht:
                        return False,"x ernuet in basis"
                    if basis_gedreht == []:
                        basis_gedreht = ['*','1']
                    if basis_gedreht == ['-']:
                        basis_gedreht = ['*','1','-']
                    if basis_gedreht == ['+']:
                        basis_gedreht = ['*','1','+']
                    if basis_gedreht[0] == "*":
                        del basis_gedreht[0]
                    elif basis_gedreht[0] == "/":
                        im_bruch = True
                        del basis_gedreht[0]
                    elif basis_gedreht != []:
                        break
                    if basis_gedreht[-1] != "+" and basis_gedreht[-1] != "-":
                        basis_gedreht.append("+")
                    basis = []
                    for i in range(len(basis_gedreht)-1,-1,-1):
                        basis.append(basis_gedreht[i])
                    exponent = []
                    geoeffnete_klammern = 0
                    is_basis_hinten_dran = False
                    char_nach_x_count = count+1
                    char_nach_x = ""
                    while char_nach_x_count < len(funktion) and geoeffnete_klammern >= 0:
                        char_nach_x = funktion[char_nach_x_count]
                        if char_nach_x == "(":
                            geoeffnete_klammern += 1
                        if char_nach_x == ")":
                            geoeffnete_klammern -= 1
                            if geoeffnete_klammern < 0 and char_vor_x_count == len(char_vor_x)-2:
                                if funktion[char_vor_x_count + 1] == "+":
                                    break
                                elif funktion[char_vor_x_count + 1] == "-":
                                    break
                                else:
                                    return False, "ausklammern"
                        if (char_nach_x == "+" or char_nach_x == "-") and geoeffnete_klammern == 0:
                            break
                        if (char_nach_x == "*" or char_nach_x == "/") and geoeffnete_klammern == 0:
                            is_basis_hinten_dran = True
                        if is_basis_hinten_dran:
                            basis.append(char_nach_x)
                            if "x" in basis:
                                return False,"x erneut in Basis"
                        else:
                            exponent.append(char_nach_x)
                        char_nach_x_count += 1
                    if 'x' in exponent:
                        return False,"x in exponent"
                    if exponent == []:
                        exponent = ["'",'1']
                    if exponent[0] == "'":
                        del exponent[0]
                    elif exponent != []:
                        break
                    if im_bruch:
                        if not ("".join(i for i in exponent)).isnumeric() and (exponent[0] != "(" or exponent[-1] != ")"):
                            exponent.insert(0, '(')
                            exponent.append(')')
                        exponent.insert(0,'-')
                    count = char_nach_x_count-1
                    num_plus_or_minus_since_last_expo = 0
                    klammern_offen = 0
                    try:
                        wert = eval(self.funktion_to_computer_readable(self.funktion_verschoenern("".join(i for i in basis))))
                        if isinstance(wert, int):
                            if wert >= 0:
                                basis_vereinfacht = "+" + str(wert)
                            else:
                                basis_vereinfacht = str(wert)
                        else:
                            basis_vereinfacht = "".join(i for i in basis)
                    except:
                        return False, "Funktion nicht ausfühbar"
                    try:
                        wert = eval(self.funktion_to_computer_readable(self.funktion_verschoenern("".join(i for i in exponent))))
                        if isinstance(wert,int):
                            if wert >= 0:
                                exponent_vereinfacht = str(wert)
                            else:
                                exponent_vereinfacht = "("+str(wert)+")"
                        else:
                            exponent_vereinfacht = "".join(i for i in exponent)
                    except:
                        return False,"Funktion nicht ausfühbar"
                    exponenten.append([basis_vereinfacht,exponent_vereinfacht])
                count += 1
            if exponenten == []:
                return False,"kein Exponent gefunden"
            exponenten = self.__exponenten_zusammenfuehren_und_sortieren(exponenten)
            expos_zu_funktion = ""
            for exponent in exponenten:
                if int(eval(exponent[1])) < 0:
                    expos_zu_funktion += exponent[0] + "*x'(" + exponent[1] + ")"
                else:
                    expos_zu_funktion += exponent[0] + "*x'" + exponent[1]
            # Checken
            x = -30
            if not check_funktionen_gleich(funktion,expos_zu_funktion):
                return False, "Funktion am Ende passt nicht"
            return exponenten,expos_zu_funktion
        else:
            return False,"kein x in Funktion"

    def __set_values_after_set_funktion_wurzel(self, funktion):
        self.__check_funktion_wurzel_funktion_and_convert(funktion)
        if self.debug_sonstiges != False:
            self.debug_sonstiges.add_funktion_not_erkannt_reason("Wurzelfunktion", "comming soon")
        self.is_wurzel = False
        self.funktion_wurzel_x_ersetzbar = ""
        self.funktion_wurzel_computer_readable = ""
        self.wurzel_a = 0
        self.wurzel_b = 0
        self.wurzel_c = 0

    def __check_funktion_wurzel_funktion_and_convert(self,funktion):
        return False,"comming soon"

    def __set_values_after_set_funktion_exponential(self, funktion):
        self.__check_funktion_exponential_funktion_and_convert(funktion)
        if self.debug_sonstiges != False:
            self.debug_sonstiges.add_funktion_not_erkannt_reason("Exponentialfunktion", "comming soon")
        self.is_ = False

    def __check_funktion_exponential_funktion_and_convert(self,funktion):
        return False,"comming soon"

    def __set_values_after_set_funktion_logarithmus(self, funktion):
        self.__check_funktion_logarithmus_funktion_and_convert(funktion)
        self.is_logarithmus = False
        if self.debug_sonstiges != False:
            self.debug_sonstiges.add_funktion_not_erkannt_reason("Logarithmusfunktion", "comming soon")
        self.funktion_logarithmus_x_ersetzbar = ""
        self.funktion_logarithmus_computer_readable = ""
        self.logarithmus_a = 0
        self.logarithmus_b = 0
        self.logarithmus_c = 0
        self.logarithmus_d = 0
        self.logarithmus_e = 0

    def __check_funktion_logarithmus_funktion_and_convert(self,funktion):
        return False,"comming soon"

    def __set_values_after_set_funktion_trigonometrische(self, funktion):
        self.is_trigonometrisch = False
        self.funktion_trigonometrisch_x_ersetzbar = ""
        self.funktion_trigonometrisch_computer_readable = ""
        self.trigonometrisch_a = 0
        self.trigonometrisch_b = 0
        self.trigonometrisch_c = 0
        self.trigonometrisch_d = 0
        for trigonometrische_funktion in ["sin","cos","tan"]:
            a,b,c,d = self.__check_funktion_trigonometrische_funktion_and_convert(funktion,trigonometrische_funktion)
            if not False in [a,b,c,d]:
                a,b,c,d = eval(a),eval(b),eval(c),eval(d)
                self.is_trigonometrisch = True
                self.trigonometrische_funktion = trigonometrische_funktion
                self.funktion_trigonometrisch_x_ersetzbar = ""
                if a != 1:
                    self.funktion_trigonometrisch_x_ersetzbar += str(a)+" * "
                self.funktion_trigonometrisch_x_ersetzbar += "sin("
                if b != 1:
                    self.funktion_trigonometrisch_x_ersetzbar += str(b)
                if c != 0:
                    self.funktion_trigonometrisch_x_ersetzbar += "*(x"+vorzeichen_str(c)+"))"
                else:
                    self.funktion_trigonometrisch_x_ersetzbar += "x)"
                if d != 0:
                    self.funktion_trigonometrisch_x_ersetzbar += vorzeichen_str(d)
                self.funktion_trigonometrisch_computer_readable = self.funktion_to_computer_readable(self.funktion_trigonometrisch_x_ersetzbar)
                self.trigonometrisch_a = a
                self.trigonometrisch_b = b
                self.trigonometrisch_c = c
                self.trigonometrisch_d = d
            else:
                if self.debug_sonstiges != False:
                    self.debug_sonstiges.add_funktion_not_erkannt_reason("Trigonometrisch "+trigonometrische_funktion, d)

    def __check_funktion_trigonometrische_funktion_and_convert(self,funktion,trigonometrische_funktion):
        funktion_array = []
        funktion_array.extend(funktion)
        a = ""
        b = ""
        c = ""
        d = ""
        if trigonometrische_funktion in funktion:
            pos = funktion.index(trigonometrische_funktion)
            if pos > 0:
                for index in range(pos):
                    a += funktion[index]
                if a[-1] != "*":
                    return False, False, False, "Vorfaktor nicht mal genommen"
                else:
                    a = a[:-1]
            else:
                a = "1"
            if funktion_array[pos + 3] == "(":
                offenen_klammern = 0
                klammer_ende = 0
                index = pos + 3
                while index < len(funktion_array):
                    if funktion_array[index] == "(":
                        offenen_klammern += 1
                    elif funktion_array[index] == ")":
                        offenen_klammern -= 1
                        if offenen_klammern == 0:
                            klammer_ende = index
                            index = len(funktion_array)
                    index += 1
                b, c = get_n_m_from_n_mal_x_plus_m(Funktion(funktion[pos + 4:klammer_ende]))
                if b == False or c == False:
                    return False, False, False, "innerer Term nicht erkannt"
                else:
                    for index in range(klammer_ende + 1, len(funktion)):
                        d += funktion_array[index]
            else:
                return False, False, False, "Keine Klammer nach Sinus"
            if "x" in a or "x" in b or "x" in c or "x" in d:
                return False, False, False, "x in a,b,c or d"
            for value in [a, b, c, d]:
                try:
                    wert = eval(value)
                    if not (isinstance(wert, int) or isinstance(wert, float)):
                        return False, False, False, "nicht definierter Wert in a,b,c or d"
                except Exception:
                    return False, False, False, "unsolvable value in a,b,c or d"
            result_funktion = str(eval(a))+"*sin("+str(eval(b))+"*(x"+vorzeichen_str(eval(c))+"))"+vorzeichen_str(eval(d))
            if not check_funktionen_gleich(funktion,result_funktion):
                return False,False,False,"Funktion am Ende passt nicht"
            return a, b, c, d
        else:
            return False,False,False,"Kein "+trigonometrische_funktion+" in Funktion"

    def string_an_zeichen_teilen(self,string,zeichen1,zeichen2):
        output = []
        for splitet1 in string.split(zeichen1):
            if splitet1 != '':
                for splitet2 in splitet1.split(zeichen2):
                    if splitet2 != '':
                        output.append(splitet2)
        return output

    def x_einsetzen(self,x):
        try:
            wert = eval(self.funktion_computer_readable.replace("x","("+str(x)+")"))
            if isinstance(wert,complex):
                return "nicht definiert"
            elif isinstance(wert,int) or isinstance(wert,float):
                return wert
        except Exception:
            return "nicht definiert"

    def funktion_x_eingesetzt(self,x):
        if isinstance(x,int) or isinstance(x,float):
            if x < 0:
                return self.funktion_user_x_ersetztbar.replace("x", "(" + str(x) + ")")
            else:
                return self.funktion_user_x_ersetztbar.replace("x", str(x))
        elif isinstance(x,str):
            if x.isnumeric():
                if eval(x) < 0:
                    return self.funktion_user_x_ersetztbar.replace("x", "(" + str(eval(x)) + ")")
                else:
                    return self.funktion_user_x_ersetztbar.replace("x", str(eval(x)))
            else:
                return self.funktion_user_x_ersetztbar.replace("x", "(" + x + ")")
        else:
            #print(Fehler beim einsetzen in Funktion",x)
            return ""

    def set_funktion(self,funktion):
        for letter in funktion:
            if letter == " " or letter == "+":
                funktion = funktion[1:]
            else:
                break
        funktion = self.funktion_verschoenern(self.funktion_verschoenern(self.funktion_verschoenern(funktion)))
        computer_funktion = self.funktion_to_computer_readable(funktion)
        if funktion != self.funktion_user_x_ersetztbar or computer_funktion != self.funktion_computer_readable:
            versuchs_x = [-10,-5,-2,-1-0.5,0,1,2,5,10,math.pi,math.pi/2,math.pi/3,math.e,math.e/2]
            working = True
            for x in versuchs_x:
                working = True
                try:
                    eval(computer_funktion)
                except Exception as e:
                    working = False
                if working:
                    break
            if working: # Funktion fehlerfrei
                self.funktion_user_x_ersetztbar = funktion
                self.funktion_user_kurz = self.funktion_to_user_kurz(funktion)
                self.funktion_computer_readable = computer_funktion
                self.funktion_sympy_readable = self.funktion_to_sympy_readable(funktion)
                self.exponenten_array = []
                self.nur_exponenten = []
                self.nur_basen = []
                self.exponenten_aufgefuellt_array = []
                self.nur_exponenten_aufgefuellt = []
                self.nur_basen_aufgefuellt = []
                self.__set_values_after_set_funktion_exponential(funktion)
                self.__set_values_after_set_funktion_logarithmus(funktion)
                self.__set_values_after_set_funktion_polynom(funktion)
                self.__set_values_after_set_funktion_trigonometrische(funktion)
                self.__set_values_after_set_funktion_wurzel(funktion)
                return True
            else:
                # Fehler in Funktion
                print("Funktion nicht erkannt:",funktion," (für computer",computer_funktion+")")
                return False
        else:
            return "unverändert"