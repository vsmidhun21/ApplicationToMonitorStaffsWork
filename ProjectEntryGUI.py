import HomePage
from HomePage import *
from pathlib import Path
# from tkinter import *
import DatabaseDetails
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, INSERT,ttk
import tkinter.messagebox
import sys
import pypyodbc as odbc
from prettytable import PrettyTable
#from HomePage import HmPg

##########################################Path of GUI Comp
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path('assets/frame0')

##################################################Functions
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def addbtn(cursor,entry_1,entry_2,entry_3):
    code=entry_1.get()
    #print(code)
    name=entry_2.get()
    #print(name)
    cuname=entry_3.get()
    #print(cuname)
    if (code!='' and name!='' and cuname!=''):
        ent_strig =f"""INSERT INTO project VALUES({code},'{name}','{cuname}');"""
        try:
            print(ent_strig)
            cursor.execute(ent_strig)
        except Exception as e:
            cursor.rollback()
            print(e)
            print('rolled back')
            tkinter.messagebox.showinfo("Status", "Fill the details correctly")
        else:
            print('Inserted Successfully')
            tkinter.messagebox.showinfo("Status", "Successfully Updated")
            entry_1.delete(0,'end')
            entry_2.delete(0,'end')
            entry_3.delete(0,'end')
    else:
        tkinter.messagebox.showinfo("Status", "Need to fill the Mandatory Fields")

def sltbtn(cursor,entry_4,entry_5,entry_6):
    dcode=entry_4.get()
    #print(dcode)
    if (dcode!=''):
        sch_pn_string=f"""SELECT Project_Name FROM project WHERE Project_Code ={dcode};"""
        #print(sch_pn_string)
        try:
            cursor.execute(sch_pn_string)
            fch=cursor.fetchone()
            for i in fch:
                dname=i
            print(dname)
            sch_cn_string = f"""SELECT Customer_Name FROM project WHERE Project_Code ={dcode};"""
            #print(sch_cn_string)
            cursor.execute(sch_cn_string)
            fech = cursor.fetchone()
            for i in fech:
                dcnam=i
            print(dcnam)
            entry_5.insert(0,f'{dname}')
            entry_6.insert(0,f'{dcnam}')
        except Exception as e:
            print(e)
            tkinter.messagebox.showinfo("Status", "No Such Project Code")
    else:
        tkinter.messagebox.showinfo("Status", "Select Project Code")

def dltbtn(cursor,entry_4,entry_5,entry_6):
    dcd=entry_4.get()
    dpn=entry_5.get()
    dcn=entry_6.get()
    if(dcd!='' and dpn!='' and dcn!=''):
        dl_string=f"""delete from project where Project_Code = {dcd}"""
        print(dl_string)
        try:
            cursor.execute(dl_string)
        except Exception as e:
            print(e)
            tkinter.messagebox.showinfo("Status", "Sorry Project Not Deleted")
        else:
            tkinter.messagebox.showinfo("Status", "Successfully Deleted")
            entry_4.set('')
            entry_5.delete(0, 'end')
            entry_6.delete(0, 'end')
    else:
        tkinter.messagebox.showinfo("Status", "Details Missing!!!")

def disply(cursor):
    qry_str="""SELECT * FROM project"""
    try:
        print(qry_str)
        cursor.execute(qry_str)
        fch=cursor.fetchall()
        print(fch)
        print(type(fch))
    except Exception as e:
        print(e)
    else:
        disp = Tk()
        disp.geometry('750x500')
        disp.title("Projects")
        t = Text(disp)
        t.config(width=750,height=500)
        x=PrettyTable()
        x.field_names = ["Project Code","Project Name","Customer Name"]
        ln = len(fch)
        for i in range(0, ln):
            x.add_row(fch[i])
        t.insert(INSERT, x)
        t.config(state="disabled")
        t.pack()
        disp.mainloop()

def cncl(ui,conn,cursor):
    ui.destroy()
    cursor.commit()
    cursor.close()
    if conn.connected == 1:
        print('Connection Closed')
        conn.close()
    HomePage.HmPg()


def MainPrjPg():

    try:
        conn = odbc.connect(DatabaseDetails.conn_string)
        print('connecting...')
    except Exception as e:
        print(e)
        print('Connection Terminated')
        sys.exit()
    else:
        print('Success')
        cursor = conn.cursor()

    try:
        qr_str="""SELECT Project_Code from project"""
        cursor.execute(qr_str)
    except Exception as e:
        print(e)
    else:
        pcode=[]
        fl=cursor.fetchall()
        for i in fl:
            pcode.append(i[0])

    #############################GUI Tkinter
    ui = Tk()
    ui.state('zoomed')
    ui.configure(bg = "#3A3A3A")
    ui.title('ProjectEntry')

    canvas = Canvas(
        ui,
        bg = "#3A3A3A",
        height = 704,
        width = 1352,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_text(
        326.0,
        38.0,
        anchor="nw",
        text="PROJECT DETAILS",
        fill="#FFFFFF",
        font=("LexendMega Regular", 64 * -1)
    )

    canvas.create_text(
        120.0,
        163.0,
        anchor="nw",
        text="Add Project",
        fill="#FFFFFF",
        font=("InknutAntiqua Regular", 48 * -1)
    )

    canvas.create_text(
        842.0,
        162.0,
        anchor="nw",
        text="Delete Project",
        fill="#FFFFFF",
        font=("InknutAntiqua Regular", 48 * -1)
    )

    canvas.create_text(
        100.0,
        345.0,
        anchor="nw",
        text="Project Code :",
        fill="#FFFFFF",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        100.0,
        403.0,
        anchor="nw",
        text="Project Name :",
        fill="#FFFFFF",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        100.0,
        460.0,
        anchor="nw",
        text="Customer Name :",
        fill="#FFFFFF",
        font=("Inter", 24 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        437.5,
        359.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=('Arial 15')
    )
    entry_1.place(
        x=322.0,
        y=345.0,
        width=231.0,
        height=26.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        437.5,
        416.0,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=('Arial 15')
    )
    entry_2.place(
        x=322.0,
        y=402.0,
        width=231.0,
        height=26.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        437.5,
        474.0,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=('Arial 15')
    )
    entry_3.place(
        x=322.0,
        y=460.0,
        width=231.0,
        height=26.0
    )

    canvas.create_text(
        818.0,
        289.0,
        anchor="nw",
        text="Project Code :",
        fill="#FFFFFF",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        818.0,
        414.0,
        anchor="nw",
        text="Project Name :",
        fill="#FFFFFF",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        818.0,
        471.0,
        anchor="nw",
        text="Customer Name :",
        fill="#FFFFFF",
        font=("Inter", 24 * -1)
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        1155.5,
        303.0,
        image=entry_image_4
    )
    entry_4 =  ttk.Combobox(
        state="readonly",
        values=pcode,
        font=('Arial 15')
    )
    entry_4.place(
        x=1040.0,
        y=289.0,
        width=231.0,
        height=26.0
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        1155.5,
        427.0,
        image=entry_image_5
    )
    entry_5 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=('Arial 15')
    )
    entry_5.place(
        x=1040.0,
        y=413.0,
        width=231.0,
        height=26.0
    )

    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        1155.5,
        485.0,
        image=entry_image_6
    )
    entry_6 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=('Arial 15')
    )
    entry_6.place(
        x=1040.0,
        y=471.0,
        width=231.0,
        height=26.0
    )

    canvas.create_rectangle(
        674.0,
        125.0,
        676.0,
        675.0,
        fill="#FFFFFF",
        outline="")

    #############################################Button Part
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:addbtn(cursor,entry_1,entry_2,entry_3),
        relief="flat"
    )
    button_1.place(
        x=168.32464599609375,
        y=536.7432250976562,
        width=305.70904541015625,
        height=59.270263671875
    )
    ###########################################################2
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:dltbtn(cursor,entry_4,entry_5,entry_6),
        relief="flat"
    )
    button_2.place(
        x=886.454833984375,
        y=547.7432250976562,
        width=305.70904541015625,
        height=59.270263671875
    )
    ###################################################################3
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:sltbtn(cursor,entry_4,entry_5,entry_6),
        relief="flat"
    )
    button_3.place(
        x=968.0,
        y=345.0,
        width=141.0,
        height=38.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:disply(cursor),
        relief="flat"
    )
    button_4.place(
        x=168.0,
        y=616.0,
        width=305.70904541015625,
        height=59.270263671875
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:cncl(ui,conn,cursor),
        relief="flat"
    )
    button_5.place(
        x=886.0,
        y=630.0,
        width=305.70904541015625,
        height=59.270263671875
    )
    ui.mainloop()
