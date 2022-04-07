import threading
import IR
import websocket
import json

ws = websocket.WebSocket()
ws.connect('ws://eodmat.herokuapp.com/ws/matserver/')

def send_ir():
    while True:
        output = IR.get_reading()
        #ir_output_file = open('ir_output.txt', 'wt')
        #ir_output_file.write(str(output))
        #ir_output_file.close()
        
        #ir_file = open('ir_output.txt', 'r')
        #ir_val = ir_file.readline()
        #ir_file.close()
        ws.send(json.dumps({'type':'data','value':{'sensor':'ircamera','value':output}}))
        
        #time.sleep(.5)
        

ir_thread = threading.Thread(target=send_ir)

if __name__=='__main__':
    ir_thread.start()