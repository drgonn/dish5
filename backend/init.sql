-- dish5 种子数据
-- 精选常见家常菜作为初始数据

INSERT INTO dishes (name, dtype, ftype, start_month, end_month, eats, main_ingredients, side_ingredients, seasonings, cooking_steps, cooking_time, difficulty, sort_order) VALUES

-- 硬菜
('红烧肉', '硬菜', '跑', 1, 12, 0,
 '[{"name": "五花肉", "amount": "500g"}]',
 '[{"name": "葱", "amount": "2根"}, {"name": "姜", "amount": "5片"}, {"name": "八角", "amount": "2个"}, {"name": "桂皮", "amount": "1块"}, {"name": "香叶", "amount": "2片"}]',
 '[{"name": "生抽", "amount": "2勺"}, {"name": "老抽", "amount": "1勺"}, {"name": "料酒", "amount": "2勺"}, {"name": "冰糖", "amount": "30g"}, {"name": "盐", "amount": "适量"}]',
 '[{"name": "五花肉切块焯水", "step": 1}, {"name": "炒糖色", "step": 2}, {"name": "加调料炖煮40分钟", "step": 3}, {"name": "大火收汁", "step": 4}]',
 60, '中等', 1),

('糖醋排骨', '硬菜', '跑', 1, 12, 0,
 '[{"name": "排骨", "amount": "500g"}]',
 '[{"name": "葱", "amount": "2根"}, {"name": "姜", "amount": "5片"}]',
 '[{"name": "料酒", "amount": "1勺"}, {"name": "生抽", "amount": "2勺"}, {"name": "老抽", "amount": "1勺"}, {"name": "醋", "amount": "3勺"}, {"name": "白糖", "amount": "4勺"}]',
 '[{"name": "排骨焯水", "step": 1}, {"name": "炒糖色", "step": 2}, {"name": "加入调料炖煮", "step": 3}, {"name": "收汁出锅", "step": 4}]',
 45, '中等', 2),

('可乐鸡翅', '硬菜', '飞', 1, 12, 0,
 '[{"name": "鸡翅", "amount": "10个"}]',
 '[{"name": "姜", "amount": "5片"}, {"name": "葱", "amount": "1根"}]',
 '[{"name": "可乐", "amount": "1罐"}, {"name": "生抽", "amount": "2勺"}, {"name": "老抽", "amount": "1勺"}, {"name": "料酒", "amount": "1勺"}]',
 '[{"name": "鸡翅划刀腌制", "step": 1}, {"name": "煎至两面金黄", "step": 2}, {"name": "倒入可乐炖煮15分钟", "step": 3}, {"name": "大火收汁", "step": 4}]',
 30, '简单', 3),

-- 肉汤
('排骨玉米汤', '肉汤', '跑', 6, 10, 0,
 '[{"name": "排骨", "amount": "500g"}, {"name": "玉米", "amount": "2根"}]',
 '[{"name": "姜", "amount": "5片"}, {"name": "葱", "amount": "2根"}, {"name": "枸杞", "amount": "10粒"}]',
 '[{"name": "盐", "amount": "适量"}, {"name": "料酒", "amount": "2勺"}]',
 '[{"name": "排骨焯水", "step": 1}, {"name": "玉米切段", "step": 2}, {"name": "一起入锅煲1小时", "step": 3}, {"name": "加盐调味", "step": 4}]',
 90, '简单', 10),

-- 素汤
('番茄蛋花汤', '素汤', '草', 1, 12, 0,
 '[{"name": "番茄", "amount": "2个"}, {"name": "鸡蛋", "amount": "2个"}]',
 '[{"name": "葱", "amount": "1根"}]',
 '[{"name": "盐", "amount": "适量"}, {"name": "香油", "amount": "几滴"}]',
 '[{"name": "番茄切块", "step": 1}, {"name": "炒出汁加水煮沸", "step": 2}, {"name": "淋入蛋液", "step": 3}, {"name": "调味出锅", "step": 4}]',
 15, '简单', 11),

-- 素菜
('酸辣土豆丝', '素菜', '草', 1, 12, 0,
 '[{"name": "土豆", "amount": "2个"}]',
 '[{"name": "干辣椒", "amount": "5个"}, {"name": "蒜", "amount": "3瓣"}, {"name": "葱", "amount": "1根"}]',
 '[{"name": "醋", "amount": "2勺"}, {"name": "盐", "amount": "适量"}, {"name": "花椒", "amount": "10粒"}]',
 '[{"name": "土豆切丝泡水去淀粉", "step": 1}, {"name": "爆香花椒干辣椒", "step": 2}, {"name": "大火翻炒2分钟", "step": 3}, {"name": "加醋出锅", "step": 4}]',
 15, '简单', 20),

('手撕包菜', '素菜', '草', 1, 12, 0,
 '[{"name": "包菜", "amount": "半个"}]',
 '[{"name": "干辣椒", "amount": "5个"}, {"name": "蒜", "amount": "3瓣"}]',
 '[{"name": "生抽", "amount": "1勺"}, {"name": "醋", "amount": "1勺"}, {"name": "盐", "amount": "适量"}]',
 '[{"name": "包菜手撕成块", "step": 1}, {"name": "爆香蒜和干辣椒", "step": 2}, {"name": "大火翻炒至断生", "step": 3}, {"name": "调味出锅", "step": 4}]',
 10, '简单', 21),

('番茄炒蛋', '素菜', '草', 1, 12, 0,
 '[{"name": "番茄", "amount": "3个"}, {"name": "鸡蛋", "amount": "3个"}]',
 '[{"name": "葱", "amount": "1根"}, {"name": "蒜", "amount": "2瓣"}]',
 '[{"name": "盐", "amount": "适量"}, {"name": "白糖", "amount": "半勺"}]',
 '[{"name": "鸡蛋打散炒熟盛出", "step": 1}, {"name": "番茄炒出汁", "step": 2}, {"name": "倒入鸡蛋翻炒", "step": 3}, {"name": "调味出锅", "step": 4}]',
 15, '简单', 22),

-- 半素
('麻婆豆腐', '半素', '草', 1, 12, 0,
 '[{"name": "豆腐", "amount": "1块"}, {"name": "猪肉末", "amount": "100g"}]',
 '[{"name": "蒜", "amount": "3瓣"}, {"name": "姜", "amount": "3片"}, {"name": "葱", "amount": "2根"}, {"name": "花椒", "amount": "1把"}]',
 '[{"name": "郫县豆瓣酱", "amount": "2勺"}, {"name": "生抽", "amount": "1勺"}, {"name": "淀粉", "amount": "适量"}, {"name": "花椒粉", "amount": "适量"}]',
 '[{"name": "豆腐切块焯水", "step": 1}, {"name": "炒肉末至变色", "step": 2}, {"name": "加豆瓣酱炒出红油", "step": 3}, {"name": "加水和豆腐炖煮5分钟", "step": 4}, {"name": "勾芡撒花椒粉出锅", "step": 5}]',
 20, '中等', 30);
