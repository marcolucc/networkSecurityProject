import os
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from tkinter import *
from tkinter import ttk
from attacks import mitm
import subprocess


class App:
    ATTACK_CMD = ["plc-attack", "-c", "config.ini"]

    MITM_CMD = ["python", "-m", "attacks.mitm"]

    ATTACKS = {
        "threshold": "attacks/threshold.py",
        "chattering": "attacks/chattering.py",
        "mitm": "attacks/mitm.py",
    }

    IP = {"PLC1": "127.0.0.1", "PLC2": "127.0.0.1", "PLC3": "127.0.0.1"}

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

        self.cbx_attack_selection = ttk.Combobox(
            self.cmd_frame, values=list(App.ATTACKS.keys()), state="readonly"
        )
        self.cbx_attack_selection.current(0)
        self.cbx_attack_selection.grid(
            row=2, column=0, columnspan=3, sticky="ew", pady=5, padx=20
        )
        self.cbx_attack_selection.bind("<<ComboboxSelected>>", self.on_attack_selection)

        self.dynamic_cbx_frame_ip = Frame(self.cmd_frame)

        self.lbl_dynamic_cbx_ip = Label(self.dynamic_cbx_frame_ip, text="Select PLC")
        self.lbl_dynamic_cbx_ip.pack(side=LEFT, padx=(0, 5))

        picks = list(App.IP.keys())
        self.ip_picked = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self.dynamic_cbx_frame_ip, text=pick, variable=var)
            chk.pack(side=LEFT, anchor=W, expand=YES)
            self.ip_picked.append(var)

        self.dynamic_cbx_frame_time = Frame(self.cmd_frame)

        self.lbl_dynamic_cbx_time = Label(
            self.dynamic_cbx_frame_time, text="Select Time (minutes)"
        )
        self.lbl_dynamic_cbx_time.pack(side=LEFT, padx=(0, 5))

        self.entry_time = Entry(self.dynamic_cbx_frame_time, state="normal")
        self.entry_time.pack(side=LEFT)

        self.action_frame = Frame(self.cmd_frame)
        self.action_frame.grid(row=5, column=0, sticky="ew", padx=5, pady=15)

        self.lbl_cmd = Label(self.action_frame, text="Actions")
        self.lbl_cmd.grid(row=0, column=0, sticky="ew", pady=5)

        self.btn_frame = Frame(self.action_frame)
        self.btn_frame.grid(row=1, column=0, sticky="ew", pady=5)

        self.btn_start = Button(
            self.btn_frame, text="Start attack", command=self.start_main
        )
        self.btn_start.grid(row=0, column=0, sticky="ew", padx=5)
        self.btn_stop = Button(self.btn_frame, text="Stop attack", command=self.stop_attack)
        self.btn_stop["state"] = "disabled"
        self.btn_stop.grid(row=0, column=1, sticky="ew", padx=5)
        self.btn_clear = Button(self.btn_frame, text="Clear", command=self.clear_output)
        self.btn_clear.grid(row=0, column=2, sticky="ew", padx=5)
        self.btn_exit = Button(self.btn_frame, text="Exit", fg="red", command=self.exit)
        self.btn_exit.grid(row=0, column=3, sticky="ew", padx=5)
        

        self.text_box = Text(bg="black", fg="white", state="disabled")
        self.text_box.grid(row=0, column=1, sticky="nsew", pady=20, padx=20)


    def on_attack_selection(self, event):
        selected_attack = self.cbx_attack_selection.get()

        if selected_attack == "mitm":
            self.dynamic_cbx_frame_ip.grid(
                row=3, column=0, columnspan=3, sticky="ew", padx=20, pady=5
            )
            self.dynamic_cbx_frame_time.grid(
                row=4, column=0, columnspan=3, sticky="ew", padx=20, pady=5
            )
        else:
            self.dynamic_cbx_frame_ip.grid_forget()
            self.dynamic_cbx_frame_time.grid_forget()

    def start_main(self):
        attack_key = self.cbx_attack_selection.get()
        if attack_key == "mitm":
            self.start_mitm()
        else:
            self.start_attack()


    def start_mitm(self):
        attack_key = self.cbx_attack_selection.get()
        if attack_key == "mitm":
            ip_addresses = [
                App.IP[key]
                for key, var in zip(App.IP.keys(), self.ip_picked)
                if var.get() == 1
            ]
            plc_names = [
                key.lower()
                for key, var in zip(App.IP.keys(), self.ip_picked)
                if var.get() == 1
            ]
            time_value = self.entry_time.get()

            cmd = App.MITM_CMD.copy()
            cmd.extend(["--plc"] + ip_addresses)
            cmd.extend(["--time", time_value])
            cmd.extend(["--prefix"] + plc_names)

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
                self.text_box.configure(state="normal")
                self.text_box.insert("end", data.decode())
                self.text_box.see("end")
                self.text_box.configure(state="disabled")
            else:
                return None


    def exit(self):
        if self.attack:
            self.attack.terminate()
        self.master.destroy()
    
    def clear_output(self):
    	self.text_box.configure(state="normal")
    	self.text_box.delete("1.0", END)
    	self.text_box.configure(state="disabled")



root = Tk()
app = App(root)
root.mainloop()
