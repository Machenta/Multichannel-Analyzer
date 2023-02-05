import numpy as np
import pyqtgraph as pg

x = np.linspace(0, 400, 400)
y = np.sin(x/20)
c1 = pg.PlotCurveItem(x=x, y=y)
plot = pg.plot()
plot.addItem(c1)

fill_x = [100,100,300,300]
fill_y = [0, y[100], y[300], 0]
fill = pg.FillBetweenItem(c1, fill_x, fill_y)
plot.addItem(fill)