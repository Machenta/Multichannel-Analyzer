import serial
import time
import serial.tools.list_ports
import random


#create serial object - Arduino
class Arduino:
    def __init__(self, port : str = "COM3", 
                    baud : int = 9600,
                    channels : int = 10):
                    
        self.port = port
        self.baud = baud
        self.channels = channels
        self.ports = list(serial.tools.list_ports.comports())
        for port in self.ports:
            if "VID:PID" in port[2]:
                self.port = port[0]
                
                print("Detected arduino at port: " + self.port)
                break
        self.ser = None

    def open_connection(self):
        if self.ser == None:
            self.ser = serial.Serial(self.port, self.baud)
        else:
            print("Connection already open.")
        print("Connected to Arduino port: " + self.port + " at " + str(self.baud) + " baud.")

    def close_connection(self):
        if self.ser.is_open() == True:
            self.ser.close()
            print("Closed connection to Arduino port: " + self.port + " at " + str(self.baud) + " baud.")
        else:
            print("No connection found to close.")    

    def read_serial(self):
        #if self.ser.in_waiting > 0:
        #    val = int(self.ser.readline().decode("utf-8").strip())
        #else:
        #    val = 0
        #get only the last number in the string
        val = random.randint(0, self.channels-1)
        return val
        
 
    
    def prepare_acquisition(self):
        
        self.open_connection()
        self.ser.flush()
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        return True

    def close_device(self):
        self.close_connection()
        return True


if __name__ == "__main__":
    dev = Arduino()
    dev.prepare_acquisition()
    while True:
        dev.read_serial()
    dev.close_device()



