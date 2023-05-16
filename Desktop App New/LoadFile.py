# -*- coding: utf-8 -*-
"""
@author: JORGE PICADO CARINO
"""

from PIL import ImageTk, Image
from tkinter import filedialog

import tkinter as tk  

global image_selected

def load_file(self):
    num_widgets = 0
    for widgets in self.winfo_children():
        # print(widgets)
        if(num_widgets > 3):
            widgets.destroy()
        
        num_widgets = num_widgets + 1
        
    global image_selected
    self.filename = filedialog.askopenfilename(initialdir=r"C:\Users\jorge\Desktop\DATASET\test",
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