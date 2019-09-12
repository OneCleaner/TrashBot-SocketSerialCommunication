# Questo programma va eseguito sul PC

import socket
import sys


def invia_comandi(s):
    while True:
        comando = input("-> ")
        if comando == "ESC":
            print("Sto chiudendo la connessione con il Raspberry")
            s.close()
            sys.exit()
        else:
            s.send(comando.encode())
            data = s.recv(4096)
            print(str(data, "utf-8"))



def connessione_server(indirizzo_server):
    try:
        s = socket.socket()
        s.connect(indirizzo_server)
        print("Connessione al Raspberry Riuscita !")
    except socket.error as errore:
        print(f"Connessione Fallita: \n{errore}")
        sys.exit()
    invia_comandi(s)

if __name__ == "__main__"
    IP_RASPBERRY = input("Inserisci l'indirizzo del Raspberry -> ")
    PORTA_RASPBERRY = input("Inserisci la porta che hai inserito nel Raspberry ->")
    connessione_server((IP_RASPBERRY, int(PORTA_RASPBERRY)))