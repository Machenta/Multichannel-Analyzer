import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

#create axis object
ax1 = plt.subplot2grid((1,1),(0,0))

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    ax1.hist(y, bins=5)
    plt.pause(0.05)


plt.show()


