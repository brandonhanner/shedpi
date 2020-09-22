# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
from azure.iot.device.aio import IoTHubModuleClient

import BlynkLib as blynk

import Adafruit_DHT

import adc
import bms
import solar

class Shed(object):
    def __init__(self):
        self.adc = adc.ADC()
        self.battery = bms.battery(self.adc)
        self.solar = solar.Solar('/dev/ttyS0')

        f = open("blynk_auth.txt", "r")

        self.BLYNK_AUTH = f.readline()

        self.blynk = blynk.Blynk(self.BLYNK_AUTH)

        self.battery_v_adc_pin = 0     #battery voltage
        self.battery_i_pin = 1     #battery current
        self.cell_1_pin = 2        #cell 1 voltage
        self.cell_2_pin = 3        #cell 2 voltage
        self.cell_3_pin = 4        #cell 3 voltage
        self.cell_4_pin = 5        #cell 4 voltage
        self.solar_v_pin = 6       #solar voltage
        self.solar_w_pin = 7       #solar wattage
        self.battery_t_pin = 8     #battery temperature
        self.charging_w_pin = 9    #battery charging current
        self.load_i_pin = 10       #load current
        self.charging_indicator_pin = 11
        self.battery_v_solar_pin = 12


    def update_blynk(self):
        self.blynk.virtual_write(self.battery_v_adc_pin, self.battery.voltage)
        self.blynk.virtual_write(self.battery_i_pin, (self.solar.charging_current - self.battery.load_current))
        self.blynk.virtual_write(self.cell_1_pin, self.battery.cell_voltages[0])
        self.blynk.virtual_write(self.cell_2_pin, self.battery.cell_voltages[1])
        self.blynk.virtual_write(self.cell_3_pin, self.battery.cell_voltages[2])
        self.blynk.virtual_write(self.cell_4_pin, self.battery.cell_voltages[3])
        self.blynk.virtual_write(self.solar_v_pin, self.solar.solar_voltage)
        self.blynk.virtual_write(self.solar_w_pin, self.solar.solar_power)
        self.blynk.virtual_write(self.battery_t_pin, self.battery.temperature)
        self.blynk.virtual_write(self.charging_w_pin, (self.solar.charging_current - self.battery.load_current) * (self.solar.battery_voltage-0.5))
        self.blynk.virtual_write(self.load_i_pin, self.battery.load_current)
        self.blynk.virtual_write(self.battery_v_solar_pin,self.solar.battery_voltage)

        if self.solar.charging_status == "deactivated":
            self.blynk.virtual_write(self.charging_indicator_pin,0)
        else:
            self.blynk.virtual_write(self.charging_indicator_pin,255)


shed = Shed()

while True:

    shed.update_blynk()
    shed.blynk.run()

    #print("{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}".format(shed.battery.cell_voltages[0],shed.battery.cell_voltages[1],shed.battery.cell_voltages[2],shed.battery.cell_voltages[3],shed.battery.voltage))
    
    time.sleep(1)