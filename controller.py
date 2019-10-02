"""Complete joystick control"""
# pylint: disable=no-name-in-module
from socket import socket, AF_INET, SOCK_STREAM
#from time import sleep
from threading import Thread
from tkinter import Tk, PhotoImage, Label
from pygame.joystick import Joystick
from pygame import init, JOYBUTTONDOWN
from pygame.event import get
# 0-180
GUI = Tk()
GUI.title = "Main"
SOCK = socket(AF_INET, SOCK_STREAM)
while 1:
    IP = input("IP: ")
    PORT = int(input("Port: "))
    try:
        SOCK.connect((IP, PORT))
        break
    except ConnectionRefusedError:
        print("Connection refused")
        continue


def joystick():
    """Handle joystick actions"""
    init()
    joystick_object = Joystick(0)
    joystick_object.init()
    axes = joystick_object.get_numaxes()
    mode = 1
    debug = 1
    speed = 230
    angle = [90] * 5
    while True:
        send_off = False
        events = get()
        for event in events:
            if event.type == JOYBUTTONDOWN:
                if joystick_object.get_button(0):
                    if debug == 1:
                        print("■")
                    SOCK.send(b"sinistra")
                    send_off = True
                elif joystick_object.get_button(1):
                    if debug == 1:
                        print("✚")
                    SOCK.send(b"retro")
                    send_off = True
                elif joystick_object.get_button(2):
                    if debug == 1:
                        print("●")
                    SOCK.send(b"destra")
                    send_off = True
                elif joystick_object.get_button(3):
                    if debug == 1:
                        print("▲")
                    SOCK.send(b"dritto")
                    send_off = True
                elif joystick_object.get_button(8):
                    if debug == 1:
                        print("Share")
                    if mode == 1:
                        mode = 0
                    else:
                        mode = 1
                elif joystick_object.get_button(9):
                    if debug == 1:
                        print("Options")
                        debug = 0
                    else:
                        debug = 1
                elif joystick_object.get_button(10):
                    if debug == 1:
                        print("Left Button")
                    if speed < 250 and speed > 100:
                        speed -= 5
                        SOCK.send(str(speed).encode())
                    else:
                        print("Invalid speed")
                elif joystick_object.get_button(11):
                    if debug == 1:
                        print("Right Button")
                    if speed < 250 and speed > 100:
                        speed += 5
                        SOCK.send(str(speed).encode())
                    else:
                        print("Invalid speed")
                elif joystick_object.get_button(12):
                    if debug == 1:
                        print("PS4 Button")
                    SOCK.send(b"accendi")
                elif joystick_object.get_button(13):
                    if debug == 1:
                        print("Touchpad Press")
                    SOCK.send(b"spegni")
            else:
                if mode == 1:
                    if send_off:
                        SOCK.send(b"spegni")
                    for lvr in range(axes):
                        axis = joystick_object.get_axis(lvr)
                        if lvr == 0:
                            if axis > 0.50:
                                if debug == 1:
                                    print("Routa pinza a destra")
                                if angle[3] > 3:
                                    angle[3] -= 1
                                SOCK.send(b"r-pinza|" +
                                          str.encode(str(angle[3])))
                                #sleep(0.15)
                            elif axis < -0.50:
                                if debug == 1:
                                    print("Routa pinza a sinistra")
                                if angle[3] < 180:
                                    angle[3] += 1
                                SOCK.send(b"r-pinza|" +
                                          str.encode(str(angle[3])))
                                #sleep(0.15)
                        if lvr == 1:
                            if axis > 0.50:
                                if debug == 1:
                                    print("Cosa in basso")
                                if angle[4] > 3:
                                    angle[4] -= 1
                                SOCK.send(b"estensione|" +
                                          str.encode(str(angle[4])))
                                #sleep(0.15)
                            elif axis < -0.50:
                                if debug == 1:
                                    print("Cosa in alto")
                                if angle[4] < 180:
                                    angle[4] += 1
                                SOCK.send(b"estensione|" +
                                          str.encode(str(angle[4])))
                                #sleep(0.15)
                        if lvr == 2:
                            if axis > 0.50:
                                if debug == 1:
                                    print("Ruota a destra")
                                if angle[2] > 0:
                                    angle[2] -= 1
                                SOCK.send(b"base|" + str.encode(str(angle[2])))
                                #sleep(0.15)
                            elif axis < -0.50:
                                if debug == 1:
                                    print("Ruota a sinistra")
                                if angle[2] < 180:
                                    angle[2] += 1
                                SOCK.send(b"base|" + str.encode(str(angle[2])))
                                #sleep(0.15)
                        if lvr == 3:
                            if axis > 0.50:
                                if debug == 1:
                                    print("Abbassa")
                                if angle[1] > 3:
                                    angle[1] -= 1
                                SOCK.send(b"altezza|" +
                                          str.encode(str(angle[1])))
                                #sleep(0.15)
                            elif axis < -0.50:
                                if debug == 1:
                                    print("Alza")
                                if angle[1] < 180:
                                    angle[1] += 1
                                SOCK.send(b"altezza|" +
                                          str.encode(str(angle[1])))
                                #sleep(0.15)
                        if lvr == 4:
                            if axis > 0.50:
                                if debug == 1:
                                    print("Apri la pinza")
                                if angle[0] > 0:
                                    angle[0] -= 1
                                SOCK.send(
                                    b"a-pinza|" + str.encode(str(angle[0])))
                                #sleep(0.15)
                        if lvr == 5:
                            if axis > 0.50:
                                if debug == 1:
                                    print("Chiudi la pinza")
                                if angle[0] < 180:
                                    angle[0] += 1
                                SOCK.send(
                                    b"a-pinza|" + str.encode(str(angle[0])))
                                #sleep(0.15)
                        if lvr == 6:
                            if axis > 0.50:
                                if debug == 1:
                                    print("Cosa1")
                                if angle[4] > 3:
                                    angle[4] -= 1
                                SOCK.send(b"estensione|" +
                                          str.encode(str(angle[4])))
                                #sleep(0.15)
                            elif axis < -0.50:
                                if debug == 1:
                                    print("Cosa2")
                                if angle[4] < 180:
                                    angle[4] += 1
                                SOCK.send(b"estensione|" +
                                          str.encode(str(angle[4])))
                                #sleep(0.15)
        if mode == 1:
            if send_off:
                SOCK.send(b"spegni")


def camera():
    """Show camera pictures"""
    try:
        image_sock = socket(AF_INET, SOCK_STREAM)
        image_sock.connect((IP, PORT + 100))
        while 1:
            image_file = open("image.png", "wb")
            image_file.write(image_sock.recv(65536))
            image_file.close()
            image_object = PhotoImage("image.png")
            image_panel = Label(GUI, image=image_object)
            image_panel.pack()
    except Exception as error:
        print(error)


CAMERA_THREAD = Thread(target=camera, daemon=True)
#CAMERA_THREAD.start()
JOYSTICK_THREAD = Thread(target=joystick, daemon=True)
JOYSTICK_THREAD.start()
GUI.mainloop()
