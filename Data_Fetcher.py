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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#Deals with an issue with matplotlib on mac
#matplotlib.use("TkAgg")

#My imports
import UI_class
#import PlotInteraction as pi
import ArduinoV2 as device
import AcquisitionSetupWindowv2 as acq
from MainWindow import Ui_MainWindow
from AcquisitionParams import  *

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





class Plotter(FigureCanvas):
      def __init__(self, acquisition_parameters : AcquisitionParameters, parent=None, width=5, height=4, dpi=100):
      #creates all necessary parameters for the plot to be displayed
      #intializes an empty plot with a line y=0 for each channel
            #initialize the plot
            self.fig, self.ax = plt.subplots()
            #set the title
            #plt.title("Acquisition: " + str(acquisition_parameters.get_current_n()) + " of " + acquisition_parameters.get_n_acquisitions(), fontsize=16, fontweight='bold')
            #set a tentative x and y 
            self.x = np.arange(0, 100, 1)
            self.y = np.arange(0, 100, 1)
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
            self.y_temp = np.arange(0, 100, 1)

            #assimilate some variables from the acquisition parameters to make the code more readable and easier to change
            #this should only be done with variables that are not going to change during the acquisition
            #this is because the acquisition parameters are shared between the processes
            #and if we change a variable in the acquisition parameters, it will change for all processes
            #whereas here it does not propagate to the other processes
            #self.n_channels = acquisition_parameters.get_n_channels()

            FigureCanvas.__init__(self, self.fig)
            self.setParent(parent)
            FigureCanvas.setSizePolicy(self,
                                    QSizePolicy.Expanding,
                                    QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)



      def update_y_data(self, acquisition_parameters : AcquisitionParameters):
            #first we have to take into account if the user requested a clear plot
            #while at the same time we have to take into account if the user input a threshold
            print("threshold: " + str(acquisition_parameters.get_threshold()))
            threshold = acquisition_parameters.get_threshold()
            print("got here")
            if acquisition_parameters.get_clear_plot() == True:
                  for key in range(self.n_channels):
                        acquisition_parameters.update_current_acq_channel(key, 0)
                  self.y_temp = [acquisition_parameters.get_current_acq_channel(i) if i >= threshold else 0 for i in range(self.n_channels)]
                  #since we have cleared the plot, we have to set the clear plot flag to false
                  acquisition_parameters.set_clear_plot(False)
            else:
                  self.y_temp = [acquisition_parameters.get_current_acq_channel(i) if i >= threshold else 0 for i in range(self.n_channels)]

      def redraw_plot(self, acquisition_parameters : AcquisitionParameters, cid= None):
            cid = self.fig.canvas.mpl_connect('button_press_event', onclick)
            #now we take the y_temp that we have updated and we plot it
            #along with all other elements such as threshold line and cursor line
            #first we update the y data
            self.update_y_data(acquisition_parameters)
            #now we update the plot 
            self.line.set_ydata(self.y_temp)
            self.ax.set_ylim(0, 1.1*max(self.y_temp)+5)
            self.ax.set_yscale(acquisition_parameters.get_plot_scale())
            self.ax.plot(self.x, self.y_temp, 'r-')
            #if the threshold is not 0, we plot the threshold line
            #if acquisition_parameters.get_threshold() != 0:
            #      line = self.ax.axvline(x=acquisition_parameters.get_threshold(), color='k', linestyle='--')
            #      self.lines.append(line)

            #remove all other lines from the plot
            #for line in self.lines[:-1]:
            #      line.remove()
            #      self.lines.remove(line)

            #now we have to draw the cursor if there is one
            #if cid is not None:
            #      self.fig.canvas.mpl_disconnect(cid)
            #cid = self.fig.canvas.mpl_connect('button_press_event', onclick)

            #finally we draw the plot
            #self.fig.draw()
            #self.fig.flush_events()

            self.draw()


            
            


def run(lock: multiprocessing.Lock, acquisition_parameters):

      dev = device.Arduino()

      #create the data retriever
      data_retriever = DataRetriever(dev, acquisition_parameters)

      data_retriever.get_multiple_acquisitions(lock, acquisition_parameters)

def run_main_window(lock: multiprocessing.Lock, acquisition_parameters):
      app = QtWidgets.QApplication(sys.argv)
      MainWindow = QtWidgets.QMainWindow()
      ui = Ui_MainWindow()
      ui.setupUi(MainWindow)
      MainWindow.show()
      sys.exit(app.exec_()) 

def metrics_backend(lock: multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):
      #create the metrics backend to pass to the main window 
      # this will be used to update the metrics in the main window

      #first the plot figure and axes to be updated 
      #fig = plt.figure()
      #ax = fig.add_subplot(111)
      #ax.set_xlabel("Channel")
      #ax.set_ylabel("Counts")
#
      ##initialize the plot with zeros
      #x=np.linspace(1, acquisition_parameters.get_n_channels(), acquisition_parameters.get_n_channels())
      #y=np.zeros(acquisition_parameters.get_n_channels())
#
      ##setting the limits of the plot 
      #ax.set_xlim(0, acquisition_parameters.get_n_channels())
      #ax.set_ylim(0, 100)
      #ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.5)
#
      ##create the plot
      #line, = ax.plot(x, y, 'r-')
      #plt.show()

      #we create the Plotter object to be passed to the main window
      #this contains a gif and axes object to be updated
      plotter = Plotter(acquisition_parameters)
      print("here###############################################")
      #we update the plot with the data that is already in the acquisition parameters
      plotter.redraw_plot(acquisition_parameters)

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

      managed_acquisition_parameters.set_t_acquisition(1)
      managed_acquisition_parameters.set_n_acquisitions(1)
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
      GUI_process = multiprocessing.Process(target=run_main_window, args=(lock, managed_acquisition_parameters))

      #start the process
      process.start()
      metrics_process.start()
      GUI_process.start()


      #join the process
      process.join()
      metrics_process.join()
      GUI_process.join()

