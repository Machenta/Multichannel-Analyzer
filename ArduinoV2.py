import serial
import time
import serial.tools.list_ports
import random


#create serial object - Arduino
class Arduino:
    def __init__(self, port : str = "COM3", 
                    baud : int = 250000,
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

    def get_arduino_baud_rate():
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description  # adjust this to match your board
        ]
        if not arduino_ports:
            raise ValueError("No Arduino found")
        # assume the first Arduino is the one we want to use
        arduino_port = arduino_ports[0]
        ser = serial.Serial(arduino_port)
        ser.baudrate = 9600  # set a low baud rate to ensure command is received
        ser.timeout = 1  # set a timeout in case command is not received
        ser.write(b'AT+UART_CUR?\r\n')  # send the command to retrieve baud rate
        response = ser.readline().decode().strip()
        ser.close()
        if not response.startswith('+UART_CUR:'):
            raise ValueError("Unexpected response from Arduino: %s" % response)
        baud_rate = int(response.split(':')[1])
        return baud_rate

    def open_connection(self):
        if self.ser == None:
            self.ser = serial.Serial(self.port, self.baud)
        else:
            print("Connection already open.")
        print("Connected to Arduino port: " + self.port + " at " + str(self.baud) + " baud.")

    def close_connection(self):
        #check if the serial connection exists
        if self.ser != None:
            self.ser.close()
            print("Closed connection to Arduino port: " + self.port + " at " + str(self.baud) + " baud.")
        #if self.ser.is_open() == True:
        #    self.ser.close()
        #    print("Closed connection to Arduino port: " + self.port + " at " + str(self.baud) + " baud.")
        else:
            print("No connection found to close.")    

    def read_serial(self):
        if self.ser.in_waiting > 0:
            val = int(self.ser.readline().decode("utf-8").strip())
        else:
            val = 0
        #get only the last number in the string
        #val = random.randint(0, self.channels-1)
        return val
        
    def prepare_other_acquisition(self):
        try: 
            self.ser.reset_input_buffer()
        except:
            print("Error resetting input buffer.")
            return False
        
        try:
            self.ser.reset_output_buffer()
        except:
            print("Error resetting output buffer.")
            return False
        

        #print the serial buffer
        #print("Serial buffer: " + str(self.ser.in_waiting))
        return True


    def prepare_acquisition(self):
        #assess possible errors
        try:
            self.open_connection()
        except:
            print("Error opening connection to Arduino.")
            return False
        

        print("Serial buffer: " + str(self.ser))

        #flush the serial buffer
        #try: 
        #    #only flush if there is something in the buffer
        #    if self.ser.in_waiting > 0:
        #        self.ser.flush()
        #    else:
        #        print("Nothing to flush.")
        #except:
        #    print("Error flushing serial buffer.")
        #    return False
        
        try: 
            self.ser.reset_input_buffer()
        except:
            print("Error resetting input buffer.")
            return False
        
        try:
            self.ser.reset_output_buffer()
        except:
            print("Error resetting output buffer.")
            return False
        

        #print the serial buffer
        #print("Serial buffer: " + str(self.ser.in_waiting))
        return True

    def close_device(self):
        self.close_connection()
        return True


if __name__ == "__main__":
    dev = Arduino()
    dev.prepare_acquisition()
    for i in range(100):
        dev.read_serial()
        i+=1
        print(1)
    #dev.close_device()
    dev.prepare_other_acquisition()
    time.sleep(2)
    for i in range(100):
        print("Serial buffer1 : " + str(dev.ser.in_waiting))
        a=dev.read_serial()
        print("a: " + str(a))
        i+=1
        print(2)


