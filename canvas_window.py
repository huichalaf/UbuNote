import tkinter as tk
import keyboard
from tkinter import filedialog
from PIL import Image, ImageTk
import io, sys, os
from canvas_window import MyCanvas

window = tk.Tk()
# first we get the dimensions of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# then we destroy the window
window.destroy()
del window

class MyCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.color = 'red'
        self.width = 2
        self.bind("<Motion>", self.tell_me_where_you_are)
        self.bind("<Button-1>", self.start_drawing)
        self.bind("<B1-Motion>", self.draw_line)
        self.bind("<ButtonRelease-1>", self.stop_drawing)
        keyboard.add_hotkey('ctrl+shift+c', self.clear_canvas)
        self.bind("<Control-Key>", self.toggle_color)

    def tell_me_where_you_are(self, event):
        self.x, self.y = event.x, event.y

    def draw_line(self, event):
        if keyboard.is_pressed('ctrl'):
            self.color = 'white'
            self.width = 10
        else:
            self.color = 'red'
            self.width = 2
        self.create_line(self.x, self.y, event.x, event.y, width=self.width, fill=self.color)
        self.x, self.y = event.x, event.y

    def toggle_color(self, event):
        if self.color == 'red':
            self.color = 'white'
        else:
            self.color = 'red'

    def start_drawing(self, event):
        self.x, self.y = event.x, event.y
        self.bind("<B1-Motion>", self.draw_line)

    def stop_drawing(self, event):
        self.unbind("<B1-Motion>")

    def clear_canvas(self):
        self.delete("all")
    
    def abrir_archivo(self):
        archivo = filedialog.askopenfile(defaultextension=".jpg", filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        if archivo is not None:
            imagen = Image.open(archivo.name)
            imagen = imagen.resize((screen_width, screen_height))
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.delete("all")
            self.create_image(0, 0, anchor="nw", image=imagen_tk)
            self.image = imagen_tk

    def guardar_archivo(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        if archivo:
            self.update()
            ps_file = self.postscript(colormode="color")
            imagen = Image.open(io.BytesIO(ps_file.encode("utf-8")))
            imagen.save(archivo)