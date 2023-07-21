from pymodbus.client import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
import time

print('Start Modbus Client')
client = ModbusClient(host='127.0.0.1', port=5030)
client.connect()

# read/write holding registers

for i in range (10):
    rd = client.read_input_registers(0, count=4, slave=0)
    print('Read', rd.registers[:])
    i = i + 1
    time.sleep(2)

#wh = client.write_registers(0, [50, 60, 80, 100])
'''
rd = client.read_holding_registers(0, count=4, slave=0)
print('Read', rd.registers[:])

# read/write coils
rc= client.read_coils(0,count=8, slave=1)
print("Coils:", rc.bits[:])

#wc = client.write_coils(0, [True, True, True, True, True, True, True, True])

rc= client.read_coils(0,count=8, slave=1)
print("Coils:", rc.bits[:])

# read input registers
ri = client.read_input_registers(0, count=4, slave=2)
print('Read Input:', ri.registers[:])

# read discrete input
rdi = client.read_discrete_inputs(0, count=8, slave=3)
print('Read Discrete Input: ', rdi.bits[:])

for i in range (4) :
    dictionary = [("HoldingRegisters", rd.registers[i]), ("Coils", rc.bits[i])]
    d=dict(dictionary)
    print(d)
'''
client.close()