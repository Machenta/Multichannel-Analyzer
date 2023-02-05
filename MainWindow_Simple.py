import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QTextEdit, QApplication
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import pyqtgraph as pg
from AcquisitionParams import *
from PlotterQT import *
from functools import partial

uiclass, baseclass = pg.Qt.loadUiType("untitled.ui")

class AppSignal(QObject):
    finished = pyqtSignal()

class TextEditSignal(QObject):
    textEntered = pyqtSignal(str)



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
            
            #create a timer that will update the plot every 100ms
            #self.timer = QTimer()
            #self.timer.timeout.connect(lambda: self.update_plot(acq_params))
            #self.timer.start(100)
            
            #enable the text edits boxes 
            self.entry_boxes= [self.lower_peak1, self.upper_peak1, 
                              self.lower_peak2, self.upper_peak2,
                              self.plot_min_entry, self.plot_max_entry,
                              self.channel_select_entry]

            self.user_entries = UserEntries()

            self.upper_peak1.textChanged.connect(self.text_changed_upper_peak1)
            #self.upper_peak1.returnPressed.connect(self.return_pressed)

            self.upper_peak2.textChanged.connect(self.text_changed_upper_peak2)
            #self.upper_peak2.returnPressed.connect(self.return_pressed)

            self.lower_peak1.textChanged.connect(self.text_changed_lower_peak1)
            #self.lower_peak1.returnPressed.connect(self.return_pressed)

            self.lower_peak2.textChanged.connect(self.text_changed_lower_peak2)
            #self.lower_peak2.returnPressed.connect(self.return_pressed)

            self.plot_min_entry.textChanged.connect(self.text_changed_plot_min)
            #self.plot_min_entry.returnPressed.connect(self.return_pressed)

            self.plot_max_entry.textChanged.connect(self.text_changed_plot_max)
            #self.plot_max_entry.returnPressed.connect(self.return_pressed)

            self.channel_select_entry.textChanged.connect(self.text_changed_channel_select)
            #self.channel_select_entry.returnPressed.connect(self.return_pressed)

            self.threshold_entry.textChanged.connect(self.text_changed_threshold)
            #self.threshold_entry.returnPressed.connect(self.return_pressed)



      def initPlot(self, AcquisitionParameters: AcquisitionParameters):
        #m = tests.Plotter(self.PlotdrawWidget, width=10, height=12)
        #m.move(0,0)
        #self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        #self.show()

            self.m = Plotter(acquisition_parameters =AcquisitionParameters, 
                        parent = self.PlotdrawWidget, 
                        width=10, 
                        height=10)  
            self.m.move(0,0)
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)
            self.layout = QtWidgets.QVBoxLayout()
            self.layout.addWidget(self.m)
            self.PlotdrawWidget.setLayout(self.layout)

      def text_changed_upper_peak1(self, text):
            #text = line_edit.text()
            try:
                  self.user_entries.upper_peak1 = int(text)
                  print(f"Text changed upper_peak1: {self.user_entries.upper_peak1}")
            except ValueError:
                  print("ValueError")
                  self.user_entries.upper_peak1 = 0
      
      def text_changed_upper_peak2(self, text):
            #text = line_edit.text()
            try:
                  self.user_entries.upper_peak2 = int(text)
                  print(f"Text changed: {text}")
            except ValueError:
                  print("ValueError")
                  self.user_entries.upper_peak2 = 0

      def text_changed_lower_peak1(self, text):
            #text = line_edit.text()
            try:
                  self.user_entries.lower_peak1 = int(text)
                  print(f"Text changed: {text}")
            except ValueError:
                  print("ValueError")
                  self.user_entries.lower_peak1 = 0

      def text_changed_lower_peak2(self, text):
            #text = line_edit.text()
            try:
                  self.user_entries.lower_peak2 = int(text)
                  print(f"Text changed: {text}")
            except ValueError:
                  print("ValueError")
                  self.user_entries.lower_peak2 = 0

      def text_changed_plot_min(self, text):
            #text = line_edit.text()
            try:
                  self.user_entries.plot_min = int(text)
                  print(f"Text changed: {text}")
            except ValueError:
                  print("ValueError")
                  self.user_entries.plot_min = 0

      def text_changed_plot_max(self, text):

            #text = line_edit.text()
            try:
                  self.user_entries.plot_max = int(text)
                  print(f"Text changed: {text}")
            except ValueError:
                  print("ValueError")
                  self.user_entries.plot_max = 0

      def text_changed_channel_select(self, text):
            #text = line_edit.text()
            try:
                  self.user_entries.channel_select = int(text)
                  print(f"Text changed: {text}")
            except ValueError:
                  print("ValueError")
                  self.user_entries.channel_select = 0

      def text_changed_threshold(self, text):
            #text = line_edit.text()
            try:
                  self.user_entries.threshold = int(text)
                  print(f"Text changed: {text}")
            except ValueError:
                  print("ValueError")
                  self.user_entries.threshold = 0


      def update_plot(self, acq_params : AcquisitionParameters):
            #updating the plot with the new data que is coming from the acquisition process
            self.m.redraw_plot(acquisition_parameters=acq_params , user_entries=self.user_entries)


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
            #print("populate metrics grid")

            if acq_params.get_acquisition_running():
                  self.acquisition_status.setText("Running")
            else:
                  self.acquisition_status.setText("Stopped")
            
            self.start_time.setText(str(acq_params.get_start_time()))
            self.preset_time.setText(str(acq_params.get_t_acquisition()))
            self.n_channels.setText(str(acq_params.get_n_channels()))
            self.n_acquisitions.setText(str(acq_params.get_n_acquisitions()))
            self.current_acquisition.setText(str(acq_params.get_current_n() ))
            self.time_elapsed.setText(str(acq_params.get_live_time()))
            self.total_counts.setText(str(acq_params.get_total_counts()))
            cr= (acq_params.get_total_counts() / (acq_params.get_live_time()+0.00001))
            self.count_rate.setText(str(round(cr,2)))
            #self.threshold_entry.setText(str(acq_params.get_threshold()))

            #print("cr", cr)
      

      def update_peak_counts(self, acq_params : AcquisitionParameters):
            #calculate the peak counts for the entire peak based on the user entries for the upper and lower limits

            #calculate the peak counts for the first peak
            #sum the counts in the first peak
            total_counts_peak1 = 0
            for i in range(self.user_entries.lower_peak1, self.user_entries.upper_peak1):
                  total_counts_peak1 += acq_params.get_current_acq_channel(i)

            #set the label for the first peak
            self.counts1.setText(str(total_counts_peak1))

            #calculate the peak counts for the second peak
            #sum the counts in the second peak
            total_counts_peak2 = 0
            for i in range(self.user_entries.lower_peak2, self.user_entries.upper_peak2):
                  total_counts_peak2 += acq_params.get_current_acq_channel(i)

            #set the label for the second peak
            self.counts2.setText(str(total_counts_peak2))
            

      def update_window(self, acq_params : AcquisitionParameters):
            #update the window with the new data
            self.update_plot(acq_params)
            self.populate_metrics_grid(acq_params)
            self.update_peak_counts(acq_params)     
            



if __name__ == "__main__":
    app = QApplication(sys.argv)
    acq_params = AcquisitionParameters()
    window = MainWindow(acq_params)
    window.show()
    sys.exit(app.exec_())