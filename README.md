# dish5 — 菜谱推荐系统

## 项目概述

dish5 是一个智能每日菜谱推荐系统。每天自动推荐 1 硬菜 + 2 素菜 + 1 汤，附带合并后的购物清单，支持菜谱管理和历史回顾。

这是第 5 个迭代版本，整合了前 4 个版本的最佳实践。

### 历史版本演变

| 版本 | 目录 | 技术栈 | 定位 | 优点 | 问题 |
|------|------|--------|------|------|------|
| v1 | `dish_online2/` | React (UmiJS) + FastAPI + SQLite | 简易菜单浏览 | 简单自包含 | 功能少，无推荐 |
| v2 | `dish_online/` | React (UmiJS) + FastAPI + MySQL | CRUD 菜谱管理 | 丰富 JSON 字段，聚合视图 | 无推荐算法，前端无源码 |
| v3 | `dish3/` | FastAPI + MySQL + APScheduler | 定时推送推荐 | 推荐算法，JWT 认证，测试 | 5 分钟轮询浪费，CRUD 大量重复 |
| v4 | `dish4/` | 微信小程序 + FastAPI + PostgreSQL | 全栈小程序 | 购物清单，收藏，管理后台 | 推荐代码损坏，假认证，硬编码数据 |
| v5 | **dish5/** | uni-app (Vue 3) + FastAPI + PostgreSQL | 全栈 Web + 小程序 | **本次重构** | — |

### 设计目标

1. **保留好的**：FastAPI 异步架构、推荐算法、JSON 菜品结构、聚合视图、管理后台
2. **修复坏的**：CRUD 重复代码、硬编码凭证、损坏的推荐代码、同步/异步混合
3. **后端风格不变**：继续使用 FastAPI + SQLAlchemy 2.0 async，代码组织保持一致
4. **Web 优先，小程序跟进**：使用 uni-app (Vue 3) 实现一套代码编译 H5 + 微信小程序

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | FastAPI (Python 3.11+) | 全异步 |
| ORM | SQLAlchemy 2.0 async | 统一的异步数据访问 |
| 数据库 | PostgreSQL 16 | JSONB 字段支持 |
| 驱动 | asyncpg | PostgreSQL 异步驱动 |
| 数据验证 | Pydantic v2 + pydantic-settings | 配置与请求验证 |
| 调度器 | APScheduler (cron) | 每日 8:00 触发 |
| 通知 | 企业微信 Webhook | URL 从环境变量读取 |
| 管理后台 | Jinja2 + Bootstrap 5 | 轻量级后台 |
| 前端 (计划) | uni-app (Vue 3) + uView Plus | H5 + 微信小程序复用 |
| 部署 | Docker Compose | PostgreSQL + Backend + Nginx |

## 目录结构

```
dish5/
├── backend/                          # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py                   # FastAPI 入口 (lifespan + scheduler)
│   │   ├── admin.py                  # 管理后台 Jinja2 路由
│   │   ├── api/v1/                   # REST API
│   │   │   ├── router.py             # 路由聚合
│   │   │   └── endpoints/            # 端点实现
│   │   │       ├── dishes.py         # 菜品 CRUD
│   │   │       ├── daily.py          # 每日推荐
│   │   │       ├── shopping.py       # 购物清单
│   │   │       ├── favorites.py      # 收藏
│   │   │       └── aggregation.py    # 聚合接口
│   │   ├── core/                     # 配置与基础设施
│   │   │   ├── config.py             # pydantic-settings
│   │   │   └── database.py           # async engine/session
│   │   ├── models/                   # SQLAlchemy 模型
│   │   │   ├── dish.py               # 菜品 (Dish)
│   │   │   ├── daily_recommend.py    # 每日推荐
│   │   │   ├── user.py               # 用户 (预留)
│   │   │   └── favorite.py           # 收藏
│   │   ├── schemas/                  # Pydantic 请求/响应
│   │   ├── crud/                     # 数据访问层
│   │   │   ├── base.py               # 通用 CRUD 基类
│   │   │   ├── crud_dish.py
│   │   │   ├── crud_daily.py
│   │   │   └── crud_favorite.py
│   │   ├── services/                 # 业务逻辑
│   │   │   ├── recommend.py          # 推荐算法
│   │   │   └── notification.py       # 通知推送
│   │   ├── tasks/                    # 定时任务
│   │   │   └── scheduler.py          # APScheduler 配置
│   │   └── templates/admin/          # 管理后台模板
│   ├── tests/                        # 测试
│   ├── requirements.txt              # Python 依赖
│   ├── Dockerfile                    # 后端镜像
│   ├── .env.example                  # 环境变量模板
│   └── init.sql                      # 种子数据
├── frontend/                         # uni-app 前端 (待开发)
├── docker-compose.yml                # 一键部署
├── Makefile                          # 常用命令
└── README.md                         # 本文件
```

## 数据模型

### dishes (菜品表)

| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `id` | SERIAL PK | | |
| `name` | VARCHAR(100) UNIQUE | 菜名 | |
| `dtype` | ENUM('硬菜','肉汤','素汤','素菜','半素') | 荤素分类 | dish3 |
| `ftype` | ENUM('跑','飞','游','草') | 主材分类 | dish3 |
| `start_month` | SMALLINT 1-12 | 应季开始月 | dish3 |
| `end_month` | SMALLINT 1-12 | 应季结束月 | dish3 |
| `eats` | INT DEFAULT 0 | 被推荐次数 | dish3 |
| `main_ingredients` | JSONB | 主料列表 `[{"name":"肉","amount":"500g"}]` | dish_online |
| `side_ingredients` | JSONB | 辅料列表 | dish_online |
| `seasonings` | JSONB | 调料列表 | dish_online |
| `cooking_steps` | JSONB | 烹饪步骤 `[{"name":"焯水","step":1}]` | dish_online |
| `attentions` | JSONB | 注意事项 | dish_online |
| `prep_steps` | JSONB | 备菜 `[{"act":"洗","name":"菜"}]` | dish_online |
| `cooking_time` | INT | 烹饪时间(分钟) | dish4 |
| `difficulty` | ENUM('简单','中等','困难') | 难度 | dish4 |
| `image_url` | VARCHAR(255) | 图片 | dish4 |
| `sort_order` | INT | 排序 | dish3 |
| `created_at` | TIMESTAMP | | |
| `updated_at` | TIMESTAMP | | |

### daily_recommends (每日推荐表)

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | SERIAL PK | |
| `date` | DATE UNIQUE INDEX | 推荐日期 |
| `recipes` | JSONB | 推荐菜品快照 `[{id,name,dtype}]` |
| `shopping_list` | JSONB | 购物清单 `[{name,amount,bought}]` |
| `aggregated` | JSONB | 预计算聚合数据 |
| `notified` | BOOL | 是否已推送 |
| `notified_at` | TIMESTAMP | 推送时间 |
| `created_at` | TIMESTAMP | |

### favorites (收藏表)

| 字段 | 类型 |
|------|------|
| `id` | SERIAL PK |
| `user_id` | FK→users |
| `dish_id` | FK→dishes |
| `created_at` | TIMESTAMP |
| UNIQUE(user_id, dish_id) | |

### users (用户表 — 预留)

| 字段 | 类型 |
|------|------|
| `id` | SERIAL PK |
| `username` | VARCHAR(63) UNIQUE |
| `hashed_password` | VARCHAR(255) |
| `is_admin` | BOOL |
| `created_at` | TIMESTAMP |

## API 文档

所有 API 前缀 `/api/v1`，统一响应格式：

```json
// 单条
{"code": 200, "success": true, "data": {...}, "detail": null}
// 分页
{"code": 200, "success": true, "data": [...], "total": N, "current": 1, "pageSize": 10}
```

### 端点列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 健康检查 |
| GET | `/health` | 健康检查 |
| **菜品** | | |
| GET | `/api/v1/dishes` | 分页列表 (排序白名单 + 搜索筛选) |
| GET | `/api/v1/dishes/{id}` | 获取详情 |
| POST | `/api/v1/dishes` | 创建 |
| PATCH | `/api/v1/dishes/{id}` | 部分更新 |
| DELETE | `/api/v1/dishes/{id}` | 删除 |
| DELETE | `/api/v1/dishes` | 批量删除 (body: [ids]) |
| GET | `/api/v1/dishes/aggregate?ids=1,2,3` | 多选聚合食材步骤 |
| **每日推荐** | | |
| GET | `/api/v1/daily/today` | 今日推荐 |
| GET | `/api/v1/daily/{date}` | 指定日期推荐 |
| POST | `/api/v1/daily/generate?target_date=2026-06-05` | 手动生成 |
| GET | `/api/v1/daily/history/list` | 历史分页 |
| **购物清单** | | |
| GET | `/api/v1/shopping/{date}` | 获取购物清单 |
| PUT | `/api/v1/shopping/{date}` | 更新已购状态 |
| **收藏** | | |
| GET | `/api/v1/favorites` | 我的收藏 |
| POST | `/api/v1/favorites?dish_id=1` | 添加收藏 |
| DELETE | `/api/v1/favorites/{dish_id}` | 取消收藏 |
| GET | `/api/v1/favorites/check/{dish_id}` | 检查收藏状态 |
| **管理后台** (Jinja2 HTML) | | |
| GET | `/admin` | 仪表板 |
| GET | `/admin/dishes` | 菜品管理 |
| GET | `/admin/daily` | 推荐管理 |

## 推荐算法

```
输入: target_date
1. month = target_date.month
2. 查询 dishes WHERE start_month <= month <= end_month
3. 分类选择 (按 eats ASC — 优先最少吃过的):
   ├── 硬菜 (dtype=硬菜): 1 道
   ├── 素菜 (dtype=素菜): 2 道
   └── 汤   (dtype=肉汤 or 素汤): 1 道
4. 空类回退: 从所有菜品中按 eats ASC 补充
5. 选中菜品 eats += 1
6. 合并 4 道菜的 main_ingredients + side_ingredients + seasonings → shopping_list
7. 预计算聚合数据 → aggregated JSON
8. 存入 daily_recommends 表
9. 发送企业微信 Webhook 通知 (如已配置)
```

### 调度器

- APScheduler + CronTrigger: 每天 8:00 AM (Asia/Shanghai)
- misfire_grace_time: 300 秒 (5 分钟容错)
- 启动前先检查当天是否已生成，避免重复

## 关键设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 前端框架 | uni-app (Vue 3) | 一套代码编译 H5 + 微信小程序，风格统一 |
| 数据库 | PostgreSQL | 用户指定；JSONB 字段优于 MySQL JSON |
| 认证 | 暂不实现 | 先做核心功能，后续加多用户 |
| 调度器 | cron 而非轮询 | dish3 的 5 分钟轮询浪费资源 |
| CRUD 模式 | BaseCRUD 基类 | 消除 dish3 中 3 个文件 150+ 行重复 |
| 错误处理 | HTTPException | 修复 dish3 的 `return {"success": False}` 模式 |
| 通知 | 环境变量配置 | 修复 dish3 硬编码 webhook URL |
| 聚合预计算 | 存入 DB | 避免每次请求重复计算 |

## 快速开始

### 前置要求

- Python 3.11+
- PostgreSQL 16+ (或 Docker)
- Node.js 18+ (前端开发)

### 1. 配置环境

```bash
cd dish5/backend
cp .env.example .env
# 编辑 .env 填入数据库密码等
```

### 2. 启动 (Docker 推荐)

```bash
cd dish5
make up          # 启动 PostgreSQL + Backend
make init-db     # 导入种子数据
```

### 3. 本地开发

```bash
cd dish5/backend
pip install -r requirements.txt
cd app && uvicorn main:app --reload --port 8010
```

### 4. 访问

- API 文档: http://localhost:8010/docs
- 管理后台: http://localhost:8010/admin
- 健康检查: http://localhost:8010/health

## 开发计划

- [x] Phase 1: 后端核心 (模型 + CRUD + API + 推荐 + 调度)
- [x] Phase 2: 测试 + 种子数据 + Docker
- [ ] Phase 3: 前端 Web (uni-app H5)
- [ ] Phase 4: 小程序编译 + 功能增强

## 从旧项目复用的关键代码

| 来源 | 文件 | 用途 |
|------|------|------|
| dish3 | `schemas/__init__.py` | BaseResponse, PaginationResponse |
| dish3 | `models/mydish.py` | DtypeEnum, FtypeEnum, eats/start_month/end_month |
| dish_online | `api/v1/dish_custom.py` | merge_and_sum_weights 聚合函数 |
| dish4 | `services/recommend.py` | 推荐算法骨架 (修复损坏代码) |
| dish4 | `tasks/scheduler.py` | cron 调度器模式 |
| dish4 | `templates/admin/` | Jinja2 管理后台模板 |
| dish4 | `crud/` | CRUD 类模式 |
| dish3 | `alembic/` | 迁移框架 (后续配置) |
