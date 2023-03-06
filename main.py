import multiprocessing
from multiprocessing.managers import BaseManager
from dataclasses import dataclass, field
import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer

#my imports 
from AcquisitionParams import * 
import Arduino as device
from DataRetriever import *
from MainWindow import *


def run(acquisition_parameters : AcquisitionParameters):

      dev = device.Arduino(channels=acquisition_parameters.get_n_channels())

      #create the data retriever
      data_retriever = DataRetriever(dev, acquisition_parameters)

      data_retriever.get_multiple_acquisitions(acquisition_parameters)


def run_main_window(acquisition_parameters : AcquisitionParameters):
      app = QApplication(sys.argv)
      icon = QtGui.QIcon('Icon.png')
      app.setWindowIcon(icon)
      window = MainWindow(acquisition_parameters)
      
      
      # Connect a slot to the destroyed signal
      window.destroyed.connect(lambda: print("Window closed"))
      window.show()

      #check if the window is open
      def check_window_open():
            #print(str(window.isVisible()))
            if window.isVisible():
                  
                  #print("window open")
                  acquisition_parameters.set_window_is_open(True)
                  window.update_plot(acquisition_parameters)
                  window.populate_metrics_grid(acquisition_parameters)
                  window.update_peak_counts(acquisition_parameters)
                  #sleep(0.2)
                  QTimer.singleShot(10, check_window_open)
            else:
                  
                  acquisition_parameters.set_window_is_open(False)
                  window.update_plot(acquisition_parameters)
                  window.populate_metrics_grid(acquisition_parameters)
                  window.update_peak_counts(acquisition_parameters)
                  QTimer.singleShot(10, app.quit)

      QTimer.singleShot(10, check_window_open)

      signal = AppSignal()
      signal.finished.connect(app.quit)
      app.aboutToQuit.connect(signal.finished.emit)
      sys.exit(app.exec())   



if __name__ == "__main__":
      
      #create the lock

      lock = multiprocessing.Lock()

      #create a multiprocessing event
      stop_event = multiprocessing.Event()

      #create the manager
      BaseManager.register('AcquisitionParameters', AcquisitionParameters)
      manager = BaseManager()
      manager.start()
      managed_acquisition_parameters = manager.AcquisitionParameters()


      #define the default acquisition parameters
      managed_acquisition_parameters.set_t_acquisition(400)
      managed_acquisition_parameters.set_n_acquisitions(2)
      managed_acquisition_parameters.set_n_channels(1024) 

      #create the process
      GUI_process = multiprocessing.Process(target=run_main_window, args=(managed_acquisition_parameters,))
      process = multiprocessing.Process(target=run, args=(managed_acquisition_parameters,))
      

      #start the processes
      GUI_process.start()
      process.start()
      
      #kill background processes when the main process is killed
      GUI_process.join()
      process.terminate()

