import numpy as np
import pyqtgraph as pg
app = pg.mkQApp()
pw = pg.PlotWidget()
pw.show()
pi = pw.getPlotItem()
y = np.arange(1, 500, dtype=np.float64)
ai = pi.getAxis("bottom")
ai.setLogMode(True)
pdi = pi.plot(y)
pdi.setLogMode(True, False)
app.exec()