from pathlib import Path
from tkinter import *
from tkcalendar import DateEntry
from tkinter import ttk
import tkinter.messagebox
import sys
import pypyodbc as odbc
from datetime import datetime, timedelta
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
#from prettytable import PrettyTable

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"F:\Tia Prj\Applicatn\assets\frame4")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def prjdet(cursor, cn, pttl, pid):
    pttl.config(state="normal")
    cn.config(state="normal")
    id = pid.get()
    if (id != ''):
        cn.config(state="normal")
        pttl.config(state="normal")
        pttl.delete(0, 'end')
        cn.delete(0, 'end')
        pjtitle = ''
        cname = ''
        cursor.execute(f"SELECT Project_Name FROM project where Project_Code = {id};")
        fech = cursor.fetchone()
        for i in fech:
            pjtitle += i

        pttl.insert(0, f'{pjtitle}')
        pttl.config(state="disabled")

        cursor.execute(f"SELECT Customer_Name FROM project where Project_Code = {id};")
        fch = cursor.fetchone()
        for i in fch:
            cname += i
        cn.insert(0, f'{cname}')
        cn.config(state="disabled")
        del id
        del pjtitle
        del cname
    else:
        tkinter.messagebox.showinfo("Status", "Select Project Code")


# Submit Fun#
def submitFunction(cursor, nam, wrk, cal, tm, et, wt, pid, pttl, cn, exd, wp, rm):
    name = nam.get()
    # cursor.execute(f"SELECT Start_Date FROM employeeFill WHERE Name = '{name}'")
    # ddtl=cursor.fetchall()
    work = wrk.get()
    sdate = cal.get_date()
    stime = tm.get()
    etime = et.get()
    wktym = wt.get()
    id = pid.get()
    title = pttl.get()
    cname = cn.get()
    exdate = exd.get_date()
    wrkper = wp.get()
    remark = rm.get()
    if (
            name != '' and work != '' and sdate != '' and stime != '' and exdate != '' and etime != '' and wktym != '' and cname != '' and id != '' and title != '' and wrkper != ''):
        insert_string = f"""
            INSERT INTO employeeFill
            VALUES('{name}','{work}','{title}','{exdate}','{remark}','{sdate}','{stime}','{etime}','{wktym}','{cname}',{id},{wrkper})
        """
        try:
            print(insert_string)
            cursor.execute(insert_string)
        except Exception as e:
            cursor.rollback()
            print(e)
            print('rolled back')
            tkinter.messagebox.showinfo("Status", "Fill the details correctly")
        else:
            print('Inserted Successfully')
            #tkinter.messagebox.showinfo("Status", "Successfully Updated")
            pttl.config(state="normal")
            cn.config(state="normal")
            wt.config(state="normal")
            nam.set('')
            wrk.set('')
            wt.delete(0, 'end')
            pid.set('')
            pttl.delete(0, 'end')
            cn.delete(0, 'end')
            exd.delete(0, 'end')
            wp.delete(0, 'end')
            rm.delete(0, 'end')

            qry_str = f"""SELECT * FROM employeeFill WHERE Name ='{name}'"""
            try:
                print(qry_str)
                cursor.execute(qry_str)
                fch = cursor.fetchall()

            except Exception as e:
                print(e)
            else:
                disp = Tk()
                #disp.geometry('750x500')
                disp.title("Your Details")
                trv = ttk.Treeview(disp, selectmode='browse')
                trv.grid(row=1, column=1)

                # number of columns
                trv["columns"] = ("1", "2", "3", "4", "5","6","7","8","9","10","11","12")
                hed=["Name","Work","Project Name","Expecting Date","Remarks","Start Date","Strat Time","End Time","Work Hours","Customer Name","Project Code","Work Percentage"]
                # Defining heading
                trv['show'] = 'headings'

                # Headings
                # respective columns
                for i in range(0,len(hed)):
                    trv.column(i+1, width=110, anchor='c')
                    trv.heading(i+1, text=hed[i])

                # getting data from MySQL student table
                #r_set = my_conn.execute('''SELECT * from student LIMIT 0,10''')
                for i in range(0,len(fch)):
                    trv.insert("", 'end',values=(fch[i]))

                vs = ttk.Scrollbar(disp, orient="vertical", command=trv.yview)  # V Scrollbar
                trv.configure(yscrollcommand=vs.set)  # connect to Treeview
                vs.grid(row=1, column=2, sticky='ns')
                hs = ttk.Scrollbar(disp, orient="horizontal", command=trv.yview)  # h Scrollbar
                trv.configure(yscrollcommand=vs.set)  # connect to Treeview
                hs.grid(row=2, column=1, sticky='ns')
                btn = Button(disp,text="Close",command=lambda: disp.destroy())
                btn.grid(row=3,column=1)
                disp.mainloop()
    else:
        tkinter.messagebox.showinfo("Status", "Need to fill the Mandatory Fields")


def Exit(wi, conn, cursor):
    wi.destroy()
    cursor.commit()
    cursor.close()
    if conn.connected == 1:
        print('Connection Closed')
        conn.close()


def wrktm(tm, et, wt):
    wt.config(state="normal")
    wt.delete(0, 'end')
    st = tm.get()
    ent = et.get()
    format_ = '%H:%M:%S'
    lunch = ['13:00:00', '13:30:00']
    start_dt = datetime.strptime(st, format_)
    end_dt = datetime.strptime(ent, format_)
    lunch_start_dt = datetime.strptime(lunch[0], format_)
    lunch_end_dt = datetime.strptime(lunch[1], format_)
    # print('st',int(start_dt.strftime("%H")))
    # print('et',int(end_dt.strftime("%H")))
    # print('ls',int(lunch_start_dt.strftime("%H")))
    # print('le',int(lunch_end_dt.strftime("%H")))
    if (st == ent):
        tkinter.messagebox.showinfo("Status", "Check the Start and End Time")
    else:
        if (int(start_dt.strftime("%H")) < int(lunch_start_dt.strftime("%H")) and int(end_dt.strftime("%H")) > int(
                lunch_end_dt.strftime("%H"))):
            lunch_duration = lunch_end_dt - lunch_start_dt
            print('ld', lunch_duration)
            elapsed = end_dt - start_dt - lunch_duration
        else:
            elapsed = end_dt - start_dt
            lunch_duration = timedelta(0)
            print('ld', lunch_duration)

        # elapsed = end_dt - start_dt - lunch_duration
        hours = elapsed.seconds / 3600
        print(hours)
        wt.insert(0, f'{float(hours)}')
        wt.config(state="disabled")


#def MainEntry():
# CurrentTime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# SQL Connection #
DRIVER = 'SQL Server'
SERVER_NAME = 'MIDHUN\SQLEXPRESS'
DATABASE_NAME = 'workProgress'

conn_string = f"""
        Driver={{{DRIVER}}};
        Server={SERVER_NAME};
        Database={DATABASE_NAME};
        Trust_Connection=yes;
    """
try:
    conn = odbc.connect(conn_string)
    print('connecting...')
except Exception as e:
    print(e)
    print('Task Terminated')
    sys.exit()
else:
    print('Success')
    cursor = conn.cursor()

### Fetch details for UI part ###
cursor.execute("SELECT Name FROM names;")
rows = cursor.fetchall()
name_list = []
for i in rows:
    name_list.append(i[0])

cursor.execute("SELECT Work FROM works;")
rows = cursor.fetchall()
work_list = []
for i in rows:
    work_list.append(i[0])

cursor.execute("SELECT Project_Code FROM project;")
rows = cursor.fetchall()
pjid_list = []
for i in rows:
    pjid_list.append(i[0])

wi = Tk()
wi.title("Fill Details")
wi.state('zoomed')
wi.configure(bg="#252525")

ca = Canvas(
    wi,
    bg="#252525",
    height=841,
    width=1440,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

ca.place(x=0, y=0)
ca.create_text(
    591.0,
    21.0,
    anchor="nw",
    text="ENTRY FORM",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = ca.create_image(
    556.0,
    135.5,
    image=entry_image_1
)
nam = ttk.Combobox(
    state="readonly",
    values=name_list,
    font=('Georgia 20')
)
nam.place(
    x=403.0,
    y=112.0,
    width=306.0,
    height=45.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = ca.create_image(
    556.0,
    316.5,
    image=entry_image_2
)
wrk = ttk.Combobox(
    state="readonly",
    values=work_list,
    font=('Georgia 20')
)
wrk.place(
    x=403.0,
    y=293.0,
    width=306.0,
    height=45.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = ca.create_image(
    1246.5,
    406.5,
    image=entry_image_3
)
et = Entry(wi,
           bd=0,
           bg="#FFFFFF",
           fg="#000716",
           highlightthickness=0,
           font=('Georgia 20')
           )
et.insert(0, f'{current_time}')
et.place(
    x=1093.0,
    y=383.0,
    width=307.0,
    height=45.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = ca.create_image(
    556.0,
    591.5,
    image=entry_image_4
)
pid = ttk.Combobox(
    state="readonly",
    values=pjid_list,
    font=('Georgia 20')
)
pid.place(
    x=403.0,
    y=568.0,
    width=306.0,
    height=45.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = ca.create_image(
    556.0,
    681.5,
    image=entry_image_5
)
pttl = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=('Georgia 20')
)
pttl.place(
    x=403.0,
    y=658.0,
    width=306.0,
    height=45.0
)
pttl.config(state='disabled')
entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = ca.create_image(
    556.0,
    226.5,
    image=entry_image_6
)
wp = Spinbox(wi, from_=0, to=100, font=('Georgia 20'))
wp.place(
    x=403.0,
    y=203.0,
    width=306.0,
    height=45.0
)

ca.create_text(
    39.0,
    112.0,
    anchor="nw",
    text="Name                     :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    39.0,
    203.0,
    anchor="nw",
    text="Work Percentage  :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    39.0,
    658.0,
    anchor="nw",
    text="Project Title           :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    39.0,
    293.0,
    anchor="nw",
    text="Work                      :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    730.0,
    383.0,
    anchor="nw",
    text="End Time               :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    39.0,
    568.0,
    anchor="nw",
    text="Project Code         :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = ca.create_image(
    1246.5,
    135.5,
    image=entry_image_7
)
cal = DateEntry(wi, width=20, font=('Arial 15'))
cal.place(
    x=1093.0,
    y=112.0,
    width=307.0,
    height=45.0
)

entry_image_8 = PhotoImage(
    file=relative_to_assets("entry_8.png"))
entry_bg_8 = ca.create_image(
    556.0,
    406.5,
    image=entry_image_8
)
tm = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=('Georgia 20')
)
tm.insert(0, f'{current_time}')
tm.place(
    x=403.0,
    y=383.0,
    width=306.0,
    height=45.0
)

entry_image_9 = PhotoImage(
    file=relative_to_assets("entry_9.png"))
entry_bg_9 = ca.create_image(
    1246.5,
    497.0,
    image=entry_image_9
)
wt = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=('Georgia 20')
)
wt.place(
    x=1093.0,
    y=473.0,
    width=307.0,
    height=46.0
)
wt.config(state='disabled')
entry_image_10 = PhotoImage(
    file=relative_to_assets("entry_10.png"))
entry_bg_10 = ca.create_image(
    1246.5,
    681.5,
    image=entry_image_10
)
cn = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=('Georgia 20')
)
cn.place(
    x=1093.0,
    y=658.0,
    width=307.0,
    height=45.0
)
cn.config(state="disabled")
entry_image_11 = PhotoImage(
    file=relative_to_assets("entry_11.png"))
entry_bg_11 = ca.create_image(
    1246.5,
    316.5,
    image=entry_image_11
)
exd = DateEntry(wi, width=20, font=('Arial 15'))
exd.place(
    x=1093.0,
    y=293.0,
    width=307.0,
    height=45.0
)

entry_image_12 = PhotoImage(
    file=relative_to_assets("entry_12.png"))
entry_bg_12 = ca.create_image(
    1246.5,
    226.5,
    image=entry_image_12
)
rm = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=('Georgia 20')
)
rm.place(
    x=1093.0,
    y=203.0,
    width=307.0,
    height=45.0
)

ca.create_text(
    730.0,
    112.0,
    anchor="nw",
    text="Date                      :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    730.0,
    203.0,
    anchor="nw",
    text="Remarks                :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    730.0,
    293.0,
    anchor="nw",
    text="Expected Date      :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    39.0,
    383.0,
    anchor="nw",
    text="Start Time             :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    730.0,
    473.0,
    anchor="nw",
    text="Work Hours           :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)

ca.create_text(
    730.0,
    658.0,
    anchor="nw",
    text="Customer Name   :",
    fill="#FFFFFF",
    font=("Inter", 40 * -1)
)
#############################################Button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: wrktm(tm, et, wt),
    relief="flat"
)
button_1.place(
    x=249.29168701171875,
    y=473.4080505371094,
    width=306.593505859375,
    height=51.02873611450195
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: prjdet(cursor, cn, pttl, pid),
    relief="flat"
)
button_2.place(
    x=940.1097412109375,
    y=563.6896362304688,
    width=306.593505859375,
    height=51.02873229980469
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: submitFunction(cursor, nam, wrk, cal, tm, et, wt, pid, pttl, cn, exd, wp, rm),
    relief="flat"
)
button_3.place(
    x=248.0,
    y=744.0,
    width=352.90106201171875,
    height=75.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Exit(wi, conn, cursor),
    relief="flat"
)
button_4.place(
    x=840.0989379882812,
    y=744.0,
    width=352.90106201171875,
    height=75.0
)
# wi.resizable(False, False)
wi.mainloop()
