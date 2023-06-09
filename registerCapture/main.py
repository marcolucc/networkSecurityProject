import pandas as pd #json 
import os
from datetime import datetime # Per il timestamp dei file JSON (per uso futuro)
import time #needed for sleep and to capture data for set amount of time
import ray#thread parall, per usarlo basta inserire il decoratore @ray.remote sopra alla funzione interessata
## Execute in parallel -> ray.get([plc1.remote(), plc2.remote()])
import json 
from collections import defaultdict
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks
import logging
import itertools
from time import sleep

#logger
logger = modbus_tk.utils.create_logger("console", level=logging.DEBUG)

logging.basicConfig(filename="plcHistoryTOOL",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

#parallel distributed execution
ray.init()


'''
#timestamp1=[]
#timestamp2=[]

ora=datetime.now(tz=None)

with open(f'historian/PLC1-{plc1}-{port1}@{ora}.json', 'w') as sp:
            sp.write(json.dumps(single_plc_registers, indent=4))
            #print(single_plc_registers)

@ray.remote
def test1():
    ora=datetime.now(tz=None)
    timestamp1.append(ora)
    with open(f'PLC1@{ora}.json', 'w') as sp:
        sp.write("test1")
        #print(single_plc_registers)

@ray.remote
def test2():
    ora=datetime.now(tz=None)
    timestamp2.append(ora)
    with open(f'PLC1@{ora}.json', 'w') as sp:
        sp.write("test2")

        #print(single_plc_registers)
'''

def connect_to_slave(ip,port):
    """Connect to the slave

    Args:
        ip (string): ip of the modbus slave
        port (int): port of the modbus slave
    """
    # Connect to the slave
    ip=str(ip)
    port=int(port)
    master = modbus_tcp.TcpMaster(host=ip,port=port)
    master.set_timeout(5.0)
    logger.info("Connected to ip=%s:%s",ip,port)
    return(master)

##Functions to read data from the PLCs
def read_c(master):
    """read coils, coils are addressed as follows: [0-xxx].[0-7]

    Args:
        master (object): to send the read command to the right plc
    """
    registers= {}
    values=master.execute(1, cst.READ_COILS, 0, 90)  
    count=0
    for c in range(0,11):
        for a in range(0,8):
            registers['%QX' + str(c) + '.' + str(a)] = str(values[count])
            count+=1
            
    return(registers)
    
def read_ir(master):
    """read input registers, ir are addressed as follows: [0-xxx]

    Args:
        master (object): to send the read command to the right plc
    """
    registers= {}
    values=master.execute(1, cst.READ_INPUT_REGISTERS, 0, 11)
    c=0
    for i in values:
        registers['%IW' + str(c)] = str(i)
        c+=1    
    return(registers)

def read_di(master):
    """read discrete input, di are addressed as follows: [0-xxx].[0-7]

    Args:
        master (object): to send the read command to the right plc
    """
    registers= {}
    values=master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 90)
    count=0
    for c in range(0,11):
        for a in range(0,8):
            registers['%IX' + str(c) + '.' + str(a)] = str(values[count])
            count+=1
    return(registers)
    
def read_mr(master):
    """read memory registers, mr are addressed as follows: [0-xxx] and are holding registers starting from the address 1024

    Args:
        master (object): to send the read command to the right plc
    """
    registers= {}
    values=master.execute(1, cst.READ_HOLDING_REGISTERS, 1024, 11)
    c=0
    for i in values:
        registers['%MW' + str(c)] = str(i)
        c+=1    
    return(registers)
    
def read_hr(master):
    """read holding registers, hr are addressed as follows: [0-xxx]

    Args:
        master (object): to send the read command to the right plc
    """
    registers= {}
    values=master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 11)
    c=0
    for i in values:
        registers['%QW' + str(c)] = str(i)
        c+=1    
    return(registers)
    
    

@ray.remote
def read_registers(name,ip,port,master):
    name=str(name)
    ip=str(ip)
    port=str(port)
    single_plc_registers = defaultdict(dict)
    
    single_plc_registers[ip]['DiscreteInputRegisters'] = read_di(master)
    single_plc_registers[ip]['InputRegisters'] = read_ir(master)
    single_plc_registers[ip]['HoldingOutputRegisters'] = read_hr(master)
    single_plc_registers[ip]['MemoryRegisters'] = read_mr(master)
    single_plc_registers[ip]['Coils'] = read_c(master)
    
    ora=datetime.now(tz=None)

    with open(f'historian/{name}-{ip}-{port}@{ora}.json', 'w') as sp:
        sp.write(json.dumps(single_plc_registers, indent=4))


def main(): 
    master = connect_to_slave("127.0.0.1",8502)
    master1 = connect_to_slave("127.0.0.1",8503)
    master2 = connect_to_slave("127.0.0.1",8504)
    
    #hr = read_hr.remote("PLC1",master)
    #hr1 = read_hr.remote("PLC2",master1)
    #hr2 = read_hr.remote("PLC3",master2)
    
    #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 1024, 12))
    #logger.info(master1.execute(1, cst.READ_HOLDING_REGISTERS, 1024, 12))
    #ray.get([hr,hr1,hr2])
    
    #ids = [hr, hr1,hr2]
    
    #ray.get(ids)
    #read_registers("plc1","127.0.0.1",8502,master)
    t_end = time.time() + 3600
    #This will run for 15 min x 60 s = 900 seconds.
    while time.time() < t_end:
        plc1=read_registers.remote("plc1","127.0.0.1",8502,master)
        plc2=read_registers.remote("plc2","127.0.0.1",8503,master1)
        plc3=read_registers.remote("plc3","127.0.0.1",8504,master2)
        sleep(0.8)
        ids = [plc1,plc2,plc3]
        ray.get(ids)
    
    '''
    ready, not_ready = ray.wait(ids)
    print("ready: %s",len(ready))
    print("not ready: %s",len(not_ready))
    
    while(True):
        print("ready: %s",len(ready))
        print("not ready: %s",len(not_ready))
        ready, not_ready = ray.wait(ids)
        ray.get(ready)
        ids = not_ready
        if not ids:
            break
    '''
        
    
    '''
    for i in range(1,40): 
        ready, not_ready = ray.wait(ids)
        print('iteration:', i) 
        print('Ready length, values: ', len(ready), ray.get(ready))
        print('Not Ready length:', len(not_ready))
        ids = not_ready
        if not ids:
            break
    '''



if __name__ == '__main__':
    main()
