# networkSecurityProject
 
### Introduzione
This project demonstrates a DoS attack on a PLC system.

### Configurazione
Before launching the DoS program, you need to configure:
1. IP addresses and ports of the PLC
2. Sending packets for the DoS
3. Conditions for starting the attack

#### IP and ports
To configure the IP addresses and ports of the PLC, click the <b>IP</b> button in the graphical interface. A window will open where you can enter and/or modify these parameters.
#### Packets and conditions
To configure the content of the packets and which PLCs to target with the attack, click the <b>Config</b> button in the graphical interface. A window will open where you can choose the PLCs to attack and the content of the packets that will be sent.

### Launching the attack
Once the configuration is complete, select the DoS attack through the Combobox and click the <b>Start attack</b> button.

### Notes for use on Ubuntu
For use on Ubuntu, it is necessary to modify various lines of code.

In the <b>gui.py</b> file, you need to modify the following instructions:
- Replace all occurrences of script launches that use the word <b>python</b> with the word <b>python3</b>. Here's an example:
  ```python
  cmd[0] = "python attackplc/attack.py"
  ```
  should be replaced with
  ```python
  cmd[0] = "python3 attackplc/attack.py"
  ```
- 
    ```python
    pid_list = self.get_pid_by_process_name('python.exe')
    ```
  should be replaced with
    ```python
    pid_list = get_pid_by_process_name('python3')
    ```
- 
    ```python
    subprocess.run(['taskkill', '/f', '/im', str(temp[0])])
    ```
  should be replaced with
    ```python
    subprocess.run(['pkill', '-f', str(temp[0])])
    ```