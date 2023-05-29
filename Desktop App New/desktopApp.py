# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# https://www.javatpoint.com/tkinter-application-to-switch-between-different-page-frames-in-python #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# -*- coding: utf-8 -*-
"""
@author: JORGE PICADO CARINO
"""

from PIL import ImageTk, Image
from tkinter import filedialog
import segmentation, cut, restore, classification
import tkinter as tk  
from tkinter import ttk
import time
  
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
        if(nwidget > 2):
            widgets.destroy()
        
        nwidget += 1


# Funcion para cargar un archivo
def load_file(self):
    clear_frame(self)
    
    num_widgets = 0
    for widgets in self.winfo_children():
        if(num_widgets > 3):
            widgets.destroy()
        
        num_widgets = num_widgets + 1
        
    global image_selected
    self.filename = filedialog.askopenfilename(initialdir=r"C:\Users\jorge\Desktop\galaxy_segmentation\test_images",
                                               title="Select A File",
                                               filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        
    label = tk.Label(self, text='\nLa imagen seleccionada es la siguiente: \n')
    label.pack()
    label.config(font=("Verdana", 16))
    
    label2 = tk.Label(self, text=self.filename[-26:])
    label2.pack()
    
    image_selected = ImageTk.PhotoImage(Image.open(self.filename))
    image_selected_label = tk.Label(self, image=image_selected)
    image_selected_label.pack()
    
    global name
    name = self.filename
    

def show_images(self, path_image):
    
    if(len(self.winfo_children()) == 6):
    
        clear_frame(self)
        
        progressbar = ttk.Progressbar()
        progressbar.place(x=580, y=580, width=200)
        self.update()
        
        global im0, im1, im2, im3
        
        seg_im, mask_im = segmentation.seg_inference(path_image)
        im0 = ImageTk.PhotoImage(Image.open(seg_im))
        progressbar.step(25)
        
        text0 = tk.Label(self, text='Segmentación')
        text0.place(x=110, y=170)
        text0.config(font=("Verdana", 14))
        im0_label = tk.Label(self, image=im0, height=256, width=256)
        im0_label.place(x=50, y=250)
        self.update()
    
        cut_im = cut.cut_inference(path_image, mask_im)
        im1 = ImageTk.PhotoImage(Image.open(cut_im))
        progressbar.step(25)
        
        text1 = tk.Label(self, text='Recorte')
        text1.place(x=440, y=170)
        text1.config(font=("Verdana", 14))
        im1_label = tk.Label(self, image=im1, height=256, width=256)
        im1_label.place(x=350, y=250)
        self.update()
        
        res_im = restore.process_input(cut_im)
        im2 = ImageTk.PhotoImage(Image.open(res_im))
        progressbar.step(25)
        
        text2 = tk.Label(self, text='Restauración')
        text2.place(x=710, y=170)
        text2.config(font=("Verdana", 14))
        im2_label = tk.Label(self, image=im2, height=256, width=256)
        im2_label.place(x=650, y=250)
        self.update()
        
        label_class, confidence_class = classification.class_inference(res_im)
        im3 = ImageTk.PhotoImage(Image.open(path_image))
        progressbar.step(24)
        
        text3 = tk.Label(self, text='Clasificación')
        text3.place(x=1010, y=170)
        text3.config(font=("Verdana", 14))
        im3_label = tk.Label(self, image=im3, height=256, width=256)
        im3_label.place(x=950, y=250)
        
        pred_text = 'Pred: ' + label_class
        text4 = tk.Label(self, text=pred_text)
        text4.place(x=950, y=200)
        
        conf_text = '% de confianza: ' + str(confidence_class)
        text5 = tk.Label(self, text=conf_text)
        text5.place(x=950, y=220)
        self.update()
        
        time.sleep(2)
        
        progressbar.step(1)
        progressbar.place_forget()    
        self.update()


class StartPage(tk.Frame):  
  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="GALAXIES", font=LARGE_FONT)  
        label.pack(pady=10,padx=10)  

        button = tk.Button(self, text="Load File", height=3, width=20, command=lambda: load_file(self))  
        button.pack(side='top', pady=15)

#         altura = tk.Frame.winfo_screenheight(self)
#         anchura = tk.Frame.winfo_screenwidth(self)
        
#         paltura = 1 - (150/altura)
#         panchura = 1 - (150/anchura)
        
#         tamx = anchura * panchura
#         tamy = altura * paltura
        
        button2 = tk.Button(self, text="Start Process", height=3, width=20, command=lambda: show_images(self, name))
        button2.place(x=1120, y=600)
        

class PageOne(tk.Frame):
                  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  
        
        #label = tk.Label(self, text="CLASSIFICATION", font=LARGE_FONT)  
        #label.pack(pady=10,padx=10)  
  
        button1 = tk.Button(self, text="Back to Home", command=lambda: clear_frame(self, controller))  
        button1.place(x=20, y=20)
  
        #label = tk.Label(self, text="Pulse en el boton para cargar \nla imagen que desea clasificar\n")
        #label.pack()
        
        #button2 = tk.Button(self, text="Load File", 
        #                    command=lambda: PageOneFunctions.load_file(self))
        #button2.pack()
  
        # button3 = tk.Button(self, text="Segmentation",  
        #                     command=lambda: controller.show_frame(PageTwo))  
        # button3.place(x=500, y=10)
  
    
class PageTwo(tk.Frame):  
  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="PROCESS", font=LARGE_FONT)  
        label.pack(pady=10,padx=10)  
  
        button1 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.place(x=20, y=10)
        
        label = tk.Label(self, text="Pulse en el boton para llevar a cabo el proceso de segmentación y clasificación\n")
        label.pack()
  
        button2 = tk.Button(self, text="Start Process", command=lambda: show_images(self, name))  
        button2.pack()  
          

name = ''
app = SeaofBTCapp()
app.title("App Desktop")  
app.geometry("600x400")

app.mainloop()