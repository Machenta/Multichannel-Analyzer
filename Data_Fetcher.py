import time
import multiprocessing
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import serial
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib 
import matplotlib.pyplot as plt
import tkinter as tk
from dataclasses import dataclass, field
import random
import sys
#from PyQt5 import QtCore, QtGui, QtWidgets
#Deals with an issue with matplotlib on mac
matplotlib.use("TkAgg")

#My imports
import UI_class
#import PlotInteraction as pi
import ArduinoV2 as device
import AcquisitionSetupWindowv2 as acq
#from MainWindow import Ui_MainWindow

def onclick(event : matplotlib.backend_bases.MouseEvent):
    global x_val1, y_val1

    if event.inaxes:
        fig = plt.gcf()
        if hasattr(fig, 'line'):
            fig.line.remove()
        fig.line = plt.axvline(event.xdata, color='black')
        x_val1 = event.xdata
        y_val1 = event.ydata
        fig.canvas.draw()
    return x_val1



class AcquisitionParameters:
      def __init__(self, n_acquisitions : int = 1, t_acquisition : float = 5):
            self.acquisition_running : bool = True
            self.n_channels : int = 10
            self.arduino_port : str = "COM3"
            self.baud : int = 9600
            self.n_acquisitions : int = n_acquisitions
            self.t_acquisition : int = t_acquisition
            self.current_acq_duration : float = 0
            self.current_act_start_time : float = 0
            self.dir_path : str = os.path.dirname(os.path.realpath(__file__))
            self.default_save_folder: str = "DataAcquisition"
            self.acquisition_filesave_directory: str = os.path.join(self.dir_path, self.default_save_folder)
            self.settings_dict: dict = field(default_factory=dict)
            self.threshold : int = 0
            self.default_filename : str = "AnalogData"
            self.current_filename : str = self.default_filename
            self.current_n : int =0
            self.live_time : float = 0
            self.current_acq : dict = {i: 0 for i in range(self.n_channels)}
            #self.current_acq : dict = {}
            self.start_time : float = 0
            self.savefile_format : str = ".csv"
            self.plot_scale : str = "linear"

            #self.create_dict

      def update_with_inputs (self, parms ):
          self.n_acquisitions = parms.n_acquisitions
          self.t_acquisition = parms.t_acquisition
          self.dir_path = parms.savefile_directory
          self.default_save_folder = parms.default_folder
          self.default_filename = parms.default_filename

      def create_dict(self):
            for key in range(self.n_channels):
                  self.current_acq[int(key)] = 0

      def get_acquisition_running(self):
            return self.acquisition_running
      
      def set_acquisition_running(self, value):
            self.acquisition_running = value

      def get_n_channels(self):
            return self.n_channels

      def set_n_channels(self, value):
            self.n_channels = value

      def get_arduino_port(self):
            return self.arduino_port

      def set_arduino_port(self, value):
            self.arduino_port = value

      def get_baud(self):
            return self.baud

      def set_baud(self, value):
            self.baud = value

      def get_n_acquisitions(self):
            return self.n_acquisitions

      def set_n_acquisitions(self, value):
            self.n_acquisitions = value

      def get_t_acquisition(self):
            return self.t_acquisition

      def set_t_acquisition(self, value):
            self.t_acquisition = value

      def get_current_acq_duration(self):
            return self.current_acq_duration
      
      def set_current_acq_duration(self, value):
            self.current_acq_duration = value
      
      def get_current_act_start_time(self):
            return self.current_act_start_time
      
      def set_current_act_start_time(self, value):
            self.current_act_start_time = value

      def get_dir_path(self):
            return self.dir_path
      
      def set_dir_path(self, value):
            self.dir_path = value

      def get_default_save_folder(self):
            return self.default_save_folder

      def set_default_save_folder(self, value):
            self.default_save_folder = value

      def get_acquisition_filesave_directory(self):
            return self.acquisition_filesave_directory
      
      def set_acquisition_filesave_directory(self, value):
            self.acquisition_filesave_directory = value
      
      def get_settings_dict(self):
            return self.settings_dict

      def set_settings_dict(self, value):
            self.settings_dict = value
      
      def get_threshold(self):
            return self.threshold
      
      def set_threshold(self, value):
            self.threshold = value

      def get_default_filename(self):
            return self.default_filename

      def set_default_filename(self, value):
            self.default_filename = value

      def get_current_filename(self):
            return self.current_filename

      def set_current_filename(self, value):
            self.current_filename = value

      def get_current_n(self):
            return self.current_n

      def update_current_n(self):
            self.current_n +=1

      def set_current_n(self, value):
            self.current_n = value

      def get_live_time(self):
            return self.live_time

      def set_live_time(self, value):
            self.live_time = value

      def get_current_acq(self):
            return self.current_acq

      def set_current_acq(self, value):
            self.current_acq = value

      def get_current_acq_channel(self, channel):
            return self.current_acq[channel]

      def set_current_acq_channel(self, channel, value):
            self.current_acq[channel] = value

      def update_current_acq_channel(self, channel):
            self.current_acq[channel] +=1     

      def get_start_time(self):
            return self.start_time

      def set_start_time(self, value):
            self.start_time = value

      def get_savefile_format(self):
            return self.savefile_format

      def set_savefile_format(self, value):
            self.savefile_format = value

      def get_plot_scale(self):
            return self.plot_scale

      def set_plot_scale(self, value : str):
            self.plot_scale = value


      def create_header(self):
            h = ["ADC Channels: " +  str(self.n_channels),
                  "Number of Acquisitions: " + str(self.n_acquisitions),
                  "Preset Time: " + str(self.t_acquisition),
                  "Save Directory: " + str(self.acquisition_filesave_directory),
                  "Threshold: " + str(self.threshold),
                  "Live Time: " + str(self.live_time),
                  "Date: " + str(dt.now())
                  ]
            return h

      def print_settings(self):
            print("ADC Channels: " +  str(self.n_channels))
            print("Number of Acquisitions: " + str(self.n_acquisitions))
            print("Preset Time: " + str(self.t_acquisition))
            print("Save Directory: " + str(self.acquisition_filesave_directory))
            print("Threshold: " + str(self.threshold))
            print("Live Time: " + str(self.live_time))
            print("Date: " + str(dt.now()))

      def print_data(self):
            print("Data: " + str(self.current_acq))

      def save_data(self):
            if not os.path.exists(self.acquisition_filesave_directory):
                  os.makedirs(self.acquisition_filesave_directory)
            filename = self.default_filename + "_" + str(dt.now()) + ".csv"
            filepath = os.path.join(self.acquisition_filesave_directory, filename)
            with open(filepath, "w", newline="") as f:
                  writer = csv.writer(f)
                  writer.writerow(self.create_header())
                  writer.writerow(self.current_acq)
            print("Data saved to: " + str(filepath))
            return filepath

      def clear_data_current_acq(self):
            for key in range(self.n_channels):
                  self.current_acq[key] = 0

class DataRetriever: 
      def __init__(self, 
                  device : device.Arduino, 
                  acquisition_parameters : AcquisitionParameters):


            self.device = device
            self.acquisition_parameters = acquisition_parameters 

      def update_parameters(self, acquisition_parameters : AcquisitionParameters):
            self.acquisition_parameters = acquisition_parameters

      def prepare_acquisition(self):
            self.device.prepare_acquisition()

      def get_data(self):
            return self.device.read_serial()

      def set_current_file_name (self):
            self.acquisition_parameters.set_current_filename(self.acquisition_parameters.get_default_filename() + "_" + 
                                                            str(self.acquisition_parameters.get_start_time()) + "_" + 
                                                            str(self.acquisition_parameters.get_current_n()).zfill(4) + 
                                                            self.acquisition_parameters.get_savefile_format())


      def prepare_acquisition(self, 
                              acquisition_parameters : AcquisitionParameters):
            #update the acquisition parameters 
            acquisition_parameters.update_current_n() #increment the current acquisition number
            acquisition_parameters.set_start_time( dt.now().strftime("%Y_%m_%d-%H_%M_%S")) #set the start time
            acquisition_parameters.set_current_filename(acquisition_parameters.get_default_filename() + "_" + 
                                                            str(acquisition_parameters.get_start_time()) + "_" + 
                                                            str(acquisition_parameters.get_current_n()).zfill(4) + 
                                                            acquisition_parameters.get_savefile_format()) #set the current filename
            print("Preparing acquisition: " + str(acquisition_parameters.get_current_filename()))
            #reset the current acquisition dictionary
            #acquisition_parameters.create_dict()
            acquisition_parameters.clear_data_current_acq()
            self.device.prepare_acquisition()

      def set_save_directory(self, acquisition_parameters : AcquisitionParameters):
            #if the directory does not exist, create it
            save_dir = os.path.join(self.acquisition_parameters.get_dir_path(), self.acquisition_parameters.get_default_save_folder())
            if not os.path.exists(save_dir):
                  os.makedirs(save_dir)
                  print("Directory " , save_dir ,  " Created ")

                  #change the current directory to the save directory
                  os.chdir(save_dir)
                  acquisition_parameters.set_acquisition_filesave_directory(save_dir)
            else: 
                  print("Directory " , save_dir ,  " already exists. Saving to this directory.")
                  acquisition_parameters.set_acquisition_filesave_directory(save_dir)

      def save_acquisition(self, acquisition_parameters : AcquisitionParameters):
            #Save the acquisition
            self.set_save_directory(acquisition_parameters)

            print("Saving data to: " + str(acquisition_parameters.get_acquisition_filesave_directory()))
            file = os.path.join(acquisition_parameters.get_acquisition_filesave_directory(), acquisition_parameters.get_current_filename())
            with open(file, "w", newline="") as f:
                  writer = csv.writer(f)
                  writer.writerow(acquisition_parameters.create_header())
                  for key, value in acquisition_parameters.get_current_acq().items():
                        writer.writerow([key, value])
            print("Data saved to: " + str(acquisition_parameters.get_acquisition_filesave_directory()))
            return acquisition_parameters.get_acquisition_filesave_directory()

      def get_one_full_acquisition(self, lock : multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):

            #Prepare the acquisition
            self.prepare_acquisition(acquisition_parameters)
            
            #check condictions for acquisition

            #make sure the acquisition is supposed to be running 
            while acquisition_parameters.get_acquisition_running() == True:
                  t_total_acq = 0 
                  
                   #reset the current live time on the acquisition parameters
                  acquisition_parameters.set_live_time(0) 
                  
                  #run the acquisition for the preset time
                  while (t_total_acq) < acquisition_parameters.get_t_acquisition() and acquisition_parameters.get_acquisition_running() == True:
                        
                        t_start = dt.now()
                        with lock:
                              #get the data from the arduino
                              val = self.get_data()
                              #update the current acquisition with the new data
                              #acquisition_parameters.current_acq[int(val)] = val
                              acquisition_parameters.update_current_acq_channel(int(val))
                              #save the data
                              print("Data: " + str(val))
                        t_end = dt.now()

                        #update the current acquisition duration with the time it took to get the data
                        t_total_acq += (t_end-t_start).total_seconds()
                        print("t_total_acq: " + str(t_total_acq))
                        print("t_acquisition: " + str(acquisition_parameters.get_t_acquisition()))
                  #update the current acquisition duration with the time it took to get the data
                  acquisition_parameters.set_current_acq_duration(t_total_acq)
                  #save the acquisition
                  self.save_acquisition(acquisition_parameters)         
                  #reset the running_acquisition flag
                  acquisition_parameters.set_acquisition_running(False)

      def get_multiple_acquisitions(self, lock : multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):
            #getting multiple acquisitions is just a loop of get_one_full_acquisition

            #check condictions for acquisition
            while acquisition_parameters.get_current_n() < acquisition_parameters.get_n_acquisitions():
                  # we need to reset the running_acquisition flag to true
                  print("Starting acquisition: " + str(acquisition_parameters.get_current_n()) + " of " + str(acquisition_parameters.get_n_acquisitions()))
                  acquisition_parameters.set_acquisition_running(True)
                  self.get_one_full_acquisition(lock , acquisition_parameters)

class Plotter:
      def __init__(self, acquisition_parameters : AcquisitionParameters):
      #creates all necessary parameters for the plot to be displayed
      #intializes an empty plot with a line y=0 for each channel
            #initialize the plot
            self.fig, self.ax = plt.subplots()
            #set the title
            #plt.title("Acquisition: " + str(acquisition_parameters.get_current_n()) + " of " + acquisition_parameters.get_n_acquisitions(), fontsize=16, fontweight='bold')
            #set a tentative x and y 
            self.x = np.arange(0, 100, 1)
            self.y = np.zeros(100)
            #set the x and y limits
            self.ax.set_xlim(0, max(self.x))
            self.ax.set_ylim(0, max(self.y)+5)
            #set the x and y labels
            self.ax.set_xlabel("Channel")
            self.ax.set_ylabel("Counts")
            self.line,= self.ax.plot(self.x, self.y, 'r-')
            #initialize the lines list 
            self.lines = []
            #set the grid 
            self.ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.5)
            self.y_temp = np.zeros(100)

            #assimilate some variables from the acquisition parameters to make the code more readable and easier to change
            #this should only be done with variables that are not going to change during the acquisition
            #this is because the acquisition parameters are shared between the processes
            #and if we change a variable in the acquisition parameters, it will change for all processes
            #whereas here it does not propagate to the other processes
            self.n_channels = acquisition_parameters.get_n_channels()
            


      def update_y_data(self, acquisition_parameters : AcquisitionParameters):
            #first we have to take into account if the user requested a clear plot
            #while at the same time we have to take into account if the user input a threshold
            threshold = acquisition_parameters.get_threshold()
            if acquisition_parameters.get_clear_plot() == True:
                  for key in range(self.n_channels):
                        acquisition_parameters.update_current_acq_channel(key, 0)
                  self.y_temp = [acquisition_parameters.current_acq.get(key) if i >= threshold else 0 for i in range(self.n_channels)]
                  #since we have cleared the plot, we have to set the clear plot flag to false
                  acquisition_parameters.set_clear_plot(False)
            else:
                  self.y_temp = [acquisition_parameters.current_acq.get(key) if i >= threshold else 0 for i in range(self.n_channels)]

      def redraw_plot(self, acquisition_parameters : AcquisitionParameters):
            #now we take the y_temp that we have updated and we plot it
            #along with all other elements such as threshold line and cursor line
            #first we update the y data
            self.update_y_data(self, acquisition_parameters)

            #now we update the plot 
            self.line.set_ydata(self.y_temp)
            self.ax.set_ylim(0, 1.1*max(self.y_temp)+5)
            self.ax.set_yscale(acquisition_parameters.get_plot_scale())

            #if the threshold is not 0, we plot the threshold line
            if acquisition_parameters.get_threshold() != 0:
                  line = self.ax.axvline(x=acquisition_parameters.get_threshold(), color='k', linestyle='--')
                  self.lines.append(line)

            #remove all other lines from the plot
            for line in self.lines[:-1]:
                  line.remove()
                  self.lines.remove(line)

            #now we have to draw the cursor if there is one
            if acquisition_parameters.get_cursor() != 0:
            

      def update_plot(self, acquisition_parameters : AcquisitionParameters):
            #plot the data
            #first we have to take into account if the user requested a clear plot
            #while at the same time we have to take into account if the user input a threshold
            if acquisition_parameters.get_clear_plot() == True:
                  for key in range(acquisition_parameters.get_n_channels()):
                        acquisition_parameters.update_current_acq_channel(key, 0)
                  self.y_temp = 

def run(lock: multiprocessing.Lock, acquisition_parameters):

      dev = device.Arduino()

      #create the data retriever
      data_retriever = DataRetriever(dev, acquisition_parameters)

      data_retriever.get_multiple_acquisitions(lock, acquisition_parameters)

#def run_main_window(lock: multiprocessing.Lock, acquisition_parameters):
#      app = QtWidgets.QApplication(sys.argv)
#      MainWindow = QtWidgets.QMainWindow()
#      ui = Ui_MainWindow()
#      ui.setupUi(MainWindow)
#      MainWindow.show()
#      sys.exit(app.exec_()) 

def metrics_backend(lock: multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):
      #create the metrics backend to pass to the main window 
      # this will be used to update the metrics in the main window

      #first the plot figure and axes to be updated 
      fig = plt.figure()
      ax = fig.add_subplot(111)
      ax.set_xlabel("Channel")
      ax.set_ylabel("Counts")

      #initialize the plot with zeros
      x=np.linspace(1, acquisition_parameters.get_n_channels(), acquisition_parameters.get_n_channels())
      y=np.zeros(acquisition_parameters.get_n_channels())

      #setting the limits of the plot 
      ax.set_xlim(0, acquisition_parameters.get_n_channels())
      ax.set_ylim(0, 100)
      ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.5)

      #create the plot
      line, = ax.plot(x, y, 'r-')
      plt.show()
if __name__ == "__main__":
      #create the manager
      #manager = multiprocessing.Manager()
      #manager.register('AcquisitionParameters', AcquisitionParameters)
      #create the lock
      lock = multiprocessing.Lock()

      BaseManager.register('AcquisitionParameters', AcquisitionParameters)
      manager = BaseManager()
      manager.start()
      managed_acquisition_parameters = manager.AcquisitionParameters()

      managed_acquisition_parameters.set_t_acquisition(2)
      managed_acquisition_parameters.set_n_acquisitions(2)
      managed_acquisition_parameters.set_n_channels(512) 
      #managed_acquisition_parameters.set_default_save_folder("test_folder")

      #create the acquisition parameters
      #managed_acquisition_parameters = AcquisitionParameters(t_acquisition=5)

             
      #create the process
      process = multiprocessing.Process(target=run, args=(lock, managed_acquisition_parameters))
      #process_main_window = multiprocessing.Process(target=run_main_window, args=(lock, managed_acquisition_parameters))
      #create another process
      #process2 = multiprocessing.Process(target=run2, args=(lock, managed_acquisition_parameters))
      metrics_process = multiprocessing.Process(target=metrics_backend, args=(lock, managed_acquisition_parameters))
      #start the process
      process.start()
      metrics_process.start()
      #process_main_window.start()
      #process2.start()

      #join the process
      process.join()
      metrics_process.join()
      #process_main_window.join()
      #process2.join()
