#from future import printfunction
#from _future import division
import smbus
import os
from time import sleep
import logging

i2c = smbus.SMBus(1)

MCP3021_I2CADDR = 0x4b  # default address

class MCP3021(object):

    def init(self):
        try:
            dummy = i2c.read_word_data(MCP3021_I2CADDR, 0)
        except:
            print('Could not connect to MCP3021 | I2C init')

    def get_voltage(self):
        try:

                # read data from i2c bus. the 0 command is mandatory for the protocol but not used in this chip.
            voltage = 0
            average_count = 1
            for x in range(0, average_count):
                data = i2c.read_word_data(MCP3021_I2CADDR, 0)

                    # from this data we need the last 4 bits and the first 6.

                last_4 = data & 0b1111  # using a bit mask
                first_6 = data >> 10  # left shift 10 because data is 16 bits

                    # together they make the voltage conversion ratio
                    # to make it all easier the last_4 bits are most significant :S

                vratio  = last_4 << 6 | first_6
                print(vratio)

                    # Now we can calculate the battery voltage like so:

                ratio = float(os.environ.get('MCP3021_RATIO', '0.0217')) # calibration value based on measurements
                voltage = vratio * 3.3/1023.0 # voltage + vratio * ratio
                print(voltage)
            return '{:.3F}'.format(voltage/average_count)
        except:

            print("Couldn't connect to MCP3021")
            return 0
