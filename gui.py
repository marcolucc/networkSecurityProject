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
        self.slow_choice = StringVar()
        self.time_ee = StringVar()
        self.coil_values = [IntVar() for _ in range(3)]
        self.trigger_var = IntVar()
        self.trigger_var.set(0)
        
        
        # Create instance variables to store trigger inputs
        self.ip_port_entries = []
        self.conditions = []
        self.trigger_inputs = []
        self.choice_entries = []
        
        self.row_counter = 0

        self.reset_configuration()
        
        
    def start_attack(self):
        
        # Get the selected attack key from the combobox
        attack_key = self.cbx_attack_selection.get()

        self.trigger_var.set(0)
        self.packets_number.set("")
        self.packets_value.set("")
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
            self.optionWindow.geometry("1500x1000")
            self.optionWindow.title("Attack Configuration")
            
            self.display_tutorial()
            self.trigger_var.set(0)

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

            if(self.cbx_attack_selection.get() == "dos"):

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
                
                # Time emptying
                time_emp= Frame(self.optionWindow)
                time_emp.grid(row=self.row_counter, column=0, sticky="w", padx=10, pady=5)

                time_empty_label = Label(time_emp, text="Emptying time")
                time_empty_label.grid(row=0, column=0, sticky="w")

                self.time_empty_entry = Entry(time_emp, textvariable=self.time_ee)
                self.time_empty_entry.grid(row=0, column=1, sticky="w", columnspan=3, padx = 132)

                self.row_counter += 1

                combo_frame = Frame(self.optionWindow)
                combo_frame.grid(row=self.row_counter, column=0, sticky="w", padx=10, pady=5)

                combo_label = Label(combo_frame, text="Select Option:")
                combo_label.grid(row=0, column=0, sticky="w")

                self.combo_var = ttk.Combobox(combo_frame, values=["Slow down time", "Slow down percentage"])
                self.combo_var.grid(row=0, column=1, sticky="w", padx=10)

                # Entry field for value 1 (Slow down time)
                time_label = Label(combo_frame, text="Value:")
                time_label.grid(row=0, column=2, sticky="w")

                self.time_send_entry = Entry(combo_frame, textvariable=self.slow_choice)
                self.time_send_entry.grid(row=0, column=3, sticky="w", padx=10)

                self.row_counter += 1
        
            # Trigger condition checkbox
            trigger_checkbox = Checkbutton(self.optionWindow, text="Enable trigger condition", variable=self.trigger_var, command=self.toggle_trigger_inputs)
            trigger_checkbox.grid(row=self.row_counter, column=0, sticky="we", pady=5)
            self.row_counter += 1

            # Start attack button within the configuration window
            
            start_attack_button = Button(self.optionWindow, text="Start Attack", command=lambda: self.execute_attack(attack_key))
            start_attack_button.grid(column=0, pady=10)
            self.row_counter += 1
            start2_attack_button = Button(self.optionWindow, text="Start Attack with PC", command=lambda: self.execute_previous(attack_key))
            start2_attack_button.grid(column=0, pady=10)
            self.row_counter += 1
            
            # Create the "Add another" button and pack it initially

            self.add_button = Button(self.optionWindow, text="Add another", command=self.add_another_condition)
            
            
            self.row_counter += 3

    
    def new_condition(self):
        for _ in range(1):  # Generate input fields for one coil
            coil_frame = Frame(self.optionWindow)
            coil_frame.grid(row=self.row_counter, column=0, sticky="nsew", pady=5)

            plc_trigger_entry = Entry(coil_frame)
            plc_trigger_entry.grid(row=0, column=0, sticky="nsew")

            device_entry = Entry(coil_frame)
            device_entry.grid(row=0, column=1, sticky="nsew")

            # Dropdown choice for comparison selection
            comparison_choice_var = StringVar()
            comparison_choice_var.set("Select Comparison")
            comparison_choice_menu = OptionMenu(coil_frame, comparison_choice_var, ">", "<", "is", "isnt")
            comparison_choice_menu.grid(row=0, column=2, sticky="nsew")

            # Input field for value
            value_entry = Entry(coil_frame)
            value_entry.grid(row=0, column=3, sticky="nsew")

            # Button to remove this condition
            remove_button = Button(coil_frame, text="Remove Condition", command=lambda frame=coil_frame: self.remove_condition(frame))
            remove_button.grid(row=0, column=4, sticky="nsew")

            self.conditions.append((plc_trigger_entry, device_entry, comparison_choice_var, value_entry))  # Store input field references
            self.trigger_inputs.append((coil_frame, device_entry, comparison_choice_menu, value_entry, plc_trigger_entry, remove_button))  # Store input field references

            self.row_counter += 1
            
            

            # Configure column weights for centering within the coil_frame
            for col in range(5):
                coil_frame.grid_columnconfigure(col, weight=1)


    

    from tkinter import Label, Frame, Entry, OptionMenu, StringVar, Button

    def toggle_trigger_inputs(self):
        if self.trigger_var.get() == 1:
            self.add_button.grid(column=0, row=self.row_counter, pady=5, sticky="w", padx=350)
            self.row_counter += 1
            
            trigger_frame = Frame(self.optionWindow)
            trigger_frame .grid(row=self.row_counter, column=0, sticky="nsew", pady=10)
            # Labels
            self.plc_trigger_label = Label(trigger_frame, text="PLC Trigger")
            self.device_label = Label(trigger_frame, text="Device")
            self.comparison_label = Label(trigger_frame, text="Comparison")
            self.value_label = Label(trigger_frame, text="Value")
            
            self.plc_trigger_label.grid(row=self.row_counter, column=0, sticky="w", padx=(5, 0), pady=5)
            self.device_label.grid(row=self.row_counter, column=1, sticky="w", padx=90, pady=5)
            self.comparison_label.grid(row=self.row_counter, column=2, sticky="w", padx=50, pady=5)
            self.value_label.grid(row=self.row_counter, column=3, sticky="w", padx=50, pady=5)
            self.row_counter += 1
            self.new_condition()
        else:
            # Remove the trigger-related widgets
            for items in self.trigger_inputs:
                coil_frame, comparison_choice_menu, value_entry, plc_trigger_entry, device_entry, remove_button = items
                coil_frame.destroy()
                plc_trigger_entry.destroy()
                comparison_choice_menu.destroy()
                value_entry.destroy()
                remove_button.destroy()

                self.row_counter -= 1

                

            # Clear the list of trigger inputs and hide the "Add another" button
            self.trigger_inputs.clear()
            self.add_button.grid_forget()
            self.plc_trigger_label.grid_forget()
            self.device_label.grid_forget()
            self.comparison_label.grid_forget()
            self.value_label.grid_forget()
            self.row_counter -= 2
            self.optionWindow.update_idletasks()  # Refresh the window layout
            self.trigger_var.set(0)


    def remove_condition(self, frame):
        # Remove the condition and its associated widgets
        for items in self.trigger_inputs:
            if items[0] == frame:
                for widget in items[1:]:  # Skip the first item which is the frame
                    widget.destroy()  # Remove other widgets from the layout
                    
                self.trigger_inputs.remove(items)
                self.row_counter -= 1
                break
    
    def add_another_condition(self):
        self.new_condition()  # Call the existing function to add a new condition
    
    def execute_previous(self, attack_key):

        self.trigger_var.set(0)
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

            if self.ip_port_entries[0].get() == "":                         
                print("ERROR! Missing 1 PLC adress")
                return False

            if self.choice_entries[0].get() == "":
                print("ERROR! Choose at least one coil or input register")
                return False
            
            if( attack_key == "dos" ):
                if(self.packets_number.get() == ""):
                    print("ERROR! Missing packet number")
                    return False

                if(self.packets_value.get() == ""):
                    print("ERROR! Missing packet value")
                    return False
            elif (attack_key == "chattering" ):
                if(self.time_ee.get() == ""):
                    print("ERROR! Missing time value")
                    return False
            

            return True
    



        # Update file config.ini with user's input
        def updateConfig():
            
            # Generate the configuration data
            triggers = []  # To store the trigger conditions
            
            if self.trigger_var.get() == 1:
                for i, (plc_trigger, device, condition_choice, value) in enumerate(self.conditions):
                    plc_trigger_value = plc_trigger.get()
                    device_value = device.get()
                    condition_choice_value = condition_choice.get()
                    value_value = value.get()
                    
                    if plc_trigger_value and device_value and condition_choice_value and value_value:
                        trigger = f"conditions_{i+1} = {plc_trigger_value} {device_value} {condition_choice_value} {value_value}"
                        triggers.append(trigger)

            plc_lines = "\n".join([f"plc{i+1} = {info.get()}" for i, info in enumerate(self.ip_port_entries) if info.get() != ""])
            triggers_str = "\n".join(triggers)

            config_data = (
                "[plc]\n" + plc_lines +
                "\n\n[params]\n" +
                "max-level = 80\n" +
                "min-level = 70\n" +
                "plc1_choice =\n" +
                "plc2_choice =\n" + 
                "plc3_choice =\n" + 
                "packets_number = \n" +
                "packets_value =\n" +
                "time_empty =\n " +
                "time_send =\n" +
                "percentage =\n" +
                triggers_str
            )


            
            with open('config.ini', 'w') as configfile:
                    configfile.write(config_data)
                        
            config = configparser.ConfigParser()
            config.read('config.ini')        
            
            config.set('params', 'plc1_choice', str(self.choice_entries[0].get()))
            config.set('params', 'plc2_choice', str(self.choice_entries[1].get()))
            config.set('params', 'plc3_choice', str(self.choice_entries[2].get()))
            
            #parameters settings
            config.set('params', 'packets_number', self.packets_number.get())
            config.set('params', 'packets_value', self.packets_value.get())

            if(str(self.cbx_attack_selection.get()) == "chattering"):
                config.set('params', 'time_empty', self.time_ee.get())
                if str(self.combo_var.get()) == "Slow down time":
                    config.set('params', 'time_send', self.slow_choice.get())
                    config.set('params', 'percentage', "")
                if str(self.combo_var.get()) == "Slow down percentage":
                    config.set('params', 'time_send', "")
                    config.set('params', 'percentage', self.slow_choice.get())
            
                               
            with open('config.ini', 'w') as configfile:
                    config.write(configfile) 
    
        
        
        # Check input data before executing
        if validateConfig(self) == True:
            updateConfig()

            
            self.reset_configuration()
            # LaunchDos
            print("Launching attack")
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

            self.trigger_var.set(0)
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
        acoil1_label = Label(tutorial, text="c0 (%QX0.0), c1 (%QX0.1), c2 (%QX0.2)")
        acoil1_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)
        self.row_counter += 1
        acoil11_label = Label(tutorial, text="m0 (%MW1), m1 (%MW2)")
        acoil11_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)
        
        self.row_counter += 1
        aplc2_label = Label(tutorial, text="PLC2 - IP 0.0.0.0 - PORT 5021")
        aplc2_label.grid(row=self.row_counter, column=0, sticky="w")
        acoil2_label = Label(tutorial, text="m1 (%MW1), m2 (%MW2)")
        acoil2_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)
        self.row_counter += 1
        aplc3_label = Label(tutorial, text="PLC3 - IP 0.0.0.0 - PORT 5022")
        aplc3_label.grid(row=self.row_counter, column=0, sticky="w")
        acoil3_label = Label(tutorial, text="c1 (%QX0.0), c2 (%QX0.1)")
        acoil3_label.grid(row=self.row_counter, column=3, sticky="w", padx=40)    
        self.row_counter += 4
        separator_label = Label(tutorial, bg="gray", width=95, height=0)
        separator_label.grid(row=self.row_counter, column=0, columnspan=4, pady=5)              
        self.row_counter += 4

    def reset_configuration(self):
        self.trigger_var.set(0)
        self.packets_number.set("")
        self.packets_value.set("")
        self.conditions = []
        
        


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