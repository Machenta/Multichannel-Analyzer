import os 
import datetime as dt
from dataclasses import field
import csv

class AcquisitionParameters:
      def __init__(self, n_acquisitions : int = 1, t_acquisition : float = 5):
            self.acquisition_running : bool = False
            self.n_channels : int = 512
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
            self.clear_plot : bool = False
            self.restart : bool = False
            self.total_counts : int = 0
            self.window_is_open : bool = False
            self.selected_channel : int = 0
            self.selected_channel_counts : int = 0


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

      def set_n_channels(self, value : int):
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

      def get_current_acq_channel(self, channel : int ):
            return int(self.current_acq[channel])

      def set_current_acq_channel(self, channel : int , value):
            self.current_acq[int(channel)] = value

      def update_current_acq_channel(self, channel : int):
            self.current_acq[int(channel)] +=1   


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

      def get_clear_plot(self):
            return self.clear_plot

      def set_clear_plot(self, value : bool):
            self.clear_plot = value

      def get_restart(self):
            return self.restart

      def set_restart(self, value : bool):
            self.restart = value

      def get_total_counts(self):
            return self.total_counts

      def set_total_counts(self, value : int):
            self.total_counts = value

      def update_total_counts(self):
            self.total_counts +=1

      def get_window_is_open(self):
            return self.window_is_open
      
      def set_window_is_open(self, value : bool):
            self.window_is_open = value

      def get_selected_channel(self):
            return self.selected_channel

      def set_selected_channel(self, value : int):
            self.selected_channel = value

      def get_selected_channel_counts(self):
            return self.selected_channel_counts
      
      def set_selected_channel_counts(self, value : int):
            self.selected_channel_counts = value

      def create_header(self):
            h = ["ADC Channels: " +  str(self.n_channels),
                  "Number of Acquisitions: " + str(self.n_acquisitions),
                  "Preset Time: " + str(self.t_acquisition),
                  "Save Directory: " + str(self.acquisition_filesave_directory),
                  "Threshold: " + str(self.threshold),
                  "Live Time: " + str(self.live_time),
                  "Date: " + str(dt.datetime.now())
                  ]
            return h

      def print_settings(self):
            print("ADC Channels: " +  str(self.n_channels))
            print("Number of Acquisitions: " + str(self.n_acquisitions))
            print("Preset Time: " + str(self.t_acquisition))
            print("Save Directory: " + str(self.acquisition_filesave_directory))
            print("Threshold: " + str(self.threshold))
            print("Live Time: " + str(self.live_time))
            print("Date: " + str(dt.datetime.now()))

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