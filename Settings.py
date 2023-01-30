from dataclasses import dataclass, field
import AcquisitionSetupWindowv2 as acq
import os
import multiprocessing

@dataclass
class Settings:
    stop_flag : bool = False
    n_channels : int = 10
    arduino_port : str = "COM3"
    baud : multiprocessing.Value = multiprocessing.Value('i', 9600)
    n_acquisitions : int = 1
    t_acquisition : int = 4
    dir_path : str = os.path.dirname(os.path.realpath(__file__))
    default_save_folder: str = "DataAcquisition"
    acquisition_filesave_path: str = os.path.join(dir_path, default_save_folder)
    settings_dict: dict = field(default_factory=dict)
    stop_flag : bool = False
    threshold : int = 0
    default_filename : str = "AnalogData"
    current_n : int =0
    infinite_acquisition : bool = False

    def update_with_inputs (self, parms : acq.AcquisitionSettings):
        self.n_acquisitions = parms.n_acquisitions
        self.t_acquisition = parms.t_acquisition
        self.dir_path = parms.savefile_directory
        self.default_save_folder = parms.default_folder
        self.default_filename = parms.default_filename

    def create_header(self):
        h = ["ADC Channels: " +  str(self.n_channels),
        "Number of Acquisitions: " + str(self.n_acquisitions),
        "Preset Time: " + str(self.t_acquisition),
        "Save Directory: " + str(self.acquisition_filesave_path)]
        return h

    def update_baud(self,n):
        self.baud.value = n

    def get_baud(self):
        return int(self.baud)   