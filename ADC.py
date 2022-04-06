import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1015(i2c)

resistor_chan = AnalogIn(ads, ADS.P0)
diode_chan = AnalogIn(ads, ADS.P1)
sound_chan = AnalogIn(ads, ADS.P2)

# P0 resistor
# P1 diode
# P2 sound

'''
print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(.05)
'''