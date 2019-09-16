# Questo programma va eseguito sul PC

from tkinter import Tk, Label, Entry, Button, PhotoImage, Scale, HORIZONTAL
import socket
import sys


def avanti():
    skt.send(b"dritto")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def avanti1(self):
    skt.send(b"dritto")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def retro():
    skt.send(b"retro")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def retro1(self):
    skt.send(b"retro")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


def destra():
    skt.send(b"destra")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def destra1(self):
    skt.send(b"destra")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


def sinistra():
    skt.send(b"sinistra")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def sinistra1(self):
    skt.send(b"sinistra")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


def accendi():
    skt.send(b"accendi")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def accendi1(self):
    skt.send(b"accendi")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


def spegni():
    skt.send(b"spegni")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def spegni1(self):
    skt.send(b"spegni")
    data = skt.recv(4096)
    print(str(data, "utf-8"))


def esc():
    skt.send(b"ESC")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def esc1(self):
    skt.send(b"ESC")
    data = skt.recv(4096)
    print(str(data, "utf-8"))

# vel2 = 0

def vel():
    skt.send(str(vel1.get()).encode())
    data = skt.recv(4096)
    print(str(data, "utf-8"))

def vel4(self):
    skt.send(str(vel1.get()).encode())
    data = skt.recv(4096)
    print(str(data, "utf-8"))


if __name__ == "__main__":

    ip = input("Inserisci l'indirizzo ip -> ")
    porta = input("Inserisci la porta -> ")

    try:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect(( ip, int(porta)))
    except socket.error as errore:
        print("Connessione Fallita: \n" + str(errore))
        skt.shutdown(socket.SHUT_RDWR)
        skt.close()
        sys.exit()
    else:
        print("Connessione al Raspberry Riuscita!")

        root = Tk()
        root.title("Controllo Raspy")
        root.geometry("300x200")
        root.resizable(False, False)
        load_arrow_up = PhotoImage(file="arrow-up-solid.png")
        arrow_up = load_arrow_up.subsample(50, 50)
        load_arrow_down = PhotoImage(file="arrow-down-solid.png")
        arrow_down = load_arrow_down.subsample(50, 50)
        load_arrow_left = PhotoImage(file="arrow-left-solid.png")
        arrow_left = load_arrow_left.subsample(50, 50)
        load_arrow_right = PhotoImage(file="arrow-right-solid.png")
        arrow_right = load_arrow_right.subsample(50, 50)
        Button(root, image=arrow_up, command=avanti).place(x=60, y=20)
        root.bind("w", avanti1)
        Button(root, image=arrow_down, command=retro).place(x=60, y=100)
        root.bind("s", retro1)
        Button(root, image=arrow_left, command=sinistra).place(x=20, y=60)
        root.bind("a", sinistra1)
        Button(root, image=arrow_right, command=destra).place(x=100, y=60)
        root.bind("d", destra1)
        Button(root, text="Accendi", command=accendi).place(x=220, y=40)
        root.bind("q", accendi1)
        Button(root, text=" Spegni ", command=spegni).place(x=220, y=70)
        root.bind("e", spegni1)
        Button(root, text="    Esc    ", command=esc).place(x=220, y=100)
        vel1 = Entry(root, width=20)
        vel1.place(x=50, y=150)
        Button(root, text="Invia Vel", command=vel).place(x=170, y=165)

        root.mainloop()








