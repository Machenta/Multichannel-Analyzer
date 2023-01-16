import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
import tkinter as tk
import AcquisitionSetupWindow as acq




if __name__ == "__main__":
    #root = tk.Tk()
    #setup_window = acq.AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
#
    #a,b = setup_window.return_params()
##
    #print("Number of acquisitions:", str(a))
    #print("Acquisition time:", str(b))

    mydict = {1:2, 2:3, "stop":4}
    mydict.update({"stop":"ad"})
    print(mydict)

    print(mydict["stop"].value)
    