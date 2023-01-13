import serial
import csv
import os
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
from scipy import stats
import time
from datetime import datetime as dt
from collections import Counter

#basic setup 
#arduino_port = "COM3" #serial port of Arduino
arduino_port = "/dev/cu.usbmodem11101" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud

#default time and number of acquisitions
n_acquisitions = 10
acquisition_time = 10


#get directory path
dir_path = os.path.dirname(os.path.realpath(__file__))

#change file directory to dir_path
os.chdir(dir_path+"/DataAcquisition")
print("Changed directory to " + dir_path)

#filename definition
fileName="analog-data.csv" #name of the CSV file generated
#add current time to file name
fileName = dt.now().strftime("%Y_%m_%d-%H_%M_%S") + fileName

class NewWindow(tk.Toplevel):
     
    def __init__(self, master = None):
         
        super().__init__(master = master)
        self.title("New Window")
        self.geometry("200x200")
        label = tk.Label(self, text ="This is a new Window")
        label.pack()


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


def get_acquisitions():  
    global n_acquisitions
    n_acquisitions = entry1.get()

def get_acquisition_time():  
    global acquisition_time
    acquisition_time = entry2.get()

def changeText_n_acquisitions():  
    button1['text'] = 'Submitted'
    label1 = tk.Label(window, text=n_acquisitions)
    canvas1.create_window(200, 110, window=label1)

def changeText_acquisition_time():
    button2['text'] = 'Submitted'
    label2 = tk.Label(window, text=acquisition_time)
    canvas1.create_window(400, 110, window=label2)

def Close():
    window.destroy()

def open_Window():
    newWindow = tk.Toplevel(window)
    newWindow.title("Data Acquisition Dashboard")
    newWindow.geometry("800x600")
    Label1 = tk.Label(newWindow, text="Data Acquisition Dashboard") 
    Label1.pack()   



#initialize root window
window= tk.Tk()
window.title("Data Acquisition Settings")
#create canvas for window
canvas1 = tk.Canvas(window, width=600, height=150, relief = 'raised')
canvas1.pack()

#entry for number of acquisitions 
ent1var = tk.StringVar()
entry1 = tk.Entry(window, textvariable= ent1var) 
entry1.pack()
canvas1.create_window(200, 40, window=entry1)
canvas1.create_text(200, 20, text="Number of Acquisitions")


button1 = tk.Button(window, text='Submit', command=combine_funcs(get_acquisitions, changeText_n_acquisitions))
button1.pack() 
canvas1.create_window(200, 80, window=button1)

#entry for acquisition time
ent2var = tk.StringVar()
entry2 = tk.Entry(window, textvariable= ent2var)
entry2.pack()
canvas1.create_window(400, 40, window=entry2)
canvas1.create_text(400, 20, text="Acquisition Time (s)")


button2 = tk.Button(window, text='Submit', command=combine_funcs(get_acquisition_time, changeText_acquisition_time))
button2.pack()
canvas1.create_window(400, 80, window=button2)


exit_button = tk.Button(window, text="Start Acqusition and Open Dashboard", command=Close)
exit_button.pack(pady=20)
#new_dashboard_button = tk.Button(window, text="Open Dashboard", command=open_Window)
#new_dashboard_button.bind("<Button-1>", lambda e: NewWindow(window))
#new_dashboard_button.pack(pady=20)


window.mainloop()

print("Value entered:")
print(n_acquisitions)
print(acquisition_time)




base_filename    = "analog-data.csv" #name of the CSV file generated
n_acquisitions   = int(n_acquisitions) #number of acquisitions
acquisition_time = int(acquisition_time) #seconds
n=0 #counter
n_bins = 10 #number of bins for histogram

print("Collecting data for " + str(acquisition_time) + " seconds")

#serial port setup
ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port: " + arduino_port)

#initialize array containing all acquired arrays as an numpy array
data_arr = np.array([])
#initialize array to store data of all acquisitions
sensor_data_all = [] #store data

x=np.linspace(0, 10, n_bins)
y=np.linspace(0, 10, n_bins)

#x,y=np.zeros(n_bins), np.zeros(10) 

print("x: ", x)
plt.ion() #

#create plot window to update in real time
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
#set axis limits
ax1.set_ylim(0, 100)
ax1.set_xlim(0, n_bins)

line1, = ax1.plot(x, y, 'r-')

#create a dictionay to store the data with n_bins keys
data_dict = {i:0 for i in range(n_bins)}


while n < n_acquisitions:

    

    n = n+1
    timeout = time.time() + acquisition_time #set the timeout

    #update filename
    fileName = dt.now().strftime("%Y_%m_%d-%H_%M_%S") + "-"+ base_filename

    #open new file with new filename for new acquisition 
    f = open(fileName, "a")
    print("Created file: " + fileName)


    #reset array 
    sensor_data = [] #store data





    while time.time() < timeout:
        
        getData=ser.readline()
        dataString = getData.decode('utf-8')
        data=dataString[0:][:-2]
        print(data)

        readings = data.split(",")
        #print("readings: ", readings)
        #convert readings to float and append to sensor_data array
        number = [float(x) for x in readings][0]
        sensor_data.append(readings)
        sensor_data_all.append(number)
        #update dictionary by updating the value of the key corresponding to the detected event 
        data_dict.update({int(number) : data_dict[int(number)] + 1})

        #update plot 
        line1.set_ydata(list(data_dict.values()))
        fig.canvas.draw()
        fig.canvas.flush_events()
        


    print("Data collection complete")

    # write the data to a CSV file
    with open(fileName, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(sensor_data)

    print("Data written to file")
    print("\n")

    f.close()

    #append new acquisitions to data_arr
    data_arr = np.append(data_arr, sensor_data)


#flatten data_arr
data_arr = data_arr.flatten()

##Create new ax figure
#fig, ax1 = plt.subplots()
#ax1 = plt.subplot2grid((2,1),(0,0))
#lineVal1, = ax1.hist(data_arr, bins=5)
#
#def onMouseMove(event):
#    ax1.lines = [ax1.lines[0]]
#    ax1.axvline(x=event.xdata, color="k")


