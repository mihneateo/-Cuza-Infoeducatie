import tkinter as tk
import sys
import adafruit_dht
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import RPi.GPIO as GPIO
import time
import board
import lgpio as GP
TRIG = 23  
ECHO = 24  
import ooo
import newshit
from adafruit_servokit import ServoKit
import busio
import gpiod
dir(board)
kit = ServoKit(channels=16,address=0x40)
kit1 = ServoKit(channels=16,address=0x41)

h = GP.gpiochip_open(0)
GP.gpio_claim_output(h, TRIG)
GP.gpio_claim_input(h, ECHO)
def cap():
    kit1.servo[0].angle=90
    time.sleep(1)
    for i in range(90,180):
        kit1.servo[0].angle=i
        time.sleep(0.02)
    time.sleep(1)
    for i in range (180,-1,-1):
        kit1.servo[0].angle=i
        time.sleep(0.02)
    time.sleep(1)
    for i in range(91):
        kit1.servo[0].angle=i
        time.sleep(0.02)
    time.sleep(2)
    kit1.servo[1].angle=180
    time.sleep(1)
    kit1.servo[1].angle=0
    kit1.servo[2].angle=89
    kit1.servo[3].angle=99
    time.sleep(2)
    kit1.servo[2].angle=96
    kit1.servo[3].angle=76
    kit1.servo[11].angle=135
    kit1.servo[15].angle=135
    time.sleep(1)
    kit1.servo[11].angle=90
    kit1.servo[15].angle=90
    time.sleep(1)
    kit1.servo[11].angle=135
    kit1.servo[15].angle=135
    time.sleep(1)
    kit1.servo[11].angle=180
    kit1.servo[15].angle=180
    time.sleep(1)
    kit1.servo[11].angle=135
    kit1.servo[15].angle=135
def maini():
    kit.servo[14].angle=0
    time.sleep(1)
    kit.servo[14].angle=90
    kit.servo[15].angle=180
    time.sleep(1)
    kit.servo[15].angle=90
    time.sleep(2)
    kit.servo[14].angle=180
    time.sleep(1)
    kit.servo[14].angle=90
    kit.servo[15].angle=0
    time.sleep(1)
    kit.servo[15].angle=90
    time.sleep(2)
    kit.servo[10].angle=180
    time.sleep(1)
    kit.servo[10].angle=90
    kit.servo[11].angle=180
    time.sleep(1)
    kit.servo[11].angle=90
    time.sleep(2)
    kit.servo[10].angle=0
    time.sleep(1)
    kit.servo[10].angle=90
    kit.servo[11].angle=0
    time.sleep(1)
    kit.servo[11].angle=90
    time.sleep(2)
    kit.servo[0].angle=180
    kit.servo[1].angle=180
    kit.servo[2].angle=180
    kit.servo[3].angle=180
    kit.servo[4].angle=180
    kit.servo[5].angle=180
    kit.servo[6].angle=180
    kit.servo[7].angle=180
    kit.servo[8].angle=180
    kit.servo[9].angle=180
    time.sleep(2)
    kit.servo[0].angle=0
    kit.servo[1].angle=0
    kit.servo[2].angle=0
    kit.servo[3].angle=0
    kit.servo[4].angle=0
    kit.servo[5].angle=0
    kit.servo[6].angle=0
    kit.servo[7].angle=0
    kit.servo[8].angle=0
    kit.servo[9].angle=0
def get_distance():

    GP.gpio_write(h, TRIG, 0)
    time.sleep(2)


    GP.gpio_write(h, TRIG, 1)
    time.sleep(0.00001)
    GP.gpio_write(h, TRIG, 0)

  
    while GP.gpio_read(h, ECHO) == 0:
        pulse_start = time.time()


    while GP.gpio_read(h, ECHO) == 1:
        pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start
  
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

def button_clicked():
    print("click")
  
dht_device = adafruit_dht.DHT11(board.D4)
temperature = dht_device.temperature()

distance=10
if distance<20:
    root = tk.Tk()
    path="/home/informatica-pentru-viitor/Desktop/img.jpeg"
    root['background']='#ffffff'
    root.attributes('-fullscreen',True)
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(root, image = img)
    panel.pack(side = "bottom", expand = "yes")
    T = tk.Text(root, height = 5, width = 52)
    T.insert(tk.END, measure_temp())
    T.place(x=400,y=400)
    T1=tk.Text(root,height=5,width=52)
    T1.insert(tk.End,temperature)
    T1.place(x=400,y=410)

    button = tk.Button(root, 
                   text="Salut", 
                   command=button_clicked,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="w",
                   bd=3,
                   bg="blue",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=10,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="left",
                   overrelief="raised",
                   padx=20,
                   pady=15,
                   width=10,
                   wraplength=100)
    button1 = tk.Button(root,
                   text="vorbeste",
                   command=newshit.main,
                   activebackground="blue",
                   activeforeground="white",
                   anchor="w",
                   bd=3,
                   bg="blue",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=10,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="left",
                   overrelief="raised",
                   padx=20,
                   pady=15,
                   width=10,
                   wraplength=100
                    )
    button2 = tk.Button(root,
                   text="maini",
                   command=maini,
                   activebackground="blue",
                   activeforeground="white",
                   anchor="w",
                   bd=3,
                   bg="blue",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=10,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="left",
                   overrelief="raised",
                   padx=20,
                   pady=15,
                   width=10,
                   wraplength=100
                    )
    button3 = tk.Button(root,
                   text="cap",
                   command=root.destroy,
                   activebackground="blue",
                   activeforeground="white",
                   anchor="w",
                   bd=3,
                   bg="blue",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=10,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="left",
                   overrelief="raised",
                   padx=20,
                   pady=15,
                   width=10,
                   wraplength=100
                    )
button4=tk.Button(root,
                   text="vorbeste",
                   command=ooo.start,
                   activebackground="blue",
                   activeforeground="white",
                   anchor="w",
                   bd=3,
                   bg="blue",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=10,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="left",
                   overrelief="raised",
                   padx=20,
                   pady=15,
                   width=10,
                   wraplength=100
                    )
    button4['background']='#92eddc'
    button3['background']='#92eddc'
    button2['background']='#92eddc'
    button['background']='#92eddc'
    button1['background']='#92eddc'
    button2.place(x=1100,y=400)
    button.place(x=0,y=0)
    button.place(x=400 ,y=450)
    button3.place(x=0,y=400)
    button1.place(x=1100,y=0)
    root.mainloop()

