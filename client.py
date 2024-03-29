"""
客户端代码。
用于捕获图像，将图像发送到服务器，并接收处理结果。
目前是调用的摄像头
"""

import cv2
import requests
import numpy as np

# 捕获图像
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

# 将图像转换为JPEG格式
retval, buffer = cv2.imencode('.jpg', frame)
jpg_as_text = buffer.tobytes()

# 将图像发送到服务器
response = requests.post('http://your_server_ip:5000/ocr', files={'image': jpg_as_text})

# 打印服务器的响应
print(response.json())



