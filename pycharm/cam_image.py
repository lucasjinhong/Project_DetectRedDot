import cv2
import numpy as np


class image_process:
    def __init__(self, cap, lower, upper, red_count):
        self.cap = cap
        self.lower = lower
        self.upper = upper
        self.red_count = red_count

    def process(self):
        # 從攝影機擷取一張影像
        kernel_sharpening = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])

        _, frame = self.cap.read()
        orig_frame = frame.copy()
        blur_image = cv2.GaussianBlur(orig_frame, (21, 21), 0)
        img = cv2.cvtColor(blur_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img, self.lower, self.upper)

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
            self.red_count += 1

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(orig_frame, str(self.red_count), (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        return orig_frame, self.red_count

        # 顯示圖片

        # cv2.imshow('mask', mask)
        # cv2.imshow('img', img)
        # cv2.imshow('frame', frame)

        # imgResize = cv2.resize(orig_frame, (280, 210))

