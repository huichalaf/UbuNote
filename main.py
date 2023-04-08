import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import keyboard
import io, sys, os
from canvas_window import MyCanvas

window = tk.Tk()
# first we get the dimensions of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# then we destroy the window
window.destroy()
del window

class App(tk.Tk):
    def __init__(self):
        global screen_width, screen_height
        # init the window
        tk.Tk.__init__(self)
        # set the title
        self.title("UbuntuNote")
        # set the size
        self.x = self.y = 0
        self.color = 'red'
        self.canvas = tk.Canvas(self, width=screen_width*2, height=screen_height, cursor="cross", bg="white")
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)
        self.width = 2

        archivo_menu = tk.Menu(barra_menu, tearoff=0)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.quit)
        barra_menu.add_cascade(label="Archivo", menu=archivo_menu)
        barra_menu.add_command(label="Añadir pestaña", command=self.add_tab)
        self.notebook = tk.ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Motion>", self.tell_me_where_you_are)
        self.bind("<Control-Key>", self.toggle_color)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        keyboard.add_hotkey('ctrl+shift+c', self.clear_canvas)
        keyboard.add_hotkey('ctrl+s', self.guardar_archivo)
        keyboard.add_hotkey('ctrl+o', self.abrir_archivo)
        keyboard.add_hotkey('ctrl+q', self.quit)

    def tell_me_where_you_are(self, event):
        self.x, self.y = event.x, event.y

    def draw_line(self, event):
        if keyboard.is_pressed('ctrl'):
            self.color = 'white'
            self.width = 10
        else:
            self.color = 'red'
            self.width = 2
        self.canvas.create_line(self.x, self.y, event.x, event.y, width=self.width, fill=self.color)
        self.x, self.y = event.x, event.y

    def toggle_color(self, event):
        if self.color == 'red':
            self.color = 'white'
        else:
            self.color = 'red'

    def start_drawing(self, event):
        self.x, self.y = event.x, event.y
        self.canvas.bind("<B1-Motion>", self.draw_line)

    def stop_drawing(self, event):
        self.canvas.unbind("<B1-Motion>")

    def clear_canvas(self):
        self.canvas.delete("all")
    
    def add_tab(self):
        tab = ttk.Frame(self.notebook)
        canvas = MyCanvas(tab, width=screen_width*2, height=screen_height, cursor="cross", bg="white")
        canvas.pack(side="top", fill="both", expand=True)
        self.notebook.add(tab, text="Pestaña")
        self.notebook.select(tab)


    def abrir_archivo(self):
        archivo = filedialog.askopenfile(defaultextension=".jpg", filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        if archivo is not None:
            imagen = Image.open(archivo.name)
            imagen = imagen.resize((screen_width, screen_height))
            imagen_tk = ImageTk.PhotoImage(imagen)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=imagen_tk)
            self.canvas.image = imagen_tk

    def guardar_archivo(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        if archivo:
            self.update()
            ps_file = self.canvas.postscript(colormode="color")
            imagen = Image.open(io.BytesIO(ps_file.encode("utf-8")))
            imagen.save(archivo)

    def quit(self):
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
