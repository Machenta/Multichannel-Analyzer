import time 
from AcquisitionParams import * 


class Timer():
      def __init__(self,
                  acquisition_parameters : AcquisitionParameters):
            #getting the start time to use as a reference for the timer
            self.init_time : float = 0
            self.stop : bool = False

      def start_timer(self, acquisition_parameters : AcquisitionParameters):
            #getting the start time to use as a reference for the timer
            self.init_time = time.time()

            #update the acquisition parameters start time
            acquisition_parameters.set_current_act_start_time(self.init_time)

      def get_run_time(self, acquisition_parameters : AcquisitionParameters):

            #getting the run time of the current acquisition
            run_time = time.time() - self.init_time

            #updating the acquisition parameters run time
            #this is used to calculate the time remaining and to update the display window
            #we use this method because it allows for reduces overhead by accessing the acquisition parameters only once
            
            if run_time >= acquisition_parameters.get_t_acquisition():
                  stop = True

            acquisition_parameters.update_run_time_and_status(run_time, stop)

            return 