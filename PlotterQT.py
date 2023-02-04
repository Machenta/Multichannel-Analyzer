
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from datetime import datetime as dt
#import matplotlib.pyplot as plt
import tkinter as tk
from dataclasses import dataclass, field
import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from AcquisitionParams import *


class Plotter(QWidget):
      def __init__(self, acquisition_parameters : AcquisitionParameters, parent=None, width=7, height=6, dpi=100):
      #creates all necessary parameters for the plot to be displayed
      #intializes an empty plot with a line y=0 for each channel
            super().__init__()
            self.n_channels = acquisition_parameters.get_n_channels()
            print("n_channels1: " + str(self.n_channels))

            #initialize the plot
      
            y = [2,4,6,8,10,12,14,16,18,20]
            y2 = [0,1,2,4,12,14,16,17,14,22]
            x = range(0,10)

            #we create the plot
            self.plot = pg.plot()
            self.plot.showGrid(x=True,y=True)
            self.plot.addLegend()
            # set properies
            self.plot.setLabel('left', 'Value', units='V')
            self.plot.setLabel('bottom', 'Time', units='s')
            self.plot.setXRange(0,10)
            self.plot.setYRange(0,20)

            # plot
            c1 = self.plot.plot(x, y, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='red')
            c2 = self.plot.plot(x, y2, pen='r', symbol='o', symbolPen='r', symbolBrush=0.2, name='blue')

            # Add the plot to a layout
            layout = QVBoxLayout()
            layout.addWidget(self.plot)
            self.setLayout(layout)
            



      def update_y_data(self, acquisition_parameters : AcquisitionParameters):
            #first we have to take into account if the user requested a clear plot
            #while at the same time we have to take into account if the user input a threshold
            print("threshold: " + str(acquisition_parameters.get_threshold()))
            threshold = acquisition_parameters.get_threshold()
            print("got here")
            if acquisition_parameters.get_clear_plot() == True:
                  for key in range(self.n_channels):
                        acquisition_parameters.update_current_acq_channel(key, 0)
                        print(acquisition_parameters.get_current_acq_channel(key))
                  #self.y_temp = [acquisition_parameters.get_current_acq_channel(i) if i >= threshold else 0 for i in range(acquisition_parameters.get_n_channels())]
                  #since we have cleared the plot, we have to set the clear plot flag to false
                  acquisition_parameters.set_clear_plot(False)
            else:
                  #print(acquisition_parameters.get_current_acq_channel(100))
                  print(acquisition_parameters.get_current_acq())
                  self.y_temp = [acquisition_parameters.get_current_acq_channel(i) if i >= threshold else 0 for i in range(acquisition_parameters.get_n_channels())]

                  a=1

      def redraw_plot(self, acquisition_parameters : AcquisitionParameters, cid= None):
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