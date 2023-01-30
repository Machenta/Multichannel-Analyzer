from dataclasses import dataclass, field
import os


@dataclass
class AcquisitionSettings:
    n_acquisitions : int = 1
    t_acquisition : float = 5
    default_filename : str = "-Analog-data.csv"
    default_folder : str = "DataAcquisition"
    savefile_directory : str = os.path.join((os.path.dirname(os.path.realpath(__file__))),default_folder)
    n_channels : int = 512
    is_open : bool = True
    infinite_acquisition : bool = False
    threshold : int = 0
    forbidden_characters : str = "[^a-zA-Z0-9_.-]"
    main_program_open = True
    running_acquisition = False
    clear_flag = False
    plot_scale= "linear"

    def print(self):
        print("Number of acquisitions:", self.n_acquisitions)
        print("Acquisition time:", self.t_acquisition)
        print("Default filename:", self.default_filename)
        print("Default folder:", self.default_folder)
        print("Savefile directory:", self.savefile_directory)