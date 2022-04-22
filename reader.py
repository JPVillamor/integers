import json
import requests
import websocket
import time
import forcemux
import counter
import PIR
import ADC
import board
import neopixel
import rel
import _thread
import threading

#websocket.enableTrace(True)
ws = websocket.WebSocketApp('ws://eodmat.herokuapp.com/ws/matserver/')
#ws.connect('wss://eodmat.herokuapp.com/ws/matserver/')
ws.run_forever(skip_utf8_validation=True, dispatcher=rel)
rel.abort()
rel.dispatch()

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

thresholds = {'temp': 27, 'accx': 1, 'accy': 1, 'accz': 11.5, 'force': 16, 'photoR': 3, 'photoD': .5, 'sound': 1.5, 'pir': 1}

def fast_sensor_poll():
    while True:
        try:
            if counter.get_temp() >= thresholds['temp']:
                pixels[0] = RED
            else:
                pixels[0] = OFF
                
            if abs(counter.get_acc('x')) >= thresholds['accx']:
                pixels[1] = RED
            else:
                pixels[1] = OFF
            
            if abs(counter.get_acc('y')) >= thresholds['accy']:
                pixels[2] = RED
            else:
                pixels[2] = OFF
            
            if abs(counter.get_acc('z')) >= thresholds['accz']:
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

def read_all():
    temp_dict = {'sensor':'temp','value':0}
    accx_dict = {'sensor':'accx','value':0}
    accy_dict = {'sensor':'accy','value':0}
    accz_dict = {'sensor':'accz','value':0}
    bottomForce_dict = {'sensor':'bottomForce','value':0}
    topForce_dict = {'sensor':'topForce','value':0}
    leftForce_dict = {'sensor':'leftForce','value':0}
    rightForce_dict = {'sensor':'rightForce','value':0}
    photoResistor_dict = {'sensor':'photoResistor','value':0}
    photoDiode_dict = {'sensor':'photoDiode','value':0}
    sound_dict = {'sensor':'sound','value':0}
    pir_dict = {'sensor':'pir','value':0}
    
    payload_list = [
        temp_dict, accx_dict, accy_dict, accz_dict,
        topForce_dict, leftForce_dict, rightForce_dict, bottomForce_dict,
        photoResistor_dict, photoDiode_dict, sound_dict, pir_dict
        ]
    while True:
        try:
            temp_dict['value'] = counter.get_temp()
        except:
            continue
        
        try:
            accx_dict['value'] = counter.get_acc('x')
        except:
            continue
        
        try:
            accy_dict['value'] = counter.get_acc('y')
        except:
            continue
        
        try:
            accz_dict['value'] = counter.get_acc('z')
        except:
            continue
        
        try:
            with forcemux.force2:
                forcemux.function(forcemux.force2, 2)
            bottomForce_dict['value'] = round(forcemux.force_out2, 2)
        except:
            continue
        
        try:
            with forcemux.force3:
                forcemux.function(forcemux.force3, 3)
            topForce_dict['value'] = round(forcemux.force_out3, 2)
        except:
            continue
        
        try:
            with forcemux.force1:
                forcemux.function(forcemux.force1, 1)
            leftForce_dict['value'] = round(forcemux.force_out1, 2)
        except:
            continue
        
        try:
            with forcemux.force4:
                forcemux.function(forcemux.force4, 4)
            rightForce_dict['value'] = round(forcemux.force_out4, 2)
        except:
            continue
        
        try:
            photoResistor_dict['value'] = round(ADC.resistor_chan.voltage, 3)
        except:
            continue
        
        try:
            photoDiode_dict['value'] = round(ADC.diode_chan.voltage, 3)
        except:
            continue
        
        try:
            sound_dict['value'] = round(ADC.sound_chan.voltage, 3)
        except:
            continue
        
        try:
            pir_dict['value'] = PIR.get_reading()
        except:
            continue
        
        time.sleep(.2)
            
        try:
            ws.send(json.dumps({'type':'data','value':payload_list}))
            time.sleep(.2)
        except:
            ws = websocket.WebSocketApp('ws://eodmat.herokuapp.com/ws/matserver/')
            #ws.connect('wss://eodmat.herokuapp.com/ws/matserver/')
            ws.run_forever(skip_utf8_validation=True, dispatcher=rel)
            rel.abort()
            rel.dispatch()
            #print('sending error')
            #time.sleep(.5)
            #ws.connect('ws://eodmat.herokuapp.com/ws/matserver/')
            #ws.send(json.dumps({'type':'data','value':payload_list}))
            continue
        
sender_thread = threading.Thread(target=read_all)
led_thread = threading.Thread(target=fast_sensor_poll)

if __name__=='__main__':
    sender_thread.start()
    led_thread.start()

