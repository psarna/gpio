import RPi.GPIO as GPIO
import time
import sys
 
GPIO.setmode(GPIO.BCM)
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24
 

delay = 0.001
count = 512

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
def do_step(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
 
def forward(sequence, delay, steps):
    for _ in range(steps):
        for step in sequence:
            do_step(*step)
            time.sleep(delay)

sequence = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
 
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'rev':
            sequence = [s for s in reversed(sequence)]
    forward(sequence, delay, count)
