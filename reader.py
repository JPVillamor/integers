import json
import requests
import websocket
import time
import os
import forcemux
import counter
import PIR
import ADC

ws = websocket.WebSocket()
ws.connect('ws://eodmat.herokuapp.com/ws/matserver/')

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
            accx_dict['value'] = counter.get_acc('x')
            accy_dict['value'] = counter.get_acc('y')
            accz_dict['value'] = counter.get_acc('z')
            with forcemux.force2:
                forcemux.function(forcemux.force2, 2)
            bottomForce_dict['value'] = round(forcemux.force_out2, 2)
            with forcemux.force3:
                forcemux.function(forcemux.force3, 3)
            topForce_dict['value'] = round(forcemux.force_out3, 2)
            with forcemux.force1:
                forcemux.function(forcemux.force1, 1)
            leftForce_dict['value'] = round(forcemux.force_out1, 2)
            with forcemux.force4:
                forcemux.function(forcemux.force4, 4)
            rightForce_dict['value'] = round(forcemux.force_out4, 2)
            
            photoResistor_dict['value'] = round(ADC.resistor_chan.voltage, 3)
            photoDiode_dict['value'] = round(ADC.diode_chan.voltage, 3)
            sound_dict['value'] = round(ADC.sound_chan.voltage, 3)
            
            pir_dict['value'] = PIR.get_reading()
            time.sleep(.2)
        except:
            continue
            
        try:
            ws.send(json.dumps({'type':'data','value':payload_list}))
            time.sleep(.2)
        except:
            ws.connect('ws://eodmat.herokuapp.com/ws/matserver/')
            ws.send(json.dumps({'type':'data','value':payload_list}))
        
if __name__=='__main__':
    read_all()

