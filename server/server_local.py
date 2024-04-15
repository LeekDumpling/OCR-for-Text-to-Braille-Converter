"""
服务器端代码。
监听5000端口上的POST请求,使用Flask接收图像。
当收到一个包含图像的请求时，运行OCR代码，并将结果返回给客户端。
目前返回的参数是一个字典，键值包括文本和坐标。
"""

import MangWen
from PIL import Image
import pytesseract
import io
import os
from flask import Flask, request
import traceback
import serial
from time import sleep

# # 串口通信
# serial = serial.Serial('COM3', 9600, timeout=0.5)
# if serial.isOpen() :
#     print("open success")
# else :
#     print("open failed")

app = Flask(__name__)
# 设置tesseract.exe的路径，保存在.env文件中
tesseract_path = os.getenv('TESSERACT_PATH')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
        sleep(0.02)
    return data

def send(serial, send_data):
    if (serial.isOpen()):
        serial.write(send_data.encode('utf-8'))  # 编码
        print("发送成功", send_data)
    else:
        print("发送失败！")

@app.route('/ocr', methods=['POST'])
def ocr_image_with_coordinates():
    try:
        file = request.files['image']
        image = Image.open(io.BytesIO(file.read()))
        image.save('debug_image.jpg')
        text = pytesseract.image_to_string(image)
        coordinates = pytesseract.image_to_boxes(image)
        binary_text = MangWen.ascii_to_braille(text)
        # for i in range(0, len(binary_text), 6):
        #     send(serial, binary_text[i:i+6])
        #     sleep(0.5)
        return {'text': text, 'coordinates': coordinates, 'binary_text': binary_text}
    except Exception as e:
        print("Error: ", str(e))
        print(traceback.format_exc())
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

