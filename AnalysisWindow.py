import tkinter as tk
from tkinter import ttk
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
import copy

matplotlib.use("TkAgg") #use the TkAgg backend for matplotlib

@dataclass
class PlotParams:
    peak1_lower_bound : int = 0
    peak1_upper_bound : int = 0
    peak2_lower_bound : int = 0
    peak2_upper_bound : int = 0

    peak1_counts : int = 0
    peak2_counts : int = 0

    plot_lower_bound : int = None
    plot_upper_bound : int = None

    threshold : int = None
    scale : str = "linear"
    filled : bool = False

    lines = []

    def has_changed(self, other : "PlotParams"):
        if self.peak1_lower_bound != other.peak1_lower_bound:
            return True
        if self.peak1_upper_bound != other.peak1_upper_bound:
            return True
        if self.peak2_lower_bound != other.peak2_lower_bound:
            return True
        if self.peak2_upper_bound != other.peak2_upper_bound:
            return True
        if self.plot_lower_bound != other.plot_lower_bound:
            return True
        if self.plot_upper_bound != other.plot_upper_bound:
            return True
        if self.threshold != other.threshold:
            return True
        if self.scale != other.scale:
            return True
        return False

    def print(self, n : str ):
        #print the name of the object
        print("PlotParams: " , n)
        print("peak1_lower_bound: ",self.peak1_lower_bound)
        print("peak1_upper_bound: ",self.peak1_upper_bound)
        print("peak2_lower_bound: ",self.peak2_lower_bound)
        print("peak2_upper_bound: ",self.peak2_upper_bound)
        print("plot_lower_bound: ",self.plot_lower_bound)
        print("plot_upper_bound: ",self.plot_upper_bound)
        print("threshold: ",self.threshold)
        print("scale: ",self.scale)

def onclick(event : matplotlib.backend_bases.MouseEvent):
        global x_val1, y_val1

        if event.inaxes:
            fig = plt.gcf()
            if hasattr(fig, 'line'):
                fig.line.remove()
            fig.line = plt.axvline(event.xdata, color='red')
            x_val1 = event.xdata
            y_val1 = event.ydata
            fig.canvas.draw()
        return x_val1

class AnalysisWindow(tk.Frame):
    def __init__(self, 
                    root, 
                    title : str = "Analysis Window",
                    geometry : str = "1200x900", 
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
        self.lines = []
        self.first_plot = False
        self.discaarded_files = []

        self.plot_params = PlotParams()
        self.current_plot_params = PlotParams()

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
        
        self.plot1.grid(True)


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
        self.plot_frame.grid(row=0, column=0, rowspan=3)

        #creating a canvas to hold the plot
        self.canvas = FigureCanvasTkAgg( self.matplot_fig , master = self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew" , rowspan=2)

        ###############################################################################################

        #creating a frame to hold the widgets for file selection
        self.file_frame = tk.Frame(self.root, bg="#2596be")
        self.file_frame.grid(row=0, column=1, sticky="nsew")
        self.file_frame.config(width=200, height=50)
        
        ######################################################

        #create a button to open the file selection window 
        #self.select_files_button = tk.Button(self.file_frame, text="Select Files", command=self.select_files)
        #self.select_files_button.grid(row=0, column=0, sticky="nsew")



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
        self.file_list_box.config(width=51, height=15)

        #populate the file list box
        for file in self.files.files_list:
            self.file_list_box.insert(tk.END, file)

        ######################################################


        ###############################################################################################

        #create a frame to hold the scroll bar to navigate the plots for the multiples files
        
        self.scroll_frame = tk.Frame(self.root, bg="#e3b3ab")
        self.scroll_frame.grid(row=3, column=0, sticky="nsew")
        self.scroll_frame.configure(width=200, height=100)

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
                                            command= self.update_plot_slider)
        self.current_file_slider.grid(row=0, column=1, sticky="nsew")
        
        #increase the size of the scroll bar


        ###############################################################################################

        #create a frame to hold the plot commands for peak finding
        self.command_frame = tk.Frame(self.root, bg = "#eab676")
        self.command_frame.grid(row=4, column=0,sticky="nsew")

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
        self.peak1_lower_bound = tk.Entry(self.command_frame, width=10)
        self.peak1_lower_bound.grid(row=1, column=1)
        self.peak1_lower_bound.bind("<Return>", self.get_peak1_lower_bound)

        #create a text box to display the upper bound for the peak finding for peak 1
        self.peak1_upper_bound_entry = tk.Entry(self.command_frame, width=10)
        self.peak1_upper_bound_entry.grid(row=2, column=1)
        self.peak1_upper_bound_entry.bind("<Return>", self.get_peak1_upper_bound)

        #create a text box to display the lower bound for the peak finding for peak 2
        self.peak2_lower_bound = tk.Entry(self.command_frame, width=10)
        self.peak2_lower_bound.grid(row=1, column=2)
        self.peak2_lower_bound.bind("<Return>",  self.get_peak2_lower_bound)

        #create a text box to display the upper bound for the peak finding for peak 2
        self.peak2_upper_bound = tk.Entry(self.command_frame, width=10)
        self.peak2_upper_bound.grid(row=2, column=2)
        self.peak2_upper_bound.bind("<Return>", self.get_peak2_upper_bound)

        

        ######################################################

        #create a text box to display the counts for peak 1
        self.peak_count_text1 = tk.Label(self.command_frame, height=1, width=10)
        self.peak_count_text1.grid(row=3, column=1)
        #self.peak_count_text1.config(state="disabled")

        #create a text box to display the counts for peak 2
        self.peak_count_text2 = tk.Label(self.command_frame, height=1, width=10)
        self.peak_count_text2.grid(row=3, column=2)
        #self.peak_count_text2.config(state="disabled")

        ######################################################

        #create a label for lower plot bound
        self.lower_plot_bound_label = tk.Label(self.command_frame, text="Lower Plot Bound: ")
        self.lower_plot_bound_label.grid(row=1, column=3)

        #create an entry box for lower plot bound

        self.lower_plot_bound_entry = tk.Entry(self.command_frame, width=10)
        self.lower_plot_bound_entry.grid(row=1, column=4)
        self.lower_plot_bound_entry.bind("<Return>", self.get_plot_lower_bound)

        ######################################################

        #create a label for upper plot bound
        self.upper_plot_bound_label = tk.Label(self.command_frame, text="Upper Plot Bound: ")
        self.upper_plot_bound_label.grid(row=2, column=3)


        #create an entry box for upper plot bound
        self.upper_plot_bound_entry = tk.Entry(self.command_frame, width=10)
        self.upper_plot_bound_entry.grid(row=2, column=4)
        self.upper_plot_bound_entry.bind("<Return>", self.get_plot_upper_bound)

        ######################################################
        #button to get all the parameters
        self.get_parameters_button = tk.Button(self.command_frame, 
                                                text="Get Parameters", 
                                                command= self.get_all_params)
        self.get_parameters_button.grid(row=4, column=0)
        #self.get_parameters_button.bind("<Return>", self.get_all_params)

        ######################################################
        #button to switch between linear and log scale
        self.scale_button = tk.Button(self.command_frame, 
                                        text="Log Scale", 
                                        command= self.switch_scale)
        self.scale_button.grid(row=4, column=1)

        ###############################################################################################

        #create a new frame to hold the analysis buttons and output
        self.analysis_frame = tk.Frame(self.root, bg="yellow")
        self.analysis_frame.grid(row=1, column=1, sticky="nsew", rowspan=2)

        #create a label for the analysis frame
        self.analysis_label = tk.Label(self.analysis_frame, text="Analysis", bg="yellow")
        self.analysis_label.grid(row=0, column=0, sticky="nsew")
        self.analysis_label.config(font=("Arial", 16), anchor="center")

        #create a label for the discarded files at the start of the acquisition
        self.discarded_files_label = tk.Label(self.analysis_frame, text="Discarded Files: ")
        self.discarded_files_label.grid(row=1, column=0, sticky="nsew")

        #create an entry box for the discarded files at the start of the acquisition
        self.discarded_files_entry = tk.Entry(self.analysis_frame, width=10)
        self.discarded_files_entry.grid(row=1, column=1, sticky="nsew")
        self.discarded_files_entry.bind("<Return>", self.get_discarded_files)
        



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
        self.first_plot = True

        self.generate_all_plots()

    def get_all_params(self, event):
        #get all parameters from the text boxes for the peak finding

        #plot bounds

        self.plot_params.plot_lower_bound = self.get_plot_lower_bound()
        self.plot_params.plot_upper_bound = self.get_plot_upper_bound()
        
        #peak 1 bounds
        self.plot_params.peak1_lower_bound = self.get_peak1_lower_bound()
        self.plot_params.peak1_upper_bound = self.get_peak1_upper_bound()

        #peak 2 bounds
        self.plot_params.peak2_lower_bound = self.get_peak2_lower_bound()
        self.plot_params.peak2_upper_bound = self.get_peak2_upper_bound()


        print("peak 1 lower bound: ", self.plot_params.peak1_lower_bound)
        print("peak 1 upper bound: ", self.plot_params.peak1_upper_bound)
        print("peak 2 lower bound: ", self.plot_params.peak2_lower_bound)
        print("peak 2 upper bound: ", self.plot_params.peak2_upper_bound)

        print("lower plot bound: ", self.plot_params.plot_lower_bound)
        print("upper plot bound: ", self.plot_params.plot_upper_bound)


    #def process_input(self):



    def get_peak1_lower_bound(self, event = None):
        try: 
            val= self.peak1_lower_bound.get()
        except ValueError:
            val = 0

        self.plot_params.peak1_lower_bound = float(val)
        

    def get_peak1_upper_bound(self, event = None ):
        #returns the upper bound for peak 1
        try:
            val = self.peak1_upper_bound_entry.get()
        except ValueError:
            val = 0
        self.plot_params.peak1_upper_bound = float(val)

    def get_peak2_lower_bound(self, event = None):
        #returns the lower bound for peak 2
        val = self.peak2_lower_bound.get()
        try:
            self.plot_params.peak2_lower_bound = float(val)
        except ValueError:
            self.plot_params.peak2_lower_bound = 0   

    def get_peak2_upper_bound(self, event=None):
        #returns the upper bound for peak 2
        val = self.peak2_upper_bound.get()
        try:
            self.plot_params.peak2_upper_bound = float(val)
        except ValueError:
            self.plot_params.peak2_upper_bound = 0
                
    def get_plot_lower_bound(self, event=None):
        #returns the lower bound for the plot
        val = self.lower_plot_bound_entry.get()
        try:
            self.plot_params.plot_lower_bound = float(val)
        except ValueError:
            self.plot_params.plot_lower_bound = 0

    def get_plot_upper_bound(self, event=None):
        #returns the upper bound for the plot
        val = self.upper_plot_bound_entry.get()
        try:
            self.plot_params.plot_upper_bound = float(val)
        except ValueError:
            self.plot_params.plot_upper_bound = 0      


    def plot_graph(self, index : int = 0):
        #plots the graph for the selected file
        #create the plot object
        x,y = self.get_x_y(index)
        print("x: ", x)
        print("y: ", y)

        self.plot1.clear()
        self.plot1.plot(x, y, 'b-')
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



    def update_plot_slider(self, event = None):
        #updates the plot based on the current file
        print("self.current_file_slider.get()" , self.current_file_slider.get())
        self.plot_graph(index = self.current_file_slider.get())

    

    def update_plot(self):
        #function to be executed in the loop instead of mainloop to 
        # update the plot in real time with the new parameters
        x = []
        y = []


        if self.first_plot:
            if self.plot_params.plot_lower_bound != None :
                #self.plot1.set_xlim(self.plot_params.plot_lower_bound, self.plot_params.plot_upper_bound)
                self.matplot_fig.axes[0].set_xlim(left = self.plot_params.plot_lower_bound)
            if self.plot_params.plot_upper_bound != None :
                #self.plot1.set_xlim(self.plot_params.plot_lower_bound, self.plot_params.plot_upper_bound)
                self.matplot_fig.axes[0].set_xlim(right = self.plot_params.plot_upper_bound)
            x, y = self.matplot_fig.axes[0].lines[0].get_data()
            #self.plot1.plot(x, y)

            #clear previous fillings of the plot if any
            for collection in self.plot1.collections:
                if type(collection) == matplotlib.collections.PolyCollection:
                    collection.remove()

            #set the peak bounds
            if self.plot_params.peak1_lower_bound !=0  and self.plot_params.peak1_upper_bound != 0 :
                mask = (x > self.plot_params.peak1_lower_bound) & (x < self.plot_params.peak1_upper_bound) 
                self.matplot_fig.axes[0].fill_between(x, y, where=mask, color='gray', alpha=0.5)
                self.plot_params.peak1_counts = self.get_peak_counts(x, y, self.plot_params.peak1_lower_bound, self.plot_params.peak1_upper_bound)
                self.peak_count_text1.config(text = self.plot_params.peak1_counts)

            if self.plot_params.peak2_lower_bound !=0  and self.plot_params.peak2_upper_bound != 0 :
                mask = (x > self.plot_params.peak2_lower_bound) & (x < self.plot_params.peak2_upper_bound) 
                self.matplot_fig.axes[0].fill_between(x, y, where=mask, color='yellow', alpha=0.5)
                self.plot_params.peak2_counts = self.get_peak_counts(x, y, self.plot_params.peak2_lower_bound, self.plot_params.peak2_upper_bound)
                self.peak_count_text2.config(text = self.plot_params.peak2_counts)
        #update peak counts if the peaks are set
        #if self.plot_params.peak1_lower_bound !=0  and self.plot_params.peak1_upper_bound != 0 :
        #    self.plot_params.peak1_counts, self.plot_params.peak2_counts = self.get_peak_counts(x, y)
        #    self.peak_count_text1.config(text = self.plot_params.peak1_counts)
        #    self.peak_count_text2.config(text = self.plot_params.peak2_counts)

        # Connect the pick event to a callback function
        self.matplot_fig.canvas.mpl_connect('button_press_event', onclick)
        self.matplot_fig.canvas.draw()
        self.matplot_fig.canvas.flush_events()

        self.root.update()

    def get_peak_counts(self, x, y, lower_bound, upper_bound):
        #returns the counts in the peak
        peak_counts = 0
        for i in range(len(x)):
            if x[i] > lower_bound and x[i] < upper_bound:
                peak_counts += y[i]


        
        return peak_counts

    def switch_scale(self):
        if self.plot_params.scale == "linear":
            self.plot_params.scale = "log"
            self.plot1.set_yscale("log")
        else:
            self.plot_params.scale = "linear"
            self.plot1.set_yscale("linear")

    def get_discarded_files(self):
        try: 
            discarded_files = int(self.discarded_files_entry.get())
        except ValueError:
            discarded_files = 0
        self.discaarded_files = discarded_files
        
        return discarded_files

    def calculate_all_integrated_counts(self, lower_bound, upper_bound):
        #calculates the integrated counts for all the files
        peak_counts = []
        for i in range(len(self.files.all_headless)):
            x, y = self.get_x_y(i)
            peak_counts.append(self.get_peak_counts(x, y, lower_bound , upper_bound))
        return peak_counts

if __name__ == "__main__":
    root = tk.Tk()
    test= AnalysisWindow(root)
    while True:
        test.update_plot()



