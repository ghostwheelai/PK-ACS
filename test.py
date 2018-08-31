import RPi.GPIO as GPIO
import time
import signal

def end_read(signal,frame):
    global continue_reading

    GPIO.cleanup()

    print "Ctrl+C captured, ending read."
    continue_reading = False

signal.signal(signal.SIGINT, end_read)
continue_reading = True
pin = 14

ison = False

GPIO.setmode(GPIO.BCM)
# GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)

while continue_reading:

    if ison:
    	print "ison True"
        #GPIO.output(14, GPIO.LOW)

        GPIO.cleanup(14)

        ison = False
    else:
    	print "ison False"
    	# GPIO.output(14, GPIO.HIGH)
        GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)

    	ison = True

    print "\nWaiting..."
    
    time.sleep(1)