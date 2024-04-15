import cv2
import numpy as np
import pyautogui
import keyboard
import time
import socket

def capture_screen():
    # 抓取屏幕
    screenshot = pyautogui.screenshot()
    # 将图片转换为numpy数组
    frame = np.array(screenshot)
    # 将图片从BGR转换为RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 压缩图片大小
    frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
    return frame

# 1.创建socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 增加缓冲区
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)

# 2. 链接服务器
server_addr = ("182.92.122.137", 32771)
tcp_socket.connect(server_addr)

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

    # 每隔100秒抓取屏幕
    if time.time() - start_time >= 1000:
        cap = capture_screen()
        print("captured automatically")
        start_time = time.time()  # 重置计时器

    if cap is not None:
        # 将图像转换为JPEG格式
        retval, buffer = cv2.imencode('.jpg', cap)
        jpg_as_text = buffer.tobytes()

        try:
            # 将图像发送到服务器
            tcp_socket.sendall(jpg_as_text)  # 使用sendall一次性发送整个图像
            print("Image sent to the server")

        except socket.error as e:
            print("Something went wrong", e)

# 3. 关闭套接字
tcp_socket.close()
