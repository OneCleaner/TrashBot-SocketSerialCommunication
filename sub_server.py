# Questo programma va eseguito sul Raspberry

import socket
import sys
from serial import Serial

def comandi(conn, serial):   #ci mettiamo all'infinito in ascolto
    while True:
        richiesta = conn.recv(4096)
        serial.write(str.encode(richiesta.decode()))   #manda sulla seriale di arduino i comandi ricevuti dal client
        conn.sendall("Comando eseguito con successo !")


def server(indirizzo, serial, backlog=1):
    try:
        skt = socket.socket()    #apriamo la comunicazione tramite socket
        skt.bind(indirizzo)
        skt.listen(backlog)
        print("Server inizializzato. In ascolto ... ")
    except socket.error as errore:     #se esplode tutto ci si riprova
        print("Qualcosa è andato storto (" + str(contErrori) + "): \n" + str(errore))
        print("Reinizialiazzazione Server in corso...")
        server(indirizzo, serial, backlog=1)
    else:   #se non esplode stabiliamo la connessione
        conn, indirizzo_client = skt.accept()  # conn = socket_client
        print("Connessione Server - Client Stabilita: " + str(indirizzo_client))
        comandi(conn, serial)


if __name__ == "__main__":      #eseguiamo soltanto se questa è la classe main
    port = "/dev/tty"  # la porta
    p = input("Inserire l'ultima parte della porta di arduino (escluso tty) -> ")    #prendiamo la seriale di arduino
    port += p
    serial = Serial(port, 9600)  #inizializziamo la comunicazione con arduino
    serial.flushInput()
    PORTA_SERVER = input("Inserisci una porta (Qualsiasi numero tra 1024 e 65000) ->")   #prendiamo la porta su cui aprire la comunicazione con il PC
    server(("", PORTA_SERVER), serial) #TODO: decidere porta server fissa.
