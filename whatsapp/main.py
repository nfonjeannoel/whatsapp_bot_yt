import pyautogui as pt
from time import sleep
import pyperclip
import random

sleep(5)

position1 = pt.locateOnScreen("smiley_paperclip.png", confidence=.5)
x = position1[0]
y = position1[1]


# gets message
def get_message():
    global x, y

    position = pt.locateOnScreen("smiley_paperclip.png", confidence=.6)
    x = position[0]
    y = position[1]
    pt.moveTo(x, y, duration=.5)
    pt.moveTo(x + 70, y - 100, duration=.5)
    pt.tripleClick()
    pt.rightClick()
    pt.moveRel(20, -140, duration=1)
    pt.click()
    whatsapp_message = pyperclip.paste()
    pt.click()
    print("message received " + whatsapp_message)
    return whatsapp_message


# post
def post_response(message):
    global x, y
    position = pt.locateOnScreen("smiley_paperclip.png", confidence=.6)
    x = position[0]
    y = position[1]
    pt.moveTo(x + 200, y + 10, duration=1)
    pt.click()
    pt.typewrite(message, interval=.01)


#  pt.typewrite("\n", interval=.01)

# processes response
def process_response(message):
    random_no = random.randrange(3)

    if "?" in str(message).lower():
        return "Don't ask me any questions!"
    else:
        if random_no == 0:
            return "Thats cool"
        elif random_no == 1:
            return "interesting. ok"
        else:
            return "talk later."


# check for  new messages
def check_for_new_messages():
    pt.moveTo(x + 80, y - 35, duration=1)

    while True:
        # continuosly check green dot and new messages
        try:
            position = pt.locateOnScreen("green_circle.png", confidence=0.7)

            if position is not None:
                pt.moveTo(position)
                pt.moveRel(-100, 0)
                pt.click()
                sleep(.5)
        except(Exception):
            print("no new messages")

        if pt.pixelMatchesColor(int(x + 80), int(y - 35), (56, 56, 56), tolerance=10):
            print("it is black")
            processed_message = process_response(get_message())
            post_response(processed_message)
        else:
            print("no new messages")


check_for_new_messages()
