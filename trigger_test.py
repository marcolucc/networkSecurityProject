from pymodbus.client import ModbusTcpClient

PLC_IP = "127.0.0.1"

client = ModbusTcpClient(PLC_IP)
client.connect()
client.write_coil(2, False)
client.write_coil(1, False)
client.close()
