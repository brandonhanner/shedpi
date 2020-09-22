import threading
import time

class battery(object):
    def __init__(self,adc):
        self.adc=adc
        self.cell_voltages = [0,0,0,0]
        self.voltage = 0
        self.load_current = 0
        #set up the divider constants
        self.cell_1_resistors = 2400/(2400+750)
        self.cell_2_resistors = 2400/(2400+3900)
        self.cell_3_resistors = 1500/(1500+4775)
        self.cell_4_resistors = 1200/(1200+5100)
        self.resistor_constants = [self.cell_1_resistors,self.cell_2_resistors,self.cell_3_resistors,self.cell_4_resistors]
        #set up the mapping from cell [i] to adc channel
        self.cell_adc_map = [12,13,14,15]
        self.adc_current_channel = 1
        self.adc_current_zero_offset = 0.02
        self.adc_tare_voltage = 3.3/2
        
        self.temperature = 0

        self.load_current_list = [0,0,0,0,0,0,0,0,0,0]

        thread = threading.Thread(target=self.run,daemon=True)
        thread.start()

    def update_cells(self):
        prev_channel = 0
        for i,channel in enumerate(self.cell_adc_map):
            raw_v = self.adc.read_channel(channel)
            corrected_v = raw_v/self.resistor_constants[i]
            if i == 0:
                self.cell_voltages[i] = corrected_v
            elif i>0:
                self.cell_voltages[i] = corrected_v - prev_channel
            prev_channel = corrected_v
        
        voltage = 0
        for volts in self.cell_voltages:
            voltage += volts
        self.voltage = voltage
    
    def update_load_current(self):
        #1.670 0 current voltage 3.3/2 = 1.65v
        raw = self.adc.read_channel(1)
        corrected = raw - self.adc_current_zero_offset

        diff = corrected - self.adc_tare_voltage

        amps = diff / .040

        self.load_current_list.pop(0)
        self.load_current_list.append(amps)

        self.load_current = sum(self.load_current_list)/10

        #print (self.load_current)

    def run(self):
        while True:
            self.update_cells()
            self.update_load_current()
            time.sleep(0.1)


