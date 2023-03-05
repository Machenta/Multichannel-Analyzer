
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from datetime import datetime as dt
import time
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
            self.plot_min : int = 1
            self.plot_max : int = 1024
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
      
            y = [0.01 for i in range(self.n_channels)]
            x = [i for i in range(self.n_channels)]
            
            #defines the color and width of the line to be plotted
            pen = pg.mkPen(color=(118,181,197))
            pen.setWidth(3)

            #we create the plot
            self.plot = pg.PlotItem()
            self.plot.setMouseEnabled(x=False, y=False)
            # set properies
            self.y_label= self.plot.setLabel('left', 'Counts', color='b', **{'font-size':'12pt', 'font-weight':'bold'})
            #self.y_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            self.x_label=self.plot.setLabel('bottom', 'Channel', color='b', **{'font-size':'12pt', 'font-weight':'bold'})
            #self.x_label.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            self.plot.setXRange(1,self.n_channels)
            self.plot.setYRange(0.1,10)
            

            # plot
            self.c1= pg.PlotDataItem(x, y, name='Spectrum',setFillLevel=1)
            self.c1.setPen(pen)
            self.plot.addItem(self.c1)
            self.plot.setLogMode(x=False, y=True)
            #set customizations
            self.plot.showGrid(x=True,y=True)

            # Add the plot to a layout
            layout = QVBoxLayout()
            self.plotWidget = pg.PlotWidget()
            self.plotWidget.setCentralItem(self.plot)
            self.plotWidget.setBackground('w')
            layout.addWidget(self.plotWidget)
            self.setLayout(layout)
            


      def update_y_data(self, acquisition_parameters : AcquisitionParameters):
            #first we have to take into account if the user requested a clear plot
            #while at the same time we have to take into account if the user input a threshold
            threshold = acquisition_parameters.get_threshold()
            if acquisition_parameters.get_clear_plot() == True:
                  for key in range(self.n_channels):
                        acquisition_parameters.set_current_acq_channel(key, 0.01)
                  self.y_temp = [acquisition_parameters.get_current_acq_channel(i)+0.01 if i >= threshold else 0.01 for i in range(1, acquisition_parameters.get_n_channels())]
                  #since we have cleared the plot, we have to set the clear plot flag to false
                  acquisition_parameters.set_clear_plot(False)
            else:
                  self.y_temp = [acquisition_parameters.get_current_acq_channel(i)+0.01 if i >= threshold else 0.01 for i in range(1, acquisition_parameters.get_n_channels())]


            #print("y_temp: " + str(self.y_temp))

      def redraw_plot(self, acquisition_parameters : AcquisitionParameters, user_entries : UserEntries):
            #now we take the y_temp that we have updated and we plot it
            #along with all other elements such as threshold line and cursor line
            #time the update of the plot
            #start_time = time.time()


            self.update_y_data(acquisition_parameters)
            #now we update the plot with the new data
            self.c1.setData(y= self.y_temp)
            
            #self.plot.getAxis("left").setLimits(min=0.01, max=1.1*max(self.y_temp)+10)
            #print data to console
            #print("y_temp: " + str(self.y_temp))
            
            if acquisition_parameters.get_plot_scale() == "log":
                self.plot.setLogMode(x=False, y=True)
                self.plot.setYRange(np.log10(1),np.log10(2*max(self.y_temp)+10))
                #self.plot.getAxis('left').logFilter = 0.1
            else:
                self.plot.setLogMode(x=False, y=False)
                self.plot.setYRange(0.0001,1.1*max(self.y_temp)+10)

            #self.plot.getAxis("left").setScale(scale="log")
            #adjust the range of the plot based on the user input
            #if either of the entries result in ValueError, we set the range to the default
            try:
      
                  #if the entries are the same we set the range to the default
                  if user_entries.plot_min == user_entries.plot_max:
                        self.plot.setXRange(1, self.n_channels)
                        #update the user entries with the new range
                        user_entries.plot_min = 1
                        user_entries.plot_max = self.n_channels
                  else:
                        self.plot.setXRange(user_entries.plot_min, user_entries.plot_max)
            except ValueError:
                  self.plot.setXRange(1, 1024)
            

            if not hasattr(self, 'cursor_line'):
                  self.cursor_line = pg.InfiniteLine(angle=90, pen='blue', movable=True, name='Cursor', label='Cursor', labelOpts={'position':0.95, 'color':(255,255,255,200), 'fill':(0,0,255,100)})
                  self.plot.addItem(self.cursor_line)
                  #account for the fact that the cursor line is movable and set the channel accordingly
                  self.cursor_line.sigPositionChangeFinished.connect(lambda: self.cursor_line_moved(user_entries))

                  #update the acquisition parameters with the current channel
                  acquisition_parameters.set_selected_channel(user_entries.channel_select)
                  #update the channel counts
                  acquisition_parameters.set_selected_channel_counts(self.y_temp[user_entries.channel_select])

            self.cursor_line.setPos(user_entries.channel_select)
            #account for the fact that the cursor line is movable and set the channel accordingly
            self.cursor_line.sigPositionChangeFinished.connect(lambda: self.cursor_line_moved(user_entries))

            #update the acquisition parameters with the current channel
            acquisition_parameters.set_selected_channel(user_entries.channel_select)
            #update the channel counts
            acquisition_parameters.set_selected_channel_counts(self.y_temp[user_entries.channel_select])

            if not hasattr(self, 'threshold_line'):
                  self.threshold_line = pg.InfiniteLine(angle=90, pen='red', movable=True, name='Threshold', label='Threshold', labelOpts={'position':0.9, 'color':(255,255,255,200), 'fill':(255,0,0,100)})
                  self.plot.addItem(self.threshold_line)
                  #account for the fact that the threshold line is movable and set the threshold value accordingly
                  self.threshold_line.sigPositionChangeFinished.connect(lambda: self.threshold_line_moved(user_entries))
                  #update the acquisition parameters with the current threshold
                  acquisition_parameters.set_threshold(user_entries.threshold)

            #update the acquisition parameters with the current threshold
            acquisition_parameters.set_threshold(user_entries.threshold)

            self.threshold_line.setPos(user_entries.threshold)
            #account for the fact that the threshold line is movable and set the threshold value accordingly
            self.threshold_line.sigPositionChangeFinished.connect(lambda: self.threshold_line_moved(user_entries))

            #create a linear region item to highlight the peak
            if not hasattr(self, 'peak_region1'):
                  self.peak_region1 = pg.LinearRegionItem([user_entries.lower_peak1, user_entries.upper_peak1], pen=(247, 213, 149, 1), brush=(247, 213, 149, 100), movable=True, )
                  self.plot.addItem(self.peak_region1)
                  #label the region
                  #self.peak_region_label = pg.TextItem(text='Peak 1', color="black", anchor=(0.5,0.5))
                  #self.peak_region_label.setPos(user_entries.lower_peak1, 1.1*max(self.y_temp)+6)
                  #self.plot.addItem(self.peak_region_label)
                  #account for the fact that the region is movable and set the peak accordingly
            else:
                  self.peak_region1.setRegion([user_entries.lower_peak1, user_entries.upper_peak1])
                  #self.peak_region_label.setPos((user_entries.lower_peak1+user_entries.upper_peak1)/2, 1.1*max(self.y_temp)+6)

            #create a linear region item to highlight the peak
            if not hasattr(self, 'peak_region2'):
                  self.peak_region2 = pg.LinearRegionItem([user_entries.lower_peak2, user_entries.upper_peak2], pen=(171,219,227,100), brush=(171,219,227,100), movable=True)
                  self.plot.addItem(self.peak_region2)
                  #label the region
                  #self.peak_region_label2 = pg.TextItem(text='Peak 2', color="black", anchor=(0.5,0.5))
                  #self.peak_region_label2.setPos(user_entries.lower_peak2, 1.1*max(self.y_temp)+6)
                  #self.plot.addItem(self.peak_region_label2)
                  #account for the fact that the region is movable and set the peak accordingly
            else:
                  self.peak_region2.setRegion([user_entries.lower_peak2, user_entries.upper_peak2])
                  #self.peak_region_label2.setPos((user_entries.lower_peak2+user_entries.upper_peak2)/2, 1.1*max(self.y_temp)+6)


            #sync the threshold with the main acquisition parameters object
            acquisition_parameters.set_threshold(user_entries.threshold)
            #t_end = time.time()
            #print(f"Time to update plot: {t_end-start_time}")

      def get_point(self):
            return self.cursor_line.getPos()


      def cursor_line_moved(self, user_entries : UserEntries):
            user_entries.channel_select = int(self.cursor_line.getPos()[0])

      def threshold_line_moved(self, user_entries : UserEntries):
            user_entries.threshold = int(self.threshold_line.getPos()[0])

