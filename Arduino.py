import serial
import time
import serial.tools.list_ports


#create serial object - Arduino
class Arduino:
    def __init__(self, port : str = "COM3", 
                    baud : int = 1000000,
                    channels : int = 10):
                    
        self.port = port
        self.baud = baud
        self.channels = channels
        self.ports = list(serial.tools.list_ports.comports())
        self.error_n : int = 0
        #auto detect the port
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
        #check if the serial connection exists
        if self.ser != None:
            self.ser.close()
            print("Closed connection to Arduino port: " + self.port + " at " + str(self.baud) + " baud.")
        else:
            print("No connection found to close.")    

    def read_serial(self):
        if self.ser.in_waiting > 0:
            try:
                val = int(self.ser.readline().decode("utf-8").strip())
            except ValueError:
                print("Error decoding serial data.")
                val = 0 
                self.error_n += 1
        else:
            try:
                val = int(self.ser.readline().decode("utf-8").strip())
            except ValueError:
                print("Error decoding serial data.")
                val = 0
                self.error_n += 1
        return val, self.error_n
        
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
        return True


    def prepare_acquisition(self):
    # assess possible errors
        try:
            self.open_connection()
        except:
            print("Error opening connection to Arduino.")
            return False
        print("Successfully opened connection to Arduino.")

        # flush the serial buffer
        try: 
            # only flush if there is something in the buffer
            if self.ser and self.ser.is_open and hasattr(self.ser, 'fileno'):
                if self.ser.in_waiting > 0:
                    self.ser.flush()
                else:
                    pass
            else:
                print("Serial connection not initialized or closed or has no file descriptor.")

        except:
            print("Error flushing serial buffer.")
            return False
        return True

    def prep_connection(self):
        #open the serial connection
        try:
            self.open_connection()
        except:
            print("Error opening connection to Arduino.")
            return False


    def close_device(self):
        self.close_connection()
        return True


if __name__ == "__main__":
    dev = Arduino()
    dev.prepare_acquisition()
    #b= dev.get_arduino_baud_rate()
    #print("Arduino baud rate: " + str(b) + " baud.")
    for i in range(100):
        dev.read_serial()
        i+=1
        print(1)
    
    #dev.prepare_other_acquisition()
    time.sleep(1)
    for i in range(100):
        #print("Serial buffer1 : " + str(dev.ser.in_waiting))
        a=dev.read_serial()
        print("a: " + str(a))
        i+=1
        print(2)


