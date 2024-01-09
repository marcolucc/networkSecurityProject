# PLC Attack Tool

This tool allows you to perform PLC (Programmable Logic Controller) attacks using different modes: "dos" and "chattering".

## Getting Started

### Prerequisites

Make sure you have the following software installed:

- [Python 3](https://www.python.org/downloads/)
- [pip3](https://pip.pypa.io/en/stable/)

### Installation

Clone the project repository:

```bash
git clone <repository_link>
```

Install the required dependencies using pip3:

```bash
pip3 install .
```

## Usage

Launch the GUI by running:

```bash
python3 gui.py
```

### DOS Attack Mode

If you choose "dos" mode:

1. Enter the PLC address(es) and port(s) following this template: `ip:port`.
2. Specify the coil or register you want to attack (e.g., c0 for coil 0, m0 for register 0).
3. Set the value of packets to send between "0" and "1".
4. Choose how many packets you want to send (you can input a number or "loop" for continuous sending).
5. Optionally, add one or more triggers by checking the "Add triggers" box. Triggers allow you to select a PLC (ip:port), a coil, a condition, and a value. For example, you can start the attack only if c1 of PLC1 is ON.
6. Click "Start attack"

### Chattering Attack Mode

If you choose "chattering" mode:

1. Enter the PLC address(es) and port(s) following this template: `ip:port`.
2. Specify the coil or register you want to attack (e.g., c0 for coil 0, m0 for register 0).
3. Set the emptying time of the system.
4. Select the mode of the chattering attack (percentage or time slow).
5. Insert the value corresponding to the selected mode.
6. Optionally, add one or more triggers by checking the "Add triggers" box. Triggers allow you to select a PLC (ip:port), a coil, a condition, and a value. For example, you can start the attack only if c1 of PLC1 is ON.
7. Click "Start attack"

## License

This project is licensed under the [MIT License](LICENSE.md).

