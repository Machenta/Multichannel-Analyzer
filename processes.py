import multiprocessing
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib
from dataclasses import dataclass, field
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#my imports 
from AcquisitionParams import * 
import ArduinoV2 as device
from DataRetriever import *
from MainWindow import *

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


def run(lock: multiprocessing.Lock, acquisition_parameters):

      dev = device.Arduino()

      #create the data retriever
      data_retriever = DataRetriever(dev, acquisition_parameters)

      data_retriever.get_multiple_acquisitions(lock, acquisition_parameters)

def run_main_window(lock: multiprocessing.Lock, acquisition_parameters):
      app = QtWidgets.QApplication(sys.argv)
      MainWindow = QtWidgets.QMainWindow()
      ui = Ui_MainWindow()
      ui.setupUi(MainWindow, acquisition_parameters)
      MainWindow.show()
      sys.exit(app.exec_()) 

def metrics_backend(lock: multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):
      #create the metrics backend to pass to the main window 
      # this will be used to update the metrics in the main window

      #we create the Plotter object to be passed to the main window
      #this contains a gif and axes object to be updated
      plotter = Plotter(acquisition_parameters)
      print("here###############################################")
      #we update the plot with the data that is already in the acquisition parameters
      while acquisition_parameters.get_acquisition_running():
            with lock:
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