import time, threading

import counter
import forcemux
import PIR
import ADC
import websocket
import json

ws = websocket.WebSocket()
ws.connect('ws://eodmat.herokuapp.com/ws/matserver/')

def write_temp():
	while True:
		output = counter.get_temp()
		temp_output_file = open('temp_output.txt', 'wt')
		temp_output_file.write(str(output))
		temp_output_file.close()
		time.sleep(.5)

def write_accx():
	while True:
		output = counter.get_acc('x')
		accx_output_file = open('accx_output.txt', 'wt')
		accx_output_file.write(str(output))
		accx_output_file.close()
		time.sleep(.5)
		
def write_accy():
	while True:
		output = counter.get_acc('y')
		accy_output_file = open('accy_output.txt', 'wt')
		accy_output_file.write(str(output))
		accy_output_file.close()
		time.sleep(.5)

def write_accz():
	while True:
		output = counter.get_acc('z')
		accz_output_file = open('accz_output.txt', 'wt')
		accz_output_file.write(str(output))
		accz_output_file.close()
		time.sleep(.5)
		
def write_bottomForce():
	while True:
		with forcemux.force1:
			forcemux.function(forcemux.force1, 1)
		output = forcemux.force_out1
		bforce_output_file = open('lforce_output.txt', 'wt')
		bforce_output_file.write(str(round(output, 2)))
		bforce_output_file.close()
		time.sleep(.5)

def write_topForce():
	while True:
		with forcemux.force3:
			forcemux.function(forcemux.force3, 3)
		output = forcemux.force_out3
		tforce_output_file = open('tforce_output.txt', 'wt')
		tforce_output_file.write(str(round(output, 2)))
		tforce_output_file.close()
		time.sleep(.5)

def write_leftForce():
	while True:
		with forcemux.force4:
			forcemux.function(forcemux.force4, 4)
		output = forcemux.force_out4
		lforce_output_file = open('rforce_output.txt', 'wt')
		lforce_output_file.write(str(round(output, 2)))
		lforce_output_file.close()
		time.sleep(.5)
		
def write_rightForce():
	while True:
		with forcemux.force2:
			forcemux.function(forcemux.force2, 2)
		output = forcemux.force_out2
		rforce_output_file = open('bforce_output.txt', 'wt')
		rforce_output_file.write(str(round(output, 2)))
		rforce_output_file.close()
		time.sleep(.5)
		
def write_PIR():
    while True:
        output = PIR.get_reading()
        PIR_output_file = open('PIR_output.txt', 'wt')
        PIR_output_file.write(str(output))
        PIR_output_file.close()
        time.sleep(.5)
        
def write_adc():
    while True:
        output = ADC.resistor_chan.voltage
        photoResistor_output_file = open('photoResistor_output.txt', 'wt')
        photoResistor_output_file.write(str(round(output, 3)))
        photoResistor_output_file.close()
        
        output = ADC.diode_chan.voltage
        photoDiode_output_file = open('photoDiode_output.txt', 'wt')
        photoDiode_output_file.write(str(round(output, 3)))
        photoDiode_output_file.close()
        
        output = ADC.sound_chan.voltage
        sound_output_file = open('sound_output.txt', 'wt')
        sound_output_file.write(str(round(output, 3)))
        sound_output_file.close()
        
        time.sleep(.5)

temp_thread = threading.Thread(target=write_temp)
accx_thread = threading.Thread(target=write_accx)
accy_thread = threading.Thread(target=write_accy)
accz_thread = threading.Thread(target=write_accz)
bottomForce_thread = threading.Thread(target=write_bottomForce)
topForce_thread = threading.Thread(target=write_topForce)
leftForce_thread = threading.Thread(target=write_leftForce)
rightForce_thread = threading.Thread(target=write_rightForce)
pir_thread = threading.Thread(target=write_PIR)
adc_thread = threading.Thread(target=write_adc)


if __name__=='__main__':
	temp_thread.start()
	accx_thread.start()
	accy_thread.start()
	accz_thread.start()
	bottomForce_thread.start()
	topForce_thread.start()
	leftForce_thread.start()
	rightForce_thread.start()
	pir_thread.start()
	adc_thread.start()
