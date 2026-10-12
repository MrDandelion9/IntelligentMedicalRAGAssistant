# ============================================================
# IntelligentMedicalRAGAssistant - Agentic Medical
# Python 3.12.14
# ============================================================


# =========================
# 构建阶段
# =========================
FROM python:3.12.14 AS builder

# 设置工作目录
WORKDIR /app

# 使用清华 PyPI 镜像
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 创建虚拟环境
RUN python -m venv /opt/venv

# 后续 pip/python 默认使用虚拟环境
ENV PATH="/opt/venv/bin:$PATH"

# 先复制 requirements.txt
# 这样代码修改时 Docker 可以复用依赖安装缓存
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt


# =========================
# 运行阶段
# =========================
FROM python:3.12.14

WORKDIR /app

# 创建非 root 用户
RUN groupadd -r appuser && \
    useradd -r -g appuser appuser

# 复制构建阶段的虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 使用虚拟环境
ENV PATH="/opt/venv/bin:$PATH"

# 复制整个项目
COPY . .

# 创建运行时需要的目录
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app

# 使用非 root 用户运行
USER appuser

# FastAPI 端口
EXPOSE 8000

# 健康检查
# 如果你的项目没有 /health 接口，
# 后面需要删除或者改成你实际存在的接口
HEALTHCHECK --interval=300s \
            --timeout=300s \
            --start-period=300s \
            --retries=3 \
            CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')" || exit 1

# 启动 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]