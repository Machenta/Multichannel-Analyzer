import time
import threading

x = [0]

def update_var(var):
    while True:
        var[0] += 1
        time.sleep(2.0)

threading.Thread(target=update_var, args=(x,)).start()


print (x[0])