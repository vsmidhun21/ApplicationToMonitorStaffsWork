import pypyodbc as odbc
from pathlib import Path
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys
from fpdf import FPDF
import DatabaseDetails
import tkinter.messagebox
from HomePage import *
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path('assets/frame5')
pdf = FPDF()
pans=[]
wans=[]
twrkstr=""
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def ccl(cursor,window,conn):
    window.destroy()
    cursor.commit()
    cursor.close()
    if conn.connected == 1:
        print('Connection Closed')
        conn.close()
    from HomePage import HmPg
    HmPg()

def clr(entry_2,entry_4,entry_6,entry_7,entry_12):
    entry_2.set('')
    entry_4.set('')
    entry_6.set('')
    for item in entry_7.get_children():
        entry_7.delete(item)
    pans.clear()
    wans.clear()
    entry_12.config(state="normal")
    entry_12.delete(0,'end')
    entry_12.config(state="disabled")

def sel1(cursor,entry_2):
    pans.clear()
    qry=f"""Select DISTINCT Project_Code FROM employeeFill WHERE Name = '{entry_2.get()}'"""
    try:
        print(qry)
        cursor.execute(qry)
    except Exception as e:
        print(e)
    else:
        fch=cursor.fetchall()
        for i in fch:
            pans.append(i[0])

def sel2(cursor,entry_2,entry_4):
    wans.clear()
    qry=f"""Select DISTINCT Work FROM employeeFill WHERE Project_Code = {entry_4.get()} and Name = '{entry_2.get()}'"""
    try:
        print(qry)
        cursor.execute(qry)
    except Exception as e:
        print(e)
    else:
        fch=cursor.fetchall()
        for i in fch:
            wans.append(i[0])


def GetValue(cursor,entry_2,entry_4,entry_6,entry_7,entry_12):
    entry_12.config(state="normal")
    entry_12.delete(0,'end')
    tWrkHr=0
    for i in entry_7.get_children():
        entry_7.delete(i)
    f1eq = entry_2.get()
    f2eq = entry_4.get()
    f3eq = entry_6.get()
    if(f1eq != '' and f2eq=='' and f3eq==''):
        qry_st=f"""SELECT * FROM employeeFill WHERE Name = '{f1eq}'"""
        qry_wrkHr=f"""SELECT Work_Hours FROM employeeFill WHERE Name = '{f1eq}'"""
        try:
            print(qry_st)
            cursor.execute(qry_st)
        except Exception as e:
            print(e)
        else:
            data=cursor.fetchall()
            entry_7["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
            hed = ["Name", "Work", "Project Name", "Expected Date", "Remarks", "Start Date", "Strat Time", "End Time",
                   "Work Hours", "Customer Name", "Project Code", "Work Percentage"]
            entry_7['show'] = 'headings'
            for i in range(0, len(hed)):
                entry_7.column(i + 1, width=110, anchor='c')
                entry_7.heading(i + 1, text=hed[i])
            for i in range(0, len(data)):
                entry_7.insert("", 'end', values=(data[i]))
            try:
                print(qry_wrkHr)
                cursor.execute(qry_wrkHr)
            except Exception as e:
                print(e)
            else:
                wrkHr=cursor.fetchall()
                for i in wrkHr:
                    tWrkHr+=i[0]
                entry_12.insert(0, f'{tWrkHr}')
                entry_12.config(state="disabled")

    elif (f1eq == '' and f2eq != '' and f3eq == ''):
        qry_st = f"""SELECT * FROM employeeFill WHERE Project_Code = {f2eq}"""
        qry_wrkHr = f"""SELECT Work_Hours FROM employeeFill WHERE Project_Code = {f2eq}"""
        try:
            print(qry_st)
            cursor.execute(qry_st)
        except Exception as e:
            print(e)
        else:
            data = cursor.fetchall()
            entry_7["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
            hed = ["Name", "Work", "Project Name", "Expected Date", "Remarks", "Start Date", "Strat Time", "End Time",
                   "Work Hours", "Customer Name", "Project Code", "Work Percentage"]
            entry_7['show'] = 'headings'
            for i in range(0, len(hed)):
                entry_7.column(i + 1, width=110, anchor='c')
                entry_7.heading(i + 1, text=hed[i])
            for i in range(0, len(data)):
                entry_7.insert("", 'end', values=(data[i]))
            try:
                print(qry_wrkHr)
                cursor.execute(qry_wrkHr)
            except Exception as e:
                print(e)
            else:
                wrkHr=cursor.fetchall()
                for i in wrkHr:
                    tWrkHr+=i[0]
                entry_12.insert(0, f'{tWrkHr}')
                entry_12.config(state="disabled")


    elif (f1eq == '' and f2eq == '' and f3eq != ''):
        qry_st = f"""SELECT * FROM employeeFill WHERE Work = '{f3eq}'"""
        qry_wrkHr = f"""SELECT Work_Hours FROM employeeFill WHERE Work = '{f3eq}'"""
        try:
            print(qry_st)
            cursor.execute(qry_st)
        except Exception as e:
            print(e)
        else:
            data = cursor.fetchall()
            entry_7["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
            hed = ["Name", "Work", "Project Name", "Expected Date", "Remarks", "Start Date", "Strat Time", "End Time",
                   "Work Hours", "Customer Name", "Project Code", "Work Percentage"]
            entry_7['show'] = 'headings'
            for i in range(0, len(hed)):
                entry_7.column(i + 1, width=110, anchor='c')
                entry_7.heading(i + 1, text=hed[i])
            for i in range(0, len(data)):
                entry_7.insert("", 'end', values=(data[i]))
            try:
                print(qry_wrkHr)
                cursor.execute(qry_wrkHr)
            except Exception as e:
                print(e)
            else:
                wrkHr=cursor.fetchall()
                for i in wrkHr:
                    tWrkHr+=i[0]
                entry_12.insert(0, f'{tWrkHr}')
                entry_12.config(state="disabled")


    elif(f1eq != '' and f2eq != '' and f3eq==''):
        qry_st = f"""SELECT * FROM employeeFill WHERE Name = '{f1eq}' AND Project_Code = {f2eq}"""
        qry_wrkHr = f"""SELECT Work_Hours FROM employeeFill WHERE Name = '{f1eq}' AND Project_Code = {f2eq}"""
        try:
            print(qry_st)
            cursor.execute(qry_st)
        except Exception as e:
            print(e)
        else:
            data = cursor.fetchall()
            entry_7["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
            hed = ["Name", "Work", "Project Name", "Expected Date", "Remarks", "Start Date", "Strat Time", "End Time",
                   "Work Hours", "Customer Name", "Project Code", "Work Percentage"]
            entry_7['show'] = 'headings'
            for i in range(0, len(hed)):
                entry_7.column(i + 1, width=110, anchor='c')
                entry_7.heading(i + 1, text=hed[i])
            for i in range(0, len(data)):
                entry_7.insert("", 'end', values=(data[i]))
            try:
                print(qry_wrkHr)
                cursor.execute(qry_wrkHr)
            except Exception as e:
                print(e)
            else:
                wrkHr=cursor.fetchall()
                for i in wrkHr:
                    tWrkHr+=i[0]
                entry_12.insert(0, f'{tWrkHr}')
                entry_12.config(state="disabled")


    elif (f1eq != '' and f2eq == '' and f3eq != ''):
        qry_st = f"""SELECT * FROM employeeFill WHERE Name = '{f1eq}' AND Work = '{f3eq}'"""
        qry_wrkHr = f"""SELECT Work_Hours FROM employeeFill WHERE Name = '{f1eq}' AND Work = '{f3eq}'"""
        try:
            print(qry_st)
            cursor.execute(qry_st)
        except Exception as e:
            print(e)
        else:
            data = cursor.fetchall()
            entry_7["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
            hed = ["Name", "Work", "Project Name", "Expected Date", "Remarks", "Start Date", "Strat Time", "End Time",
                   "Work Hours", "Customer Name", "Project Code", "Work Percentage"]
            entry_7['show'] = 'headings'
            for i in range(0, len(hed)):
                entry_7.column(i + 1, width=110, anchor='c')
                entry_7.heading(i + 1, text=hed[i])
            for i in range(0, len(data)):
                entry_7.insert("", 'end', values=(data[i]))
            try:
                print(qry_wrkHr)
                cursor.execute(qry_wrkHr)
            except Exception as e:
                print(e)
            else:
                wrkHr=cursor.fetchall()
                for i in wrkHr:
                    tWrkHr+=i[0]
                entry_12.insert(0, f'{tWrkHr}')
                entry_12.config(state="disabled")


    elif(f1eq != '' and f2eq != '' and f3eq!=''):
        qry_st = f"""SELECT * FROM employeeFill WHERE Name = '{f1eq}' AND Project_Code = {f2eq} AND Work = '{f3eq}'"""
        qry_wrkHr = f"""SELECT Work_Hours FROM employeeFill WHERE Name = '{f1eq}' AND Project_Code = {f2eq} AND Work = '{f3eq}'"""
        try:
            print(qry_st)
            cursor.execute(qry_st)
        except Exception as e:
            print(e)
        else:
            data = cursor.fetchall()
            entry_7["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
            hed = ["Name", "Work", "Project Name", "Expected Date", "Remarks", "Start Date", "Strat Time", "End Time",
                   "Work Hours", "Customer Name", "Project Code", "Work Percentage"]
            entry_7['show'] = 'headings'
            for i in range(0, len(hed)):
                entry_7.column(i + 1, width=110, anchor='c')
                entry_7.heading(i + 1, text=hed[i])
            for i in range(0, len(data)):
                entry_7.insert("", 'end', values=(data[i]))
            try:
                print(qry_wrkHr)
                cursor.execute(qry_wrkHr)
            except Exception as e:
                print(e)
            else:
                wrkHr=cursor.fetchall()
                for i in wrkHr:
                    tWrkHr=tWrkHr+i[0]
                entry_12.insert(0, f'{tWrkHr}')
                entry_12.config(state="disabled")


    else:
        tkinter.messagebox.showinfo("Status", "Fill The Fields")



def report():
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

    qry_str = """SELECT Name FROM names"""
    try:
        cursor.execute(qry_str)
    except Exception as e:
        print(e)
    else:
        nans=[]
        f=cursor.fetchall()
        for i in f:
            nans.append(i[0])

    wdow = Tk()
    wdow.state('zoomed')
    wdow.geometry("1420x800")
    wdow.configure(bg = "#252525")

    canvas = Canvas(
        wdow,
        bg = "#252525",
        height = 800,
        width = 1420,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_text(
        602.0,
        32.0,
        anchor="nw",
        text="REPORT",
        fill="#FFFFFF",
        font=("Inter", 48 * -1)
    )

    canvas.create_text(
        451.0,
        163.0,
        anchor="nw",
        text=",",
        fill="#FFFFFF",
        font=("Inter", 40 * -1)
    )

    canvas.create_text(
        910.0,
        163.0,
        anchor="nw",
        text=",",
        fill="#FFFFFF",
        font=("Inter", 40 * -1)
    )

    canvas.create_text(
        50.0,
        113.0,
        anchor="nw",
        text="FILTERS :",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )

    canvas.create_text(
        50.0,
        163.0,
        anchor="nw",
        text="Name",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        365.5,
        189.5,
        image=entry_image_2
    )
    entry_2 = ttk.Combobox(
        values=nans,
        font=('Arial 20')
    )
    entry_2.place(
        x=279.0,
        y=163.0,
        width=173.0,
        height=51.0
    )

    canvas.create_text(
        507.0,
        163.0,
        anchor="nw",
        text="Prj Code",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        823.5,
        189.5,
        image=entry_image_4
    )
    entry_4 = ttk.Combobox(
        values=pans,
        font=('Arial 20'),
        postcommand=lambda: entry_4.configure(values=pans)
    )

    entry_4.place(
        x=737.0,
        y=163.0,
        width=173.0,
        height=51.0
    )


    entry_5 = canvas.create_text(
        968.0,
        163.0,
        anchor="nw",
        text="Work",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )


    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        1283.5,
        189.5,
        image=entry_image_6
    )
    entry_6 = ttk.Combobox(
        #state="readonly",
        values=wans,
        font=('Arial 20'),
        postcommand=lambda: entry_6.configure(values=wans)
    )
    entry_6.place(
        x=1197.0,
        y=163.0,
        width=173.0,
        height=51.0
    )

    entry_7 = ttk.Treeview(wdow,selectmode='browse')

    entry_7.place(
        x=49.0,
        y=292.0,
        width=1390.0,
        height=400.0
    )

    entry_8 = canvas.create_text(
        240.0,
        166.0,
        anchor="nw",
        text="=",
        fill="#FFFFFF",
        font=("Inter", 40 * -1)
    )

    entry_9 = canvas.create_text(
        700,
        166.0,
        anchor="nw",
        text="=",
        fill="#FFFFFF",
        font=("Inter", 40 * -1)
    )

    entry_10 = canvas.create_text(
        1160.0,
        166.0,
        anchor="nw",
        text="=",
        fill="#FFFFFF",
        font=("Inter", 40 * -1)
    )

    entry_11=canvas.create_text(
        500.0,
        710.0,
        anchor="nw",
        text="Total Work Hour =",
        fill="#FFFFFF",
        font=("Inter", 36 * -1)
    )
    entry_12=Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font=('Arial 15')
    )
    entry_12.place(
        x=800.0,
        y=710.0,
        width=100.0,
        height=50.0
    )
    entry_12.config(state="disabled")

#########################################################################Buttons
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: GetValue(cursor,entry_2,entry_4,entry_6,entry_7,entry_12),
        relief="flat"
    )
    button_1.place(
        x=1198.0,
        y=238.0,
        width=172.7890625,
        height=32.02598571777344
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: ccl(cursor,wdow,conn),
        relief="flat"
    )
    button_3.place(
        x=1066.0,
        y=710.0,
        width=209.0,
        height=61.0
    )
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: clr(entry_2,entry_4,entry_6,entry_7,entry_12),
        relief="flat"
    )
    button_4.place(
        x=146.0,
        y=710.0,
        width=209,
        height=61
    )
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: sel1(cursor,entry_2),
        relief="flat"
    )
    button_5.place(
        x=280.0,
        y=238.0,
        width=172.78912353515625,
        height=32.02598571777344
    )
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: sel2(cursor,entry_2,entry_4),
        relief="flat"
    )
    button_6.place(
        x=738.0,
        y=238.0,
        width=172.78912353515625,
        height=32.02598571777344
    )
    #wdow.resizable(False, False)
    wdow.mainloop()