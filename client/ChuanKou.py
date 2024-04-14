import serial
from time import sleep

# 开启串口
serial = serial.Serial('COM3', 9600, timeout=0.5)
if serial.isOpen():
    print("open success")
else:
    print("open failed")


def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
        sleep(0.02)
    return data


def send(send_data):
    if (serial.isOpen()):
        serial.write(send_data.encode('utf-8'))  # 编码
        print("发送成功", send_data)
    else:
        print("发送失败！")


def chuankou(send_data):
    # 这里如果不加上一个while True，程序执行一次就自动跳出了
    # 二注：客户端也有一个无限循环，作为函数调用方便先把while true去掉
    # while True:
    #     # a = input("输入要发送的数据：")
    #     send(send_data)
    #     sleep(0.5)  # 起到一个延时的效果
    #     data = recv(serial)
    #     if data != '':
    #         print("receive : ", data)
    #         if data == b'x':
    #             print("exit")
    #             break

    # 发送数据
    send(send_data)
    sleep(0.5)  # 起到一个延时的效果
    data = recv(serial)
    if data != '':
        print("receive : ", data)
        if data == b'x':
            print("exit")


if __name__ == '__main__':
    chuankou("111100")
