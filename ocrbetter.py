from PIL import Image
import pytesseract
import playsound
import argparse
import cv2
import os
#import pyttsx3
from gtts import gTTS
from langdetect import detect
import os
import time


def input():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
	    help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="blur",
	    help="type of preprocessing to be done")
    args = vars(ap.parse_args())
    return args
    


def image_processing(args): 
    #must write image processing code here
    image = cv2.imread(args['image'])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    print(gray)
    gray=cv2.Canny(gray,100,200)
    #print("after canny")
    print(gray)
    #writing to new file
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    return filename


def read_image(filename):
    text = pytesseract.image_to_string(Image.open(filename),lang='eng')
    
    language=detect(text)
    if language!='en':
        text = pytesseract.image_to_string(Image.open(filename),lang='hin')
        language=detect(text)
        print(language)
        if language=='hi':
            tts = gTTS(text=text, lang='hi')
            tts.save("output.mp3")
        else:
            text="unrecognised language, make sure you are holding the reading material properly, or the language is either hindi or english."
            tts = gTTS(text=text, lang='hi')
            tts.save("output.mp3")
    else:
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
    
    os.remove(filename)
    print(language)
    print(text)


def read_out():
    playsound.playsound(os.getcwd()+"/output.mp3", True)
    os.remove('output.mp3')


processed_filename=image_processing(input())
#read_image(processed_filename)
#time.sleep(2)
#read_out()