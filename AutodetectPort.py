import serial.tools.list_ports
import Arduino

ports = list(serial.tools.list_ports.comports())
for port in ports:
    if "VID:PID" in port[2]:
        arduino_port = port[0]
        break

print("Arduino port is: " + arduino_port)

dev=Arduino.Arduino(n_acquisitions=1, acquisition_time=5)