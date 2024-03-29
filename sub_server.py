# Questo programma va eseguito sul Raspberry

import socket
from serial import Serial
import platform

def server(indirizzo, serial, backlog=1):

    try:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #apriamo la comunicazione tramite socket
        skt.bind(indirizzo)
        skt.listen(backlog)
        print("Server inizializzato. In ascolto ... ")
    except socket.error as errore:     #se esplode tutto ci si riprova
        print("Qualcosa è andato storto: \n" + str(errore))
        print("Reinizialiazzazione Server in corso...")
        server(indirizzo, serial, backlog=1)
    else:   #se non esplode stabiliamo la connessione
        conn, indirizzo_client = skt.accept()  # conn = socket_client
        print("Connessione Server - Client Stabilita: " + str(indirizzo_client))

        while True:
            try:
                richiesta = conn.recv(4096)
            except ConnectionResetError:        #se il client chiude forzatamente la connessione ci rimettiamo in ascolto
                print("\n\nConnessione persa, ritorno in ascolto")
                skt.close()
                server(indirizzo, serial, backlog=1)

            if richiesta.decode() == "ESC":    #se il client afferma di voler terminare la connessione ci rimettiamo in ascolto
                print("\n\nConnessione con Client terminata, ritorno in ascolto")
                skt.close()
                server(indirizzo, serial, backlog=1)

            serial.write(str.encode(richiesta.decode()))   #manda sulla seriale di arduino i comandi ricevuti dal client, si potrebbe fare senza codificare e decodificare ma noi siamo matti
            #serial.write(richiesta)
            toRead = serial.readline()
            if toRead:
                conn.sendall(("Comando ricevuto con successo! \n" + toRead.decode()).encode())
                #conn.sendall(("Comando ricevuto con successo! \n").encode() + toRead)

if __name__ == "__main__":      #eseguiamo soltanto se questa è la classe main

    if platform.system() == "Windows":
        port = "COM" + input("Inserire il numero della porta di arduino \n-> ") #windows
    else:
        port = "/dev/tty" + input("Inserire l'ultima parte della porta di arduino (escluso tty) \n-> ")    #prendiamo la seriale di arduino
    serial = Serial(port, 9600)  #inizializziamo la comunicazione con arduino
    serial.flushInput()
    PORTA_SERVER = input("Inserisci una porta (Qualsiasi numero tra 1024 e 65000) \n-> ")   #prendiamo la porta su cui aprire la comunicazione con il PC
    server(("", int(PORTA_SERVER)), serial) #TODO: decidere porta server fissa.
