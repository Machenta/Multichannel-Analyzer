import multiprocessing
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import numpy as np
from datetime import datetime as dt


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


if __name__ == "__main__":
      #create the manager
      #manager = multiprocessing.Manager()
      #manager.register('AcquisitionParameters', AcquisitionParameters)
      #create the lock
      lock = multiprocessing.Lock()

      BaseManager.register('AcquisitionParameters', AcquisitionParameters)
      manager = BaseManager()
      manager.start()
      managed_acquisition_parameters = manager.AcquisitionParameters()

      managed_acquisition_parameters.set_t_acquisition(1)
      managed_acquisition_parameters.set_n_acquisitions(1)
      managed_acquisition_parameters.set_n_channels(512) 
      #managed_acquisition_parameters.set_default_save_folder("test_folder")

      #create the acquisition parameters
      #managed_acquisition_parameters = AcquisitionParameters(t_acquisition=5)

             
      #create the process
      process = multiprocessing.Process(target=run, args=(lock, managed_acquisition_parameters))
      #process_main_window = multiprocessing.Process(target=run_main_window, args=(lock, managed_acquisition_parameters))
      #create another process
      #process2 = multiprocessing.Process(target=run2, args=(lock, managed_acquisition_parameters))
      metrics_process = multiprocessing.Process(target=metrics_backend, args=(lock, managed_acquisition_parameters))
      GUI_process = multiprocessing.Process(target=run_main_window, args=(lock, managed_acquisition_parameters))

      #start the process
      process.start()
      metrics_process.start()
      GUI_process.start()


      #join the process
      process.join()
      metrics_process.join()
      GUI_process.join()