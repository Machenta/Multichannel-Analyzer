import ArduinoV2 as device
from AcquisitionParams import *
import multiprocessing
import datetime as dt

class DataRetriever: 
      def __init__(self, 
                  device : device.Arduino, 
                  acquisition_parameters : AcquisitionParameters):


            self.device = device
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
            save_dir = os.path.join(acquisition_parameters.get_dir_path(), acquisition_parameters.get_default_save_folder())
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

      def get_one_full_acquisition(self, lock : multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):

            #Prepare the acquisition
            self.prepare_acquisition(acquisition_parameters)
            
            #check condictions for acquisition

            #make sure the acquisition is supposed to be running 
            while acquisition_parameters.get_acquisition_running() == True:
                  t_total_acq = 0 
                  
                   #reset the current live time on the acquisition parameters
                  acquisition_parameters.set_live_time(0) 
                  
                  #run the acquisition for the preset time
                  while (t_total_acq) < acquisition_parameters.get_t_acquisition() and acquisition_parameters.get_acquisition_running() == True:
                        
                        t_start = dt.datetime.now()
                        with lock:
                              #get the data from the arduino
                              val = self.get_data()
                              #update the current acquisition with the new data
                              #acquisition_parameters.current_acq[int(val)] = val
                              acquisition_parameters.update_current_acq_channel(int(val))
                              #save the data
                              print("Data: " + str(val))
                        t_end = dt.datetime.now()

                        #update the current acquisition duration with the time it took to get the data
                        t_total_acq += (t_end-t_start).total_seconds()
                        print("t_total_acq: " + str(t_total_acq))
                        print("t_acquisition: " + str(acquisition_parameters.get_t_acquisition()))
                  #update the current acquisition duration with the time it took to get the data
                  acquisition_parameters.set_current_acq_duration(t_total_acq)
                  #save the acquisition
                  self.save_acquisition(acquisition_parameters)         
                  #reset the running_acquisition flag
                  acquisition_parameters.set_acquisition_running(False)

      def get_multiple_acquisitions(self, lock : multiprocessing.Lock, acquisition_parameters : AcquisitionParameters):
            #getting multiple acquisitions is just a loop of get_one_full_acquisition

            #check condictions for acquisition
            while acquisition_parameters.get_current_n() < acquisition_parameters.get_n_acquisitions():
                  # we need to reset the running_acquisition flag to true
                  print("Starting acquisition: " + str(acquisition_parameters.get_current_n()) + " of " + str(acquisition_parameters.get_n_acquisitions()))
                  acquisition_parameters.set_acquisition_running(True)
                  self.get_one_full_acquisition(lock , acquisition_parameters)