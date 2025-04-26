# Dockerfile (放在项目根目录 OrbitDo/)
FROM python:3.12-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 2. 设置工作目录
WORKDIR /app

# 3. 安装系统依赖 (如果需要，在这里添加)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package \
#  && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 暴露端口
# 暴露 Gunicorn 将要监听的端口
EXPOSE 8080

RUN python manage.py collectstatic --noinput

# 调试一下
RUN echo "--- Contents of STATIC_ROOT ---" && ls -lR /app/staticfiles

# 7. 运行命令 (使用 Gunicorn)
# 假设你的 Django 项目(包含 wsgi.py 的目录)名为 'App'
# 如果你的项目主应用名不同，请修改 'App.wsgi:application'
# --workers 3: 指定 3 个工作进程处理请求 (可以根据需要调整)
# --bind 0.0.0.0:8080: 监听所有网络接口的 8080 端口
CMD ["gunicorn", "OrbitDo.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
