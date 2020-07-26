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



# ventanaInicio_Menu = tkinter.Menu(root)
# root.config(menu=ventanaInicio_Menu)

# ventanaInicio_Menu_Opc1 = tkinter.Menu(ventanaInicio_Menu, bg=Fun_Rgb(C_Pal5), fg=Fun_Rgb(C_Black),
#                              activebackground=Fun_Rgb(C_Pal4), activeforeground=Fun_Rgb(C_Black),
#                              tearoff=0)                         
# ventanaInicio_Menu.add_cascade(label="File", menu=ventanaInicio_Menu_Opc1)
# ventanaInicio_Menu_Opc1.add_command(label='Open file', command=read_File) 
# ventanaInicio_Menu_Opc1.add_command(label='Detect WPI port', command=Detect_WPI) 
# ventanaInicio_Menu_Opc1.add_command(label='Stop WPI connection', command=close_WPI_Connection) 
# ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-1', command=check_Input_1)
# ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-2', command=check_Input_2)
# ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-3', command=check_Input_3)
# ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-4', command=check_Input_4)
# ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-5', command=check_Input_5)
# ventanaInicio_Menu_Opc1.add_command(label='Check Inputs WPI-6', command=check_Input_6)
# ventanaInicio_Menu_Opc1.add_command(label='Stop check Inputs', command=stop_check_Input)
# ventanaInicio_Menu_Opc1.add_command(label='License', command=Fun_Lincense)  
# ventanaInicio_Menu_Opc1.add_command(label='Information', command=Fun_WTS) 
# ventanaInicio_Menu_Opc1.add_command(label='Exit', command=exitApp)


menubar = tkinter.Menu(root)
root.config(menu=menubar)

Menu_Opc1 = tkinter.Menu(root, bg=Fun_Rgb(C_White), fg=Fun_Rgb(C_Primary),
                             activebackground=Fun_Rgb(C_White), activeforeground=Fun_Rgb(C_Primary),
                             tearoff=0)                         
menubar.add_cascade(label="File", menu=Menu_Opc1)
Menu_Opc1.add_command(label='Cut video') 
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

#%%Mainloop
root.mainloop()