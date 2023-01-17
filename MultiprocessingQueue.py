import time
import multiprocessing
import serial
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import Arduino
import tkinter as tk
import AcquisitionSetupWindow as acq


stop_flag = False
#create new process to read data from arduino
#read_data = multiprocessing.Process(target=device.full_collection, args=(all_arr))


def collect_data(dev, all_arr, shared_dict, settings_dict, lock):
    
    n=0
    n_iter= [i for i in range(int(dev.n_acquisitions))]
    for n in n_iter:

        #reset dictionary
        shared_dict = {key: 0 for key in shared_dict}
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
            
            
        print("Shared dict just outside of function: " + str(shared_dict))
        

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
        print("dict at the end: " + str(shared_dict))
        

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
                                lock):

    device = Arduino.Arduino(arduino_port, 
                                baud, 
                                n_acquisitions  = settings_dict["n_acquisitions"],
                                sensor_data_all = all_arr,
                                current_dict    = shared_dict)  

    collect_data(device, 
                    all_arr,
                    shared_dict, 
                    settings_dict, 
                    lock) 
    
    print("Shared dict in create_device_read_process outside all funcs: " + str(shared_dict))
    return stop_flag

        

if __name__ == "__main__":


    #basic setup 
    arduino_port = "COM3" #serial port of Arduino
    #arduino_port = "/dev/cu.usbmodem11101" #serial port of Arduino
    baud = 9600 #arduino uno runs at 9600 baud
    n_channels = 10 #number of channels on the arduino



    #setup directory for file storage
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path+"/DataAcquisition")
    print("Changed directory to " + dir_path)

    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")

    n_acquisitions , t_acquisition = setup_window.return_params()
    print(".....................Starting data acquisition.....................")
    print("Number of acquisitions:", str(int(n_acquisitions)))
    print("Acquisition time:", str(t_acquisition), " seconds")

    #manager for shared memory dictionary
    manager = multiprocessing.Manager()
    lock= multiprocessing.Lock()
    current_acquisition_dict = manager.dict()
    #set entire dictionary to 0
    current_acquisition_dict = {i:0 for i in range(n_channels)}
    #dictionary with all settings for the current acquisition 
    settings_dict = manager.dict()
    settings_dict["n_channels"] = n_channels
    settings_dict["arduino_port"] = arduino_port
    settings_dict["baud"] = baud
    settings_dict["n_acquisitions"] = n_acquisitions
    settings_dict["t_acquisition"] = t_acquisition
    settings_dict["dir_path"] = dir_path
    settings_dict["acquisition_filesave"] = os.chdir(dir_path+"/DataAcquisition")
    settings_dict["stop_flag"] = 0


    all_arr= []

    #create new process to read data from arduino 
    read_data = multiprocessing.Process(target=create_device_read_process, args=(all_arr,arduino_port, baud, current_acquisition_dict, settings_dict,lock))

    #process to print the shared dictionary
    print_dict_proc = multiprocessing.Process(target=print_dict, args=(current_acquisition_dict, settings_dict, lock))

    #process to sync the shared dictionary
    sync_dict_proc = multiprocessing.Process(target=sync_dict, args=(current_acquisition_dict, lock, settings_dict))

    #process for UI, data analysis and plotting
    #UI_process = multiprocessing.Process(target=launch_setup_window, args=(all_arr, current_acquisition_dict, settings_dict))

    #sync_dict_proc.start()
    #sync_dict_proc.join()

    read_data.start()
    print_dict_proc.start()
    
    read_data.join()
    print_dict_proc.join()
    
    print("Shared dict just outside of main: " + str(current_acquisition_dict))
