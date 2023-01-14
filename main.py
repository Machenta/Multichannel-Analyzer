import asyncio
import serial
import numpy as np
import time
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import Arduino
import threading


#basic setup 
arduino_port = "COM3" #serial port of Arduino
#arduino_port = "/dev/cu.usbmodem11101" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud

#setup directory for file storage
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path+"/DataAcquisition")
print("Changed directory to " + dir_path)

all_arr= []
device = Arduino.Arduino(arduino_port, baud)


#start new thread for data collection
thread = threading.Thread(target=device.full_collection(all_arr), args=(all_arr))

#function to plot all_arr
def plot_data(all_arr):
    plt.plot(all_arr)
    plt.show()

#new thread to plot data
thread2 = threading.Thread(target=plot_data(all_arr), args=(all_arr))
