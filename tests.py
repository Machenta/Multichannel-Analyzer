import pyqtgraph as pg

x = [i for i in range(100)]
y = [i**2 for i in x]

# Create the plot
plot = pg.plot(x, y)

# Create the linear region item
region = pg.LinearRegionItem(values=[20, 40])
region.setZValue(-10)

# Add the region to the plot
plot.addItem(region)

# Show the plot
plot.show()
#dont close the window
app = pg.mkQApp()
app.exec()