import tkinter as tk
from dataclasses import dataclass, field
import re
import os
import AcquisitionSettings as a_sets
#def main():
#    root = tk.Tk()
#    window1= AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
#    return None
    
#def main():
#    root = tk.Tk()
#    window1= AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
#    return None


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
    main_program_open : bool  = True
    running_acquisition = False
    clear_flag = False
    plot_scale= "linear"

    def print(self):
        print("Number of acquisitions:", self.n_acquisitions)
        print("Acquisition time:", self.t_acquisition)
        print("Default filename:", self.default_filename)
        print("Default folder:", self.default_folder)
        print("Savefile directory:", self.savefile_directory)



class AcquisitionSetupWindow(tk.Frame):
    def __init__(self, root , 
                    title : str = "Acquisition Settings", 
                    geometry : str = "500x200"):
        super().__init__(root)
        self.root=root
        self.root.title(title)
        self.root.geometry(geometry)
        self.filename = "-Analog-data.csv"
        self.directory = None
        self.forbidden_characters = "[^a-zA-Z0-9_.-]"
        self.label_size = [20,1]
        self.standard_font = ("Helvetica", 12)
        self.standard_button_size = (5,5)
        self.standard_button_font = ("Helvetica", 12)
        self.standard_label_size = (15,2)
        self.standard_label_font = ("Helvetica", 12)
        self.standard_entry_size = (10,30)
        self.standard_entry_font = ("Helvetica", 12)

        self.acquisition_settings=AcquisitionSettings()

        #Aquisition Parameters Frame
        self.acquisition_params_frame = tk.Frame(self.root , width=700, height=700, relief = 'raised', bg="white")
        self.acquisition_params_frame.grid(sticky="nsew")

        #define labels for number of acquisitions and acquisition time
        self.n_acquisitions_label = tk.Label(self.acquisition_params_frame, text="Number of Acquisitions", width=self.label_size[0], height=self.label_size[1])
        self.n_acquisitions_label.grid(row=0, column=0, sticky="nsew")

        self.time_acquisition_label = tk.Label(self.acquisition_params_frame, text="Acquisition Time (s)", width=self.label_size[0], height=self.label_size[1])
        self.time_acquisition_label.grid(row=1, column=0, sticky="nsew")

        #define entry boxes for number of acquisitions and acquisition time
        self.acquisition_settings.n_acquisitions = tk.StringVar()
        self.n_acquisitions_entry = tk.Entry(self.acquisition_params_frame, textvariable=self.acquisition_settings.n_acquisitions)
        self.n_acquisitions_entry.insert(0,"1")
        self.n_acquisitions_entry.grid(row=0, column=1, sticky="nsew")

        self.acquisition_settings.t_acquisition = tk.StringVar()
        self.time_acquisition_entry = tk.Entry(self.acquisition_params_frame, textvariable=self.acquisition_settings.t_acquisition)
        self.time_acquisition_entry.insert(0,"5")
        self.time_acquisition_entry.grid(row=1, column=1, sticky="nsew")

        #define buttons for number of acquisitions and acquisition time
        self.n_acquisitions_button = tk.Button(self.acquisition_params_frame, text="OK", command=self.get_n_acquisitions)
        self.n_acquisitions_button.grid(row=0, column=2, sticky="nsew")

        self.time_acquisition_button = tk.Button(self.acquisition_params_frame, text="OK", command=self.get_t_acquisitions)
        self.time_acquisition_button.grid(row=1, column=2, sticky="nsew")


        #define a radio button to toggle infinite acquisition 
        #self.acquisition_settings.infinite_acquisition = tk.BooleanVar()
        #self.acquisition_settings.infinite_acquisition.set(False)
        #self.infinite_acquisition_button = tk.Radiobutton(self.acquisition_params_frame, text="Infinite Acquisition", variable=self.acquisition_settings.infinite_acquisition, value=1, command=self.toggle_infinite_acquisition)
        #self.infinite_acquisition_button.grid(row=2, column=0, sticky="nsew")

        #define a button to toggle infinite acquisition
        self.infinite_acquisition_button = tk.Button(self.acquisition_params_frame, text="Infinite Acquisition", command=self.toggle_infinite_acquisition)
        self.infinite_acquisition_button.grid(row=0, column=3, sticky="nsew", rowspan=3)

        #Frame for directory select, file name and savefile directory
        self.savefile_frame = tk.Frame(self.root,bg="white", width=400, height=100, bd=1, relief = 'raised')
        self.savefile_frame.grid(sticky="nsew")

        #add label for file name
        self.file_name_label = tk.Label(self.savefile_frame, text="Default File Name", width=self.label_size[0], height=self.label_size[1])
        self.file_name_label.grid(row=0, column=0, sticky="nsew") 

        #add entry box for file name
        self.acquisition_settings.default_filename = tk.StringVar()
        self.file_name_entry = tk.Entry(self.savefile_frame, textvariable=self.acquisition_settings.default_filename)
        self.file_name_entry.insert(0,"Spectrum-data")
        self.file_name_entry.config(validate="key", validatecommand=lambda: self.validate(self.file_name_entry.get()))
        self.file_name_entry.grid(row=0, column=1, sticky="nsew")

        #add button for file name
        self.file_name_button = tk.Button(self.savefile_frame, text="OK", command=self.get_filename)
        self.file_name_button.grid(row=0, column=2, sticky="nsew")

        #add label for savefile directory
        self.savefile_directory_label = tk.Label(self.savefile_frame, text="Savefile Directory")
        self.savefile_directory_label.grid(row=1, column=0, sticky="nsew")

        #create a filedialog button to select savefile directory
        self.savefile_directory_button = tk.Button(self.savefile_frame, text="Select Directory", command=self.open_file_dialog)
        self.savefile_directory_button.grid(row=1, column=1, sticky="nsew",columnspan=2)



        #frame for submit button
        self.submit_frame = tk.Frame(self.root, width=400, height=100, bd=1, relief = 'raised')
        self.submit_frame.grid(sticky="nsew")

        #button to submit acquisition parameters and close window
        self.submit_button = tk.Button(self.submit_frame, text="Submit all", command=self.get_acquisitions_params, width=41, height=2)
        self.submit_button.grid(sticky="nsew")
        self.root.bind('<Return>', lambda event: self.submit_button.invoke())



    def get_acquisitions_params(self): 
        try: 
            self.acquisition_settings.n_acquisitions = int(self.n_acquisitions_entry.get())
            print("self.acquisition_settings.n_acquisitions " + str(self.acquisition_settings.n_acquisitions))
        except ValueError:
            self.acquisition_settings.n_acquisitions = None
            tk.messagebox.showerror("Error","Please enter an integer value for the number of acquisitions")

        try:    
            self.acquisition_settings.t_acquisition = float(self.time_acquisition_entry.get())
            print("self.acquisition_settings.t_acquisition " + str(self.acquisition_settings.t_acquisition))
        except ValueError:
            self.acquisition_settings.n_acquisitions = None
            tk.messagebox.showerror("Error","Please enter an integer value for the acquisition time")

        self.acquisition_settings.default_filename = self.file_name_entry.get()
        self.acquisition_settings.is_open = False
        #self.acquisition_settings.savefile_directory = self.directory
        #self.acquisition_settings.print()
        return True

    def return_params(self):
        return self.acquisition_settings

    def run(self):
        self.root.update()

    def get_n_acquisitions(self): 
        try: 
            self.acquisition_settings.n_acquisitions = int(self.n_acquisitions_entry.get())
        except ValueError:
            self.acquisition_settings.n_acquisitions = None
            tk.messagebox.showerror("Error","Please enter an integer value for the number of acquisitions")

    def get_t_acquisitions(self): 
        try:
            self.acquisition_settings.t_acquisition = float(self.time_acquisition_entry.get())
        except ValueError:
            self.acquisition_settings.n_acquisitions = None
            tk.messagebox.showerror("Error","Please enter an integer value for the acquisition time")

    def get_filename(self): 
        self.acquisition_settings.default_filename = re.sub(self.forbidden_characters, "", self.file_name_entry.get())
        #get value from entry box and save it in n_acquisitions variable
        #print("type of n_acquisitions_entry:", type(self.n_acquisitions_entry))
        self.acquisition_settings.default_filename = self.file_name_entry.get()
        if not self.acquisition_settings.default_filename:
            self.acquisition_settings.default_filename = None
            tk.messagebox.showerror("Error","Forbidden characters found in the input, please enter a new name")
        else:
            None
    def open_file_dialog(self):
        self.acquisition_settings.savefile_directory = tk.filedialog.askdirectory()
        print(self.acquisition_settings.savefile_directory)

    def print_setup_params(self):
        if self.root.state() == 'normal':
            self.acquisition_settings.print()
            self.root.withdraw()
        else:
            return

    def print_params(self):
        self.acquisition_settings.print()


    def toggle_infinite_acquisition(self):
        if self.acquisition_settings.infinite_acquisition == False:
            self.acquisition_settings.infinite_acquisition = True
            self.n_acquisitions_entry.config(state='disabled')
            self.time_acquisition_entry.config(state='disabled')
            print("infinite acquisition is true: " + str(self.acquisition_settings.infinite_acquisition))
            self.acquisition_settings.t_acquisition = 999999999999999999999999999999
            #self.acquisition_settings.infinite_acquisition.set(True)
        else:
            self.acquisition_settings.infinite_acquisition = False
            self.n_acquisitions_entry.config(state='normal')
            self.time_acquisition_entry.config(state='normal')
            #self.acquisition_settings.infinite_acquisition.set(False)
            print("infinite acquisition is false: " + str(self.acquisition_settings.infinite_acquisition))

    def run_app(self):
        self.root.destroy()
        return self.acquisition_settings

    def get_savefile_name(self):
        return self.acquisition_settings.default_filename

    #define a function to combine multiple functions
    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def validate(self, P):
        self.forbidden_characters = "[^a-zA-Z0-9_.-]"
        if re.search(self.forbidden_characters, P):
            self.file_name_entry.bell()
            return False
        else:
            return True



if __name__ == "__main__":
    root=tk.Tk()
    temp = AcquisitionSetupWindow(root)
    