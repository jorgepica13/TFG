# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# https://www.javatpoint.com/tkinter-application-to-switch-between-different-page-frames-in-python #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# -*- coding: utf-8 -*-
"""
@author: JORGE PICADO CARINO
"""

from PIL import ImageTk, Image
from tkinter import filedialog

import Segmentation, Cut, restore

#Python program for creating an application to switch pages using trinket.  
  
import tkinter as tk  
  
LARGE_FONT= ("Verdana", 12)  

  
class SeaofBTCapp(tk.Tk):  
  
    def __init__(self, *args, **kwargs):  
          
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.state('zoomed')
        
        container = tk.Frame(self)  
  
        container.pack(side="top", fill="both", expand = True)  
  
        container.grid_rowconfigure(0, weight=1)  
        container.grid_columnconfigure(0, weight=1)  
  
        self.frames = {}  
  
        for F in (StartPage, PageOne, PageTwo):  
  
            frame = F(container, self)  
  
            self.frames[F] = frame  
  
            frame.grid(row=0, column=0, sticky="nsew")  
  
        self.show_frame(StartPage)  
  
    def show_frame(self, cont):  
  
        frame = self.frames[cont]  
        frame.tkraise()  

def clear_frame(self):
    nwidget = 0
    
    for widgets in self.winfo_children():
        #print(widgets)
        if(nwidget > 2):
            widgets.destroy()
        
        nwidget += 1
    
    #controller.show_frame(StartPage)
    


# Funcion para cargar un archivo
def load_file(self):
    clear_frame(self)
    
    num_widgets = 0
    for widgets in self.winfo_children():
        # print(widgets)
        if(num_widgets > 3):
            widgets.destroy()
        
        num_widgets = num_widgets + 1
        
    global image_selected
    self.filename = filedialog.askopenfilename(initialdir=r"C:\Users\jorge\Desktop\galaxy_segmentation\test_images",
                                                 title="Select A File",
                                                 filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
    #image_created = classify_image(self.filename)
    
    label = tk.Label(self, text='La imagen seleccionada es la siguiente: \n')
    label.pack()
    label.config(font=("Verdana", 16))
    
    label2 = tk.Label(self, text=self.filename[-26:])
    label2.pack()
    
    image_selected = ImageTk.PhotoImage(Image.open(self.filename))
    
    image_selected_label = tk.Label(self, image=image_selected)
    image_selected_label.pack()
    
    global name
    name = self.filename


class StartPage(tk.Frame):  
  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="GALAXIES", font=LARGE_FONT)  
        label.pack(pady=10,padx=10)  


        button = tk.Button(self, text="Load File",
                           height=5,
                           width=30,
                           command=lambda: load_file(self))  
        button.pack(side='top', pady=50)

        altura = tk.Frame.winfo_screenheight(self)
        anchura = tk.Frame.winfo_screenwidth(self)
        
        paltura = 1 - (150/altura)
        panchura = 1 - (150/anchura)
        
        tamx = anchura * panchura
        tamy = altura * paltura
        
        button2 = tk.Button(self, text="Process",
                           height=3,
                           width=15,
                           command=lambda: controller.show_frame(PageTwo))
        button2.place(x=tamx, y=tamy)  
  
class PageOne(tk.Frame):
                  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  
        
        #label = tk.Label(self, text="CLASSIFICATION", font=LARGE_FONT)  
        #label.pack(pady=10,padx=10)  
  
        button1 = tk.Button(self, text="Back to Home",  
                            command=lambda: clear_frame(self, controller))  
        button1.place(x=20, y=20)
  
        #label = tk.Label(self, text="Pulse en el boton para cargar \nla imagen que desea clasificar\n")
        #label.pack()
        
        #button2 = tk.Button(self, text="Load File", 
        #                    command=lambda: PageOneFunctions.load_file(self))
        #button2.pack()
  
        # button3 = tk.Button(self, text="Segmentation",  
        #                     command=lambda: controller.show_frame(PageTwo))  
        # button3.place(x=500, y=10)
  
    
def show_images(self, path_image):
    print('INICIO')
    
    seg_im, mask_im = Segmentation.seg_inference(path_image)
    
    global im0
    im0 = ImageTk.PhotoImage(Image.open(seg_im))
    
    im0_label = tk.Label(self, image=im0,
                         height=256,
                         width=256)
    im0_label.place(x=50, y=250)
    
    print('SEGMENTATION')
    
    cut_im = Cut.cut_inference(path_image, mask_im)
    
    global im1
    im1 = ImageTk.PhotoImage(Image.open(cut_im))
    
    im1_label = tk.Label(self, image=im1,
                         height=256,
                         width=256)
    im1_label.place(x=350, y=250)
    
    print('RESTORATION')
    
    res_im = restore.process_input(cut_im)
    
    global im2
    im2 = ImageTk.PhotoImage(Image.open(res_im))
    
    im2_label = tk.Label(self, image=im2,
                         height=256,
                         width=256)
    im2_label.place(x=650, y=250)
    
    print('DONE')
    
class PageTwo(tk.Frame):  
  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="PROCESS", font=LARGE_FONT)  
        label.pack(pady=10,padx=10)  
  
        button1 = tk.Button(self, text="Back to Home",  
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x=20, y=10)
        
        label = tk.Label(self, text="Pulse en el boton para llevar a cabo el proceso de segmentación y clasificación\n")
        label.pack()
  
        button2 = tk.Button(self, text="Start Process",  
                            command=lambda: show_images(self, name))  
        button2.pack()  
          

name = ''
app = SeaofBTCapp()
app.title("App Desktop")  
app.geometry("600x400")

print(name)

app.mainloop()