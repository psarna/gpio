import RPi.GPIO as GPIO
import time
import sys
 
GPIO.setmode(GPIO.BCM)
pin1 = 4
pin2 = 17
pin3 = 23
pin4 = 24
 

delay = 0.001
count = 512

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)
 
def do_step(s1, s2, s3, s4):
    GPIO.output(pin1, s1)
    GPIO.output(pin2, s2)
    GPIO.output(pin3, s3)
    GPIO.output(pin4, s4)
 
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
