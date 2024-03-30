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




try:
    # 将图像发送到服务器
    response = requests.post('http://localhost:5000/ocr', files={'image': jpg_as_text})

    # 检查服务器的响应状态
    response.raise_for_status()

    # 尝试解析服务器的响应为JSON
    try:
        data = response.json()
        # 打印响应
        print(data)
    except ValueError:
        print("服务器的响应不是有效的JSON格式")

except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
except requests.exceptions.RequestException as err:
    print ("Something went wrong",err)


