# -*- coding: utf-8 -*-

from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

confidenceRating = 0.90

# generates a random sleep interval in milliseconds
def rngSleep(min, max):
    time.sleep(random.randint(min, max)/1000)

# clicks at the (X, Y) position on the screen
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    rngSleep(20, 50)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def doubleClick(x, y):
    click(x,y)
    rngSleep(100, 200)
    click(x,y)

def getClickPosition(target):
    retryCount = 0
    position = pyautogui.locateOnScreen(target, grayscale = True, confidence = confidenceRating)
    while position == None and retryCount <= 3:
        position = pyautogui.locateOnScreen(target, grayscale = True, confidence = confidenceRating)
        retryCount += 1
        rngSleep(100, 200)
    return pyautogui.center(position)

def buyBookmark(position, buyButton):
    bookmarkPoint = pyautogui.center(position)
    doubleClick(bookmarkPoint[0] + 800, bookmarkPoint[1] + 50)
    rngSleep(300, 400)
    buyPoint = getClickPosition(buyButton)
    doubleClick(buyPoint[0], buyPoint[1])
    rngSleep(300, 400)

def buyRefresh(refreshButton, confirmButton):
    point = getClickPosition(refreshButton)
    doubleClick(point[0], point[1])
    rngSleep(300, 400)
    point = getClickPosition(confirmButton)
    doubleClick(point[0], point[1])
    rngSleep(1000, 1500)

#Aprox place X: 1263 Y:  590
scrollState = 0
covenantCount = 0
mysticCount = 0
refreshCount = 0

# waits for 5 seconds after start
time.sleep(5)
covenantDetected = 0
mysticDetected = 0
while keyboard.is_pressed('q') == False:
    try:
    # finds the position of covenant bookmarks
        covenantPos = pyautogui.locateOnScreen("covenant.PNG", grayscale = True, confidence = 0.85)
    # finds the position of mystic bookmarks
        mysticPos = pyautogui.locateOnScreen("mystic.PNG", grayscale = True, confidence = 0.85)
        print("Covenant Position: ", covenantPos, " | Mystic Position: ", mysticPos)

    # check for covenant
        if (covenantPos) != None and covenantDetected == 0:
            print("Buy Covenant Summons.")
            buyBookmark(covenantPos, "buy_covenant.PNG")
            scrollState = 0
            covenantCount += 1
            covenantDetected += 1
            print("Covenant Summons bought=", covenantCount)
        else:
            print("No Covenant summons to buy.")
            
    # check for mystics
        if (mysticPos) != None and mysticDetected == 0:
            print("Buy Mystic Summons.")
            buyBookmark(mysticPos, "buy_mystic.PNG")
            scrollState = 0
            mysticCount += 1
            mysticDetected += 1
            print("Mystic Summons bought=", mysticCount)
        else:
            print("No Mystic summons to buy.")

    # scroll if nothing found
        if scrollState < 1 :
            click(x=1263, y = 590)
            pyautogui.scroll(-5, x=1263, y=590)
            scrollState += 1
            rngSleep(1000, 1500)
    # refresh after scrolling
        elif scrollState == 1 :
            buyRefresh("refresh.PNG", "confirm.PNG")
            covenantDetected = 0
            mysticDetected = 0
            scrollState = 0
            refreshCount += 1
            print("Refreshes: ", refreshCount, " | Covenant :", covenantCount * 5, " | Mystic : ", mysticCount * 50)
    except TypeError:
        print("Unable to locate set sprite, retrying from last successful state")
print("Q key is held down! Exiting.")