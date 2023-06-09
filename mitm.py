#!/usr/bin/env python3

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks

from time import time, sleep

master = modbus_tcp.TcpMaster(host='127.0.0.1' , port=8502)
master.set_timeout(5.0)


server = modbus_tcp.TcpServer(port=9502)
server.start()
slave = server.add_slave(1)
slave.add_block('0', cst.ANALOG_INPUTS, 0, 4)
slave.add_block('1', cst.COILS, 0, 3)

history = []

state = 0
i = 0

while True:
    
    print('STATE:', state)

    data = {}

    if state in (0, 1, 2):
        #
        # leggo tutti i registri del master
        #
        try:
            data['I'] = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 4)
            data['C'] = master.execute(1, cst.READ_COILS, 0, 3)
        except:
            print('error reading master')
            continue

        print('read:', data)

        v = data['I'][0]
        if state == 0 and v > 75:
            state = 1
        elif state == 1 and v < 60:
            state = 2
        elif state == 2 and v > 75:
            state = 3
         
        if state in (1, 2):
            history.append(data)
            
        v1 = v

    if state == 3:
        data = history[i % len(history)]
        i += 1
        
    #
    # scrivo i dati nello slave
    # 
    print('write', data)
    slave.set_values('0', 0, data['I'])
    slave.set_values('1', 0, data['C'])

    sleep(0.5)

