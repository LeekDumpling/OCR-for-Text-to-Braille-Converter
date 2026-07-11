# OCR for Text to Braille Converter

一个将屏幕图像中的文字识别（OCR）并转换为盲文点阵数据的实验项目。项目由客户端截图发送、服务端识别转换、串口输出三部分组成，适用于“文字信息转盲文数据”的原型验证。

## 功能概览

- 屏幕截图采集（支持热键触发与区域选择）
- 图像上传到服务端（TCP/HTTP 两种实现）
- 基于 Tesseract 的文字识别
- ASCII 文本到 6 点盲文二进制映射转换
- 可选串口转发到单片机设备

## 项目结构

```text
.
├── client/
│   ├── client.py          # TCP 客户端：截图并发送到远端 server.py
│   ├── client_local.py    # HTTP 客户端：截图并请求本地 Flask 服务
│   ├── ChuanKou.py        # 串口发送工具
│   └── requirements.txt
├── server/
│   ├── server.py          # TCP 服务端：接收图片并做 OCR/盲文转换
│   ├── server_local.py    # Flask 服务端：提供 /ocr HTTP 接口
│   ├── MangWen.py         # ASCII -> 盲文映射逻辑
│   ├── local_ocr.py       # 本地 OCR 测试脚本
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

## 环境要求

- Python 3.8+
- Tesseract OCR（需可执行文件可用）
- 客户端依赖的图形/输入能力（`pyautogui`、`keyboard`）
- 若使用串口功能：可用串口设备与 `pyserial`

## 安装依赖

### 服务端

```bash
cd /home/runner/work/OCR-for-Text-to-Braille-Converter/OCR-for-Text-to-Braille-Converter/server
pip install -r requirements.txt
```

### 客户端

```bash
cd /home/runner/work/OCR-for-Text-to-Braille-Converter/OCR-for-Text-to-Braille-Converter/client
pip install -r requirements.txt
```

## 运行方式

### 方式一：TCP 模式（当前主流程）

1. 启动服务端（监听 `0.0.0.0:32771`）：

```bash
cd /home/runner/work/OCR-for-Text-to-Braille-Converter/OCR-for-Text-to-Braille-Converter/server
python server.py
```

2. 修改客户端中的服务端地址（`client/client.py` 里的 `server_addr`）。
3. 启动客户端：

```bash
cd /home/runner/work/OCR-for-Text-to-Braille-Converter/OCR-for-Text-to-Braille-Converter/client
python client.py
```

4. 按 `F12` 选择截图区域，客户端会发送图像到服务端。

### 方式二：本地 HTTP 模式（调试用）

1. 启动 Flask 服务：

```bash
cd /home/runner/work/OCR-for-Text-to-Braille-Converter/OCR-for-Text-to-Braille-Converter/server
python server_local.py
```

2. 根据 `server_local.py` 的端口配置，检查并调整 `client/client_local.py` 中请求地址。
3. 启动本地客户端：

```bash
cd /home/runner/work/OCR-for-Text-to-Braille-Converter/OCR-for-Text-to-Braille-Converter/client
python client_local.py
```

## 数据流说明

1. 客户端截图并压缩为 JPG
2. 发送给服务端
3. 服务端 OCR 提取文本
4. 使用 `MangWen.ascii_to_braille` 转成盲文点阵数组
5. 客户端（可选）将盲文数据通过串口发送至外设

## 关键模块

- `server/MangWen.py`：盲文映射表与转换函数
- `server/server.py`：TCP 协议处理、心跳、图片接收
- `client/client.py`：热键截图、重试发送、服务端连通性处理
- `client/ChuanKou.py`：串口收发封装

## 已知限制

- 当前盲文映射主要针对 ASCII 字符，非 ASCII 字符会回退为空格映射
- 客户端与服务端地址/端口在脚本中为硬编码，部署前需手动修改
- 串口参数（如端口号 `COM3`）需根据实际设备调整

## 后续可改进方向

- 统一配置管理（IP、端口、OCR 参数）
- 增加中文/多语言到盲文规则支持
- 完善异常处理与日志
- 补充自动化测试与端到端验证
