from PIL import Image
import pytesseract

# 如果 tesseract 可执行文件不在 PATH 中，需要指定路径
pytesseract.pytesseract.tesseract_cmd = r'D:/CV/tesseractOCR/tesseract.exe'


# 从图像中提取文本和坐标
def ocr_image_with_coordinates(image_path):
    image = Image.open(image_path)
    # 自动识别语言
    text = pytesseract.image_to_string(image)
    # 获取每个字符的坐标
    coordinates = pytesseract.image_to_boxes(image)
    return text, coordinates


if __name__ == '__main__':
    screenshot_text, screenshot_coordinates = ocr_image_with_coordinates('test.png')
    print("提取的文本：")
    print(screenshot_text)
    print("\n每个字符的坐标：")
    print(screenshot_coordinates)
