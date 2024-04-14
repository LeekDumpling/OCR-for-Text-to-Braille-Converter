# 使用官方Python镜像作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 安装tesseract-ocr及其语言包
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-chi-sim

# 安装SSH服务
RUN apt-get install -y openssh-server
# 生成SSH密钥
RUN ssh-keygen -A
# 设置SSH允许root登录
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# 设置SSH使用密码登录
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
# 更改root密码（请替换为您自己的密码）
RUN echo 'root:123456' | chpasswd

# 将本地文件复制到容器中
COPY requirements.txt requirements.txt
COPY server.py server.py
COPY local_ocr.py local_ocr.py
COPY ../client/ChuanKou.py ChuanKou.py
COPY MangWen.py
COPY test.png test.png


# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露容器的22端口和5000端口
EXPOSE 22 5000

# 运行SSH服务和Flask应用
CMD service ssh start && python server.py
