import os
import configparser
import tkinter as tk
from pyModbusTCP.client import ModbusClient
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from tkinter import *
from tkinter import ttk

class App:
    ATTACK_CMD = ["plc-attack", "-c", "config.ini"]

    ATTACKS = {
        "threshold": "attacks/threshold.py",
        "chattering": "attacks/chattering.py",
        "DoS manual": "attacks/dos.py",
        "DoS specular - VPN": "attacks/dosSpecular.py",
        "DoS powerON - VPN": "attacks/dosPowerON.py",
        "DoS specular - LOCAL": "attacks/dosSpecular.py",
        "DoS powerON - LOCAL": "attacks/dosPowerON.py"
    }

    def __init__(self, master):
        self.master = master
        self.attack = None

        self.master.title("PLC Attack")
        self.master.rowconfigure(0, minsize=500, weight=1)
        self.master.columnconfigure(0, minsize=300, weight=1)
        self.master.columnconfigure(1, minsize=1000, weight=1)

        self.cmd_frame = Frame(self.master)
        self.cmd_frame.grid(row=0, column=0, sticky="ns")

        self.out_fram = Frame(self.master)
        self.out_fram.grid(row=0, column=1, sticky="nsew")

        self.lbl_title = Label(self.cmd_frame, text="PLC Attack")
        self.lbl_title.grid(row=0, column=0, pady=15)

        self.lbl_attack_selection = Label(self.cmd_frame, text="Select attack type")
        self.lbl_attack_selection.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)

        self.cbx_attack_selection = ttk.Combobox(self.cmd_frame, values=list(App.ATTACKS.keys()), state='readonly')
        self.cbx_attack_selection.current(0)
        self.cbx_attack_selection.grid(row=2, column=0, columnspan=3, sticky="ew", pady=5, padx=20)

        self.action_frame = Frame(self.cmd_frame)
        self.action_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=15)

        self.lbl_cmd = Label(self.action_frame, text="Actions")
        self.lbl_cmd.grid(row=0, column=0, sticky="ew", pady=5)

        self.btn_frame = Frame(self.action_frame)
        self.btn_frame.grid(row=1, column=0, sticky="ew", pady=5)

        self.btn_start = Button(self.btn_frame, text="Start attack", command=self.start_attack)
        self.btn_start.grid(row=0, column=0, sticky="ew",padx=5)

        self.btn_stop = Button(self.btn_frame, text="Stop attack", command=self.stop_attack)
        self.btn_stop["state"] = "disabled"
        self.btn_stop.grid(row=0, column=1, sticky="ew",padx=5)
        self.btn_exit = Button(self.btn_frame, text="Exit", fg="red", command=self.exit)
        self.btn_exit.grid(row=0, column=2, sticky="ew", padx=5)

        self.text_box = Text(bg="black", fg="white", state='disabled')
        self.text_box.grid(row=0, column=1, sticky="nsew", pady=20, padx=20)

    
    def start_attack(self):   

        def childPatternSpecWindow():
            newWindow = Toplevel(root)
            newWindow.geometry("400x130")
            center_window(newWindow)
            newWindow.title("Attacco Denial of Service")

        
            etichettaIndirizzo1 = ttk.Label(newWindow, text=" Indirizzo IP PLC da attaccare n°1 [ip:porta]*")
            etichettaIndirizzo2 = ttk.Label(newWindow, text="Indirizzo IP PLC da attaccare n°2 [ip:porta]")
            etichettaIndirizzo3 = ttk.Label(newWindow, text="Indirizzo IP PLC da attaccare n°3 [ip:porta]")

            campoIndirizzo1 = ttk.Entry(newWindow)
            campoIndirizzo2 = ttk.Entry(newWindow)
            campoIndirizzo3 = ttk.Entry(newWindow)
            campi_testo = [campoIndirizzo1, campoIndirizzo2, campoIndirizzo3]
                       
            bottone_attacco = ttk.Button(newWindow, text="Lancia DoS", command=lambda: launchAutoSpecularDoS(newWindow, campi_testo))
            bottone_indietro = ttk.Button(newWindow, text="Annulla", command=lambda: closeChildWindow(newWindow))

            # Posizionamento dei widget nella griglia
            etichettaIndirizzo1.grid(row=0, column=0, padx=8, pady=4)
            campoIndirizzo1.grid    (row=0, column=1, padx=5, pady=4)
            etichettaIndirizzo2.grid(row=1, column=0, padx=8, pady=4)
            campoIndirizzo2.grid    (row=1, column=1, padx=5, pady=4)
            etichettaIndirizzo3.grid(row=2, column=0, padx=8, pady=4)
            campoIndirizzo3.grid    (row=2, column=1, padx=5, pady=4)
            bottone_indietro.grid   (row=3, column=0, padx=5, pady=4)
            bottone_attacco.grid    (row=3, column=1, padx=5, pady=4)

        def launchAutoSpecularDoS(window, campi_testo):
            config = configparser.ConfigParser()
            config.read('config.ini')
            # Modifica i valori nel file .ini
            if campi_testo[0].get() == "":                         
                print("ERRORE: Il primo indirizzo è obbligatorio da inserire!")
                exit()
            config.set('plc', 'plc1', campi_testo[0].get())

            if campi_testo[1].get() == "":
                config.set('plc', 'plc2', campi_testo[0].get())
            if campi_testo[2].get() == "":
                config.set('plc', 'plc3', campi_testo[0].get())

            if campi_testo[0].get() != "" and campi_testo[1].get() != "" and campi_testo[2].get() == "":
                config.set('plc', 'plc1', campi_testo[0].get())
                config.set('plc', 'plc2', campi_testo[1].get())
                config.set('plc', 'plc3', campi_testo[0].get())

            if campi_testo[0].get() != "" and campi_testo[1].get() != "" and campi_testo[2].get() != "":
                config.set('plc', 'plc1', campi_testo[0].get())
                config.set('plc', 'plc2', campi_testo[1].get())
                config.set('plc', 'plc3', campi_testo[2].get())
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            launchSpecularDoSVPN()
            closeChildWindow(window)

        def childPatternPowerWindow():
            newWindow = Toplevel(root)
            newWindow.geometry("400x130")
            center_window(newWindow)
            newWindow.title("Attacco Denial of Service")

        
            etichettaIndirizzo1 = ttk.Label(newWindow, text=" Indirizzo IP PLC da attaccare n°1 [ip:porta]*")
            etichettaIndirizzo2 = ttk.Label(newWindow, text="Indirizzo IP PLC da attaccare n°2 [ip:porta]")
            etichettaIndirizzo3 = ttk.Label(newWindow, text="Indirizzo IP PLC da attaccare n°3 [ip:porta]")

            campoIndirizzo1 = ttk.Entry(newWindow)
            campoIndirizzo2 = ttk.Entry(newWindow)
            campoIndirizzo3 = ttk.Entry(newWindow)
            campi_testo = [campoIndirizzo1, campoIndirizzo2, campoIndirizzo3]
                       
            bottone_attacco = ttk.Button(newWindow, text="Lancia DoS", command=lambda: launchAutoPowerONDoS(newWindow, campi_testo))
            bottone_indietro = ttk.Button(newWindow, text="Annulla", command=lambda: closeChildWindow(newWindow))

            # Posizionamento dei widget nella griglia
            etichettaIndirizzo1.grid(row=0, column=0, padx=8, pady=4)
            campoIndirizzo1.grid    (row=0, column=1, padx=5, pady=4)
            etichettaIndirizzo2.grid(row=1, column=0, padx=8, pady=4)
            campoIndirizzo2.grid    (row=1, column=1, padx=5, pady=4)
            etichettaIndirizzo3.grid(row=2, column=0, padx=8, pady=4)
            campoIndirizzo3.grid    (row=2, column=1, padx=5, pady=4)
            bottone_indietro.grid   (row=3, column=0, padx=5, pady=4)
            bottone_attacco.grid    (row=3, column=1, padx=5, pady=4)

        def launchAutoPowerONDoS(window, campi_testo):
            config = configparser.ConfigParser()
            config.read('config.ini')
            # Modifica i valori nel file .ini
            if campi_testo[0].get() == "":                         
                print("ERRORE: Il primo indirizzo è obbligatorio da inserire!")
                exit()
            config.set('plc', 'plc1', campi_testo[0].get())

            if campi_testo[1].get() == "":
                config.set('plc', 'plc2', campi_testo[0].get())
            if campi_testo[2].get() == "":
                config.set('plc', 'plc3', campi_testo[0].get())

            if campi_testo[0].get() != "" and campi_testo[1].get() != "" and campi_testo[2].get() == "":
                config.set('plc', 'plc1', campi_testo[0].get())
                config.set('plc', 'plc2', campi_testo[1].get())
                config.set('plc', 'plc3', campi_testo[0].get())

            if campi_testo[0].get() != "" and campi_testo[1].get() != "" and campi_testo[2].get() != "":
                config.set('plc', 'plc1', campi_testo[0].get())
                config.set('plc', 'plc2', campi_testo[1].get())
                config.set('plc', 'plc3', campi_testo[2].get())
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            launchPoweredDosVPN()
            closeChildWindow(window)

        def validate_numberSent_entry(coil_entry):
            input = coil_entry.get()
            if not input:
                print("Il valore del campo 'Quanti pacchetti vuoi inviare (continuamente = 'loop'):' non è consentito. Riprova!")
            else:
                result = False
                input_value = coil_entry.get()
                if input_value.isdigit():
                    result = True
                elif input_value == "loop":
                    result = True
                else:
                    print("Il valore del campo 'Quanti pacchetti vuoi inviare (continuamente = 'loop'):' non è consentito. Riprova!")
                return result
        
        def validate_Binary_entry(command):
            input = command.get()
            if not input:
                print("Il valore del campo 'Valore del pacchetto: (0 - OFF; 1 - ON)' non è consentito! Riprova.")
            elif input == "0" or input == "1":
                inputCommand = int(command.get())
                result = False
                if inputCommand == 0:
                    result = True
                elif inputCommand == 1:
                    result = True
                return result
            else:
                print("Il valore del campo 'Valore del pacchetto: (0 - OFF; 1 - ON)' non è consentito! Riprova.")
        
        def center_window(window):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            window_width = window.winfo_reqwidth()
            window_height = window.winfo_reqheight()

            position_x = int((screen_width / 2) - (window_width / 2))
            position_y = int((screen_height / 3) - (window_height / 3))

            window.geometry(f"+{position_x}+{position_y}")
        
        def closeChildWindow(window):
            window.destroy()
        
        def updateIniFile():
            config = configparser.ConfigParser()
            # Leggi il file .ini esistente
            config.read('config.ini')
            # Modifica i valori nel file .ini
            if campi_testo[0].get() == "":                         
                print("ERRORE: Il primo indirizzo è obbligatorio da inserire!")
                exit()
            config.set('plc', 'plc1', campi_testo[0].get())

            if campi_testo[1].get() == "":
                config.set('plc', 'plc2', campi_testo[0].get())
            if campi_testo[2].get() == "":
                config.set('plc', 'plc3', campi_testo[0].get())

            if campi_testo[0].get() != "" and campi_testo[1].get() != "" and campi_testo[2].get() == "":
                config.set('plc', 'plc1', campi_testo[0].get())
                config.set('plc', 'plc2', campi_testo[1].get())
                config.set('plc', 'plc3', campi_testo[0].get())

            if campi_testo[0].get() != "" and campi_testo[1].get() != "" and campi_testo[2].get() != "":
                config.set('plc', 'plc1', campi_testo[0].get())
                config.set('plc', 'plc2', campi_testo[1].get())
                config.set('plc', 'plc3', campi_testo[2].get())

            config.set('params', 'coil1', str(var1.get()))
            config.set('params', 'coil2', str(var2.get()))
            config.set('params', 'coil3', str(var3.get()))
            config.set('params', 'number_of_packages', packet_number_entry.get())
            config.set('params', 'value_of_package', packet_value_entry.get())

            with open('config.ini', 'w') as configfile:
                config.write(configfile)   

        def prepareAttackCommand(attack_key):
            attack_script_path = App.ATTACKS[attack_key]
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)           
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()

        def launchDoS(window, attack_key):
            if(validate_numberSent_entry(packet_number_entry) == True and 
               validate_Binary_entry(packet_value_entry) == True):
                updateIniFile()
                prepareAttackCommand(attack_key)
                closeChildWindow(window)

#DOS - ATTACCO CHE INVERTE SEMPRE IL COMANDO ON/OFF
        def launchSpecularDoSVPN():
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('params', 'number_of_packages', "loop")
            config.set('params', 'value_of_package', "0")
            # Scrivi le modifiche nel file .ini
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            attack_script_path = App.ATTACKS["DoS specular - VPN"]
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)           
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()

        def launchSpecularDoSLOCAL():
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('plc', 'plc1', "127.0.0.1:502")
            config.set('plc', 'plc2', "127.0.0.1:502")
            config.set('plc', 'plc3', "127.0.0.1:502")
            config.set('params', 'number_of_packages', "loop")
            
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            attack_script_path = App.ATTACKS["DoS specular - VPN"] #tanto si riferisce allo stesso file solo con ip diversi
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)           
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()

        #DOS - ATTACCO SEMPRE ON ANCHE SE SI PROVA A SPEGNERE
        def launchPoweredDosVPN():
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('params', 'number_of_packages', "loop")
            config.set('params', 'value_of_package', "0")
            # Scrivi le modifiche nel file .ini
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            attack_script_path = App.ATTACKS["DoS powerON - VPN"]
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)           
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()

        def launchPoweredDosLOCAL():
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('plc', 'plc1', "127.0.0.1:502")
            config.set('plc', 'plc2', "127.0.0.1:502")
            config.set('plc', 'plc3', "127.0.0.1:502")
            config.set('params', 'number_of_packages', "loop")
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            attack_script_path = App.ATTACKS["DoS powerON - VPN"] #tanto si riferisce allo stesso file solo con ip diversi
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)           
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()

            
#######################################################################################################################################
        #Se scelgo l'attacco DOS mi si apre una nuova finestra dove potrò settare i parametri utili per l'attacco
        if self.cbx_attack_selection.get() == "DoS manual":
            newWindow = Toplevel(root)
            newWindow.geometry("490x280")
            center_window(newWindow)
            newWindow.title("Attacco manuale Denial of Service")
            
            etichettaIndirizzo1 = ttk.Label(newWindow, text=" Indirizzo IP PLC da attaccare n°1 [ip:porta]*")
            etichettaIndirizzo2 = ttk.Label(newWindow, text="Indirizzo IP PLC da attaccare n°2 [ip:porta]")
            etichettaIndirizzo3 = ttk.Label(newWindow, text="Indirizzo IP PLC da attaccare n°3 [ip:porta]")

            campoIndirizzo1 = ttk.Entry(newWindow)
            campoIndirizzo2 = ttk.Entry(newWindow)
            campoIndirizzo3 = ttk.Entry(newWindow)
            campi_testo = [campoIndirizzo1, campoIndirizzo2, campoIndirizzo3]
            
            etichettaCoils = tk.Label(newWindow, text=" Quale coil vuoi attaccare? ", padx = 20)

            var1 = tk.IntVar()
            var2 = tk.IntVar()
            var3 = tk.IntVar()
            
            c1 = tk.Checkbutton(newWindow, text='Coil 1',variable=var1, onvalue=1, offvalue=0)
            c2 = tk.Checkbutton(newWindow, text='Coil 2',variable=var2, onvalue=1, offvalue=0)
            c3 = tk.Checkbutton(newWindow, text='Coil 3',variable=var3, onvalue=1, offvalue=0)

            packet_number_label = ttk.Label(newWindow, text="Quanti pacchetti vuoi inviare (continuamente = 'loop'):")
            packet_number_entry = ttk.Entry(newWindow, width=6)

            packet_value_label = ttk.Label(newWindow, text="Valore del pacchetto: (0 - OFF; 1 - ON)")
            packet_value_entry = ttk.Entry(newWindow, width=1)

            bottone_attacco = ttk.Button(newWindow, text="Lancia DoS", command=lambda: launchDoS(newWindow, attack_key))
            bottone_indietro = ttk.Button(newWindow, text="Annulla", command=lambda: closeChildWindow(newWindow))

            # Posizionamento dei widget nella griglia
            etichettaIndirizzo1.grid(row=0, column=0, padx=8, pady=4)
            campoIndirizzo1.grid    (row=0, column=1, padx=5, pady=4)
            etichettaIndirizzo2.grid(row=1, column=0, padx=8, pady=4)
            campoIndirizzo2.grid    (row=1, column=1, padx=5, pady=4)
            etichettaIndirizzo3.grid(row=2, column=0, padx=8, pady=4)
            campoIndirizzo3.grid    (row=2, column=1, padx=5, pady=4)  
            etichettaCoils.grid     (row=3, column=0, padx=5, pady=4)  
            c1.grid                 (row=3, column=1, padx=5, pady=1)
            c2.grid                 (row=4, column=1, padx=5, pady=1)
            c3.grid                 (row=5, column=1, padx=5, pady=1)
            packet_number_label.grid(row=6, column=0, padx=5, pady=4)
            packet_number_entry.grid(row=6, column=1, padx=5, pady=4)
            packet_value_label.grid (row=7, column=0, padx=5, pady=4)
            packet_value_entry.grid (row=7, column=1, padx=5, pady=4)
            bottone_indietro.grid   (row=8, column=0, padx=5, pady=4)
            bottone_attacco.grid    (row=8, column=1, padx=5, pady=4)
            
            attack_key = self.cbx_attack_selection.get()
             
#############################################################################################################################################
        #CASO DI UN QUALSIASI ALTRO ATTACCO CHE NON SIA IL DOS
        
        elif self.cbx_attack_selection.get() == "DoS specular - VPN":
            childPatternSpecWindow()
        elif self.cbx_attack_selection.get() == "DoS powerON - VPN":
            childPatternPowerWindow()
        elif self.cbx_attack_selection.get() == "DoS specular - LOCAL":
            launchSpecularDoSLOCAL()
        elif self.cbx_attack_selection.get() == "DoS powerON - LOCAL":
            launchPoweredDosLOCAL()
        else:
            attack_key = self.cbx_attack_selection.get()
            attack_script_path = App.ATTACKS[attack_key]
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()
        
    def stop_attack(self):
        self.attack.terminate()
        self.btn_stop["state"] = "disabled"
        self.btn_start["state"] = "normal"

    def read_output(self, pipe):
        while True:
            data = os.read(pipe.fileno(), 1 << 20)
            data = data.replace(b"\r\n", b"\n")
            if data:
                self.text_box.configure(state='normal')
                self.text_box.insert("end", data.decode())
                self.text_box.see("end")
                self.text_box.configure(state='disabled')
            else:
                return None
    
    def exit(self):
        if self.attack:
            self.attack.terminate()
        self.master.destroy()


root = Tk()
app = App(root)
root.mainloop()

