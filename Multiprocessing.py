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

#Deals with an issue with matplotlib on mac
matplotlib.use("TkAgg")

#My imports
import UI_class
#import PlotInteraction as pi
import Arduino
import AcquisitionSetupWindow as acq


@dataclass
class Settings:
    stop_flag: bool = False
    n_channels: int = 1024
    arduino_port: str = "COM3"
    baud: int = 9600
    n_acquisitions: int = 1
    t_acquisition: int = 4
    dir_path: str = os.path.dirname(os.path.realpath(__file__))
    default_save_folder: str = "DataAcquisition"
    acquisition_filesave_path: str = os.path.join(dir_path, default_save_folder)
    settings_dict: dict = field(default_factory=dict)
    stop_flag
    threshold: int = 0


#create list with all parameters inside of the get_metrics function
params_list= ["Total Counts", "Start Time", "Preset Time", "ADC Channels", "Number of Acquisitions", "Save Directory","Data Collection Rate (Hz)"]


def get_metrics(data_dict, settings_dict, t_elapsed, print_flag=False):

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


def collect_data(dev, all_arr, shared_dict, settings_dict, lock, settings):
    
    n=0
    
    while n < settings.n_acquisitions:

        #reset dictionary
        #shared_dict = {key: 0 for key in shared_dict}
        #3print("Shared dict just before function: " + str(shared_dict))
        for key in range(settings.n_channels):
            shared_dict[key] = 0
        #get the current time and set the timeout
        timeout = time.time() + dev.acquisition_time #set the timeout
        sensor_data = []

        #update filename
        fileName = dt.now().strftime("%Y_%m_%d-%H_%M_%S") + "-"+ dev.filename

        #open new file with new filename for new acquisition 
        f = open(fileName, "a")
        print("Created file: " + fileName)

        while time.time() < timeout:
            with lock:
                val = dev.get_data_time_loop(sensor_data, shared_dict, all_arr)
                #shared_dict.update({int(val) : shared_dict[int(val)] + 1})
                #shared_dict.update()
                shared_dict[int(val)] += 1
                shared_dict.update()
            #print("Shared dict in function: " + str(shared_dict))
            time.sleep(0.00001)
        
        #print("sensor_data: " + str(sensor_data))
        print("Completed data collection: " + str(dev.n + 1) + " of " + str(dev.n_acquisitions))
        #write data to file
        writer = csv.writer(f)
        writer.writerow(sensor_data)

        # close file
        print("Data collection complete")
        print("\n")
        f.close()
        n=n+1
        

    settings_dict.update({"stop_flag":True})

def print_dict(shared_dict, settings_dict, lock):
    while not settings_dict["stop_flag"]:
        #print("Shared dict in print_dict process:")
        shared_dict.update()
        #print(shared_dict)
        time.sleep(0.5)

def launch_setup_window():
    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
    return setup_window.return_params()

#create new process to read data from arduino after creating a new device object 
#this is necessary because the device object is not picklable
def create_device_read_process(all_arr, 
                                shared_dict,
                                settings_dict,
                                lock, settings):

    device = Arduino.Arduino( n_acquisitions  = settings.n_acquisitions,
                                sensor_data_all = all_arr,
                                current_dict    = shared_dict,
                                n_channels=settings.n_channels,
                                acquisition_time=settings.t_acquisition)  

    collect_data(device, 
                    all_arr,
                    shared_dict, 
                    settings_dict, 
                    lock,
                    settings) 


x_val1 = 0
y_val1 = 0

def onclick(event : matplotlib.backend_bases.MouseEvent):
    global x_val1, y_val1

    if event.inaxes:
        fig = plt.gcf()
        if hasattr(fig, 'line'):
            fig.line.remove()
        fig.line = plt.axvline(event.xdata, color='r')
        x_val1 = event.xdata
        y_val1 = event.ydata
        fig.canvas.draw()
    return x_val1

def UI_run(settings : Settings, shared_dict : dict):

    #first we create the figure to pass to the UI class
    x=np.linspace(0, settings.n_channels, settings.n_channels)
    y=np.linspace(0, settings.n_channels, settings.n_channels)
    fig, ax1  = plt.subplots()
    ax1.set_ylim(0, 100)
    ax1.set_xlim(0, settings.n_channels)
    ax1.set_title("Data Acquisition")
    ax1.set_xlabel("Channel")
    ax1.set_ylabel("Counts")

    #draw a tentative plot 
    line1, = ax1.plot(x, y, 'r-')

    #create the UI object
    root= tk.Tk()
    UI_obj= UI_class.UI_Window(root, title = "Data Acquisition", geometry = "1000x700", matplot_fig = fig)

    t_start = time.time()
    now=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
    cid = None
    xvalue= None
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
        line1.set_ydata(y_temp)
        ax1.set_ylim(0, 1.1*max(shared_dict.values())+ 5)
        #ax1.fill_between(x, y_temp, color='red', alpha=0.5)
        if settings.threshold != 0: 
            ax1.axvline(x=settings.threshold, color='blue', linestyle='--', linewidth=0.5)
        if cid is not None:
            fig.canvas.mpl_disconnect(cid)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        fig.canvas.draw()
        fig.canvas.flush_events()
    
        #print("x: " + str(x_val1))
        #print("y: " + str(y_val1))
        interactive_metrics = [settings.threshold, x_val1, y_val1]

        time.sleep(0.00001)
        new_threshold= UI_obj.run_real_time(data= shared_dict, metrics = metrics, interactive_metrics = interactive_metrics)
        settings.threshold = new_threshold


if __name__ == "__main__":

    #start with default settings for arduino and acquisition
    settings= Settings(n_channels=1024)

    print("Settings: " + str(settings))

    #setup directory for file storage
    dir_path = os.path.dirname(os.path.realpath(__file__))

    #change directory to the new folder to save data
    #if directory not found, create it
    directory_save_folder = os.path.join((dir_path),"DataAcquisition")

    if not os.path.exists(directory_save_folder):
        os.makedirs(directory_save_folder)
        print("Created savefile directory at " + directory_save_folder)
        #change directory to the new folder
        os.chdir(directory_save_folder)
    else:
        #change directory to the new folder
        os.chdir(directory_save_folder)


    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")

    #n_acquisitions , t_acquisition = setup_window.return_params()
    settings.n_acquisitions, settings.t_acquisition = setup_window.return_params()

    print("Number of acquisitions:", str(int(settings.n_acquisitions)))
    print("Acquisition time:", str(settings.t_acquisition), " seconds")

    print(".....................Starting data acquisition.....................")
    print("Number of acquisitions:", str(int(settings.n_acquisitions)))
    print("Acquisition time:", str(settings.t_acquisition), " seconds")

    #manager for shared memory dictionary
    manager = multiprocessing.Manager()
    lock= multiprocessing.Lock()

    current_acquisition_dict = manager.dict()
    #set entire dictionary to 0
    #current_acquisition_dict = {i:0 for i in range(n_channels)}
    for key in range(settings.n_channels):
        current_acquisition_dict[key] = 0

       

    #dictionary with all settings for the current acquisition 
    settings_dict = manager.dict()
    settings_dict["n_channels"] = 1024
    settings_dict["arduino_port"] = "COM3"
    settings_dict["baud"] = 9600
    settings_dict["n_acquisitions"] = settings.n_acquisitions
    settings_dict["t_acquisition"] = settings.t_acquisition
    settings_dict["dir_path"] = dir_path
    settings_dict["acquisition_filesave"] = directory_save_folder
    settings_dict["stop_flag"] = 0

   

    all_arr= []

    #create new process to read data from arduino 
    read_data = multiprocessing.Process(target=create_device_read_process, args=(all_arr, current_acquisition_dict, settings_dict,lock, settings))

    #process to print the shared dictionary
    print_dict_proc = multiprocessing.Process(target=print_dict, args=(current_acquisition_dict, settings_dict, lock))

    #create UI process
    ui_process = multiprocessing.Process(target=UI_run, args=(settings,current_acquisition_dict))



    #starting all processes
    read_data.start()
    print_dict_proc.start()
    ui_process.start()
    

    #wait for all processes to finish
    read_data.join()
    print_dict_proc.join()
    ui_process.join()
    

