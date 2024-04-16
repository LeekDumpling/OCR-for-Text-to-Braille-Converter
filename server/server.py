import socketserver
import socket
import pytesseract
from PIL import Image
import io
import traceback
import json
import MangWen
import time

# 单片机的IP地址和端口号
microcontroller_ip = '192.168.1.100'    # 瞎填的
microcontroller_port = 12345

# 创建一个socket对象
microcontroller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到单片机
microcontroller_socket.connect((microcontroller_ip, microcontroller_port))

class MyTCPHandler(socketserver.BaseRequestHandler):
    def send_to_microcontroller(self, binary_text):
        # 用前面那个连接到单片机的socket对象
        for char in binary_text:
            microcontroller_socket.send(char.encode())
            time.sleep(0.5)  # 每个字符发送后等待0.5秒
        print("盲文数据发送完毕")

    def handle(self):
        data = b''  # 初始化一个变量来保存数据
        while True:  # 添加循环以处理多个请求
            try:
                # 接收图像数据
                chunk = self.request.recv(1024)
                if not chunk:
                    break  # 如果没有更多的数据被接收，就跳出循环
                data += chunk  # 将接收到的数据添加到总数据中
            except Exception as e:
                print("Error: ", str(e))
                print(traceback.format_exc())
                response = {'error': str(e)}
                self.request.sendall(json.dumps(response).encode())
                return  # 如果发生错误，返回以退出函数

        # 在接收到所有数据后，处理图像
        try:
            image = Image.open(io.BytesIO(data))
            image.save('debug_image.jpg')
            print('image saved')
            text = pytesseract.image_to_string(image)
            coordinates = pytesseract.image_to_boxes(image)  # 获取文本对应的坐标，暂时没用到
            binary_text = MangWen.ascii_to_braille(text)    # 转盲文
            response = {'text': text, 'coordinates': coordinates, 'binary_text': binary_text}
            print('text:', response['text'], 'binary_text:', response['binary_text'])
            self.request.sendall(json.dumps(response).encode())
            self.send_to_microcontroller(response['binary_text'])  # 调用前面的发送方法
        except Exception as e:
            print("Error: ", str(e))
            print(traceback.format_exc())
            response = {'error': str(e)}
            self.request.sendall(json.dumps(response).encode())



if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 32771
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # 允许在端口仍处于TIME_WAIT状态时重新使用端口
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.serve_forever()
