import cv2
import requests
import numpy as np
import pyautogui
import keyboard
import time

# 捕获图像
# 从摄像头
# cap = cv2.VideoCapture(0)
#从屏幕
def capture_screen():
    # 抓取屏幕
    screenshot = pyautogui.screenshot()
    # 将图片转换为numpy数组
    frame = np.array(screenshot)
    # 将图片从BGR转换为RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

# 设置热键
hotkey = 'F12'

print(f"按下 {hotkey} 键来抓取屏幕")

# 初始化时间
start_time = time.time()

cap = None  # 初始化 cap 变量

while True:
    # 如果按下热键，则抓取屏幕
    if keyboard.is_pressed(hotkey):
        cap = capture_screen()
        print("captured from hotkey")
        start_time = time.time()  # 重置计时器

    # 每隔10秒抓取屏幕
    if time.time() - start_time >= 10:
        cap = capture_screen()
        print("captured automatically")
        start_time = time.time()  # 重置计时器

    if cap is not None:
        # 将图像转换为JPEG格式
        retval, buffer = cv2.imencode('.jpg', cap)
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
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong", err)
