import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
import pyqtgraph as pg
from AcquisitionParams import *
from PlotterQT import *

uiclass, baseclass = pg.Qt.loadUiType("untitled.ui")

class MainWindow(uiclass, baseclass):
      def __init__(self, acq_params : AcquisitionParameters ):
            super().__init__()
            self.setupUi(self)

            self.left = 50
            self.top = 50
            self.width = 1300
            self.height = 1000
            self.title = 'MainWindow'
            self.initPlot(AcquisitionParameters = acq_params)

            #give functionality to the buttons in the GUI that are placed above the plot window
            self.start_button.clicked.connect(lambda: self.start_button_clicked(acq_params))
            self.restart_button.clicked.connect(lambda: self.restart_button_clicked(acq_params))
            self.stop_button.clicked.connect(lambda: self.stop_button_clicked(acq_params))
            self.clear_button.clicked.connect(lambda: self.clear_button_clicked(acq_params))

            #populate the metrics grid with the metrics that are available
            self.populate_metrics_grid(acq_params)
            
            #print if the window is open
            


      def initPlot(self, AcquisitionParameters: AcquisitionParameters):
        #m = tests.Plotter(self.PlotdrawWidget, width=10, height=12)
        #m.move(0,0)
        #self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        #self.show()

            m = Plotter(acquisition_parameters =AcquisitionParameters, 
                        parent = self.PlotdrawWidget, 
                        width=10, 
                        height=10)  
            m.move(0,0)
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(m)
            self.PlotdrawWidget.setLayout(layout)



      #functions that are called when the user clicks on the buttons
      def start_button_clicked(self, acq_params : AcquisitionParameters):
            #update the acquisition parameters
            acq_params.set_acquisition_running(True)
            print("self.acq_params", acq_params.get_acquisition_running())
            print("start button clicked")
      
      def restart_button_clicked(self, acq_params : AcquisitionParameters):
            print("restart button clicked")
            acq_params.set_restart(True)
            print("self.acq_params", acq_params.get_restart())

      def stop_button_clicked(self, acq_params : AcquisitionParameters):
            print("stop button clicked")
            acq_params.set_acquisition_running(False)
            print("self.acq_params", acq_params.get_acquisition_running())

      def clear_button_clicked(self, acq_params : AcquisitionParameters):
            print("clear button clicked")
            acq_params.set_clear_plot(True)
            print("self.acq_params", acq_params.get_clear_plot())

      def populate_metrics_grid(self, acq_params : AcquisitionParameters):
            print("populate metrics grid")
            self.acquisition_status.setText(str(acq_params.get_acquisition_running()))
            self.start_time.setText(str(acq_params.get_start_time()))
            self.preset_time.setText(str(acq_params.get_t_acquisition()))
            self.n_channels.setText(str(acq_params.get_n_channels()))
            self.n_acquisitions.setText(str(acq_params.get_n_acquisitions()))
            self.current_acquisition.setText(str(acq_params.get_current_n() ))
            self.time_elapsed.setText(str(acq_params.get_current_acq_duration()))
            self.total_counts.setText(str(acq_params.get_total_counts()))
            cr= (acq_params.get_total_counts() / (acq_params.get_current_acq_duration()+0.00001))
            self.count_rate.setText(str(round(cr,2)))
            self.threshold.setText(str(acq_params.get_threshold()))

            
            
            
            
            
            



if __name__ == "__main__":
    app = QApplication(sys.argv)
    acq_params = AcquisitionParameters()
    window = MainWindow(acq_params)
    window.show()
    sys.exit(app.exec_())