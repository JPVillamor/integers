import forcemux
import counter
import PIR
import ADC
import board
import neopixel
import time

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

OFF = (0,0,0)
RED = (255,0,0)

thresholds = {'temp': 23, 'acc': 11, 'force': 3, 'photoR': 3, 'photoD': 1, 'sound': .7, 'pir': 1}

def fast_sensor_poll():
    while True:
        try:
            if counter.get_temp() >= thresholds['temp']:
                pixels[0] = RED
            else:
                pixels[0] = OFF
                
            if counter.get_acc('x') >= thresholds['acc']:
                pixels[1] = RED
            else:
                pixels[1] = OFF
            
            if counter.get_acc('y') >= thresholds['acc']:
                pixels[2] = RED
            else:
                pixels[2] = OFF
            
            if counter.get_acc('z') >= thresholds['acc']:
                pixels[3] = RED
            else:
                pixels[3] = OFF
            
            with forcemux.force2:
                forcemux.function(forcemux.force2, 2)
            bottomForceVal = round(forcemux.force_out2, 2)
                
            with forcemux.force3:
                forcemux.function(forcemux.force3, 3)
            topForceVal = round(forcemux.force_out3, 2)
                            
            with forcemux.force1:
                forcemux.function(forcemux.force1, 1)
            leftForceVal = round(forcemux.force_out1, 2)
                            
            with forcemux.force4:
                forcemux.function(forcemux.force4, 4)
            rightForceVal = round(forcemux.force_out4, 2)
            
            if max(bottomForceVal, topForceVal, leftForceVal, rightForceVal) >= thresholds['force']:
                pixels[4] = RED
            else:
                pixels[4] = OFF
                
            if round(ADC.resistor_chan.voltage, 3) >= thresholds['photoR']:
                pixels[5] = RED
            else:
                pixels[5] = OFF
            if round(ADC.diode_chan.voltage, 3) >= thresholds['photoD']:
                pixels[6] = RED
            else:
                pixels[6] = OFF
            
            if round(ADC.sound_chan.voltage, 3) >= thresholds['sound']:
                pixels[7] = RED
            else:
                pixels[7] = OFF
            
            if PIR.get_reading() >= thresholds['pir']:
                pixels[8] = RED
            else:
                pixels[8] = OFF
                
            pixels.show()
            time.sleep(.02)
        except:
            #print('error')
            continue

if __name__=='__main__':
    fast_sensor_poll()