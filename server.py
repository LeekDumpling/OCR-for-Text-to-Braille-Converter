"""
服务器端代码。
监听5000端口上的POST请求,使用Flask接收图像。
当收到一个包含图像的请求时，运行OCR代码，并将结果返回给客户端。
目前返回的参数是一个字典，键值包括文本和坐标。
"""

from PIL import Image
import pytesseract
import io
import os
from flask import Flask, request
import traceback

app = Flask(__name__)
# 设置tesseract.exe的路径，保存在.env文件中
tesseract_path = os.getenv('TESSERACT_PATH')
pytesseract.pytesseract.tesseract_cmd = tesseract_path


# 定义一个路由，用于处理POST请求
@app.route('/ocr', methods=['POST'])
def ocr_image_with_coordinates():
    try:
        # 从请求中获取图像文件
        file = request.files['image']
        # 打开图像文件
        image = Image.open(io.BytesIO(file.read()))
        # 保存图像以进行调试
        image.save('debug_image.jpg')
        # 使用pytesseract库提取图像中的文字
        text = pytesseract.image_to_string(image)
        # 使用pytesseract库获取每个字符的坐标
        coordinates = pytesseract.image_to_boxes(image)
        # 将提取的文字和坐标返回给客户端
        return {'text': text, 'coordinates': coordinates}
    except Exception as e:
        # 如果出现异常，打印错误信息和堆栈跟踪
        print("Error: ", str(e))
        print(traceback.format_exc())
        return {'error': str(e)}, 500



if __name__ == '__main__':
    # 启动服务器，监听5000端口，打开debug
    app.run(host='0.0.0.0', port=5000, debug=True)

