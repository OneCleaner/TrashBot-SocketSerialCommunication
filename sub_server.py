# Questo programma va eseguito sul Raspberry

import socket
from serial import Serial

def comandi(conn, serial):
    while True:
        richiesta = conn.recv(4096)
        serial.write(str.encode(richiesta.decode()))
        conn.sendall("Comando eseguito con successo !")


def server(indirizzo, serial, backlog=1):
    try:
        s = socket.socket()
        s.bind(indirizzo)
        s.listen(backlog)
        print("Server inizializzato. In ascolto ... ")
    except socket.error as errore:
        print(f"Qualcosa è andato storto: \n{errore}")
        print("Reinizialiazzazione Server in corso...")
        server(indirizzo, backlog=1)
    conn, indirizzo_client = s.accept()  # conn = socket_client
    print(f"Connessione Server - Client Stabilita: {indirizzo_client}")
    comandi(conn, serial)

if __name__ == "__main__":
    port = "/dev/tty"  # la porta
    p = input("Inserire l'ultima parte della porta (escluso tty) -> ")
    port += p
    serial = Serial(port, 9600)
    serial.flushInput()
    PORTA_SERVER = input("Inserisci una porta (Qualsiasi numero tra 1024 e 65000) ->")
    server(("", PORTA_SERVER), serial)