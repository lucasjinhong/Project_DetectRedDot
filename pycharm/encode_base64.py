import io
import cv2
import pybase64
from PIL import Image


# base64 encode
def encode(orig_frame):
    cv2.imwrite(r'C:\Users\asus\Desktop\MmsLab\Project_DetectRedDot\bb_img.jpg', orig_frame)  # save
    im = Image.open(r'C:\Users\asus\Desktop\MmsLab\Project_DetectRedDot\bb_img.jpg')  # open image
    image_byte_arr = io.BytesIO()  # change format
    im.save(image_byte_arr, format='JPEG')

    img_base64 = pybase64.b64encode(image_byte_arr.getvalue()).decode('ascii')  # 編碼並採用ascii

    return img_base64
