#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import os


def toggle_screen_off():
    os.system('xscreensaver-command -activate')
    return False


def toggle_screen_on():
    os.system('xscreensaver-command -deactivate')
    return True


def check_for_activity():
    if (GPIO.input(GPIO_PIR) == 1):
        return True
    else:
        return False


def count():
    # lastTime = time.time()
    # elapsedTime = 0
    counted = 0
    # while elapsedTime < 1.0:
    while True:
        if GPIO.input(GPIO_PIR) == 1:
            # currentTime = time.time()
            # elapsedTime = currentTime - lastTime
            counted += 1
        else:
            counted = 0
            # else:
            # print(counted)
            # print('STOP')


def main():
    GPIO.setmode(GPIO.BOARD)

    global GPIO_PIR
    GPIO_PIR = 7

    global counted
    counted = 0

    print("Bewegungsmelder (CTRL-C zum Beenden)")
    print("====================================")

    GPIO.setup(GPIO_PIR, GPIO.IN)

    lastTime = time.time()
    status = toggle_screen_off()

    # count()
    count_log = open('count_log.txt', 'a')

    try:
        while True:
            activity = check_for_activity()

            if activity:
                counted += 1
            if activity and counted > 350000:
                # counted += 1
                if not status:
                    status = toggle_screen_on()
                lastTime = time.time()
            elif (not activity) and (counted > 0):
                # print('print')
                # count_log.write(str(counted) + '\n')
                counted = 0

            # if GPIO.input(GPIO_PIR) == 1:
            #    counted += 1
            # elif (counted != 0) and (GPIO.input(GPIO_PIR) != 1):
            #    counted = 0

            currentTime = time.time()
            elapsedTime = currentTime - lastTime  # elapsed time since the last motion was detected
            # print(elapsedTime)
            # print(counted)

            if elapsedTime > 10.0:
                # print("No Activity detected")
                if status:
                    status = toggle_screen_off()
    except KeyboardInterrupt:
        GPIO.cleanup()
        count_log.close()


if __name__ == '__main__':
    main()