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
        "Denial of Service": "attacks/dos.py",
        "Specular - VPN": "attacks/dosSpecular.py",
        "PowerON - VPN": "attacks/dosPowerON.py",
        "Specular - LOCAL": "attacks/dosSpecular.py",
        "PowerON - LOCAL": "attacks/dosPowerON.py"
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
            """
            Questa funzione crea la finestra secondaria dove è possibile inserire gli indirizzi delle plc
            su cui lanciare l'attacco di tipo specular (Mando ON se la plc è OFF e viceversa in modo continuativo)
            """
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
            """
            Questa funzione aggiorna il file 'config.ini' al fine 
            di lanciare l'attacco specularDoS sulle plc precedentemente selezionate
            Alla fine lancio la funzione 'launchSpecularDoSVPN()' che lancerà l'attacco
            e chiamo la funzione 'closeChildWindow(window)' con la quale si chiude la 
            finestra secondaria usata per l'inserimento degli indirizzi ip:porta
            """
            config = configparser.ConfigParser()
            config.read('config.ini')
            
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
            """
            Questa funzione crea la finestra secondaria dove è possibile inserire gli indirizzi delle plc
            su cui lanciare l'attacco di tipo powerON (Mando ON se la plc è OFF e attendo altrimenti,
            in modo continuativo)
            """
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
            """
            Questa funzione aggiorna il file 'config.ini' al fine 
            di lanciare l'attacco powerON sulle plc precedentemente selezionate
            Alla fine lancio la funzione 'launchPoweredDosVPN()' che lancerà l'attacco
            e chiamo la funzione 'closeChildWindow(window)' con la quale si chiude la 
            finestra secondaria usata per l'inserimento degli indirizzi ip:porta
            """
            config = configparser.ConfigParser()
            config.read('config.ini')

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

        def validate_number_entry(coil_entry):
            """
            Questa funzione fa un controllo per verificare che sia stato inserito un valore numerico 
            o la stringa 'loop' allinterno del campo 
            'Quanti pacchetti vuoi inviare (continuamente = 'loop'):' nell'ambito dell'attacco manuale
            """
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
            """
            Questa funzione fa un controllo per verificare che sia stato inserito un valore numerico 
            pari o a 1 o a 0 all'interno del campo 
            'Valore del pacchetto: (0 - OFF; 1 - ON)' nell'ambito dell'attacco manuale
            """
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
        
        def validate_inf_sup(inf, sup):
            if inf.get() == "" and sup.get() == "":
                return True
            
            inferior_value = int(inf.get())
            superior_value = int(sup.get())
            print(superior_value)
            print(inferior_value)

            if inferior_value >= 0 and inferior_value <= 100 and superior_value >= 0 and superior_value <= 100:        
                if superior_value > inferior_value:
                        print("OK coppia valori")
                        return True
                else:
                    return False
        def center_window(window):
            """
            Questa funzione si occupa di centrare rispetto allo schermo la 
            finestra che si apre per l'inserimento degli ip da attaccare.
            """
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            window_width = window.winfo_reqwidth()
            window_height = window.winfo_reqheight()

            position_x = int((screen_width / 2) - (window_width / 2))
            position_y = int((screen_height / 3) - (window_height / 3))

            window.geometry(f"+{position_x}+{position_y}")
        
        def closeChildWindow(window):
            """
            Questa funzione si occupa di chiudere la finestra 
            passata come parametro formale.
            """
            window.destroy()
        
        def updateIniFile():
            """
            Questa funzione si occupa di aggiornare il file .ini con i parametri 
            utili per lanciare un attacco DoS.
            """
            config = configparser.ConfigParser()
            config.read('config.ini')

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
            config.set('params', 'sup1', sup_value_entry1.get())
            config.set('params', 'inf1', inf_value_entry1.get())

            config.set('params', 'sup2', sup_value_entry2.get())
            config.set('params', 'inf2', inf_value_entry2.get())

            config.set('params', 'sup3', sup_value_entry3.get())
            config.set('params', 'inf3', inf_value_entry3.get())

            with open('config.ini', 'w') as configfile:
                config.write(configfile)   

        def prepareAttackCommand(attack_key):
            """
            Questa funzione si occupa di preparare i parametri d'attacco.
            """
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
            """
            Questa funzione si occupa di lanciare l'attacco DoS in modalità manuale.
            """
            if validate_number_entry(packet_number_entry) == True and validate_Binary_entry(packet_value_entry) == True:
                print("ok controllo loop e valore pacchetto")
                if validate_inf_sup(inf_value_entry1, sup_value_entry1) == True and validate_inf_sup(inf_value_entry2, sup_value_entry2) == True and validate_inf_sup(inf_value_entry3 ,sup_value_entry3) == True:
                    print("ok controllo VALORI sup1,inf1,sup2,inf2,sup3,inf3")    
                    updateIniFile()
                    prepareAttackCommand(attack_key)
                    closeChildWindow(window)
                else:
                    print("Il valore superiore in percentuale non può essere inferiore o uguale rispetto a quello inferiore in percentuale")

#DOS - ATTACCO CHE INVERTE SEMPRE IL COMANDO ON/OFF
        def launchSpecularDoSVPN():
            """
            Questa funzione si occupa di lanciare l'attacco DoS in modalità automatica di tipo specular.
            Con VPN accesa.
            """
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('params', 'number_of_packages', "loop")
            config.set('params', 'value_of_package', "0")
            # Scrivi le modifiche nel file .ini
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            attack_script_path = App.ATTACKS["Specular - VPN"]
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)           
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()

        def launchSpecularDoSLOCAL():
            """
            Questa funzione si occupa di lanciare l'attacco DoS in modalità automatica di tipo specular.
            Usata solo in ambito LOCALE in caso la vpn non andasse.
            """
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('plc', 'plc1', "127.0.0.1:502")
            config.set('plc', 'plc2', "127.0.0.1:502")
            config.set('plc', 'plc3', "127.0.0.1:502")
            config.set('params', 'number_of_packages', "loop")
            
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            attack_script_path = App.ATTACKS["Specular - VPN"] #tanto si riferisce allo stesso file solo con ip diversi
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
            """
            Questa funzione si occupa di lanciare l'attacco DoS in modalità automatica di tipo powerON.
            Con VPN accesa.
            """
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('params', 'number_of_packages', "loop")
            config.set('params', 'value_of_package', "0")
            # Scrivi le modifiche nel file .ini
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            attack_script_path = App.ATTACKS["PowerON - VPN"]
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)           
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()

        def launchPoweredDosLOCAL():
            """
            Questa funzione si occupa di lanciare l'attacco DoS in modalità automatica di tipo powerON.
            Usata solo in ambito LOCALE in caso la vpn non andasse.
            """
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('plc', 'plc1', "127.0.0.1:502")
            config.set('plc', 'plc2', "127.0.0.1:502")
            config.set('plc', 'plc3', "127.0.0.1:502")
            config.set('params', 'number_of_packages', "loop")
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            attack_script_path = App.ATTACKS["PowerON - VPN"] #tanto si riferisce allo stesso file solo con ip diversi
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)           
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()
        
#######################################################################################################################################
        #Se scelgo l'attacco DOS manuale mi si apre una nuova finestra dove potrò settare i parametri utili per l'attacco
        if self.cbx_attack_selection.get() == "Denial of Service":
            """
            Qui si crea la finestra utile ad immettere i parametri per settare il DoS.
            """
            newWindow = Toplevel(root)
            newWindow.geometry("460x540")
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

            trigger_label1 = ttk.Label(newWindow, text="Attacco a trigger 1")
            sup_value_label1 = ttk.Label(newWindow, text="Valore di 'level' sopra al quale mando i pacchetti: (>)")
            sup_value_entry1 = ttk.Entry(newWindow, width=3)
            inf_value_label1 = ttk.Label(newWindow, text="Valore di 'level' sotto al quale mando i pacchetti: (<)")
            inf_value_entry1 = ttk.Entry(newWindow, width=3)

            trigger_label2 = ttk.Label(newWindow, text="Attacco a trigger 2")
            sup_value_label2 = ttk.Label(newWindow, text="Valore di 'level' sopra al quale mando i pacchetti: (>)")
            sup_value_entry2 = ttk.Entry(newWindow, width=3)
            inf_value_label2 = ttk.Label(newWindow, text="Valore di 'level' sotto al quale mando i pacchetti: (<)")
            inf_value_entry2 = ttk.Entry(newWindow, width=3)

            trigger_label3 = ttk.Label(newWindow, text="Attacco a trigger 3")
            sup_value_label3 = ttk.Label(newWindow, text="Valore di 'level' sopra al quale mando i pacchetti: (>)")
            sup_value_entry3 = ttk.Entry(newWindow, width=3)
            inf_value_label3 = ttk.Label(newWindow, text="Valore di 'level' sotto al quale mando i pacchetti: (<)")
            inf_value_entry3 = ttk.Entry(newWindow, width=3)


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
            trigger_label1.grid      (row=8, column=0, padx=5, pady=4)
            sup_value_label1.grid    (row=9, column=0, padx=5, pady=4)
            sup_value_entry1.grid    (row=9, column=1, padx=5, pady=4)
            inf_value_label1.grid    (row=10, column=0, padx=5, pady=4)
            inf_value_entry1.grid    (row=10, column=1, padx=5, pady=4)

            trigger_label2.grid      (row=11, column=0, padx=5, pady=4)
            sup_value_label2.grid    (row=12, column=0, padx=5, pady=4)
            sup_value_entry2.grid    (row=12, column=1, padx=5, pady=4)
            inf_value_label2.grid    (row=13, column=0, padx=5, pady=4)
            inf_value_entry2.grid    (row=13, column=1, padx=5, pady=4)

            trigger_label3.grid      (row=14, column=0, padx=5, pady=4)
            sup_value_label3.grid    (row=15, column=0, padx=5, pady=4)
            sup_value_entry3.grid    (row=15, column=1, padx=5, pady=4)
            inf_value_label3.grid    (row=16, column=0, padx=5, pady=4)
            inf_value_entry3.grid    (row=16, column=1, padx=5, pady=4)


            bottone_indietro.grid   (row=17, column=0, padx=5, pady=4)
            bottone_attacco.grid    (row=17, column=1, padx=5, pady=4)
            
            attack_key = self.cbx_attack_selection.get()
             
#############################################################################################################################################
        #CASO DI UN QUALSIASI ALTRO ATTACCO CHE NON SIA IL DOS MANUALE
        
        elif self.cbx_attack_selection.get() == "Specular - VPN":
            childPatternSpecWindow()
        elif self.cbx_attack_selection.get() == "PowerON - VPN":
            childPatternPowerWindow()
        elif self.cbx_attack_selection.get() == "Specular - LOCAL":
            launchSpecularDoSLOCAL()
        elif self.cbx_attack_selection.get() == "PowerON - LOCAL":
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
        """
        Questa funzione stoppa l'attacco in corso.
        """
        self.attack.terminate()
        self.btn_stop["state"] = "disabled"
        self.btn_start["state"] = "normal"

    def read_output(self, pipe):
        """
        Questa funzione mostra il terminale dentro il programma in esecuzione.
        """
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
        """
        Questa funzione chiude il programma in esecuzione.
        """
        if self.attack:
            self.attack.terminate()
        self.master.destroy()

root = Tk()
app = App(root)
root.mainloop()

