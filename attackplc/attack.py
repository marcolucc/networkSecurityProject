#!/usr/bin/env python3

import io
import sys
import signal
import logging
import argparse
import coloredlogs
import configparser

from types import FunctionType
from typing import Dict, List

from attackplc.ModbusInterface import ModbusInterface
from attackplc.ModbusContext import ModbusContext
from pymodbus.client import ModbusTcpClient
from time import sleep

parser = argparse.ArgumentParser(description='a python tool to attack Modbus PLCs')
parser.add_argument('--log-level', help='log level to use (standard level names of python logging library, e.g. DEBUG, INFO, ecc)', default='INFO')
parser.add_argument('--config', '-c', help='configuration file to use', default=None)
parser.add_argument('--param', '-p', help='override configuration parameter section.key=value', action='append')
parser.add_argument('script', help='script to attack the PLC')


def load_config(args):
    config = configparser.ConfigParser()
    if args.config is not None:
        logging.debug('loading configuration file')
        if not config.read(args.config):
            logging.error('cannot load configuration file')
            sys.exit(1)

    # load command-line override
    if args.param:
        for p in args.param:
            try:
                key, value = p.split('=')
                section, option = key.split('.')
                if not config.has_section(section):
                    config.add_section(section)
                config.set(section, option, value)
            except Exception:
                logging.error(f'invalid argument {p}: must be of format section.key=value')
                sys.exit(1)

    return config


def main():
    args = parser.parse_args()
    coloredlogs.install(level=args.log_level.upper(), fmt='%(asctime)s %(name)s %(levelname)s %(message)s')
    config = load_config(args)

    interfaces: Dict[str, ModbusInterface] = {}
    if not config.has_section('plc'):
        logging.error('configuration error: missing plc section in config')
        sys.exit(1)

    # create PLC instances
    for name in config['plc']:
        address = config.get('plc', name)
        parts = address.split(':')
        if len(parts) == 1:
            host = parts[0]
            port = 502
        elif len(parts) == 2:
            host = parts[0]
            port = int(parts[1])
        else:
            logging.error(f'invalid address format {address} for plc {name}')
            sys.exit(1)

        logging.info(f'creating interface for plc {name} host {address}')
        interfaces[name] = ModbusInterface(host, port)

    context = ModbusContext(config, interfaces)

    # stop everything on CTRL-C
    signal.signal(signal.SIGINT, lambda: context.stop())

    # load attack script
    with open(args.script) as f:
        attack_script_source = f.read()

    attack_logger = logging.getLogger(args.script)

    def print_override(*args, **kwargs):
        with io.StringIO() as f:
            print(*args, file=f, end='', **kwargs)
            attack_logger.info(f.getvalue())

    attack_globals = {
        'print': print_override
    }
    exec(attack_script_source, attack_globals)

    if not isinstance(attack_globals.get('attack'), FunctionType):
        logging.error('attack script should define an attack function')

    logging.info('opening PLC connections')
    for interface in interfaces.values():
        interface.connect()

    logging.info('running exploit')
    attack_globals['attack'](context)

    context.run()
