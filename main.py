#######################################################

'''
This script is the main program of SMART GLASSES PROJECT
It check if a object is present in front of the class and
if so then it takes a photo of the object and reads the text
present in that image

AUTHOR : Gautam S Patil (BE CSE 8th Sem)

Ultrasonic sensor connection
VCC to Pin 2 (VCC)
GND to Pin 6 (GND)
TRIG to Pin 12 (GPIO18)
connect the 330Ω resistor to ECHO.  
On its end you connect it to Pin 18 (GPIO24) 
and through a 470Ω resistor you connect it also to Pin6 (GND).
Please refer to connections folder for the diagram

OBJECT_DETECTED_LED is connection to PIN --> 7
which blinks for 2 seconds if any object is detected

'''

################################################################



#Libraries
import RPi.GPIO as GPIO
import time
from espeak import espeak
from picamera import PiCamera
from PIL import Image
import pytesseract

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
OBJECT_DETECTED_LED = 7
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(OBJECT_DETECTED_LED, GPIO.OUT)

#camera object
camera = PiCamera()

#Minimum distance at which object must be detected
MAX_DISTANCE = 4      #4cm

#Path of capture image
imagePath = '/home/pi/Desktop/SmartGlasses/snaps/object.jpg'


def getDistance():
    '''
     This function calculates the distance of any object
     from the ultrasonic sensor
     
     params : None
     return value :  float value representing calculated distance
    '''
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def takephoto(imagePath):
    '''
     This function takes the photo using raspberry pi
     camera and saves the image at the given path.
     
     params : string path at which the captured image will be saved
              must be stored.
     return value : None
    '''
    global camera
    
    #starts the camera
    camera.start_preview()
    
    #waits for 4 seconds
    time.sleep(4)
    
    #captures the image
    camera.capture(imagePath)
    
    #stops the camera
    camera.stop_preview()

def speak(text):
    '''
     This function is responsible for giving audio output.
     It converts text to audio form
     
     params : String which represents the text 
     return value : None
    '''
    
    espeak.synth(text)

def convertImageToText(imagePath):
    '''
     This function extracts the text from the image
     
     params : String path of the image of which text should
             should be extracted
     return value : String which contains the extracted text
    '''
    
    text = pytesseract.image_to_string(Image.open(imagePath), lang="eng")
    
    return text

while(True):
    #check if any object is placed in front by calculating distance
    distance = getDistance()
    if(distance < MAX_DISTANCE):
        GPIO.output(OBJECT_DETECTED_LED, True)
        speak("Object Detected")
        time.sleep(2)
        GPIO.output(OBJECT_DETECTED_LED, False)
        speak("Taking Photo in 4 seconds please hold the object steady")
        takephoto(imagePath)
        text = convertImageToText(imagePath)
        speak(text)
    
    time.sleep(1)    
        
        
        
        
    