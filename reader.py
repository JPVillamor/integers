import json
import requests
import websocket
import time
import os

#from models import Record

ws = websocket.WebSocket()

#ws.connect('ws://127.0.0.1:8000/ws/some_url/')
#ws.connect('ws://localhost:8000/ws/some_url/')
ws.connect('ws://eodmat.herokuapp.com/ws/matserver/')

prev_temp = float(0)
prev_accx = float(0)
prev_accy = float(0)
prev_accz = float(0)
prev_bottomForce = float(0)
prev_topForce = float(0)
prev_leftForce = float(0)
prev_rightForce = float(0)
prev_photoResistor = float(0)
prev_photoDiode = float(0)
prev_sound = float(0)

def read_and_send(sensor, filename, previous):
    #val = float(0)
    sensor_file = open(filename, 'r')
    val = sensor_file.readline()
    sensor_file.close()
    ws.send(json.dumps({'type':'data','value':{'sensor':sensor,'value':val}}))
    #else:
        #val = previous
        #ws.send(json.dumps({'type':'data','value':{'sensor':'temp','value':val}}))

def read_all():
    global prev_temp
    global prev_accx
    global prev_accy
    global prev_accz
    global prev_bottomForce
    global prev_topForce
    global prev_leftForce
    global prev_rightForce
    global prev_photoResistor
    global prev_photoDiode
    global prev_sound
    
    counter = 0
    while True:
        time.sleep(.5)
        counter = counter + 500
        
        
        read_and_send('temp', 'temp_output.txt', prev_temp)
        read_and_send('accx', 'accx_output.txt', prev_accx)
        read_and_send('accy', 'accy_output.txt', prev_accy)
        read_and_send('accz', 'accz_output.txt', prev_accz)
        read_and_send('bottomForce', 'bforce_output.txt', prev_bottomForce)
        read_and_send('topForce', 'tforce_output.txt', prev_topForce)
        read_and_send('leftForce', 'lforce_output.txt', prev_leftForce)
        read_and_send('rightForce', 'rforce_output.txt', prev_rightForce)
        read_and_send('photoResistor', 'photoResistor_output.txt', prev_photoResistor)
        read_and_send('photoDiode', 'photoDiode_output.txt', prev_photoDiode)
        read_and_send('sound', 'sound_output.txt', prev_sound)
        
        pir_file = open('PIR_output.txt', 'r')
        pir_val = pir_file.readline()
        pir_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'pir','value':pir_val}}))
        '''
        
        
        if os.stat('temp_output.txt').st_size != 0
            temperature_file = open('temp_output.txt', 'r')
            temp_val = temperature_file.readline()
            temperature_file.close()
            global prev_temp = temp_val
            ws.send(json.dumps({'type':'data','value':{'sensor':'temp','value':temp_val}}))
        else:
            temp_val = global prev_temp
            ws.send(json.dumps({'type':'data','value':{'sensor':'temp','value':temp_val}}))
        
        
        temperature_file = open('temp_output.txt', 'r')
        temp_val = temperature_file.readline()
        temperature_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'temp','value':temp_val}}))

        accx_file = open('accx_output.txt', 'r')
        accx_val = accx_file.readline()
        accx_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'accx','value':accx_val}}))

        accy_file = open('accy_output.txt', 'r')
        accy_val = accy_file.readline()
        accy_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'accy','value':accy_val}}))

        accz_file = open('accz_output.txt', 'r')
        accz_val = accz_file.readline()
        accz_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'accz','value':accz_val}}))

        bottomForce_file = open('bforce_output.txt', 'r')
        bottomForce_val = bottomForce_file.readline()
        bottomForce_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'bottomForce','value':bottomForce_val}}))

        topForce_file = open('tforce_output.txt', 'r')
        topForce_val = topForce_file.readline()
        topForce_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'topForce','value':topForce_val}}))

        leftForce_file = open('lforce_output.txt', 'r')
        leftForce_val = leftForce_file.readline()
        leftForce_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'leftForce','value':leftForce_val}}))

        rightForce_file = open('rforce_output.txt', 'r')
        rightForce_val = rightForce_file.readline()
        rightForce_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'rightForce','value':rightForce_val}}))
        '''

if __name__=='__main__':
    read_all()


