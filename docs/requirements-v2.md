# dish5 功能需求 V2

## 功能全景

### 功能 1：智能每日推荐

**核心流程**：不知道吃什么 → 系统推荐 → 买菜清单 → 备菜清单 → 烹饪步骤

#### 1.1 可配置推荐
- 用户可设置：推荐 X 道荤菜、Y 道素菜、Z 道汤
- 默认：1 荤 + 2 素 + 1 汤
- 存储为用户偏好，每次生成时生效

#### 1.2 买菜清单
- 合并所有推荐菜品的食材
- 相同食材自动合并用量（如两盘菜都用五花肉，合并为一份）
- 剔除厨房常备调料（盐、酱油、料酒等）
- 按品类分组展示（肉类、蔬菜、豆制品、干货）

#### 1.3 备菜清单（重点）
不是简单罗列，而是**按工序智能编排**：

```
优先级 1：需要等待的（腌、泡、发）
  例：「腌五花肉 20分钟」「木耳泡发 30分钟」— 用户第一步就该做
优先级 2：清洗（洗）
  合并所有要洗的食材 → 统一洗
  例：「洗：五花肉、青菜、葱、姜」
优先级 3：切配（切）
  合并所有要切的 → 统一切
  例：「切片：大蒜」「切块：土豆、胡萝卜」「切段：葱」
优先级 4：备调料（备）
  合并所有共用调料 → 提前备好
  例：「大蒜 3瓣切末」「姜 5片」
优先级 5：烹饪（烹）
  按菜谱逐个展示烹饪步骤
```

**关键规则**：
- 多个菜共用同一食材时，备菜只出现一次（合并量）
- 腌/泡等耗时步骤必须排最前面
- 每步标注预估时间

#### 1.4 烹饪步骤
- 所有备菜结束后的制作流程
- 按菜谱逐个展示，每道菜的步骤独立
- 标注烹饪时间和难度

---

### 功能 2：冰箱图鉴

#### 2.1 食材库存
- 用户可以「录入」家里有的食材
- 食材来源：
  - 手动添加
  - 从购物清单一键入库（买了菜 → 入冰箱）
  - 推荐系统自动扣减（做了菜 → 从冰箱移除）
- 库存按品类排列

#### 2.2 视觉呈现
- 有库存的食材 → 彩色图标
- 无库存的食材 → 灰色图标
- 彩色自动排到顶部
- 按品类分组（肉禽蛋 / 蔬菜 / 豆制品 / 干货调料）

#### 2.3 「冰箱里有啥，能做啥」
- 根据冰箱现存食材，匹配出**全部可做的菜**
- 匹配规则：菜的主料全部在冰箱里 → 显示为「可做」
- 缺 1-2 样辅料 → 显示为「差 X 个食材」
- 差太多 → 不显示
- 排序：完全匹配 > 差 1 样 > 差 2 样

#### 2.4 「我买了 X，能做什么」
- 反向搜索：输入食材名 → 列出所有用到该食材的菜
- 支持多食材组合搜索

---

### 功能 3：长期功能（后续迭代）
- 多用户系统
- 营养统计
- 历史偏好学习
- 季节推荐权重

---

## 数据模型重新评估

### 结论：部分拆表，混合方案

| 方案 | 优点 | 缺点 |
|------|------|------|
| 纯 JSONB | CRUD 简单，已验证 | 无法高效做反向搜索 |
| 纯关系表 | 查询灵活 | 一个菜需要 6+ 次请求 |
| **混合（推荐）** | JSONB 存展示数据 + 关系表做搜索 | 写时需同步 |

### 新表结构

#### 保持不变
- `dishes` — 仍然用 JSONB 存储食材/步骤（前端展示用）
- `daily_recommends` — 每日推荐快照
- `favorites` — 收藏
- `users` — 用户（预留）

#### 新增

**1. recommend_preferences（推荐偏好）**
```sql
id            SERIAL PK
user_id       INT FK→users (暂时 = 1)
meat_count    INT DEFAULT 1   -- 荤菜数量
vegetable_count INT DEFAULT 2 -- 素菜数量
soup_count    INT DEFAULT 1   -- 汤数量
created_at    TIMESTAMP
```

**2. fridge_items（冰箱库存）**
```sql
id            SERIAL PK
user_id       INT FK→users (暂时 = 1)
ingredient_name VARCHAR(100) NOT NULL  -- 标准化食材名
category      VARCHAR(20)   -- 肉禽蛋/蔬菜/豆制品/干货调料/水果
quantity      VARCHAR(50)   -- 可选，数量描述
added_from    VARCHAR(50)   -- 'manual' / 'shopping' / 'recommend_deduct'
dish_id       INT FK→dishes -- 从哪个菜推荐的（扣减关联）
created_at    TIMESTAMP
updated_at    TIMESTAMP
UNIQUE(user_id, ingredient_name)
```

**3. ingredients（食材主表，标准化）**
```sql
id            SERIAL PK
name          VARCHAR(100) UNIQUE  -- 标准化名称
category      VARCHAR(20)          -- 品类
aliases       JSONB DEFAULT '[]'   -- 别名 ["土豆","马铃薯","洋芋"]
is_staple     BOOL DEFAULT false   -- 常用调料/常备品（排除在购物清单外）
```

### 关键变更：dish 表增强

`prep_steps` JSONB 结构细化：
```json
[
  {"act": "腌", "items": [{"name": "五花肉", "amount": "500g"}], "time_minutes": 20, "note": "加料酒酱油腌制"},
  {"act": "泡", "items": [{"name": "木耳", "amount": "50g"}], "time_minutes": 30, "note": "温水泡发"},
  {"act": "洗", "items": [{"name": "青菜"}, {"name": "葱"}, {"name": "姜"}]},
  {"act": "切", "items": [{"name": "五花肉", "shape": "块"}, {"name": "大蒜", "shape": "末"}, {"name": "姜", "shape": "片"}]},
  {"act": "备", "items": [{"name": "大蒜", "amount": "3瓣"}, {"name": "姜", "amount": "5片"}, {"name": "葱段", "amount": "3段"}]}
]
```

> 注意：旧的 `[{act, name}]` 格式升级为分组格式，每个 act 下包含 items 列表，可选 time_minutes。

### 购物清单生成逻辑增强

```
1. 收集所有推荐菜品的 main_ingredients + side_ingredients
2. 剔除 is_staple = true 的常备品
3. 对比 fridge_items：已存在的标记为「已有」，不加入清单
4. 合并同名食材
5. 输出：
   - need_buy: 需要买的
   - already_have: 冰箱已有，不用买
```

**4. dish_ingredients（食材关系表 — JSONB 的索引副本）**
```sql
id            SERIAL PK
dish_id       INT FK→dishes ON DELETE CASCADE
name          VARCHAR(100)   -- 标准化食材名
type          VARCHAR(20)    -- 'main' / 'side' / 'seasoning'
```
> 写入 dish 时自动同步。不替代 JSONB，仅用于搜索/匹配查询。
> `CREATE INDEX idx_di_name ON dish_ingredients(name);`

### 设计决策：为什么 dish_ingredients 是「索引副本」而非替代品

| 用法 | 存哪里 | 理由 |
|------|--------|------|
| 展示详情、购物清单、聚合 | `dishes.*` JSONB | 一次读出全量，CRUD 简单 |
| 冰箱匹配、食材反查 | `dish_ingredients` 关系表 | SQL JOIN + INDEX，毫秒级 |

### 冰箱匹配算法（使用 dish_ingredients）

```sql
-- 「冰箱里有 [A,B,C,D]，哪些菜完全可做？」
SELECT d.id, d.name
FROM dishes d
JOIN dish_ingredients di ON d.id = di.dish_id
WHERE di.type IN ('main', 'side')
GROUP BY d.id, d.name
HAVING COUNT(*) = (
    SELECT COUNT(*) FROM dish_ingredients
    WHERE dish_id = d.id AND type IN ('main', 'side')
      AND name = ANY(ARRAY['猪肉','鸡蛋','番茄','青菜','豆腐'])
);
```

```sql
-- 「我买了猪肉，能做啥」（反向搜索）
SELECT DISTINCT d.* FROM dishes d
JOIN dish_ingredients di ON d.id = di.dish_id
WHERE di.name = '猪肉';
```

---

## 实现路线

### Phase 3：数据库升级
1. `ingredients` 主表（种子数据 ~100 种常见食材）
2. `fridge_items` 表
3. `recommend_preferences` 表
4. `dishes.prep_steps` 结构升级
5. 数据迁移脚本（旧格式 → 新格式）

### Phase 4：后端新功能
6. 推荐偏好 API（GET/PUT `/api/v1/preferences`）
7. 冰箱 API（CRUD `/api/v1/fridge`）
8. 冰箱匹配 API（GET `/api/v1/fridge/match`）
9. 反向搜索 API（GET `/api/v1/dishes/by-ingredient?name=猪肉`）
10. 购物清单增强（对比冰箱库存）
11. 备菜编排算法增强（合并 + 排序）

### Phase 5：前端
12. uni-app Web 版本
13. 冰箱图鉴页面
14. 推荐设置页面
15. 备菜清单页面

---

## 设计决策记录

| 决策 | 选择 | 理由 |
|------|------|------|
| dish 食材存储 | 保持 JSONB | 一次读写全量数据，已验证 |
| 食材搜索 | 单独的 ingredients 表 | 需要标准化名称 + 别名匹配 |
| 冰箱库存 | 单独 fridge_items 表 | 独立实体，需要 UPDATE/DELETE |
| 推荐偏好 | 单独表 | 以后多用户时按 user_id 隔离 |
| 常备调料 | ingredients.is_staple | 标记而非硬编码列表 |
