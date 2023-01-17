import matplotlib.pyplot as plt

def onclick(event):
    fig = plt.gcf()
    if hasattr(fig, 'line'):
        fig.line.remove()
    fig.line = plt.axvline(event.xdata, color='r')
    plt.show()

#fig, ax = plt.subplots()
#plt.plot(range(10))
#cid = fig.canvas.mpl_connect('button_press_event', onclick)
#plt.show()