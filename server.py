from modbus_tk import modbus_tcp, hooks
from modbus_tk.defines import ModbusSlaveRequest
import threading

def read_data(address, function_code, starting_address, quantity):
    # Implementa qui la logica per leggere i dati richiesti dal tuo sistema
    # Restituisci i dati letti come una lista di valori

    # Esempio: restituisce valori incrementali a partire dall'indirizzo di avvio
    return list(range(starting_address, starting_address + quantity))

class ModbusServer(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.server = modbus_tcp.TcpServer(address=ip, port=port)
        self.server.set_timeout(5.0)

        # Registra la funzione di callback per la lettura dei dati
        hooks.install_hook(ModbusSlaveRequest.READ_HOLDING_REGISTERS, read_data)

    def run(self):
        # Avvia il server Modbus
        self.server.start()

    def stop(self):
        # Ferma il server Modbus
        self.server.stop()

def main():
    # Configura l'indirizzo IP e la porta del server Modbus
    server_ip = '0.0.0.0'
    server_port = 502

    # Crea e avvia il server Modbus
    server = ModbusServer(server_ip, server_port)
    server.start()

    print(f"Server Modbus in esecuzione su {server_ip}:{server_port}")

    # Attendi l'interruzione del programma
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Ferma il server Modbus quando viene premuto Ctrl+C
        server.stop()

if __name__ == '__main__':
    main()
