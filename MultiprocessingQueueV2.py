import time
import multiprocessing
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Arduino
import tkinter as tk
import AcquisitionSetupWindow as acq


stop_flag = False
#create new process to read data from arduino
#read_data = multiprocessing.Process(target=device.full_collection, args=(all_arr))

#create list with all parameters inside of the get_metrics function
params_list= ["Total Counts", "Start Time", "Preset Time", "ADC Channels", "Number of Acquisitions", "Save Directory","Data Collection Rate (Hz)"]


def collect_data(dev, all_arr, q, settings_dict, lock):
    
    n=0
    while n < settings_dict["n_acquisitions"]:

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

def get_metrics(data_dict, settings_dict, lock, t_elapsed, print_flag=False):

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

    return total_counts, start_time, preset_time, n_channels, n_acquisitions, count_rate

def update_table(table,new_data,canvas):
    for i in range(1):
        for j in range(6):
            table.get_celld()[(i,j)].get_text().set_text(str(new_data[i][j]))
    canvas.draw()
    root.after(1, update_table)        
    return table


def print_q_plot(q, settings_dict, lock, q_val_arr, vals_dict, params_list):


    x=np.linspace(0, 10, settings_dict["n_channels"])
    y=np.linspace(0, 1, settings_dict["n_channels"])
    #plt.ion()

    #create plot window to update in real time
    fig, ax1  = plt.subplots()
    ax1.set_title("Multichannel Acquisition")
    #set axis limits
    ax1.set_ylim(0, 100)
    ax1.set_xlim(0, settings_dict["n_channels"])

    line1, = ax1.plot(x, y, 'r-')

    data_dict = {i:0 for i in range(settings_dict["n_channels"])}

    #launch window to imbed plot
    root = tk.Tk()
    root.title("Multichannel Acquisition") 
    root.geometry("1000x1000")
    root.configure(background='white')

    #draw canvas to imbed plot
    canvas_plot = FigureCanvasTkAgg(fig, master=root)
    canvas_plot.draw()


    fig_table, ax_table = plt.subplots()
    ax_table.axis('off')
    table= ax_table.table(cellText=[[params_list[i], 0] for i in range(len(params_list))], loc='center')
    ax_table.add_table(table)
    canvas_table = FigureCanvasTkAgg(fig_table, master=root)
    canvas_table.draw()
    canvas_table.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    #create am empty 1x6 table to imbed in canvas
    empty_data = [[0 for j in range(1)] for i in range(6)]
    #table = ax1.table(cellText=empty_data, loc='right')
    #ax_table = fig.add_subplot(211)
    #table = ax1.table(cellText=empty_data, loc='right')
    #ax_table.add_table(table)
    #ax_table.axis('off')

    canvas_plot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    #table.scale(1,1.5)



    t_start=time.time()
    while not settings_dict["stop_flag"]:
        while not q.empty():
            last_element = q.get()
            vals_dict.update({int(last_element) : vals_dict[int(last_element)] + 1})
            q_val_arr.append(last_element)
            data_dict.update({int(last_element) : data_dict[int(last_element)] + 1})
            print("Last element: " + str(last_element))
            print("q_val_arr inside loop: " + str(q_val_arr))
            print("vals_dict inside loop: " + str(vals_dict))

            #update plot 
            line1.set_ydata(list(data_dict.values()))
            ax1.set_ylim(0, 1.1*max(data_dict.values()))
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.001)

            elpsd_time = time.time() - t_start
            total_counts, start_time, preset_time, n_channels, n_acquisitions, count_rate= get_metrics(data_dict, settings_dict, lock, elpsd_time, print_flag=True)

            #update window
            root.title("Multichannel Acquisition - " + str(round(elpsd_time,2)) + "s elapsed")
            root.update()


    print("Vals dict outside of loop: " + str(vals_dict))
    print("Finished printing queue")

    #update window
    root.mainloop()
    return q_val_arr

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

def read_test (q_val_arr, settings_dict, lock):
    while not settings_dict["stop_flag"]:
        print("q_val_arr inside test process: " + str(q_val_arr))
        time.sleep(0.5)

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
            time.sleep(0.0001)

        #print("sensor_data: " + str(sensor_data))
        print("Completed data collection: " + str(device.n + 1) + " of " + str(int(device.n_acquisitions)))
        #write data to file
        writer = csv.writer(f)
        writer.writerow(sensor_data)
        # close file
        print("Data collection complete")
        print("\n")
        f.close()

        n += 1
        

        settings_dict.update({"stop_flag":True})
        settings_dict.update()
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
    vals_dict = manager2.dict()
    vals_dict = {i:0 for i in range(n_channels)}

    #create new process to read data from arduino 
    read_data = multiprocessing.Process(target=create_device_read_process, args=(q_vals,arduino_port, baud, q, settings_dict,lock))

    #process to print the shared dictionary
    print_dict_proc = multiprocessing.Process(target=print_q_plot, args=(q, settings_dict, lock, q_vals, vals_dict, params_list))

    #test process to see if the queue is being updated
    #test_proc = multiprocessing.Process(target=read_test, args=(q, vals_dict, settings_dict, lock))


    #create new process to save data from queue to array
    #save_data_proc = multiprocessing.Process(target=save_val, args=(q_vals, q, settings_dict, lock))

    #process to sync the shared dictionary
    #sync_dict_proc = multiprocessing.Process(target=sync_dict, args=(q, lock, settings_dict))

    #process for UI, data analysis and plotting
    #UI_process = multiprocessing.Process(target=launch_setup_window, args=(all_arr, current_acquisition_dict, settings_dict))

    #sync_dict_proc.start()
    #sync_dict_proc.join()

    read_data.start()
    print_dict_proc.start()
    #test_proc.start()
    #save_data_proc.start()
    
    read_data.join()
    print_dict_proc.join()
    #test_proc.join()
    #save_data_proc.join()
    

