# OCR-for-Text-to-Braille-Converter

基于 OCR 的屏幕文字识别与盲文转换系统。客户端捕获屏幕截图并发送至服务端，服务端利用 Tesseract OCR 识别文字，再将文字转换为标准六点盲文编码，最终可通过串口输出到盲文显示单片机。

---

## 目录

- [功能特性](#功能特性)
- [系统架构](#系统架构)
- [目录结构](#目录结构)
- [依赖环境](#依赖环境)
- [快速上手](#快速上手)
  - [服务端（本地运行）](#服务端本地运行)
  - [服务端（Docker 部署）](#服务端docker-部署)
  - [客户端](#客户端)
- [模块说明](#模块说明)
- [配置说明](#配置说明)
- [当前进展与待办](#当前进展与待办)
- [贡献指南](#贡献指南)

---

## 功能特性

- 🖥️ **屏幕截图**：支持全屏自动截图和按 `F12` 热键框选截图
- 🔍 **OCR 识别**：基于 [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)，支持英文及简体中文
- ⠿ **盲文转换**：将 ASCII 文本映射为标准六点盲文二进制编码
- 🌐 **远程传输**：客户端通过 TCP 将图片传输到云端服务器
- 🔌 **串口输出**：预留串口接口，可将盲文数据发送至单片机盲文显示器
- 🐳 **Docker 支持**：服务端提供 Dockerfile，已在阿里云成功部署

---

## 系统架构

```
┌─────────────────────────────────────────┐
│               客户端 (Client)            │
│                                         │
│  截图 (pyautogui / OpenCV)              │
│       │                                 │
│  压缩为 JPEG (OpenCV, quality=40)       │
│       │                                 │
│  TCP Socket → 服务端 (port 32771)       │
│  HTTP POST  → 服务端 (port 5000)        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│               服务端 (Server)            │
│                                         │
│  接收图像数据                            │
│       │                                 │
│  Tesseract OCR → 提取文本               │
│       │                                 │
│  MangWen.py → 转换为六点盲文编码         │
│       │                                 │
│  返回结果 (JSON) / 转发至单片机           │
└─────────────────────────────────────────┘
                    │
                    ▼ (预留接口)
┌─────────────────────────────────────────┐
│           单片机盲文显示器               │
│  串口通信 (COM3, 9600 baud)             │
└─────────────────────────────────────────┘
```

---

## 目录结构

```
OCR-for-Text-to-Braille-Converter/
├── client/
│   ├── client.py          # TCP 模式客户端（连接远程服务器）
│   ├── client_local.py    # HTTP 模式客户端（连接本地 Flask 服务）
│   ├── ChuanKou.py        # 串口通信模块（向单片机发送盲文数据）
│   └── requirements.txt   # 客户端 Python 依赖
├── server/
│   ├── server.py          # TCP Socket 服务端（云部署版）
│   ├── server_local.py    # Flask HTTP 服务端（本地开发版）
│   ├── MangWen.py         # ASCII → 六点盲文编码转换模块
│   ├── local_ocr.py       # 本地 OCR 测试工具
│   ├── Dockerfile         # Docker 镜像构建文件
│   ├── requirements.txt   # 服务端 Python 依赖
│   ├── .env               # 环境变量（Tesseract 路径等，本地使用）
│   └── test.png           # OCR 测试图片
├── debug_image.jpg        # 调试用：服务端最近处理的截图
└── README.md
```

---

## 依赖环境

### 系统依赖

| 依赖 | 说明 |
|------|------|
| [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) | OCR 引擎，需额外安装简体中文语言包 `tesseract-ocr-chi-sim` |
| Python 3.8+ | 运行环境 |
| Docker（可选） | 服务端容器化部署 |

### 服务端 Python 依赖（`server/requirements.txt`）

```
pytesseract
pillow
flask
python-dotenv
pyserial
```

### 客户端 Python 依赖（`client/requirements.txt`）

```
pillow~=10.2.0
requests~=2.31.0
numpy~=1.26.4
pyautogui
keyboard
pyserial
```

---

## 快速上手

### 服务端（本地运行）

1. **安装 Tesseract OCR**

   - Windows：从 [官方发布页](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装，并安装中文语言包。
   - Linux：
     ```bash
     sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
     ```

2. **安装 Python 依赖**

   ```bash
   cd server
   pip install -r requirements.txt
   ```

3. **配置 `.env` 文件**（Windows 本地运行时需要指定 Tesseract 路径）

   ```
   TESSERACT_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
   ```

4. **启动 Flask 服务（HTTP 模式，端口 5000）**

   ```bash
   python server_local.py
   ```

   或启动 **TCP Socket 服务（端口 32771）**：

   ```bash
   python server.py
   ```

---

### 服务端（Docker 部署）

```bash
cd server

# 构建镜像
docker build -t ocr-braille-server .

# 运行容器，映射 TCP 服务端口
docker run -d -p 32771:32771 --name ocr-server ocr-braille-server
```

> 镜像基于 `python:3.8-slim`，内置 Tesseract OCR 及简体中文语言包。

---

### 客户端

1. **安装 Python 依赖**

   ```bash
   cd client
   pip install -r requirements.txt
   ```

2. **连接远程服务器（TCP 模式）**

   编辑 `client/client.py` 中的服务器地址：
   ```python
   server_addr = ("你的服务器IP", 32771)
   ```
   然后运行：
   ```bash
   python client.py
   ```

3. **连接本地服务（HTTP 模式）**

   ```bash
   python client_local.py
   ```

4. **操作说明**

   - 程序启动后，按下 **`F12`** 键框选屏幕区域进行截图并发送。
   - 截图将被压缩后传输到服务端进行 OCR 识别和盲文转换。

---

## 模块说明

### `server/MangWen.py` — 盲文转换核心

将 ASCII 字符映射为标准六点盲文编码。每个字符对应一个长度为 6 的二进制列表，依次代表盲文点 1–6（1 为凸起，0 为平坦）。

```python
from MangWen import ascii_to_braille

braille = ascii_to_braille("Hello")
# 返回: [[1,1,0,0,1,0], [1,0,0,0,0,0], ...]  每个列表对应一个字符的六点编码
```

### `client/ChuanKou.py` — 串口通信

通过串口（默认 `COM3`，波特率 `9600`）将盲文数据逐字发送至单片机。使用前请根据实际串口号修改 `serial.Serial('COM3', 9600)` 中的参数。

### `server/local_ocr.py` — 本地 OCR 测试

独立运行，对指定图片文件执行 OCR 识别并输出文本及字符坐标，用于调试。

---

## 配置说明

| 配置项 | 位置 | 说明 |
|--------|------|------|
| `TESSERACT_PATH` | `server/.env` | Tesseract 可执行文件路径（Windows 本地运行时需要） |
| `server_addr` | `client/client.py` | 远程 TCP 服务器 IP 和端口 |
| `hotkey` | `client/client.py` | 截图热键，默认为 `F12` |
| 串口号 | `client/ChuanKou.py` | 单片机串口号，默认为 `COM3` |

---

## 当前进展与待办

- [x] 服务端 Flask HTTP 模式开发完成
- [x] 服务端 TCP Socket 模式开发完成
- [x] 制作 Docker 镜像并部署至阿里云
- [x] 客户端与服务端联调成功，可获取屏幕截图的盲文数据
- [x] 解决服务器端响应缓慢问题
- [ ] 实现客户端与单片机的串口通信（接口已预留）
- [ ] 支持更多 OCR 语言包
- [ ] 优化盲文编码标准（当前仅支持 ASCII 字符集）

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'feat: add your feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源协议。
