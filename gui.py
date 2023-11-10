import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import psutil

from threading import Thread
from tkinter import *
from tkinter import ttk

class App:
    ATTACK_CMD = ["plc-attack", "-c", "config.ini"]

    #attackplc.attack:main

    ATTACKS = {
        "dos": "attacks/dos.py",
        "threshold": "attacks/threshold.py",
        "chattering": "attacks/chattering.py"
    }

    #IP = {"PLC1": "0", "PLC2": "0", "PLC3": "0"}

    def __init__(self, master):
        self.master = master
        self.attack = None

        self.pid = self.get_pid_by_process_name('python.exe')

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
        self.btn_config = Button(self.btn_frame, text="Config", fg="cyan", command=self.open_config_window)
        self.btn_config.grid(row=0, column=3, sticky="ew", padx=5)
        self.btn_ip = Button(self.btn_frame, text="IP", fg="green", command=self.open_ip_window)
        self.btn_ip.grid(row=0, column=4, sticky="ew", padx=5)

        self.text_box = Text(bg="black", fg="white", state='disabled')
        self.text_box.grid(row=0, column=1, sticky="nsew", pady=20, padx=20)


    def start_attack(self):
        attack_key = self.cbx_attack_selection.get()
        attack_script_path = App.ATTACKS[attack_key]
        cmd = App.ATTACK_CMD.copy()
        cmd.append(attack_script_path)
        cmd[0] = "python attackplc/attack.py"
        cmd = str(cmd).replace(',', '').replace('[', '').replace(']','').replace("'", "")
        print(cmd)

        self.text_box.delete("0.0", END)
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"
        self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True, encoding = 'utf-8')
        self.thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
        self.thread.start()

    def stop_attack(self):
        self.attack.terminate()
        pid_list = self.get_pid_by_process_name('python.exe')
        #pid_list = get_pid_by_process_name('python3')              UBUTNU
        temp = list(set(pid_list) - set(self.pid))
        subprocess.run(['taskkill', '/f', '/im', str(temp[0])])
        #subprocess.run(['pkill', '-f', str(temp[0])])              UBUNTU
        self.btn_stop["state"] = "disabled"
        self.btn_start["state"] = "normal"

    def read_output(self, pipe):
        while True:
            data = os.read(pipe.fileno(), 1 << 20)
            data = data.replace(b"\r\n", b"\n")
            if data:
                self.text_box.configure(state='normal')
                try:
                    decoded_data = data.decode('utf-8')
                except UnicodeDecodeError:
                    # Se la decodifica UTF-8 fallisce, prova con un'altra codifica
                    decoded_data = data.decode('iso-8859-1', errors='replace')
                self.text_box.insert("end", decoded_data)
                self.text_box.see("end")
                self.text_box.configure(state='disabled')
            else:
                return None
    
    def exit(self):
        if self.attack:
            self.attack.terminate()
        self.master.destroy()

    def open_config_window(self):
        Popen('python config.py', stdout=PIPE, stderr=STDOUT, shell=True, encoding = 'utf-8')

    def open_ip_window(self):
        Popen('python ip.py', stdout=PIPE, stderr=STDOUT, shell=True, encoding = 'utf-8')

    def get_pid_by_process_name(self, process_name):
        process_list = list()
        process = psutil.process_iter()
        for p in process:
            if p.name() == process_name:
                process_list.append(p.pid)
        return process_list


root = Tk()
app = App(root)
root.mainloop()
