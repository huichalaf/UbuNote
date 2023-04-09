import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import json

def get_json_data():
    with open("config.json", "r") as f:
        data = json.load(f)
    return data

def modify_json_data(data):
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

#a class that contains a menu with diferent options and buttons that will help us to make changes in the configuration of the editor
class Settings(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Settings")
        self.geometry("400x400")
        self.config(bg="white")
        self.crucial_data = get_json_data()
        #now we add 4 diferent buttons, change pencil color, change width of the pencil, change width of the rubber and change the color of the background
        self.button1 = tk.Button(self, text="Change pencil color", command=self.change_color)
        self.button1.pack()
        self.button2 = tk.Button(self, text="Change width of the pencil", command=self.change_width_pencil)
        self.button2.pack()
        self.button3 = tk.Button(self, text="Change width of the rubber", command=self.change_width_rubber)
        self.button3.pack()
        self.button4 = tk.Button(self, text="Change background color", command=self.change_background_color)
        self.button4.pack()
        self.mainloop()

    def change_color(self):
        self.pencil_color = simpledialog.askstring("Change color", "Introduce the color of the pencil")
        if self.pencil_color is None:
            self.pencil_color = 'red'
        else:
            try:
                self.pencil_color = self.pencil_color
            except:
                self.pencil_color = 'red'
        self.crucial_data["pencil_color"] = self.pencil_color
        modify_json_data(self.crucial_data)
    
    def change_width_rubber(self):
        self.width_pencil = simpledialog.askinteger("Change width", "Introduce the width of the rubber")
        if self.width_pencil is None:
            self.width_rubber = 10
        else:
            self.width_rubber = self.width_rubber
        self.crucial_data["width_rubber"] = self.width_rubber
        modify_json_data(self.crucial_data)
    
    def change_width_pencil(self):
        self.width_pencil = simpledialog.askinteger("Change width", "Introduce the width of the pencil")
        if self.width_pencil is None:
            self.width_pencil = 2
        else:
            self.width_pencil = self.width_pencil
        self.crucial_data["width_pencil"] = self.width_pencil
        modify_json_data(self.crucial_data)

    def change_background_color(self):
        self.background_color = simpledialog.askstring("Change color", "Introduce the color of the background")
        if self.background_color is None:
            self.background_color = 'white'
        else:
            try:
                self.background_color = self.background_color
            except:
                self.background_color = 'white'
        self.crucial_data["background_color"] = self.background_color
        modify_json_data(self.crucial_data)

if __name__ == "__main__":
    print("This is a module, not a program")