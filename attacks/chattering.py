import time
import configparser
import random
from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime

def attack(ctx):

    def pump(level, value, mode):
        increment = 1
        ct = 0
        ct_2 = 0
        status = "text"
        level_start = 0
        level_end = 0
        time_2_commands = 0
        limit = 0

        print(mode)

        if(mode == "percentage"): 
            percentage = int(config.get('params', 'percentage'))
            time_empty = int(config.get('params', 'time_empty'))
            new_time_slowed = int(time_empty + (time_empty * (percentage / 100)))
            limit = int((100-percentage) /25)
        else:
            time_2_commands = int(config.get('params', 'time_send'))
            print(time_2_commands)
        while True:
            
            if level > 90:
                increment = -1
                status = "dec"
            elif level < 30:
                increment = 1
                status = "inc"
            

            if(ct == 0):
                level_start = level
                ct = 1
            elif(ct == 1):
                level_end = level
                ct = 2
            
            if(ct == 2):
                if(level_start > level_end): # decreasing
                    status = "dec"
                elif(level_start < level_end): # increasing
                    status = "inc"
                else:
                    status = "stopped"
                ct_2 = 0
                ct = 3
            
            if status == "dec" and ct == 3:
                #apro la coil/pompa
                if checkTrigger:
                    # Trigger checked
                    # Call the function to evaluate conditions
                    all_conditions_true = evaluate_conditions(config, level)

                    # Perform an operation if all conditions are true
                    if all_conditions_true:
                        if mode == "time_command":
                            level += 1 # write_coil(off)
                            time.sleep(time_2_commands)
                            level -=1 # write_coil(on) 
                        elif mode == "percentage":
                            if ct_2 < limit:
                                    ct_2 += 1
                            elif ct_2 >= limit and ct_2 < 4: 
                                ct_2 += 1
                                level += 1
                            elif ct_2 >= 4 and percentage != 100:
                                ct_2 = 1
                            elif ct_2 >= 4 and percentage == 100:
                                ct_2 = 0
                                level += 1
                else:
                    # No triggers
                        if mode == "time_command":
                            print("hi")
                            level += 1 # write_coil(off)
                            time.sleep(time_2_commands)
                            level -=1 # write_coil(on)
                        elif mode == "percentage":
                            if ct_2 < limit:
                                    ct_2 += 1
                            elif ct_2 >= limit and ct_2 < 4:
                                ct_2 += 1
                                level += 1
                            elif ct_2 >= 4 and percentage != 100:
                                ct_2 = 1
                            elif ct_2 >= 4 and percentage == 100:
                                ct_2 = 0
                                level += 1

            elif status == "inc"  and ct == 3:
                #chiudo la coil/pompa
                if checkTrigger:
                    # Trigger checked
                    # Call the function to evaluate conditions
                    all_conditions_true = evaluate_conditions(config, level)

                    # Perform an operation if all conditions are true
                    if all_conditions_true:
                        if mode == "time_command":
                            level += 1 # write_coil(off)
                            time.sleep(time_2_commands)
                            level -=1 # write_coil(on)
                        elif mode == "percentage":
                            if ct_2 < limit:
                                    ct_2 += 1
                            elif ct_2 >= limit and ct_2 < 4:
                                ct_2 += 1
                                level -= 1
                            elif ct_2 >= 4 and percentage != 100:
                                ct_2 = 1
                            elif ct_2 >= 4 and percentage == 100:
                                ct_2 = 0
                                level -= 1
                else:
                    # No triggers
                        if mode == "time_command":
                            level += 1 # write_coil(off)
                            time.sleep(time_2_commands)
                            level -=1 # write_coil(on)
                        elif mode == "percentage":
                            if ct_2 < limit:
                                    ct_2 += 1
                            elif ct_2 >= limit and ct_2 < 4:
                                ct_2 += 1
                                level -= 1
                            elif ct_2 >= 4 and percentage != 100:
                                ct_2 = 1
                            elif ct_2 >= 4 and percentage == 100:
                                ct_2 = 0
                                level -= 1

            current_datetime = datetime.now()
            timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
            level += increment
            print(f"Level: {level}, Timestamp: {timestamp}")  # Print the current level and time
            time.sleep(value)
    
    def checkTrigger(address):
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'params' in config:
            for param_name in config['params']:
                if param_name.startswith('condition'):
                    return True
        return False
    
    def evaluate_conditions(config, level):
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

                        if(cond == ">"):
                            if(level <= value):
                                return False
                        elif(cond == "<"):
                            if(level >= value):
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

    # Random water level
    level = random.randint(1, 100)

    # Read from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    time_empty= int(config.get('params', 'time_empty'))

    
    time_empty = time_empty / 60

    if(config.get('params', 'time_send') == ""):
        mode = "percentage"
    else:
        mode = "time_command"


    pump(level, time_empty, mode)

