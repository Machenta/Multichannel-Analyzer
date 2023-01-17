import time
import multiprocessing
import serial
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import tkinter as tk
from dataclasses import dataclass, field

#My imports
import UI_class
import PlotInteraction as pi
import Arduino
import AcquisitionSetupWindow as acq

@dataclass
class Settings:
    stop_flag: bool = False
    n_channels: int = 10
    arduino_port: str = "COM3"
    baud: int = 9600
    n_acquisitions: int = 1
    t_acquisition: int = 4
    dir_path: str = os.path.dirname(os.path.realpath(__file__))
    default_save_folder: str = "DataAcquisition"
    acquisition_filesave_path: str = os.path.join(dir_path, default_save_folder)
    settings_dict: dict = field(default_factory=dict)

   

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
        print("Shared dict just before function: " + str(shared_dict))
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
            print("Shared dict in function: " + str(shared_dict))
            time.sleep(0.001)
        
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
        print("Shared dict in print_dict process:")
        shared_dict.update()
        print(shared_dict)
        time.sleep(0.5)

def sync_dict(d, lock, settings_dict):
     while not settings_dict["stop_flag"]:
        lock.acquire()
        d.update()
        lock.release()

def launch_setup_window():
    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
    return setup_window.return_params()

#create new process to read data from arduino after creating a new device object 
#this is necessary because the device object is not picklable
def create_device_read_process(all_arr, 
                                arduino_port,
                                baud, 
                                shared_dict,
                                settings_dict,
                                lock, settings):

    device = Arduino.Arduino(arduino_port, 
                                baud, 
                                n_acquisitions  = settings.n_acquisitions,
                                sensor_data_all = all_arr,
                                current_dict    = shared_dict,)  

    collect_data(device, 
                    all_arr,
                    shared_dict, 
                    settings_dict, 
                    lock,
                    settings) 
    

def UI_run(settings, shared_dict):

    #first we create the figure to pass to the UI class
    x=np.linspace(0, 10, settings.n_channels)
    y=np.linspace(0, 10, settings.n_channels)
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
    UI_obj= UI_class.UI_Window(root, title = "Data Acquisition", geometry = "900x900", matplot_fig = fig)

    t_start = time.time()
    #main UI window loop
    while not settings.stop_flag:

        #getting metrics from the data acquisition process
        total_counts = sum(shared_dict.values())
        start_time = dt.now().strftime("%Y/%m/%d - %H:%M:%S")
        preset_time = settings.t_acquisition
        n_channels = settings.n_channels
        n_acquisitions = settings.n_acquisitions
        t_elapsed = round(time.time() - t_start,1)
        count_rate = round(float(total_counts)/(t_elapsed+0.0001),2)

        metrics= [total_counts, start_time, preset_time, n_channels, n_acquisitions, t_elapsed, count_rate]

        line1.set_ydata(list(shared_dict.values()))
        ax1.set_ylim(0, 1.1*max(shared_dict.values())+ 5)
        cid = fig.canvas.mpl_connect('button_press_event', pi.onclick)
        fig.canvas.draw()
        fig.canvas.flush_events()

        

        time.sleep(0.001)
        UI_obj.run_real_time(data= shared_dict, metrics = metrics)


if __name__ == "__main__":


    settings= Settings()

    #basic setup 
    arduino_port = "COM3" #serial port of Arduino
    #arduino_port = "/dev/cu.usbmodem11101" #serial port of Arduino
    baud = 9600 #arduino uno runs at 9600 baud
    n_channels = 10 #number of channels on the arduino



    #setup directory for file storage
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(os.path.join((dir_path),"DataAcquisition"))
    print("Changed savefile directory to " + dir_path)

    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")

    #n_acquisitions , t_acquisition = setup_window.return_params()
    settings.n_acquisitions, settings.t_acquisition = setup_window.return_params()

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
    settings_dict["n_channels"] = n_channels
    settings_dict["arduino_port"] = arduino_port
    settings_dict["baud"] = baud
    settings_dict["n_acquisitions"] = settings.n_acquisitions
    settings_dict["t_acquisition"] = settings.t_acquisition
    settings_dict["dir_path"] = dir_path
    settings_dict["acquisition_filesave"] = os.chdir(dir_path+"/DataAcquisition")
    settings_dict["stop_flag"] = 0

   

    all_arr= []

    #create new process to read data from arduino 
    read_data = multiprocessing.Process(target=create_device_read_process, args=(all_arr,arduino_port, baud, current_acquisition_dict, settings_dict,lock, settings))

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
    

