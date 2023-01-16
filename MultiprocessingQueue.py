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
    
def print_q(q, settings_dict, lock, q_val_arr):
    while not settings_dict["stop_flag"]:
        while not q.empty():
            last_element = q.get()
            q_val_arr.append(last_element)
            print("Last element: " + str(last_element))


    print("Finished printing queue")

def save_val(q_val_arr, q,settings_dict, lock):
    while not settings_dict["stop_flag"]:
        while not q.empty():
                q_val_arr.append(q.get())

    print("All values in queue: " + str(q_val_arr))


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
#this is necessary because the device object is not picklable and cannot be passed to a new process
def create_device_read_process(all_arr, 
                                arduino_port,
                                baud, 
                                q,
                                settings_dict,
                                lock):

    #create new empt dictionary to store data
    shared_dict = multiprocessing.Manager().dict()
    device = Arduino.Arduino(arduino_port, 
                                baud, 
                                n_acquisitions  = settings_dict["n_acquisitions"],
                                sensor_data_all = all_arr,
                                current_dict    = shared_dict)  

    n=0
    while n < device.n_acquisitions:

        #reset dictionary
        shared_dict = {key: 0 for key in shared_dict}
        #get the current time and set the timeout
        timeout = time.time() + device.acquisition_time #set the timeout
        sensor_data = []
        #update filename
        fileName = dt.now().strftime("%Y_%m_%d-%H_%M_%S") + "-"+ device.filename
        #open new file with new filename for new acquisition 
        f = open(fileName, "a")
        print("Created file: " + fileName)
        while time.time() < timeout:
            with lock:
                val = device.get_data_time_loop(sensor_data, shared_dict, all_arr)
                #append value to queue
                q.put(val)
            time.sleep(0.001)

        #print("sensor_data: " + str(sensor_data))
        print("Completed data collection: " + str(device.n + 1) + " of " + str(int(device.n_acquisitions)))
        #write data to file
        writer = csv.writer(f)
        writer.writerow(sensor_data)
        # close file
        print("Data collection complete")
        print("\n")
        f.close()

        n+=1
        

        settings_dict.update({"stop_flag":True})
        print("Reading process complete")
    
    
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
    manager1 = multiprocessing.Manager()
    settings_dict = manager1.dict()
    settings_dict["n_channels"] = n_channels
    settings_dict["arduino_port"] = arduino_port
    settings_dict["baud"] = baud
    settings_dict["n_acquisitions"] = n_acquisitions
    settings_dict["t_acquisition"] = t_acquisition
    settings_dict["dir_path"] = dir_path
    settings_dict["acquisition_filesave"] = os.chdir(dir_path+"/DataAcquisition")
    settings_dict["stop_flag"] = 0


    #create a queue to store data from arduino
    manager2 = multiprocessing.Manager()
    q= manager2.Queue()
    q_vals = []


    #create new process to read data from arduino 
    read_data = multiprocessing.Process(target=create_device_read_process, args=(q_vals,arduino_port, baud, q, settings_dict,lock))

    #process to print the shared dictionary
    print_dict_proc = multiprocessing.Process(target=print_q, args=(q, settings_dict, lock, q_vals))

    #create new process to save data from queue to array
    #save_data_proc = multiprocessing.Process(target=save_val, args=(q_vals, q, settings_dict, lock))

    #process to sync the shared dictionary
    sync_dict_proc = multiprocessing.Process(target=sync_dict, args=(q, lock, settings_dict))

    #process for UI, data analysis and plotting
    #UI_process = multiprocessing.Process(target=launch_setup_window, args=(all_arr, current_acquisition_dict, settings_dict))

    #sync_dict_proc.start()
    #sync_dict_proc.join()

    read_data.start()
    print_dict_proc.start()
    #save_data_proc.start()
    
    read_data.join()
    print_dict_proc.join()
    #save_data_proc.join()
    
    print("Saved values: " )
    print(q_vals)