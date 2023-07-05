import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from tkinter import filedialog
import segmentation, cut, restore, classification
from tkinter import ttk
import time
        
def colocarBotonesTrasFoto():
    botonLoadFile.place_forget()
    
    global ruta_imagen
    ruta_imagen = cargarImagen()
    
    imageOr = Image.open(ruta_imagen)
    imageOr = imageOr.resize((256, 256))  # Ajusta el tamaño de la imagen 
    imageOr_tk = ImageTk.PhotoImage(imageOr)
    label_imageOr.configure(image=imageOr_tk)
    label_imageOr.image = imageOr_tk
    
    idImSelec.configure(text=ruta_imagen[-26:])
    
    textoImSelec.place(x=0.4375*ancho_pantalla, y=0.2*alto_pantalla)
    botonHomeScreen.place(x=0.31*ancho_pantalla, y=0.75*alto_pantalla)
    botonStartProcess.place(x=0.51*ancho_pantalla, y=0.75*alto_pantalla)
    label_imageOr.place(x=0.4*ancho_pantalla, y=0.275*alto_pantalla)
    idImSelec.place(x=0.41*ancho_pantalla, y=0.62*alto_pantalla)
    
def proceso_segmentacion():
    segImage, maskImage = segmentation.seg_inference(ruta_imagen)

    imageSeg = Image.open(segImage)
    imageSeg = imageSeg.resize((256, 256))  # Ajusta el tamaño de la imagen 
    imageSeg_tk = ImageTk.PhotoImage(imageSeg)
    label_imageSeg.configure(image=imageSeg_tk)
    label_imageSeg.image = imageSeg_tk
    
    label_imageSeg.place(x=0.05*ancho_pantalla, y=0.25*alto_pantalla)
    textoImSeg.place(x=0.0825*ancho_pantalla, y=0.625*alto_pantalla)
    
    return segImage, maskImage

def proceso_recorte(mask):
    cutImage = cut.cut_inference(ruta_imagen, mask)

    imageRec = Image.open(cutImage)
    imageRec_tk = ImageTk.PhotoImage(imageRec)
    label_imageRec.configure(image=imageRec_tk)
    label_imageRec.image = imageRec_tk
    
    label_imageRec.place(x=0.38*ancho_pantalla, y=0.4225*alto_pantalla, anchor="center")
    textoImRec.place(x=0.36*ancho_pantalla, y=0.625*alto_pantalla)
    
    return cutImage

def calculo_dimRes(dims):
    proporcion = 0.0
    x_dim = 0
    y_dim = 0
    
    if dims[0] < dims[1]:
        proporcion = dims[1]/256
        x_dim = dims[0]/proporcion
        y_dim = 256
    else:
        proporcion = dims[0]/256
        x_dim = 256
        y_dim = dims[1]/proporcion

    return round(x_dim), round(y_dim)
        
    
def proceso_restauracion(cutImage):
    resImage = restore.process_input(cutImage)
    
    imageRes = Image.open(resImage)
    
    if imageRes.size[0] > 256 or imageRes.size[1] > 256:
        x_dim, y_dim = calculo_dimRes(imageRes.size)
        imageRes = imageRes.resize((x_dim, y_dim))  # Ajusta el tamaño de la imagen 
        
    imageRes_tk = ImageTk.PhotoImage(imageRes)
    label_imageRes.configure(image=imageRes_tk)
    label_imageRes.image = imageRes_tk
    
    label_imageRes.place(x=0.615*ancho_pantalla, y=0.4225*alto_pantalla, anchor="center")
    textoImRes.place(x=0.56*ancho_pantalla, y=0.625*alto_pantalla)
    
    return resImage

def proceso_clasificacion(resImage):
    classPred, confPred = classification.class_inference(resImage)
    
    imageOr = Image.open(ruta_imagen)
    imageOr = imageOr.resize((256, 256))  # Ajusta el tamaño de la imagen 
    imageOr_tk = ImageTk.PhotoImage(imageOr)
    label_imageOr.configure(image=imageOr_tk)
    label_imageOr.image = imageOr_tk
    
    label_imageOr.place(x=0.755*ancho_pantalla, y=0.25*alto_pantalla)
    textoImClass.place(x=0.7875*ancho_pantalla, y=0.625*alto_pantalla)
    
    global textResult
    textConfPercen = "PREDICTION: " + classPred.upper() + "\n\n"
    textConfPercen += "CONFIDENCE PERCENTAGE: " + confPred + " %"
    textResult = canvasConfPercen.create_text(ancho_pantalla*0.15,
                                              alto_pantalla*0.035, 
                                              text=textConfPercen, 
                                              font=fuente_resultado,
                                              fill="#FFFFFF",
                                              anchor="n",
                                              justify="center")

    return classPred, confPred

def mostrarFotos():
    textoImSelec.place_forget()
    botonLoadFile.place_forget()
    botonStartProcess.place_forget()
    label_imageOr.place_forget()
    idImSelec.place_forget()
    botonHomeScreen.place_forget()
    
    barra_progreso.place(x=0.35*ancho_pantalla,
                         y=0.75*alto_pantalla,
                         width=0.3*ancho_pantalla,
                         height=0.05*alto_pantalla)

    ventana.update()
    
    segImage, maskImage = proceso_segmentacion()
    barra_progreso.step(20)
    ventana.update()

    cutImage = proceso_recorte(maskImage)
    barra_progreso.step(20)
    ventana.update()
    
    resImage = proceso_restauracion(cutImage)
    barra_progreso.step(40)
    ventana.update()
    
    classPred, confPred = proceso_clasificacion(resImage)
    barra_progreso.step(19.99)
    ventana.update()
    
    time.sleep(2)
    barra_progreso.step(0.01)
    barra_progreso.place_forget()
    
    canvasConfPercen.place(x=0.64*ancho_pantalla, y=0.715*alto_pantalla)
    
    botonHomeScreen.place(x=0.05*ancho_pantalla, y=0.8*alto_pantalla)
    
def canvas_tiene_texto(can):
    # Obtener todos los elementos en el lienzo
    all_items = can.find_all()

    # Verificar si alguno de los elementos es un elemento de texto y tiene contenido
    for item in all_items:
        if can.type(item) == "text":
            text_content = can.itemcget(item, "text")
            if text_content.strip():
                return True

    return False

def volver_inicio():
    textoImSelec.place_forget()
    botonLoadFile.place_forget()
    botonStartProcess.place_forget()
    label_imageOr.place_forget()
    idImSelec.place_forget()
    label_imageSeg.place_forget()
    textoImSeg.place_forget()
    label_imageRec.place_forget()
    textoImRec.place_forget()
    label_imageRes.place_forget()
    textoImRes.place_forget()
    label_imageOr.place_forget()
    textoImClass.place_forget()
    canvasConfPercen.place_forget()
    botonHomeScreen.place_forget()
    
    if canvas_tiene_texto(canvasConfPercen):
        canvasConfPercen.delete(textResult)
    
    botonLoadFile.place(x=0.41*ancho_pantalla, y=0.4*alto_pantalla)
    
def cargarImagen():
    return filedialog.askopenfilename(initialdir=r"C:\Users\jorge\Desktop\galaxy_segmentation\test_images",
                                               title="SELECT AN IMAGE",
                                               filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
    
    
# Crear la ventana
ventana = tk.Tk()
ventana.state("zoomed") # Maximiza la ventana al tamano completo de la pantalla
ventana.configure(bg="white") # Establecer el fondo en blanco

ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
dimensiones_pantalla = str(ancho_pantalla) + 'x' + str(alto_pantalla)

titulo = tk.Canvas(ventana, width=ancho_pantalla, height=alto_pantalla*0.15)
titulo.config(background="#A6A6A6")  # Establecer el color de fondo del canvas
titulo.create_text(ancho_pantalla*0.5,
                   alto_pantalla*0.045, 
                   text='CLASSIFICATION OF GALAXIES',
                   font=('Glacial indifference', 40),
                   fill='#FFFFFF',
                   anchor="n",
                   justify="center")
titulo.pack()

inicio = tk.Canvas(ventana, width=ancho_pantalla*0.9875, height=alto_pantalla*0.745)
inicio.config(background="#FFFFFF")  # Establecer el color de fondo del canvas
inicio.place(x=ancho_pantalla*0.005, y=alto_pantalla*0.16)

# Dibujar el contorno del Canvas
x1, y1 = ancho_pantalla*0.0025, alto_pantalla*0.0025  # Coordenadas del vértice superior izquierdo
x2, y2 = ancho_pantalla*0.9875, alto_pantalla*0.745  # Coordenadas del vértice inferior derecho
inicio.create_line(x1, y1, x2, y1, fill="#A6A6A6", width=5)  # Línea superior
inicio.create_line(x1, y1, x1, y2, fill="#A6A6A6", width=5)  # Línea izquierda
inicio.create_line(x2, y1, x2, y2, fill="#A6A6A6", width=5)  # Línea derecha
inicio.create_line(x1, y2, x2, y2, fill="#A6A6A6", width=5)  # Línea inferior

# Crear una fuente personalizada
fuente_boton = font.Font(family='Glacial indifference', size=20, weight="bold")

# Crear un botón con un diseño personalizado
botonLoadFile = tk.Button(ventana, 
                  text="Load File", 
                  font=fuente_boton, 
                  bg="#A6A6A6", 
                  fg='#FFFFFF',
                  width=int(0.01*ancho_pantalla),
                  height=int(0.0025*alto_pantalla),
                  command=colocarBotonesTrasFoto)
botonLoadFile.place(x=0.41*ancho_pantalla, y=0.4*alto_pantalla) # Colocar el botón en el marco

# Crear un botón con un diseño personalizado
botonStartProcess = tk.Button(ventana, 
                  text="Start Process", 
                  font=fuente_boton, 
                  bg="#169D53", 
                  fg='#FFFFFF',
                  width=int(0.01*ancho_pantalla),
                  height=int(0.0025*alto_pantalla),
                  command=mostrarFotos)

textoImSelec = tk.Label(ventana, 
                        text="Select image:", 
                        font=("Glacial indifference", 18), 
                        fg="#000000", 
                        bg="#FFFFFF", 
                        justify="center")

label_imageOr = tk.Label(ventana)

# Crear una fuente personalizada
fuente_id = font.Font(family='Arimo', size=12, weight="bold")

idImSelec = tk.Label(ventana, 
                        text="", 
                        font=fuente_id, 
                        fg="#000000", 
                        bg="#FFFFFF", 
                        justify="center")

label_imageSeg = tk.Label(ventana)
label_imageRec = tk.Label(ventana, width=256, height=256, bg="#FFFFFF")
label_imageRes = tk.Label(ventana, width=256, height=256, bg="#FFFFFF")

textoImSeg = tk.Label(ventana, 
                        text="SEGMENTATION", 
                        font=("Glacial indifference", 15), 
                        fg="#000000", 
                        bg="#FFFFFF", 
                        justify="center")

textoImRec = tk.Label(ventana, 
                        text="CUT", 
                        font=("Glacial indifference", 15), 
                        fg="#000000", 
                        bg="#FFFFFF", 
                        justify="center")

textoImRes = tk.Label(ventana, 
                        text="RESTORATION", 
                        font=("Glacial indifference", 15), 
                        fg="#000000", 
                        bg="#FFFFFF", 
                        justify="center")

textoImClass = tk.Label(ventana, 
                        text="CLASSIFICATION", 
                        font=("Glacial indifference", 15), 
                        fg="#000000", 
                        bg="#FFFFFF", 
                        justify="center")

canvasConfPercen = tk.Canvas(ventana, width=0.3*ancho_pantalla, height=0.15*alto_pantalla)
canvasConfPercen.configure(bg="#169D53")

# Crear una fuente personalizada
fuente_resultado = font.Font(family='Arimo', size=15, weight="bold")

# Crear un botón con un diseño personalizado
botonHomeScreen = tk.Button(ventana, 
                  text="Home Screen", 
                  font=fuente_boton, 
                  bg="#A6A6A6", 
                  fg='#FFFFFF',
                  width=int(0.01*ancho_pantalla),
                  height=int(0.0025*alto_pantalla),
                  command=volver_inicio)

s = ttk.Style()
s.theme_use('clam')
s.configure("grey.Horizontal.TProgressbar", foreground='#3B3B3B', background='#3B3B3B')
barra_progreso = ttk.Progressbar(ventana, 
                                 style="grey.Horizontal.TProgressbar", 
                                 orient="horizontal",
                                 mode="determinate")

ventana.mainloop()