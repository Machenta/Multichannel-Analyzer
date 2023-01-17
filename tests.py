import matplotlib.pyplot as plt

def onclick(event):
    plt.axvline(event.xdata)
    plt.show()

fig, ax = plt.subplots()
plt.plot(range(10))
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()


