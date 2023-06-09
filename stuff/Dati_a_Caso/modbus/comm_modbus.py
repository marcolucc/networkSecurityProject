import easymodbus.modbusClient
import time

plc1 = easymodbus.modbusClient.ModbusClient('127.0.0.1', 8502)

plc2 = easymodbus.modbusClient.ModbusClient('127.0.0.1', 8503)
plc2.connect()
plc1.connect()

while (True):
    #leggo i registri di input (level e request)
    
    try:
        print("leggo da plc2")
        inputRegisters = plc2.read_coils(0, 1)
        print(inputRegisters)
    except:
        print("Errore in lettura coil")

    try:
        print("\n Richiesta: ")
        richiesta = inputRegisters[0]
    
        print(richiesta)
    except:
        print("errore lettura buffer registro")
    

    

    #scrivo i coil di richiesta
    print("Scrivo su plc1")
    try:
        plc1.write_single_coil(2, richiesta)

        
    except:
        print("errore scrittura")
    print("close connection")
    time.sleep(1)
    
