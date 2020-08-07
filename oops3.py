from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox,filedialog


class Mainframe2:

    def customcan(self, framename, w, h, color, xc, yc):
        self.c1 = Canvas(framename, width=w, height=h, bg=color, bd=0, highlightthickness=0)
        self.c1.place(x=xc, y=yc)
        return self.c1

    def packedCanvas(self,frameno,w,h,bgc,side):
        packed_can=Canvas(frameno,bg=bgc,width=w,height=h)
        packed_can.pack(side=side)
        packed_can.pack(side=side)
        return packed_can

    def image(self, path, x, y):
        self.pic = PhotoImage(file=path)
        self.picofcan = self.c1.create_image(x, y, image=self.pic, anchor=NW)
        return self.picofcan

    def line(self, xs, ys, xf, yf, color, w):
        self.linesoncan = self.c1.create_line(xs, ys, xf, yf, fill=color, width=w)

    def text(self, x, y, name, fonts, color):
        self.c1.create_text(x, y, text=name, font=fonts, fill=color)

    def custombuttons(self, frameno, name, w, h, action, xc, yc, **kwargs):
        kdic = kwargs
        if kdic != {}:
            self.b = Button(frameno, text=name, width=w, height=h, command=action, bg=kdic['bg'], fg=kdic['fg'])
        else:
            self.b = Button(frameno, text=name, width=w, height=h, command=action)
        self.b.place(x=xc, y=yc)
        return self.b

    def customlabels(self, frameno, name, fonts, bgc, xc, yc, *args, **kwargs):
        style = kwargs
        if style == {}:
            wh = args
            if wh == ():
                self.l1 = Label(frameno, text=name, font=fonts, bg=bgc)
            else:
                w = wh[0]
                h = wh[1]
                self.l1 = Label(frameno, text=name, width=w, height=h, font=fonts, bg=bgc)
        else:
            wh = args
            if wh == ():
                self.l1 = Label(frameno, text=name, font=fonts, bg=bgc, fg=style['fg'])
            else:
                w = wh[0]
                h = wh[1]
                self.l1 = Label(frameno, text=name, width=w, height=h, font=fonts, bg=bgc, fg=style['fg'])
        self.l1.place(x=xc, y=yc)
        return self.l1

    def emailentry(self, frameno, xc, yc, *args):
        em = args
        self.emailvar = StringVar()
        if em != ():
            self.emen = Entry(frameno, width=em[0], textvariable=self.emailvar)
        else:
            self.emen = Entry(frameno, textvariable=self.emailvar)
        self.emen.place(x=xc, y=yc)

    def userEntry(self, frameno, xc, yc, *args):
        t = args
        self.valname = StringVar()
        if t != ():
            self.en1 = Entry(frameno, width=t[0], textvariable=self.valname)
        else:
            self.en1 = Entry(frameno, textvariable=self.valname)
        self.en1.place(x=xc, y=yc)

    def userintentry(self, frameno, xc, yc, *args):
        t2 = args
        self.intvalname = StringVar()
        if t2 != ():
            self.en23 = Entry(frameno, width=t2[0], textvariable=self.intvalname)
        else:
            self.en23 = Entry(frameno, textvariable=self.intvalname)
        self.en23.place(x=xc, y=yc)

    def customframes(self, frameno, w, h, color, xc, yc):
        self.f1 = Frame(frameno, width=w, height=h, bg=color)
        self.f1.place(x=xc, y=yc)
        return self.f1

    def customcombobox(self, frameno, name, v, w, xc, yc):
        self.c1 = Combobox(frameno, values=v, width=w, state='readonly')
        self.c1.set(name)
        self.c1.place(x=xc, y=yc)
        return self.c1

    def passwordentry(self, frameno, xc, yc, *args):
        t = args
        if t != ():
            self.en = Entry(frameno, show='*', width=t[0])
        else:
            self.en = Entry(frameno)
        self.en.place(x=xc, y=yc)

    def packedFrame(self, frameno, w, h, color, side, **kwargs):
        adic = kwargs
        self.f1 = Frame(frameno, width=w, height=h, bg=color)
        if adic == {}:
            self.f1.pack(side=side)
        else:
            self.f1.pack(side=side, fill=adic['fill'])
        return self.f1

    def txtarea(self, frameno, w, h, xc, yc, **kwargs):
        state = kwargs
        self.t1 = Text(frameno, width=w, height=h, wrap=WORD, padx=5, pady=5)
        if state == {}:
            pass
        else:
            self.t1.config(state=state['state'])
        self.t1.place(x=xc, y=yc)
        return self.t1

    def packedlabels(self, frameno, name, w, h, color, *args):
        k = args
        self.l1 = Label(frameno, text=name, width=w, height=h, bg=color)
        if k == ():
            self.l1.pack()
        else:
            side = k[0]
            fill = k[1]
            self.l1.pack(side=side, fill=fill)
        return self.l1

    def genralentry(self, frameno, xc, yc, *args):
        t3 = args
        self.em = StringVar()
        if t3 != ():
            self.enem = Entry(frameno, width=t3[0], textvariable=self.em)
        else:
            self.enem = Entry(frameno, textvariable=self.em)
        self.enem.place(x=xc, y=yc)

    #-------------------------------------------------  TRACKER ENRTY   -------------------------------------------

    def track_entry(self,frameno,xc,yc,fun,**kwargs):
        tempdic=kwargs
        self.tracker=StringVar()
        if tempdic=={}:
            self.t_ent=Entry(frameno,textvariable=self.tracker)
        elif len(tempdic)==1:
            fs=tempdic['fs']
            self.t_ent=Entry(frameno,textvariable=self.tracker,font=fs)

        self.t_ent.place(x=xc,y=yc)
        self.tracker.trace('w',lambda name,index,mode:fun())
        return self.t_ent
    #--------------------------------------------------------------------------------------------------------------
    def set_tracker_entry(self,value):
        self.tracker.set(value)

    #-------------------------------------------------  LIST   -------------------------------------------

    def customListBox(self,frameno,w,h,side,*args):
        coordinates_specifier=args
        self.lBox = Listbox(frameno, width=w, height=h, selectmode=SINGLE)
        if len(coordinates_specifier)==0:
            self.lBox.pack(side=side)
            return self.lBox
        else:
            self.lBox.pack(side=side,fill=coordinates_specifier[0],extend=coordinates_specifier[1])
            return self.lBox

    def listBox_values(self,valList):
        self.ind_counter = 1
        for val in valList:
            self.lBox.insert(self.ind_counter,val)
            self.ind_counter+=1

    def get_List_selected(self):
        self.clicked_items=self.lBox.curselection()
        if self.clicked_items !=():
            return [self.lBox.get(val) for val in self.clicked_items]
        else:
            return -1

    def delete_list_selected(self):
        self.target=self.lBox.curselection()
        if self.target !=():
            self.lBox.delete(self.target)
            return 1
        else:
            return -1
    #----------------------------------------------- TOGGLE BUTTON--------------------------------------------------------

    switch_status = 0

    def toggle_button(self,frameno,xc,yc,value,onclr,offclr,togglename0='',togglename1='',onclick=None):
        global switch_status
        self.toggleID=0
        switch_status = not value
        toggle=Canvas(frameno,bg=offclr,width=70,height=20,highlightthickness=0)
        toggle.place(x=xc,y=yc)
        tog_switch=Canvas(toggle,width=35,height=18,bg='white',highlightthickness=0)
        tog_switch.place(x=1,y=1)
        togtext = tog_switch.create_text(8, 4, text=togglename0, font='none 7', anchor=NW, fill=offclr)

        def onclick_ON(event=''):
            global switch_status
            if switch_status == 0:
                tog_switch.place(x=34, y=1)
                toggle.config(bg=onclr)
                tog_switch.itemconfig(togtext, text=togglename1, fill=onclr)
                switch_status = 1
                self.toggleID=1
                onclick() if onclick != None else -1
            else:
                tog_switch.place(x=1, y=1)
                toggle.config(bg=offclr)
                tog_switch.itemconfig(togtext, text=togglename0, fill=offclr)
                switch_status = 0
                self.toggleID=0
                onclick() if onclick != None else -1

        onclick_ON()
        toggle.bind('<Button-1>', onclick_ON)
        tog_switch.bind('<Button-1>', onclick_ON)
        return toggle,tog_switch,
    def get_toggle_status(self):
        return self.toggleID


    #--------------------------------------------------------------------------------------------------------------

    #------------------------------------------------   T A B S    --------------------------------------------------------------

    def customTab_Square(self,frameno,w,h,bgc,txtclr,name,fonts,xc,yc,txc,tyc,bclr,barwidth):
        self.tabcan_ = Canvas(frameno, width=w, height=h, bg=bgc,  cursor='hand2')
        self.tabcan_.place(x=xc, y=yc)
        self.tabcan_.create_text(txc, tyc, text=name, fill=txtclr, font=fonts,anchor=NW)
        self.bar=self.tabcan_.create_line(0, h, w+2, h,fill=bclr,width=barwidth)
        return self.tabcan_,self.bar,

    def customTab_Polygon(self,frameno,bgc,txtclr,name,fonts,xc,yc,txc,tyc,bclr,barwidth,outline,**polyCoordinates):
        px0, py0, px1, py1, px2, py2, px3, py3=polyCoordinates['coords']
        tabcan1 = Canvas(frameno, width=px3, height=py0,bg=bgc,cursor='hand2',highlightthickness=0)
        tabcan1.place(x=xc,y=yc)
        tabcan1.create_polygon([px0, py0, px1, py1, px2, py2, px3, py3], fill=bgc, outline=outline)
        tabcan1.create_text(txc, tyc, text=name,font=fonts,fill=txtclr)
        negation=3 if barwidth>5 else 2
        self.polybar=tabcan1.create_line(negation, py0, px3-negation, py0,fill=bclr,width=barwidth)
        return tabcan1,self.polybar,



    #--------------------------------------------------------------------------------------------------------------

    def getuserentry(self):
        self.userdata = self.valname.get().title()
        return self.userdata

    def getpassword(self):
        self.passdata = self.en.get()
        return self.passdata

    def gettext(self):
        self.txtdata = self.t1.get(1.0, END)
        return self.txtdata

    def getcombodata(self):
        self.choice = self.c1.get()
        return self.choice

    def getint(self):
        self.intdat = self.intvalname.get()
        return self.intdat

    def getgenralentrydata(self):
        self.emmeta = self.em.get()
        return self.emmeta

    def getemail(self):
        self.emdat = self.emailvar.get().endswith('@gmail.com')
        if self.emdat == True:
            return self.emen.get()
        else:
            return False



    # clearing the data

    def clearuserentry(self):
        self.en1.delete(0, END)

    def clearpassword(self):
        self.en.delete(0, END)

    def cleartext(self):
        self.t1.delete(1.0, END)

    def clearcombo(self):
        self.c1.delete(0, END)

    def ex(self):
        meta = self.c1.get()
        self.c1.bind('<<ComboboxSelected>>')
        return meta

    def cleangenral(self):
        self.enem.delete(0, END)

    def clearinten(self):
        self.en23.delete(0, END)

    # setting values
    def setuserentry(self, val):
        self.valname.set(val)

    def setintegerentry(self, valofint2):
        self.intvalname.set(valofint2)

    def setgenraluser(self, valofint):
        self.em.set(valofint)

    def setemail(self, emaildata):
        self.emailvar.set(emaildata)

#---------------------------------------------------C A N V A S BUTTONS-------------------------------------------------

def can_but(frno,name,clr,fg,fontstyle,xc,yc,fun,w,h,txtalignX,txtalignY):
    globalobj=Mainframe2()
    projectbut = globalobj.customcan(frno, w, h,clr, xc, yc)
    butname=projectbut.create_text(txtalignX, txtalignY, text=name, font=fontstyle, fill=fg)
    if fun==None:
        pass
    else:
        projectbut.bind('<Button-1>', lambda event:fun())
    return projectbut,butname,




