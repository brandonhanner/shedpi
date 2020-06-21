import time

from gpiozero import LED

import board
import busio

import adafruit_ads1x15.ads1115 as ADS

from adafruit_ads1x15.analog_in import AnalogIn

class ADC(object):
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.gain = 1
        self.chan = AnalogIn(self.ads, ADS.P0)

        self.s0 = LED(19)
        self.s1 = LED(13)
        self.s2 = LED(6)
        self.s3 = LED(5)

        self.mux_en = LED(26)

        self.mux_en.off()

        self.bcdPins = [self.s0,self.s1,self.s2,self.s3]

        #S3 -> GPIO5
        #S2 -> GPIO6
        #S1 -> GPIO13
        #S0 -> GPIO19 lsb
        #EN -> GPIO26

        #CELL4 -> C15
        #CELL3 -> C14
        #CELL2 -> C13
        #CELL1 -> C12

        #CURRENT1 -> C1
        #CURRENT2 -> C0

        #UART -> UART

        #ADS -> I2C
    def capture_readings(self):
        for i in [0,1,12,13,14,15]:
            volts = self.read_channel(i)
            print("Channel: {} Voltage: {}".format(i,volts))
            
    def read_channel(self, channel):
        self.set_channel(channel)
        time.sleep(.05)
        return self.chan.voltage


    def set_channel(self, channel):
        for j in range(0,4):
                digit = (channel & (1 << j)) >> j
                # print("{} element: {}".format(j,digit))
                if digit == 1:
                    self.bcdPins[j].on()
                else:
                    self.bcdPins[j].off()
