import pyautogui
import time
import sys
from PIL import ImageGrab
import pytesseract
from textblob import TextBlob

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



#GUIDE

#do not move anything around aafter the program has started
#do not move the flaming window from its default position
#windowed option in maplestory must be checked and needs to be windowed to a small resolution
#flame window should be fully uncovered
#should have both the program window and maplestory visible next to each other

#WARNINGS
#the program has a decent possibility to skip over flames that fit the requirement, because image reading is not perfect on this small ass window that has a low ass dpi
#reads int wrong 50% of the time, not good for magic classes
#make sure to have a gigantic stack of flames
#made for 1080p windows 10 monitor




#y is the number of pixels the image is from the top
#x is the number of pixels the image is from the left

#tests if program can work
def setup():
    global tryagaincenter
    global referencex
    global referencey

    #attempts to find the try again button on screen, sets up some values for the mouse moving
    tryagain = pyautogui.locateOnScreen("tryagain.png", confidence = 0.99)
    tryagaincenter = pyautogui.center(tryagain)
    referencewindow = pyautogui.center(pyautogui.locateOnScreen("referencewindow.png", confidence=0.99))
    referencex, referencey = referencewindow
    referencex = int(referencex)
    referencey = int(referencey)

    #prints out accept or deny message
    if tryagain and referencewindow:
        print("everything working well")
        print(referencex, referencey)
    
    else:
        print("could not find the try again button")
        
#creates a dictionary
maindict = {}


#input that stops the program from running automatically
a = input("type ready to start: ")


#if input ready -> let user input first stat and its value
if a.lower() == 'ready':
    stat1 = input("stat1: ")
    stat1val = int(input("stat1 value (greater or equal than): "))
    stat2 = input("stat2: ")
    stat2val = int(input("stat2 value (greater or equal than): "))
    
    print()
    setup()
    print()
    

    key = True
  
else:
    print("restart program")
    key = False


#mainloop
while key:
    #try and except clause for when the image reading inevitably fails
    
    try:
        #uses the reference image to create a snapshot of a box, reads the contents of the box every loop
        screen = ImageGrab.grab(bbox = (referencex - 85, referencey + 125, referencex + 85, referencey + 218)) #(left_x, top_y, right_x, bottom_y)
        text = pytesseract.image_to_string(screen) #converts box content to plain text
        list1 = text.strip().split("\n")

        #reset 
        mainlist = []
        maindict.clear()

        
        #attempts to minimize the damage of incorrect image reading by removing as many of the affecting variables as possible
        for i in list1:
            if i:
                if "Aitack" in i:
                    i = i.replace("Aitack", "Attack")
                if "|" in i:
                    i = i.replace('|', '')

                i = i.replace(':', '')
                mainlist.append(str(TextBlob("".join(i.split())).correct()).strip(',').strip(')').strip('(').strip()) #long ass text correctifier


        #converts the list into an usable and efficient dictionary
        for i in mainlist:
            if '-' not in i:
                a, b = i.split('+')
                b = int(b.strip('+').strip('%'))
                maindict[a] = b
            else:
                a, b = i.split('-')
                b = int(b.strip('-'))
                maindict[a] = b

        #prints maindictionary
        print(maindict)
            
            
        
        #block of code that tests if the flame exists on the screen (sometimes the info is inaccurate)
        if (stat1 in maindict and maindict[stat1] >= stat1val) and (stat2 in maindict and maindict[stat2] >= stat2val):  
            print('found flame')
            sys.exit()
            
        else: #else, keep clicking the try again button
            print('did not find')
            pyautogui.click(tryagaincenter)
            time.sleep(0.05)
            pyautogui.press('enter')
            time.sleep(0.05)
            pyautogui.press('enter')

        #prints newline for organisation and pauses for 2.5 seconds to give the game time to do its dumbass animation
        print() 
        time.sleep(2.5)


    #in the very probable case the image reads completely wrong and the code above does not fix it, comes to except section and goes to next flame
    except Exception:
        print("error: probably image read wrong")
        pyautogui.click(tryagaincenter)
        time.sleep(0.05)
        pyautogui.press('enter')
        time.sleep(0.05)
        pyautogui.press('enter')
        print()
