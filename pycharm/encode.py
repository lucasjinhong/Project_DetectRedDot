from PIL import Image
import base64,io

scale = 0.3

def tobase64(img):
	return base64.b64encode(img).decode('ascii')

def imgResize(img, scale=1):
	height, width = img.size
	return img.resize((int(height*scale), int(width*scale)), Image.BILINEAR)

def main():
	#開啟檔案
	im = Image.open('test.png')
	#檔案變更尺寸
	rs_im = imgResize(im, 0.3)

	#格式轉換
	imgByteArr = io.BytesIO()
	rs_im.save(imgByteArr, format='PNG')

	#編碼並採用ascii
	encode = tobase64(imgByteArr.getvalue())

	#存檔
	f = open("base64.txt", "w")
	f.write(encode);

if __name__ == '__main__':
    main()
