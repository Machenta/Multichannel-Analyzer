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


#async def full_collection_async(all_data):
#    device.full_collection(all_data)
#    await asyncio.sleep(0.0001)
#
#async def print_array(all_data):
#    print(all_data)
#    await asyncio.sleep(0.0001)
#
#async def main(obj=device,data_array=all_arr):
#    tasks= [asyncio.ensure_future(device.full_collection(data_array)),
#            asyncio.ensure_future(print_array(data_array))
#            ]
#    await asyncio.gather(
#        *tasks
#    )    
#
#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())
#loop.close()

#device.full_collection(all_arr)


async def print_array(all_data):
    print(all_data)


async def main(obj=device,data_array=all_arr):
    tasks= [asyncio.ensure_future(collect_data(obj, data_array)),
            asyncio.ensure_future(print_array(data_array))
            ]
    await asyncio.gather(
        *tasks
    )     

async def collect_data(dev, all_arr):
    sensor_data_all = []
    data_dict = {i:0 for i in range(dev.channels)}
    n=0
    while n<dev.n_acquisitions:
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
            await asyncio.sleep(0.001)

        

        #print("sensor_data: " + str(sensor_data))
        print("Completed data collection: " + str(dev.n + 1) + " of " + str(dev.n_acquisitions))
        #write data to file
        writer = csv.writer(f)
        writer.writerow(sensor_data)

        # close file
        print("Data collection complete")
        print("\n")
        f.close()
        await asyncio.sleep(0.001)

    await asyncio.sleep(0.001)    


 

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()


#collect_data(device, all_arr)




print("all_arr: " + str(all_arr))
