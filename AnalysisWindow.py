import tkinter as tk
from dataclasses import dataclass, field
import re
import os
import numpy as np
import FileSelectionWindow 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import AnalysisPlot

matplotlib.use("TkAgg") #use the TkAgg backend for matplotlib

class AnalysisWindow(tk.Frame):
    def __init__(self, 
                    root, 
                    title : str = "Analysis Window",
                    geometry : str = "800x800", 
                    default_savefile_folder_name : str = "DataAcquisition",
                    default_savefile_dir : str = None,
                    ):
        super().__init__(root)
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.matplot_fig = None 
        self.files = FileSelectionWindow.file_data( default_savefile_dir = default_savefile_dir, 
                                                    default_savefile_folder_name = default_savefile_folder_name)

        if default_savefile_dir == None:
            self.files.default_savefile_dir = os.path.join(os.getcwd(), self.files.default_savefile_folder_name)


        #temporary plot to display for testing
        self.matplot_fig = plt.figure(figsize=(7,7), dpi=100)
        self.matplot_fig.suptitle("You did not pass a figure and axis", fontsize=16)
        y = [i**2 for i in range(101)]
        self.plot1 = self.matplot_fig.add_subplot(111)
        self.plot1.plot(y)


        #create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.setup_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Setup", menu=self.setup_menu)
        self.setup_menu.add_command(label="Select Files", command=self.select_files)

        #creating a frame to hold the widgets
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.grid(row=0, column=0)

        #creating a canvas to hold the plot
        self.canvas = FigureCanvasTkAgg( self.matplot_fig , master = self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        #creating a frame to hold the widgets for file selection
        self.file_frame = tk.Frame(self.root, bg="red")
        self.file_frame.grid(row=0, column=1, sticky="nsew")
        
        ###############################################################################################

        #create a frame to hold the plot commands for peak finding
        self.command_frame = tk.Frame(self.root, bg = "blue")
        self.command_frame.grid(row=1, column=0,sticky="nsew")

        ######################################################

        #create labels for peak 1 and 2
        self.peak1_label = tk.Label(self.command_frame, text="Peak 1")
        self.peak1_label.grid(row=0, column=1)
        ##########
        self.peak2_label = tk.Label(self.command_frame, text="Peak 2")
        self.peak2_label.grid(row=0, column=2)

        ######################################################

        #create a label to display the lower bound for the peak finding
        self.left_peak_label1 = tk.Label(self.command_frame, text="Lower bound: ")
        self.left_peak_label1.grid(row=1, column=0)

        #create a label to display the upper bound for the peak finding
        self.right_peak_label1 = tk.Label(self.command_frame, text="Upper bound: ")
        self.right_peak_label1.grid(row=2, column=0)

        #create a label to display the counts for each peak
        self.peak_count_label1 = tk.Label(self.command_frame, text="Peak Counts: ")
        self.peak_count_label1.grid(row=3, column=0)

        ######################################################

        #create a text box to display the lower bound for the peak finding for peak 1 
        self.left_peak_text1 = tk.Text(self.command_frame, height=1, width=10)
        self.left_peak_text1.grid(row=1, column=1)

        #create a text box to display the lower bound for the peak finding for peak 2
        self.right_peak_text2 = tk.Text(self.command_frame, height=1, width=10)
        self.right_peak_text2.grid(row=1, column=2)

        #create a text box to display the upper bound for the peak finding for peak 1
        self.right_peak_text1 = tk.Text(self.command_frame, height=1, width=10)
        self.right_peak_text1.grid(row=2, column=1)

        #create a text box to display the upper bound for the peak finding for peak 2
        self.right_peak_text2 = tk.Text(self.command_frame, height=1, width=10)
        self.right_peak_text2.grid(row=2, column=2)

        ######################################################

        #create a text box to display the counts for peak 1
        self.peak_count_text1 = tk.Text(self.command_frame, height=1, width=10)
        self.peak_count_text1.grid(row=3, column=1)
        self.peak_count_text1.config(state="disabled")

        #create a text box to display the counts for peak 2
        self.peak_count_text2 = tk.Text(self.command_frame, height=1, width=10)
        self.peak_count_text2.grid(row=3, column=2)
        self.peak_count_text2.config(state="disabled")

        ######################################################


    def select_files(self):
        #creates a new top level window to select files to analyze
        self.file_window = tk.Toplevel(self.root)
        self.file_window = FileSelectionWindow.FileSelectionWindow(self.file_window,
                                                                    title="File Selection", 
                                                                    geometry="800x600")
        #copy for convienence
        self.files = self.file_window.files    

    def plot_graph(self, index : int = 0):
        #plots the graph for the selected file
        #create the plot object
        x,y = self.get_x_y(index)
        self.plot = AnalysisPlot(self.files[index].x, self.files[index].y)
        self.root.mainloop()

        
        
    def get_x_y(self, index : int = 0):
        #returns the x and y data for the selected file
        x= []
        y= []
        for element in self.files.all_headless[index]:
            x.append(element.split(",")[0])
            y.append(element.split(",")[1])
        return x,y
    


if __name__ == "__main__":
    root = tk.Tk()
    test= AnalysisWindow(root)
    test.root.mainloop()



