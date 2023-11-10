import os
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from tkinter import *
from tkinter import ttk
import configparser


class App:
    ATTACK_CMD = ["plc-attack", "-c", "config.ini"]

    ATTACKS = {
        "threshold": "attacks/threshold.py",
        "chattering": "attacks/chattering.py",
        "dos": "attacks/dos.py"
    }

    def __init__(self, master):
        self.master = master
        self.attack = None
        self.popup = None

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

        self.btn_start = Button(self.btn_frame, text="Start attack", command=self.show_config_and_start)
        self.btn_start.grid(row=0, column=0, sticky="ew",padx=5)
        self.btn_stop = Button(self.btn_frame, text="Stop attack", command=self.stop_attack)
        self.btn_stop["state"] = "disabled"
        self.btn_stop.grid(row=0, column=1, sticky="ew",padx=5)
        self.btn_exit = Button(self.btn_frame, text="Exit", fg="red", command=self.exit)
        self.btn_exit.grid(row=0, column=2, sticky="ew", padx=5)

        self.text_box = Text(bg="black", fg="white", state='disabled')
        self.text_box.grid(row=0, column=1, sticky="nsew", pady=20, padx=20)

        # plc variables in dos windows
        self.plc1_use = StringVar()
        self.plc1_regs = StringVar()
        self.plc1_coil = StringVar()
        self.plc1_trig = StringVar()

        self.plc2_use = StringVar()
        self.plc2_regs = StringVar()
        self.plc2_coil = StringVar()
        self.plc2_trig = StringVar()

        self.plc3_use = StringVar()
        self.plc3_regs = StringVar()
        self.plc3_coil = StringVar()
        self.plc3_trig = StringVar()

        self.packets = StringVar()
        self.value_p = StringVar()

    def show_config_and_start(self):
        attack_key = self.cbx_attack_selection.get()

        # composing a popup to allow the user to configure the attack
        if attack_key == 'dos':
            self.show_dos_config()
        elif attack_key == 'chattering':
            self.start_attack()
        elif attack_key == 'threshold':
            self.start_attack()

    def start_attack(self):
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

    # function that shows a graphical popup to allow setting the attack configuration
    def show_dos_config(self):
        self.popup = Toplevel(self.master)
        self.popup.title("Attack configuration")

        #
        # geometry of popup window
        window_width = 600
        window_height = 400
        center_x = int(self.popup.winfo_screenwidth() / 2 - window_width / 2)
        center_y = int(self.popup.winfo_screenheight() / 2 - window_height / 2)
        self.popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # grid configuration
        self.popup.columnconfigure(0, weight=1)
        self.popup.columnconfigure(1, weight=1)
        self.popup.columnconfigure(2, weight=1)

        # show title label
        title_label = ttk.Label(self.popup, text="CONFIGURE YOUR ATTACK", font=('Helvetica', 15, 'bold'))
        title_label.grid(column=0, row=0, columnspan=3, ipadx=10, ipady=20)
        separator = ttk.Separator(self.popup, orient='horizontal')
        separator.grid(column=0, row=1, columnspan=3, sticky=EW)

        # show plc1 labels
        plc1_label = ttk.Label(self.popup, text="PLC1", font=('Helvetica', 12, 'bold'))
        plc1_label.grid(column=0, row=2, ipadx=10, ipady=10)
        plc1_checkbox = ttk.Checkbutton(self.popup, text="Attack", variable=self.plc1_use, onvalue="True", offvalue="False")
        plc1_checkbox.grid(column=0, row=3)

        plc1_regs_label = ttk.Label(self.popup, text="Target registers:")
        plc1_regs_label.grid(column=0, row=4)
        plc1_regs_entry = ttk.Entry(self.popup, textvariable=self.plc1_regs)
        plc1_regs_entry.grid(column=0, row=5)

        plc1_coils_label = ttk.Label(self.popup, text="Target coils:")
        plc1_coils_label.grid(column=0, row=6)
        plc1_coils_entry = ttk.Entry(self.popup, textvariable=self.plc1_coil)
        plc1_coils_entry.grid(column=0, row=7)

        plc1_trigs_label = ttk.Label(self.popup, text="Triggers:")
        plc1_trigs_label.grid(column=0, row=8)
        plc1_trigs_entry = ttk.Entry(self.popup, textvariable=self.plc1_trig)
        plc1_trigs_entry.grid(column=0, row=9)

        # show plc2 labels
        plc2_label = ttk.Label(self.popup, text="PLC2", font=('Helvetica', 12, 'bold'))
        plc2_label.grid(column=1, row=2, ipadx=10, ipady=10)
        plc2_checkbox = ttk.Checkbutton(self.popup, text="Attack", variable=self.plc2_use, onvalue="True", offvalue="False")
        plc2_checkbox.grid(column=1, row=3)

        plc2_regs_label = ttk.Label(self.popup, text="Target registers:")
        plc2_regs_label.grid(column=1, row=4)
        plc2_regs_entry = ttk.Entry(self.popup, textvariable=self.plc2_regs)
        plc2_regs_entry.grid(column=1, row=5)

        plc2_coils_label = ttk.Label(self.popup, text="Target coils:")
        plc2_coils_label.grid(column=1, row=6)
        plc2_coils_entry = ttk.Entry(self.popup, textvariable=self.plc2_coil)
        plc2_coils_entry.grid(column=1, row=7)

        plc2_trigs_label = ttk.Label(self.popup, text="Triggers:")
        plc2_trigs_label.grid(column=1, row=8)
        plc2_trigs_entry = ttk.Entry(self.popup, textvariable=self.plc2_trig)
        plc2_trigs_entry.grid(column=1, row=9)

        # show plc3 labels
        plc3_label = ttk.Label(self.popup, text="PLC3", font=('Helvetica', 12, 'bold'))
        plc3_label.grid(column=2, row=2, ipadx=10, ipady=10)
        plc3_checkbox = ttk.Checkbutton(self.popup, text="Attack", variable=self.plc3_use, onvalue="True", offvalue="False")
        plc3_checkbox.grid(column=2, row=3)

        plc3_regs_label = ttk.Label(self.popup, text="Target registers:")
        plc3_regs_label.grid(column=2, row=4)
        plc3_regs_entry = ttk.Entry(self.popup, textvariable=self.plc3_regs)
        plc3_regs_entry.grid(column=2, row=5)

        plc3_coils_label = ttk.Label(self.popup, text="Target coils:")
        plc3_coils_label.grid(column=2, row=6)
        plc3_coils_entry = ttk.Entry(self.popup, textvariable=self.plc3_coil)
        plc3_coils_entry.grid(column=2, row=7)

        plc3_trigs_label = ttk.Label(self.popup, text="Triggers:")
        plc3_trigs_label.grid(column=2, row=8)
        plc3_trigs_entry = ttk.Entry(self.popup, textvariable=self.plc3_trig)
        plc3_trigs_entry.grid(column=2, row=9)

        # packet info labels
        pi_frame = ttk.Frame(self.popup)
        pi_frame.grid(column=0, row=10, columnspan=3, padx=20, pady=20, sticky=W)
        pi_frame.columnconfigure(0, weight=1)
        pi_frame.columnconfigure(1, weight=3)

        packets_label = ttk.Label(pi_frame, text="N. of packets:")
        packets_label.grid(column=0, row=0, sticky=E)
        packets_entry = ttk.Entry(pi_frame, textvariable=self.packets)
        packets_entry.grid(column=1, row=0)

        value_label = ttk.Label(pi_frame, text="Value of packets:")
        value_label.grid(column=0, row=1, sticky=E)
        value_entry = ttk.Entry(pi_frame, textvariable=self.value_p)
        value_entry.grid(column=1, row=1)

        # show start button
        start_button = ttk.Button(self.popup, text="Save and start", command=self.dos_start_button_clicked)
        start_button.grid(column=1, row=11, padx=10, pady=10)

    # function that saves the dos configuration and starts the attack
    def dos_start_button_clicked(self):
        config = configparser.ConfigParser()
        config.read('attack_config.ini')
        config.sections()

        config["plc1"]["use"] = 'False' if self.plc1_use.get() == "" else self.plc1_use.get()
        config["plc1"]["registers"] = self.plc1_regs.get()
        config["plc1"]["coils"] = self.plc1_coil.get()
        config["plc1"]["triggers"] = self.plc1_trig.get()

        config["plc2"]["use"] = 'False' if self.plc2_use.get() == "" else self.plc2_use.get()
        config["plc2"]["registers"] = self.plc2_regs.get()
        config["plc2"]["coils"] = self.plc2_coil.get()
        config["plc2"]["triggers"] = self.plc2_trig.get()

        config["plc3"]["use"] = 'False' if self.plc3_use.get() == "" else self.plc3_use.get()
        config["plc3"]["registers"] = self.plc3_regs.get()
        config["plc3"]["coils"] = self.plc3_coil.get()
        config["plc3"]["triggers"] = self.plc3_trig.get()

        config["general"]["packet_number"] = self.packets.get()
        config["general"]["packet_value"] = self.value_p.get()

        # write new configuration in attack_config.ini
        with open('attack_config.ini', 'w') as file_to_write:
            config.write(file_to_write)

        # close the popup window and start attack
        self.popup.destroy()
        self.start_attack()


root = Tk()
app = App(root)
root.mainloop()
