from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT) #Pin 12 raspberry untuk nyalakan lampu

global image, gray, digitCnts, DIGITS_LOOKUP

# membuat kamus segmen dari tiap digit
DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9,
}

def CariLayar():
	# proses awal, mengatur ukuran, ubah ke grayscale, memblur dan
	# memcompute edge map
	image = imutils.resize(image, height=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(blurred, 50, 200, 255)
	# mencari contour di edge, lalu mengurutkanya berdasar ukuran di urutan descending
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	displayCnt = None	 
	# loop di contour
	for c in cnts:
		# memperkirakan contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	 	# jika contour memiliki 4 vertikal, maka kita dapat displaynya
		if len(approx) == 4:
			displayCnt = approx
			break

def CariDigit():
	# mengekstrak display dan menerapkan four point transform
	warped = four_point_transform(gray, displayCnt.reshape(4, 2))
	output = four_point_transform(image, displayCnt.reshape(4, 2))

	# menthreshold gambar yang sudah diluruskan, dan mengaplikasikan serangkaian
	# aplikasi morfologi untuk membersihkan gambar yang di threshold
	thresh = cv2.threshold(warped, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

	# mencari contour di gambar yang telah di threshold, lalu
	# menginisialisasi daftar contour digit
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	digitCnts = []
	 
	# loop di area kandidat digit
	for c in cnts:
		# compute the bounding box of the contour
		(x, y, w, h) = cv2.boundingRect(c)	 
		# if the contour is sufficiently large, it must be a digit
		if w >= 15 and (h >= 30 and h <= 40):
			digitCnts.append(c)
	# mengurutkan contour dari kanan ke kiri, lalu inisialisasi digit 
	# sebenarnya dari contour tsb
	digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0]
	digits = []

def Kuantisasi():
	for c in digitCnts:
		# extract the digit ROI
		(x, y, w, h) = cv2.boundingRect(c)
		roi = thresh[y:y + h, x:x + w]
	 
		# menghitung lebar dan tinggi dari setiap digit
		(roiH, roiW) = roi.shape
		(dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
		dHC = int(roiH * 0.05)
	 
		# mendefinisikan set dari 7 segment
		segments = [
			((0, 0), (w, dH)),	# atas
			((0, 0), (dW, h // 2)),	# atas-kiri
			((w - dW, 0), (w, h // 2)),	# atas-kanan
			((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # tengah
			((0, h // 2), (dW, h)),	# bawah-kiri
			((w - dW, h // 2), (w, h)),	# bawah-kanan
			((0, h - dH), (w, h))	# bawah
		]
		on = [0] * len(segments)
		# loop terhadap masing2 segments
		for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
			# extract the segment ROI, count the total number of
			# thresholded pixels in the segment, and then compute
			# the area of the segment
			segROI = roi[yA:yB, xA:xB]
			total = cv2.countNonZero(segROI)
			area = (xB - xA) * (yB - yA)
	 
			# if the total number of non-zero pixels is greater than
			# 50% of the area, mark the segment as "on"
			if total / float(area) > 0.5:
				on[i]= 1
				
		# lookup digitnya dan kasih kotak disana
		digit = DIGITS_LOOKUP[tuple(on)]
		digits.append(digit)
		cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
		cv2.putText(output, str(digit), (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
		
	'''	
print(u"{}{}.{} \u00b0C".format(*digits))
cv2.imshow("Input", image)
cv2.imshow("Output", output)
cv2.waitKey(0)'''

if __name__ = '__main__':
	GPIO.output(12,GPIO.LOW)
	image = cv2.imread("example01.jpg")
	'''	
	cap = cv2.VideoCapture(0)
	ret,image = cv2.VideoCapture(0)
	cap.release()
	'''
	GPIO.output(12,GPIO.HIGH)
	Carilayar()
	CariDigit()
	Kuantisasi()
	print(digits)
	cv2.imshow("Input", image)
	cv2.imshow("Output", output)
	cv2.waitKey(0)
	GPIO.cleanup()

