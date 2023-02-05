from tkinter import *
import serial
import functools
import serial.tools.list_ports
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import time

style.use("dark_background")
file = open('logs.txt', 'w')

ports = serial.tools.list_ports.comports()
serialObj = serial.Serial()
background_color = "#2b2b2b"
foreground_color = "#ffffff"
c = " 0;0;0;0;0;0;0"
b = 0


def init_com_port(index, win):
    currentPort = str(ports[index])
    comPortVar = str(currentPort.split(' ')[0])
    serialObj.port = comPortVar
    serialObj.baudrate = 115200
    serialObj.open()
    win.destroy()


def choose_com():
    com_chooser_win = Toplevel()
    com_chooser_win.config(bg=background_color)
    for onePort in ports:
        comButton = Button(com_chooser_win, text=onePort, font=('Roboto', '13'),
                           height=1, width=45, bg="#252525",
                           fg=foreground_color, border="0",
                           command=functools.partial(init_com_port, index=ports.index(onePort), win=com_chooser_win))
        comButton.grid(row=ports.index(onePort), column=0, pady=2)


def do_the_funni():
    if serialObj.is_open and serialObj.in_waiting:
        raw = serialObj.readline()
        global c
        c = raw.decode('utf_8')


def read_the_funni(c):
    g = str(c)
    a = g.split(";")
    global b
    if a[0] != b:
        if a[0] != 0:
            file.write(f"{a[0]};{a[1]};{a[2]}\n")
    b = a[0]
    # time
    if c != "0;0;0;0;0;0;0":
        text.config(
            text=f"Time: {int(a[0]) // 3600}:{(int(a[0]) % 3600) // 60}:{((int(a[0]) % 3600) % 60) % (24 * 3600)}"
                 f"\nPressure: {a[1]} hPa\n"
                 f"Temp: {a[2]} C\n"
                 f"Longitude: {a[3]}\n"
                 f"Latitude: {a[4]}\n"
                 f"Height: {float(a[5]) + float(a[6])}\n"
            )
    else:
        text.config(text="No Signal :(")


# main window settings
root = Tk()
root.title("Włodzimierz Biały")
root.config(bg=background_color)
root.geometry("240x700+700+300")

choose_com()

# text visuals
text = Label(bg="#252525", fg=foreground_color, text="TEMP", font=("Roboto", 25))
text.pack(side=LEFT, fill=BOTH)

while 1:
    root.update()
    do_the_funni()
    read_the_funni(c)
