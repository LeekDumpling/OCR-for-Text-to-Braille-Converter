# 定义ASCII字符到盲文点数的映射
braille_mapping = {
    ' ': [0, 0, 0, 0, 0, 0], '!': [0, 1, 1, 1, 0, 1], '"': [0, 0, 0, 0, 1, 0],
    '#': [0, 0, 1, 1, 1, 1], '$': [1, 1, 0, 1, 0, 1], '%': [1, 0, 0, 1, 0, 1],
    '&': [1, 1, 1, 1, 0, 1], "'": [0, 0, 1, 0, 1, 0], '(': [1, 1, 1, 0, 1, 1],
    ')': [0, 1, 1, 1, 1, 1], '*': [1, 0, 0, 0, 0, 1], '+': [0, 1, 1, 0, 1, 0],
    ',': [0, 0, 0, 0, 0, 1], '-': [0, 0, 1, 0, 0, 1], '.': [0, 0, 0, 1, 0, 1],
    '/': [0, 0, 1, 1, 0, 0], '0': [0, 0, 1, 0, 1, 1], '1': [0, 1, 0, 0, 0, 0],
    '2': [0, 1, 1, 0, 0, 0], '3': [0, 1, 0, 0, 1, 0], '4': [0, 1, 0, 0, 1, 1],
    '5': [0, 1, 0, 0, 0, 1], '6': [0, 1, 1, 0, 1, 0], '7': [0, 1, 1, 0, 1, 1],
    '8': [0, 1, 1, 0, 0, 1], '9': [0, 0, 1, 0, 1, 0], ':': [1, 0, 0, 0, 1, 1],
    ';': [0, 0, 0, 0, 1, 1], '<': [1, 1, 0, 0, 0, 1], '=': [1, 1, 1, 1, 1, 1],
    '>': [0, 0, 1, 1, 1, 0], '?': [1, 0, 0, 1, 1, 1], '@': [0, 0, 0, 1, 0, 1],
    'A': [1, 0, 0, 0, 0, 0], 'B': [1, 1, 0, 0, 0, 0], 'C': [1, 0, 0, 1, 0, 0],
    'D': [1, 0, 0, 1, 1, 0], 'E': [1, 0, 0, 0, 1, 0], 'F': [1, 1, 0, 1, 0, 0],
    'G': [1, 1, 0, 1, 1, 0], 'H': [1, 1, 0, 0, 1, 0], 'I': [0, 1, 0, 1, 0, 0],
    'J': [0, 1, 0, 1, 1, 0], 'K': [1, 0, 1, 0, 0, 0], 'L': [1, 1, 1, 0, 0, 0],
    'M': [1, 0, 1, 1, 0, 0], 'N': [1, 0, 1, 1, 1, 0], 'O': [1, 0, 1, 0, 1, 0],
    'P': [1, 1, 1, 1, 0, 0], 'Q': [1, 1, 1, 1, 1, 0], 'R': [1, 1, 1, 0, 1, 0],
    'S': [0, 1, 1, 1, 0, 0], 'T': [0, 1, 1, 1, 1, 0], 'U': [1, 0, 1, 0, 0, 1],
    'V': [1, 1, 1, 0, 0, 1], 'W': [0, 1, 0, 1, 1, 1], 'X': [1, 0, 1, 1, 0, 1],
    'Y': [1, 0, 1, 1, 1, 1], 'Z': [1, 0, 1, 0, 1, 1], '|': [0, 0, 1, 1, 0, 1],
    '[': [0, 1, 0, 1, 0, 1], '\\': [1, 1, 0, 0, 1, 1], ']': [1, 1, 0, 1, 1, 1],
    '^': [0, 0, 0, 1, 1, 0], '_': [0, 0, 0, 1, 1, 1]
}


def ascii_to_braille(text):
    # 将文本转换为大写
    text = text.upper()
    braille_text = []
    # 遍历文本中的每个字符
    for char in text:
        # 如果字符在映射中
        if char in braille_mapping:
            # 将对应的盲文点数添加到结果列表中
            braille_text.append(braille_mapping[char])
        else:
            # 如果字符不在映射中，则用空格替代
            braille_text.append(braille_mapping[' '])

    return braille_text


def print_braille(braille_text):
    # 打印盲文凸点数
    for char_braille in braille_text:
        # 将6个二进制数转换为字符串
        binary_string = ''.join(map(str, char_braille))
        # 每个字符一行打印输出
        print(binary_string)


# 示例用法
if __name__ == '__main__':
    text = "Hello, \ World!"
    braille_text = ascii_to_braille(text)
    print_braille(braille_text)
