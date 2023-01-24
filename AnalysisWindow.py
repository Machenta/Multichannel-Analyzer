import tkinter as tk
from dataclasses import dataclass, field
import re
import os

class AnalysisWindow(tk.Frame):
    def __init__(self, 
                    root, 
                    title : str = "Analysis Window",
                    geometry : str = "800x800"):
        super().__init__(root)
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.current_dir = os.getcwd()
        self.file_name = None
        self.file_path = None

        #create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.setup_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Setup", menu=self.setup_menu)

        #creating a frame to hold the widgets
        self.plot_frame = tk.Frame(self.root)

        #creating a canvas to hold the plot
        self.canvas = tk.Canvas(self.plot_frame, width=500, height=500)
        self.canvas.config(bg="red")
        self.canvas.pack()


        #creating a frame to hold the widgets for file selection
        self.file_frame = tk.Frame(self.root)

        


        
if __name__ == "__main__":
    root = tk.Tk()
    AnalysisWindow(root)
    root.mainloop()



