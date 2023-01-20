import asyncio
import serial
import numpy as np
import time
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import serial.tools.list_ports
import random


#create serial object - Arduino
class Arduino:
    def __init__(self, port : str = "COM3", 
                    baud : int = 9600, 
                    n_acquisitions : int = 1, 
                    acquisition_time : int =5, 
                    sensor_data_all : list = [], 
                    n_channels : int = 1024, 
                    current_dict={}):
                    
        self.port = port
        self.baud = baud
        
        self.ports = list(serial.tools.list_ports.comports())
        for port in self.ports:
            if "VID:PID" in port[2]:
                self.port = port[0]
                
                print("Detected arduino at port: " + self.port)
                break

        print("Connected to Arduino port: " + self.port + " at " + str(self.baud) + " baud.")
        self.data = []  # store data
        self.n = 0
        #default time and number of acquisitions
        self.n_acquisitions = n_acquisitions
        self.acquisition_time = acquisition_time
        self.sensor_data_all = sensor_data_all
        self.channels=n_channels
        self.current_dict=current_dict
        self.stop_flag = False
        self.ser = serial.Serial(self.port, self.baud)

    def return_data(array,instance):
        array.append(instance)
        return instance

    def open_connection(self):
        self.ser = serial.Serial(self.port, self.baud)
        print("Connected to Arduino port: " + self.port + "at " + str(self.baud) + " baud.")

    def close_connection(self):
        self.ser.close()
        print("Closed connection to Arduino port: " + self.port + "at " + str(self.baud) + " baud.")    

    def read_serial(self):
        val = float(self.ser.readline().decode("utf-8").strip())
        #get a random number according to a guassian distribution mean 5 standard deviation 1
        #val = random.randint(0, self.channels-1)
        time.sleep(0.001)
        return val

    def get_data_time_loop(self, current_dict, all_data):
        var = self.read_serial()
        return var 

    def get_data_acquisition_loop(self, all_data):
        print("Starting data collection: " + str(self.n) + " of " + str(self.n_acquisitions))
        self.n = self.n + 1
        timeout = time.time() + self.acquisition_time  # set the timeout
    
        # update filename
        tempFilename = dt.now().strftime("%Y_%m_%d-%H_%M_%S") + "-" + self.filename
    
        # open new file with new filename for new acquisition
        f = open(tempFilename, "a")
        print("Created file: " + tempFilename)
    
        # reset array
        sensor_data = []  # store data

        #reset shared_dict  
        current_dict = {i:0 for i in range(self.channels)}

        while time.time() < timeout:
            self.get_data_time_loop(sensor_data=sensor_data, dictionary=current_dict, all_data=all_data)
        

        #print("sensor_data: " + str(sensor_data))
        print("Completed data collection: " + str(self.n) + " of " + str(self.n_acquisitions))
        #write data to file
        writer = csv.writer(f)
        writer.writerow(sensor_data)

        # close file
        print("Data collection complete")
        print("\n")
        f.close()
        print("all_data: " + str(all_data))

    def full_collection(self, all_data):

        while self.n < self.n_acquisitions:
            self.get_data_acquisition_loop(all_data)
        
        print("all_data: " + str(all_data))
        self.stop_flag = True
        return self.stop_flag
  





