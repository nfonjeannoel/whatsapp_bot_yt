import pyautogui as pt
from time import sleep
import pyperclip
import random

# pagezoom = 54
lines = []
prevLine = ""

x_col1 = 540
x_col2 = 750
y_colxy = 150

# page_number = 0

skips = 95

centers = []
centerId = -1
paperCounter = 0
isNewCenter = True
counter = 0
sameLine = 0
oldLine = ""

newNameFlag = False
nameBuilder = ""


def changePageNumber(page_number):
    # x = 565
    # y = 100
    # global page_number
    # page_number += 1
    pt.moveTo(x_col1 + 25, y_colxy - 50)
    pt.leftClick()
    pt.typewrite(str(page_number), interval=.00001)
    pt.moveRel(-50, 0)
    pt.click()


def goToFirstColumn():
    pt.moveTo(x_col1, y_colxy)
    for i in range(skips):
        pt.tripleClick()
        smallWait()
        getLineText()
        moveDown()


def getLineText():
    thisLine = copy_clipboard()
    # global prevLine
    # prevLine = thisLine
    addToList(thisLine)
    # print(line)


def moveDown():
    pt.moveRel(0, 6.9, 0.0001)


def smallWait():
    sleep(0.0001)


def addToList(thisLine):
    global prevLine
    if prevLine == thisLine:
        # print("duplicate")
        None
    else:
        # print("not equal")
        lines.append(thisLine)
        prevLine = thisLine


def goToSecondColumn():
    pt.moveTo(x_col2, y_colxy)
    for i in range(skips):
        pt.tripleClick()
        smallWait()
        getLineText()
        moveDown()


def copy_clipboard():
    pt.hotkey('ctrl', 'c')
    sleep(.001)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()


def getResults():
    sleep(10)
    print("start")
    for i in range(2):
        changePageNumber(i + 1)
        goToFirstColumn()
        goToSecondColumn()
    with open("result.txt", "w") as f:
        for line in lines:
            f.write(line)
    f.close()
    print("done")



