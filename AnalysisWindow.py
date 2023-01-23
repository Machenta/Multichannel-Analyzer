import tkinter as tk
from dataclasses import dataclass, field
import re
import os

class AnalysisWindow(tk.Frame):
    def __init__(self, 
                    root, 
                    title : str = "Analysis Window",
                    geometry : str = "500x500"):
        super().__init__(root)
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)

        #creating a frame to hold the widgets
        self.frame = tk.Frame(self.root)

        


