import serial, time
import datetime as dt
import numpy as np
import cv2

# function to get Emissivity from MCU
def get_emissivity():
	ser.write(serial.to_bytes([0xA5,0x55,0x01,0xFB]))
	read = ser.read(4)
	return read[2]/100

# function to get temperatures from MCU (Celsius degrees x 100)
def get_temp_array(d):

	# getting ambient temperature
	T_a = (int(d[1540]) + int(d[1541])*256)/100

	# getting raw array of pixels temperature
	raw_data = d[4:1540]
	T_array = np.frombuffer(raw_data, dtype=np.int16)
	
	return T_a, T_array

# function to convert temperatures to pixels on image
def td_to_image(f):
	norm = np.uint8((f/100 - Tmin)*255/(Tmax-Tmin))
	norm.shape = (24,32)
	return norm

########################### Main cycle #################################
# Color map range
Tmax = 40
Tmin = 20

print ('Configuring Serial port')
ser = serial.Serial ('/dev/serial0')
ser.baudrate = 115200

# set frequency of module to 4 Hz
ser.write(serial.to_bytes([0xA5,0x25,0x01,0xCB]))
time.sleep(0.1)

# Starting automatic data colection
ser.write(serial.to_bytes([0xA5,0x35,0x02,0xDC]))
t0 = time.time()

try:
	while True:
		# waiting for data frame
		data = ser.read(1544)
		
		# The data is ready, let's handle it!
		Ta, temp_array = get_temp_array(data)
		ta_img = td_to_image(temp_array)
		
		# Image processing
		img = cv2.applyColorMap(ta_img, cv2.COLORMAP_JET)
		img = cv2.resize(img, (320,240), interpolation = cv2.INTER_CUBIC)
		img = cv2.flip(img, 1)
		
		text = 'Tmin = {:+.1f} Tmax = {:+.1f} FPS = {:.2f}'.format(temp_array.min()/100, temp_array.max()/100, 1/(time.time() - t0))
		cv2.putText(img, text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
		cv2.imshow('Output', img)
		
		# if 's' is pressed - saving of picture
		key = cv2.waitKey(1) & 0xFF
		if key == ord("s"):
			fname = 'pic_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
			cv2.imwrite(fname, img)
			print('Saving image ', fname)
		
		t0 = time.time()

except KeyboardInterrupt:
	# to terminate the cycle
	ser.write(serial.to_bytes([0xA5,0x35,0x01,0xDB]))
	ser.close()
	cv2.destroyAllWindows()
	print(' Stopped')

# just in case 
ser.close()
cv2.destroyAllWindows()
