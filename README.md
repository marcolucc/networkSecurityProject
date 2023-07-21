# networkSecurityProject
 
Nel file config.ini nella sezione params troviamo i campi plc1, plc2, plc3 che indicano quali coil
sono state selezionate dall'utente per essere colpite per l'attacco [0 = non selezionata per l'attacco; 
1 = selezionata per l'attacco]
Nel file config.ini nella sezione params troviamo anche i campi number_of_packages e value_of_package.

number_of_packages --> indica quanti pacchetti voglio inviare per l'attacco (o un numero fissato oppure 
                        digitando la stringa 'loop' vengono inviati un numero infinito di pacchetti)

value_of_package --> indica il payload dei pacchetti inviati (0 = comando di spegnimento coil; 
                        1 = comando di accensione coil)




I due attacchi (specular, powerON) sono stati implementati pensandoli come attacchi basati su trigger ma poi 
        ho ritenuto più giusto creare attacchi che venissero attivati sulla base del valore di level di ogni
        vasca.
        Non ho ritenuto necessario rimuoverli dato che sono stati implementati e testati.

specular: in modalità loop, leggo lo stato della coil ed in base al suo valore invio un pacchetto corrispondente allo stato opposto.

powerON: in modalità loop, leggo lo stato della coil e forzo una accensione continua dello strumento, se è acceso attendo altrimenti 
  se il sistema prova a spegnerlo viene mandato un pacchetto con un payload pari a 1 (quindi accensione 1 = ON).




NB: 
    per la continua mancanza di disponibilità dello strumenti di testing (Sistema PLC & HMI sotto VPN) l'attivazione
    del comando basato su trigger (ovvero mandare un certo numero/infinito di pacchetti con valore 0/1
    sulla base del fatto che sia maggiore o minore del valore 'level' di una pompa) non è stato testato nel 
    suo corretto funzionamento a runtime.
    Mi sono operato per testare localmente il codice andando a simulare il parametro formale delle funzioni
    on_status_mode(value: int) [value: int --> sarebbe il livello aggiornato in real time del valore 'level' 
    su %IW0] usando la variabile hardcodata value (1 riga di codice dentro ogni funzione) andando a modificare 
    i valori di input da gui per la verifica di funzionamento.

ESECUZIONE:
    Lanciare il file gui.py per avviare il programma principale.
    Selezionare l'attacco ed inserire i campi richiesti per procedere.
    Con una finestra chrome aperta, dopo aver avviato OpenPLC Runtime, aprire su http://127.0.0.1:8080
    la finestra di monitoraggio della plc. Se non è avviata la plc premere su start plc.
    Se manca il file plc.st caricarlo nell'apposita sezione della pagina web.
    I file .st si trovano in questa repository nella cartella 
    "networkSecurityProject\stuff\Dati_a_Caso\cyberRange\sorgenti docker (plc1,plc2,plc3,scadabr)\PLC1-2-3"