import os
import configparser
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from tkinter import *
from tkinter import ttk

class App:
    ATTACK_CMD = ["plc-attack", "-c", "config.ini"]

    ATTACKS = {
        "threshold": "attacks/threshold.py",
        "dos": "attacks/dos.py",
        "chattering": "attacks/chattering.py"
    }

    def __init__(self, master):
        self.master = master
        self.attack = None
        self.cmd = []

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

        
        # Create instance variables to store user inputs
        self.ip_port_value = StringVar()
        self.packets_number = StringVar()
        self.packets_value = StringVar()
        self.time_s = StringVar()
        self.time_e = StringVar()
        self.coil_values = [IntVar() for _ in range(3)]
        self.trigger_var = IntVar()
        
        # Create instance variables to store trigger inputs
        self.ip_port_entries = []
        self.conditions = []
        self.trigger_inputs = []
        self.choice_entries = []
        
        self.row_counter = 0
        
        
    def start_attack(self):
        
        # Get the selected attack key from the combobox
        attack_key = self.cbx_attack_selection.get()
        #print(attack_key)

        if(self.cbx_attack_selection.get() == "threshold"):
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
        else:

            # Create a new window for the attack configuration
            self.optionWindow = Toplevel(root)
            self.optionWindow.geometry("780x1000")
            self.optionWindow.title("Attack Configuration")
            
            self.display_tutorial()

            # IP and PORT inputs
            ip_port_entries = []
            choice_entries = []

            for _ in range(3):
                ip_port_frame = Frame(self.optionWindow)
                ip_port_frame.grid(row=self.row_counter, column=0, sticky="w")

                ip_port_label = Label(ip_port_frame, text="Insert PLC IP and PORT (ip:port):")
                ip_port_label.grid(row=0, column=0, padx=10, pady=5)

                ip_port_entry = Entry(ip_port_frame)
                ip_port_entry.grid(row=0, column=1, padx=10, pady=5)

                choice_label = Label(ip_port_frame, text="Insert coil or register:")
                choice_label.grid(row=0, column=2, padx=10, pady=5)

                choice_entry = Entry(ip_port_frame)
                choice_entry.grid(row=0, column=3, padx=10, pady=5)


                ip_port_entries.append(ip_port_entry)
                choice_entries.append(choice_entry)

                self.row_counter += 1
            
            # Populate ip_port_entries after creating Entry elements
            self.ip_port_entries = ip_port_entries
            self.choice_entries = choice_entries

            # Number of packets to send input
            packets1_frame = Frame(self.optionWindow)
            packets1_frame.grid(row=self.row_counter, column=0, sticky="w", padx=10, pady=5)

            packets_number_label = Label(packets1_frame, text="How many packets to send?")
            packets_number_label.grid(row=0, column=0, sticky="w")

            self.packets_number_entry = Entry(packets1_frame, textvariable=self.packets_number)
            self.packets_number_entry.grid(row=0, column=1, sticky="w", columnspan=3, padx=43)

            self.row_counter += 1

            # Value of packets to send input
            packets_frame = Frame(self.optionWindow)
            packets_frame.grid(row=self.row_counter, column=0, sticky="w", padx=10, pady=5)

            packets_label = Label(packets_frame, text="Set the value of packets")
            packets_label.grid(row=0, column=0, sticky="w")
        
            self.packets_entry = Entry(packets_frame, textvariable=self.packets_value)
            self.packets_entry.grid(row=0, column=1, sticky="w", padx=68)

            self.row_counter += 1

            if(self.cbx_attack_selection.get() == "chattering"):
                # Time between 2 packets
                time_send = Frame(self.optionWindow)
                time_send.grid(row=self.row_counter, column=0, sticky="w", padx=10, pady=5)

                time_label = Label(time_send, text="How much time between 2 packets?")
                time_label.grid(row=0, column=0, sticky="w")

                self.time_send_entry = Entry(time_send, textvariable=self.time_s)
                self.time_send_entry.grid(row=0, column=1, sticky="w", columnspan=3)

                self.row_counter += 1

                # Emptying time
                time_empty = Frame(self.optionWindow)
                time_empty.grid(row=self.row_counter, column=0, sticky="w", padx=5, pady=5)

                time2_label = Label(time_empty, text="Enter the percentage to slow down the emptying time")
                time2_label.grid(row=0, column=0, sticky="w")

                self.time_empty_entry = Entry(time_empty, textvariable=self.time_e)
                self.time_empty_entry.grid(row=0, column=1, sticky="w", columnspan=3)

                self.row_counter += 1
        
            # Trigger condition checkbox
            trigger_checkbox = Checkbutton(self.optionWindow, text="Enable trigger condition", variable=self.trigger_var, command=self.toggle_trigger_inputs)
            trigger_checkbox.grid(row=self.row_counter, column=0, sticky="we", pady=5)
            self.row_counter += 1

            # Start attack button within the configuration window
            
            start_attack_button = Button(self.optionWindow, text="Start Attack", command=lambda: self.execute_attack(attack_key))
            start_attack_button.grid(column=0, pady=10, sticky="nsew")
            self.row_counter += 1
            start2_attack_button = Button(self.optionWindow, text="Start Attack with PC", command=lambda: self.execute_previous(attack_key))
            start2_attack_button.grid(column=0, pady=10, sticky="nsew")
            self.row_counter += 1
            
            # Create the "Add another" button and pack it initially
            self.add_button = Button(self.optionWindow, text="Add another", command=self.add_another_condition)

    
    def new_condition(self):
        for _ in range(1):  # Generate input fields for one coil
            coil_frame = Frame(self.optionWindow)
            coil_frame.grid(row=self.row_counter, column=0, sticky="nsew", pady=10)

            # Dropdown choice for PLC selection
            plc_choice_var = StringVar()
            plc_choice_var.set("Select PLC")
            plc_choice_menu = OptionMenu(coil_frame, plc_choice_var, "level plc 1", "level plc 2", "level plc 3")
            plc_choice_menu.grid(row=0, column=0, sticky="nsew", padx=10)

            # Dropdown choice for comparison selection
            comparison_choice_var = StringVar()
            comparison_choice_var.set("Select Comparison")
            comparison_choice_menu = OptionMenu(coil_frame, comparison_choice_var, ">", "<")
            comparison_choice_menu.grid(row=0, column=1, sticky="nsew")

            # Input field for value
            value_entry = Entry(coil_frame)
            value_entry.grid(row=0, column=2, sticky="nsew")

            # Button to remove this condition
            remove_button = Button(coil_frame, text="Remove Condition", command=lambda frame=coil_frame: self.remove_condition(frame))
            remove_button.grid(row=0, column=3, sticky="nsew")

            self.conditions.append((plc_choice_var, comparison_choice_var, value_entry))  # Store input field references
            self.trigger_inputs.append((coil_frame, plc_choice_menu, comparison_choice_menu, value_entry, remove_button))  # Store input field references

            self.row_counter += 1

            # Configure column weights for centering within the coil_frame
            for col in range(4):
                coil_frame.grid_columnconfigure(col, weight=1)

    

    from tkinter import Label, Frame, Entry, OptionMenu, StringVar, Button

    def toggle_trigger_inputs(self):
        if self.trigger_var.get() == 1:
            self.add_button.grid(column=0, row=self.row_counter, pady=10, sticky="w", padx=350)
            self.row_counter += 1
            self.new_condition()
        else:
            # Remove the trigger-related widgets
            for items in self.trigger_inputs:
                coil_frame, plc_choice_menu, comparison_choice_menu, value_entry, remove_button = items
                coil_frame.destroy()
                plc_choice_menu.destroy()
                comparison_choice_menu.destroy()
                value_entry.destroy()
                remove_button.destroy()

            # Clear the list of trigger inputs and hide the "Add another" button
            self.trigger_inputs.clear()
            self.add_button.grid_forget()
            self.row_counter -= 2
            self.optionWindow.update_idletasks()  # Refresh the window layout


    def remove_condition(self, frame):
        # Remove the condition and its associated widgets
        for items in self.trigger_inputs:
            if items[0] == frame:
                for widget in items[1:]:  # Skip the first item which is the frame
                    widget.destroy()  # Remove other widgets from the layout
                self.trigger_inputs.remove(items)
                break
    
    def add_another_condition(self):
        self.new_condition()  # Call the existing function to add a new condition
    
    def execute_previous(self, attack_key):
        # LaunchDos
        print("Launching Dos with PC")
        self.optionWindow.destroy() 
        attack_key = self.cbx_attack_selection.get()
        attack_script_path = App.ATTACKS[attack_key]
        cmd = App.ATTACK_CMD.copy()
        cmd.append(attack_script_path)
        self.text_box.delete("0.0", END)
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"
        self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
        print("Launching done")
        thread.start()


    def execute_attack(self, attack_key):
    
        def validateConfig(self):
            #Fields to be validated: ip_port_value, coil selected >=1, packets_value (>=1 or loop), trigger values

            """
            # Print the data entered by the user in the text fields
            for entry in self.ip_port_entries:
                print("PLC IP and PORT:", entry.get())

            # Print the values from the checkboxes
            selected_coils = [coil_label for coil_label, coil_var in zip(["coil1", "coil2", "coil3"], self.coil_values) if coil_var.get()]
            print("Selected Coils:", ", ".join(selected_coils))

            print("Packets to send:", self.packets_number.get())
            print("Value to send:", self.packets_value.get())
            

            # Print the values from the trigger inputs, if applicable   
            print("Trigger conditions:")
            for plc_var, comparison_var, value_entry in self.conditions:
                plc_value = plc_var.get()
                comparison_value = comparison_var.get()
                value = value_entry.get()
                print(f"PLC: {plc_value}, Comparison: {comparison_value}, Value: {value}")
            """
            if self.ip_port_entries[0].get() == "":                         
                print("ERROR! Missing 1 PLC adress")
                return False

            if self.choice_entries[0].get() == "":
                print("ERROR! Choose at least one coil or input register")
                return False
            
            if(self.packets_number.get() == ""):
                print("ERROR! Missing packet number")
                return False

            if(self.packets_value.get() == ""):
                print("ERROR! Missing packet value")
                return False
            

            return True
        
        def resetConfig(config):
            # Settings all plcs and params to empty strings
            config.set('plc', 'plc1', "0.0.0.0:5023")
            config.set('plc', 'plc2', "0.0.0.0:5022")
            config.set('plc', 'plc3', "0.0.0.0:5021")

            config.set('params', 'plc1_choice', "")
            config.set('params', 'plc2_choice', "")
            config.set('params', 'plc3_choice', "")
            config.set('params', 'packets_number', "")
            config.set('params', 'packets_value', "")

            config.set('params', 'coil1_sup_limit', "")
            config.set('params', 'coil1_inf_limit', "")
            config.set('params', 'coil2_sup_limit', "")
            config.set('params', 'coil2_inf_limit', "")
            config.set('params', 'coil3_sup_limit', "")
            config.set('params', 'coil3_inf_limit', "")



        # Update file config.ini with user's input
        def updateConfig(): 
            config = configparser.ConfigParser()
            config.read('config.ini')

            resetConfig(config)

            config.set('plc', 'plc1', self.ip_port_entries[0].get())
            if self.ip_port_entries[1].get() != "":
                config.set('plc', 'plc2', self.ip_port_entries[1].get())
            if self.ip_port_entries[2].get() != "":
                config.set('plc', 'plc2', self.ip_port_entries[2].get())

            #parameters settings
            config.set('params', 'plc1_choice', str(self.choice_entries[0].get()))
            config.set('params', 'plc2_choice', str(self.choice_entries[1].get()))
            config.set('params', 'plc3_choice', str(self.choice_entries[2].get()))
            config.set('params', 'packets_number', self.packets_number.get())
            config.set('params', 'packets_value', self.packets_value.get())
            
            # Write triggers input
            for plc_var, comparison_var, value_entry in self.conditions:
                if(plc_var.get() == "level plc 1"):
                    if(comparison_var.get() == ">"):
                        config.set('params', 'coil1_sup_limit', value_entry.get())
                    else:
                        config.set('params', 'coil1_inf_limit', value_entry.get())

                elif(plc_var.get() == "level plc 2"):
                    if(comparison_var.get() == ">"):
                        config.set('params', 'coil2_sup_limit', value_entry.get())
                    else:
                        config.set('params', 'coil2_inf_limit', value_entry.get())

                elif(plc_var.get() == "level plc 3"):
                    if(comparison_var.get() == ">"):
                        config.set('params', 'coil3_sup_limit', value_entry.get())
                    else:
                        config.set('params', 'coil3_inf_limit', value_entry.get())

            
            with open('config.ini', 'w') as configfile:
                    config.write(configfile) 
    
        # Check input data before executing
        if validateConfig(self) == True:
            updateConfig()
            
            # LaunchDos
            print("Launching Dos")
            self.optionWindow.destroy() 
            attack_key = self.cbx_attack_selection.get()
            attack_script_path = App.ATTACKS[attack_key]
            cmd = App.ATTACK_CMD.copy()
            cmd.append(attack_script_path)
            self.text_box.delete("0.0", END)
            self.btn_start["state"] = "disabled"
            self.btn_stop["state"] = "normal"
            self.attack = Popen(cmd, stdout=PIPE, stderr=STDOUT)
            thread = Thread(target=self.read_output, args=(self.attack.stdout, ))
            print("Launching done")
            thread.start()
            
    def display_tutorial(self):
        tutorial= Frame(self.optionWindow)
        tutorial.grid(row=self.row_counter, column=0, sticky="w", padx=10, pady=5)
        aplc_label = Label(tutorial, text="PLCs available")
        aplc_label.grid(row=self.row_counter, column=0, sticky="w")
        acoil_label = Label(tutorial, text="Available c/r")
        acoil_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)
        self.row_counter += 1
        aplc1_label = Label(tutorial, text="PLC1 - IP 0.0.0.0 - PORT 5023")
        aplc1_label.grid(row=self.row_counter, column=0, sticky="w")
        acoil1_label = Label(tutorial, text="c1 (%QX0.0), c2 (%QX.1), c3 (%QX.2)")
        acoil1_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)
        self.row_counter += 1
        acoil11_label = Label(tutorial, text="r1 (%MX0.0), r2 (%MX0.1), r3 (%QX.3), r4 (%QX.4), m1 (%MW0), m2 (%MW0)")
        acoil11_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)
        
        self.row_counter += 1
        aplc2_label = Label(tutorial, text="PLC2 - IP 0.0.0.0 - PORT 5022")
        aplc2_label.grid(row=self.row_counter, column=0, sticky="w")
        acoil2_label = Label(tutorial, text="c1 (%QX0.0), r1 (%MX0.0), r2 (%MX0.1), m1 (%MW1), m2 (%MW2)")
        acoil2_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)
        self.row_counter += 1
        aplc3_label = Label(tutorial, text="PLC3 - IP 0.0.0.0 - PORT 5021")
        aplc3_label.grid(row=self.row_counter, column=0, sticky="w")
        acoil3_label = Label(tutorial, text="c1 (%QX0.0), c2 (%QX0.1)")
        acoil3_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)    
        self.row_counter += 4
        separator_label = Label(tutorial, bg="gray", width=95, height=0)
        separator_label.grid(row=self.row_counter, column=0, columnspan=4, pady=5)              
        self.row_counter += 4

    

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
