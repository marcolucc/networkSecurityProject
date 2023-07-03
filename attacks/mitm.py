import tkinter as tk
from modbus_tk import modbus_tcp

def read_data(ip, register_address):
    # Crea una connessione TCP con il PLC
    master = modbus_tcp.TcpMaster(host=ip, port=502)
    master.set_timeout(5.0)

    try:
        # Leggi il valore dal registro specificato
        value = master.execute(1, modbus_tcp.READ_HOLDING_REGISTERS, register_address, 1)[0]
        return value
    except modbus_tcp.ModbusError as e:
        print("Errore Modbus:", e)
        return None
    finally:
        # Chiudi la connessione TCP
        master.close()

def main():
    # Funzione di gestione del pulsante "Lettura"
    def read_button_handler():
        ip = ip_entry.get()
        register_address = int(register_entry.get())

        # Leggi il valore dal PLC
        value = read_data(ip, register_address)

        if value is not None:
            result_label.config(text="Valore letto: " + str(value))
        else:
            result_label.config(text="Errore durante la lettura.")

    # Creazione dell'interfaccia grafica
    window = tk.Tk()
    window.title("Lettura PLC Modbus")

    ip_label = tk.Label(window, text="Indirizzo IP del PLC:")
    ip_label.pack()

    ip_entry = tk.Entry(window)
    ip_entry.pack()

    register_label = tk.Label(window, text="Indirizzo del registro:")
    register_label.pack()

    register_entry = tk.Entry(window)
    register_entry.pack()

    read_button = tk.Button(window, text="Lettura", command=read_button_handler)
    read_button.pack()

    result_label = tk.Label(window, text="")
    result_label.pack()

    window.mainloop()

if __name__ == '__main__':
    main()
