import serial
import sys
import time
import Header

'''
Albert HM
& Saduran dari www.pyimagesearch.com
################### Konsensus ################### 
-varTest
Glukosa = 1
Kolestrol = 2
AsamUrat = 3
'''

def main():
	waktuGlukosa = 10;
	waktuKolestrol = 150;
	waktuAsamUrat = 20;
	waktuHb = 1;
	alamatArduino = '/dev/tty.usbserial'
	
	if len(sys.argv)==1:
		print("No Argument Error")
		break;
	else:
		varTest = int(sys.argv[2])
	#Switching delay
	if(varTest == 1):
		time.sleep(waktuGlukosa)
	elif(varTest == 2):
		time.sleep(waktuKolestrol)
	elif(varTest == 3):
		time.sleep(waktuAsamUrat)
	elif(varTest == 4):
		time.sleep(waktuHb)
	else:
		print("Error")
		return 0
		
	ser = serial.Serial(alamatArduino, 9600)
	ser.write(b'1')
	while(True):
		responArduino = ser.read()
		if responArduino == 1:
			break
	hasil = Header.SSOCR()
	laporan = open('Hasil', w)
	laporan.write(hasil)
	laporan.close
	

if __name__ == '__main__':
	main()
	
