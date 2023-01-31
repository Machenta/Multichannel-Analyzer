import time
import multiprocessing
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

#Deals with an issue with matplotlib on mac
matplotlib.use("TkAgg")

#My imports
import UI_class
#import PlotInteraction as pi
import ArduinoV2 as device
import AcquisitionSetupWindowv2 as acq

@dataclass
class AcquisitionParameters:
      acquisition_running : bool = False
      n_channels : int = 10
      arduino_port : str = "COM3"
      baud : int = 9600
      n_acquisitions : int = 1
      t_acquisition : int = 4
      dir_path : str = os.path.dirname(os.path.realpath(__file__))
      default_save_folder: str = "DataAcquisition"
      acquisition_filesave_directory: str = os.path.join(dir_path, default_save_folder)
      settings_dict: dict = field(default_factory=dict)
      threshold : int = 0
      default_filename : str = "AnalogData"
      current_n : int =0
      live_time : float = 0
      current_acq : dict = field(default_factory=dict)

      #def update_with_inputs (self, parms ):
      #    self.n_acquisitions = parms.n_acquisitions
      #    self.t_acquisition = parms.t_acquisition
      #    self.dir_path = parms.savefile_directory
      #    self.default_save_folder = parms.default_folder
      #    self.default_filename = parms.default_filename

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

      def get_full_acquisition(self):
