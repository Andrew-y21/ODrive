import serial

class SerialComms:
    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyACM0',9600, timeout=0.5) # init serial
            self.ser.reset_input_buffer()

        except serial.SerialException as e:
            print(f"Serial port error: {e}")



    def runComms(self, inputVal):
        thingToSend = inputVal
        
        self.ser.write((thingToSend + "\n").encode)



    def reciveComms(self):
        while True:
            response = self.ser.readline().decode().strip()
            print(response)

            return response





