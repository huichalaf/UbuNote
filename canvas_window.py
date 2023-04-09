import tkinter as tk
import keyboard
from tkinter import filedialog
from PIL import Image, ImageTk
import io
from functions import get_json_data, modify_json_data

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
        self.crucial_data = get_json_data()
        self.pencil_color_original = self.crucial_data["pencil_color"]
        self.rubber_color = self.crucial_data["rubber_color"]
        self.background_color = self.crucial_data["background_color"]
        self.width_pencil = self.crucial_data["width_pencil"]
        self.width_rubber = self.crucial_data["width_rubber"]
        self.color = 'red'
        self.width = 2
        self.bind("<Motion>", self.tell_me_where_you_are)
        self.bind("<Button-1>", self.start_drawing)
        self.bind("<B1-Motion>", self.draw_line)
        self.bind("<ButtonRelease-1>", self.stop_drawing)
        keyboard.add_hotkey('ctrl+shift+c', self.clear_canvas)
        keyboard.add_hotkey('ctrl+s', self.guardar_archivo)
        keyboard.add_hotkey('ctrl+o', self.abrir_archivo)
        self.bind("<Control-Key>", self.toggle_color)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def tell_me_where_you_are(self, event):
        self.x, self.y = event.x, event.y

    def draw_line(self, event):
        if keyboard.is_pressed('ctrl'):
            self.pencil_color = self.rubber_color
            self.width = self.width_rubber
        else:
            self.pencil_color = self.pencil_color_original
            self.width = self.width_pencil
        self.create_line(self.x, self.y, event.x, event.y, width=self.width, fill=self.pencil_color)
        self.x, self.y = event.x, event.y

    def toggle_color(self, event):
        if self.pencil_color == self.pencil_color_original:
            self.pencil_color = self.rubber_color
        else:
            self.pencil_color = self.pencil_color_original
    
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
            imagen = imagen.resize((self.screen_width, self.screen_height))
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