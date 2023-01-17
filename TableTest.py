import matplotlib.pyplot as plt
from matplotlib.table import Table
import random

# Create a figure and axis
fig, ax = plt.subplots(1,1)
ax.axis("off")

# Create a table with initial values
data = [[random.randint(0, 10) for j in range(1)] for i in range(6)]
print("data: ", data)
table = ax.table(cellText=data, loc="center")
ax.add_table(table)

def update(num):
    data = [[random.randint(0, 10) for j in range(1)] for i in range(6)]
    for i in range(4):
        for j in range(4):
            table.get_celld()[(i,j)].get_text().set_text(str(data[i][j]))
    return table,

# Create the animation object
#ani = plt.FuncAnimation(fig, update, frames=range(10), blit=True)

plt.show()
