from backendComponents import (extDatabase, AdvanceOperation, reset_counter, UserConfig,
                               autoSense_confirmation, aSError, redundent_files, ask,
                               add_New_EXTENSION, delete_file_type, del_eXtensions)
from oops3 import * # this module contains all the gui components in a class
from directoryManager import *
from ctypes import windll

e=windll.shcore.SetProcessDpiAwareness(2) # For Setting DPI according to screen resolution

""" Variables and lists """
update_list_FE=[]
themecolor = '#303030'
closing_counter = 0
move_redundent=[]
_ASPATH=[]

bodycolor = '#1e1e1e'
fonttxt = 'Ebrima'
terminator = 0
file_types = extDatabase('','ft')


autosense_win_manager = 0 # Ensures that only one toplevel window appear at once.

def enabel_AutoSense():

    """ This function shows the option panel for yes and cancel to activate the auto sense service """

    global autosense_win_manager
    if not autosense_win_manager:
        autosense_win_manager = 1
        arguList=[]
        autoSense_panel = Toplevel()
        width = 700
        height = 225
        x = (autoSense_panel.winfo_screenwidth() // 2) - (width // 2)
        y = (autoSense_panel.winfo_screenheight() // 2) - (height // 2)
        autoSense_panel.geometry(f'{width}x{height}+{x}+{y}')
        autoSense_panel.focus()
        askglobal_obj = Mainframe2()
        autoSense_panel.title('AutoSense Feature')
        autoSense_panel.focus()
        autoSense_panel.resizable(0,0)
        askcan = askglobal_obj.customcan(autoSense_panel, width, height, 'white', 0, 0)
        pic=PhotoImage(file=autoSense_Enable_graphic)
        askcan.create_image(20,20,image=pic,anchor=NW)
        askcan.create_text(200, 20, text='AutoSense', anchor=NW, font='Ebrima 20')
        askcan.create_line(200,66,450,66,fill='#cdcdcd')
        askcan.create_text(200, 80, text='AutoSense enables Automatic background sorting whenever\na new file arrives in selected directory.', anchor=NW)
        askcan.create_text(200, 120, text='Just select the directory on which you want to apply AutoSense\nand Software will take care of rest.', anchor=NW)
        def cancelling():
            global autosense_win_manager
            autosense_win_manager = 0
            arguList.insert(0,0)
            autoSense_panel.quit()
            autoSense_panel.destroy()

        b1=askglobal_obj.custombuttons(askcan,'Cancel',15,1,cancelling,450,180)
        b1.config(borderwidth=2,relief='groove',cursor="hand2")
        def turningONN():
            arguList.insert(0,1)
            autoSense_panel.quit()
            autoSense_panel.destroy()
        b2=askglobal_obj.custombuttons(askcan,'Enable',15,1,turningONN,300,180)
        autoSense_panel.protocol('WM_DELETE_WINDOW',cancelling)
        b2.config(borderwidth=2,relief='groove',cursor="hand2")
        autoSense_panel.mainloop()
        return arguList[0]


def proceed():

    """   The main Function for root window   """

    global terminator
    root=Tk()
    width = 900
    height=650
    butclr='white'
    deadlink='#cdcdcd'
    root.config(background=bodycolor)

    #
    logo_path=icon_logo

    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight()//2)-(height//2)-20
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.resizable(False,False)
    place=' '*100
    root.title(f'{place} fileSWAP')
    root.iconbitmap(logo_path)

    root.iconbitmap(root,logo_path)


    root.focus()
    globalobj=Mainframe2()

    rootCanvas=globalobj.customcan(root,width-3,height-23,bodycolor,0,1)
    footerCanvas=globalobj.customcan(root,897,37,bodycolor,0,height-65)

    # -----------------------------------------------------  EXTENSIONS MANAGER FUNC.    ---------------------------------------------

    def eXTENSIONS_MANAGER():

        """   This function is the extension manager GUI panel thru which you can add, delete or see what types of extensions
           are available.    """

        sglobal_obj = Mainframe2()
        sobj1 = Mainframe2()
        sobj2 = Mainframe2()
        sobj3 = Mainframe2()

        sroot = Toplevel()
        width = 800
        height = 600

        sroot.title('Extensions Manager')
        sroot.focus()
        sroot.resizable(0,0)
        x = (sroot.winfo_screenwidth() // 2) - (width // 2)
        y = (sroot.winfo_screenheight() // 2) - (height // 2)

        sroot.geometry(f'{width}x{height}+{x}+{y}')

        sroot_can = sglobal_obj.customcan(sroot, width-6, height-6, '#303030', 0, 0)
        sroot_can.config(highlightthickness=3, highlightbackground='white')

        # ----------------------------------------------------   ADDING NEW EXTENSION    ---------------------------------------

        sroot_can.create_text(10, 20, text='Add New Extension >', anchor=NW, font='Ebrima', fill='white')
        sroot_can.create_line(210, 35, 630, 35, fill='white')

        sroot_can.create_text(30, 60, text='Select Ext Type : ', anchor=NW, fill='white')
        sroot_can.create_text(360, 60, text='-> Select the File type by drop down from Previously added.', anchor=NW,
                              fill='white')
        extCombo = sobj1.customcombobox(sroot, '-', ['-'] + extDatabase(0, 0), 23, 130, 58)

        sroot_can.create_text(30, 100, text='Ext. Name : ', anchor=NW, fill='white')
        sroot_can.create_text(360, 95, text='-> Give a name to the Extension (e.g : Image, video, Zip.. etc.)',
                              anchor=NW, fill='white')
        sroot_can.create_text(360, 115, text='                (Leave Empty if Above option is selected.)', anchor=NW,
                              fill='yellow')
        nameVar_xt=StringVar()
        extName = Entry(sroot_can, highlightthickness=1, highlightbackground='black', width=26,textvariable=nameVar_xt)
        extName.place(x=130, y=98)

        sroot_can.create_text(30, 140, text='Extension : ', anchor=NW, fill='white')
        sroot_can.create_text(360, 140, text='-> Specify the Syntax of Extension (e.g : .png, .zip, .mp4... etc.)',
                              anchor=NW, fill='white')
        xtVar=StringVar()
        eXtension = Entry(sroot_can, highlightthickness=1, highlightbackground='black', width=26,textvariable=xtVar)
        eXtension.place(x=130, y=138)

        # ----------------------------------------------------   DISPLAY EXTENSIONS    ---------------------------------------

        sroot_can.create_text(10, 240, text='Manage Extensions >', anchor=NW, font='Ebrima', fill='white')
        sroot_can.create_line(210, 255, 630, 255, fill='white')

        sroot_can.create_text(30, 283, text='File Type :', anchor=NW, fill='white')
        sobj2.customcombobox(sroot_can, '-', ['-'] + extDatabase(0, 0), 25, 110, 280)

        list_holder = sglobal_obj.customframes(sroot_can, 300, 150, 'red', 370, 290)
        y_scrol = Scrollbar(list_holder)
        y_scrol.pack(side=RIGHT, fill=Y)

        sroot_can.create_text(400, 265, text='Available Extensions', anchor=NW, font='none 10 bold underline',
                              fill='white')

        listbox = sobj3.customListBox(list_holder, 30, 10, LEFT)
        listbox.config(justify=CENTER, yscrollcommand=y_scrol.set, highlightthickness=1, highlightbackground='white',
                       fg='white', bg='#303030')
        y_scrol.config(command=listbox.yview)

        def insert_list_values():
            listbox.delete(0, 'end')
            selected_type = sobj2.getcombodata()
            if selected_type != '-':
                extFromDatabase = extDatabase(selected_type, 'e')
                sobj3.listBox_values(extFromDatabase)
            else:
                messagebox.showwarning('Type Select', 'No file type is selected to show extensions.',parent=sroot)

        def resetEntries():
            nameVar_xt.set('')
            xtVar.set('')
            extCombo.set('-')

        def add_new_ext():
            xname = nameVar_xt.get()
            xtype = xtVar.get()
            previousXtyp=sobj1.getcombodata()

            if len(xname)==0 and len(xtype)==0 and previousXtyp=='-':
                messagebox.showerror('Empty Type', 'No Specifications are given to proceed.', parent=sroot)
            elif len(xname) !=0 and len(xtype) !=0 and previousXtyp=='-':
                add_New_EXTENSION(xname, xtype,sroot)
            elif len(xname)==0 and len(xtype) !=0 and previousXtyp !='-':
                add_New_EXTENSION(previousXtyp, xtype,sroot,caller='update')
            elif len(xname) != 0 and len(xtype) != 0 and previousXtyp != '-':
                messagebox.showerror('Empty Type', 'If you have choosen the File type from the dropdown then leave the Name EMPTY or Vice Versa.\n\n'
                                                   'All Three Entry can not be filled at the same time.', parent=sroot)
            else:
                messagebox.showerror('Empty Type', 'Proper Specifications are not given to proceed.', parent=sroot)

        def del_from_database():
            sel_typ = sobj2.getcombodata()
            ext_selected = sobj3.get_List_selected()
            if sel_typ != '-':
                if ext_selected != -1:
                    user_response = messagebox.askokcancel('Confirmation',
                                                           f'Selected extension with name : {ext_selected} will be deleted.',
                                                           parent=sroot)
                    if user_response == 1:
                        del_eXtensions(sel_typ, ext_selected[0],sroot)
                else:
                    messagebox.showerror('Not Selected', ' There is no ext selected to delete.', parent=sroot)
            else:
                messagebox.showerror('Database Error', 'There is error to delete this extension without its filetype.',
                                     parent=sroot)
        def permanentDelete():
            sel_typ = sobj2.getcombodata()
            if sel_typ !='-':
                user_response=messagebox.askokcancel('Confirmation','All the extensions under selected file type will also be deleted permanently.',parent=sroot)
                if user_response==1:
                    delete_file_type(sel_typ,sroot)
            else:
                messagebox.showerror('Not Selected', ' No File Type selected to delete.', parent=sroot)
        #
        sb1 = sglobal_obj.custombuttons(sroot_can, 'Add', 10, 1, add_new_ext, 30, 190)
        sb2 = sglobal_obj.custombuttons(sroot_can, 'Reset', 10, 1, resetEntries, 135, 190)
        sb3 = sglobal_obj.custombuttons(sroot_can, 'See', 10, 1, insert_list_values, 30, 400)
        sb4 = sglobal_obj.custombuttons(sroot_can, 'Delete', 10, 1, del_from_database, 135, 400, fg='white', bg='red')
        sb5 = sglobal_obj.custombuttons(sroot_can, 'Delete File type', 20, 1, permanentDelete, 30, 450, fg='white',bg='black')

        sb1.config(borderwidth=2,relief='ridge')
        sb2.config(borderwidth=2,relief='ridge')
        sb3.config(borderwidth=2,relief='ridge')
        sb4.config(borderwidth=2,relief='ridge')
        sb5.config(borderwidth=2,relief='ridge')

        sroot.mainloop()

    #=============================================================  MAIN MENU   ==================================================================
    user_obj=UserConfig()
    def changecolor(t,c=404):
        """    This function changes the highlighted lines around the window. You can chech this in Backlit option in menu of gui.     """
        if c==404:
            rootCanvas.config(highlightthickness=t)
            footerCanvas.config(highlightthickness=1, highlightbackground='steelblue')
            user_obj.update_val('edge','steelblue')
        else:
            rootCanvas.config(highlightthickness=t,highlightbackground=backlit_colors[c])
            footerCanvas.config(highlightthickness=1, highlightbackground=backlit_colors[c])
            user_obj.update_val('edge',backlit_colors[c])

    _edge_clr=user_obj.get_val('edge')
    print(_edge_clr)
    if _edge_clr=='steelblue':
        rootCanvas.config(highlightthickness=0, highlightbackground=_edge_clr)
        footerCanvas.config(highlightthickness=1, highlightbackground=_edge_clr)
    else:
        rootCanvas.config(highlightthickness=1, highlightbackground=_edge_clr)
        footerCanvas.config(highlightthickness=1, highlightbackground=_edge_clr)

    space=' '*8
    as_status,as_path=user_obj.get_val('autosense','AS')
    print(as_status,as_path)

    def activatingAS(caller):
        """Ensuring AS is activated """
        global terminator

        if terminator==0:
            permission=enabel_AutoSense()
            if permission==1:
                terminator=1
                status=autoSence()
                if status==1:
                    messagebox.showinfo('Activated','AutoSense Service is Successfully activated on selected directory.\n\n'
                                                    'Minimise the software , we will not consume much Power.',parent=root)
                    s=asstatadv[0]
                    s.config(text='AutoSense is Running....')
                    advas=asstatadv[0]
                    advPath=asstatadv[1]
                    advas.config(text='AutoSense is Running....')
                    advPath.config(text=f'AutoSense Dir : {_ASPATH[0]}')
                else:
                    terminator=0
            else:
                pass
        elif terminator!=0 and caller =='':
            confrm=messagebox.askyesno('Turn Off AutoSence','You are about to turn off AutoSence.\n\nBy turning off, we will no longer be able to keep track of'
                                                            ' new comming files, So new file will not be sorted automatically.\n\nDo you want to Turn Off '
                                                            'AutoSense ?',parent=root)
            if confrm==True:
                terminator=0
                messagebox.showinfo('Activated', 'AUtoSense Service is Successfully Deactivated ! .', parent=root)
                kl=asstatadv[0]
                kl.config(text='')
                advas = asstatadv[0]
                adv__=asstatadv[1]
                advas.config(text='')
                adv__.config(text='')
                user_obj.update_val('autosense',0,'None')
            else:
                pass
        elif terminator==3 and caller=='Initial Call':
            s = asstatadv[0]
            s.config(text='AutoSense is Running....')
            advas = asstatadv[0]
            advas.config(text='AutoSense is Running....')
            rr=autoSence(as_path)



    main_menu=Menu(root)
    root.config(menu=main_menu)

    menue_label=Menu(main_menu,tearoff=0)
    main_menu.add_cascade(label="Menu",menu=menue_label)

    menue_label.add_command(label='AutoSense',command=lambda :activatingAS(''))
    menue_label.add_separator()

    backlitMenu=Menu(menue_label,tearoff=0)
    menue_label.add_cascade(label='Backlit Color',menu=backlitMenu)

    backlitMenu.add_command(label='Default',command=lambda :changecolor(0))
    backlitMenu.add_separator()
    backlitMenu.add_command(label='White',command=lambda:changecolor(1,0))
    backlitMenu.add_command(label='Red',command=lambda:changecolor(1,1))
    backlitMenu.add_command(label='Green',command=lambda :changecolor(1,2))
    backlitMenu.add_command(label='Blue',command=lambda :changecolor(1,3))
    backlitMenu.add_command(label='Cyan',command=lambda :changecolor(1,4))
    backlitMenu.add_command(label='Lawn Green',command=lambda :changecolor(1,5))

    menue_label.add_separator()

    settings_label=Menu(main_menu,tearoff=0)
    main_menu.add_cascade(label="Settings",menu=settings_label)

    settings_label.add_command(label='Manage Extensions',command=eXTENSIONS_MANAGER)

    def autoSence(previous_path=''):
        def rigidFun(path1):

                mainpath = path1
                files = os.walk(mainpath)
                processed_files = next(files)[2]
                if 'desktop.ini' in processed_files:
                    processed_files.remove('desktop.ini')
                else:
                    pass


        def checkNewFileindir(path):

                """ This function keep monitoring the assigned folder for arrival of new files """
                global  terminator

                mainpath = path
                files = os.walk(mainpath)
                processed_files = next(files)[2]
                if 'desktop.ini' in processed_files:
                    processed_files.remove('desktop.ini')
                else:
                    pass
                if len(processed_files) > 0:
                    aSense=AdvanceOperation(extDatabase(0,0),0,0,0,'AutoSense')
                    aSense.file_processor(mainpath)
                else:
                    pass
                def looping():
                    try:
                        if terminator!=0:
                            checkNewFileindir(path)
                        else:
                            if len(processed_files)>0:
                                ask([f for f in processed_files if f not in redundent_files])
                    except StopIteration:
                        messagebox.showerror('Unexpected Error','Something happend to the folder which was currently being monitored by autosense.')

                root.after(1000, looping)

        if previous_path=='':
            _ASPATH.clear()
            path = filedialog.askdirectory(title='Select the folder/directory on which you want tp apply AutoSense')
            _ASPATH.insert(0,path)
        else:
            _ASPATH.clear()
            path=previous_path
            _ASPATH.insert(0,path)
        if path!='':
            if path !='C:/':
                user_obj.update_val('autosense', 1, path=path)
                rigidFun(path)
                checkNewFileindir(path)
                return 1

            else:
                errorhandleing('Access Denied !','We can not apply Autosense on C drive.')
        else:
            errorhandleing('Abort !', "Operation aborted.")
            terminator=0
            return 0

    #=============================================================  Menu Function   ==================================================================


    backlit_colors=['white','red','green','blue','cyan','lawngreen']


    sd_adv=[]

    noinfo='---------------'
    a_metainformation="""This process will Automatically creates multiple folder depending on the types 
    of files found and then sort them accordingly and organize them into the same directory."""

    asstat=[]
    asstatadv=[]

    obj6=Mainframe2()

    fonttxt='Ebrima'
    headerclr='white'


    rootCanvas.create_text(770,30,text='file SWAP',fill=headerclr,font=f'{fonttxt} 20 ')

    rootCanvas.create_line(680,10,680,50,fill=butclr)

    footerCanvas.config(highlightthickness=1,highlightbackground=None)
    footerCanvas.create_line(20,20,880,20,fill=backlit_colors[0])

    def backlitdivider(objectofroot,x,y,x1,y1):
        divid=objectofroot.create_line(x, y, x1, y1, fill='white')
        return divid

    # ====================================== Main Options  ===========================================================


    def closing():
        global closing_counter,terminator
        if terminator==0:
            exitresp=messagebox.askyesno('Exit','Confirm the exit by clicking Yes.',parent=root)
            if exitresp==True:
                root.destroy()
            else:
                pass
        elif terminator!=0:
            if closing_counter==0:
                closing_counter=1
                exitresp2=autoSense_confirmation(root)
                closing_counter=0
                if exitresp2==True:
                    root.destroy()
                else:
                    closing_counter=0
                    pass
        elif terminator not in [0,1,3]:
            errorhandleing('Fatal Error','Something Terribly Went Wrong. Unable to Close Application!')





    #0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

    def advancetab():

            """This is the main tab you see when you run the software """

            global update_list_FE,terminator

            panel2 = Canvas(root, width=840, height=500, bg=themecolor, highlightthickness=0, highlightbackground='cyan')
            panel2.place(x=30, y=60)
            asservice2 = globalobj.customlabels(panel2, '', f'{fonttxt} 14', themecolor, 300, 5, fg=butclr)
            asservice3 = globalobj.customlabels(panel2, '', f'{fonttxt} 14', themecolor, 80, 350, fg=butclr)
            if terminator!=0:
                asservice2.config(text='AutoSense is Running....')
                asservice3.config(text=f'AutoSense Dir : {_ASPATH[0]}')
            else:
                asservice2.config(text='')
                asservice3.config(text='')
            asstatadv.insert(0,asservice2)
            asstatadv.insert(1,asservice3)
    #------------------------------------------------------------------------------------------------------------------------------------------------------ ADV Directories
            adinfo=globalobj.customlabels(panel2,'Directories  >',f'{fonttxt} 14 bold',themecolor,20,25,fg=butclr)
            # div=panel2.create_line(99,42,800,42,fill=butclr)
            backlitdivider(panel2,99,42,800,42)
            metainfo1=globalobj.customlabels(panel2,'Select the directory to be Autometically Organize ',f'{fonttxt} 12',themecolor,250,50,fg=deadlink)

            adirlabel=globalobj.customlabels(panel2,'Directory : ',f'{fonttxt} 12',themecolor,80,80,fg=butclr)
            obj6.genralentry(panel2,180,87,70)
    #------------------------------------------------------------------------------------------------------------------------------------------------------ ADV Buttons
            def getfiles():
                rawpath=filedialog.askdirectory(title='Select the directory to sort',parent=root)
                if os.path.exists(rawpath) and rawpath !='C:/':
                    obj6.setgenraluser(rawpath)
                    sd_adv.insert(0,rawpath)

                    df=os.walk(rawpath)
                    filefound=next(df)[2]
                    for removable in filefound:
                        try:
                            if removable.endswith('.tmp') :
                                filefound.remove(removable)
                                filefound.remove('desktop.ini')
                            else:
                                try:
                                    if 'desktop.ini' in filefound:
                                        filefound.remove('desktop.ini')
                                    else:
                                        pass
                                except:
                                    pass
                        except:
                            pass
                    if len(filefound) !=0:
                        afileinfo.config(text=f'{len(filefound)} messed files found.',fg=butclr)

                        aprocessinfo.config(text='Pending...')
                    else:
                        afileinfo.config(text=f'{0} messed files found. This directory is already managed.',fg='cyan')
                        asubbut.bind('<Button-1>',lambda event: messagebox.showinfo('Already Managed !','There is nothing to be managed in this directiory.'))
                elif not rawpath:
                    pass
                else:
                    errorhandleing('Critical Error','The path is invalid OR leads to C drive directly.\n\nWe suggest you not to manipulate C drive')

            def setdefault():
                obj6.cleangenral()

            def processingFiles(event=''):
                pathentered=obj6.getgenralentrydata()

                if pathentered!='':
                    sd_adv.insert(0, pathentered)

                    sourceDirectory = sd_adv[0]
                    if os.path.exists(sourceDirectory):
                        adv_Obj=AdvanceOperation(extDatabase(0,0),aprocessinfo,folderinfo2,setdefault,'normal')
                        adv_Obj.file_processor(sourceDirectory)
                    else:
                        errorhandleing('Invalid Attempt!', 'The path you have entered does not exist.')
                else:
                    errorhandleing('Error','Please select a directory.')

            ab1=globalobj.custombuttons(panel2,'',3,1,getfiles,765,81)
            ab1.bind('<Enter>',lambda x,b=ab1:b.config(bg='#8ec5ea'))
            ab1.bind('<Leave>',lambda x,b=ab1:b.config(bg='white'))

            asubbut=globalobj.customcan(panel2,80,30,themecolor,725,450)
            asubinfo=asubbut.create_text(40,14,text='START',fill=butclr,font=f'{fonttxt} 12')
            asubbut.bind('<Enter>',lambda x,b=asubbut:b.config(highlightthickness=2,highlightbackground='green'))
            asubbut.bind('<Leave>',lambda x,b=asubbut:b.config(highlightthickness=0,highlightbackground=None))
            asubbut.bind('<Button-1>',processingFiles)

            acanbut=globalobj.customcan(panel2,80,30,themecolor,630,450)
            acaninfo=acanbut.create_text(40,14,text='Exit',fill=butclr,font=f'{fonttxt} 12')
            acanbut.config(cursor='hand2')
            acanbut.bind('<Enter>',lambda x,b=acanbut:b.config(highlightthickness=1,highlightbackground='red'))
            acanbut.bind('<Leave>',lambda x,b=acanbut:b.config(highlightthickness=0,highlightbackground=None))
            acanbut.bind("<Button-1>",lambda event:closing())

            refresh=globalobj.customcan(panel2,80,30,themecolor,540,450)
            refresh_info=refresh.create_text(40,14,text='Refresh',fill=butclr,font=f'{fonttxt} 12')
            refresh.config(cursor='hand2')
            refresh.bind('<Enter>',lambda x,b=refresh:b.config(highlightthickness=1,highlightbackground='cyan'))
            refresh.bind('<Leave>',lambda x,b=refresh:b.config(highlightthickness=0,highlightbackground=None))

            def reFreshingAdvanceTab():
                advancetab()
                reset_counter()


            refresh.bind('<Button-1>',lambda event:reFreshingAdvanceTab())
    #------------------------------------------------------------------------------------------------------------------------------------------------------ ADV Process
            apifo=globalobj.customlabels(panel2,'Process  >',f'{fonttxt} 14 bold',themecolor,20,150,fg=butclr)
            # div=panel2.create_line(99,148,800,148,fill=butclr)
            backlitdivider(panel2,99,170,800,170)

            # metainfo3=globalobj.customlabels(panel2,a_metainformation,f'{fonttxt} 12',themecolor,80,180,fg=deadlink)


            afinfo=globalobj.customlabels(panel2,'Total Files Found  : ',f'{fonttxt} 12',themecolor,80,200,fg=butclr)
            afileinfo=globalobj.customlabels(panel2,noinfo,f'{fonttxt} 12',themecolor,250,200,fg=butclr)

            apinfo=globalobj.customlabels(panel2,'Process Status      : ',f'{fonttxt} 12',themecolor,80,235,fg=butclr)
            aprocessinfo=globalobj.customlabels(panel2,noinfo,f'{fonttxt} 12',themecolor,250,235,fg=butclr)

            fldinfo2=globalobj.customlabels(panel2,'Folders Created    : ',f'{fonttxt} 12',themecolor,80,270,fg=butclr)
            folderinfo2=globalobj.customlabels(panel2,noinfo,f'{fonttxt} 12',themecolor,250,270,fg=deadlink)

    advancetab()

    if as_status=="1":
        if os.path.exists(as_path):
            terminator=3
            activatingAS('Initial Call')
            asstatadv[1].config(text=f'AutoSense Dir : {_ASPATH[0]}')
        else:
            aSError()
            user_obj.update_val('autosense',0,'none')


    gen= Canvas(root, width=90, height=35, bg=themecolor, highlightthickness=0, highlightbackground='steelblue',cursor='hand2')
    gen.place(x=30, y=25)
    genlabel=gen.create_text(45,16,text='Genral',fill='white',font='none')
    div = backlitdivider(gen, 0, 32, 92, 32)
    gen.itemconfig(div, fill='steelblue', width=3)

    # ====================================== ============ ===========================================================
    def errorhandleing(head,message):
        messagebox.showerror(head, message, parent=root)

    root.protocol('WM_DELETE_WINDOW',closing)
    root.mainloop()

proceed()