# dish5 Makefile

.PHONY: help up down restart logs status \
        init-db migrate seed \
        install dev test lint clean \
        shell psql

# 默认目标
help: ## 显示帮助信息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ============================================================
# Docker 环境
# ============================================================

up: ## 启动所有服务 (PostgreSQL + Backend)
	docker-compose up -d
	@echo "✅ 服务已启动 → http://localhost:8010"
	@echo "📖 API 文档 → http://localhost:8010/docs"
	@echo "🔧 管理后台 → http://localhost:8010/admin"

down: ## 停止所有服务
	docker-compose down

restart: down up ## 重启所有服务

logs: ## 查看后端日志
	docker-compose logs -f backend

status: ## 查看服务运行状态
	docker-compose ps

# ============================================================
# 前端
# ============================================================

fe-install: ## 安装前端依赖
	cd frontend && npm install --legacy-peer-deps

fe-dev: ## 启动前端 H5 开发服务器
	cd frontend && npm run dev

fe-build: ## 构建前端 H5 版本
	cd frontend && npm run build

fe-build-mp: ## 构建微信小程序版本
	cd frontend && npm run build:mp-weixin

# ============================================================
# 数据库
# ============================================================

init-db: ## 导入种子数据 (需要先启动数据库)
	@echo "📦 导入菜品种子数据..."
	PGPASSWORD=postgres psql -h localhost -p 5434 -U postgres -d dish5 -f backend/init.sql
	@echo "📦 导入食材主表 (55 种)..."
	PGPASSWORD=postgres psql -h localhost -p 5434 -U postgres -d dish5 -f backend/init_ingredients.sql
	@echo "✅ 种子数据导入完成 (12 道菜 + 55 种食材)"

seed: init-db ## 同 init-db

migrate: ## 运行 Alembic 数据库迁移
	cd backend && alembic upgrade head
	@echo "✅ 数据库迁移完成"

makemigrations: ## 生成 Alembic 迁移（自动检测模型变更）
	cd backend && alembic revision --autogenerate -m "auto migration"
	@echo "✅ 迁移文件已生成，请检查 alembic/versions/ 后提交"

# ============================================================
# 开发
# ============================================================

install: ## 安装 Python 依赖
	cd backend && pip install -r requirements.txt
	@echo "✅ 依赖安装完成"

dev: ## 启动开发服务器 (hot reload)
	cd backend/app && uvicorn main:app --reload --host 0.0.0.0 --port 8010

shell: ## 进入后端容器 shell
	docker-compose exec backend bash

psql: ## 连接数据库
	docker-compose exec db psql -U postgres -d dish5

# ============================================================
# 测试
# ============================================================

test: ## 运行所有测试
	cd backend && python -m pytest tests/ -v

test-cov: ## 运行测试并生成覆盖率报告
	cd backend && python -m pytest tests/ -v --cov=app --cov-report=html

# ============================================================
# 代码质量
# ============================================================

lint: ## 代码检查
	cd backend && python -m py_compile app/**/*.py
	@echo "✅ 语法检查通过"

clean: ## 清理临时文件
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	@echo "✅ 清理完成"

# ============================================================
# 一键操作
# ============================================================

setup: install init-db ## 全新安装 (安装依赖 + 导入数据)

fresh: down ## 完全重置 (停止 + 清理数据 + 重建)
	docker-compose down -v
	docker-compose up -d --build
	sleep 5
	$(MAKE) init-db
	@echo "✅ 环境重置完成"
