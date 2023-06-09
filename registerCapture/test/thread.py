import pandas as pd #json 
import os
from datetime import datetime # Per il timestamp dei file JSON (per uso futuro)
import time #needed for sleep and to capture data for set amount of time
import ray#thread parall, per usarlo basta inserire il decoratore @ray.remote sopra alla funzione interessata
## Execute in parallel -> ray.get([plc1.remote(), plc2.remote()])
ray.init()
timestamp1=[]
timestamp2=[]
'''
ora=datetime.now(tz=None)

with open(f'historian/PLC1-{plc1}-{port1}@{ora}.json', 'w') as sp:
            sp.write(json.dumps(self.single_plc_registers, indent=4))
            #print(self.single_plc_registers)
'''
@ray.remote
def test1():
    ora=datetime.now(tz=None)
    timestamp1.append(ora)
    with open(f'PLC1@{ora}.json', 'w') as sp:
        sp.write("test1")
        #print(self.single_plc_registers)

@ray.remote
def test2():
    ora=datetime.now(tz=None)
    timestamp2.append(ora)
    with open(f'PLC1@{ora}.json', 'w') as sp:
        sp.write("test2")

        #print(self.single_plc_registers)

def main():
    i=0
    while(i<10):
        ray.get([test1.remote(), test2.remote()])
        i+=1

if __name__ == '__main__':
    main()