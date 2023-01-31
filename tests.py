import time
import multiprocessing
import serial
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import Arduino
import tkinter as tk
import AcquisitionSetupWindow as acq
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataclasses import dataclass, field

import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow

def change_text():
    button.setText("Button text changed!")

app = QApplication(sys.argv)
window = QMainWindow()
button = QPushButton("Click me!", window)
button.clicked.connect(change_text)
button.show()
sys.exit(app.exec_())


