"""Questo programma va eseguito sul Raspberry"""
#pylint: disable=line-too-long
#Porta camera temporanea: 8081

from socket import socket, AF_INET, SOCK_STREAM, error
from threading import Thread
from time import sleep
import platform
from serial import Serial
from picamera import PiCamera


def send_photos(addr):
    """Send picamera photos to client"""
    camera_sock = socket(AF_INET, SOCK_STREAM)
    while 1:
        try:
            camera_sock.connect((addr, 8081))
            break
        except ConnectionRefusedError:
            continue
    camera = PiCamera()
    while True:
        camera.capture("image.png")
        image = open("image.png", 'rb')
        camera_sock.sendfile(image, 0)
        image.close()
        sleep(1.5)



def server(indirizzo, serial, backlog=1):
    """Main server (?)"""
    try:
        # apriamo la comunicazione tramite socket
        skt = socket(AF_INET, SOCK_STREAM)
        skt.bind(indirizzo)
        skt.listen(backlog)
        print("Server inizializzato. In ascolto ... ")
    except error as errore:  # se esplode tutto ci si riprova
        print("Qualcosa è andato storto: \n" + str(errore))
        print("Reinizialiazzazione Server in corso...")
        server(indirizzo, serial, backlog=1)
    else:  # se non esplode stabiliamo la connessione
        conn, indirizzo_client = skt.accept()  # conn = socket_client
        send_photos_thread = Thread(
            target=send_photos, daemon=True, args=[indirizzo_client[0], ])
        send_photos_thread.start()
        print("Connessione Server - Client Stabilita: " + str(indirizzo_client))

        while True:
            try:
                richiesta = conn.recv(4096)
            except ConnectionResetError:  # se il client chiude forzatamente la connessione ci rimettiamo in ascolto
                print("\n\nConnessione persa, ritorno in ascolto")
                skt.close()
                server(indirizzo, serial, backlog=1)

            if richiesta.decode() == "ESC":  # se il client afferma di voler terminare la connessione ci rimettiamo in ascolto
                print("\n\nConnessione con Client terminata, ritorno in ascolto")
                skt.close()
                server(indirizzo, serial, backlog=1)

            # manda sulla seriale di arduino i comandi ricevuti dal client, si potrebbe fare senza codificare e decodificare ma noi siamo matti
            serial.write(str.encode(richiesta.decode()))
            to_read = serial.readline()
            if to_read:
                conn.sendall(
                    ("Comando ricevuto con successo! \n" + to_read.decode()).encode())


if __name__ == "__main__":  # eseguiamo soltanto se questa è la classe main

    if platform.system() == "Windows":
        PORT = "COM" + \
            input("Inserire il numero della porta di arduino \n-> ")  # windows
    else:
        # prendiamo la seriale di arduino
        PORT = "/dev/tty" + \
            input("Inserire l'ultima parte della porta di arduino (escluso tty) \n-> ")
    SERIAL = Serial(PORT, 9600)  # inizializziamo la comunicazione con arduino
    SERIAL.flushInput()
    # prendiamo la porta su cui aprire la comunicazione con il PC
    PORTA_SERVER = input(
        "Inserisci una porta (Qualsiasi numero tra 1024 e 65000) \n-> ")
    # TODO: decidere porta server fissa.
    server(("", int(PORTA_SERVER)), SERIAL)
