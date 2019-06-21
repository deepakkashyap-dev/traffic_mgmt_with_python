import numpy as np
import cv2
import os
import RPi.GPIO as GPIO
import time 

# get working directory
loc = os.path.abspath('')

#this is the cascade
car_cascade = cv2.CascadeClassifier(loc+'/cars3.xml')

# Video source
inputFile = loc+'/625_201709281121.mp4'
cap = cv2.VideoCapture(inputFile)
fps = cap.get(cv2.CAP_PROP_FPS)
rate = fps * 5

# get frame size
frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# create a mask (manual for each camera)
mask = np.zeros((frame_h, frame_w), np.uint8)
mask[:,:] = 255
mask[:120, :] = 0

frame_no = 0

ret, img = cap.read()
empty_list = []

while frame_no < 4:    
    ret, img = cap.read()
    # print('frame size' + str(fps))
    frameId = int(round(cap.get(1)))
    if frameId % 7 == 0:
        print('frameID :' + str(frameId))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # apply mask
        gray = cv2.bitwise_and(gray, gray, mask = mask)
        
        # image, reject levels level weights.
        cars = car_cascade.detectMultiScale(gray, 1.008, 5)
        
        # add this
        for (x, y, w, h) in cars:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
        frame_no = frame_no + 1
        if frame_no <= 4:
            empty_list.append(len(cars))
        

        print('Processing %d : cars detected : [%s]' % (frame_no, len(cars)))
        #import pdb; pdb.set_trace()
    
        if cv2.waitKey(27) and 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print(*empty_list,sep=",")

###############################################
def operate_led():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    
    # all red initial on
    GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(40, GPIO.OUT, initial=GPIO.HIGH)
    
    # 4 side all pin out mode one by one like loop
    def setupgpio(LED_RED, LED_AMBER, LED_GREEN,wait):
        GPIO.setup(LED_RED, GPIO.OUT)
        GPIO.setup(LED_AMBER, GPIO.OUT)
        GPIO.setup(LED_GREEN, GPIO.OUT)
        wait = (wait * 3)
        
        def green (LED_RED, LED_AMBER, LED_GREEN,wait):
            GPIO.output (LED_RED, LEDOFF)
            print('1.red is off')
            GPIO.output (LED_GREEN, LEDON)
            print('led green for sec',wait)
            time.sleep(wait)
            GPIO.output (LED_GREEN, LEDOFF)
            print('green is off')
            GPIO.output (LED_AMBER, LEDON)
            print('amber is bliunk')
            time.sleep(0.5)
            GPIO.output (LED_AMBER, LEDOFF)
            time.sleep(0.5)
            GPIO.output (LED_AMBER, LEDON)
            time.sleep(0.5)
            GPIO.output (LED_AMBER, LEDOFF)
            time.sleep(0.5)
            print('amber off')
            GPIO.output (LED_AMBER, LEDON)
            time.sleep(0.5)
            GPIO.output (LED_AMBER, LEDOFF)
            time.sleep(0.5)
            GPIO.output (LED_AMBER, LEDON)
            time.sleep(0.5)
            GPIO.output (LED_AMBER, LEDOFF)
            print('red on')
            GPIO.output (LED_RED, LEDON)
        
        green(LED_RED, LED_AMBER, LED_GREEN,wait) 
        
    
    RED = [7, 15, 26, 40]
    AMBER = [5, 13, 24, 38]
    GREEN = [3, 11, 22, 36]
    
    LEDOFF = 0
    LEDON = 1
    
    setupgpio(RED[0],AMBER[0],GREEN[0],empty_list[0])
    setupgpio(RED[1],AMBER[1],GREEN[1],empty_list[1])
    setupgpio(RED[2],AMBER[2],GREEN[2],empty_list[2])
    setupgpio(RED[3],AMBER[3],GREEN[3],empty_list[3])






################################
operate_led()
import http.client as httplib
import urllib
def transmit_data(empty_list):
    # setup_modem()
    key = 'GSRMPHCP3NF0YHZA'
    params = urllib.parse.urlencode({'field1': empty_list[0], 'field2': empty_list[1],'field3': empty_list[2],'field4': empty_list[3],'key':key }) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        print('data transmit')
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        print(data)
        conn.close()
    except:
        print("Connection failed")


######################################
import serial
def setup_modem():
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1) 
    port.flush()
    import pdb; pdb.set_trace()
    port.write(b'AT'+b'\r')
    rcv = port.readline()
    print("setup modem is running")
    return rcv

transmit_data(empty_list)
setup_modem()
