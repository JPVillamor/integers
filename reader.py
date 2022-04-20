import json
import requests
import websocket
import time
import os

ws = websocket.WebSocket()
ws.connect('ws://eodmat.herokuapp.com/ws/matserver/')

def read_sensor(filename):
    sensor_file = open(filename, 'r')
    val = sensor_file.readline()
    sensor_file.close()
    #ws.send(json.dumps({'type':'data','value':{'sensor':sensor,'value':val}}))
    return val

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
        time.sleep(.4)
        try:
            temp_dict['value'] = read_sensor('temp_output.txt')
            accx_dict['value'] = read_sensor('accx_output.txt')
            accy_dict['value'] = read_sensor('accy_output.txt')
            accz_dict['value'] = read_sensor('accz_output.txt')
            bottomForce_dict['value'] = read_sensor('bforce_output.txt')
            topForce_dict['value'] = read_sensor('tforce_output.txt')
            leftForce_dict['value'] = read_sensor('lforce_output.txt')
            rightForce_dict['value'] = read_sensor('rforce_output.txt')
            photoResistor_dict['value'] = read_sensor('photoResistor_output.txt')
            photoDiode_dict['value'] = read_sensor('photoDiode_output.txt')
            sound_dict['value'] = read_sensor('sound_output.txt')
            
            pir_file = open('PIR_output.txt', 'r')
            pir_val = pir_file.readline()
            pir_file.close()
            pir_dict['value'] = pir_val
            
            ws.send(json.dumps({'type':'data','value':payload_list}))
        except:
            pass
        
if __name__=='__main__':
    read_all()

