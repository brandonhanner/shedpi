import renogy 
import time
import threading
import serial

from w1thermsensor import W1ThermSensor


class Solar(object):
    def __init__(self, port):
        self.serw = serial.Serial()

        self.serw.port = port
        self.serw.baudrate = 9600
        self.serw.bytesize = serial.EIGHTBITS
        self.serw.parity = serial.PARITY_NONE
        self.serw.stopbits = serial.STOPBITS_ONE
        self.serw.write_timeout = 1

        self.controller = renogy.RenogyRover(port, 1,self.serw)

        self.battery_voltage = 0
        self.solar_voltage = 0
        self.solar_current = 0
        self.solar_power = 0
        self.charger_temperature = 0
        self.charging_status = 'none'
        self.charging_current = 0

        self.thread = threading.Thread(target=self.run,daemon=True)
        self.thread.start()

    def update_readings(self):
        self.battery_voltage = self.controller.battery_voltage()
        self.solar_voltage = self.controller.solar_voltage()
        self.solar_current = self.controller.solar_current()
        self.solar_power = self.controller.solar_power()
        self.charger_temperature = self.controller.controller_temperature()
        self.charging_status = self.controller.charging_status_label()
        self.charging_current = self.controller.charging_current()

        #print(self.battery_voltage,self.solar_voltage,self.solar_power,self.solar_current,self.charging_current,self.charging_status,self.charger_temperature)

    def run(self):
        while True:
            self.update_readings()
            time.sleep(1)