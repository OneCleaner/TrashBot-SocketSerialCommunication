# Questo programma va eseguito sul PC

from tkinter import Tk, Label, Entry, Button, PhotoImage, Scale, HORIZONTAL
import socket
import sys

comando = ""

def avanti():
    global comando
    comando = "dritto"


def retro():
    global comando
    comando = "retro"


def destra():
    global comando
    comando = "destra"


def sinistra():
    global comando
    comando = "sinistra"


def accendi():
    global comando
    comando = "accendi"


def spegni():
    global comando
    comando = "spegni"


def esc():
    global comando
    comando = "ESC"

vel2 = 0

def vel():
    global comando, vel2
    comando = str(vel2)
    print(comando)


def invia_comandi(skt):
    global comando, vel2

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
    Button(root, image=arrow_down, command=retro).place(x=60, y=100)
    Button(root, image=arrow_left, command=sinistra).place(x=20, y=60)
    Button(root, image=arrow_right, command=destra).place(x=100, y=60)
    Button(root, text="Accendi", command=accendi).place(x=220, y=40)
    Button(root, text=" Spegni ", command=spegni).place(x=220, y=70)
    Button(root, text="    Esc    ", command=esc).place(x=220, y=100)
    vel1 = Scale(root, from_=90, to=255, orient=HORIZONTAL)
    vel1.place(x=50, y=150)
    vel2 = vel1.get()
    Button(root, text="Invia Vel", command=vel).place(x=170, y=165)
    print(comando)
    if comando == "ESC":
        print("Sto chiudendo la connessione con il Raspberry")
        skt.send(comando.encode())
        skt.shutdown(socket.SHUT_RDWR)  # solo client
        skt.close()
        sys.exit()
    elif comando != "":
        skt.send(comando.encode())
        data = skt.recv(4096)
        print(str(data, "utf-8"))
        comando = ""


    root.mainloop()

def access_connection():
    ip = ip_entry.get()
    door = door_entry.get()
    access.destroy()
    connessione_server((ip, int(door)))



def connessione_server(indirizzo_server):
    try:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect(indirizzo_server)
    except socket.error as errore:
        print("Connessione Fallita: \n" + str(errore))
        skt.shutdown(socket.SHUT_RDWR)
        skt.close()
        sys.exit()
    else:
        print("Connessione al Raspberry Riuscita!")
        invia_comandi(skt)





if __name__ == "__main__":

    access = Tk()
    access.title("Collegamento Raspy")
    access.geometry("300x300")
    access.resizable(False, False)
    Label(access, text="Indirizzo IP Raspy: ").place(x=30, y=20)
    Label(access, text="Porta Raspy: ").place(x=30, y=50)
    ip_entry = Entry(access)
    ip_entry.place(x=140, y=20)
    door_entry = Entry(access)
    door_entry.place(x=140, y=50)
    Button(access, text="Invia", command=access_connection).pack(pady="100")
    access.mainloop()








