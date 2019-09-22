#!/bin/env python
"""Controller test and pinger"""
# pylint: disable=global-statement
from os import system, remove
from os.path import exists
from platform import system as platformSystem
from socket import (AF_INET, SHUT_RD, SOCK_STREAM, gethostbyname,
                    gethostname, inet_aton, socket)
from socket import error as socketError
from subprocess import PIPE, Popen
from threading import Thread, active_count
OS = platformSystem()
MACHINE_IP = gethostbyname(gethostname())
CAMERA_SOCK = socket(AF_INET, SOCK_STREAM)
try:
    from guizero import App, error, Picture, Text, TextBox, PushButton
    from pygame.event import get
    from pygame.joystick import Joystick
    # pylint: disable=no-name-in-module
    from pygame import init, JOYBUTTONDOWN, JOYBUTTONUP
    # pylint: enable=no-name-in-module
    # from adafruit_pca9685 import PCA9685  # Test
    import tensorflow
except ModuleNotFoundError:
    try:
        import pip._internal as pip
        pip.main(["install", "pygame"])
        pip.main(["install", "tensorflow"])
        # pip.main(["install", "adafruit-circuitpython-pca9685"])  # Test
        # pip.main(["install", "adafruit-circuitpython-servokit"])  # Test
    except ModuleNotFoundError:
        print(
            """Pip not found. Some libraries must be installed manually
            guizero pygame adafruit-circuitpython-pca9685
            adafruit-circuitpython-servokit.""")  # Tkiniter for guizero??
        exit(1)


class GUIZeroException(Exception):
    """Custom GUIZeroException"""


def is_alive_windows(ip_end):  # Windows
    """Ping local network devices"""
    host = IP_RANGE + str(ip_end)
    _ = Popen(["ping", "-n", '1', host], stdout=PIPE).communicate()[0]
    if "ms" in _.decode():
        print(host, "is up")
        DEVICES[len(DEVICES)] = host


def is_alive_linux(ip_end):  # Linux
    """Ping local network devices"""
    host = IP_RANGE + str(ip_end)
    _ = system("ping -c 1 " + host)
    if _:
        print(host, "is up")
        DEVICES[len(DEVICES)] = host


def update_speed(flag):
    """Send custom speed"""
    global SPEED
    try:
        if flag is None:
            if int(GUI_TXT1.value) >= 95 and int(GUI_TXT1.value) <= 250:
                SOCK.send((str(int(GUI_TXT1.value))).encode())
                SPEED = int(GUI_TXT1.value)
            else:
                raise ValueError
        elif flag is False:
            if SPEED >= 95:
                SPEED -= 5
                SOCK.send((str(SPEED)).encode())
            else:
                raise ValueError
        elif flag is True:
            if SPEED <= 250:
                SPEED += 5
                SOCK.send((str(SPEED)).encode())
            else:
                raise ValueError
    except ValueError:
        error("Error", "Invalid speed (95-250)", GUI)


def handle_joystick():
    """Handle joystick input"""
    global MODE
    send_off = True
    axes = JOYSTICK.get_numaxes()  # Test
    while True:
        events = get()
        for event in events:
            if event.type == JOYBUTTONDOWN:
                if JOYSTICK.get_button(0):
                    print("■")
                    if MODE == 1:
                        SOCK.send(b"accendi")
                    SOCK.send(b"sinistra")
                    send_off = True
                elif JOYSTICK.get_button(1):
                    print("✚")
                    if MODE == 1:
                        SOCK.send(b"accendi")
                    SOCK.send(b"indietro")
                elif JOYSTICK.get_button(2):
                    print("●")
                    if MODE == 1:
                        SOCK.send(b"accendi")
                    SOCK.send(b"destra")
                    send_off = True
                elif JOYSTICK.get_button(3):
                    print("▲")
                    if MODE == 1:
                        SOCK.send(b"accendi")
                    SOCK.send(b"dritto")
                    send_off = True
                elif JOYSTICK.get_button(8):
                    print("Share")
                    MODE = 0
                    send_off = False
                elif JOYSTICK.get_button(9):
                    print("Options")
                    MODE = 1
                    send_off = False
                elif JOYSTICK.get_button(10):
                    print("Left Button")
                    update_speed(False)
                    send_off = False
                elif JOYSTICK.get_button(11):
                    print("Right Button")
                    update_speed(True)
                    send_off = False
                elif JOYSTICK.get_button(12):
                    print("PS4 Button")
                    SOCK.send(b"accendi")
                    send_off = False
                elif JOYSTICK.get_button(13):
                    print("Touchpad Press")
                    SOCK.send(b"spegni")
                    send_off = False
            elif event.type == JOYBUTTONUP:
                print("Release")
                if MODE == 1:
                    if send_off:
                        SOCK.send(b"spegni")
        for lvr in range(axes):  # Test
            axis = JOYSTICK.get_axis(lvr)  # Test
            if lvr == 0:
                if axis > 0.70:
                    print("Muovi a destra")
                elif axis < -0.70:
                    print("Muovi a sinistra")
            if lvr == 1:
                if axis > 0.70:
                    print("Muovi in basso")
                elif axis < -0.70:
                    print("Muovi in alto")
            if lvr == 2:
                if axis > 0.70:
                    print("Ruota a destra")  # ?
                elif axis < -0.70:
                    print("Ruota a sinistra")  # ?
            if lvr == 3:
                if axis > 0.70:
                    print("Chiudi la pinza")
                elif axis < -0.70:
                    print("Apri la pinza")


def handle_camera():
    """Show received photos on GUI"""
    if exists("image.png"):
        remove("image.png")
    CAMERA_SOCK.listen()
    conn, addr = CAMERA_SOCK.accept()
    print(addr, "connected to send images.")
    photo_file = open("image.png", "wb")
    while True:
        photo_data = conn.recv(8192)
        photo_file.write(photo_data)
        photo_file.close()
        try:
            IMAGE1.image = "image.png"
            # Tensorflow
            _ = Popen(["python3", "--graph=output_graph.pb",
                       "--labels=output_labels.txt --input_layer=Placeholder",
                       "--output_layer=final_result",
                       "--image=image.png"],
                      stdout=PIPE).communicate()[0]
            print(_)
            remove("image.png")
            photo_file = open("image.png", "wb")
        # pylint: disable=broad-except
        except Exception:
            # pylint: enable=broad-except
            photo_file = open("image.png", "ab")
            continue


while 1:
    try:
        # 0 = Default; 1 = manual ip, no ping or port scan
        SAFE = int(input("Safe:~$ "))
        if SAFE == 0 or SAFE == 1:
            break
    except ValueError:
        continue
while 1:
    try:
        MANUAL = int(input("Manual:~$ "))
        if MANUAL == 0 or MANUAL == 1:
            break
    except ValueError:
        continue
while 1:
    try:
        # SHARE = 0; OPTIONS = 1 #0 = Default; 1 = Press&Hold
        MODE = int(input("Mode:~$ "))
        if MODE == 0 or MODE == 1:
            break
    except ValueError:
        continue
if SAFE == 1:
    while 1:
        try:
            REMOTE_IP = input("Remote Ip:~$ ")
            inet_aton(REMOTE_IP)
            break
        except socketError:
            continue
if MANUAL == 1:
    while 1:
        try:
            LOCAL_IP = input("Local Ip:~$ ")
            inet_aton(LOCAL_IP)
            break
        except socketError:
            continue
while 1:
    try:
        PORT = int(input("Port:~$ "))
        break
    except ValueError:
        continue
while 1:
    try:
        # Enable camera photos
        CAMERA = int(input("Camera:~$ "))
        if CAMERA == 0 or CAMERA == 1:
            if CAMERA == 1:
                while 1:
                    try:
                        CAMERA_PORT = int(input("Camera Port:~$ "))
                        break
                    except ValueError:
                        continue
        break
    except ValueError:
        continue


SPEED = 100
SOCK = socket(AF_INET, SOCK_STREAM)
if SAFE == 0:
    IP_RANGE = (MACHINE_IP).split('.')
    del IP_RANGE[len(IP_RANGE) - 1]
    IP_RANGE = '.'.join(IP_RANGE) + '.'
    DEVICES = {}
    if OS == "Windows":
        for i in range(0, 256):
            pingThread = Thread(target=is_alive_windows, args=(i, ))
            pingThread.daemon = True
            pingThread.start()
    else:
        for i in range(0, 256):
            pingThread = Thread(target=is_alive_linux, args=(i, ))
            pingThread.daemon = True
            pingThread.start()
    try:
        while active_count() != 7:
            pass
    except KeyboardInterrupt:
        print("Network scanning interrupted")
    for value in DEVICES:
        SOCK = socket(AF_INET, SOCK_STREAM)
        SOCK.settimeout(0.1)
        ERR = SOCK.connect_ex((DEVICES[value], PORT))
        if ERR == 0:
            print(f"{DEVICES[value]} has port {PORT} open")
        SOCK.close()
    print(DEVICES)
    while True:
        while 1:
            SELECTED = input("Select ip:~$ ")
            try:
                if int(SELECTED) < len(DEVICES):
                    break
            except ValueError:
                continue
        SOCK = socket(AF_INET, SOCK_STREAM)
        ERR = SOCK.connect_ex((DEVICES[int(SELECTED)], PORT))
        if ERR == 0:
            REMOTE_IP = DEVICES[int(SELECTED)]
            break
        else:
            print("Connection error")
            print(ERR)
else:
    while 1:
        if CAMERA == 1:
            if MANUAL == 1:
                try:
                    CAMERA_SOCK.bind((LOCAL_IP, CAMERA_PORT))
                except OSError:
                    pass
            else:
                CAMERA_SOCK.bind((MACHINE_IP, CAMERA_PORT))
        ERR = SOCK.connect_ex((REMOTE_IP, PORT))
        if ERR == 0:
            break
        else:
            print("Connection error")
            while 1:
                try:
                    REMOTE_IP = input("Remote Ip:~$ ")
                    inet_aton(REMOTE_IP)
                    break
                except socketError:
                    continue
            while 1:
                try:
                    PORT = int(input("Port:~$ "))
                    break
                except ValueError:
                    continue

SOCK.shutdown(SHUT_RD)
SPEED = 150
try:
    init()
    JOYSTICK = Joystick(0)
    JOYSTICK.init()
    # pylint: disable=broad-except
except Exception:
    # pylint: enable=broad-except
    print("No joystick found. Quitting.")
    exit(1)
GUI = App(title="Main")
GUI.title = "Main"
#GUI.minsize(300, 300)
GUI_LBL1 = Text(GUI, text="Commander")
GUI_LBL2 = Text(GUI, text="Speed")
GUI_TXT1 = TextBox(GUI)
GUI_BTN1 = PushButton(GUI, text="Confirm", command=lambda: update_speed(None))
IMAGE1 = Picture(GUI, image="test1.png")
HANDLE_JOYSTICK_THREAD = Thread(target=handle_joystick, daemon=True)
HANDLE_JOYSTICK_THREAD.start()
if CAMERA == 1:
    HANDLE_CAMERA_THREAD = Thread(target=handle_camera, daemon=True)
    HANDLE_CAMERA_THREAD.start()
GUI.display()
