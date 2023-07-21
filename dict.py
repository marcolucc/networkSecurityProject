import json

def Dict(json_path):
    register_dict = load_json_file(json_path)

    # Estrai i valori dal dizionario
    return extract_values_from_registers_dict(register_dict)

def extract_values_from_registers_dict(self, registers_dict):
    discrete_input_values = []
    input_register_values = []
    holding_output_register_values = []
    memory_register_values = []
    coil_values = []

    # Extract values from DiscreteInputRegisters
    for i in range(11):
        for j in range(8):
            key = f"%IX{i}.{j}"
            value = int(registers_dict["127.0.0.1"]["DiscreteInputRegisters"][key])
            discrete_input_values.append(value)

    # Extract values from InputRegisters
    for i in range(11):
        key = f"%IW{i}"
        value = int(registers_dict["127.0.0.1"]["InputRegisters"][key])
        input_register_values.append(value)

    # Extract values from HoldingOutputRegisters
    for i in range(11):
        key = f"%QW{i}"
        value = int(registers_dict["127.0.0.1"]["HoldingOutputRegisters"][key])
        holding_output_register_values.append(value)

    # Extract values from MemoryRegisters
    for i in range(11):
        key = f"%MW{i}"
        value = int(registers_dict["127.0.0.1"]["MemoryRegisters"][key])
        memory_register_values.append(value)

    # Extract values from Coils
    for i in range(11):
        for j in range(8):
            key = f"%QX{i}.{j}"
            value = int(registers_dict["127.0.0.1"]["Coils"][key])
            coil_values.append(value)

    return (
        discrete_input_values,
        input_register_values,
        holding_output_register_values,
        memory_register_values,
        coil_values
    )

def load_json_file(self, file_name):
    try:
        with open(file_name, "r") as json_file:
            registers_dict = json.load(json_file)
        print(f"File JSON '{file_name}' caricato con successo.")
        return registers_dict
    except FileNotFoundError:
        print(f"Errore: il file '{file_name}' non esiste.")
    except json.JSONDecodeError:
        print(f"Errore: il file JSON '{file_name}' è malformato.")
        return None

'''
class Dict:

    def __init__(self, json_path) -> None:
        #self.json_path = json_path

        self.register_dict = self.load_json_file(json_path)

        # Estrai i valori dal dizionario
        (
            self.discrete_input_values,
            self.input_register_values,
            self.holding_output_register_values,
            self.memory_register_values,
            self.coil_values
        ) = self.extract_values_from_registers_dict(self.register_dict)

    def get_all_data(self):
        return (
            self.discrete_input_values,
            self.input_register_values,
            self.holding_output_register_values,
            self.memory_register_values,
            self.coil_values
        )

    def extract_values_from_registers_dict(self, registers_dict):
        discrete_input_values = []
        input_register_values = []
        holding_output_register_values = []
        memory_register_values = []
        coil_values = []

        # Extract values from DiscreteInputRegisters
        for i in range(11):
            for j in range(8):
                key = f"%IX{i}.{j}"
                value = int(registers_dict["127.0.0.1"]["DiscreteInputRegisters"][key])
                discrete_input_values.append(value)

        # Extract values from InputRegisters
        for i in range(11):
            key = f"%IW{i}"
            value = int(registers_dict["127.0.0.1"]["InputRegisters"][key])
            input_register_values.append(value)

        # Extract values from HoldingOutputRegisters
        for i in range(11):
            key = f"%QW{i}"
            value = int(registers_dict["127.0.0.1"]["HoldingOutputRegisters"][key])
            holding_output_register_values.append(value)

        # Extract values from MemoryRegisters
        for i in range(11):
            key = f"%MW{i}"
            value = int(registers_dict["127.0.0.1"]["MemoryRegisters"][key])
            memory_register_values.append(value)

        # Extract values from Coils
        for i in range(11):
            for j in range(8):
                key = f"%QX{i}.{j}"
                value = int(registers_dict["127.0.0.1"]["Coils"][key])
                coil_values.append(value)

        return (
            discrete_input_values,
            input_register_values,
            holding_output_register_values,
            memory_register_values,
            coil_values
        )

    # Carica il file JSON
    def load_json_file(self, file_name):
        try:
            with open(file_name, "r") as json_file:
                registers_dict = json.load(json_file)
            print(f"File JSON '{file_name}' caricato con successo.")
            return registers_dict
        except FileNotFoundError:
            print(f"Errore: il file '{file_name}' non esiste.")
        except json.JSONDecodeError:
            print(f"Errore: il file JSON '{file_name}' è malformato.")
            return None

    

    # Stampa le liste di valori estratti
    # print("Discrete Input Values:", discrete_input_values)
    # print("Input Register Values:", input_register_values)
    # print("Holding Output Register Values:", holding_output_register_values)
    # print("Memory Register Values:", memory_register_values)
    # print("Coil Values:", coil_values)
    '''
