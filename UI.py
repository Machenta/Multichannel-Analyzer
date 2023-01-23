import time
import multiprocessing
import serial
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import Arduino
import tkinter as tk
import AcquisitionSetupWindow as acq
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataclasses import dataclass, field

import AcquisitionSetupWindowv2 as acq
import AnalysisWindow as ana

class UI_Window(tk.Frame):
    def __init__(self, master=None, title="UI", geometry="900x900", matplot_fig=None):
        super().__init__(master)
        self.root= master
        self.root.title(title)
        self.root.geometry(geometry)
        self.matplot_fig = matplot_fig
        self.label_width = 20
        self.label_height = 3
        self.standard_font = ("Helvetica", 12)
        self.standard_button_size = (5,5)
        self.standard_button_font = ("Helvetica", 12)
        self.standard_label_size = (15,2)
        self.standard_label_font = ("Helvetica", 11,"bold")
        self.standard_entry_size = (10,30)
        self.standard_entry_font = ("Helvetica", 12)

        #Acquisition Settings object to store all the acquisition settings in a single object
        self.acquisition_settings = acq.AcquisitionSettings()
        

        #adding a menu bar
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.acquisition_setup_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.analysis_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Setup", menu=self.acquisition_setup_menu)
        self.menu_bar.add_cascade(label="Analysis", menu=self.analysis_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.file_menu.add_command(label="Open", command = lambda: print("Open"))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command = self.change_win_status)
        self.acquisition_setup_menu.add_command(label="Acquisition Setup", command= self.launch_setup_window)
        self.analysis_menu.add_command(label="Analysis", command = self.launch_analysis_window)


        #create default figure for the multichannel plot
        if matplot_fig is None:
            self.matplot_fig = plt.figure(figsize=(7,7), dpi=100)
            self.matplot_fig.suptitle("You did not pass a figure and axis", fontsize=16)
            y = [i**2 for i in range(101)]

            self.plot1 = self.matplot_fig.add_subplot(111)
            self.plot1.plot(y)

        #create frame for the multichannel plot
        self.frame_multichannel = tk.Frame(self.root, relief = 'raised', bg='#ba994a')
        self.frame_multichannel.grid(sticky="nsew")
        self.frame_multichannel.grid_columnconfigure(0, weight=1)
        self.frame_multichannel.grid_rowconfigure(1, weight=1)

        #create canvas for the actual plot
        self.canvas_fig = FigureCanvasTkAgg(self.matplot_fig, master=self.frame_multichannel,)
        self.canvas_fig_widget = self.canvas_fig.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        #create frame for the metrics
        self.frame_metrics = tk.Frame(self.root, width=700, height=400, relief = 'raised', bg='white', bd=1)
        self.frame_metrics.grid(sticky="nsew",column=1,row=0)

        #adding labels to the metrics frame 
        
        self.label_names= ["Total Counts", "Start Time" , "Preset Time", "ADC Channels", "Number of Acquisitions", "Current Acquisition", "Time Elapsed" , "Count Rate (Hz)"]
        self.name_table = [0 for label in self.label_names]

        for i in range(len(self.label_names)):
            self.name_table[i] = tk.Label(self.frame_metrics, 
                                            text=self.label_names[i], 
                                            font=self.standard_label_font,
                                            anchor="center", 
                                            width=self.label_width, 
                                            height=self.label_height).grid(row=i, column=0, sticky="nsew")

        self.value_table = [0 for label in self.label_names]
        for i in range(len(self.label_names)):
            self.value_table[i] = tk.Label(self.frame_metrics, 
                                            text=str(0), 
                                            font = self.standard_label_font,
                                            anchor="center", 
                                            width=self.standard_label_size[0]+2, 
                                            height=self.standard_label_size[1])  
            self.value_table[i].grid(row=i, column=1, sticky="nsew")  



        #create frame for the table with interactive metrics
        #self.frame_interactive_metrics = tk.Frame(self.root, width=200, height=700, relief = 'raised', bg='#4ababa', bd=1)
        #self.frame_interactive_metrics.grid(sticky="nsew",column=1,row=1)

        #adding labels to the interactive metrics frame
        self.interactive_metrics = ["Threshold Value", "Channel", "Selected Channel Count"] 
        self.interactive_metrics_table = [0 for label in self.interactive_metrics]

        for i in range(len(self.interactive_metrics)):
            self.interactive_metrics_table[i] = tk.Label(self.frame_metrics, 
                                                            text = self.interactive_metrics[i], 
                                                            font = self.standard_label_font,
                                                            anchor ="center", 
                                                            width = self.label_width, 
                                                            height = self.label_height).grid(row=i+8, column=0, sticky="nsew"
                                                            )

        #attribute values for the interactive metrics
        self.interactive_metrics_values = [0 for label in self.interactive_metrics]
        for i in range(len(self.interactive_metrics)):
            self.interactive_metrics_values[i] = tk.Label(self.frame_metrics, 
                                                            text=str(0), 
                                                            font = self.standard_label_font,
                                                            anchor="center", 
                                                            width=self.standard_label_size[0], 
                                                            height=self.standard_label_size[1])  
            self.interactive_metrics_values[i].grid(row=i+8, column=1, sticky="nsew")      



        #create frame for the buttons 
        self.config_frame = tk.Frame(self.root, width=200, height=50, relief = 'raised', bg = '#5abf4b')
        self.config_frame.grid(sticky="nsw",column=0,row=1,columnspan=2)

        #create entry box for the threshold value and add it to the config frame 
        self.threshold_value= tk.StringVar()
        self.threshold_label = tk.Label(self.config_frame, text="Threshold \n Value", anchor="center", width=10, height=2)
        self.threshold_label.grid(row=0, column=0, sticky="nsew")

        self.threshold_entry = tk.Entry(self.config_frame, textvariable=self.acquisition_settings.threshold)
        self.threshold_entry.config(width=self.standard_entry_size[0], font=self.standard_entry_font)
        self.threshold_entry.grid(row=0, column=1, sticky="nsew")
        self.threshold_entry.bind("<Return>", self.get_threshold_bind)
    
        #create button to submit the threshold value and add it to the config frame
        self.threshold_button = tk.Button(self.config_frame, text="OK", command=self.get_threshold, width=self.standard_button_size[0], height=2)
        self.threshold_button.grid(row=0, column=2, sticky="nsew")

        #create a button to start the acquisition and add it to the config frame
        self.stop_button = tk.Button(self.config_frame, text="Start", command=self.run_acquisition, width=self.standard_button_size[0], height=2)
        self.stop_button.grid(row=0, column=3, sticky="nsew")

        #create a button to stop the acquisition and add it to the config frame
        self.stop_button = tk.Button(self.config_frame, text="Stop", command=self.stop_acquisition, width=self.standard_button_size[0], height=2)
        self.stop_button.grid(row=0, column=4, sticky="nsew")

        #create a button to clear the acquisition and add it to the config frame
        self.clear_button = tk.Button(self.config_frame, text="Clear", command=self.clear_acquisition, width=self.standard_button_size[0], height=2)
        self.clear_button.grid(row=0, column=5, sticky="nsew")

        #create a button to toggle linear or log scale and add it to the config frame
        self.scale_button = tk.Button(self.config_frame, text="Log Scale", command=self.toggle_scale, width=self.standard_button_size[0]+5, height=2)
        self.scale_button.grid(row=0, column=6, sticky="nsew")



    def run(self):
        self.root.update()

    def launch_setup_window(self):
        #create the setup window 
        top_level = tk.Toplevel(self.root)
        self.setup_window = acq.AcquisitionSetupWindow(top_level, "Acquisition Setup", "450x150")
        is_open = True
        while is_open:
            #print("is_open: ", is_open) 
            self.setup_window.update()
            time.sleep(0.05)
            self.acquisition_settings = self.setup_window.return_params()
            is_open = self.acquisition_settings.is_open
            #print("self.acquisition_settings: ", self.acquisition_settings)

        #print("Parameters: ", self.acquisition_settings)

    #A figure MUST be passed to this function as well a continuously updated data stream (data)

    def launch_analysis_window(self, figure, data):
        #creates a new top level window for the analysis
        top_level = tk.Toplevel(self.root)
        self.analysis_window = ana.AnalysisWindow(top_level, "Analysis", "450x150", figure, data)
        is_open = True
        while is_open:
            self.analysis_window.update()
            time.sleep(0.05)
            is_open = self.analysis_window.is_open
    def run_real_time(self, metrics, interactive_metrics):
        #we must update the labels with the new updated metrics from the data stream
        for i in range(len(self.label_names)):
            self.value_table[i].config(text=str(metrics[i]))
            self.value_table[i].update()
            if i < len(self.interactive_metrics):
                self.interactive_metrics_values[i].config(text=str(int(interactive_metrics[i])))
                self.interactive_metrics_values[i].update()
        self.root.update()
        return self.acquisition_settings.threshold

    def get_threshold(self):
        try:
            self.acquisition_settings.threshold = float(self.threshold_entry.get())
            print("threshold:" + str(self.acquisition_settings.threshold))
            return float(self.acquisition_settings.threshold)
        except:
            print("Please enter a valid number")
            print("threshold:" + str(self.acquisition_settings.threshold))
            return float(0)

    def get_threshold_bind(self,event=None):
        try:
            self.acquisition_settings.threshold = float(self.acquisition_settings.threshold_entry.get())
        except:
            print("Please enter a valid number")  
            self.acquisition_settings.threshold = float(0)    

    def change_text_submitted(self):
        self.acquisition_settings.threshold_button(text="Threshold Submitted")

    def stop_acquisition(self):
        self.acquisition_settings.running_acquisition = False 
        print("Stopping Acquisition: " + str(self.acquisition_settings.running_acquisition))
        print("window open: " + str(self.acquisition_settings.main_program_open))

    def run_acquisition(self):
        self.acquisition_settings.running_acquisition = True
        print("Running Acquisition: " + str(self.acquisition_settings.running_acquisition))
        print("window open: " + str(self.acquisition_settings.main_program_open))

    def clear_acquisition(self):
        self.acquisition_settings.clear_flag = True
        print("Clearing Acquisition" )

    def toggle_scale(self):
        if self.acquisition_settings.plot_scale =="linear":
            self.acquisition_settings.plot_scale= "log"
            self.scale_button.config(text="Linear Scale")
        else:
            self.acquisition_settings.plot_scale = "linear"
            self.scale_button.config(text="Log Scale")
        print("Scale: " + str(self.acquisition_settings.plot_scale))


    def stop(self):
        self.root.destroy()

    def change_win_status(self):
        self.acquisition_settings.main_program_open = False

    #define a function to combine multiple functions
    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def stop(self):
        self.root.destroy()

def on_closing():
    global run_condition
    run_condition = False
    root.destroy()


if __name__ == "__main__":

    root=tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app=UI_Window(root)
    run_condition = True
    while run_condition:
        app.run()
        #print("app.acquisition_settings.n_acquisitions: " + str(app.acquisition_settings.n_acquisitions))
        #print("app.acquisition_settings.t_acquisitions: " + str(app.acquisition_settings.t_acquisition))
        #time.sleep(0.3)
        
    