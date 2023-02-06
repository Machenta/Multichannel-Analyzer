
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from datetime import datetime as dt
#import matplotlib.pyplot as plt
import tkinter as tk
from dataclasses import dataclass, field
import matplotlib
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt
from time import sleep

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from AcquisitionParams import *

class UserEntries():
      def __init__(self):
            self.lower_peak1 : int = 0
            self.upper_peak1 : int = 0
            self.lower_peak2 : int = 0
            self.upper_peak2 : int = 0
            self.plot_min : int = 0
            self.plot_max : int = 512
            self.channel_select : int = 0
            self.threshold : int = 0


class Plotter(QWidget):
      def __init__(self, acquisition_parameters : AcquisitionParameters, parent=None, width=7, height=6, dpi=100):
      #creates all necessary parameters for the plot to be displayed
      #intializes an empty plot with a line y=0 for each channel
            super().__init__()
            self.n_channels = acquisition_parameters.get_n_channels()
            #print("n_channels1: " + str(self.n_channels))

            #initialize the plot
      
            y = [0 for i in range(self.n_channels)]
            x = [i for i in range(self.n_channels)]
            

            #we create the plot
            self.plot = pg.plot()
            #self.plot.addLegend()
            # set properies
            self.y_label= self.plot.setLabel('left', 'Counts', color='b', **{'font-size':'12pt', 'font-weight':'bold'})
            #self.y_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            self.x_label=self.plot.setLabel('bottom', 'Channel', color='b', **{'font-size':'12pt', 'font-weight':'bold'})
            #self.x_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            self.plot.setXRange(0,self.n_channels)
            self.plot.setYRange(0,10)

            # plot
            self.c1= pg.PlotCurveItem(x, y, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='Spectrum')
            #self.c1 = self.plot.plot(x, y, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='Spectrum')
            #c2 = self.plot.plot(x, y2, pen='r', symbol='o', symbolPen='r', symbolBrush=0.2, name='blue')
            self.plot.addItem(self.c1)
            #set customizations
            self.plot.setBackground('w')
            self.plot.showGrid(x=True,y=True)
            pen = pg.mkPen(color=(255, 0, 0))
            pen.setWidth(3)

            self.c1.setPen(pen)
            #c2.setPen(pen)

            # Add the plot to a layout
            layout = QVBoxLayout()
            layout.addWidget(self.plot)
            self.setLayout(layout)
            
            
                  


      def update_y_data(self, acquisition_parameters : AcquisitionParameters):
            #first we have to take into account if the user requested a clear plot
            #while at the same time we have to take into account if the user input a threshold
            #print("threshold: " + str(acquisition_parameters.get_threshold()))
            threshold = acquisition_parameters.get_threshold()
            if acquisition_parameters.get_clear_plot() == True:
                  for key in range(self.n_channels):
                        acquisition_parameters.set_current_acq_channel(key, 0)
                        #print(acquisition_parameters.get_current_acq_channel(key))
                  self.y_temp = [acquisition_parameters.get_current_acq_channel(i) if i >= threshold else 0 for i in range(acquisition_parameters.get_n_channels())]
                  #since we have cleared the plot, we have to set the clear plot flag to false
                  acquisition_parameters.set_clear_plot(False)
            else:
                  #print(acquisition_parameters.get_current_acq_channel(100))
                  #print(acquisition_parameters.get_current_acq())
                  self.y_temp = [acquisition_parameters.get_current_acq_channel(i) if i >= threshold else 0 for i in range(acquisition_parameters.get_n_channels())]

                  a=1

            #print("y_temp: " + str(self.y_temp))

      def redraw_plot(self, acquisition_parameters : AcquisitionParameters, user_entries : UserEntries):
            #now we take the y_temp that we have updated and we plot it
            #along with all other elements such as threshold line and cursor line

            self.update_y_data(acquisition_parameters)
            #now we update the plot with the new data
            self.c1.setData(y= self.y_temp)
            self.plot.setYRange(0,1.1*max(self.y_temp)+10)
            #adjust the range of the plot based on the user input
            self.plot.setXRange(user_entries.plot_min, user_entries.plot_max)

            #first we remove all other lines from the plot
            # Remove previous vertical lines
            lines_to_remove = []
            #now we add the threshold line
            #self.plot.infineLine(x=acquisition_parameters.get_threshold(), pen='r', name='Threshold')
            #now we add the cursor line
            #self.plot.addLine(x=user_entries.channel_select, pen='g', name='Cursor')
            if not hasattr(self, 'cursor_line'):
                  self.cursor_line = pg.InfiniteLine(angle=90, pen='blue', movable=True, name='Cursor', label='Cursor', labelOpts={'position':0.95, 'color':(255,255,255,200), 'fill':(0,0,255,100)})
                  self.plot.addItem(self.cursor_line)
            self.cursor_line.setPos(user_entries.channel_select)

            if not hasattr(self, 'threshold_line'):
                  self.threshold_line = pg.InfiniteLine(angle=90, pen='red', movable=True, name='Threshold', label='Threshold', labelOpts={'position':0.9, 'color':(255,255,255,200), 'fill':(255,0,0,100)})
                  self.plot.addItem(self.threshold_line)
            self.threshold_line.setPos(user_entries.threshold)

            #draw the lines for the peaks
            if not hasattr(self, 'peak1_line_lower'):
                  self.peak1_line_lower = pg.InfiniteLine(angle=90, pen='green', movable=False, name='Peak1_lower', label='Peak1_lower', labelOpts={'position':0.9, 'color':(255,255,255,200), 'fill':(0,255,0,100)})
                  self.plot.addItem(self.peak1_line_lower)
            self.peak1_line_lower.setPos(user_entries.lower_peak1)

            if not hasattr(self, 'peak1_line_upper'):
                  self.peak1_line_upper = pg.InfiniteLine(angle=90, pen='green', movable=False, name='Peak1_upper', label='Peak1_upper', labelOpts={'position':0.9, 'color':(255,255,255,200), 'fill':(0,255,0,100)})
                  self.plot.addItem(self.peak1_line_upper)
            self.peak1_line_upper.setPos(user_entries.upper_peak1)

            if not hasattr(self, 'peak2_line_lower'):
                  self.peak2_line_lower = pg.InfiniteLine(angle=90, pen='green', movable=False, name='Peak2_lower', label='Peak2_lower', labelOpts={'position':0.9, 'color':(255,255,255,200), 'fill':(0,255,0,100)})
                  self.plot.addItem(self.peak2_line_lower)
            self.peak2_line_lower.setPos(user_entries.lower_peak2)

            if not hasattr(self, 'peak2_line_upper'):
                  self.peak2_line_upper = pg.InfiniteLine(angle=90, pen='green', movable=False, name='Peak2_upper', label='Peak2_upper', labelOpts={'position':0.9, 'color':(255,255,255,200), 'fill':(0,255,0,100)})
                  self.plot.addItem(self.peak2_line_upper)
            self.peak2_line_upper.setPos(user_entries.upper_peak2)

            if acquisition_parameters.get_plot_scale() == "log":
                  self.plot.setLogMode(y=True)
            else:
                  self.plot.setLogMode(y=False)

            #sync the threshold with the main acquisition parameters object
            acquisition_parameters.set_threshold(user_entries.threshold)

      def set_lin_log_scale(self, acquisition_parameters : AcquisitionParameters):
            if acquisition_parameters.get_plot_scale == True:
                  self.plot.setLogMode(x= False, y=True, min=0)
            else:
                  self.plot.setLogMode(x= False, y=False, min=0)
