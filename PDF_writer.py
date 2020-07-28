from fpdf import FPDF

pdf = FPDF()

def draw_title():
    pdf.set_text_color(0)
    pdf.set_font("font", size=15)
    pdf.cell(200, 15, txt="Kurvendiskussion", ln=1, align="C")
def draw_second_title(funktion:str):
    pdf.set_text_color(0)
    pdf.set_font("font", size=13)
    pdf.cell(200, 10, txt=funktion, ln=1, align="C")
def draw_topic(string,y):
    pdf.set_text_color(50,50,180)
    pdf.set_xy(10,y)
    pdf.set_font("font", size=13)
    pdf.write(10, string)
    return 8
def draw_second_topic(string,y):
    pdf.set_text_color(65,65,200)
    pdf.set_xy(12,y)
    pdf.set_font("font", size=12)
    pdf.write(10, string)
    return 8
def draw_rechenschritt(string,y):
    pdf.set_text_color(80,80,220)
    pdf.set_xy(15,y)
    pdf.set_font("font", size=10)
    pdf.write(10,string)
    return 8
def draw_funktion(string,y):
    pdf.set_text_color(0)
    pdf.set_xy(30, y)
    pdf.set_font("font", size=10)
    pdf.write(10, string)
    return 8
def draw_rechen_operation(string,y):
    pdf.set_text_color(0)
    pdf.set_xy(95, y-10)
    pdf.set_font("font", size=10)
    pdf.write(10, string)
    return 0
def draw_ergebnis(string:str,y):
    pdf.set_text_color(50,200,80)
    pdf.set_xy(20,y)
    pdf.set_font("font", size=10)
    pdf.write(10,string)
    return 8
def draw_now_ergebnis(string:str,y):
    pdf.set_text_color(200, 50, 80)
    pdf.set_xy(20, y)
    pdf.set_font("font", size=10)
    pdf.write(10, string)
    return 8

def draw_texts(texts,y):
    for line in texts:
        if y > 260:
            pdf.add_page()
            y = 20
        if line[0] == "fkt":
            y += draw_funktion(line[1], y)
        if line[0] == "op":
            y += draw_rechen_operation(line[1], y)
        if line[0] == "erg":
            y += draw_ergebnis(line[1], y)
        if line[0] == "noerg":
            y += draw_ergebnis(line[1], y)
        if line[0] == "calc":
            y += draw_rechenschritt(line[1], y)
        if line[0] == "title":
            y += draw_second_topic(line[1], y)
    return y

def create_pdf(file_name,pdf_settings):
    pdf.add_page()
    pdf.add_font("font", "", """C:\\Users\\Public\\Documents\\Amiga Files\\Shared\\dir\\System\\Fonts\\_TrueType\\arial.ttf""", uni=True)

    draw_title()
    draw_second_title("Funtion: f(x) = "+str(pdf_settings.funktion))
    y = 40
    if pdf_settings.second_funktion != "":
        draw_second_title("Zweite Funktion: g(x) = "+str(pdf_settings.second_funktion))
        y += 10
    if pdf_settings.draw_image:
        pdf.image("image.png",x=40,y=32,w=128,h=96)
        y += 90
    if pdf_settings.draw_schnittpunkt_y_achse:
        y += draw_topic("Schnittpunkt mit der Y-Achse", y)
        y = draw_texts(pdf_settings.schnittpunkt_y_achse_texte,y) + 20
    if pdf_settings.draw_nullstellen:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Nullstellen",y)
        y += draw_rechenschritt("Ermitteln durch f(x) = 0",y)
        y = draw_texts(pdf_settings.nullstellen_texte,y) + 20
    if pdf_settings.draw_globales_verhalten:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Globales Verhalten", y)
        y = draw_texts(pdf_settings.globales_verhalten_texte,y) + 20
    if pdf_settings.draw_differenz_funktion and pdf_settings.second_funktion != "":
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Differenzfunktion", y)
        y = draw_texts(pdf_settings.differenz_funktion_texte,y) + 20
    if pdf_settings.draw_nullstellen_differenz_funktion and pdf_settings.second_funktion != "":
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Nullstellen der Differenzfunktion (Schnittpunkte der Funktionen)", y)
        y = draw_texts(pdf_settings.nullstellen_differenz_funktion_texte,y) + 20
    if pdf_settings.draw_stammfunktion_differenzfunktion and pdf_settings.second_funktion != "":
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Stammfunktion der Differenzfunktion", y)
        y = draw_texts(pdf_settings.stammfunktion_differenzfunktion_texte,y) + 20
    if pdf_settings.draw_ableitung:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Ableitungen", y)
        y = draw_texts(pdf_settings.ableitung_texte,y) + 20
    if pdf_settings.draw_normale:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Normale", y)
        y = draw_texts(pdf_settings.normale_texte,y) + 20
    if pdf_settings.draw_tangente:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Tangente", y)
        y = draw_texts(pdf_settings.tangente_texte,y) + 20
    if pdf_settings.draw_steigung:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Steigung (Extrempunkte)", y)
        y = draw_texts(pdf_settings.steigung_texte,y) + 20
    if pdf_settings.draw_kruemmung:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Krümmung (Wendepunkte)", y)
        y = draw_texts(pdf_settings.kruemmung_texte,y) + 20
    if pdf_settings.draw_stammfunktion:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Stammfunktion", y)
        y = draw_texts(pdf_settings.stammfunktion_texte,y) + 20
    if pdf_settings.draw_integral:
        if y > 220:
            pdf.add_page()
            y = 20
        y += draw_topic("Integral", y)
        y = draw_texts(pdf_settings.integral_texte,y) + 20

    print(file_name)
    pdf.output(file_name)