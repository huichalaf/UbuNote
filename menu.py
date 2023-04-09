import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from functions import get_json_data, modify_json_data, Settings
from main import main_function

class menu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Menu")
        self.geometry("300x300")
        self.config(bg="white")
        # now we add 2 different buttons
        self.button1 = tk.Button(self, text="Settings", command=self.settings)
        self.button1.pack()
        self.button2 = tk.Button(self, text="Editor", command=self.editor)
        self.button2.pack()
        self.mainloop()
        self.crucial_data = get_json_data()
    
    def settings(self):
        self.destroy()
        Settings()

    def editor(self):
        self.destroy()
        main_function()
        
    def change_color(self):
        self.pencil_color = simpledialog.askstring("Change color", "Introduce the color of the pencil")
        if self.pencil_color is None:
            self.pencil_color = 'red'
        self.crucial_data["pencil_color"] = self.pencil_color
        modify_json_data(self.crucial_data)
        
    def change_width_rubber(self):
        self.width_pencil = simpledialog.askinteger("Change width", "Introduce the width of the rubber")
        if self.width_pencil is None:
            self.width_pencil = 10
        self.crucial_data["width_rubber"] = self.width_pencil
        modify_json_data(self.crucial_data)
    
    def change_width_pencil(self):
        self.width_pencil = simpledialog.askinteger("Change width", "Introduce the width of the pencil")
        if self.width_pencil is None:
            self.width_pencil = 2
        self.crucial_data["width_pencil"] = self.width_pencil
        modify_json_data(self.crucial_data)

if __name__ == "__main__":
    menu()
