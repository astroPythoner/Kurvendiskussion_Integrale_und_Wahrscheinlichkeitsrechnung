import math

from time import sleep

class Funktion():

    funktion_user_kurz = ""
    funktion_user_x_ersetztbar = ""
    funktion_computer_readable = ""
    funktion_polinom_x_ersetzbar = ""
    funktion_polinom_computer_readable = ""
    exponenten_array = []
    nur_exponenten = []
    nur_basen = []
    funktion_polinom_aufgefüllt_x_ersetzbar = ""
    funktion_polinom_aufgefüllt_computer_readable = ""
    exponenten_aufgefüllt_array = []
    nur_exponenten_aufgefüllt = []
    nur_basen_aufgefüllt = []
    is_polinomfunktion = False


    def funktion_verschönern(self,funktion):
        # ganz ausschreiben  (3x -> 3*x)
        funktion = funktion.replace("^", "'")
        funktion = funktion.replace(",", ".")
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
                if letter_davor != None and (letter_davor.isnumeric() or letter_davor==")" or letter_davor=="i" or letter_davor=="e" or letter_davor=="c" or letter_davor=="g"  or letter_davor == "x"):
                    funktion_array.insert(count, "*")
                    count -= 1
                if letter_danach != None and (letter_danach.isnumeric() or letter_danach == "(" or letter_danach=="p" or letter_danach=="e" or letter_danach=="c" or letter_danach=="g"  or letter_danach == "x"):
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
        funktion_array = []
        funktion_array.extend(funktion)
        for count,letter in enumerate(funktion_array):
            if letter == "'":
                funktion_array[count] = "**"
        funktion = "".join(i for i in funktion_array)
        funktion = funktion.replace("e","math.e")
        funktion = funktion.replace("pi", "math.pi")
        funktion = funktion.replace("c", "299729458")
        funktion = funktion.replace("g", "9.80665")
        if "asin" in funktion or "atan" in funktion or "acos" in funktion or "arcsin" in funktion or "arccos" in funktion or "arctan" in funktion:
            funktion = funktion.replace("asin", "math.asin")
            funktion = funktion.replace("acos", "math.acos")
            funktion = funktion.replace("atan", "math.atan")
            funktion = funktion.replace("arcsin", "math.asin")
            funktion = funktion.replace("arccos", "math.acos")
            funktion = funktion.replace("arctan", "math.atan")
        else:
            funktion = funktion.replace("sin", "math.sin")
            funktion = funktion.replace("cos", "math.cos")
            funktion = funktion.replace("tan", "math.tan")
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

    def exponenten_zusammenführen_und_sortieren(self,exponenten_mit_basis):
        gekürzte_exponenten = []
        gekürzte_basen = []
        # ausrechnen
        for count,exponent_mis_basis in enumerate(exponenten_mit_basis):
            gekürzte_exponenten.append(str(eval(self.funktion_to_computer_readable(self.funktion_verschönern(exponent_mis_basis[1])))))
            wert = eval(self.funktion_to_computer_readable(self.funktion_verschönern(exponent_mis_basis[0])))
            if wert > 0:
                gekürzte_basen.append("+"+str(wert))
            else:
                gekürzte_basen.append(str(wert))
        # zusammenführen
        count1=0
        count2=0
        while count1 < len(gekürzte_exponenten):
            expo1 = gekürzte_exponenten[count1]
            while count2 < len(gekürzte_exponenten):
                expo2 = gekürzte_exponenten[count2]
                if count1 != count2 and expo1 == expo2:
                    wert = int(gekürzte_basen[count1])+int(gekürzte_basen[count2])
                    if wert > 0:
                        gekürzte_basen[count1] = "+" + str(wert)
                    else:
                        gekürzte_basen[count1] = str(wert)
                    del gekürzte_exponenten[count2]
                    del gekürzte_basen[count2]
                count2 += 1
            count1 += 1
        exponenten_mit_basis = []
        for x in range(len(gekürzte_exponenten)):
            exponenten_mit_basis.append([gekürzte_basen[x],gekürzte_exponenten[x]])
        # sortieren
        switched_something = True
        while switched_something:
            switched_something = False
            for j in range(len(exponenten_mit_basis)-1):
                if eval(exponenten_mit_basis[j+1][1]) > eval(exponenten_mit_basis[j][1]):
                    switched_something = True
                    exponenten_mit_basis[j], exponenten_mit_basis[j + 1] = exponenten_mit_basis[j + 1], exponenten_mit_basis[j]
        return exponenten_mit_basis

    def sortierte_exponenten_auffüllen(self,exponenten_sortiert_mit_basis):
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

    def check_funktion_exponential_funktion_and_convert(self,funktion):
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
                    geöffnete_klammern = 0
                    char_vor_x_count = count-1
                    while char_vor_x_count >= 0 and geöffnete_klammern >= 0:
                        char_vor_x = funktion[char_vor_x_count]
                        if char_vor_x == ")":
                            geöffnete_klammern += 1
                        if char_vor_x == "(":
                            geöffnete_klammern -= 1
                            if geöffnete_klammern < 0 and char_vor_x_count > 0:
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
                        if (char_vor_x == "+" or char_vor_x == "-") and geöffnete_klammern == 0:
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
                    geöffnete_klammern = 0
                    is_basis_hinten_dran = False
                    char_nach_x_count = count+1
                    char_nach_x = ""
                    while char_nach_x_count < len(funktion) and geöffnete_klammern >= 0:
                        char_nach_x = funktion[char_nach_x_count]
                        if char_nach_x == "(":
                            geöffnete_klammern += 1
                        if char_nach_x == ")":
                            geöffnete_klammern -= 1
                            if geöffnete_klammern < 0 and char_vor_x_count == len(char_vor_x_count)-2:
                                if funktion[char_vor_x_count + 1] == "+":
                                    break
                                elif funktion[char_vor_x_count + 1] == "-":
                                    break
                                else:
                                    return False, "ausklammern"
                        if (char_nach_x == "+" or char_nach_x == "-") and geöffnete_klammern == 0:
                            break
                        if (char_nach_x == "*" or char_nach_x == "/") and geöffnete_klammern == 0:
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
                        wert = eval(self.funktion_to_computer_readable(self.funktion_verschönern("".join(i for i in basis))))
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
                        wert = eval(self.funktion_to_computer_readable(self.funktion_verschönern("".join(i for i in exponent))))
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
            exponenten = self.exponenten_zusammenführen_und_sortieren(exponenten)
            expos_zu_funktion = ""
            for exponent in exponenten:
                expos_zu_funktion += exponent[0] + "*x'" + exponent[1]
            # Checken
            x = -30
            while x < 30:
                if x < 0:
                    x_str = "("+str(x)+")"
                else:
                    x_str = str(x)
                wert_orig = eval(self.funktion_to_computer_readable(funktion).replace("x",x_str))
                wert_eigen = eval(self.funktion_to_computer_readable(expos_zu_funktion).replace("x",x_str))
                if not ((isinstance(wert_eigen, complex) or "e" in str(wert_eigen))):
                    if round(wert_eigen,6) != round(wert_orig,6):
                        return False,"Funktion am Ende passt nicht "+str(exponenten)+"  "+self.funktion_to_computer_readable(expos_zu_funktion)+" <-> "+self.funktion_to_computer_readable(funktion)+"   x="+x_str + "  " + str(wert_orig) + " <-> "+str(wert_eigen)
                x += 0.1
            for x in [math.pi,math.pi/2,math.pi/3]:
                wert_orig = eval(self.funktion_to_computer_readable(funktion).replace("x",str(x)))
                wert_eigen = eval(self.funktion_to_computer_readable(expos_zu_funktion).replace("x",str(x)))
                if not ((isinstance(wert_eigen, complex) or "e" in str(wert_eigen))):
                    if round(wert_eigen,6) != round(wert_orig,6):
                        return False,"Funktion am Ende passt nicht "+str(exponenten)+"  "+self.funktion_to_computer_readable(expos_zu_funktion)+" <-> "+self.funktion_to_computer_readable(funktion)+"   x="+x_str + "  " + str(wert_orig) + " <-> "+str(wert_eigen)
            return exponenten,expos_zu_funktion
        else:
            return False,"kein x in Funktion"

    def string_an_zeichen_teilen(self,string,zeichen1,zeichen2):
        output = []
        for splitet1 in string.split(zeichen1):
            if splitet1 != '':
                for splitet2 in splitet1.split(zeichen2):
                    if splitet2 != '':
                        output.append(splitet2)
        return output

    def set_funktion(self,funktion):
        funktion = self.funktion_verschönern(self.funktion_verschönern(self.funktion_verschönern(funktion)))
        computer_funktion = self.funktion_to_computer_readable(funktion)
        if funktion != self.funktion_user_x_ersetztbar or computer_funktion != self.funktion_computer_readable:
            versuchs_x = [-10,-5,-2,-1-0.5,0,1,2,5,10,math.pi,math.pi/2,math.pi/3,math.e,math.e/2]
            working = True
            for x in versuchs_x:
                working = True
                try:
                    eval(computer_funktion)
                except Exception:
                    working = False
                if working:
                    break
            if working:
                #Funktion fehlerfrei
                self.funktion_user_x_ersetztbar = funktion
                self.funktion_user_kurz = self.funktion_to_user_kurz(funktion)
                self.funktion_computer_readable = computer_funktion
                self.exponenten_array = []
                self.nur_exponenten = []
                self.nur_basen = []
                self.exponenten_aufgefüllt_array = []
                self.nur_exponenten_aufgefüllt = []
                self.nur_basen_aufgefüllt = []
                exponenten,expo_funktion = self.check_funktion_exponential_funktion_and_convert(funktion)
                if exponenten == False or exponenten == None:
                    self.is_polinomfunktion = False
                    self.funktion_polinom_x_ersetzbar = ""
                    self.funktion_polinom_computer_readable = ""
                    self.funktion_polinom_aufgefüllt_x_ersetzbar = ""
                    self.funktion_polinom_aufgefüllt_computer_readable = ""
                else:
                    self.is_polinomfunktion = True
                    self.exponenten_array = exponenten
                    for exponent in self.exponenten_array:
                        self.nur_exponenten.append(exponent[1])
                        self.nur_basen.append(exponent[0])
                    self.funktion_polinom_x_ersetzbar = self.funktion_verschönern(expo_funktion)
                    self.funktion_polinom_computer_readable = self.funktion_to_computer_readable(self.funktion_polinom_x_ersetzbar)
                    self.exponenten_aufgefüllt_array = self.sortierte_exponenten_auffüllen(exponenten)
                    funktion = ""
                    for exponent in self.exponenten_aufgefüllt_array:
                        self.nur_exponenten_aufgefüllt.append(exponent[1])
                        self.nur_basen_aufgefüllt.append(exponent[0])
                        if eval(exponent[1])<0:
                            funktion += exponent[0] + "*x'(" + exponent[1]+")"
                        else:
                            funktion += exponent[0] + "*x'" + exponent[1]
                    self.funktion_polinom_aufgefüllt_x_ersetzbar = self.funktion_verschönern(funktion)
                    self.funktion_polinom_aufgefüllt_computer_readable = self.funktion_to_computer_readable(self.funktion_polinom_x_ersetzbar)
                return True
            else:
                # Fehler in Funktion
                return False
        else:
            return "unverändert"



'''
print(funktion)
funktion.replace(" ","")
erg = []
# Klammern
funktion_klammer_geteilt = self.string_an_zeichen_teilen(funktion,"(",")")
print(funktion_klammer_geteilt)
for funktionsteil in funktion_klammer_geteilt:
    # Striche (+ und -)
    if funktionsteil != "(" and funktionsteil != ")":
        print("teil:",funktionsteil)
        if "x" in funktionsteil:
            funktion_strich_geteilt = self.string_an_zeichen_teilen(funktionsteil,"+","-")
            for funktionsteil2 in funktion_strich_geteilt:
                if funktionsteil2 != "+" and funktionsteil2 != "-":
                    if "x" in funktionsteil2:
                        if "'" in funktionsteil2:
                            print("1 exponent:",funktionsteil2)
                            erg.append(funktionsteil2)
                        else:
                            print("1 x_teil:",funktionsteil2)
                            erg.append(funktionsteil2)
                    else:
                        try:
                            eval(funktionsteil2)
                            if isinstance(eval(funktionsteil2),int):
                                print("1 vereinfachter_funktionesteil:",eval(funktionsteil2))
                                erg.append(eval(funktionsteil2))
                            else:
                                print("1 nicht vereinfachter_funktionesteil:",funktionsteil2)
                                erg.append(funktionsteil2)
                        except:
                            print("1 nicht vereinfachter_funktionesteil:", funktionsteil2)
                            erg.append(funktionsteil2)
        else:
            try:
                eval(funktionsteil)
                if isinstance(eval(funktionsteil), int):
                    print("1 vereinfachter_funktionesteil:", eval(funktionsteil))
                    erg.append(eval(funktionsteil))
                else:
                    print("1 nicht vereinfachter_funktionesteil:", funktionsteil)
                    erg.append(funktionsteil)
            except:
                print("1 nicht vereinfachter_funktionesteil:", funktionsteil)
                erg.append(funktionsteil)
return erg
'''