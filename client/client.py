import cv2
import numpy as np
import pyautogui
import keyboard
import time
import socket
from tkinter import Tk, Canvas

# 设置超时时间和最大重试次数
timeout = 1000
max_retries = 3

# 热键
hotkey = 'F12'

# # TCP
# tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)
#
# # 服务器网络参数
# server_addr = ("182.92.122.137", 32771)
# tcp_socket.connect(server_addr)


def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # # 直接压缩图片大小，效果不好
    # frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
    return frame


def capture_selected():
    root = Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.2)  # 设置不透明度为20%
    root.wait_visibility(root)
    root.configure(background='grey')  # 设置背景颜色为灰色
    root.lift()  # 置于顶层
    canvas = Canvas(root, bg='grey')
    canvas.pack(fill='both', expand=True)

    def on_start(event):
        global rect, start_x, start_y
        start_x, start_y = pyautogui.position()
        rect = canvas.create_rectangle(0, 0, 0, 0, outline='green', fill='green')  # 设置选择框的颜色为绿色

    def on_drag(event):
        cur_x, cur_y = pyautogui.position()
        canvas.coords(rect, start_x, start_y, cur_x, cur_y)
        canvas.itemconfig(rect, fill='')  # 设置选择框的填充颜色为空，即透明

    def on_release(event):
        root.quit()

    canvas.bind('<Button-1>', on_start)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)

    root.mainloop()
    root.destroy()

    region = (min(start_x, pyautogui.position()[0]), min(start_y, pyautogui.position()[1]),
              abs(start_x - pyautogui.position()[0]), abs(start_y - pyautogui.position()[1]))
    return capture_screen(region)

print(f"按下 {hotkey} 键来选择截图范围")

while True:


    start_time = time.time()

    cap = None

    # 检测热键截图
    if keyboard.is_pressed(hotkey):
        cap = capture_selected()
        print("captured from selected region")
        start_time = time.time()

    # 每隔一段时间捕获全屏
    if time.time() - start_time >= 1000:
        cap = capture_screen()
        print("captured automatically")
        start_time = time.time()

    # 抓到图了！
    if cap is not None:
        # 最后一个参数用来压缩，1-100
        retval, buffer = cv2.imencode('.jpg', cap, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
        jpg_as_text = buffer.tobytes()

        # 保存图片
        with open('debug_pic.jpg', 'wb') as f:
            f.write(buffer)

        # 添加一个标志位来跟踪是否已经达到最大重试次数
        connection_failed = False

        # 标志图片发送是否成功
        image_is_received = False

        # 发出去！
        while True:
            # 连不上break
            if connection_failed:
                break

            # 已经发成功break
            if image_is_received:
                break

            # 在每次循环开始时创建一个新的套接字
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)

            # 服务器网络参数
            server_addr = ("182.92.122.137", 32771)
            try:
                tcp_socket.connect(server_addr)
            except socket.error as e:
                print("Something went wrong when connecting", e)
                connection_failed = True
                break

            retries = 0
            while retries < max_retries:
                try:
                    # 发送心跳信息
                    tcp_socket.sendall('HEARTBEAT'.encode())
                    data = tcp_socket.recv(1024)
                    if data.decode() != 'HEARTBEAT_ACK':
                        print("Heartbeat failed, connection might be lost")
                        connection_failed = True
                        break

                    # 在发送图片数据前，先发送一个标识符
                    tcp_socket.sendall('IMAGE_DATA'.encode())
                    tcp_socket.sendall(jpg_as_text)
                    print("Image sent to the server")
                    # 等一下图片送到
                    time.sleep(1)
                    tcp_socket.sendall('IMAGE_END'.encode())  # 添加结束标识符
                    print("image end")
                    # 等待服务端的确认信息
                    data = tcp_socket.recv(1024)
                    if data.decode() == 'IMAGE_RECEIVED':
                        image_is_received = True
                        print("Server has received the image")
                        break
                    else:
                        print("Server has not received the image, resending...")
                        retries += 1

                    # # 等待服务端的结果
                    # response = tcp_socket.recv(1024)
                    # if response.decode():
                    #     print("got response:",response)
                    #     break
                    # else:
                    #     print("Server has not sent response.")
                    #     retries += 1

                except socket.timeout:
                    print("Timeout, resending...")
                    retries += 1
                except socket.error as e:
                    print("Something went wrong", e)
                    break

            if retries == max_retries:
                print("Connection failed after maximum retries, stop sending images")
                connection_failed = True

            tcp_socket.close()
