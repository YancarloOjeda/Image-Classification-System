
#%%Libraries 
import tkinter 
import cv2
import os
import os.path
import numpy as np
import serial
import PIL.Image
from PIL import Image, ImageTk
from ast import literal_eval
from scipy import misc, ndimage
from tkinter import PhotoImage, messagebox, ttk, Canvas, filedialog, Tk, Frame, BOTH
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import font
from tkinter.font import Font
from tkinter.simpledialog import askstring
from screeninfo import get_monitors
from tkinter import Button, Frame, INSERT, LEFT, RIGHT, Label
from tkinter import  Scrollbar, Text, Tk, TOP, X, Y, filedialog
from tkinter import *
import cv2
from screeninfo import get_monitors



#%%-------------GENERAL FUNCTIONS-------------
#%%Colors 
C_Primary = (21,21,21)
C_Light_Dark = (48,48,48)
C_White = (255,255,255)
C_Dark = (0,0,0)
C_Grey = (200,200,200)
C_Red = (255,0,0)
Font_CV = cv2.FONT_HERSHEY_SIMPLEX
Font_1 = 'Sans'

def Fun_Rgb(RGB):
    return "#%02x%02x%02x" % RGB  


#%%Fun Size
def Fun_Size(img, size):
    img = PIL.Image.open(img)
    size_1 = img.size
    width = int(size_1[0]*size)
    height = int(size_1[1]*size)
    img = img.resize((width, height))
    img = ImageTk.PhotoImage(img)
    return img

         
#%%Diectories
Dir_Images = 'Image/'
Dir_Projects = 'Projects/'
Dir_Videos = 'Videos/'
Dir_Project_Images = '/Images/'

#%%Windows size
aux_monitor = 0

try:
    for monitor in get_monitors():
        aux_monitor += 1
        if aux_monitor == 1:
            monitor_size = monitor
            aux_string_monitor = str(monitor_size)
            aux_cortar = aux_string_monitor.split('Monitor(')
            aux_cortar = aux_cortar[1].split(')')
            parameters_monitor = aux_cortar[0].split('width=')
            parameters_monitor = parameters_monitor[1].split(', height=')
            width_monitor = int(parameters_monitor[0])
            parameters_monitor = parameters_monitor[1].split(', width_mm=')
            height_monitor = int(parameters_monitor[0])
    
        if aux_monitor == 2:
            monitor_size = monitor
            aux_string_monitor = str(monitor_size)
            aux_cortar = aux_string_monitor.split('Monitor(')
            aux_cortar = aux_cortar[1].split(')')
            parameters_monitor = aux_cortar[0].split('width=')
            parameters_monitor = parameters_monitor[1].split(', height=')
            width_monitor = int(parameters_monitor[0])
            parameters_monitor = parameters_monitor[1].split(', width_mm=')
            height_monitor = int(parameters_monitor[0])
     
    aux_size = .65
    
except:
    width_monitor = 1280
    height_monitor = 800
    aux_size = .75
    
    
aux_width_monitor = width_monitor/15 
aux_height_monitor = height_monitor/15  


#%%Tool tip
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 20
        y = y + cy + self.widget.winfo_rooty() +20
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

#%%-------------PROGRAM FUNCTIONS-------------   
#%%Fun info
def info():
    messagebox.showinfo('ICS v-0.1 ','Program developed by Yancarlo Ojeda at University of Guadalajara, México, under a open source license. For more information plase contact me at yanojedaps@gmail.com')
 
#%%Fun cutVideo
def cutVideo():
    global Dir_Project
    pathVideo = filedialog.askopenfilename(initialdir = Dir_Videos,
                                            title = "Select Video",
                                            filetypes = (("all files","*.*"),
                                            ("mp4 files","*.mp4")))
    
    pathNewProject =  filedialog.asksaveasfilename(initialdir = Dir_Projects,
                                title = "Save image project",
                                filetypes = (("all files","*.*"),
                                ("jpeg files","*.jpg")))
    
    
    
    Dir_Project_Img = pathNewProject + Dir_Project_Images        
    if os.path.exists(pathNewProject):
        os.path.exists(pathNewProject)
        os.mkdir(Dir_Project_Img)
    else:
        os.mkdir(pathNewProject)
        os.mkdir(Dir_Project_Img)
        
    Captura_Video = cv2.VideoCapture(pathVideo)    
    Rate_Video = round(Captura_Video.get(5))
    

    Win_Establecer_Rate = tkinter.Tk()
    Win_Establecer_Rate.config(width=400, height=400)
    Win_Establecer_Rate.geometry('700x230+0+0') 
    Win_Establecer_Rate.title('Video Capture')
    Win_Establecer_Rate.config(bg = Fun_Rgb(C_Primary))
    
    Win_Establecer_Rate_Can = Canvas(Win_Establecer_Rate, width=700, height=230, bg=Fun_Rgb(C_Primary))
    Win_Establecer_Rate_Can.create_rectangle(10, 10, 690, 220, outline=Fun_Rgb(C_White), width=2)
    Win_Establecer_Rate_Can.create_rectangle(40, 40, 530, 95, outline=Fun_Rgb(C_White), width=1)
    Win_Establecer_Rate_Can.create_rectangle(40, 120, 530, 200, outline=Fun_Rgb(C_White), width=1)
    Win_Establecer_Rate_Can.place(x=0,y=0) 

    Lbl_Win_Establecer_Text_1 = tkinter.Label(Win_Establecer_Rate, bg = Fun_Rgb(C_Primary), 
                                              fg = Fun_Rgb(C_White), text = 'Frames per second in the video:  ' + str(Rate_Video))
    Lbl_Win_Establecer_Text_1.config(font = ('Arial',16))
    Lbl_Win_Establecer_Text_1.place(x=60, y = 50)
    
    Lbl_Win_Establecer_Text_2 = tkinter.Label(Win_Establecer_Rate, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White), text = 'Select the number of frames per second:')
    Lbl_Win_Establecer_Text_2.config(font = ('Arial',16))
    Lbl_Win_Establecer_Text_2.place(x=60, y = 130)
    
    videoDuration = (Captura_Video.get(cv2.CAP_PROP_FRAME_COUNT)+1)/Rate_Video
    miliseconds = 1000/Rate_Video

    def Fun_Cortar(): 
        
        
        if int(entRate.get()) > int(Rate_Video):
            messagebox.showerror("Error", "Frames per second must not exceed original video frames")
            Win_Establecer_Rate.destroy()
        else:
            Aux_Ent_Frame = round(Rate_Video/int(entRate.get()))
            Aux_Ent_Frame_2 = int(entRate.get())
            Aux_Contador = 1
            
            while(Captura_Video.isOpened()):
                Id_Frame = Captura_Video.get(1) 
                ret, Frame = Captura_Video.read()
                if (Aux_Contador == Aux_Ent_Frame):
                    Ruta_Frame = Dir_Project_Img + "/" +  str(int(round((Id_Frame +1) *miliseconds))) + ".jpg"
                    
                    try:
                        cv2.imwrite(Ruta_Frame, Frame)
                    except:
                        break
                    
                    Aux_Contador = 1
                    if (ret != True):
                        break
                else:
                    Aux_Contador += 1
                    if (ret != True):
                        break
                
                
                
            Captura_Video.release()
           
            Win_Establecer_Rate.destroy()
            messagebox.showinfo("Finalized", "Video has been cut")
                
    
    
    
    rate = StringVar()
    
    entRate = Entry(Win_Establecer_Rate, textvariable = rate, bd =1, width = 5)
    entRate.insert('end',str(round(Rate_Video/30)))
    entRate.place(x=100, y = 165)
    CreateToolTip(entRate, text = 'Total frames in the video = ' + str(round(Captura_Video.get(cv2.CAP_PROP_FRAME_COUNT))))
    
    
    lblIgual = Label(Win_Establecer_Rate, text = '= ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblIgual.config(font = ('Arial',12))
    lblIgual.place(x=150, y = 164)
    
    totalFrames = round(int(entRate.get()) * videoDuration)-1
    lblTotal = Label(Win_Establecer_Rate, text = str(totalFrames) + ' Total frames', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblTotal.config(font = ('Arial',12))
    lblTotal.place(x=163, y = 164)
    
    def Fun_Cal():
        entRate.get()
        totalFrames = round(int(entRate.get()) * videoDuration)-1
       
        lblTotal.destroy()
        lblTotal1 = Label(Win_Establecer_Rate, text = str(totalFrames) + ' Total frames', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
        lblTotal1.config(font = ('Arial',12))
        lblTotal1.place(x=163, y = 164)
        
    Btn_Win_Establecer = tkinter.Button(Win_Establecer_Rate,  bd=1, fg = Fun_Rgb(C_White),
                                      bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),
                                      highlightbackground=Fun_Rgb(C_Light_Dark),
                                      text = 'Accept', command = Fun_Cortar)
    Btn_Win_Establecer.config(font = ('Arial',20))
    Btn_Win_Establecer.place(x=570, y=151.5)
    
    Btn_Cal_Rate = tkinter.Button(Win_Establecer_Rate,  bd=1, fg = Fun_Rgb(C_White),
                                      bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),
                                      highlightbackground=Fun_Rgb(C_Light_Dark),
                                      text = 'Total', command = Fun_Cal)
    Btn_Cal_Rate.config(font = ('Arial',14))
    Btn_Cal_Rate.place(x=330, y=160)
    CreateToolTip(Btn_Cal_Rate, text = 'Press to calculate the total frames in the project')

    
    
    Win_Establecer_Rate.mainloop()
#%%Fun openNewObservation
def openNewObservation():
    global Lbl_Img_Original, List_Contenido, pathImageProject, currentPicture
        
    List_Contenido = sorted_aphanumeric(os.listdir(pathImageProject))
    
    img = pathImageProject+str(List_Contenido[currentPicture])
    
    lblNumberImage = Label(canRegister, text='Image '+str(currentPicture)+ ' of '+str(len(List_Contenido)) +'       ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblNumberImage.config(font = (Font_1,15))
    lblNumberImage.place(x=aux_width_monitor*10.5, y=aux_height_monitor*.5)
    
          
    Lbl_Img_Original.place_forget()
    
    Var_Tamaño_Lbl_X = int(((height_monitor/2)*1.99)-(aux_width_monitor*1.4))
    Var_Tamaño_Lbl_Y = int(((height_monitor/2)*1.37)-(aux_width_monitor*1.3))
    
    
    Img_Original= PIL.Image.open(img)
    
    if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
        if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
            Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
    elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
        if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
            Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
    else:
        Img_Original_2 = Img_Original
            
    # global Lbl_Img_Original, Lbl_Img_Original_Aux
    Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesPrincipal, image=Photo_Img_Original, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Original
    Lbl_Img_Original.place(x = (aux_width_monitor*1)+1, y = (aux_height_monitor*1)+1)
    
    return List_Contenido, pathImageProject

#%%Fun openNewProject
def openNewProject():
    global Lbl_Img_Original, List_Contenido, pathImageProject, currentPicture
    
    textEnt.delete('1.0', END)
    textEnt.insert(INSERT, 'Time (ms)              Subject            Behavior           Observation')
    
    currentPicture = 0
    
    List_Contenido = sorted_aphanumeric(os.listdir(pathImageProject))
    
    img = pathImageProject+str(List_Contenido[currentPicture])
    
    lblNumberImage = Label(canRegister, text='Image '+str(currentPicture)+ ' of '+str(len(List_Contenido)) +'       ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblNumberImage.config(font = (Font_1,15))
    lblNumberImage.place(x=aux_width_monitor*10.5, y=aux_height_monitor*.5)
    
          
    Lbl_Img_Original.place_forget()
    
    Var_Tamaño_Lbl_X = int(((height_monitor/2)*1.99)-(aux_width_monitor*1.4))
    Var_Tamaño_Lbl_Y = int(((height_monitor/2)*1.37)-(aux_width_monitor*1.3))
    
    
    Img_Original= PIL.Image.open(img)
    
    if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
        if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
            Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
    elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
        if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
            Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
    else:
        Img_Original_2 = Img_Original
            
    # global Lbl_Img_Original, Lbl_Img_Original_Aux
    Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesPrincipal, image=Photo_Img_Original, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Original
    Lbl_Img_Original.place(x = (aux_width_monitor*1)+1, y = (aux_height_monitor*1)+1)
    
    return List_Contenido, pathImageProject
#%%Fun newProject
def newProject():
    global Lbl_Img_Original, List_Contenido, pathImageProject, currentPicture
    
    textEnt.delete('1.0', END)
    textEnt.insert(INSERT, 'Time (ms)              Subject            Behavior           Observation')
    
    pathImageProject = filedialog.askdirectory(initialdir=Dir_Projects,
                title="Select Image Directory")+'/'
    
    
    currentPicture = 0
    List_Contenido = sorted_aphanumeric(os.listdir(pathImageProject))
    
    img = pathImageProject+str(List_Contenido[currentPicture])
    
    lblNumberImage = Label(canRegister, text='Image '+str(currentPicture)+ ' of '+str(len(List_Contenido)) +'       ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblNumberImage.config(font = (Font_1,15))
    lblNumberImage.place(x=aux_width_monitor*10.5, y=aux_height_monitor*.5)
    
          
    Lbl_Img_Original.place_forget()
    
    Var_Tamaño_Lbl_X = int(((height_monitor/2)*1.99)-(aux_width_monitor*1.4))
    Var_Tamaño_Lbl_Y = int(((height_monitor/2)*1.37)-(aux_width_monitor*1.3))
    
    
    Img_Original= PIL.Image.open(img)
    
    if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
        if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
            Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
    elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
        if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
            Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
    else:
        Img_Original_2 = Img_Original
            
    # global Lbl_Img_Original, Lbl_Img_Original_Aux
    Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesPrincipal, image=Photo_Img_Original, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Original
    Lbl_Img_Original.place(x = (aux_width_monitor*1)+1, y = (aux_height_monitor*1)+1)
    
    return List_Contenido, pathImageProject
#%%Fun newProjectAux
def newProjectAux():
    global currentProject
    
    if currentProject > 0:
        mensaje1 =messagebox.askyesno(message= 'You have a current project. Do you saved it?', title="Current project")
        
        if mensaje1==False:
            print('saved it!')
        else:
            newProject()
    
    else:
        currentProject += 1
        newProject()
        
        

#%%Fun nextImage        
def nextImage():
    global currentPicture, Lbl_Img_Original, text
    currentPicture +=1
    
    if currentPicture == len(List_Contenido):
        currentPicture = len(List_Contenido)-1
     
    lblNumberImage = Label(canRegister, text='Image '+str(currentPicture)+ ' of '+str(len(List_Contenido)) + '       ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblNumberImage.config(font = (Font_1,15))
    lblNumberImage.place(x=aux_width_monitor*10.5, y=aux_height_monitor*.5)
    
    img = pathImageProject+str(List_Contenido[currentPicture])
        
    Lbl_Img_Original.place_forget()
    
    Var_Tamaño_Lbl_X = int(((height_monitor/2)*1.99)-(aux_width_monitor*1.4))
    Var_Tamaño_Lbl_Y = int(((height_monitor/2)*1.37)-(aux_width_monitor*1.3))
    
    Img_Original= PIL.Image.open(img)
    
    if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
        if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
            Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
    elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
        if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
            Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
    else:
        Img_Original_2 = Img_Original
            
    Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesPrincipal, image=Photo_Img_Original, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Original
    Lbl_Img_Original.place(x = (aux_width_monitor*1)+1, y = (aux_height_monitor*1)+1)
 

#%%Fun prevImage        
def prevImage():
    global currentPicture, Lbl_Img_Original
    currentPicture -=1
    
    if currentPicture <= 0:
        currentPicture = 0
    
    img = pathImageProject+str(List_Contenido[currentPicture])
    
    lblNumberImage = Label(canRegister, text='Image '+str(currentPicture)+ ' of '+str(len(List_Contenido)) +'       ', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
    lblNumberImage.config(font = (Font_1,15))
    lblNumberImage.place(x=aux_width_monitor*10.5, y=aux_height_monitor*.5)
    
    Lbl_Img_Original.place_forget()
    
    Var_Tamaño_Lbl_X = int(((height_monitor/2)*1.99)-(aux_width_monitor*1.4))
    Var_Tamaño_Lbl_Y = int(((height_monitor/2)*1.37)-(aux_width_monitor*1.3))
    
    Img_Original= PIL.Image.open(img)
    
    if int(Img_Original.size[0])>=Var_Tamaño_Lbl_X:
        Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
        if int(Img_Original_2.size[1]) >= Var_Tamaño_Lbl_Y:
            Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
    elif int(Img_Original.size[1])>=Var_Tamaño_Lbl_Y:
        Img_Original_2 = Img_Original.resize((round((Var_Tamaño_Lbl_Y/int(Img_Original.size[1]))*int(Img_Original.size[0])),Var_Tamaño_Lbl_Y))
        if int(Img_Original_2.size[0]) >= Var_Tamaño_Lbl_X:
            Img_Original_2 = Img_Original.resize((Var_Tamaño_Lbl_X,round((Var_Tamaño_Lbl_X/int(Img_Original.size[0]))*int(Img_Original.size[1]))))
    else:
        Img_Original_2 = Img_Original
            
    Photo_Img_Original = ImageTk.PhotoImage(Img_Original_2)
    Lbl_Img_Original = tkinter.Label(pesPrincipal, image=Photo_Img_Original, bg = Fun_Rgb(C_Primary), bd = 0)
    Lbl_Img_Original.image = Photo_Img_Original
    Lbl_Img_Original.place(x = (aux_width_monitor*1)+1, y = (aux_height_monitor*1)+1)


#%%Fun showText
def showTextSub1():
    global currentPicture
    timePicture = List_Contenido[currentPicture].split('.jpg')
    timePicture = str(timePicture[0])
    textEnt.insert(INSERT, '\n' +timePicture)
    
    for i in range(30):
        if i >= len(timePicture) * 2:
            textEnt.insert(INSERT, ' ' )
    textEnt.insert(INSERT, str(sub1.get()))  
    
    for i in range(20):
        if i >= len(str(sub1.get())):
            textEnt.insert(INSERT, ' ' )

def showTextSub2():
    global currentPicture
    timePicture = List_Contenido[currentPicture].split('.jpg')
    timePicture = str(timePicture[0])
    textEnt.insert(INSERT, '\n' +timePicture)
    
    for i in range(30):
        if i >= len(timePicture) * 2:
            textEnt.insert(INSERT, ' ' )
    textEnt.insert(INSERT, str(sub2.get()))   
    
    for i in range(20):
        if i >= len(str(sub2.get())):
            textEnt.insert(INSERT, ' ' )

def showTextSub3():
    global currentPicture
    timePicture = List_Contenido[currentPicture].split('.jpg')
    timePicture = str(timePicture[0])
    textEnt.insert(INSERT, '\n' +timePicture)
    
    for i in range(30):
        if i >= len(timePicture) * 2:
            textEnt.insert(INSERT, ' ' )
    textEnt.insert(INSERT, str(sub3.get()))
    
    for i in range(20):
        if i >= len(str(sub3.get())):
            textEnt.insert(INSERT, ' ' )

def showTextSub4():
    global currentPicture
    timePicture = List_Contenido[currentPicture].split('.jpg')
    timePicture = str(timePicture[0])
    textEnt.insert(INSERT, '\n' +timePicture)
    
    for i in range(30):
        if i >= len(timePicture) * 2:
            textEnt.insert(INSERT, ' ' )
    textEnt.insert(INSERT, str(sub4.get()))
    
    for i in range(20):
        if i >= len(str(sub4.get())):
            textEnt.insert(INSERT, ' ' )

def showTextSub5():
    global currentPicture
    timePicture = List_Contenido[currentPicture].split('.jpg')
    timePicture = str(timePicture[0])
    textEnt.insert(INSERT, '\n' +timePicture)
    
    for i in range(30):
        if i >= len(timePicture) * 2:
            textEnt.insert(INSERT, ' ' )
    textEnt.insert(INSERT, str(sub5.get()))
    
    for i in range(20):
        if i >= len(str(sub5.get())):
            textEnt.insert(INSERT, ' ' )
            

def showTextBeh1():
    textEnt.insert(INSERT, str(beh1.get()))
    
    for i in range(20):
        if i >= len(str(beh1.get())):
            textEnt.insert(INSERT, ' ' )

def showTextBeh2():
    textEnt.insert(INSERT, str(beh2.get()))
    
    for i in range(20):
        if i >= len(str(beh2.get())):
            textEnt.insert(INSERT, ' ' )

def showTextBeh3():
    textEnt.insert(INSERT, str(beh3.get()))
    
    for i in range(20):
        if i >= len(str(beh3.get())):
            textEnt.insert(INSERT, ' ' )

def showTextBeh4():
    textEnt.insert(INSERT, str(beh4.get()))
    
    for i in range(20):
        if i >= len(str(beh4.get())):
            textEnt.insert(INSERT, ' ' )

def showTextBeh5():
    textEnt.insert(INSERT, str(beh5.get()))
    
    for i in range(20):
        if i >= len(str(beh5.get())):
            textEnt.insert(INSERT, ' ' )

def showTextBeh6():
    textEnt.insert(INSERT, str(beh6.get()))
    
    for i in range(20):
        if i >= len(str(beh6.get())):
            textEnt.insert(INSERT, ' ' )

def showTextBeh7():
    textEnt.insert(INSERT, str(beh7.get()))
    
    for i in range(20):
        if i >= len(str(beh7.get())):
            textEnt.insert(INSERT, ' ' )
            
def showTextBeh8():
    textEnt.insert(INSERT, str(beh8.get()))
    
    for i in range(20):
        if i >= len(str(beh8.get())):
            textEnt.insert(INSERT, ' ' )
            
def showTextBeh9():
    textEnt.insert(INSERT, str(beh9.get()))
    
    for i in range(20):
        if i >= len(str(beh9.get())):
            textEnt.insert(INSERT, ' ' )
            
def showTextBeh10():
    textEnt.insert(INSERT, str(beh10.get()))
    
    for i in range(20):
        if i >= len(str(beh10.get())):
            textEnt.insert(INSERT, ' ' )

#%%Fun saveObservation
def saveObservation():
    global currentProject, pathImageProject
    
    if currentProject == 0:
        message = messagebox.showerror(message="You don't have a current project", title='Error')
    
    
    else:   
        aux_pathImageProject = pathImageProject.split('Images/')  
        aux_pathImageProject = str(aux_pathImageProject[0])
        
        pathNameObservation =  filedialog.asksaveasfilename(initialdir = aux_pathImageProject,
                                    title = "Save observation",
                                    filetypes = (("all files","*.*"),
                                    ("jpeg files","*.jpg")))
        
        Archivo_Frames = open(pathNameObservation + '.txt','w')
        Archivo_Frames.write(str(pathImageProject)+'\n')
        Archivo_Frames.write(str(currentPicture)+'\n')
        Archivo_Frames.write(str(sub1.get())+'\n')
        Archivo_Frames.write(str(sub2.get())+'\n')
        Archivo_Frames.write(str(sub3.get())+'\n')
        Archivo_Frames.write(str(sub4.get())+'\n')
        Archivo_Frames.write(str(sub5.get())+'\n')
        Archivo_Frames.write(str(beh1.get())+'\n')
        Archivo_Frames.write(str(beh2.get())+'\n')
        Archivo_Frames.write(str(beh3.get())+'\n')
        Archivo_Frames.write(str(beh4.get())+'\n')
        Archivo_Frames.write(str(beh5.get())+'\n')
        Archivo_Frames.write(str(beh6.get())+'\n')
        Archivo_Frames.write(str(beh7.get())+'\n')
        Archivo_Frames.write(str(beh8.get())+'\n')
        Archivo_Frames.write(str(beh9.get())+'\n')
        Archivo_Frames.write(str(beh10.get())+'\n')
        Archivo_Frames.write('\n')
        Archivo_Frames.write(str(textEnt.get("1.0",END))+'\n')
        Archivo_Frames.close()
 
#%%Fun saveProject       
def saveProject():
    global currentProject, pathImageProject
    
    if currentProject == 0:
        message = messagebox.showerror(message="You don't have a current project", title='Error')
    
    
    else:   
        aux_pathImageProject = pathImageProject.split('Images/')  
        aux_pathImageProject = str(aux_pathImageProject[0])
        
        Archivo_Frames = open(aux_pathImageProject + 'data_project' + '.txt','w')
        Archivo_Frames.write(str(pathImageProject)+'\n')
        Archivo_Frames.write(str(currentPicture)+'\n')
        Archivo_Frames.write(str(sub1.get())+'\n')
        Archivo_Frames.write(str(sub2.get())+'\n')
        Archivo_Frames.write(str(sub3.get())+'\n')
        Archivo_Frames.write(str(sub4.get())+'\n')
        Archivo_Frames.write(str(sub5.get())+'\n')
        Archivo_Frames.write(str(beh1.get())+'\n')
        Archivo_Frames.write(str(beh2.get())+'\n')
        Archivo_Frames.write(str(beh3.get())+'\n')
        Archivo_Frames.write(str(beh4.get())+'\n')
        Archivo_Frames.write(str(beh5.get())+'\n')
        Archivo_Frames.write(str(beh6.get())+'\n')
        Archivo_Frames.write(str(beh7.get())+'\n')
        Archivo_Frames.write(str(beh8.get())+'\n')
        Archivo_Frames.write(str(beh9.get())+'\n')
        Archivo_Frames.write(str(beh10.get())+'\n')
        Archivo_Frames.close()  
        
        messagebox.showinfo(message="Regestry has been saved", title="Save")

#%%Fun openProject
def openProject():
    global currentPicture, pathImageProject, currentProject
    currentProject += 1
    path = filedialog.askopenfilename(initialdir = Dir_Projects,
                                            title = "Select File",
                                            filetypes = (("txt files","*.txt"),
                                            ("mp4 files","*.mp4")))
    
    Dir_Parametros =open(path,'r')  
    Arr_Parametros = Dir_Parametros.read().split('\n') 
    Dir_Parametros.close()
    
    pathImageProject = Arr_Parametros[0]
    currentPicture = int(Arr_Parametros[1])
    sub1.set(Arr_Parametros[2])
    sub2.set(Arr_Parametros[3])    
    sub3.set(Arr_Parametros[4])  
    sub4.set(Arr_Parametros[5])  
    sub5.set(Arr_Parametros[6]) 
    
    beh1.set(Arr_Parametros[7])
    beh2.set(Arr_Parametros[8])
    beh3.set(Arr_Parametros[9])
    beh4.set(Arr_Parametros[10])
    beh5.set(Arr_Parametros[11])
    beh6.set(Arr_Parametros[12])
    beh7.set(Arr_Parametros[13])
    beh8.set(Arr_Parametros[14])
    beh9.set(Arr_Parametros[15])
    beh10.set(Arr_Parametros[16])
    
    openNewProject()

#%%Fun openObservation
def openObservation():
    global currentPicture, pathImageProject, currentProject
    currentProject += 1
    path = filedialog.askopenfilename(initialdir = Dir_Projects,
                                            title = "Select File",
                                            filetypes = (("txt files","*.txt"),
                                            ("mp4 files","*.mp4")))
    
    Dir_Parametros =open(path,'r')  
    Arr_Parametros = Dir_Parametros.read().split('\n') 
    Dir_Parametros.close()
    
    pathImageProject = Arr_Parametros[0]
    currentPicture = int(Arr_Parametros[1])
    sub1.set(Arr_Parametros[2])
    sub2.set(Arr_Parametros[3])    
    sub3.set(Arr_Parametros[4])  
    sub4.set(Arr_Parametros[5])  
    sub5.set(Arr_Parametros[6]) 
    
    beh1.set(Arr_Parametros[7])
    beh2.set(Arr_Parametros[8])
    beh3.set(Arr_Parametros[9])
    beh4.set(Arr_Parametros[10])
    beh5.set(Arr_Parametros[11])
    beh6.set(Arr_Parametros[12])
    beh7.set(Arr_Parametros[13])
    beh8.set(Arr_Parametros[14])
    beh9.set(Arr_Parametros[15])
    beh10.set(Arr_Parametros[16])
    
    j = 0
    for i in Arr_Parametros:
        j +=1 
        if j >= 18:
            try: 
                aux_parameter = Arr_Parametros[j] 
                textEnt.insert(INSERT, aux_parameter+ '\n')
            except:
                j = 0
    
    openNewObservation()
    
#%%-------------WIDGETS-------------
#%%Principal window
root = Tk()
root.title('Image Classification System v-0.1')
root.geometry(str(width_monitor)+'x'+str(height_monitor-100)+'+0+0') 
root.config(bg = Fun_Rgb(C_Primary))
root.isStopped = False

#%%Global variables   
global Lbl_Img_Original, List_Contenido, pathImageProject, textEnt, currentProject, openProjectVar

currentProject = 0                
Lbl_Img_Original = Label(root, bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
List_Contenido = []
pathImageProject = ''
currentPicture = 0
openProjectVar = 0

#%%Toolbar and menu
toolbar = Frame(root)

img1 = PIL.Image.open(Dir_Images+'options.png')
useImg1 = ImageTk.PhotoImage(img1)
img2 = PIL.Image.open(Dir_Images+'cut_video.png')
useImg2 = ImageTk.PhotoImage(img2)
img3 = PIL.Image.open(Dir_Images+'new.png')
useImg3 = ImageTk.PhotoImage(img3)
img4 = PIL.Image.open(Dir_Images+'open.png')
useImg4 = ImageTk.PhotoImage(img4)
img5 = PIL.Image.open(Dir_Images+'save.png')
useImg5 = ImageTk.PhotoImage(img5)
img6 = PIL.Image.open(Dir_Images+'new_observation.png')
useImg6 = ImageTk.PhotoImage(img6)
img7 = PIL.Image.open(Dir_Images+'open_observation.png')
useImg7 = ImageTk.PhotoImage(img7)
img8 = PIL.Image.open(Dir_Images+'data.png')
useImg8 = ImageTk.PhotoImage(img8)
img9 = PIL.Image.open(Dir_Images+'user.png')
useImg9 = ImageTk.PhotoImage(img9)


iconTool_Options = Button(toolbar, image=useImg1, text="Options", width=20, command=info)
iconTool_Options.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_Options, text = 'Contact information')

iconTool_CutVideo = Button(toolbar, image=useImg2, text="Cut Video", width=20, command=cutVideo)
iconTool_CutVideo.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_CutVideo, text = 'Cut video')

iconNewProject = Button(toolbar, image=useImg3, text="New project", width=20, command=newProjectAux)
iconNewProject.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconNewProject, text = 'New project')

openFile = Button(toolbar, image=useImg4, text="Open", width=20, command=openProject)
openFile.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(openFile, text = 'Open project')

saveButton = Button(toolbar, image=useImg5, text="Save", width=20, command=saveProject)
saveButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(saveButton, text = 'Save project')

iconNewObservation = Button(toolbar, image=useImg6, text="Observation", width=20, command= openProject)
iconNewObservation.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconNewObservation, text = 'New observation')

iconOpenObservation = Button(toolbar, image=useImg7, text="Observation", width=20, command= openObservation)
iconOpenObservation.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconOpenObservation, text = 'Open observation')

closeButton = Button(toolbar, image=useImg8, text="Data", width=20)#, command=close_WPI_Connection)
closeButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(closeButton, text = 'Data analysis')

checkInputButton = Button(toolbar, image=useImg9, text="User", width=20)#, command=check_Input_1)
checkInputButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(checkInputButton, text = 'User information')



toolbar.pack(side=TOP, fill=X)

menubar = tkinter.Menu(root)
root.config(menu=menubar)

Menu_Opc1 = tkinter.Menu(root, bg=Fun_Rgb(C_White), fg=Fun_Rgb(C_Primary),
                             activebackground=Fun_Rgb(C_Grey), activeforeground=Fun_Rgb(C_Light_Dark),
                             tearoff=0)                         
menubar.add_cascade(label="File", menu=Menu_Opc1)
Menu_Opc1.add_command(label='Cut video', command=cutVideo) 
Menu_Opc1.add_command(label='New project', command = newProjectAux)
Menu_Opc1.add_command(label='Open project', command = openProject)
Menu_Opc1.add_command(label='Save project', command = saveProject)
Menu_Opc1.add_command(label='New observation', command = openProject)
Menu_Opc1.add_command(label='Open observation', command = openObservation)
Menu_Opc1.add_command(label='Data analysis')
Menu_Opc1.add_command(label='User information')
Menu_Opc1.add_command(label='License', command=info)  


#%%Notebooks
style = ttk.Style()
settings = {"TNotebook.Tab": {"configure": {"padding": [5, 1],
                                            "background": Fun_Rgb(C_Grey)
                                           },
                              "map": {"background": [("selected", Fun_Rgb(C_Primary)), 
                                                     ("active", Fun_Rgb(C_White))],
                                      
                                      "foreground": [("selected", Fun_Rgb(C_White)),
                                                     ("active", "#000000")]

                                     }
                              }
           }  


style.theme_create("mi_estilo", parent="alt", settings=settings)
style.theme_use("mi_estilo")

notebook = ttk.Notebook(root)
notebook.pack(fill = 'both', expand = 'yes')
pesRename = tkinter.Frame(notebook, background = Fun_Rgb(C_Primary))
pesPrincipal = tkinter.Frame(notebook, background = Fun_Rgb(C_Primary))

notebook.add(pesRename, text = 'Set variable names')
notebook.add(pesPrincipal, text = 'Registry')


#%%Canvas notebook rename
canSubjects = Canvas(pesRename, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

canSubjects.create_rectangle(int(aux_width_monitor*1.5), int(aux_height_monitor*1.5), int(aux_width_monitor*13.5), int(aux_width_monitor*2), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canSubjects.create_rectangle(int(aux_width_monitor*1.5), int(aux_height_monitor*5), int(aux_width_monitor*13.5), int(aux_width_monitor*5), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canSubjects.place(x=0,y=0) 


#%%Labels and entries of notebook rename         
lblSubjects = Label(pesRename, text="Subjects", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblSubjects.config(font = (Font_1,15))
lblSubjects.place(x=aux_width_monitor*1.5, y=aux_height_monitor*1)

sub1 = StringVar()
sub2 = StringVar()
sub3 = StringVar()
sub4 = StringVar()
sub5 = StringVar()

lblSubjects1 = Label(pesRename, text="Subject 1", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects1.config(font = (Font_1,12))
lblSubjects1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*2)

entSub1 = Entry(pesRename, textvariable = sub1, bd =1)
entSub1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*2.5)

lblSubjects2 = Label(pesRename, text="Subject 2", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects2.config(font = (Font_1,12))
lblSubjects2.place(x=aux_width_monitor*4.25, y=aux_height_monitor*2)

entSub2 = Entry(pesRename, textvariable = sub2, bd =1)
entSub2.place(x=aux_width_monitor*4.25, y=aux_height_monitor*2.5)

lblSubjects3 = Label(pesRename, text="Subject 3", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects3.config(font = (Font_1,12))
lblSubjects3.place(x=aux_width_monitor*6.75, y=aux_height_monitor*2)

entSub3 = Entry(pesRename, textvariable = sub3, bd =1)
entSub3.place(x=aux_width_monitor*6.75, y=aux_height_monitor*2.5)

lblSubjects4 = Label(pesRename, text="Subject 4", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects4.config(font = (Font_1,12))
lblSubjects4.place(x=aux_width_monitor*9.25, y=aux_height_monitor*2)

entSub4 = Entry(pesRename, textvariable = sub4, bd =1)
entSub4.place(x=aux_width_monitor*9.25, y=aux_height_monitor*2.5)

lblSubjects5 = Label(pesRename, text="Subject 5", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects5.config(font = (Font_1,12))
lblSubjects5.place(x=aux_width_monitor*11.7, y=aux_height_monitor*2)

entSub5 = Entry(pesRename, textvariable = sub5, bd =1)
entSub5.place(x=aux_width_monitor*11.7, y=aux_height_monitor*2.5)



lblBehaviors = Label(pesRename, text="Behaviors", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblBehaviors.config(font = (Font_1,15))
lblBehaviors.place(x=aux_width_monitor*1.5, y=aux_height_monitor*4.5)

beh1 = StringVar()
beh2 = StringVar()
beh3 = StringVar()
beh4 = StringVar()
beh5 = StringVar()
beh6 = StringVar()
beh7 = StringVar()
beh8 = StringVar()
beh9 = StringVar()
beh10 = StringVar()

lblBeh1 = Label(pesRename, text="Behavior 1", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh1.config(font = (Font_1,12))
lblBeh1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*5.5)

entBeh1 = Entry(pesRename, textvariable = beh1, bd =1)
entBeh1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*6)

lblBeh2 = Label(pesRename, text="Behavior 2", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh2.config(font = (Font_1,12))
lblBeh2.place(x=aux_width_monitor*4.25, y=aux_height_monitor*5.5)

entBeh2 = Entry(pesRename, textvariable = beh2, bd =1)
entBeh2.place(x=aux_width_monitor*4.25, y=aux_height_monitor*6)

lblBeh3 = Label(pesRename, text="Behavior 3", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh3.config(font = (Font_1,12))
lblBeh3.place(x=aux_width_monitor*6.75, y=aux_height_monitor*5.5)

entBeh3 = Entry(pesRename, textvariable = beh3, bd =1)
entBeh3.place(x=aux_width_monitor*6.75, y=aux_height_monitor*6)

lblBeh4 = Label(pesRename, text="Behavior 4", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh4.config(font = (Font_1,12))
lblBeh4.place(x=aux_width_monitor*9.25, y=aux_height_monitor*5.5)

entBeh4 = Entry(pesRename, textvariable = beh4, bd =1)
entBeh4.place(x=aux_width_monitor*9.25, y=aux_height_monitor*6)

lblBeh5 = Label(pesRename, text="Behavior 5", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh5.config(font = (Font_1,12))
lblBeh5.place(x=aux_width_monitor*11.7, y=aux_height_monitor*5.5)

entBeh5 = Entry(pesRename, textvariable = beh5, bd =1)
entBeh5.place(x=aux_width_monitor*11.7, y=aux_height_monitor*6)

lblBeh6 = Label(pesRename, text="Behavior 6", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh6.config(font = (Font_1,12))
lblBeh6.place(x=aux_width_monitor*1.75, y=aux_height_monitor*7)

entBeh6 = Entry(pesRename, textvariable = beh6, bd =1)
entBeh6.place(x=aux_width_monitor*1.75, y=aux_height_monitor*7.5)

lblBeh7 = Label(pesRename, text="Behavior 7", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh7.config(font = (Font_1,12))
lblBeh7.place(x=aux_width_monitor*4.25, y=aux_height_monitor*7)

entBeh7 = Entry(pesRename, textvariable = beh7, bd =1)
entBeh7.place(x=aux_width_monitor*4.25, y=aux_height_monitor*7.5)

lblBeh8 = Label(pesRename, text="Behavior 8", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh8.config(font = (Font_1,12))
lblBeh8.place(x=aux_width_monitor*6.75, y=aux_height_monitor*7)

entBeh8 = Entry(pesRename, textvariable = beh8, bd =1)
entBeh8.place(x=aux_width_monitor*6.75, y=aux_height_monitor*7.5)

lblBeh9 = Label(pesRename, text="Behavior 9", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh9.config(font = (Font_1,12))
lblBeh9.place(x=aux_width_monitor*9.25, y=aux_height_monitor*7)

entBeh9 = Entry(pesRename, textvariable = beh9, bd =1)
entBeh9.place(x=aux_width_monitor*9.25, y=aux_height_monitor*7.5)

lblBeh10 = Label(pesRename, text="Behavior 10", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblBeh10.config(font = (Font_1,12))
lblBeh10.place(x=aux_width_monitor*11.7, y=aux_height_monitor*7)

entBeh10 = Entry(pesRename, textvariable = beh10, bd =1)
entBeh10.place(x=aux_width_monitor*11.7, y=aux_height_monitor*7.5)


#%%Canvas notebook pesPrincipal
canRegister = Canvas(pesPrincipal, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

canRegister.create_rectangle(int(aux_width_monitor*1), int(aux_height_monitor*1), int(aux_width_monitor*8), int(aux_height_monitor*9), fill=Fun_Rgb(C_Dark), outline=Fun_Rgb(C_White), width=.1)
canRegister.create_rectangle(int(aux_width_monitor*14), int(aux_height_monitor*3), int(aux_width_monitor*8.5), int(aux_width_monitor*3), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canRegister.create_rectangle(int(aux_width_monitor*14), int(aux_height_monitor*6), int(aux_width_monitor*8.5), int(aux_width_monitor*6), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canRegister.place(x=0,y=0) 

#%%Buttons pesPrincipal
btnBacktImg = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Prev', command = prevImage)
btnBacktImg.config(font = ("Arial",20))
btnBacktImg.place(x=aux_width_monitor*8.5, y=aux_height_monitor*1)
# CreateToolTip(btnBacktImg, text = 'Previous image')


btnNextImg = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Next ', command = nextImage)
btnNextImg.config(font = ("Arial",20))
btnNextImg.place(x=aux_width_monitor*11.6, y=aux_height_monitor*1)
# CreateToolTip(btnNextImg, text = 'Next image')

btnSave = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Save Observation', command = saveObservation)
btnSave.config(font = ("Arial",15))
btnSave.place(x=aux_width_monitor*8.5, y=aux_height_monitor*11.2)
CreateToolTip(btnSave, text = 'Save observation')

btnFinish = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Light_Dark),
    highlightbackground=Fun_Rgb(C_Light_Dark), width=13, height = 2,
    text = 'Finish')#, command = cmd_Next)
btnFinish.config(font = ("Arial",15))
btnFinish.place(x=aux_width_monitor*12.1, y=aux_height_monitor*11.2)
CreateToolTip(btnFinish, text = 'Finish record')

btnSubj1 = tkinter.Button(pesPrincipal, bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = sub1, command = showTextSub1)
btnSubj1.config(font = ("Arial",13))
btnSubj1.place(x=aux_width_monitor*8.8, y=aux_height_monitor*3.5)

btnSubj2 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = sub2, command = showTextSub2)
btnSubj2.config(font = ("Arial",13))
btnSubj2.place(x=aux_width_monitor*10.7, y=aux_height_monitor*3.5)

btnSubj3 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = sub3, command = showTextSub3)
btnSubj3.config(font = ("Arial",13))
btnSubj3.place(x=aux_width_monitor*12.5, y=aux_height_monitor*3.5)

btnSubj4 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = sub4, command = showTextSub4)
btnSubj4.config(font = ("Arial",13))
btnSubj4.place(x=aux_width_monitor*8.8, y=aux_height_monitor*4.5)

btnSubj5 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = sub5, command = showTextSub5)
btnSubj5.config(font = ("Arial",13))
btnSubj5.place(x=aux_width_monitor*10.7, y=aux_height_monitor*4.5)


btnBeh1 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh1, command = showTextBeh1)
btnBeh1.config(font = ("Arial",13))
btnBeh1.place(x=aux_width_monitor*8.8, y=aux_height_monitor*6.5)

btnBeh2 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh2, command = showTextBeh2)
btnBeh2.config(font = ("Arial",13))
btnBeh2.place(x=aux_width_monitor*10.7, y=aux_height_monitor*6.5)

btnBeh3 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh3, command = showTextBeh3)
btnBeh3.config(font = ("Arial",13))
btnBeh3.place(x=aux_width_monitor*12.5, y=aux_height_monitor*6.5)

btnBeh4 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh4, command = showTextBeh4)
btnBeh4.config(font = ("Arial",13))
btnBeh4.place(x=aux_width_monitor*8.8, y=aux_height_monitor*7.5)

btnBeh5 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh5, command = showTextBeh5)
btnBeh5.config(font = ("Arial",13))
btnBeh5.place(x=aux_width_monitor*10.7, y=aux_height_monitor*7.5)

btnBeh6 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh6, command = showTextBeh6)
btnBeh6.config(font = ("Arial",13))
btnBeh6.place(x=aux_width_monitor*12.5, y=aux_height_monitor*7.5)

btnBeh7 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh7, command = showTextBeh7)
btnBeh7.config(font = ("Arial",13))
btnBeh7.place(x=aux_width_monitor*8.8, y=aux_height_monitor*8.5)

btnBeh8 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh8, command = showTextBeh8)
btnBeh8.config(font = ("Arial",13))
btnBeh8.place(x=aux_width_monitor*10.7, y=aux_height_monitor*8.5)

btnBeh9 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh9, command = showTextBeh9)
btnBeh9.config(font = ("Arial",13))
btnBeh9.place(x=aux_width_monitor*12.5, y=aux_height_monitor*8.5)

btnBeh10 = tkinter.Button(pesPrincipal,  bd=0, fg = Fun_Rgb(C_White),
    bg = Fun_Rgb(C_Dark), activebackground=Fun_Rgb(C_Primary),
    highlightbackground=Fun_Rgb(C_Primary), width=8, height = 1,
    textvariable = beh10, command = showTextBeh10)
btnBeh10.config(font = ("Arial",13))
btnBeh10.place(x=aux_width_monitor*8.8, y=aux_height_monitor*9.5)

#%%Labels in pesPrincipal
lblImage = Label(canRegister, text='Images', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblImage.config(font = (Font_1,15))
lblImage.place(x=aux_width_monitor*8.5, y=aux_height_monitor*.5)

lblSubjects = Label(canRegister, text="Subjects", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblSubjects.config(font = (Font_1,15))
lblSubjects.place(x=aux_width_monitor*8.5, y=aux_height_monitor*2.5)

lblBeh = Label(canRegister, text='Behaviors', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblBeh.config(font = (Font_1,15))
lblBeh.place(x=aux_width_monitor*8.5, y=aux_height_monitor*5.5)

lblReg = Label(canRegister, text='Registry', bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblReg.config(font = (Font_1,15))
lblReg.place(x=aux_width_monitor*1, y=aux_height_monitor*9.5)


#%%Sliders in canRegister
Slider_X1 = tkinter.Scale(canRegister, 
    from_=0, to=1, resolution=0.01,
    orient=tkinter.HORIZONTAL, width = aux_height_monitor*.3,  length=aux_width_monitor*7,
    fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
    activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
    highlightbackground=Fun_Rgb(C_White),
    showvalue=1)
Slider_X1.config(font=(Font_1,11))
Slider_X1.place(x=int(aux_width_monitor*1), y=int(aux_height_monitor*.2))

Slider_X1 = tkinter.Scale(canRegister, 
    from_=0, to=1, resolution=0.01,
    orient=tkinter.VERTICAL, width = aux_width_monitor*.2,  length=aux_height_monitor*8,
    fg=Fun_Rgb(C_White), bg=Fun_Rgb(C_Primary), bd = 0,
    activebackground=Fun_Rgb(C_Primary), troughcolor= Fun_Rgb(C_Light_Dark), 
    highlightbackground=Fun_Rgb(C_White),
    showvalue=1)
Slider_X1.config(font=(Font_1,11))
Slider_X1.place(x=int(aux_width_monitor*.2), y=int(aux_height_monitor*1))

#%%Text space in pesPrincipal
textEnt = Text(canRegister, width = int(aux_width_monitor*1), height = int(aux_height_monitor*.15))
textEnt.config(font=("Arial",10))
textEnt.place(x=aux_width_monitor*1, y=aux_height_monitor*10)

#%%Mainloop
root.mainloop()