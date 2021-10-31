import pyautogui
import cv2
from pynput.mouse import Button, Controller
from pynput.mouse import Listener
from pynput import mouse
import os


def make_screenshot():
    position = get_position()

    try:
        size = (position[1][0] - position[0][0], position[1][1] - position[0][1])
        image = pyautogui.screenshot("screen_faces_7327.png", region=(position[0][0], position[0][1], size[0], size[1]))
    except:
        print("Ошибка! Убедитесь что первая точка находится левее и выше чем второя точка\n\n")
        make_screenshot()
        return

    get_objects()


def get_position():
    print("Кликом на правую кнопку мыши, поставьте на экране 2 точки, так, чтобы первая точка была выше и левее второй точки")

    position = []

    global working
    working = True

    while working:

        def on_click(x, y, button, pressed):

            if str(button) == "Button.left" and pressed:
                position.append((x, y))

                if len(position) >= 2:
                    global working
                    working = False
                    return False

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

        listener = mouse.Listener(on_click=on_click)

        listener.start()

    return position


def get_objects():

    face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    haarcascade_frontalcatface = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalcatface.xml")

    image = cv2.imread(f"screen_faces_7327.png")
    os.remove(f"screen_faces_7327.png")

    image_converted = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = 0
    for (x, y, weight, height) in face_cascade_db.detectMultiScale(image_converted, 1.1, 19):
        cv2.rectangle(image, (x, y), (x + weight, y + height), (207, 60, 65), 2)
        faces += 1

    if faces != 0:
        for (x, y, weight, height) in eye_cascade.detectMultiScale(image_converted, 1.1, 19):
            cv2.rectangle(image, (x, y), (x + weight, y + height), (0, 60, 255), 2)

    cats = 0
    for (x, y, weight, height) in haarcascade_frontalcatface.detectMultiScale(image_converted, 1.1, 19):
        cv2.rectangle(image, (x, y), (x + weight, y + height), (176, 28, 235), 2)
        cats += 1


    print(f"\nРезультат:\nОбнаружено:\n - {faces} лиц\n - {cats} котов")
    cv2.imshow('Objects', image)
    cv2.waitKey()


make_screenshot()
