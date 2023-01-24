import matplotlib.pyplot as plt
import matplotlib
import UI #import the UI module to be able to access the UI_window class
import numpy as np
import matplotlib




class Plot:
    def __init__(self, 
                    x, 
                    y, 
                    title : str  = "Data Acquisition", 
                    xlabel : str = "Channel", 
                    ylabel : str = "Counts", 
                    settings : dict = None,
                    grid : bool = True):
        self.x = x
        self.y = y
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.lines = []

        #generate the figure and axes
        self.fig, self.ax = plt.subplots()

        #draw a tentative plot:
        self.line1,= self.ax.plot(self.x, self.y, 'r-')
        self.line2 = self.ax.scatter(x, y, c='b', marker='o', s=10, alpha=0.5)

        #set tentative y_lim
        self.ax.set_ylim(0, 5)

        if grid:
            self.ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.5)

    #update the plot
    def update_plot(self,
                    settings : dict, 
                    shared_dict : dict,
                    clear_plot : bool = False,
                    win : UI.UI_Window = None,
                    cid = None
                    ):
                    
        #update y_data taking into account the threshold and replace the erased values by zeros 
        #while taking into account the clear plot flag 
        if settings["clear_plot"] == True:
            for key in range(settings["n_channels"]):
                shared_dict[key] = 0
            self.y_temp = [shared_dict[i] if i >= settings["threshold"] else 0 for i in range(settings["n_channels"])]
            settings["clear_plot"] = False
        else:
            self.y_temp= [shared_dict[i] if i >= settings["threshold"] else 0 for i in range(settings["n_channels"])]

        win.acquisition_settings.clear_flag = False
        self.line1.set_ydata(self.y_temp)
        self.line1.set_xdata(self.x)
        self.line2.set_offsets(np.c_[self.x,self.y_temp])
        self.ax.set_ylim(0, 1.1*max(shared_dict.values())+ 5)
        self.ax.set_yscale(settings["plot_scale"])   
        if settings["threshold"] != 0: 
            line = self.ax.axvline(x=settings["threshold"], color='blue', linestyle='--', linewidth=0.5)
            self.lines.append(line)
        for line in self.lines[:-1]:
            line.remove()
            self.lines.remove(line)    
        if cid is not None:
            self.fig.canvas.mpl_disconnect(cid)
        cid = self.fig.canvas.mpl_connect('button_press_event', onclick)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        return self.y_temp


if __name__ == "__main__":
    a,=np.linspace(1, 10, 12).shape
    b= np.zeros(12)
    print("x_shape", str(a))
    print("x_shape", np.linspace(1, 10, 12))
    print("y_shape", str(b.shape))
    print("y_shape", b)
    x = np.arange(0, 100, 1)
    y = np.random.randint(0, 100, size=100)
    plot = Plot(np.linspace(1, 10, 10), np.zeros(10))
    plt.show()