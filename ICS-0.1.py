#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 14:13:35 2020

@author: Yancarlo Ojeda 
"""


#%%Libraries 
import tkinter 
import scipy
import imageio
import cv2
import os
import os.path
import re
import time
import random
import math
import statistics
import numpy as np
import serial
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from ast import literal_eval
from scipy import misc, ndimage
from tkinter import PhotoImage, messagebox, ttk, Canvas, filedialog, Tk, Frame, BOTH
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import serial.tools.list_ports
from sqlalchemy.sql.expression import column
from tkinter import font
from tkinter.font import Font
from tkinter.simpledialog import askstring
from screeninfo import get_monitors
import matplotlib.image as mpimg
import PIL.Image
from tkinter import Button, Frame, INSERT, LEFT, RIGHT, Label
from tkinter import  Scrollbar, Text, Tk, TOP, X, Y, filedialog
from PIL import Image, ImageTk
from tkinter import *
import cv2
from screeninfo import get_monitors
import tkinter


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
    img = Image.open(img)
    size_1 = img.size
    width = int(size_1[0]*size)
    height = int(size_1[1]*size)
    img = img.resize((width, height),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img

         
#%%Diectories
Dir_Images = 'Image/'


#%%Global variables    



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

    

#%%Principal window
root = Tk()
root.title('Image Classification System v-0.1')
root.geometry(str(width_monitor)+'x'+str(height_monitor-100)+'+0+0') 
root.config(bg = Fun_Rgb(C_Primary))
root.isStopped = False


#%%Toolbar and menu
toolbar = Frame(root)

img1 = PIL.Image.open(Dir_Images+'options.png')
useImg1 = ImageTk.PhotoImage(img1)
img2 = PIL.Image.open(Dir_Images+'cut_video.png')
useImg2 = ImageTk.PhotoImage(img2)
img3 = PIL.Image.open(Dir_Images+'open.png')
useImg3 = ImageTk.PhotoImage(img3)
img4 = PIL.Image.open(Dir_Images+'save.png')
useImg4 = ImageTk.PhotoImage(img4)
img5 = PIL.Image.open(Dir_Images+'data.png')
useImg5 = ImageTk.PhotoImage(img5)
img6 = PIL.Image.open(Dir_Images+'user.png')
useImg6 = ImageTk.PhotoImage(img6)


iconTool_Options = Button(toolbar, image=useImg1, text="Options", width=20)
iconTool_Options.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_Options, text = 'Options')

iconTool_CutVideo = Button(toolbar, image=useImg2, text="Cut Video", width=20)
iconTool_CutVideo.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(iconTool_CutVideo, text = 'Cut video')

openFile = Button(toolbar, image=useImg3, text="Open", width=20)#, command=read_File)
openFile.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(openFile, text = 'Open project')

saveButton = Button(toolbar, image=useImg4, text="Save", width=20)#, command=Detect_WPI)
saveButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(saveButton, text = 'Save project')

closeButton = Button(toolbar, image=useImg5, text="Data", width=20)#, command=close_WPI_Connection)
closeButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(closeButton, text = 'Data analysis')

checkInputButton = Button(toolbar, image=useImg6, text="User", width=20)#, command=check_Input_1)
checkInputButton.pack(side=LEFT, padx=2, pady=2)
CreateToolTip(checkInputButton, text = 'User information')



toolbar.pack(side=TOP, fill=X)

menubar = tkinter.Menu(root)
root.config(menu=menubar)

Menu_Opc1 = tkinter.Menu(root, bg=Fun_Rgb(C_White), fg=Fun_Rgb(C_Primary),
                             activebackground=Fun_Rgb(C_White), activeforeground=Fun_Rgb(C_Primary),
                             tearoff=0)                         
menubar.add_cascade(label="File", menu=Menu_Opc1)
Menu_Opc1.add_command(label='Cut video')#, command=close_WPI_Connection) 
Menu_Opc1.add_command(label='Open project')
Menu_Opc1.add_command(label='Save project')
Menu_Opc1.add_command(label='Data analysis')
Menu_Opc1.add_command(label='User information')
Menu_Opc1.add_command(label='License')  


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
notebook.add(pesPrincipal, text = 'Registrer')


#%%Canvas to notebook rename
canSubjects = Canvas(pesRename, width=int(width_monitor), height=int(aux_height_monitor*14), bg=Fun_Rgb(C_Primary))

canSubjects.create_rectangle(int(aux_width_monitor*1.5), int(aux_height_monitor*1.5), int(aux_width_monitor*13.5), int(aux_width_monitor*2), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canSubjects.create_rectangle(int(aux_width_monitor*1.5), int(aux_height_monitor*5), int(aux_width_monitor*13.5), int(aux_width_monitor*5), fill=Fun_Rgb(C_Light_Dark), outline=Fun_Rgb(C_White), width=.1)
canSubjects.place(x=0,y=0) 


#%%Labels and entries to notebook rename         
lblSubjects = Label(canSubjects, text="Subjects", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblSubjects.config(font = (Font_1,15))
lblSubjects.place(x=aux_width_monitor*1.5, y=aux_height_monitor*1)

sub1 = StringVar()
sub2 = StringVar()
sub3 = StringVar()
sub4 = StringVar()
sub5 = StringVar()


lblSubjects1 = Label(canSubjects, text="Subject 1", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects1.config(font = (Font_1,12))
lblSubjects1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*2)

entSub1 = Entry(pesRename, textvariable = sub1, bd =1)
entSub1.place(x=aux_width_monitor*1.75, y=aux_height_monitor*2.5)

lblSubjects2 = Label(canSubjects, text="Subject 2", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects2.config(font = (Font_1,12))
lblSubjects2.place(x=aux_width_monitor*4.25, y=aux_height_monitor*2)

entSub2 = Entry(pesRename, textvariable = sub2, bd =1)
entSub2.place(x=aux_width_monitor*4.25, y=aux_height_monitor*2.5)

lblSubjects3 = Label(canSubjects, text="Subject 3", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects3.config(font = (Font_1,12))
lblSubjects3.place(x=aux_width_monitor*6.75, y=aux_height_monitor*2)

entSub3 = Entry(pesRename, textvariable = sub3, bd =1)
entSub3.place(x=aux_width_monitor*6.75, y=aux_height_monitor*2.5)

lblSubjects4 = Label(canSubjects, text="Subject 4", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects4.config(font = (Font_1,12))
lblSubjects4.place(x=aux_width_monitor*9.25, y=aux_height_monitor*2)

entSub4 = Entry(pesRename, textvariable = sub4, bd =1)
entSub4.place(x=aux_width_monitor*9.25, y=aux_height_monitor*2.5)

lblSubjects5 = Label(canSubjects, text="Subject 5", bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects5.config(font = (Font_1,12))
lblSubjects5.place(x=aux_width_monitor*11.7, y=aux_height_monitor*2)

entSub5 = Entry(pesRename, textvariable = sub5, bd =1)
entSub5.place(x=aux_width_monitor*11.7, y=aux_height_monitor*2.5)



lblBehaviors = Label(canSubjects, text="Behaviors", bg = Fun_Rgb(C_Primary), fg = Fun_Rgb(C_White))
lblBehaviors.config(font = (Font_1,15))
lblBehaviors.place(x=aux_width_monitor*1.5, y=aux_height_monitor*4.5)

#%%Labels and buttons in pesPrincipal
lblSubjects5 = Label(pesPrincipal, textvariable=sub1, bg = Fun_Rgb(C_Light_Dark), fg = Fun_Rgb(C_White))
lblSubjects5.config(font = (Font_1,12))
lblSubjects5.place(x=aux_width_monitor*11.7, y=aux_height_monitor*2)

#%%Mainloop
root.mainloop()