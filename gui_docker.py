from pymodbus.client import ModbusTcpClient as ModbusClient
from ipaddress import ip_address
import os
from subprocess import Popen, PIPE, STDOUT
from threading import Thread, Event
import time
import tkinter 
from tkinter import ttk
from tkinter import *
import subprocess
import threading
import configparser
import signal
from psutil import process_iter
from signal import SIGTERM # or SIGKILL


class App:
    ATTACK_CMD = ["plc-attack", "-c", "config.ini"]

    MITM_CMD = ["docker", "exec", "-it", "mitm", "python3", "servermitm.py"]

    ATTACKS = {
        "threshold": "attacks/threshold.py",
        "chattering": "attacks/chattering.py",
        "mitm": "servermitm.py",
    }
    
    IP = ["PLC1", "PLC2", "PLC3", "HMI"]

    def __init__(self, master):

        self.selected_count = IntVar()  # Variabile per il conteggio dei checkbox selezionati
        self.selected_count.set(0)  # Inizializza a 0 il conteggio dei checkbox selezionati
        self.condition_combobox_timeout = None

        self.master = master
        self.attack = None

        self.master.title("PLC Attack")
        self.master.rowconfigure(0, minsize=500, weight=1)
        self.master.columnconfigure(0, minsize=1000, weight=1)
        self.master.columnconfigure(1, minsize=300, weight=1)

        self.cmd_frame = Frame(self.master)
        self.cmd_frame.grid(row=0, column=0, sticky="ns")

        self.out_fram = Frame(self.master)
        self.out_fram.grid(row=0, column=1, sticky="nsew")

        self.lbl_title = Label(self.cmd_frame, text="PLC Attack")
        self.lbl_title.grid(row=0, column=0, columnspan=3, sticky="ew", pady=15)

        self.lbl_attack_selection = Label(self.cmd_frame, text="Select attack type")
        self.lbl_attack_selection.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)

        self.cbx_attack_selection = ttk.Combobox(
            self.cmd_frame, values=list(App.ATTACKS.keys()), state="readonly"
        )
        self.cbx_attack_selection.current(0)
        self.cbx_attack_selection.grid(
            row=2, column=0, columnspan=3, sticky="ew", pady=5, padx=20
        )
        self.cbx_attack_selection.bind("<<ComboboxSelected>>", self.on_attack_selection)

        # Checkbox per la PLC da oscurare
        self.dynamic_PLC_obfuscate = Frame(self.cmd_frame)

        self.lbl_dynamic_cbx_ip = Label(self.dynamic_PLC_obfuscate, text="Select PLC to obfuscate")
        self.lbl_dynamic_cbx_ip.grid(row=2, column=0, sticky="ew", pady=5)

        picks = list(App.IP[:-1])
        self.ip_picked = []
        colonna = 1
        for pick in picks:
            colonna += 1 
            var = IntVar()
            chk = Checkbutton(self.dynamic_PLC_obfuscate, text=pick, variable=var, command=lambda var=var: self.update_progressbar_visibility(var))
            chk.grid(row=2, column=colonna, sticky="ew", pady=5)
            self.ip_picked.append((var, chk))
            
        # Checkbox per la PLC da attacare
        self.dynamic_PLC_attack = Frame(self.cmd_frame)

        self.lbl_dynamic_cbx_ip = Label(self.dynamic_PLC_attack, text="Select PLC to attack")
        self.lbl_dynamic_cbx_ip.grid(row=2, column=0, sticky="ew", pady=5)


        picks_attack = list(App.IP)
        self.ip_picked_attack = []
        colonna = 1
        for pick in picks_attack:
            colonna += 1 
            var = IntVar()
            chk = Checkbutton(self.dynamic_PLC_attack, text=pick, variable=var, command=lambda var=var: self.update_checkbox(var))
            chk.grid(row=2, column=colonna, sticky="ew", pady=5)
            self.ip_picked_attack.append((var, chk))

        # Form durata dell'attacco
        self.dynamic_cbx_frame_time = Frame(self.cmd_frame)
        self.lbl_dynamic_cbx_time = Label(self.dynamic_cbx_frame_time, text="Select Time (minutes)").grid(
            row=0, column=0, sticky="ew")
        self.entry_time_condition = Entry(self.dynamic_cbx_frame_time, state="normal")
        self.entry_time_condition.insert(0, 'Insert time in minutes')
        self.entry_time_condition.bind('<FocusIn>', self.on_entry_click_time)
        self.entry_time_condition.bind('<FocusOut>', self.on_focusout_time)
        self.entry_time_condition.config(fg = 'grey')
        self.entry_time_condition.grid(row=0, column=1, sticky="ew", padx=25)
        
        # Form condizione attacco
        self.dynamic_cbx_frame_condition = Frame(self.cmd_frame)
        self.lbl_dynamic_cbx_condition = Label(self.dynamic_cbx_frame_condition, text="Select Condition (levels)").grid(
            row=0, column=0, sticky="ew")
        self.entry_condition = Entry(self.dynamic_cbx_frame_condition, state="normal")
        self.condition_operators = ttk.Combobox(
            self.dynamic_cbx_frame_condition,
            values=["<", ">", "<=", ">=", "==", "!="],
            state="readonly",
            width=3  # Imposta la larghezza della combobox
        )
        self.entry_condition.insert(0, 'Optional')
        self.entry_condition.bind('<FocusIn>', self.on_entry_click_condition)
        self.entry_condition.bind('<FocusOut>', self.on_focusout_condition)
        self.entry_condition.config(fg = 'grey')
        self.entry_condition.grid(row=0, column=1, sticky="ew", padx=10)
        self.condition_operators.current(0)
        #self.condition_operators.bind('<FocusIn>', self.on_entry_click_condition)
        #self.condition_operators.bind('<FocusOut>', self.on_focusout_condition)
        self.condition_operators.grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.condition_operators.grid_propagate(False)
        self.condition_operators.grid_remove() # Nasconde la combobox
        
        # Creazione delle barre di avanzamento per i tank

        self.dynamic_first_pregressbar, self.progress_var1, self.first_status = self.create_progressbar(self.cmd_frame, "Real Level Tank 1")
        self.dynamic_second_pregressbar, self.progress_var2, self.second_status = self.create_progressbar(self.cmd_frame, "Simulated Level Tank 1")
        self.dynamic_third_pregressbar, self.progress_var3, self.third_status = self.create_progressbar(self.cmd_frame, "Real Level Tank 2")
        self.dynamic_fourth_pregressbar, self.progress_var4, self.fourth_status = self.create_progressbar(self.cmd_frame, "Simulated Level Tank 2")
        self.dynamic_fifth_pregressbar, self.progress_var5, self.fifth_status = self.create_progressbar(self.cmd_frame, "Real Level Tank 3")
        self.dynamic_sixth_pregressbar, self.progress_var6, self.sixth_status = self.create_progressbar(self.cmd_frame, "Simulated Level Tank 3")

        self.progress_vars = [self.progress_var1, self.progress_var2, self.progress_var3, self.progress_var4, self.progress_var5, self.progress_var6]
        self.status_list = [self.first_status, self.second_status, self.third_status, self.fourth_status, self.fifth_status, self.sixth_status]

        self.action_frame = Frame(self.cmd_frame)
        self.action_frame.grid(row=3, column=0, columnspan = 3, sticky="ew", pady=5)
        
        # Label "Actions"
        self.lbl_cmd = Label(self.action_frame, text="Actions")
        self.lbl_cmd.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)
        #self.lbl_cmd.grid_configure(ipadx=180)

        self.btn_frame = Frame(self.action_frame)
        self.btn_frame.grid(row=1, column=0, sticky="ew", pady=5)

        # Button "Start attack"
        self.btn_start = Button(self.btn_frame, text="Start attack", command=self.start_main)
        self.btn_start.grid(row=0, column=0, sticky="ew", padx=5)
        
        # Button "Stop attack"
        self.btn_stop = Button(self.btn_frame, text="Stop attack", command=self.stop_attack)
        self.btn_stop["state"] = "disabled"
        self.btn_stop.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Button "Exit"
        self.btn_exit = Button(self.btn_frame, text="Exit", fg="red", command=self.exit)
        self.btn_exit.grid(row=0, column=2, sticky="ew", padx=5)
        
        # Output  
        self.text_box = Text(bg="black", fg="white", state="disabled")
        self.text_box.grid(row=0, column=1, sticky="nsew", pady=20, padx=20)
        self.text_box.tag_configure("stderr", foreground="red")
        self.text_box.tag_configure("stdout", foreground="white")

    def parse_config_file(self,config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        ips = []
        ports = []

        ips.append(config.get("plc1", 'ip_for_tank'))
        ips.append(config.get("plc2", 'ip_for_tank'))
        ips.append(config.get("plc3", 'ip_for_tank'))
        ports.append(config.getint("plc1", 'port_for_tank'))
        ports.append(config.getint("plc2", 'port_for_tank'))
        ports.append(config.getint("plc3", 'port_for_tank'))
        mitm_ip = config.get("MY_IP", 'ip_for_tank')
        mitm_port = config.getint("MY_IP", 'port_for_tank')

        return ips, ports, mitm_ip, mitm_port
    
    def parse_config_file_for_iptables(self,config_file, target1, target2):
        config = configparser.ConfigParser()
        config.read(config_file)

        ips = []

        ips.append(config.get(target1, 'ip'))
        ips.append(config.get(target2, 'ip'))
        ips.append(config.get("MY_IP", 'ip'))

        return ips

    def create_progressbar(self, parent_frame, tank_name):
        progress_var = tkinter.IntVar()
        
        dynamic_pregressbar = Frame(parent_frame)
        
        info_pregressbar = ttk.Label(dynamic_pregressbar, text=tank_name)
        progressbar = ttk.Progressbar(dynamic_pregressbar, 
                                    variable=progress_var,
                                    orient=HORIZONTAL, 
                                    maximum=80, 
                                    length=150,
                                    mode='determinate')
        status_label = ttk.Label(dynamic_pregressbar, text="State: Waiting")
        
        info_pregressbar.grid(row=0, column=0, sticky="ew", pady=15)
        progressbar.grid(row=0, column=1, sticky="ew", padx=8, pady=15)
        status_label.grid(row=0, column=2, sticky="ew", padx=8, pady=15)
        
        return dynamic_pregressbar, progress_var, status_label


    def on_entry_click_condition(self, event):
            if self.entry_condition.cget('fg') == 'grey':
                self.entry_condition.delete(0, "end") # Cancella il testo presente nell'entry
                self.entry_condition.insert(0, '') # Inserisce il testo vuoto nell'entry
                self.entry_condition.config(fg = 'black')
                self.condition_operators.grid(row=0, column=2, sticky="w", padx=(0, 10))
                self.condition_operators.grid_propagate(False)
            
            self.condition_combobox_timeout = threading.Timer(5, self.hide_combobox)
            self.condition_combobox_timeout.start()
    
    def on_focusout_condition(self, event):
        if self.entry_condition.get() == '':
            self.entry_condition.insert(0, 'Optional')
            self.entry_condition.config(fg = 'grey')
            #self.condition_operators.grid_remove() # Nasconde la combobox
        if self.condition_combobox_timeout and self.entry_condition.get() != 'Optional':
            self.condition_combobox_timeout.cancel()
    
    def hide_combobox(self):
        # Nascondi la tendina e reimposta l'entry quando scade il timeout
        if self.entry_condition.get() == '' or self.entry_condition.get() == 'Optional':
            self.condition_operators.grid_remove()
            self.entry_condition.delete(0, "end")
            self.entry_condition.insert(0, 'Optional')
            self.entry_condition.config(fg='grey')
            self.condition_combobox_timeout = None

    def on_entry_click_time(self, event):
            if self.entry_time_condition.cget('fg') == 'grey':
                self.entry_time_condition.delete(0, "end") # Cancella il testo presente nell'entry
                self.entry_time_condition.insert(0, '') # Inserisce il testo vuoto nell'entry
                self.entry_time_condition.config(fg = 'black')
    
    def on_focusout_time(self, event):
        if self.entry_time_condition.get() == '':
            self.entry_time_condition.insert(0, 'Insert time in minutes')
            self.entry_time_condition.config(fg = 'grey')
    
    # Aggiorna la visibilità dei campi in base all'attacco selezionato
    def on_attack_selection(self, event):
        selected_attack = self.cbx_attack_selection.get()
        for (var,chk),(var_attack,chk_attack) in zip(self.ip_picked, self.ip_picked_attack):
            var.set(0)  # Deseleziona tutti i checkbox in caso di cambio attacco
            chk.config(state="normal")  # Riabilita tutti i checkbox
            var_attack.set(0)  # Deseleziona tutti i checkbox in caso di cambio attacco
            chk_attack.config(state="normal")  # Riabilita tutti i checkbox
            self.selected_count.set(0)  # Resetta il conteggio dei checkbox selezionati         
            self.condition_operators.current(0) # Resetta la combobox
            self.entry_condition.delete(0, "end") # Resetta l'entry condition della condizione
            self.entry_condition.insert(0, 'Optional') # Resetta l'entry condition della condizione
            self.entry_condition.config(fg = 'grey') # Resetta il colore dell'entry condition della condizione
            self.condition_operators.grid_remove()  # Nascondi la combobox
            self.entry_time_condition.delete(0, "end") # Resetta l'entry time
            self.entry_time_condition.insert(0, 'Insert time in minutes') # Resetta l'entry time
            self.entry_time_condition.config(fg = 'grey') # Resetta il colore dell'entry time
            self.dynamic_first_pregressbar.grid_forget() # Nascondi la prima barra di avanzamento
            self.dynamic_second_pregressbar.grid_forget() # Nascondi la seconda barra di avanzamento
            self.dynamic_third_pregressbar.grid_forget() # Nascondi la terza barra di avanzamento
            self.dynamic_fourth_pregressbar.grid_forget() # Nascondi la quarta barra di avanzamento
            self.dynamic_fifth_pregressbar.grid_forget() # Nascondi la quinta barra di avanzamento
            self.dynamic_sixth_pregressbar.grid_forget() # Nascondi la sesta barra di avanzamento


        if selected_attack == "mitm":
            self.dynamic_PLC_obfuscate.grid(
                row=3, column=0, columnspan=3, sticky="ew", padx=20, pady=5)
            self.dynamic_PLC_attack.grid(
                row=4, column=0, columnspan=3, sticky="ew", padx=20, pady=5)
            self.dynamic_cbx_frame_time.grid(
                row=5, column=0, columnspan=3, sticky="ew", padx=20, pady=5)
            self.dynamic_cbx_frame_condition.grid(
                row=6, column=0, columnspan=3, sticky="ew", padx=20, pady=5)
            self.action_frame.grid(row=11, column=0, sticky="nsew", padx=50, pady=1)
            self.lbl_cmd.grid(
                row=12, column=0, columnspan=3, sticky="ew", padx=20, pady=5)
            self.btn_frame.grid(row=13)
            self.btn_start.grid(column=0)
            self.btn_stop.grid(column=1)
            self.btn_exit.grid(column=2)
        else:
            self.dynamic_PLC_obfuscate.grid_forget()
            self.dynamic_PLC_attack.grid_forget()
            self.dynamic_cbx_frame_time.grid_forget()
            self.dynamic_cbx_frame_condition.grid_forget()
            self.dynamic_first_pregressbar.grid_forget()
            self.dynamic_second_pregressbar.grid_forget()
            self.dynamic_third_pregressbar.grid_forget()
            self.dynamic_fourth_pregressbar.grid_forget()
            self.dynamic_fifth_pregressbar.grid_forget()
            self.dynamic_sixth_pregressbar.grid_forget()


    # Aggiorna il conteggio dei checkbox selezionati
    def update_checkbox(self, clicked_var, selezione=0):
        self.selected_count.set(0) 
        if clicked_var.get() == 1:
            self.selected_count.set(self.selected_count.get() + 1)
        else:
            self.selected_count.set(self.selected_count.get() - 1)

        if selezione == 1:
            if self.selected_count.get() == 1:
                for var, chk in self.ip_picked:
                    if var.get() == 0:
                        chk.config(state="disabled")
            elif self.selected_count.get() < 1:
                for var, chk in self.ip_picked:
                    chk.config(state="normal")
        else:       
            if self.selected_count.get() == 1:
                for var, chk in self.ip_picked_attack:
                    if var.get() == 0:
                        chk.config(state="disabled")
            elif self.selected_count.get() < 1:
                for var, chk in self.ip_picked_attack:
                    chk.config(state="normal")

    # Aggiorna la visibilità delle barre di avanzamento
    def update_progressbar_visibility(self, var):
        progress_bars = [
            self.dynamic_first_pregressbar,
            self.dynamic_second_pregressbar,
            self.dynamic_third_pregressbar,
            self.dynamic_fourth_pregressbar,
            self.dynamic_fifth_pregressbar,
            self.dynamic_sixth_pregressbar
        ]
        
        self.update_checkbox(var, 1)
        rows, columns = [], []

        picked = False
        for var, _ in self.ip_picked:
            if var.get() == 1:
                picked = True
        
        for idx, ((var, _)) in enumerate(self.ip_picked):
            if var.get() == 1:
                rows.append(progress_bars[2*idx])
                columns.append(0)
                rows.append(progress_bars[(2*idx)+1])
                columns.append(0)
            else:
                if picked:
                    rows.append(progress_bars[2*idx])
                    columns.append(0)

        for index, (row, column) in enumerate(zip(rows, columns)):
            row.grid(row=7 + index, column=column, columnspan=3, sticky="ew", padx=20)
        
        for bar in progress_bars:
            if bar not in rows:
                bar.grid_forget()
        

    # Valori tank
    def get_tank_values(self, progress_var_list, status_label_list, real_addresses, mitm_address, mitm_port, real_port_list, obfuscated_plc):
        time.sleep(15)

        dev_list = App.IP[:-1]
        obfuscated_idx = dev_list.index(obfuscated_plc.upper())

        addr_idx = 0
        client1 = ModbusClient(host=real_addresses[addr_idx], port=real_port_list[addr_idx])
        client1.connect()
        addr_idx += 1
        client2 = ModbusClient(host=real_addresses[addr_idx], port=real_port_list[addr_idx])
        client2.connect()
        addr_idx += 1
        client3 = ModbusClient(host=real_addresses[addr_idx], port=real_port_list[addr_idx])
        client3.connect()

        obf_client = ModbusClient(host=mitm_address, port=mitm_port)
        obf_client.connect()

        while True:
            try:
                # Read values from real plcs
                rd = client1.read_input_registers(0, count=4, slave=0)
                level = rd.registers[0]
                progress_var_list[0].set(level)
                status_label_list[0].config(text=f"State: {level}")
                rd = client2.read_input_registers(0, count=4, slave=0)
                level = rd.registers[0]
                progress_var_list[2].set(level)
                status_label_list[2].config(text=f"State: {level}")
                rd = client3.read_input_registers(0, count=4, slave=0)
                level = rd.registers[0]
                progress_var_list[4].set(level)
                status_label_list[4].config(text=f"State: {level}")

                # Read values from mitm
                rd = obf_client.read_input_registers(0, count=4, slave=0)
                level = rd.registers[0]
                progress_var_list[(obfuscated_idx*2)+1].set(level)
                status_label_list[(obfuscated_idx*2)+1].config(text=f"State: {level}")

                self.master.update_idletasks()
                time.sleep(0.5)
            except Exception as e:
                for pvar, statlab in zip(progress_var_list, status_label_list):
                    pvar.set(0)
                    statlab.config(text="State: Waiting")
                self.btn_stop["state"] = "disabled"
                self.btn_start["state"] = "normal"
                
                client1.close()
                client2.close()
                client3.close()
                obf_client.close()
                break

    def start_main(self):
        attack_key = self.cbx_attack_selection.get()
        if attack_key == "mitm":
            self.start_mitm()
        else:
            self.start_attack()


    def start_mitm(self):
        self.text_box.configure(state="normal")
        self.text_box.insert("end", "Attack started\n")
        self.text_box.see("end")
        self.text_box.configure(state="disabled")
        
        attack_key = self.cbx_attack_selection.get()
        if attack_key == "mitm":
            plc_names = [
                key.lower()
                for (var, chk), key in zip(self.ip_picked, App.IP[:-1])
                if var.get() == 1
            ]
            plc_names = plc_names + [
                key.lower()
                for (var, chk), key in zip(self.ip_picked_attack, App.IP)
                if var.get() == 1
            ]
            
            time_value = self.entry_time_condition.get()
            condition_operator = self.condition_operators.get()
            condition_value = self.entry_condition.get()

            cmd = App.MITM_CMD.copy()
            cmd.extend(["--target"] + plc_names)
            cmd.extend(["--time", time_value])
            #print(["--target"] + plc_names)
            if condition_value != 'Optional':
                cmd.extend(["--condition", condition_operator])
                cmd.extend(["--value", condition_value])
            
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.addresses, self.ports, mitm_ip, mitm_port = self.parse_config_file("config_docker.ini")
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            threadValuesTank = Thread(target=self.get_tank_values, args=(self.progress_vars, self.status_list, self.addresses, mitm_ip, mitm_port, self.ports, plc_names[0]))
            threadValuesTank.start()
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            thread.start()


    def start_attack(self):
        self.text_box.insert("end", "Attack started\n")
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
        self.attack.kill()
        plc_names = [
            key.lower()
            for (var, chk), key in zip(self.ip_picked, App.IP[:-1])
            if var.get() == 1
        ]
        plc_names = plc_names + [
            key.lower()
            for (var, chk), key in zip(self.ip_picked_attack, App.IP)
            if var.get() == 1
        ]
        ips = self.parse_config_file_for_iptables("config_docker.ini", plc_names[0], plc_names[1])
        STOP_CMD = ["docker", "exec", "-it", "mitm", "python3", "stop_attack.py"]
        IPTABLES_DELETE_CMD = ["docker", "exec", "-it", "mitm", 'iptables', '-t', 'nat', '-D', 'PREROUTING', '-i', 'eth0', '-s', ips[1], '-d', ips[0], '-j', 'DNAT', '--to-destination', ips[2]]
        result2 = Popen(STOP_CMD, stdout=PIPE, stderr=STDOUT)
        result3 = Popen(IPTABLES_DELETE_CMD, stdout=PIPE, stderr=STDOUT)

        self.text_box.configure(state="normal")
        self.text_box.insert("end", "Attack stopped\n")
        self.text_box.see("end")
        self.text_box.configure(state="disabled")

        self.btn_stop["state"] = "disabled"
        self.btn_start["state"] = "normal"
        # self.attack.kill()
        # self.btn_stop["state"] = "disabled"
        # self.btn_start["state"] = "normal"


    def read_output(self, pipe):
        while True:
            data = os.read(pipe.fileno(), 1 << 20)
            data = data.replace(b"\r\n", b"\n")
            if data:
                self.text_box.configure(state="normal")
                self.text_box.insert("end", data.decode())
                self.text_box.see("end")
                self.text_box.configure(state="disabled")
            else:
                return None

    def exit(self):
        if self.attack:
            self.attack.kill()
        self.master.destroy()


root = Tk()
app = App(root)
root.mainloop()
