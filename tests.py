import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 50
        self.top = 50
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 700
        self.height = 500
        

        self.initUI()

    def initUI(self):
        m = Plotter(self, width=5, height=4)
        m.move(0,0)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

class Plotter(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots()

        self.x = np.arange(0, 100, 1)
        self.y = np.arange(0, 100, 1)
        self.ax.set_xlim(0, max(self.x))
        self.ax.set_ylim(0, max(self.y)+5)

        self.ax.set_xlabel("Channel")
        self.ax.set_ylabel("Counts")

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                    QSizePolicy.Expanding,
                                    QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        import random
        #data = [random.random() for i in range(25)]
        #ax = self.figure.add_subplot(111)
        #ax.plot(data, 'r-')
        #ax.set_title('PyQt Matplotlib Example')
        self.draw()

        self.x = np.arange(0, 100, 1)
        self.y = np.arange(0, 100, 1)
        self.ax.set_xlim(0, max(self.x))
        self.ax.set_ylim(0, max(self.y)+5)

        self.ax.set_xlabel("Channel")
        self.ax.set_ylabel("Counts")

        self.ax.plot(self.x, self.y, 'r-')
        self.ax.set_title('Spectrum')
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())




