# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# https://www.javatpoint.com/tkinter-application-to-switch-between-different-page-frames-in-python #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# -*- coding: utf-8 -*-
"""
@author: JORGE PICADO CARINO
"""

import sys
sys.path.append(r'C:\Users\jorge\Desktop\Training CNN Model')
import PageOneFunctions, PageTwoFunctions

#Python program for creating an application to switch pages using trinket.  
  
import tkinter as tk  
  
  
LARGE_FONT= ("Verdana", 12)  
  
  
class SeaofBTCapp(tk.Tk):  
  
    def __init__(self, *args, **kwargs):  
          
        tk.Tk.__init__(self, *args, **kwargs)  
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
  
          
class StartPage(tk.Frame):  
  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="GALAXIES", font=LARGE_FONT)  
        label.pack(pady=10,padx=10)  
  
        button = tk.Button(self, text="Classification",
                           height=5,
                           width=20,
                           command=lambda: controller.show_frame(PageOne))  
        button.place(x=100, y=100)  
  
        button2 = tk.Button(self, text="Segmentation",
                            height=5,
                            width=20,
                            command=lambda: controller.show_frame(PageTwo))  
        button2.place(x=350, y=100) 


def clear_frame(self, controller):
    num_widgets = 0
    
    for widgets in self.winfo_children():
        # print(widgets)
        if(num_widgets > 3):
            widgets.destroy()
        
        num_widgets = num_widgets + 1
    
    controller.show_frame(StartPage)
  
class PageOne(tk.Frame):
                  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="CLASSIFICATION", font=LARGE_FONT)  
        label.pack(pady=10,padx=10)  
  
        button1 = tk.Button(self, text="Back to Home",  
                            command=lambda: clear_frame(self, controller))  
        button1.place(x=20, y=10) 
  
        label = tk.Label(self, text="Pulse en el boton para cargar \nla imagen que desea clasificar\n")
        label.pack()
        
        button2 = tk.Button(self, text="Load File", 
                            command=lambda: PageOneFunctions.load_file(self))
        button2.pack()
  
        # button3 = tk.Button(self, text="Segmentation",  
        #                     command=lambda: controller.show_frame(PageTwo))  
        # button3.place(x=500, y=10)
  
class PageTwo(tk.Frame):  
  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="SEGMENTATION", font=LARGE_FONT)  
        label.pack(pady=10,padx=10)  
  
        button1 = tk.Button(self, text="Back to Home",  
                            command=lambda: clear_frame(self, controller))
        button1.place(x=20, y=10)
        
        label = tk.Label(self, text="Pulse en el boton para cargar \nla imagen que desea segmentar\n")
        label.pack()
  
        button2 = tk.Button(self, text="Load File",  
                            command=lambda: PageTwoFunctions.load_file(self))  
        button2.pack()  
          
  
app = SeaofBTCapp()
app.title("App Desktop")  
app.geometry("600x400")

app.mainloop()