import threading
import IR
import websocket
import json
import time
ws = websocket.WebSocket()
ws.connect('wss://eodmat.herokuapp.com/ws/matserver/')
def send_ir():
    while True:
        try:
            output = IR.get_reading()
        except:
            continue
            #pass
        try:
            ws.send(json.dumps({'type':'ir_data','value':[{'sensor':'ircamera','value':output}]}))
        except:
            #print('sending error')
            #time.sleep(.5)
            ws.connect('ws://eodmat.herokuapp.com/ws/matserver/')
            #ws.send(json.dumps({'type':'ir_data','value':[{'sensor':'ircamera','value':output}]}))

if __name__=='__main__':
    send_ir()