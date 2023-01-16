import asyncio
import serial
import numpy as np
import time
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt


#create serial object - Arduino
class Arduino:
    def __init__(self, port, baud, n_acquisitions=1, acquisition_time=5, filename="analog-data.csv", sensor_data_all=[], n_channels=10, current_dict={}):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(self.port, self.baud)
        print("Connected to Arduino port: " + self.port + " at " + str(self.baud) + " baud.")
        self.data = []  # store data
        self.n = 0
        #default time and number of acquisitions
        self.n_acquisitions = n_acquisitions
        self.acquisition_time = acquisition_time
        self.filename = filename
        self.sensor_data_all = sensor_data_all
        self.channels=n_channels
        self.current_dict=current_dict
        self.stop_flag = False


    def return_data(array,instance):
        array.append(instance)
        return instance


    def collect_data_with_plot(self, data_arr):

        x=np.linspace(0, 10, self.channels)
        y=np.linspace(0, 10, self.channels)
        plt.ion() #

        #create plot window to update in real time
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        #set axis limits
        ax1.set_ylim(0, 100)
        ax1.set_xlim(0, self.channels)

        line1, = ax1.plot(x, y, 'r-')

        #create array to store all sensor data for each acquisition
        sensor_data_all = []  # store data

        while self.n < self.n_acquisitions:
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

            #create a dictionay to store the data with n_bins keys
            data_dict = {i:0 for i in range(self.channels)}
    
            while time.time() < timeout:
                # read data from serial port
                var = float(self.ser.readline().decode("utf-8").strip())
                # print(self.data)
                # write data to file
                sensor_data.append(var)
                self.sensor_data_all.append(var)
                data_arr.append(var)

                print(var)

                data_dict.update({int(var) : data_dict[int(var)] + 1})

                #update plot 
                line1.set_ydata(list(data_dict.values()))
                fig.canvas.draw()
                fig.canvas.flush_events()


            #print("sensor_data: " + str(sensor_data))
            print("Completed data collection: " + str(self.n) + " of " + str(self.n_acquisitions))
            #write data to file
            writer = csv.writer(f)
            writer.writerow(sensor_data)


            # close file
            print("Data collection complete")
            print("\n")
            f.close()


    def open_connection(self):
        self.ser = serial.Serial(self.port, self.baud)
        print("Connected to Arduino port: " + self.port + "at " + str(self.baud) + " baud.")

    def close_connection(self):
        self.ser.close()
        print("Closed connection to Arduino port: " + self.port + "at " + str(self.baud) + " baud.")    

    def read_serial(self):
        return float(self.ser.readline().decode("utf-8").strip())

    def get_data_time_loop(self,sensor_data, current_dict, all_data):
        var = self.read_serial()
        sensor_data.append(var)

        #update dictionary with new data for the respective channel
        #current_dict.update({int(var) : current_dict[int(var)] + 1})
        all_data.append(var)

        print("var: " + str(var))
        #print dictionary
        #print("current_dict: " + str(current_dict))
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
  





