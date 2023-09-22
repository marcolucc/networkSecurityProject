import configparser
import os
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from tkinter import *
from tkinter import ttk
import configparser
import tkinter as tk


class App:
    ATTACK_CMD = ["plc-attack", "-c", "config.ini"]

    ATTACKS = {
        "chattering": "attacks/chattering.py",
        "dos": "attacks/dos.py",
        "threshold": "attacks/threshold.py"
    }

    def __init__(self, master):
        self.child = None
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

        self.btn_start = Button(self.btn_frame, text="Start attack", command=self.choose_ui)
        self.btn_start.grid(row=0, column=0, sticky="ew", padx=5)
        self.btn_stop = Button(self.btn_frame, text="Stop attack", command=self.stop_attack)
        self.btn_stop["state"] = "disabled"
        self.btn_stop.grid(row=0, column=1, sticky="ew", padx=5)
        self.btn_exit = Button(self.btn_frame, text="Exit", fg="red", command=self.exit)
        self.btn_exit.grid(row=0, column=2, sticky="ew", padx=5)

        self.text_box = Text(bg="black", fg="white", state='disabled')
        self.text_box.grid(row=0, column=1, sticky="nsew", pady=20, padx=20)

    def choose_ui(self):
        if self.cbx_attack_selection.get() == "chattering":
            self.chattering_ui()
        elif self.cbx_attack_selection.get() == "dos":
            self.dos_ui()
        else:
            self.start_attack()

    def chattering_ui(self):
        # build ui
        self.child = Toplevel(root)

        frame1 = tk.Frame(self.child)
        frame1.configure(height=400, width=400)
        frame4 = ttk.Frame(frame1)
        frame4.configure(height=400, width=400)
        label1 = ttk.Label(frame4)
        label1.configure(text='PLC1')
        label1.grid(column=0, row=1)
        label2 = ttk.Label(frame4)
        label2.configure(text='PLC2')
        label2.grid(column=2, row=1)
        label3 = ttk.Label(frame4)
        label3.configure(text='PLC3')
        label3.grid(column=4, row=1)
        self.plc1_ip = ttk.Entry(frame4)
        self.plc1_ip.grid(column=1, padx=10, row=1)
        self.plc2_ip = ttk.Entry(frame4)
        self.plc2_ip.grid(column=3, padx=10, row=1)
        self.plc3_ip = ttk.Entry(frame4)
        self.plc3_ip.grid(column=5, padx=10, row=1)
        label4 = ttk.Label(frame4)
        label4.configure(text='PLC Addresses')
        label4.grid(column=0, ipady=0, pady=25, row=0)

        label10 = ttk.Label(frame4)
        label10.configure(text='Basic attack - Coils to attack')
        label10.grid(column=0, ipady=0, pady=25, row=2)
        label11 = ttk.Label(frame4)
        label11.configure(text='pumps (%QX0.0)')
        label11.grid(column=0, row=3)
        label12 = ttk.Label(frame4)
        label12.configure(text='valve (%QX0.1)')
        label12.grid(column=0, row=4)
        label13 = ttk.Label(frame4)
        label13.configure(text='Richiesta (%QX0.2)')
        label13.grid(column=0, row=5)
        self.plc1_coil0 = ttk.Checkbutton(frame4)
        self.plc1_coil0_checked = tk.BooleanVar()
        self.plc1_coil0.configure(variable=self.plc1_coil0_checked)
        self.plc1_coil0.grid(column=1, row=3)
        self.plc1_coil1 = ttk.Checkbutton(frame4)
        self.plc1_coil1_checked = tk.BooleanVar()
        self.plc1_coil1.configure(variable=self.plc1_coil1_checked)
        self.plc1_coil1.grid(column=1, row=4)
        self.plc1_coil2 = ttk.Checkbutton(frame4)
        self.plc1_coil2_checked = tk.BooleanVar()
        self.plc1_coil2.configure(variable=self.plc1_coil2_checked)
        self.plc1_coil2.grid(column=1, row=5)
        label15 = ttk.Label(frame4)
        label15.configure(text='request (%QX0.0)')
        label15.grid(column=2, row=3)
        self.plc2_coil0 = ttk.Checkbutton(frame4)
        self.plc2_coil0_checked = tk.BooleanVar()
        self.plc2_coil0.configure(variable=self.plc2_coil0_checked)
        self.plc2_coil0.grid(column=3, row=3)
        label16 = ttk.Label(frame4)
        label16.configure(text='pump (%QX0.0)')
        label16.grid(column=4, row=3)
        label17 = ttk.Label(frame4)
        label17.configure(text='high (%QX0.1)')
        label17.grid(column=4, row=4)
        self.plc3_coil0 = ttk.Checkbutton(frame4)
        self.plc3_coil0_checked = tk.BooleanVar()
        self.plc3_coil0.configure(variable=self.plc3_coil0_checked)
        self.plc3_coil0.grid(column=5, row=3)
        self.plc3_coil1 = ttk.Checkbutton(frame4)
        self.plc3_coil1_checked = tk.BooleanVar()
        self.plc3_coil1.configure(variable=self.plc3_coil1_checked)
        self.plc3_coil1.grid(column=5, row=4)

        label33 = ttk.Label(frame4)
        label33.configure(text='Basic attack - Other options')
        label33.grid(column=0, pady=25, row=6)
        label34 = ttk.Label(frame4)
        label34.configure(text='Chattering interval')
        label34.grid(column=0, row=7)
        self.chattering_interval_text = ttk.Entry(frame4)
        self.chattering_interval_text.grid(column=1, row=7)

        label36 = ttk.Label(frame4)
        label36.configure(text='Delay attack - Target')
        label36.grid(column=0, pady=25, row=12)
        label37 = ttk.Label(frame4)
        label37.configure(text='Delay fill PLC1')
        label37.grid(column=0, row=13)
        self.delay_fill_plc1 = ttk.Checkbutton(frame4)
        self.delay_fill_plc1_checked = tk.BooleanVar()
        self.delay_fill_plc1.configure(variable=self.delay_fill_plc1_checked)
        self.delay_fill_plc1.grid(column=1, row=13)
        label38 = ttk.Label(frame4)
        label38.configure(text='Delay empty PLC1')
        label38.grid(column=0, row=14)
        self.delay_empty_plc1 = ttk.Checkbutton(frame4)
        self.delay_empty_plc1_checked = tk.BooleanVar()
        self.delay_empty_plc1.configure(variable=self.delay_empty_plc1_checked)
        self.delay_empty_plc1.grid(column=1, row=14)
        label39 = ttk.Label(frame4)
        label39.configure(text='Delay empty PLC3')
        label39.grid(column=4, row=13)
        self.delay_empty_plc3 = ttk.Checkbutton(frame4)
        self.delay_empty_plc3_checked = tk.BooleanVar()
        self.delay_empty_plc3.configure(variable=self.delay_empty_plc3_checked)
        self.delay_empty_plc3.grid(column=5, row=13)

        label35 = ttk.Label(frame4)
        label35.configure(text='Delay attack - Other options')
        label35.grid(column=0, ipady=0, pady=25, row=15)
        label40 = ttk.Label(frame4)
        label40.configure(text='Delay tank')
        label40.grid(column=0, row=16)
        delay_percentages = ["", "+25%", "+50%", "+75%", "+100%"]
        self.selected_delay = StringVar(frame4)
        self.tank_delay_menu = ttk.OptionMenu(frame4, self.selected_delay, None, *delay_percentages)
        self.tank_delay_menu.grid(column=1, row=16)

        label5 = tk.Label(frame4)
        label5.configure(state="normal", text='Conditions')
        label5.grid(column=0, pady=25, row=17)
        label19 = tk.Label(frame4)
        label19.configure(text='Coils conditions')
        label19.grid(column=0, row=18)
        label24 = tk.Label(frame4)
        label24.configure(text='Input registers conditions')
        label24.grid(column=3, row=18)
        self.coils_conditions = ttk.Checkbutton(frame4)
        self.coils_conditions_checked = tk.BooleanVar()
        self.coils_conditions.configure(variable=self.coils_conditions_checked)
        self.coils_conditions.grid(column=1, row=18)
        self.input_conditions = ttk.Checkbutton(frame4)
        self.input_conditions_checked = tk.BooleanVar()
        self.input_conditions.configure(variable=self.input_conditions_checked)
        self.input_conditions.grid(column=4, row=18)
        conditions_connection = ["AND", "OR"]
        self.selected_connection = StringVar(frame4)
        self.tank_delay_menu = ttk.OptionMenu(frame4, self.selected_connection, "AND", *conditions_connection)
        self.tank_delay_menu.grid(column=2, row=18)

        self.confirm_button = ttk.Button(frame4)
        self.confirm_button.configure(text='Confirm')
        self.confirm_button.grid(column=5, pady=30, row=19)
        self.confirm_button.configure(command=self.save_input_chattering)
        frame4.grid(column=0, row=0)
        frame1.pack(side="top")

        self.child.mainloop()

    def save_input_chattering(self):
        plc1_ip = self.plc1_ip.get()
        plc2_ip = self.plc2_ip.get()
        plc3_ip = self.plc3_ip.get()

        plc1_coil0_checked = self.plc1_coil0_checked.get()
        plc1_coil1_checked = self.plc1_coil1_checked.get()
        plc1_coil2_checked = self.plc1_coil2_checked.get()
        plc2_coil0_checked = self.plc2_coil0_checked.get()
        plc3_coil0_checked = self.plc3_coil0_checked.get()
        plc3_coil1_checked = self.plc3_coil1_checked.get()
        coils_conditions_checked = self.coils_conditions_checked.get()
        input_conditions_checked = self.input_conditions_checked.get()
        delay_fill_plc1_checked = self.delay_fill_plc1_checked.get()
        delay_empty_plc1_checked = self.delay_empty_plc1_checked.get()
        delay_empty_plc3_checked = self.delay_empty_plc3_checked.get()
        chattering_interval = self.chattering_interval_text.get()
        delay = self.selected_delay.get()
        conditions_connection = self.selected_connection.get()

        config = configparser.ConfigParser(interpolation=None)
        config['plc'] = {
            'plc1': plc1_ip,
            'plc2': plc2_ip,
            'plc3': plc3_ip
        }

        config['plc1 coils to attack'] = {
            'pumps_plc10': plc1_coil0_checked,
            'valve_plc11': plc1_coil1_checked,
            "richiesta_plc12": plc1_coil2_checked,
        }
        config['plc2 coils to attack'] = {
            'request_plc20': plc2_coil0_checked
        }
        config['plc3 coils to attack'] = {
            'pump_plc30': plc3_coil0_checked,
            'high_plc31': plc3_coil1_checked
        }

        config['delay target'] = {
            'fill_plc1': delay_fill_plc1_checked,
            'empty_plc1': delay_empty_plc1_checked,
            'empty_plc3': delay_empty_plc3_checked
        }

        config['other options'] = {
            'chattering_interval': chattering_interval,
            'delay': delay
        }

        config['conditions'] = {
            'coils_conditions': coils_conditions_checked,
            'input_conditions': input_conditions_checked,
            'connection': conditions_connection
        }

        with open('./config.ini', 'w') as configfile:
            config.write(configfile)
            print("Written config.ini")

        self.child.destroy()
        self.start_attack()

    def dos_ui(self):
        # print('preparo la finestra')
        newWindow = Toplevel(root)
        newWindow.geometry("600x600")
        # center_window(newWindow)
        newWindow.title("Attacco Denial of Service")

        etichettaIndirizzo1 = ttk.Label(newWindow, text=" Indirizzo IP PLC da attaccare n°1 [ip:porta]*")
        etichettaIndirizzo2 = ttk.Label(newWindow, text="Indirizzo IP PLC da attaccare n°2 [ip:porta]")
        etichettaIndirizzo3 = ttk.Label(newWindow, text="Indirizzo IP PLC da attaccare n°3 [ip:porta]")
        etichettaCoil = ttk.Label(newWindow, text="Seleziona la coil da attaccare")
        etichettaRegister = ttk.Label(newWindow, text="Seleziona l'holding register da attaccare")
        etichettaTriggers = ttk.Label(newWindow, text="Seleziona i triggers per l'attacco")
        etichettaPacchetto = ttk.Label(newWindow, text="Inserisci un valore per il pacchetto singolo")

        # preparo la selezione per la seconda plc

        etichettaCoil2 = ttk.Label(newWindow, text="Seleziona la coil da attaccare")
        etichettaRegister2 = ttk.Label(newWindow, text="Seleziona l'holding register da attaccare")
        etichettaTriggers2 = ttk.Label(newWindow, text="Seleziona i triggers per l'attacco")
        etichettaPacchetto2 = ttk.Label(newWindow, text="Inserisci un valore per il pacchetto singolo")

        etichettaCoil2.grid(row=12, column=0)
        etichettaRegister2.grid(row=12, column=1)
        etichettaTriggers2.grid(row=16, column=0)

        # preparo la selezione per la terza plc

        etichettaCoil3 = ttk.Label(newWindow, text="Seleziona la coil da attaccare")
        etichettaRegister3 = ttk.Label(newWindow, text="Seleziona l'holding register da attaccare")
        etichettaTriggers3 = ttk.Label(newWindow, text="Selezione i triggers per l'attacco")
        etichettaPacchetto3 = ttk.Label(newWindow, text="Inserisci un valore per il pacchetto singolo")

        etichettaCoil3.grid(row=20, column=0)
        etichettaRegister3.grid(row=20, column=1)
        etichettaTriggers3.grid(row=24, column=0)

        # selezione di coils per plc n. 2
        coil1_check2 = tk.StringVar()
        coil1_button2 = ttk.Checkbutton(newWindow, text="coil1", variable=coil1_check2)
        coil1_button2.grid(row=13, column=0)

        coil2_check2 = tk.StringVar()
        coil2_button2 = ttk.Checkbutton(newWindow, text="coil2", variable=coil2_check2)
        coil2_button2.grid(row=14, column=0)

        coil3_check2 = tk.StringVar()
        coil3_button2 = ttk.Checkbutton(newWindow, text="coil3", variable=coil3_check2)
        coil3_button2.grid(row=15, column=0)

        # selezione di registers per plc n. 2

        register1_check2 = tk.StringVar()
        register1_button2 = ttk.Checkbutton(newWindow, text="MW0", variable=register1_check2)
        register1_button2.grid(row=13, column=1)

        register2_check2 = tk.StringVar()
        register2_button2 = ttk.Checkbutton(newWindow, text="MW1", variable=register2_check2)
        register2_button2.grid(row=14, column=1)

        register3_check2 = tk.StringVar()
        register3_button2 = ttk.Checkbutton(newWindow, text="MW2", variable=register3_check2)
        register3_button2.grid(row=15, column=1)
        
        # selezione valore di DOS coils per plc n. 2
        
        dos_list = ["True", "False"]
        dos_coils_clicked2_1 = tk.StringVar()
        dos_coils_clicked2_1.set('True')
        dos_coils_choice2_1 = OptionMenu(newWindow, dos_coils_clicked2_1, "True", "False")
        dos_coils_choice2_1.grid(row=13, column=2)
        
        dos_coils_clicked2_2 = tk.StringVar()
        dos_coils_clicked2_2.set('True')
        dos_coils_choice2_2 = OptionMenu(newWindow, dos_coils_clicked2_2, "True", "False")
        dos_coils_choice2_2.grid(row=14, column=2)
        
        dos_coils_clicked2_3 = tk.StringVar()
        dos_coils_clicked2_3.set('True')
        dos_coils_choice2_3 = OptionMenu(newWindow, dos_coils_clicked2_3, "True", "False")
        dos_coils_choice2_3.grid(row=15, column=2)
        
        # selezione valore di DOS registri per plc n. 2
        
        campoDosRegister2_1 = ttk.Entry(newWindow, width=5)
        campoDosRegister2_1.grid(row=13, column=3)
        
        campoDosRegister2_2 = ttk.Entry(newWindow, width=5)
        campoDosRegister2_2.grid(row=14, column=3)
        
        campoDosRegister2_3 = ttk.Entry(newWindow, width=5)
        campoDosRegister2_3.grid(row=15, column=3)

        # selezione di triggers per plc n. 2

        trigger_list = ["QW0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF", "QX0.2 ON", "QX0.2 OFF", "none"]
        trigger1_clicked2 = tk.StringVar()
        trigger1_clicked2.set('none')
        trigger_choice1_2 = OptionMenu(newWindow, trigger1_clicked2, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                       "QX0.2 ON", "QX0.2 OFF")
        trigger_choice1_2.grid(row=16, column=1)

        trigger2_clicked2 = tk.StringVar()
        trigger2_clicked2.set('none')
        trigger_choice2_2 = OptionMenu(newWindow, trigger2_clicked2, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                       "QX0.2 ON", "QX0.2 OFF")
        trigger_choice2_2.grid(row=17, column=0)

        trigger3_clicked2 = tk.StringVar()
        trigger3_clicked2.set('none')
        trigger_choice3_2 = OptionMenu(newWindow, trigger3_clicked2, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                       "QX0.2 ON", "QX0.2 OFF")
        trigger_choice3_2.grid(row=17, column=1)

        # invio di pacchetto singolo per plc n. 2

        etichettaPacchetto2.grid(row=18, column=0)
        pacchetto_clicked2 = tk.StringVar()
        pacchetto_clicked2.set('none')
        pacchetto_choice2 = OptionMenu(newWindow, pacchetto_clicked2, "QX0.0", "QX0.1", "QX0.2", "MW0", "MW1", "MW2",
                                       "none")
        pacchetto_choice2.grid(row=19, column=0)
        campoPacchetto2 = ttk.Entry(newWindow)
        campoPacchetto2.grid(row=19, column=1)

        # selezione di coils per plc n. 3
        coil1_check3 = tk.StringVar()
        coil1_button3 = ttk.Checkbutton(newWindow, text="coil1", variable=coil1_check3)
        coil1_button3.grid(row=21, column=0)

        coil2_check3 = tk.StringVar()
        coil2_button3 = ttk.Checkbutton(newWindow, text="coil2", variable=coil2_check3)
        coil2_button3.grid(row=22, column=0)

        coil3_check3 = tk.StringVar()
        coil3_button3 = ttk.Checkbutton(newWindow, text="coil3", variable=coil3_check3)
        coil3_button3.grid(row=23, column=0)

        # selezione di registers per plc n. 3

        register1_check3 = tk.StringVar()
        register1_button3 = ttk.Checkbutton(newWindow, text="MW0", variable=register1_check3)
        register1_button3.grid(row=21, column=1)

        register2_check3 = tk.StringVar()
        register2_button3 = ttk.Checkbutton(newWindow, text="MW1", variable=register2_check3)
        register2_button3.grid(row=22, column=1)

        register3_check3 = tk.StringVar()
        register3_button3 = ttk.Checkbutton(newWindow, text="MW2", variable=register3_check3)
        register3_button3.grid(row=23, column=1)
        
        # selezione valore di DOS coils per plc n. 3
        
        dos_coils_clicked3_1 = tk.StringVar()
        dos_coils_clicked3_1.set('True')
        dos_coils_choice3_1 = OptionMenu(newWindow, dos_coils_clicked3_1, "True", "False")
        dos_coils_choice3_1.grid(row=21, column=2)
        
        dos_coils_clicked3_2 = tk.StringVar()
        dos_coils_clicked3_2.set('True')
        dos_coils_choice3_2 = OptionMenu(newWindow, dos_coils_clicked3_2, "True", "False")
        dos_coils_choice3_2.grid(row=22, column=2)
        
        dos_coils_clicked3_3 = tk.StringVar()
        dos_coils_clicked3_3.set('True')
        dos_coils_choice3_3 = OptionMenu(newWindow, dos_coils_clicked3_3, "True", "False")
        dos_coils_choice3_3.grid(row=23, column=2)
        
        # selezione valore di DOS registri per plc n. 3
        
        campoDosRegister3_1 = ttk.Entry(newWindow, width=5)
        campoDosRegister3_1.grid(row=21, column=3)
        
        campoDosRegister3_2 = ttk.Entry(newWindow, width=5)
        campoDosRegister3_2.grid(row=22, column=3)
        
        campoDosRegister3_3 = ttk.Entry(newWindow, width=5)
        campoDosRegister3_3.grid(row=23, column=3)

        # selezione di triggers per plc n. 3

        trigger_list = ["QW0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF", "QX0.2 ON", "QX0.2 OFF", "none"]
        trigger1_clicked3 = tk.StringVar()
        trigger1_clicked3.set('none')
        trigger_choice1_3 = OptionMenu(newWindow, trigger1_clicked3, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                       "QX0.2 ON", "QX0.2 OFF")
        trigger_choice1_3.grid(row=24, column=1)

        trigger2_clicked3 = tk.StringVar()
        trigger2_clicked3.set('none')
        trigger_choice2_3 = OptionMenu(newWindow, trigger2_clicked3, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                       "QX0.2 ON", "QX0.2 OFF")
        trigger_choice2_3.grid(row=25, column=0)

        trigger3_clicked3 = tk.StringVar()
        trigger3_clicked3.set('none')
        trigger_choice3_3 = OptionMenu(newWindow, trigger3_clicked3, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                       "QX0.2 ON", "QX0.2 OFF")
        trigger_choice3_3.grid(row=25, column=1)

        # invio di pacchetto singolo per plc n. 3

        etichettaPacchetto3.grid(row=26, column=0)
        pacchetto_clicked3 = tk.StringVar()
        pacchetto_clicked3.set('none')
        pacchetto_choice3 = OptionMenu(newWindow, pacchetto_clicked3, "QX0.0", "QX0.1", "QX0.2", "MW0", "MW1", "MW2",
                                       "none")
        pacchetto_choice3.grid(row=27, column=0)
        campoPacchetto3 = ttk.Entry(newWindow)
        campoPacchetto3.grid(row=27, column=1)

        # clicked = StringVar()
        # clicked.set('coil1')
        # drop = OptionMenu(newWindow, clicked, "coil1", "coil2", "coil3", "none")
        # drop.grid(row=4, column=1)
        etichettaCoil.grid(row=4, column=0)

        # clicked_register = StringVar()
        # clicked_register.set('low_1')
        # drop_register = OptionMenu(newWindow, clicked_register, "low_1", "high_1", "none")
        # drop_register.grid(row=5, column=1)

        etichettaRegister.grid(row=4, column=1)

        etichettaTriggers.grid(row=8, column=0)

        etichettaPacchetto.grid(row=10, column=0)

        # aggiungo checkbox per coil al posto di OptionMenu
        coil1_check = tk.StringVar()
        coil1_button = ttk.Checkbutton(newWindow, text="coil1", variable=coil1_check)
        coil1_button.grid(row=5, column=0)

        coil2_check = tk.StringVar()
        coil2_button = ttk.Checkbutton(newWindow, text="coil2", variable=coil2_check)
        coil2_button.grid(row=6, column=0)

        coil3_check = tk.StringVar()
        coil3_button = ttk.Checkbutton(newWindow, text="coil3", variable=coil3_check)
        coil3_button.grid(row=7, column=0)

        # aggiungo checkbox per register al posto di OptionMenu
        register1_check = tk.StringVar()
        register1_button = ttk.Checkbutton(newWindow, text="MW0", variable=register1_check)
        register1_button.grid(row=5, column=1)

        register2_check = tk.StringVar()
        register2_button = ttk.Checkbutton(newWindow, text="MW1", variable=register2_check)
        register2_button.grid(row=6, column=1)

        register3_check = tk.StringVar()
        register3_button = ttk.Checkbutton(newWindow, text="MW2", variable=register3_check)
        register3_button.grid(row=7, column=1)
        
        # selezione valore di DOS coils per plc n. 1
        
        dos_coils_clicked = tk.StringVar()
        dos_coils_clicked.set('True')
        dos_coils_choice = OptionMenu(newWindow, dos_coils_clicked, "True", "False")
        dos_coils_choice.grid(row=5, column=2)
        
        dos_coils_clicked2 = tk.StringVar()
        dos_coils_clicked2.set('True')
        dos_coils_choice2 = OptionMenu(newWindow, dos_coils_clicked2, "True", "False")
        dos_coils_choice2.grid(row=6, column=2)
        
        dos_coils_clicked3 = tk.StringVar()
        dos_coils_clicked3.set('True')
        dos_coils_choice3 = OptionMenu(newWindow, dos_coils_clicked3, "True", "False")
        dos_coils_choice3.grid(row=7, column=2) 
        
        # selezione valore di DOS registri per plc n. 1
        
        campoDosRegister = ttk.Entry(newWindow, width=5)
        campoDosRegister.grid(row=5, column=3)
        
        campoDosRegister2 = ttk.Entry(newWindow, width=5)
        campoDosRegister2.grid(row=6, column=3)
        
        campoDosRegister3 = ttk.Entry(newWindow, width=5)
        campoDosRegister3.grid(row=7, column=3)

        # preparo la scelta delle condizioni

        trigger_list = ["QW0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF", "QX0.2 ON", "QX0.2 OFF", "none"]
        trigger1_clicked = tk.StringVar()
        trigger1_clicked.set('none')
        trigger_choice1 = OptionMenu(newWindow, trigger1_clicked, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                     "QX0.2 ON", "QX0.2 OFF")
        trigger_choice1.grid(row=8, column=1)

        trigger2_clicked = tk.StringVar()
        trigger2_clicked.set('none')
        trigger_choice2 = OptionMenu(newWindow, trigger2_clicked, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                     "QX0.2 ON", "QX0.2 OFF")
        trigger_choice2.grid(row=9, column=0)

        trigger3_clicked = tk.StringVar()
        trigger3_clicked.set('none')
        trigger_choice3 = OptionMenu(newWindow, trigger3_clicked, "QX0.0 ON", "QX0.0 OFF", "QX0.1 ON", "QX0.1 OFF",
                                     "QX0.2 ON", "QX0.2 OFF")
        trigger_choice3.grid(row=9, column=1)

        # invio di pacchetto singolo

        pacchetto_clicked = tk.StringVar()
        pacchetto_clicked.set('none')
        pacchetto_choice = OptionMenu(newWindow, pacchetto_clicked, "QX0.0", "QX0.1", "QX0.2", "MW0", "MW1", "MW2",
                                      "none")
        pacchetto_choice.grid(row=11, column=0)

        campoIndirizzo1 = ttk.Entry(newWindow)
        campoIndirizzo2 = ttk.Entry(newWindow)
        campoIndirizzo3 = ttk.Entry(newWindow)
        campi_testo = [campoIndirizzo1, campoIndirizzo2, campoIndirizzo3]
        campoPacchetto = ttk.Entry(newWindow)
        campoPacchetto.grid(row=11, column=1)
        
        def closeChildWindow(window):
            window.destroy()
        # bottone_attacco = ttk.Button(newWindow, text="Lancia DoS", command=self.start_attack)
        var = tk.IntVar()
        # bottone_attacco = ttk.Button(newWindow, text="Lancia DoS", command=lambda: start_attack(campi_testo))
        bottone_attacco = ttk.Button(newWindow, text="Lancia DoS", command=lambda: var.set(1))
        bottone_indietro = ttk.Button(newWindow, text="Annulla", command=lambda: closeChildWindow(newWindow))

        # Posizionamento dei widget nella griglia
        etichettaIndirizzo1.grid(row=0, column=0, padx=8, pady=4)
        campoIndirizzo1.grid(row=0, column=1, padx=5, pady=4)
        etichettaIndirizzo2.grid(row=1, column=0, padx=8, pady=4)
        campoIndirizzo2.grid(row=1, column=1, padx=5, pady=4)
        etichettaIndirizzo3.grid(row=2, column=0, padx=8, pady=4)
        campoIndirizzo3.grid(row=2, column=1, padx=5, pady=4)
        bottone_indietro.grid(row=3, column=0, padx=5, pady=4)
        bottone_attacco.grid(row=3, column=1, padx=5, pady=4)

        print("waiting to launch...")
        bottone_attacco.wait_variable(var)
        print("done waiting.")

        # scelte per plc n.1

        coil1 = coil1_check.get()
        coil2 = coil2_check.get()
        coil3 = coil3_check.get()

        register1 = register1_check.get()
        register2 = register2_check.get()
        register3 = register3_check.get()
        
        coil_value = dos_coils_clicked.get()
        coil_value2 = dos_coils_clicked2.get()
        coil_value3 = dos_coils_clicked3.get()
        
        register_value = campoDosRegister.get()
        register_value2 = campoDosRegister2.get()
        register_value3 = campoDosRegister3.get()

        trigger1 = trigger1_clicked.get()
        trigger2 = trigger2_clicked.get()
        trigger3 = trigger3_clicked.get()

        pacchetto = campoPacchetto.get()
        target = pacchetto_clicked.get()
        boolean = pacchetto.startswith("T") or pacchetto.startswith("F")
        if (target.startswith("Q") and boolean == False):
            error = tk.messagebox.showerror(title="Error",
                                            message="Valore del pacchetto incompatibile con il bersaglio")
            exit()
        if (target.startswith("M") and not pacchetto.isnumeric()):
            error = tk.messagebox.showerror(title="Error",
                                            message="Valore del pacchetto incompatibile con il bersaglio")
            exit()

            # scelte per plc n.2

        coil1_2 = coil1_check2.get()
        coil2_2 = coil2_check2.get()
        coil3_2 = coil3_check2.get()

        register1_2 = register1_check2.get()
        register2_2 = register2_check2.get()
        register3_2 = register3_check2.get()
        
        coil_value2_1 = dos_coils_clicked2_1.get()
        coil_value2_2 = dos_coils_clicked2_2.get()
        coil_value2_3 = dos_coils_clicked3.get()
        
        register_value2_1 = campoDosRegister2_1.get()
        register_value2_2 = campoDosRegister2_2.get()
        register_value2_3 = campoDosRegister2_3.get()

        trigger1_2 = trigger1_clicked2.get()
        trigger2_2 = trigger2_clicked2.get()
        trigger3_2 = trigger3_clicked2.get()

        pacchetto2 = campoPacchetto2.get()
        target2 = pacchetto_clicked2.get()
        boolean2 = pacchetto2.startswith("T") or pacchetto2.startswith("F")
        if (target2.startswith("Q") and boolean2 == False):
            error2 = tk.messagebox.showerror(title="Error",
                                             message="Valore del pacchetto incompatibile con il bersaglio")
            exit()
        if (target2.startswith("M") and not pacchetto2.isnumeric()):
            error2 = tk.messagebox.showerror(title="Error",
                                             message="Valore del pacchetto incompatibile con il bersaglio")
            exit()

            # scelte per plc n.3

        coil1_3 = coil1_check3.get()
        coil2_3 = coil2_check3.get()
        coil3_3 = coil3_check3.get()

        register1_3 = register1_check3.get()
        register2_3 = register2_check3.get()
        register3_3 = register3_check3.get()
        
        coil_value3_1 = dos_coils_clicked3_1.get()
        coil_value3_2 = dos_coils_clicked3_2.get()
        coil_value3_3 = dos_coils_clicked3_3.get()
        
        register_value3_1 = campoDosRegister3_1.get()
        register_value3_2 = campoDosRegister3_2.get()
        register_value3_3 = campoDosRegister3_3.get()

        trigger1_3 = trigger1_clicked3.get()
        trigger2_3 = trigger2_clicked3.get()
        trigger3_3 = trigger3_clicked3.get()

        pacchetto3 = campoPacchetto3.get()
        target3 = pacchetto_clicked3.get()
        boolean3 = pacchetto3.startswith("T") or pacchetto3.startswith("F")
        if (target3.startswith("Q") and boolean3 == False):
            error3 = tk.messagebox.showerror(title="Error",
                                             message="Valore del pacchetto incompatibile con il bersaglio")
            exit()
        if (target3.startswith("M") and not pacchetto3.isnumeric()):
            error3 = tk.messagebox.showerror(title="Error",
                                             message="Valore del pacchetto incompatibile con il bersaglio")
            exit()

            # selected_coil = clicked.get()
        # print('hai selezionato', selected_coil)

        # selected_register = clicked_register.get()
        # print("hai selezionato il registro", selected_register)

        config = configparser.ConfigParser()
        config.add_section('plc')
        config.set('plc', 'plc1', campi_testo[0].get())
        config.set('plc', 'plc2', campi_testo[1].get())
        config.set('plc', 'plc3', campi_testo[2].get())

        # config.add_section('coil')
        # config.set('coil', 'coil_target', str(selected_coil))

        # config.add_section('register')
        # config.set('register', 'register_target', str(selected_register))

        # scrivo scelte per plc n.1

        config.add_section('coils1')
        config.set('coils1', 'coil1', str(coil1))
        config.set('coils1', 'coil2', str(coil2))
        config.set('coils1', 'coil3', str(coil3))

        config.add_section('registers1')
        config.set('registers1', 'register1', str(register1))
        config.set('registers1', 'register2', str(register2))
        config.set('registers1', 'register3', str(register3))
        
        config.add_section('coil_value1')
        config.set('coil_value1', 'value1', str(coil_value))
        config.set('coil_value1', 'value2', str(coil_value2))
        config.set('coil_value1', 'value3', str(coil_value3))
        
        config.add_section('register_value1')
        config.set('register_value1', 'value1', str(register_value))
        config.set('register_value1', 'value2', str(register_value2))
        config.set('register_value1', 'value3', str(register_value3))

        config.add_section('triggers1')
        config.set('triggers1', 'trigger1', str(trigger1))
        config.set('triggers1', 'trigger2', str(trigger2))
        config.set('triggers1', 'trigger3', str(trigger3))

        config.add_section('pacchetto1')
        config.set('pacchetto1', 'target', str(target))
        config.set('pacchetto1', 'valore', str(pacchetto))

        # scrivo scelte per plc n.2

        config.add_section('coils2')
        config.set('coils2', 'coil1', str(coil1_2))
        config.set('coils2', 'coil2', str(coil2_2))
        config.set('coils2', 'coil3', str(coil3_2))

        config.add_section('registers2')
        config.set('registers2', 'register1', str(register1_2))
        config.set('registers2', 'register2', str(register2_2))
        config.set('registers2', 'register3', str(register3_2))
        
        config.add_section('coil_value2')
        config.set('coil_value2', 'value1', str(coil_value2_1))
        config.set('coil_value2', 'value2', str(coil_value2_2))
        config.set('coil_value2', 'value3', str(coil_value2_3))
        
        config.add_section('register_value2')
        config.set('register_value2', 'value1', str(register_value2_1))
        config.set('register_value2', 'value2', str(register_value2_2))
        config.set('register_value2', 'value3', str(register_value2_3))

        config.add_section('triggers2')
        config.set('triggers2', 'trigger1', str(trigger1_2))
        config.set('triggers2', 'trigger2', str(trigger2_2))
        config.set('triggers2', 'trigger3', str(trigger3_2))

        config.add_section('pacchetto2')
        config.set('pacchetto2', 'target', str(target2))
        config.set('pacchetto2', 'valore', str(pacchetto2))

        # scrivo scelte per plc n.3

        config.add_section('coils3')
        config.set('coils3', 'coil1', str(coil1_3))
        config.set('coils3', 'coil2', str(coil2_3))
        config.set('coils3', 'coil3', str(coil3_3))

        config.add_section('registers3')
        config.set('registers3', 'register1', str(register1_3))
        config.set('registers3', 'register2', str(register2_3))
        config.set('registers3', 'register3', str(register3_3))
        
        config.add_section('coil_value3')
        config.set('coil_value3', 'value1', str(coil_value3_1))
        config.set('coil_value3', 'value2', str(coil_value3_2))
        config.set('coil_value3', 'value3', str(coil_value3_3))
        
        config.add_section('register_value3')
        config.set('register_value3', 'value1', str(register_value3_1))
        config.set('register_value3', 'value2', str(register_value3_2))
        config.set('register_value3', 'value3', str(register_value3_3))

        config.add_section('triggers3')
        config.set('triggers3', 'trigger1', str(trigger1_3))
        config.set('triggers3', 'trigger2', str(trigger2_3))
        config.set('triggers3', 'trigger3', str(trigger3_3))

        config.add_section('pacchetto3')
        config.set('pacchetto3', 'target', str(target3))
        config.set('pacchetto3', 'valore', str(pacchetto3))

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        attack_key = self.cbx_attack_selection.get()
        attack_script_path = App.ATTACKS[attack_key]
        cmd = App.ATTACK_CMD.copy()
        cmd.append(attack_script_path)
        self.text_box.delete("0.0", END)
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"
        self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        thread = Thread(target=self.read_output, args=(self.attack.stdout,))
        thread.start()

    def start_attack(self):
        attack_key = self.cbx_attack_selection.get()

        attack_script_path = App.ATTACKS[attack_key]
        cmd = App.ATTACK_CMD.copy()
        cmd.append(attack_script_path)

        self.text_box.delete("0.0", END)
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"
        self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        thread = Thread(target=self.read_output, args=(self.attack.stdout,))
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
