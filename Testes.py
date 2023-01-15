import time
import multiprocessing
import serial
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import Arduino
import threading



#create new process to read data from arduino
#read_data = multiprocessing.Process(target=device.full_collection, args=(all_arr))


def collect_data(dev, all_arr):
    sensor_data_all = []
    data_dict = {i:0 for i in range(dev.channels)}
    n=0
    n_iter= [i for i in range(dev.n_acquisitions)]
    for n in n_iter:
        n=n+1
        timeout = time.time() + dev.acquisition_time #set the timeout
        sensor_data = []

        #update filename
        fileName = dt.now().strftime("%Y_%m_%d-%H_%M_%S") + "-"+ dev.filename

        #open new file with new filename for new acquisition 
        f = open(fileName, "a")
        print("Created file: " + fileName)

        while time.time() < timeout:
            val= dev.get_data_time_loop(sensor_data, data_dict, all_arr)
            print("val: " + str(val))
            

        

        #print("sensor_data: " + str(sensor_data))
        print("Completed data collection: " + str(dev.n + 1) + " of " + str(dev.n_acquisitions))
        #write data to file
        writer = csv.writer(f)
        writer.writerow(sensor_data)

        # close file
        print("Data collection complete")
        print("\n")
        f.close()
        
def calc_square(numbers):
    for n in numbers:
        print('square ' + str(n*n))

def calc_cube(numbers):
    for n in numbers:
        print('cube ' + str(n*n*n))


#create new process to read data from arduino after creating a new device object 
#this is necessary because the device object is not picklable
def create_device_read_process(all_arr, arduino_port, baud):
    device = Arduino.Arduino(arduino_port, baud,n_acquisitions=2,sensor_data_all=all_arr)   
    collect_data(device, all_arr) 



if __name__ == "__main__":


    #basic setup 
    arduino_port = "COM3" #serial port of Arduino
    #arduino_port = "/dev/cu.usbmodem11101" #serial port of Arduino
    baud = 9600 #arduino uno runs at 9600 baud

    #setup directory for file storage
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path+"/DataAcquisition")
    print("Changed directory to " + dir_path)

    #manager for shared memory dictionary
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()


    all_arr= []

    #create new process to read data from arduino 
    read_data = multiprocessing.Process(target=create_device_read_process, args=(all_arr,arduino_port, baud))
    read_data.start()
    read_data.join()
