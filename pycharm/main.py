import cv2
import datetime
import numpy as np
import json
import paho.mqtt.client as mqtt
import torch

import http_mqtt
import encode_base64
import cam_image


def main():
    # 選擇第二隻攝影機
    cap = cv2.VideoCapture(0)

    # HSV red filter
    lower = np.array([150, 150, 150])
    upper = np.array([180, 255, 255])

    http_url = "http://localhost:4000/red"

    # mqtt 設定
    topic = "NTUT/Find-red"
    client = mqtt.Client()
    client.username_pw_set('', '')  # 設定登入帳號密碼
    client.connect("140.124.73.217", 1883, 180)  # 設定連線資訊(IP, Port, 連線時間)

    model = torch.hub.load('ultralytics/yolov5', 'yolov5n')

    wait = 0

    while True:
        red_count = 0

        # 影像處理
        orig_frame, red_count, g_blur = cam_image.image_process(cap, lower, upper, red_count).process()

        cv2.imshow('Detected Objects', orig_frame)
        cv2.imshow('g_blur', g_blur)

        result = model(orig_frame)
        result.show()

        if wait < 50:
            wait += 1

        else:
            payload = {'color': 'red', 'value': red_count,
                       'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       'imgBase64': encode_base64.encode(orig_frame)
                       }

            # Send http request
            if red_count > 0:
                http_mqtt.send_http(http_url, payload).http_request()

            # mqtt publish
            client.publish(topic, json.dumps(payload))

            wait = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # 釋放攝影機
    cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗


if __name__ == '__main__':
    main()
