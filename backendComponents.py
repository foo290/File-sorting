from oops3 import *
import shutil,webbrowser
import sqlite3
from directoryManager import *

remove_operation_counter=0
skip_operation_counter=0
redundent_files=[]
nonsorted = []

#-----------------------------------------------------DATABASE CONNECTIVITY---------------------------------------------

def add_New_EXTENSION(name,ext,win,caller=''):
    connection=sqlite3.connect(extensions_DATABASE)
    try:
        cur=connection.cursor()
        if name not in extDatabase(0,0) and ext not in extDatabase('all_ext','e') and caller=='':
                oldall=extDatabase('all_ext','e')
                oldall.append(ext)
                cur.execute(f'insert into ext values(?,?)',(name,ext))
                cur.execute(f'update ext set extension="{",".join(oldall)}" where name="all_ext"')
                messagebox.showinfo('Success!',
                                    f'A new extension is added Successfully in database. \n\nName : {name}\n\nExtension : {ext}',
                                    parent=win)
        elif caller=='update':
            if ext not in extDatabase('all_ext','e'):
                oldExt=extDatabase(name,'e')
                oldall=extDatabase('all_ext','e')
                oldExt.append(ext)
                oldall.append(ext)
                cur.execute(f'update ext set extension="{",".join(oldExt)}" where name="{name}"')
                cur.execute(f'update ext set extension="{",".join(oldall)}" where name="all_ext"')
                messagebox.showinfo('Success!',
                                    f'A new extension is added Successfully in database. \n\nName : {name}\n\nExtension : {ext}',
                                    parent=win)

            else:
                messagebox.showerror('Already Exist','This extension is already in data base.',parent=win)

        connection.commit()
    finally:
        connection.close()

def delete_file_type(ftyp,win):
    connection=sqlite3.connect(extensions_DATABASE)
    try:
        allext=extDatabase('all_ext','e')
        exttodel=extDatabase(ftyp,'e')
        updatedAllext=[exts for exts in allext if exts not in exttodel]
        cur=connection.cursor()
        cur.execute(f'delete from ext where name="{ftyp}"')
        cur.execute(f'update ext set extension="{",".join(updatedAllext)}" where name="all_ext"')
        connection.commit()
        messagebox.showinfo('Deleted', f'File Type with name : "{ftyp}" and all extensions under its catagory is deleted Successfully.',
                            parent=win)
    finally:
        connection.close()

def del_eXtensions(name,ext_discard,win):
    extstodel=extDatabase(name,'e')

    allexts=extDatabase('all_ext','e')

    if ext_discard in extstodel:
        updated_exts=[ex for ex in extstodel if ex !=ext_discard]
        updatedall=[e for e in allexts if e !=ext_discard]
        connection=sqlite3.connect(extensions_DATABASE)
        try:
            cur=connection.cursor()
            cur.execute(f'update ext set extension="{",".join(updated_exts)}" where name="{name}"')
            cur.execute(f'update ext set extension="{",".join(updatedall)}" where name="all_ext"')
            connection.commit()
            messagebox.showinfo('Deleted',f'Extension with name "{ext_discard}" if deleted successfully from "{name}"',parent=win)
        finally:
            connection.close()
        return 1
    else:
        return -1

def config_settings(id_no):
    conncection_to_settings = sqlite3.connect(user_configuration_DATABASE)
    try:
        cur=conncection_to_settings.cursor()
        cur.execute(f'select name, value from settings where id = "{id_no}"')
        data=cur.fetchall()
        return list(list(data)[0])
    finally:
        conncection_to_settings.close()


class UserConfig:
    _connection=sqlite3.connect(user_configuration_DATABASE)

    def update_val(self,name,val,path=''):
        try:
            self.cur=self._connection.cursor()
            if path=='':
                self.cur.execute(f'update settings set value="{val}" where name="{name}"')
            else:
                print(path)
                self.cur.execute(f'update settings set  value="{val}" , path="{path}" where name="{name}"')
            self._connection.commit()
        except:
            errorhandleing('Rare Case','Something is not as what we expected. Try reinstalling the software',None)

    def get_val(self,name, typ=''):
        try:
            cur = self._connection.cursor()
            if typ == '':
                cur.execute(f'select value from settings where name ="{name}"')
                data = cur.fetchall()
                return list(list(data)[0])[0]
            else:
                cur.execute(f'select value,path from settings where name ="{name}"')
                data = cur.fetchall()
                return list(list(data)[0])
        except:
            errorhandleing('Rare Case', 'Something is not as what we expected. Try reinstalling the software', None)

def reset_counter():
    global remove_operation_counter,skip_operation_counter
    remove_operation_counter=0
    skip_operation_counter=0

def ask(nonsorted):
    askwin = Toplevel()
    width = 850
    height = 500
    x = (askwin.winfo_screenwidth() // 2) - (width // 2)
    y = (askwin.winfo_screenheight() // 2) - (height // 2)

    askwin.geometry(f'{width}x{height}+{x}+{y}')
    askglobal_obj = Mainframe2()
    askobj1 = Mainframe2()
    askwin.title('Unknown Files')
    askwin.focus()
    askwin.resizable(0,0)

    askcan = askglobal_obj.customcan(askwin, width, height, 'white', 0, 0)

    askcan.create_text(30, 20, text='We were not able to sort Some of the files below.', anchor=NW, font='none 15')
    askcan.create_text(30, 60, text='If you know the type of extensions they have, Please provide us that information so in future we '
                            'will be able to sort them.', anchor=NW)

    picHolderCan=askglobal_obj.customcan(askcan,250,250,'white',490,200)
    pic=PhotoImage(file=nonsorted_graphic)
    picHolderCan.create_image(0,0,image=pic,anchor=NW)
    picHolderCan.create_text(30, 10, text='?', anchor=NW,font='Ebrima 15')
    picHolderCan.create_line(50,30,70,40)



    list_holder = askglobal_obj.customframes(askcan, 300, 200, 'red', 30, 150)
    yscrol = Scrollbar(list_holder)
    yscrol.pack(side=RIGHT, fill=Y)
    lBox = askobj1.customListBox(list_holder, 50, 13, LEFT)
    lBox.config(yscrollcommand=yscrol.set, justify=CENTER,borderwidth=0)
    yscrol.config(command=lBox.yview)

    askobj1.listBox_values(nonsorted)

    askcan.create_text(20, 350, text='', anchor=NW, fill='blue', )
    srch_label = askglobal_obj.customlabels(askcan, 'Search Online for these extensions?', 'none 10 bold underline',
                                            'white', 30, height-50, fg='blue')
    srch_label.config(cursor='hand2')

    p = [str(r).split('.')[-1] for r in nonsorted]
    def search_online(event):
        files_to_search=', '.join(p)
        webbrowser.open_new_tab(f'https://www.google.com/search?q={f"what are {files_to_search} files"}')

    srch_label.bind('<Button-1>', search_online)
    def quitDestroy():
        askwin.quit()
        askwin.destroy()

    askwin.protocol('WM_DELETE_WINDOW', quitDestroy)
    askwin.mainloop()

def extDatabase(extType,ft):
    connection = sqlite3.connect(extensions_DATABASE)
    try:
        if ft=='e':
            cur = connection.cursor()
            cur.execute(f'select extension from ext where name = "{extType}"')
            data = cur.fetchall()
            return str(list(data)[0][0]).split(',')
        else:
            temp_l=[]
            cur = connection.cursor()
            cur.execute(f'select name from ext')
            data = cur.fetchall()
            data_to=data

            for i in data_to:
                for j in i:
                    temp_l.append(j)
            return temp_l

    finally:
        connection.close()


class AdvanceOperation:
    _counter = 0
    _directory_counter = 0
    _created_folders = []
    _temp_l = []
    _extlist = []
    _call_Type=''
    _FrontEnd_update_info=[]

    def __init__(self, extlist,aprocessinfo,folderinfo2,setdefault,typ):
        if len(extlist) != 0:
            for _ in extlist:
                ltom = []
                self._temp_l.append(ltom)
                self._extlist = [ext for ext in extlist if ext != 'all_ext']
        self._FrontEnd_update_info.extend((aprocessinfo,folderinfo2,setdefault))
        self._call_Type=typ

    def directory_manager(self, sourcepath):
        self._created_folders.clear()
        global remove_operation_counter, skip_operation_counter,redundent_files
        prefix = ''
        fetchX_paths = [sourcepath + f'/{prefix} {f_name}' for f_name in self._extlist]

        for lists in self._temp_l:
            self._iteration_counter = 0

            if len(lists) != 0:
                folder = fetchX_paths[self._directory_counter]
                if not os.path.exists(folder):
                    os.mkdir(folder)
                    self._created_folders.append(1)
                    for _files_ in lists:
                        if not os.path.isfile(f'{folder}/{_files_}'):
                            shutil.move(sourcepath + '/' + _files_, folder)
                        else:
                            if _files_ not in redundent_files:
                                redundent_files.append(_files_)
                    self._directory_counter += 1
                else:
                    for __files__ in lists:
                        if not os.path.isfile(f'{folder}/{__files__}'):
                            shutil.move(sourcepath + '/' + __files__, folder)
                        else:
                            if __files__ not in redundent_files:
                                redundent_files.append(__files__)
                    self._directory_counter += 1
                self.single_file_Clash_handler_(sourcepath, redundent_files, folder)
            else:
                self._directory_counter += 1
        return 1, self._created_folders,

    def file_processor(self, raw_path):
        _files = os.listdir(raw_path)
        for file_types_ in self._extlist:
            for file_found in _files:
                for _ext in extDatabase(file_types_, 'e'):
                    if os.path.isfile(raw_path+'/'+file_found):
                        if file_found.endswith(_ext):
                            self._temp_l[self._counter].append(file_found)
                            break
            self._counter += 1
        self.dm_resp = self.directory_manager(raw_path)
        self._temp_l.clear()

        if self.dm_resp[0] == 1:
            remainingFiles = os.listdir(raw_path)
            if len(remainingFiles) == 0:
                pass
            else:
                for r_files in remainingFiles:
                    if os.path.isfile(f'{raw_path}/{r_files}'):
                        nonsorted.append(r_files)
            if len(nonsorted) != 0 and nonsorted !=redundent_files:
                if self._call_Type=='normal':
                    ask([k for k in nonsorted if k not in redundent_files])
                    if len(self._FrontEnd_update_info)==3:
                        aprocessinfo, folderinfo2, setdefault = self._FrontEnd_update_info
                        aprocessinfo.config(text='Completed!', fg='lawngreen')
                        folderinfo2.config(text=f'{len(self.dm_resp[1])} folders are created.', fg='cyan')
                        setdefault()
            else:
                if self._call_Type=='normal':
                    if len(self._FrontEnd_update_info)==3:
                        aprocessinfo, folderinfo2, setdefault = self._FrontEnd_update_info
                        aprocessinfo.config(text='Completed!', fg='lawngreen')
                        folderinfo2.config(text=f'{len(self.dm_resp[1])} folders are created.', fg='cyan')
                        setdefault()
        self._FrontEnd_update_info.clear()
        nonsorted.clear()
        redundent_files.clear()

    def single_file_Clash_handler_(self,sourcepath, red_file, folder):
        global remove_operation_counter, skip_operation_counter
        for redundent in red_file:
            if remove_operation_counter == 0:
                if skip_operation_counter == 0:
                        file_crash_handler(sourcepath + '/' +redundent , folder)
                else:
                    pass
            else:
                file_Remover(f'{sourcepath}/{redundent}', f'{folder}/{redundent}', folder)


def errorhandleing(head, message,win):
    messagebox.showerror(head, message,parent=win)

def file_Remover(src,ftr,dst):
    try:
        os.remove(ftr)
        shutil.move(src, dst)
        return 1
    except FileNotFoundError:
        return -1
def renaming_file(src,dst):
    try:
        os.rename(src, dst)
        return 1
    except:
        return -1

def file_crash_handler(src,dst):
    global remove_operation_counter,skip_operation_counter

    _fileName=src.split('/')[-1]
    excluded=['?','|','/','\\','<','>','.','"','*']

    askwin=Toplevel()
    width=800
    height=500
    askwin.title('Same File Conflict!')
    askwin.focus()
    askwin.attributes('-topmost',1)
    x=(askwin.winfo_screenwidth()//2)-(width//2)
    y=(askwin.winfo_screenheight()//2)-(height//2)

    askwin.geometry(f'{width}x{height}+{x}+{y}')
    askglobal_obj=Mainframe2()
    askobj1=Mainframe2()
    askwin.resizable(0,0)

    askcan=askglobal_obj.customcan(askwin,width,height,'white',0,0)

    askcan.create_text(100,15,text='A file with exact same name already exist in this directory.',anchor=NW,font='Ebrima 15')
    divider1=askcan.create_line(50,55,650,55)

    pic1_holder=askglobal_obj.customcan(askcan,100,100,'black',50,70)
    pic1=PhotoImage(file=fileClash_graphic)
    pic1_holder.create_image(0,0,image=pic1,anchor=NW)
    divider2=askcan.create_line(100,200,600,200)

    askcan.create_text(180,90,text='File Name      :    ',anchor=NW)
    askcan.create_text(300, 90, text=_fileName, anchor=NW)

    askcan.create_text(180,130,text='Destination    :   ',anchor=NW)
    askcan.create_text(300, 130, text=dst, anchor=NW)

    pic2_holder=askglobal_obj.customcan(askcan,100,100,'black',50,220)
    pic2_holder.create_image(0,0,image=pic1,anchor=NW)
    divider3=askcan.create_line(100,350,600,350)


    askcan.create_text(180,230,text='File Name      :    ',anchor=NW)
    askcan.create_text(300, 230, text=_fileName, anchor=NW)

    askcan.create_text(180,270,text='Source           :   ',anchor=NW)
    askcan.create_text(300, 270, text=src, anchor=NW)

    def onclick():
        state1=chb1_var.get()
        state2=chb2_var.get()
        if state1==1 and state2==0:
            chb1.config(fg='green')
            chb2_var.set(0)
            chb2.config(state=DISABLED)
            chb3.config(state=NORMAL)
            nameVar.set('')
            nnE.config(state=DISABLED)
        else:
            chb1.config(fg='black')
            chb2_var.set(0)
            chb2.config(state=NORMAL)
            chb3.config(state=DISABLED,fg='black')
            nnE.config(state=NORMAL)
            nameVar.set('')
            chb3_var.set(0)

    def onclick2():
        state1=chb1_var.get()
        state2=chb2_var.get()
        if state2==1 and state1==0:
            chb2.config(fg='green')
            chb1.config(state=DISABLED)
            chb3.config(state=NORMAL)
            nameVar.set('')
            nnE.config(state=DISABLED)
        else:
            chb2.config(fg='black')
            chb1.config(state=NORMAL)
            chb3.config(state=DISABLED,fg='black')
            nnE.config(state=NORMAL)
            nameVar.set('')
            chb3_var.set(0)
            chb1_var.set(0)


    def onclick3():
        state3=chb3_var.get()
        if state3==1:
            chb3.config(fg='green')
        else:
            chb3.config(fg='black')

    chb1_var=IntVar();  chb2_var=IntVar();chb3_var=IntVar()

    chb1=Checkbutton(askcan,bg='white',text='Remove from destination',variable=chb1_var,command=onclick)
    chb1.place(x=170,y=310)
    chb2=Checkbutton(askcan,bg='white',text='  Skip This File ? ',variable=chb2_var,command=onclick2)
    chb2.place(x=360,y=310)
    chb3=Checkbutton(askcan,bg='white',text='  Do this for all Files ? ',variable=chb3_var,command=onclick3,state=DISABLED)
    chb3.place(x=490,y=310)

    askcan.create_text(100,360,text='You can either RENAME the file to avoid clash .',anchor=NW,font='Ebrima 12 bold')

    nameVar=StringVar()
    askcan.create_text(100,400,text='New Name : ',anchor=NW)
    nnE=Entry(askcan,highlightthickness=1,highlightbackground='black',width=25,textvariable=nameVar)
    nnE.place(x=180,y=398)
    responseList=[]
    def quitDestroy():
        askwin.quit()
        askwin.destroy()

    def proceeding():
        global remove_operation_counter,skip_operation_counter

        chb1_state=chb1_var.get()
        chb2_state=chb2_var.get()
        chb3_state=chb3_var.get()

        nameE=nnE.get()

        if chb1_state==1 and chb3_state !=1:
            rmrsp=file_Remover(src,f'{dst}/{_fileName}',dst)
            if rmrsp==1:
                quitDestroy()
            else:
                errorhandleing('Error!','An error Occured during moving process',askwin)
        elif chb1_state==1 and chb3_state==1:
            rmrsp=file_Remover(src,f'{dst}/{_fileName}',dst)
            if rmrsp==1:
                remove_operation_counter=1
                quitDestroy()
            else:
                errorhandleing('Error!','An error Occured during moving process',askwin)
                quitDestroy()

        elif chb2_state==1 and chb3_state !=1:
            quitDestroy()
        elif chb2_state==1 and chb3_state==1:
            skip_operation_counter=1
            quitDestroy()
        elif nameE !='':
            inputList=list(nameE)
            templ=[]
            for alpha in inputList:
                if alpha in excluded:
                    errorhandleing('Invalid Charecter','Charecters Like     ?, |, /, \\, <, >, ., ",*   are not allowed in name of the file.',askwin)
                    templ.insert(0,'Abort')
                    break
                else:
                    templ.insert(0,'continue')
            if templ[0]=='Abort':
                pass
            else:
                rename_resp=renaming_file(src,f'{dst}/{nameE}.{_fileName.split(".")[-1]}')
                if rename_resp==1:
                    quitDestroy()
                else:
                    errorhandleing('Rename Error','A file with the given name is already exist in destination directory.',askwin)
                    quitDestroy()
        else:
            errorhandleing('Action Not Specified','YOU MUST SELECT THE ACTION TO BE PERFORMED TO AVOID MALFUNCTION !',askwin)

    askbut1=askglobal_obj.custombuttons(askcan,'Proceed',15,1,proceeding,550,450)

    askwin.protocol('WM_DELETE_WINDOW',lambda :errorhandleing('Action Not Specified','YOU MUST SELECT THE ACTION TO BE PERFORMED TO AVOID MALFUNCTION !',askwin))
    askwin.mainloop()

def autoSense_confirmation(root):
    autoS = Toplevel()
    width = 750
    height = 300
    x = (autoS.winfo_screenwidth() // 2) - (width // 2)
    y = (autoS.winfo_screenheight() // 2) - (height // 2)

    autoS.geometry(f'{width}x{height}+{x}+{y}')
    askglobal_obj = Mainframe2()
    askobj1 = Mainframe2()
    autoS.title('Feature Confirmation')
    autoS.focus()
    autoS.resizable(0,0)

    askcan = askglobal_obj.customcan(autoS, width, height, 'white', 0, 0)

    askcan.create_text(30, 20, text='AutoSense is Running...', anchor=NW, font='Ebrima 20')
    askcan.create_text(30, 70, text='We will Shut Down AutoSense after software is closed and next time it will '
                                    'Start\nAutomatically on applied folder.',font='Ebrima 10', anchor=NW)
    askcan.create_text(30, 180, text='Click "OK" for Confirmation.',font='Ebrima 10', anchor=NW)

    picHolderCan=askglobal_obj.customcan(askcan,250,250,'white',480,90)
    pic=PhotoImage(file=autoSense_Exit_graphic)
    picHolderCan.create_image(0,0,image=pic,anchor=NW)

    def ok_Clicked():
        root.destroy()

    userConfigs=UserConfig()

    def stop_and_exit():
        userConfigs.update_val('autosense',0,'')
        root.destroy()

    b1=askglobal_obj.custombuttons(askcan,'OK',15,1,ok_Clicked,30,250)
    b1.config(borderwidth=2,relief='groove',cursor="hand2")

    b2=askglobal_obj.custombuttons(askcan,'Turn off and Exit',25,1,stop_and_exit,160,250)
    b2.config(borderwidth=2,relief='groove',cursor="hand2")

    def quitDestroy():
        autoS.quit()
        autoS.destroy()

    autoS.protocol('WM_DELETE_WINDOW', quitDestroy)
    autoS.mainloop()

def aSError():
    autoS = Toplevel()
    width = 612
    height = 344
    x = (autoS.winfo_screenwidth() // 2) - (width // 2)
    y = (autoS.winfo_screenheight() // 2) - (height // 2)
    autoS.geometry(f'{width}x{height}+{x}+{y}')
    autoS.attributes('-topmost',1)
    autoS.focus()
    autoS.overrideredirect(1)
    askglobal_obj = Mainframe2()
    autoS.title('Temporary Error !      AutoSense Directory Not Found')
    autoS.focus()
    autoS.resizable(0,0)
    askcan = askglobal_obj.customcan(autoS, width, height, 'white', 0, 0)
    pic=PhotoImage(file=autoSense_404_graphic)
    askcan.create_image(0,0,image=pic,anchor=NW)
    askcan.create_text(30, 20, text='Oops!', anchor=NW, font='Ebrima 30')
    askcan.create_text(30, 100, text='Error : 404 Directory Not Found', anchor=NW, font='Ebrima 15')
    askcan.create_text(30, 140, text='We can not find the Directory on which \nAutoSense was assigned previously!', anchor=NW)
    askcan.create_text(30, 180, text='This is NOT AN ISSUE,\nbut we will no longer be able to turn on \nAutoSense Automatically.', anchor=NW)
    askcan.create_text(30, 260, text="That's all we know.", anchor=NW)
    def quitDestroy():
        autoS.quit()
        autoS.destroy()
    b1=askglobal_obj.custombuttons(askcan,'OK',15,1,quitDestroy,30,300)
    b1.config(borderwidth=2,relief='groove',cursor="hand2")
    autoS.after(10000,quitDestroy)
    autoS.protocol('WM_DELETE_WINDOW', quitDestroy)
    autoS.mainloop()
def show_online(type):
    if type=='project':
        webbrowser.open_new_tab('https://showcaseport.blogspot.com/2019/10/aspire-series.html')
    elif type=='contact':
        webbrowser.open_new_tab('https://www.linkedin.com/in/iam-nitinsharma')




from ctypes import windll
q=windll.shcore.SetProcessDpiAwareness(2)

