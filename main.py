#!/usr/bin/env python

import time, os, threading, socket

## For simplicity's sake, we'll create a string for our paths.
GPIO_MODE_PATH= os.path.normpath('/sys/devices/virtual/misc/gpio/mode/')
GPIO_PIN_PATH=os.path.normpath('/sys/devices/virtual/misc/gpio/pin/')
GPIO_FILENAME="gpio"

htmlfile = open("index.html")
htmld = htmlfile.readlines()
htmlfile.close()

html = "HTTP/1.1 200\n\n"

for line in htmld:
    html += line + "\n"

htmle = html.encode("UTF-8")

## create a couple of empty arrays to store the pointers for our files
pinMode = []
pinData = []

## Create a few strings for file I/O equivalence
HIGH = "1"
LOW =  "0"
INPUT = "0"
OUTPUT = "1"
INPUT_PU = "8"

def pinOutput(pin, action):
    file = open(pinData[pin], 'r+')
    file.write(action)
    file.close()

def fwd():
    pinOutput(12, LOW)
    pinOutput(13, HIGH)

def rev():
    pinOutput(12, HIGH)
    pinOutput(13, LOW)

def stop():
    pinOutput(12, LOW)
    pinOutput(13, LOW)

## First, populate the arrays with file objects that we can use later.
for i in range(0,18):
    pinMode.append(os.path.join(GPIO_MODE_PATH, 'gpio'+str(i)))
    pinData.append(os.path.join(GPIO_PIN_PATH, 'gpio'+str(i)))

## Now, let's make all the pins outputs...
for pin in pinMode:
    file = open(pin, 'r+')  ## open the file in r/w mode
    file.write(OUTPUT)      ## set the mode of the pin
    file.close()            ## IMPORTANT- must close file to make changes!

## ...and make them low.
for pin in pinData:
    file = open(pin, 'r+')
    file.write(LOW)
    file.close()

print("Prepared GPIO, starting")

pwma = 0.5

def pwm():
    print("starting pwm thread")
    while pwma >= 0:
        PERCISION = 0.002
        duty = PERCISION * pwma;
        noDuty = PERCISION * (1.0 - pwma);
        if duty != 0:
            pinOutput(10, HIGH)
            time.sleep(duty)
        if noDuty != 0:
            pinOutput(10, LOW)
            time.sleep(noDuty)
    pinOutput(10, LOW)
    print("stopping pwm thread")

state = "n"
DELA = 0.001

def light():
    print("starting lights thread")
    while state.find("s") == -1:
        if state.find("ab") != -1:
            pinOutput(9, HIGH)
            pinOutput(8, HIGH)
            pinOutput(11, LOW)
            time.sleep(DELA)
            pinOutput(8, LOW)
            pinOutput(11, HIGH)
            time.sleep(DELA)
        elif state.find("a") != -1:
            pinOutput(9, HIGH)
            pinOutput(8, HIGH)
            pinOutput(11, LOW)
            time.sleep(DELA*2)
        elif state.find("b") != -1:
            pinOutput(9, HIGH)
            pinOutput(8, LOW)
            pinOutput(11, HIGH)
            time.sleep(DELA*2)
        else:
            pinOutput(9, LOW)
            pinOutput(8, LOW)
            pinOutput(11, LOW)
            time.sleep(DELA*2)
    print("stopping lights thread")
    pinOutput(9, LOW)
    pinOutput(8, LOW)
    pinOutput(11, LOW)

def parseArg(arg):
    global state, pwma
    try:
        name, value = arg.split("=")
        if name.find("d") != -1:
            if value.find("f") != -1:
                print("[net] fwd")
                fwd()
            elif value.find("r") != -1:
                print("[net] rev")
                rev()
            else:
                print("[net] stop")
                stop()
        elif name.find("s") != -1:
            print("[net] speed: {}".format(float(value)))
            pwma = float(value)
        elif name.find("l") != -1:
            if value.find("ab") != -1:
                print("[net] lights ab")
                state = "ab"
            elif value.find("a") != -1:
                print("[net] lights a")
                state = "a"
            elif value.find("b") != -1:
                print("[net] lights b")
                state = "b"
            else:
                print("[net] lights none")
                state = "n"
    except Exception as e:
        print("[arg]: {}".format(e))
        print(arg)

def network():
    print("starting networking thread")
    while pwma >= 0:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", 8080))
        sock.listen(1)
        while True:
            try:
                conn, addr = sock.accept()
                print("connection to {}".format(addr[0]))
                data = conn.recv(1024)
                if data:
                    message = data.decode("utf-8")
                    mess = message.split("\n")[0].split(" ")[1]
                    print("[debug]: {}".format(mess))
                    if mess.find("?") != -1:
                        # Check for input from args
                        try:
                            url, data = mess.split("?")
                            if data.find("&") != -1:
                                args = data.split("&")
                                for arg in args:
                                    parseArg(arg)
                            else:
                                parseArg(data)
                        except:
                            print ("failed to parse args..")
                            print(message)
                    # return headers
                    conn.send("HTTP/1.1 200".encode("UTF-8"))
                    # reply with page
                    conn.send(htmle)
                conn.close()
            except Exception as e:
                print ("[net]: {}".format(e))
    print("stopping network thread")

t1 = threading.Thread(target=pwm)
t1.start()

t2 = threading.Thread(target=light)
t2.start()

t3 = threading.Thread(target=network)
t3.start()

stp = False

while not stp:
    line = str(raw_input("[::] "))
    stra = line.split(' ')
    if len(stra) == 3:
        if stra[0].find("stop") != -1:
            print("quitting")
            pwma = -1
            state = "s"
            stop()
            stp = True
        elif stra[0].find("f") != -1:
            print("Setting direction to forwards")
            fwd()
        elif stra[0].find("r") != -1:
            print("Setting direction to reverse")
            rev()
        else:
            print("stopping")
            stop()
        try:
            pwma = float(stra[1])
        except:
            pass
        print("setting speed to {}".format(pwma))
        state = stra[2]
    elif len(stra) == 1:
        if stra[0].find("stop") != -1:
            print("quitting")
            pwma = -1
            state = "s"
            stop()
            stp = True;
        else:
            stop()
            pwma = 0
