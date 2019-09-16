# Questo programma va eseguito sul PC

from tkinter import Tk, Label, Entry, Button, PhotoImage, Scale, HORIZONTAL
import socket
import sys


# Funzione per far andare avanti il robot (Pulsante su schermo)
def avanti():
    skt.send(b"dritto")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far andare avanti il robot (W su Tastiera)
def avanti1(self):
    skt.send(b"dritto")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far andare indietro il robot (Pulsante su schermo)
def retro():
    skt.send(b"retro")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far andare indietro il robot (S su Tastiera)
def retro1(self):
    skt.send(b"retro")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far andare a destra il robot (Pulsante su schermo)
def destra():
    skt.send(b"destra")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far andare a destra il robot (D su Tastiera)
def destra1(self):
    skt.send(b"destra")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far andare a sinistra il robot (Pulsante su schermo)
def sinistra():
    skt.send(b"sinistra")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far andare a sinistra il robot (A su Tastiera)
def sinistra1(self):
    skt.send(b"sinistra")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far accendere i motori del robot (Pulsante su schermo)
def accendi():
    skt.send(b"accendi")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far accendere i motori del robot (Q su Tastiera)
def accendi1(self):
    skt.send(b"accendi")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far spegnere i motori del robot (Pulsante su schermo)
def spegni():
    skt.send(b"spegni")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per far spegnere i motori del robot (E su Tastiera)
def spegni1(self):
    skt.send(b"spegni")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


def esc():
    skt.send(b"ESC")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Funzione per regolare la velocità dei motori del robot
def vel():
    skt.send(str(vel1.get()).encode())
    data = skt.recv(4096)
    print(str(data, "utf-8"))


# Eseguiamo solo se è main
if __name__ == "__main__":

    ip = input("Inserisci l'indirizzo ip -> ")  # Inserire Indirizzo Ip
    porta = input("Inserisci la porta -> ")  # Inserire la porta come nel Raspy

    try:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect(( ip, int(porta)))  # Ci connettiamo al Raspy
    except socket.error as errore:  # Interrompiamo la connessione in caso di errori
        print("Connessione Fallita: \n" + str(errore))
        skt.shutdown(socket.SHUT_RDWR)
        skt.close()
        sys.exit()
    else:
        print("Connessione al Raspberry Riuscita!")

        root = Tk()
        root.title("Controllo Raspy")  # Titolo della finestra
        root.geometry("300x200")  # Grandezza della finestra
        root.resizable(False, False)  # Gli impostiamo una grandezza fissa alla finestra

        # Carico le immagini delle frecce
        load_arrow_up = PhotoImage(file="arrow-up-solid.png")
        arrow_up = load_arrow_up.subsample(50, 50)
        load_arrow_down = PhotoImage(file="arrow-down-solid.png")
        arrow_down = load_arrow_down.subsample(50, 50)
        load_arrow_left = PhotoImage(file="arrow-left-solid.png")
        arrow_left = load_arrow_left.subsample(50, 50)
        load_arrow_right = PhotoImage(file="arrow-right-solid.png")
        arrow_right = load_arrow_right.subsample(50, 50)

        # Pulsante per andare avanti
        Button(root, image=arrow_up, command=avanti).place(x=60, y=20)
        root.bind("w", avanti1)

        # Pulsante per andare indietro
        Button(root, image=arrow_down, command=retro).place(x=60, y=100)
        root.bind("s", retro1)

        # Pulsante per girare a sinistra
        Button(root, image=arrow_left, command=sinistra).place(x=20, y=60)
        root.bind("a", sinistra1)

        # Pulstante per girare a destra
        Button(root, image=arrow_right, command=destra).place(x=100, y=60)
        root.bind("d", destra1)

        # Pulsante per accendere i motori
        Button(root, text="Accendi", command=accendi).place(x=220, y=40)
        root.bind("q", accendi1)

        # Pulsante per spegnere i motori
        Button(root, text=" Spegni ", command=spegni).place(x=220, y=70)
        root.bind("e", spegni1)

        # Pulsante per interrompere la connessione
        Button(root, text="    Esc    ", command=esc).place(x=220, y=100)

        # Regolatore della velocità
        vel1 = Entry(root, width=20)
        vel1.place(x=50, y=150)
        Button(root, text="Invia Vel", command=vel).place(x=170, y=165)

        root.mainloop()








