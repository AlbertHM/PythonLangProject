import time
import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BOARD)
ser = serial.Serial('/dev/ttyACM0',9600,timeout=5)
s = [0,1]
GPIO.setup(12, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

while True:
	read_serial=ser.readline()
	s[0] = int (ser.readline(),16)
	print s[0]
	#print read_serial

	if(s[0] <= 10):
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(7, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(7, GPIO.LOW)
		time.sleep(0.2)
	elif(s[0] <= 25):
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(7, GPIO.HIGH)
		time.sleep(0.4)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(7, GPIO.LOW)
		time.sleep(0.4)
	elif(s[0] > 25):
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(7, GPIO.HIGH)
		time.sleep(0.7)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(7, GPIO.LOW)
		time.sleep(0.7)
	ser.flushInput()
	ser.flushOutput()
GPIO.cleanup()
