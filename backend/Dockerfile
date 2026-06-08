FROM python:3.12

# 容器内路径与宿主机完全一致，方便 VSCode 调试和日志查看
WORKDIR /home/dron/projects/dish/dish5/backend

# 安装依赖
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --index-url http://host.docker.internal:6080/simple --trusted-host host.docker.internal  -r requirements.txt
# 复制应用代码
COPY app/ ./app/

# 暴露端口
EXPOSE 8000

# 启动
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
