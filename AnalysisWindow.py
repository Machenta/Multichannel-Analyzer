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
import time
from functools import partial

matplotlib.use("TkAgg") #use the TkAgg backend for matplotlib


class AnalysisWindow(tk.Frame):
    def __init__(self, 
                    root, 
                    title : str = "Analysis Window",
                    geometry : str = "1100x900", 
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
        self.setup_window_open = False
        self.plots = None

        if default_savefile_dir == None:
            self.files.default_savefile_dir = os.path.join(os.getcwd(), self.files.default_savefile_folder_name)


        #temporary plot to display for testing
        self.matplot_fig = plt.figure(figsize=(7,7), dpi=100)
        self.matplot_fig.suptitle("Spectrum", fontsize=16)
        y = [i**2 for i in range(101)]
        self.plot1 = self.matplot_fig.add_subplot(111)
        #self.plot1.plot(y)
        self.plot1.set_xlabel("Channel")
        self.plot1.set_ylabel("Counts")


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

        ###############################################################################################

        #creating a frame to hold the widgets for file selection
        self.file_frame = tk.Frame(self.root, bg="#2596be")
        self.file_frame.grid(row=0, column=1, sticky="nsew")
        
        ######################################################

        self.savefile_directory_label = tk.Label(self.file_frame, text="Savefile Directory: ")
        self.savefile_directory_label.grid(row=0, column=0, sticky="nsew")
        self.savefile_directory_label.config(wraplength=100)


        #create a label to display the directory of the files
        self.savefile_directory = tk.Label(self.file_frame, text=self.files.default_savefile_dir)
        self.savefile_directory.grid(row=0, column=1, columnspan=2, sticky="nsew")
        self.savefile_directory.config(wraplength=200)

        ######################################################

        self.total_files_count_label = tk.Label(self.file_frame, text="Number of Files: ")
        self.total_files_count_label.grid(row=1, column=0, sticky="nsew")
        self.total_files_count_label.config(wraplength=100)

        #create a label to display the number of files in the directory
        self.total_files_count = tk.Label(self.file_frame, text=self.files.file_count)
        self.total_files_count.grid(row=1, column=1, columnspan=2, sticky="nsew")


        ######################################################

        self.common_file_name_label = tk.Label(self.file_frame, text="Common File Name: ")
        self.common_file_name_label.grid(row=2, column=0, sticky="nsew")
        self.common_file_name_label.config(wraplength=100)

        #create a label to display the common file name
        self.common_file_name = tk.Label(self.file_frame, text=self.files.regular_expression)
        self.common_file_name.grid(row=2, column=1, columnspan=2, sticky="nsew")

        ######################################################

        self.file_list_label = tk.Label(self.file_frame, text="File List: ")
        self.file_list_label.grid(row=3, column=0, sticky="nsew")
        self.file_list_label.config(wraplength=100)



        #create a label to display the file list
        self.file_list = tk.Label(self.file_frame, text=self.files.files_list)
        self.file_list.grid(row=3, column=1, columnspan=2, sticky="nsew")

        ######################################################

        #create the file list box
        self.file_list_box = tk.Listbox(self.file_frame, selectmode=tk.MULTIPLE)
        self.file_list_box.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.file_list_box.config(width=51, height=20)

        #populate the file list box
        for file in self.files.files_list:
            self.file_list_box.insert(tk.END, file)

        ######################################################


        ###############################################################################################

        #create a frame to hold the scroll bar to navigate the plots for the multiples files

        self.scroll_frame = tk.Frame(self.root, bg="#e3b3ab")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        ######################################################

        #create a label to display the current file number
        self.current_file_label = tk.Label(self.scroll_frame, text="Current File: ")
        self.current_file_label.grid(row=0, column=0, sticky="nsew")
        self.current_file_label.config(wraplength=100)

        #create the slider to navigate the plots for the multiples files
        self.current_file_slider = tk.Scale(self.scroll_frame, 
                                            from_=0, 
                                            to=6, 
                                            orient=tk.HORIZONTAL, 
                                            length=620 , 
                                            command= self.update_plot)
        self.current_file_slider.grid(row=0, column=1, sticky="nsew")
        
        #increase the size of the scroll bar


        ###############################################################################################

        #create a frame to hold the plot commands for peak finding
        self.command_frame = tk.Frame(self.root, bg = "#eab676")
        self.command_frame.grid(row=2, column=0,sticky="nsew")

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

        #create a label for lower plot bound
        self.lower_plot_bound_label = tk.Label(self.command_frame, text="Lower Plot Bound: ")
        self.lower_plot_bound_label.grid(row=1, column=3)

        #create an entry box for lower plot bound

        self.lower_plot_bound_entry = tk.Entry(self.command_frame, width=10)
        self.lower_plot_bound_entry.grid(row=1, column=4)

        ######################################################

        #create a label for upper plot bound
        self.upper_plot_bound_label = tk.Label(self.command_frame, text="Upper Plot Bound: ")
        self.upper_plot_bound_label.grid(row=2, column=3)


        #create an entry box for upper plot bound
        self.upper_plot_bound_entry = tk.Entry(self.command_frame, width=10)
        self.upper_plot_bound_entry.grid(row=2, column=4)

        ######################################################


        ###############################################################################################




    def select_files(self):
        #creates a new top level window to select files to analyze
        self.file_window = tk.Toplevel(self.root)
        self.file_window.wm_attributes("-topmost", True)
        self.file_window = FileSelectionWindow.FileSelectionWindow(self.file_window)
        self.file_window.wait_window()
        #copy for convinience
        self.files = self.file_window.files
        #print("files inside the main window: ", self.files)

        #update all parameters that depend on the files ingested
        self.update_file_dependent_parameters()

        #plot the first file in the list
        self.plot_graph(index = 0)

        self.generate_all_plots()

    


    def plot_graph(self, index : int = 0):
        #plots the graph for the selected file
        #create the plot object
        x,y = self.get_x_y(index)
        print("x: ", x)
        print("y: ", y)

        self.plot = AnalysisPlot.AnalysisPlot(x, y)

        self.plot1.clear()
        #self.plot1 = self.plot.ax
        #self.plot1.plot(x, y)
        self.plot1.set_ydata(y)
        self.plot1.set_xdata(x)
        self.plot1.set_title(self.files.files_list[index])

        #self.plot1.set_xlim(self.plot.lower_plot_bound, self.plot.upper_plot_bound)
        self.canvas.draw()
        self.canvas.flush_events()

    def generate_all_plots(self):
        #creates a list of all the plots
        self.plots = [None] * self.files.file_count

        #plots all the files in the list
        print("range(self.files.file_count)", str(range(self.files.file_count)))
        for index in range(self.files.file_count):
            print("index: ", index)
            x,y = self.get_x_y(index)
            self.plots[index] = AnalysisPlot.AnalysisPlot(x, y)   

    def update_file_dependent_parameters(self):
        self.savefile_directory.config(text= self.files.default_savefile_dir)
        self.total_files_count.config(text= self.files.file_count)
        self.common_file_name.config(text= self.files.regular_expression)
        for file in self.files.files_list:
            self.file_list_box.insert(tk.END, file)
        
        #update scale bar
        self.current_file_slider.config(from_ = 0, to = self.files.file_count - 1)

    def get_x_y(self, index : int = 0):
        #returns the x and y data for the selected file
        x= []
        y= []
        for element in self.files.all_headless[index]:
            x.append(int(element.split(",")[0]))
            y.append(int(element.split(",")[1]))
        return x,y

    def update_plot(self, event = None):
        #updates the plot based on the current file
        print("self.current_file_slider.get()" , self.current_file_slider.get())
        self.plot_graph(index = self.current_file_slider.get())



if __name__ == "__main__":
    root = tk.Tk()
    test= AnalysisWindow(root)
    test.root.mainloop()



