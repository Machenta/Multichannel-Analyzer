import multiprocessing
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib
import time
from dataclasses import dataclass, field
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#my imports 
from AcquisitionParams import * 
import ArduinoV2 as device
from DataRetriever import *
from MainWindow_Simple import *




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


def run(lock: multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):

      dev = device.Arduino(channels=acquisition_parameters.get_n_channels())

      #create the data retriever
      data_retriever = DataRetriever(dev, acquisition_parameters)

      data_retriever.get_multiple_acquisitions(lock, acquisition_parameters)

def quit_application():
      # Perform any necessary cleanup tasks here

      for process in multiprocessing.active_children():
            process.terminate()
      sys.exit()

def run_main_window(lock: multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):
      app = QApplication(sys.argv)
      window = MainWindow(acquisition_parameters)
      window.show()
      def check_window_open():
            if window.isVisible():
                  #print("window open")
                  acquisition_parameters.set_window_is_open(True)
                  window.update_plot(acquisition_parameters)
                  window.populate_metrics_grid(acquisition_parameters)
                  window.update_peak_counts(acquisition_parameters)
                  #sleep(0.2)
                  QTimer.singleShot(10, check_window_open)
            else:
                  #print("window closed")
                  acquisition_parameters.set_window_is_open(False)
                  window.update_plot(acquisition_parameters)
                  window.populate_metrics_grid(acquisition_parameters)
                  window.update_peak_counts(acquisition_parameters)

      QTimer.singleShot(10, check_window_open)
      print("Window is closed")

      signal = AppSignal()
      signal.finished.connect(app.quit)
      app.aboutToQuit.connect(signal.finished.emit)
      app.aboutToQuit.connect(quit_application)
      sys.exit(app.exec()) 



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

      managed_acquisition_parameters.set_t_acquisition(5)
      managed_acquisition_parameters.set_n_acquisitions(2)
      managed_acquisition_parameters.set_n_channels(512) 
      #managed_acquisition_parameters.set_default_save_folder("test_folder")

      #create the acquisition parameters
      #managed_acquisition_parameters = AcquisitionParameters(t_acquisition=5)

             
      #create the process
      GUI_process = multiprocessing.Process(target=run_main_window, args=(lock, managed_acquisition_parameters))
      process = multiprocessing.Process(target=run, args=(lock, managed_acquisition_parameters))
      #process_main_window = multiprocessing.Process(target=run_main_window, args=(lock, managed_acquisition_parameters))
      #create another process
      #process2 = multiprocessing.Process(target=run2, args=(lock, managed_acquisition_parameters))

      

      #start the process
      GUI_process.start()
      process.start()
      


      #join the process
      
      #metrics_process.join()
      GUI_process.join()
      process.join()