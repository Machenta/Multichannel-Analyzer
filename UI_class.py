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



class UI_Window(tk.Frame):
    def __init__(self, master=None, title="UI", geometry="900x900", matplot_fig=None):
        super().__init__(master)
        self.root=master
        self.root.title(title)
        self.root.geometry(geometry)
        self.matplot_fig = matplot_fig
        self.label_width = 20
        self.label_height = 5


        #create default figure for the multichannel plot
        if matplot_fig is None:
            self.matplot_fig = plt.figure(figsize=(7,7), dpi=100)
            self.matplot_fig.suptitle("You did not pass a figure and axis", fontsize=16)
            y = [i**2 for i in range(101)]

            self.plot1 = self.matplot_fig.add_subplot(111)
            self.plot1.plot(y)

        #create frame for the multichannel plot
        self.frame_multichannel = tk.Frame(self.root, width=700, height=700, relief = 'raised', bg='blue')
        self.frame_multichannel.grid(sticky="nsew")

        #create canvas for the actual plot
        self.canvas_fig = FigureCanvasTkAgg(self.matplot_fig, master=self.frame_multichannel)
        self.canvas_fig.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


        #create frame for the metrics
        self.frame_metrics = tk.Frame(self.root, width=700, height=400, relief = 'raised', bg='yellow', bd=1)
        self.frame_metrics.grid(sticky="nsew",column=1,row=0)

        #adding labels to the metrics frame 
        
        self.label_names= ["Total Counts", "Start Time" , "Preset Time","ADC Channels","Number of Samples", "Time Elapsed" , "Count Rate (Hz)"]
        self.name_table = [0 for label in self.label_names]

        for i in range(len(self.label_names)):
            self.name_table[i] = tk.Label(self.frame_metrics, text=self.label_names[i], anchor="center", width=self.label_width, height=self.label_height).grid(row=i, column=0, sticky="nsew")

        self.value_table = [0 for label in self.label_names]
        for i in range(len(self.label_names)):
            self.value_table[i] = tk.Label(self.frame_metrics, text=str(0), anchor="center", width=self.label_width, height=self.label_height)  
            self.value_table[i].grid(row=i, column=1, sticky="nsew")  



        #create frame for the table with interactive metrics
        self.frame_interactive_metrics = tk.Frame(self.root, width=200, height=700, relief = 'raised', bg='red', bd=1)
        self.frame_interactive_metrics.grid(sticky="nsew",column=0,row=1)


    def run(self):
        self.root.update()

    #A figure MUST be passed to this function as well a continuously updated data stream (data)

    def run_real_time(self, data, metrics):
        #we must update the labels with the new updated metrics from the data stream
        for i in range(len(self.label_names)):
            self.value_table[i].config(text=str(metrics[i]))
            self.value_table[i].update()


        self.root.update()

#if __name__ == "__main__":
#
#    root=tk.Tk()
#    app=UI_Window(root)
#    while True:
#        app.run()
        
    