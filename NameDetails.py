from pathlib import Path
import sys
from prettytable import PrettyTable
import pypyodbc as odbc
from HomePage import *
import DatabaseDetails
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, INSERT
import tkinter.messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path('assets/frame2')

work_list=[]

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def Adnam(entry_1,cursor,window):
    awrk=entry_1.get()
    print(awrk)
    if(awrk!=''):
        try:
            add_str=f"""INSERT INTO names VALUES('{awrk}')"""
            print(add_str)
            cursor.execute(add_str)
        except Exception as e:
            print(e)
        else:
            tkinter.messagebox.showinfo("Status", "Name Added")
            entry_1.delete(0,'end')
            window.update()
    else:
        tkinter.messagebox.showinfo("Status", "Fill the Name to be added")

def Delnam(entry_2,cursor,window):
    dwrk=entry_2.get()
    print(dwrk)
    if(dwrk!=''):
        try:
            dl_str=f"""delete from names where Name = '{dwrk}'"""
            print(dwrk)
            cursor.execute(dl_str)
        except Exception as e:
            print(e)
        else:
            tkinter.messagebox.showinfo("Status", "Name Deleted")
            entry_2.set('')
            window.update()
            window.update_idletasks()
            print("Refresh completed.")
            work_list.remove(dwrk)
    else:
        tkinter.messagebox.showinfo("Status", "Fill the Name to be Deleted")

def ccl(cursor,window,conn):
    window.destroy()
    cursor.commit()
    cursor.close()
    if conn.connected == 1:
        print('Connection Closed')
        conn.close()
    HomePage.HmPg()

def disp(cursor):
    qry_str = """SELECT * FROM names"""
    try:
        print(qry_str)
        cursor.execute(qry_str)
        fch = cursor.fetchall()
    except Exception as e:
        print(e)
    else:
        disp = Tk()
        disp.geometry('500x500')
        disp.title("Projects")
        t = Text(disp)
        t.config(width=750, height=500)
        x = PrettyTable()
        x.field_names = ["Works"]
        ln = len(fch)
        for i in range(0, ln):
            x.add_row(fch[i])
        t.insert(INSERT, x)
        t.config(state="disabled")
        t.pack()
        disp.mainloop()


def Mainnam():
    window = Tk()
    window.title('Work Details')
    window.state('zoomed')
    window.configure(bg = "#252525")


    try:
        conn = odbc.connect(DatabaseDetails.conn_string)
        print('connecting...')
    except Exception as e:
        print(e)
        print('Task Terminated')
        sys.exit()
    else:
        print('Success')
        cursor = conn.cursor()



    canva = Canvas(
        window,
        bg = "#252525",
        height = 700,
        width = 1440,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canva.place(x = 0, y = 0)
    canva.create_rectangle(
        717.0,
        132.0,
        720.0,
        643.0,
        fill="#FFFFFF",
        outline="")

    canva.create_text(
        633.0,
        55.0,
        anchor="nw",
        text="NAMES",
        fill="#FFFFFF",
        font=("Inter", 48 * -1)
    )

    canva.create_text(
        231.0,
        135.0,
        anchor="nw",
        text="ADD NAME",
        fill="#FFFFFF",
        font=("Inter", 48 * -1)
    )

    canva.create_text(
        913.0,
        135.0,
        anchor="nw",
        text="DELETE NAME",
        fill="#FFFFFF",
        font=("Inter", 48 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canva.create_image(
        360.5,
        285.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=('Arial 20')
    )
    entry_1.place(
        x=121.0,
        y=238.0,
        width=479.0,
        height=93.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canva.create_image(
        1080.5,
        285.5,
        image=entry_image_2
    )

    cursor.execute("SELECT Name FROM names;")
    rows = cursor.fetchall()
    for i in rows:
        work_list.append(i[0])

    entry_2 = ttk.Combobox(
        state="readonly",
        values=work_list,
        font=('Arial 20')
    )
    entry_2.place(
        x=841.0,
        y=238.0,
        width=479.0,
        height=93.0
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: Adnam(entry_1,cursor,window),
        relief="flat"
    )
    button_1.place(
        x=128.0,
        y=416.0,
        width=472.0,
        height=91.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: Delnam(entry_2,cursor,window),
        relief="flat"
    )
    button_2.place(
        x=845.0,
        y=416.0,
        width=472.0,
        height=91.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: disp(cursor),
        relief="flat"
    )
    button_3.place(
        x=121.0,
        y=552.0,
        width=472.0,
        height=91.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ccl(cursor,window,conn),
        relief="flat"
    )
    button_4.place(
        x=845.0,
        y=552.0,
        width=472.0,
        height=91.0
    )
    #window.resizable(False, False)
    #window.protocol("WM_DELETE_WINDOW", close(cursor))
    window.mainloop()
