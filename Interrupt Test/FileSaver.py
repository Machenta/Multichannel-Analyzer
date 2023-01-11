import serial
import csv
import os

arduino_port = "/dev/cu.usbmodem11101" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud
#get directory path
dir_path = os.path.dirname(os.path.realpath(__file__))

#change file directory to dir_path
os.chdir(dir_path)
print("Changed directory to " + dir_path)

fileName="analog-data.csv" #name of the CSV file generated


ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
f = open(fileName, "a")
print("Created file")
getData = ser.readline()
dataString = getData.decode("utf-8") #ser.readline returns a binary, convert to string
data = dataString[0:len(dataString)-2] #remove the new-line chars 
print(data) #write the data to the console

readings = data.split(",") #split the string into an array called 'readings'
sensor_data = [] #create a new array called 'sensor_data'
sensor_data.append(readings) 

print(sensor_data) #write the data to the console

samples = 20 #how many samples to collect
print_labels = False
line = 0 #start at 0 because our header is 0 (not real data)
sensor_data = [] #store data

# collect the samples
while line <= samples:
    getData=ser.readline()
    dataString = getData.decode('utf-8')
    data=dataString[0:][:-2]
    print(data)

    readings = data.split(",")
    print(readings)

    sensor_data.append(readings)
    print(sensor_data)

    line = line+1


# write the data to a CSV file
with open(fileName, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(sensor_data)

print("Data written to file")

#create a window with a button to close the file
from tkinter import *




f.close()




