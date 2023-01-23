import time
import multiprocessing
from multiprocessing.managers import BaseManager
import serial
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib 
import matplotlib.pyplot as plt
import tkinter as tk
from dataclasses import dataclass, field
import random

#Deals with an issue with matplotlib on mac
matplotlib.use("TkAgg")

#My imports
import UI
#import PlotInteraction as pi
import Arduino
import AcquisitionSetupWindowv2 as acq



#create list with all parameters inside of the get_metrics function
params_list= ["Total Counts", "Start Time", "Preset Time", "ADC Channels", "Number of Acquisitions", "Save Directory","Data Collection Rate (Hz)"]

def create_header(settings_dict : dict):
    h = ["ADC Channels: " +  str(settings_dict["n_channels"]),
    "Number of Acquisitions: " + str(settings_dict["n_acquisitions"]),
    "Preset Time: " + str(settings_dict["t_acquisition"])
    ]
    return h

def get_metrics(data_dict : dict, settings_dict : dict, t_elapsed , print_flag=False):

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
        print ("Save directory: " + str(save_directory))

    return total_counts, start_time, preset_time, n_channels, n_acquisitions, count_rate, save_directory


def collect_data(dev : Arduino, 
                    shared_dict : dict, 
                    settings_dict : dict, 
                    lock : multiprocessing.Lock):
    
    n=0
    while settings_dict["stop_flag"] == False:
        while settings_dict["running_acquisition"]== True:
            while n < settings_dict["n_acquisitions"]:
                print("Starting data collection: " + str(n + 1) + " of " + str(settings_dict["n_acquisitions"]))
                #update settings dictionary
                settings_dict["current_n"] = n + 1
                #reset dictionary
                for key in range(settings_dict["n_channels"]):
                    shared_dict[key] = 0
                sensor_data = []
                #update filename
                fileName = dt.now().strftime("%Y_%m_%d-%H_%M_%S") + "-"+ settings_dict["savefile_default_name"] + "_" + str(n).zfill(4) + settings_dict["savefile_format"]
                #open new file with new filename for new acquisition 
                f = open(fileName, "w", newline='')
                print("Created file: " + fileName)
                writer = csv.writer(f)
                writer.writerow(create_header(settings_dict))
                while settings_dict["acquisition_duration"] < settings_dict["t_acquisition"]:
                    #print("acquisition duration: " + str(settings_dict["acquisition_duration"]))
                    #print("acquisition time: " + str(settings_dict["t_acquisition"]))
                    if settings_dict["stop_flag"] == False:
                        with lock:
                            val = dev.get_data_time_loop(sensor_data, shared_dict)
                            shared_dict[int(val)] += 1
                            shared_dict.update()   
                    #print("still collecting data")
                print("Completed data collection: " + str(dev.n + 1) + " of " + str(dev.n_acquisitions))
                #write data to file
                #print("Data to be written to file:" + str(shared_dict))
                for key, value in shared_dict.items():
                    writer.writerow([key, value])
                #writer.writerow(sensor_data)
                print("Saved data to file: " + fileName)
                # close file
                print("Data collection complete")
                print("\n")
                f.close()
                n=n+1
                if n == settings_dict["n_acquisitions"]:
                    with lock:
                        settings_dict["stop_flag"] = True
                        settings_dict.update()
                        #print("change stop flag to true inside collect data loop")

                #print("Stop Flag inside collect data: " + str(settings_dict["stop_flag"]))
    #print("escaped while loop")


def launch_setup_window():
    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
    return setup_window.return_params()

#create new process to read data from arduino after creating a new device object 
#this is necessary because the device object is not picklable
def create_device_read_process( shared_dict : dict,
                                settings_dict : dict,
                                lock : multiprocessing.Lock):

    device = Arduino.Arduino( n_acquisitions     = settings_dict["n_acquisitions"],
                                current_dict     = shared_dict,
                                n_channels       = settings_dict["n_channels"],
                                acquisition_time = settings_dict["t_acquisition"])  

    collect_data(device, 
                    shared_dict, 
                    settings_dict, 
                    lock) 


x_val1 = 0
y_val1 = 0

def onclick(event : matplotlib.backend_bases.MouseEvent):
    global x_val1, y_val1

    if event.inaxes:
        fig = plt.gcf()
        if hasattr(fig, 'line'):
            fig.line.remove()
        fig.line = plt.axvline(event.xdata, color='black')
        x_val1 = event.xdata
        y_val1 = event.ydata
        fig.canvas.draw()
    return x_val1


def launch_main_window(settings : dict, shared_dict : dict):

    
    #first we create the figure to pass to the UI class
    x=np.linspace(1, settings["n_channels"], settings["n_channels"])
    y=np.linspace(1, settings["n_channels"], settings["n_channels"])
    fig, ax1  = plt.subplots()
    ax1.set_ylim(0, 100)
    ax1.set_xlim(0, settings["n_channels"])
    ax1.set_title("Data Acquisition")
    ax1.set_xlabel("Channel")
    ax1.set_ylabel("Counts")
    ax1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.5)
    
    #draw a tentative plot 
    
    line1, = ax1.plot(x, y, 'r-')
    line2 = ax1.scatter(x, y, c='b', marker='o', s=10, alpha=0.5)

    #create the main window using the UI class
    root= tk.Tk()
    win = UI.UI_Window(root, title = "Main window", geometry = "1000x700", matplot_fig = fig)

    t_start = time.time()
    now=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
    cid = None
    lines = []
    #array to store the times at which the acquisition is started and stopped 
    current_time : float = 0
    end_of_iteration : float = 0
    #main UI window loop that runs the acquisition is stopped and the command is given to terminate the program
    while settings["stop_flag"] == False and win.acquisition_settings.main_program_open == True:
        #loop that runs the acquisition if the command is given to start it
        while win.acquisition_settings.running_acquisition == True:
            current_time = time.time()
            #updating the settings dictionary with the values entered by the user 
            settings["running_acquisition"] = win.acquisition_settings.running_acquisition
            settings["n_acquisitions"] = win.acquisition_settings.n_acquisitions
            settings["t_acquisition"] = win.acquisition_settings.t_acquisition
            settings["clear_plot"] = win.acquisition_settings.clear_flag
            settings["plot_scale"] = win.acquisition_settings.plot_scale
            #print("Stop Flag inside RUN UI at the START: " + str(settings["stop_flag"]))
            #getting metrics from the data acquisition process
            total_counts = sum(shared_dict.values())
            start_time = now
            preset_time = settings["t_acquisition"] 
            n_channels = settings["n_channels"]
            n_acquisitions = settings["n_acquisitions"]
            current_acquisition = settings["current_n"]

            #t_elapsed is the minimum of the elapsed time and the preset time
            t_elapsed = min(round(time.time() - t_start,1), preset_time)
            count_rate = round(float(total_counts)/(t_elapsed+0.0001),2)

            metrics= [total_counts, start_time, preset_time, n_channels, n_acquisitions, current_acquisition, t_elapsed, count_rate]

            #update y_data taking into account the threshold and replace the erased values by zeros
            if settings["clear_plot"] == True:
                for key in range(settings["n_channels"]):
                    shared_dict[key] = 0
                y_temp = [shared_dict[i] if i >= settings["threshold"] else 0 for i in range(settings["n_channels"])]
                settings["clear_plot"] = False
            else:
                y_temp= [shared_dict[i] if i >= settings["threshold"] else 0 for i in range(settings["n_channels"])]
            #line1.set_ydata(list(shared_dict.values()))
            win.acquisition_settings.clear_flag = False
            line1.set_ydata(y_temp)
            line1.set_xdata(x)
            line2.set_offsets(np.c_[x,y_temp])

            ax1.set_ylim(0, 1.1*max(shared_dict.values())+ 5)
            ax1.set_yscale(settings["plot_scale"])
            # clear the fill
            #fill.remove()
            #ax1.fill_between(x, y_temp, color='red', alpha=0.5)

            if settings["threshold"] != 0: 
                line = ax1.axvline(x=settings["threshold"], color='blue', linestyle='--', linewidth=0.5)
                lines.append(line)
            for line in lines[:-1]:
                line.remove()
                lines.remove(line)    
            if cid is not None:
                fig.canvas.mpl_disconnect(cid)
            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            fig.canvas.draw()
            fig.canvas.flush_events()

            #print("x: " + str(x_val1))
            #print("y: " + str(y_val1))
            interactive_metrics = [settings["threshold"], x_val1, y_temp[int(x_val1)]]
            #print(settings_dict["current_n"])
            new_threshold= win.run_real_time(metrics = metrics, interactive_metrics = interactive_metrics)
            settings["threshold"] = new_threshold
            time.sleep(0.01)

            #print("Stop Flag inside RUN UI at the END: " + str(settings["stop_flag"]))
            end_of_iteration = time.time()
            settings["acquisition_duration"] += end_of_iteration - current_time
            settings.update()
            #print("acquisition duration inside plot loop: " + str(settings["acquisition_duration"]))
            win.root.update() 
        win.root.update() 
        time.sleep(0.01) 


    while win.acquisition_settings.main_program_open == True:
        settings["running_acquisition"] = win.acquisition_settings.running_acquisition
        settings["n_acquisitions"] = win.acquisition_settings.n_acquisitions
        settings["t_acquisition"] = win.acquisition_settings.t_acquisition
        settings["clear_plot"] = win.acquisition_settings.clear_flag
        settings["plot_scale"] = win.acquisition_settings.plot_scale
        total_counts = sum(shared_dict.values())
        #update y_data taking into account the threshold and replace the erased values by zeros
        if settings["clear_plot"] == True:
            for key in range(settings["n_channels"]):
                shared_dict[key] = 0
            y_temp = [shared_dict[i] if i >= settings["threshold"] else 0 for i in range(settings["n_channels"])]
            settings["clear_plot"] = False
        else:
            y_temp= [shared_dict[i] if i >= settings["threshold"] else 0 for i in range(settings["n_channels"])]
        #line1.set_ydata(list(shared_dict.values()))
        win.acquisition_settings.clear_flag = False
        line1.set_ydata(y_temp)
        line1.set_xdata(x)
        line2.set_offsets(np.c_[x,y_temp])
        ax1.set_ylim(0, 1.1*max(shared_dict.values())+ 5)
        ax1.set_yscale(settings["plot_scale"])
        # clear the fill
        #fill.remove()
        #ax1.fill_between(x, y_temp, color='red', alpha=0.5)
        if settings["threshold"] != 0: 
            line = ax1.axvline(x=settings["threshold"], color='blue', linestyle='--', linewidth=0.5)
            lines.append(line)
        for line in lines[:-1]:
            line.remove()
            lines.remove(line)    
        if cid is not None:
            fig.canvas.mpl_disconnect(cid)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        fig.canvas.draw()
        fig.canvas.flush_events()
        #print("x: " + str(x_val1))
        #print("y: " + str(y_val1))
        interactive_metrics = [settings["threshold"], x_val1, y_temp[int(x_val1)]]
        #print(settings_dict["current_n"])
        new_threshold= win.run_real_time(metrics = metrics, interactive_metrics = interactive_metrics)
        settings["threshold"] = new_threshold
        win.root.update() 
          


if __name__ == "__main__":

    #manager and lock for shared memory dictionary
    manager = multiprocessing.Manager()
    lock= multiprocessing.Lock()
    

    #shared dictionary
    settings = manager.dict()
    settings["stop_flag"] : bool = False
    settings["n_channels"] : int = 512
    settings["threshold"] : int = 0
    settings["t_acquisition"] : float = 3
    settings["start_time"] : float = 0
    settings["total_counts"] : int = 0
    settings["current_n"] : int = 0
    settings["n_acquisitions"] : int = 1
    settings["t_elapsed"] : float = 0
    settings["acquisition_duration"] : float = 0
    settings["count_rate"] : float = 0
    settings["plot_scale"] : str = "linear"
    settings["baud"] : int = 9600
    settings["clear_plot"] : bool = False
    settings["running_acquisition"] : bool = False
    settings["savefile_default_name"] : str = "Analog_Data"
    settings["savefile_default_folder"] : str = "DataAcquisition"
    settings["savefile_format"] : str = ".csv"
    settings["savefile_default_directory"] : str = os.path.join((os.path.dirname(os.path.realpath(__file__))), settings["savefile_default_folder"])
    
    #shared dictionary for the data acquisition process
    current_acquisition_dict = manager.dict()
    #set entire dictionary to 0
    for key in range(settings["n_channels"]):
        current_acquisition_dict[key] = 0

    
    root = tk.Tk()
    setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "450x150")

    input_settings= setup_window.return_params()
    #settings= Settings.Settings(n_channels=input_settings.n_channels)
    #manager.register('Settings', Settings.Settings)
    #print("Received parameters:")
    #setup_window.print_params()


    if not os.path.exists(settings["savefile_default_directory"]):
        os.makedirs(settings["savefile_default_directory"])
        print("Directory did not exist. Created savefile directory at " + settings["savefile_default_directory"])
        #change directory to the new folder
        os.chdir(settings["savefile_default_directory"])
    else:
        #change directory to the new folder
        os.chdir(settings["savefile_default_directory"])
    
    print(".....................Starting data acquisition.....................")
    print("Number of acquisitions:", str(int(settings["n_acquisitions"])))
    print("Acquisition time:", str(settings["n_acquisitions"]), " seconds")





    #settings.update_with_inputs(input_settings)   

    #dictionary with all settings for the current acquisition 
    


   

    #create new process to read data from arduino 
    read_data = multiprocessing.Process(target=create_device_read_process, 
                                        args=(current_acquisition_dict, 
                                            settings, 
                                            lock))


    main_window_process = multiprocessing.Process(target=launch_main_window,
                                                    args=(settings,
                                                            current_acquisition_dict))

    #starting all processes
    read_data.start()
    main_window_process.start()

    #wait for all processes to finish
    read_data.join()
    main_window_process.join()

    
