import time 
import multiprocessing
from AcquisitionParams import * 


class Timer():
      def __init__(self):
            #getting the start time to use as a reference for the timer
            self.init_time : float = 0
            self.run_condition : bool = False
            self.run_time : float = 0
            self.current_run_time : float = 0
            self.total_run_time : float = 0
            self.update_interval : float = 0.3
            self.loop_init_time : float = 0
            self.stop_timer_flag : bool = False
            print("Successfully created a timer.")


      def initialize(self, total_time : float ):
            #getting the start time to use as a reference for the timer
            self.init_time = time.perf_counter()

            #get a run time for the acquisition
            self.total_run_time = total_time

            print("Started a timer with a run time of " + str(self.total_run_time) + " seconds.")


      def run_timer(self, total_time : float):
            print("Running timer")
            #getting the total time the acquisition should run
            self.initialize(total_time)

            print("Total run time: " + str(self.total_run_time))
            print("Current run time: " + str(self.run_time))

            self.stop_timer_flag = False

            self.init_time = time.perf_counter()

            #create a timer that runs for the specified time and then stops 
            #cannot be changed after calling the run_timer method
            #the total time is evaluated on a per loop basis because it must stop when the user presses the stop button
            t_loop_end = 0
            while self.run_time <= self.total_run_time: 
                  
                  while self.run_time <= self.total_run_time and self.stop_timer_flag == False:
                        t_loop_start = time.perf_counter()
                        #self.run_condition = True
                        #only update the run time every 10 ms
                        # this is to reduce overhead
                        time.sleep(0.05)
                        #vars= self.run_condition, self.run_time
                        #self.run_time = time.perf_counter() - self.init_time
                        t_loop_end = time.perf_counter()
                        t_loop= t_loop_end - t_loop_start
                        self.run_time += t_loop
                        time_left = self.update_interval - t_loop
                        #print("Loop time: " + str(t_loop))
                        
                        print("Total run time: " + str(self.run_time))
            print("Timer finished")

      def get_current_run_time(self):
            return time.perf_counter_ns() 
      
      def start_timer(self):
            self.init_time = time.perf_counter_ns()
            print("Timer started")

      def get_run_time(self):
            return time.perf_counter_ns() - self.init_time

if __name__ == "__main__":

      t= Timer()
      t.run_timer(3)
