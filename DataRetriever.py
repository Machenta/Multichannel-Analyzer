import ArduinoV2 as device
from AcquisitionParams import *
import multiprocessing
import datetime as dt
from time import sleep, time, perf_counter, perf_counter_ns
import multiprocessing

class DataRetriever: 
      def __init__(self, 
                  device : device.Arduino, 
                  acquisition_parameters : AcquisitionParameters):


            self.device = device
            self.val=0
            self.t_start = 0
            self.t_end = 0
            self.t_total_acq = 0
            #self.acquisition_parameters = acquisition_parameters 

      def update_parameters(self, acquisition_parameters : AcquisitionParameters):
            self.acquisition_parameters = acquisition_parameters

      def prepare_acquisition(self):
            self.device.prepare_acquisition()

      def get_data(self):
            return self.device.read_serial()

      def set_current_file_name (self):
            self.acquisition_parameters.set_current_filename(self.acquisition_parameters.get_default_filename() + "_" + 
                                                            str(self.acquisition_parameters.get_start_time()) + "_" + 
                                                            str(self.acquisition_parameters.get_current_n()).zfill(4) + 
                                                            self.acquisition_parameters.get_savefile_format())

      def prepare_acquisition(self, 
                              acquisition_parameters : AcquisitionParameters):
            #update the acquisition parameters 
            acquisition_parameters.update_current_n() #increment the current acquisition number
            acquisition_parameters.set_start_time( dt.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")) #set the start time
            acquisition_parameters.set_current_filename(acquisition_parameters.get_default_filename() + "_" + 
                                                            str(acquisition_parameters.get_start_time()) + "_" + 
                                                            str(acquisition_parameters.get_current_n()).zfill(4) + 
                                                            acquisition_parameters.get_savefile_format()) #set the current filename
            print("Preparing acquisition: " + str(acquisition_parameters.get_current_filename()))
            #reset the current acquisition dictionary
            #acquisition_parameters.create_dict()
            acquisition_parameters.clear_data_current_acq()
            self.device.prepare_acquisition()

      def set_save_directory(self, acquisition_parameters : AcquisitionParameters):
            #if the directory does not exist, create it
            save_dir= acquisition_parameters.get_acquisition_filesave_directory()
            #save_dir = os.path.join(acquisition_parameters.get_dir_path(), acquisition_parameters.get_default_save_folder())
            if not os.path.exists(save_dir):
                  os.makedirs(save_dir)
                  print("Directory " , save_dir ,  " Created ")

                  #change the current directory to the save directory
                  os.chdir(save_dir)
                  acquisition_parameters.set_acquisition_filesave_directory(save_dir)
            else: 
                  print("Directory " , save_dir ,  " already exists. Saving to this directory.")
                  acquisition_parameters.set_acquisition_filesave_directory(save_dir)

      def save_acquisition(self, acquisition_parameters : AcquisitionParameters):
            #Save the acquisition
            self.set_save_directory(acquisition_parameters)

            print("Saving data to: " + str(acquisition_parameters.get_acquisition_filesave_directory()))
            file = os.path.join(acquisition_parameters.get_acquisition_filesave_directory(), acquisition_parameters.get_current_filename())
            with open(file, "w", newline="") as f:
                  writer = csv.writer(f)
                  writer.writerow(acquisition_parameters.create_header())
                  for key, value in acquisition_parameters.get_current_acq().items():
                        writer.writerow([key, value])
            print("Data saved to: " + str(acquisition_parameters.get_acquisition_filesave_directory()))
            return acquisition_parameters.get_acquisition_filesave_directory()

      def get_value_from_device (self, acquisition_parameters : AcquisitionParameters):

            while (self.t_total_acq) < acquisition_parameters.get_t_acquisition():
                        while acquisition_parameters.get_acquisition_running() == True and (self.t_total_acq) < acquisition_parameters.get_t_acquisition():
                              #start the timer 
                              self.t_start = perf_counter()
                              #get the data from the arduino
                              self.val = self.get_data()
                              #get the time at the end of the acquisition
                              self.t_end = perf_counter()
                              #update the current acquisition duration with the time it took to get the data by adding the time it took to get the data
                              self.t_total_acq = round(self.t_end-self.t_start, 7)
                              #return the data and the time it took to get the data
                              return self.val, self.t_total_acq

      def save_params (self, acquisition_parameters : AcquisitionParameters):

             while (self.t_total_acq) < acquisition_parameters.get_t_acquisition():
                        while acquisition_parameters.get_acquisition_running() == True and (self.t_total_acq) < acquisition_parameters.get_t_acquisition():
                              #save the acquisition parameters to the shared memory
                              acquisition_parameters.update_for_single_pass(self.t_total_acq, self.t_total_acq, self.val,)


      def get_one_full_acquisition(self, lock : multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):
            print("Acquisition running: " + str(acquisition_parameters.get_acquisition_running()))

            #Prepare the acquisition
            self.prepare_acquisition(acquisition_parameters)
            #check condictions for acquisition
            #make sure the acquisition is supposed to be running 
            t_total_acq = 0
            t_total_acq1 = 0
            live_time = 0
            while acquisition_parameters.get_acquisition_running() == True:

                   #reset the current live time on the acquisition parameters
                  acquisition_parameters.set_live_time(0) 
                  #run the acquisition for the preset time

                  #spin up two processes to run the acquisition and save the data at the same time
                  #p1 = multiprocessing.Process(target=self.get_value_from_device, args=(acquisition_parameters,))
                  #p2 = multiprocessing.Process(target=self.save_params, args=(acquisition_parameters,))
#
                  ##start the processes
                  #p1.start()
                  #p2.start()
#
                  ##join the processes
#
                  #p1.join()
                  #p2.join()

                  while (t_total_acq) < acquisition_parameters.get_t_acquisition():
                        while acquisition_parameters.get_acquisition_running() == True and (t_total_acq) < acquisition_parameters.get_t_acquisition():
                        #check the stop acquisition flag by evaluating the "acquisition_running" flag 



                              #get the time at the start of the acquisition
                              t_start = perf_counter()
                              #with lock:
                              #get the data from the arduino
                              val = self.get_data()
                              #update the current acquisition with the new data
                              #acquisition_parameters.current_acq[int(val)] = val
                              acquisition_parameters.update_current_acq_channel(int(val))
                              #save the data
                              #print("Data: " + str(val))

                              #get the time at the end of the acquisition
                              t_end = perf_counter()
                              #update the current acquisition duration with the time it took to get the data by adding the time it took to get the data

                              t_total_acq += round(t_end-t_start,9)

                              #subtract the dead time from the acquisition time of 100us
                              live_time += (t_end-t_start) - 0.0001
                              #update total counts in the acquisition
                              t_start1 = perf_counter()
                              print("t_loop: " + str(round(t_end-t_start,7)))
                              #if val != 0:
                              #      acquisition_parameters.update_total_counts()
                              ##update the live time
                              #acquisition_parameters.set_current_acq_duration(t_total_acq)
                              #acquisition_parameters.set_live_time(live_time)
                              acquisition_parameters.update_for_single_pass(live_time, t_total_acq, val)
                              #print("t_total_acq: " + str(t_total_acq))
                              
                              #print("t_acquisition: " + str(acquisition_parameters.get_t_acquisition()))

                              t_end1 = perf_counter()
                              t_total_acq1 = round(t_end1-t_start1,9)
                              print("time to save data: " + str(t_total_acq1))

                  #update the current acquisition duration with the time it took to get the data
                  acquisition_parameters.set_current_acq_duration(t_total_acq)
                  acquisition_parameters.set_live_time(live_time)
                  #save the acquisition
                  self.save_acquisition(acquisition_parameters)        
                  #reset the running_acquisition flag
                  acquisition_parameters.set_acquisition_running(False)
                  


      def get_multiple_acquisitions(self, lock : multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):
            #getting multiple acquisitions is just a loop of get_one_full_acquisition
            while True:
                  while acquisition_parameters.get_window_is_open() == True:
                        #check condictions for acquisition
                        n=0
                        while acquisition_parameters.get_current_n() < acquisition_parameters.get_n_acquisitions():
                              #make sure the acquisition is supposed to be running
                              
                              while acquisition_parameters.get_acquisition_running() == True:
                                    #start the acquisition for the number of times specified
                                    # we need to reset the running_acquisition flag to true
                                    print("Starting acquisition: " + str(acquisition_parameters.get_current_n()) + " of " + str(acquisition_parameters.get_n_acquisitions()))

                                    self.get_one_full_acquisition(lock , acquisition_parameters)
                                    #update the current acquisition number
                                    n += 1
                                    acquisition_parameters.set_current_n(n)

                                    #reset total counts
                                    acquisition_parameters.set_total_counts(0)
                                    #if the number of acquisitions is reached, stop the acquisition if not, continue
                                    if acquisition_parameters.get_current_n() == acquisition_parameters.get_n_acquisitions():
                                          acquisition_parameters.set_acquisition_running(False)
                                          print("Acquisition finished")
                                          sleep(0.2)
                                    else:
                                          acquisition_parameters.set_acquisition_running(True)
                                    sleep(0.1)