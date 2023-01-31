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
import Arduino
import AcquisitionSetupWindowv2 as acq


@dataclass
class Settings:
    stop_flag : bool = False
    n_channels : int = 10
    arduino_port : str = "COM3"
    baud : int = 9600
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

    def update_with_inputs (self, parms ):
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



#create list with all parameters inside of the get_metrics function
params_list= ["Total Counts", "Start Time", "Preset Time", "ADC Channels", "Number of Acquisitions", "Save Directory","Data Collection Rate (Hz)"]



def get_metrics(data_dict : dict, settings_dict : dict, t_elapsed , print_flag=False):

    total_counts = sum(data_dict.values())
    start_time = dt.now().strftime("%Y/%m/%d - %H:%M:%S")
    preset_time = settings_dict["t_acquisition"]
    n_channels = settings_dict["n_channels"]
    n_acquisitions = settings_dict["n_acquisitions"]
    save_directory = settings_dict["acquisition_filesave"]
    count_rate = sum(data_dict.values())/t_elapsed


    if print_flag:
        print ("Printing metrics: ")
        print ("Total number of counts: " + str(total_counts))
        print ("Start time: " + str(start_time))
        print ("Preset time: " + str(preset_time))
        print ("Number of channels: " + str(n_channels))
        print ("Number of acquisitions: " + str(n_acquisitions))
        print ("Count rate: " + str(round(count_rate,2)))
        print ("Save directory: " + str(save_directory))

    return total_counts, start_time, preset_time, n_channels, n_acquisitions, count_rate, save_directory


def collect_data(dev : Arduino, shared_dict : dict, settings_dict : dict, lock , settings, settings_dict1):
    
    n=0
    if settings.stop_flag == False:
        while n < settings.n_acquisitions:

            #create new dictionary for timestamps 
            new_dict_timestamps = {} 
            for key in range(settings.n_channels):
                new_dict_timestamps[key] = 0
            #event counter    
            i=0
            #update settings dictionary
            settings_dict1["current_n"] = n
            settings_dict1.update()
            #reset dictionary
            for key in range(settings.n_channels):
                shared_dict[key] = 0
            #get the current time and set the timeout
            timeout = time.time() + settings.t_acquisition #set the timeout
            sensor_data = []

            #update filename
            fileName = dt.now().strftime("%Y_%m_%d-%H_%M_%S") + "-"+ settings.default_filename + "_" + str(n).zfill(4) +".csv"
            fileName_t_stamp= dt.now().strftime("%Y_%m_%d-%H_%M_%S") + "-"+ settings.default_filename + "_" + "time_stamps-" + str(n).zfill(4) +".csv" 
            #open new file with new filename for new acquisition 
            f = open(fileName, "a")
            print("Created file: " + fileName)
            writer = csv.writer(f)
            writer.writerow(settings.create_header())

            f_t = open(fileName_t_stamp, "a")
            writer_t = csv.writer(f_t)
        

            while time.time() < timeout:
                with lock:
                    val = dev.get_data_time_loop(sensor_data, shared_dict)
                    shared_dict[int(val)] += 1
                    shared_dict.update()   

            print("Completed data collection: " + str(dev.n + 1) + " of " + str(dev.n_acquisitions))
            #write data to file
            #print("Data to be written to file:" + str(shared_dict))
            for key, value in shared_dict.items():
                writer.writerow([key, value])
            #writer.writerow(sensor_data)
            print("Saved data to file: " + fileName)
            # close file
            print("Data collection complete")
            print("\n")
            f.close()
            f_t.close()
            n=n+1
        

    settings.stop_flag = True


def launch_setup_window():
    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
    return setup_window.return_params()

#create new process to read data from arduino after creating a new device object 
#this is necessary because the device object is not picklable
def create_device_read_process( shared_dict : dict,
                                settings_dict : dict,
                                lock, settings : Settings,
                                settings_dict1 ):

    device = Arduino.Arduino( n_acquisitions  = settings.n_acquisitions,
                                current_dict  = shared_dict,
                                n_channels=settings.n_channels,
                                acquisition_time=settings.t_acquisition)  

    collect_data(device, 
                    shared_dict, 
                    settings_dict, 
                    lock,
                    settings,
                    settings_dict1) 


x_val1 = 0
y_val1 = 0

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

def UI_run(settings : Settings, shared_dict : dict, settings_dict ):

    
    #first we create the figure to pass to the UI class
    x=np.linspace(1, settings.n_channels, settings.n_channels)
    #print("x: " + str(x))
    y=np.linspace(1, settings.n_channels, settings.n_channels)
    fig, ax1  = plt.subplots()
    ax1.set_ylim(0, 100)
    ax1.set_xlim(0, settings.n_channels)
    ax1.set_title("Data Acquisition")
    ax1.set_xlabel("Channel")
    ax1.set_ylabel("Counts")
    ax1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.5)
    
    #draw a tentative plot 
    
    line1, = ax1.plot(x, y, 'r-')
    line2 = ax1.scatter(x, y, c='b', marker='o', s=10, alpha=0.5)
    #create the UI object
    root= tk.Tk()
    UI_obj= UI_class.UI_Window(root, title = "Data Acquisition", geometry = "1000x700", matplot_fig = fig)

    t_start = time.time()
    now=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
    cid = None
    xvalue= None
    lines = []
    #main UI window loop
    while not settings.stop_flag:

        #getting metrics from the data acquisition process
        total_counts = sum(shared_dict.values())
        start_time = now
        preset_time = settings.t_acquisition
        n_channels = settings.n_channels
        n_acquisitions = settings.n_acquisitions
        #t_elapsed is the minimum of the elapsed time and the preset time
        t_elapsed = min(round(time.time() - t_start,1), preset_time)
        count_rate = round(float(total_counts)/(t_elapsed+0.0001),2)

        metrics= [total_counts, start_time, preset_time, n_channels, n_acquisitions, t_elapsed, count_rate]

        #update y_data taking into account the threshold and replace the erased values by zeros
        y_temp= [shared_dict[i] if i >= settings.threshold else 0 for i in range(settings.n_channels)]

        #line1.set_ydata(list(shared_dict.values()))
        #print("y_temp: " + str(y_temp))

        line1.set_ydata(y_temp)
        line1.set_xdata(x)
        line2.set_offsets(np.c_[x,y_temp])

        ax1.set_ylim(0, 1.1*max(shared_dict.values())+ 5)
        # clear the fill
        #fill.remove()
        #ax1.fill_between(x, y_temp, color='red', alpha=0.5)

        if settings.threshold != 0: 
            line = ax1.axvline(x=settings.threshold, color='blue', linestyle='--', linewidth=0.5)
            lines.append(line)
        for line in lines[:-1]:
            line.remove()
            lines.remove(line)    
        if cid is not None:
            fig.canvas.mpl_disconnect(cid)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        fig.canvas.draw()
        fig.canvas.flush_events()
    
        #print("x: " + str(x_val1))
        #print("y: " + str(y_val1))
        interactive_metrics = [settings.threshold, x_val1, y_temp[int(x_val1)]]
        #print(settings_dict["current_n"])
        new_threshold= UI_obj.run_real_time(data= shared_dict, metrics = metrics, interactive_metrics = interactive_metrics)
        settings.threshold = new_threshold
        time.sleep(0.1)
    

def print_dict(dict, lock):
        print("Shared dict: " + str(dict))

if __name__ == "__main__":

    #manager and lock for shared memory dictionary
    manager = multiprocessing.Manager()
    lock= multiprocessing.Lock()
    

    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "450x150")

    input_settings= setup_window.return_params()
    settings= Settings(n_channels=input_settings.n_channels)
    manager.register('Settings', Settings)
    print("Received parameters:")
    setup_window.print_params()


    if not os.path.exists(input_settings.savefile_directory):
        os.makedirs(input_settings.savefile_directory)
        print("Directory did not exist. Created savefile directory at " + input_settings.savefile_directory)
        #change directory to the new folder
        os.chdir(input_settings.savefile_directory)
    else:
        #change directory to the new folder
        os.chdir(input_settings.savefile_directory)
    
    print(".....................Starting data acquisition.....................")
    print("Number of acquisitions:", str(int(input_settings.n_acquisitions)))
    print("Acquisition time:", str(input_settings.t_acquisition), " seconds")



    current_acquisition_dict = manager.dict()
    #set entire dictionary to 0
    for key in range(settings.n_channels):
        current_acquisition_dict[key] = 0

    settings.update_with_inputs(input_settings)   

    #dictionary with all settings for the current acquisition 
    settings_dict = manager.dict()
    settings_dict["stop_flag"] = 0
    settings_dict["current_n"] = 0

   

    #create new process to read data from arduino 
    read_data = multiprocessing.Process(target=create_device_read_process, 
                                        args=(current_acquisition_dict, settings_dict,lock, settings, settings_dict))


    #create UI process
    ui_process = multiprocessing.Process(target=UI_run, 
                                            args=(settings,current_acquisition_dict, settings_dict))

    print_dict_proc = multiprocessing.Process(target=print_dict, args=(current_acquisition_dict,lock))

    #starting all processes
    read_data.start()
    ui_process.start()
    print_dict_proc.start()
    
    #wait for all processes to finish
    read_data.join()
    ui_process.join()
    print_dict_proc.join()
    
