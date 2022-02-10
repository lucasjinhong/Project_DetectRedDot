import io
import cv2
import json
import time
import pybase64
import requests
import datetime
import numpy as np
import paho.mqtt.client as mqtt
from PIL import Image


def http_request(url, payload):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, json.dumps(payload), headers=headers)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


# base64 encode
def base64_encode(orig_frame):
    cv2.imwrite(r'C:\Users\asus\Desktop\MmsLab\Project_DetectRedDot\bb_img.jpg', orig_frame)  # save
    im = Image.open(r'C:\Users\asus\Desktop\MmsLab\Project_DetectRedDot\bb_img.jpg')  # open image
    image_byte_arr = io.BytesIO()  # change format
    im.save(image_byte_arr, format='JPEG')

    img_base64 = pybase64.b64encode(image_byte_arr.getvalue()).decode('ascii')  # 編碼並採用ascii

    return img_base64


def main():
    # 選擇第二隻攝影機
    cap = cv2.VideoCapture(0)

    # HSV red filter
    lower = np.array([110, 43, 46])
    upper = np.array([130, 255, 255])

    # MQTT setting
    client = mqtt.Client()
    client.username_pw_set("", "")  # 設定登入帳號密碼
    client.connect("140.124.73.217", 1883, 60)  # 設定連線資訊(IP, Port, 連線時間)

    wait = 0

    while True:
        red_count = 0

        # 從攝影機擷取一張影像
        _, frame = cap.read()
        orig_frame = frame.copy()
        img = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img, lower, upper)

        # Drawing Bounding Boxes Around Detected Objects
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        '''
        draw the contours, not strictly necessary
        for i, cnt in enumerate(contours):
        cv2.drawContours(frame, contours, i, (225, 225, 255), 3)
        '''

        for contour in contours:
            '''
            continue through the loop if contour area is less than area...
            ... helps in removing noise detection
            if cv2.contourArea(contour) < area:
            continue
            '''

            # get the xmin, ymin, width, and height coordinates from the contours
            (x, y, w, h) = cv2.boundingRect(contour)

            # draw the bounding boxes
            cv2.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            red_count += 1

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(orig_frame, str(red_count), (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # 顯示圖片
        cv2.imshow('Detected Objects', orig_frame)
        cv2.imshow('mask', mask)
        cv2.imshow('img', img)
        # cv2.imshow('frame', frame)

        # output image

        # imgResize = cv2.resize(orig_frame, (280, 210))

        if wait < 50:
            wait += 1

        else:
            payload = {'color': 'red', 'value': red_count, 'time': str(datetime.datetime.now()),
                       'imgBase64': base64_encode(orig_frame)}
            url = "http://localhost:4000/red"

            # Send http request
            if red_count > 0:
                http_request(url, payload)

            # mqtt publish
            client.publish("NTUT/Find-red", json.dumps(payload))

            wait = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # 釋放攝影機
    cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗


if __name__ == '__main__':
    main()
