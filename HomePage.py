from pathlib import Path
from ReportGUI import *
from ProjectEntryGUI import *
from WorkDetails import *
from NameDetails import *
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

##########################################################################Path
OUTPUT_PATH1 = Path(__file__).parent
ASSETS_PATH1 = OUTPUT_PATH1 / Path("assets/frame1")

#####################################################################Func

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH1 / Path(path)

def prj(windo):
    windo.destroy()
    MainPrjPg()

def rprt(windo):
    windo.destroy()
    report()

def works(windo):
    windo.destroy()
    Mainwrk()

def names(windo):
    windo.destroy()
    Mainnam()

def ext(windo):
    windo.destroy()

def HmPg():
    ##########################################################3UI
    windo = Tk()
    windo.title("Home Page")
    windo.state('zoomed')
    windo.configure(bg = "#FFFFFF")


    cannva = Canvas(
        windo,
        bg = "#FFFFFF",
        height = 735,
        width = 1440,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    cannva.place(x = 0, y = 0)


    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = cannva.create_image(
        720.0,
        135.0,
        image=image_image_2
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:prj(windo),
        relief="flat"
    )
    button_1.place(
        x=137.0,
        y=248.0,
        width=324.0,
        height=68.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:rprt(windo),
        relief="flat"
    )
    button_2.place(
        x=930.0,
        y=248.0,
        width=324.0,
        height=68.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: works(windo),
        relief="flat"
    )
    button_3.place(
        x=137.0,
        y=423.0,
        width=324.0,
        height=68.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: names(windo),
        relief="flat"
    )
    button_4.place(
        x=930.0,
        y=423.0,
        width=324.0,
        height=68.0
    )
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ext(windo),
        relief="flat"
    )
    button_5.place(
        x=558.0,
        y=554.0,
        width=324.0,
        height=68.0
    )
    #windo.resizable(False, False)
    windo.mainloop()
