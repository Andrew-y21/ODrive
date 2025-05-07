import serial

class SerialComms:
    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.5)
            self.ser.reset_input_buffer()
        except serial.SerialException as e:
            print(f"Serial port error: {e}")
            self.ser = None

    def sendComms(self, inputVal):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write((inputVal + "\n").encode())
            except serial.SerialException as e:
                print(f"Error writing to serial: {e}")

    def receiveComms(self):
        if self.ser and self.ser.is_open:
            try:
                response = self.ser.readline().decode().strip()
                if response:
                    print(f"Received: {response}")
                return response
            except serial.SerialException as e:
                print(f"Error reading from serial: {e}")
                return None
