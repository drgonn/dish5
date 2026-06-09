#!/usr/bin/env python3
"""dish5 菜谱种子数据 — 50道家常菜"""
import json, asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app.core.database import AsyncSessionLocal
from app.models.dish import Dish, DtypeEnum, FtypeEnum, DifficultyEnum
from app.models.dish_ingredient import DishIngredient
from sqlalchemy import delete as sql_delete

DISHES = json.loads(r'''[
  {
    "name": "红烧肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 60,
    "difficulty": "中等",
    "health_score": 25,
    "main_ingredients": [
      {
        "name": "五花肉",
        "amount": "500g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "八角",
        "amount": "2个"
      },
      {
        "name": "桂皮",
        "amount": "1小块"
      },
      {
        "name": "香叶",
        "amount": "2片"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "冰糖",
        "amount": "30g"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "五花肉切3cm方块",
        "step": 1
      },
      {
        "name": "冷水下锅焯水捞出",
        "step": 2
      },
      {
        "name": "小火炒糖色至棕红色",
        "step": 3
      },
      {
        "name": "下肉块翻炒上色",
        "step": 4
      },
      {
        "name": "加葱姜八角桂皮香叶炒香",
        "step": 5
      },
      {
        "name": "加生抽老抽料酒倒开水没过肉",
        "step": 6
      },
      {
        "name": "大火烧开转小火炖40分钟",
        "step": 7
      },
      {
        "name": "加盐大火收汁",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "炒糖色火不能大会苦"
      },
      {
        "name": "一定要加开水冷水会让肉变柴"
      },
      {
        "name": "收汁时要不停翻动防粘锅"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "洗净沥干",
        "items": [
          {
            "name": "五花肉"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "五花肉",
            "shape": "3cm方块"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "糖醋排骨",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 45,
    "difficulty": "中等",
    "health_score": 35,
    "main_ingredients": [
      {
        "name": "排骨",
        "amount": "500g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "白芝麻",
        "amount": "少许"
      }
    ],
    "seasonings": [
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "香醋",
        "amount": "3勺"
      },
      {
        "name": "白糖",
        "amount": "4勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "排骨斩段冷水焯水",
        "step": 1
      },
      {
        "name": "调糖醋汁:料酒1生抽2老抽半醋3糖4水5勺",
        "step": 2
      },
      {
        "name": "油热下排骨煎至两面金黄",
        "step": 3
      },
      {
        "name": "倒糖醋汁加开水没过排骨",
        "step": 4
      },
      {
        "name": "大火烧开转小火炖30分钟",
        "step": 5
      },
      {
        "name": "大火收汁撒白芝麻",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "糖醋汁比例好记:1酒2酱3醋4糖"
      },
      {
        "name": "收汁注意不要糊锅"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "冷水浸泡20分钟去血水",
        "items": [
          {
            "name": "排骨"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "排骨",
            "shape": "小段"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "回锅肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 25,
    "difficulty": "中等",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "五花肉",
        "amount": "300g"
      },
      {
        "name": "蒜苗",
        "amount": "200g"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "干辣椒",
        "amount": "5个"
      }
    ],
    "seasonings": [
      {
        "name": "郫县豆瓣酱",
        "amount": "2勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "甜面酱",
        "amount": "半勺"
      },
      {
        "name": "白糖",
        "amount": "少许"
      },
      {
        "name": "花椒",
        "amount": "10粒"
      }
    ],
    "cooking_steps": [
      {
        "name": "五花肉整块冷水煮20分钟至筷子能插入",
        "step": 1
      },
      {
        "name": "捞出放凉切薄片",
        "step": 2
      },
      {
        "name": "蒜苗斜刀切段蒜白蒜叶分开",
        "step": 3
      },
      {
        "name": "锅不放油下肉片中火煸至卷曲出油",
        "step": 4
      },
      {
        "name": "肉拨一边下豆瓣酱炒出红油",
        "step": 5
      },
      {
        "name": "下姜蒜干辣椒花椒炒香",
        "step": 6
      },
      {
        "name": "加甜面酱生抽白糖翻炒",
        "step": 7
      },
      {
        "name": "先下蒜白再下蒜叶断生出锅",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "肉要煮透才能切薄片"
      },
      {
        "name": "煸肉不放油肉自己出油"
      },
      {
        "name": "豆瓣酱有咸味盐要少放"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "五花肉整块洗",
        "items": [
          {
            "name": "五花肉"
          },
          {
            "name": "蒜苗"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "五花肉",
            "shape": "薄片"
          },
          {
            "name": "蒜苗",
            "shape": "斜刀段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "宫保鸡丁",
    "dtype": "硬菜",
    "ftype": "飞",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 20,
    "difficulty": "中等",
    "health_score": 45,
    "main_ingredients": [
      {
        "name": "鸡胸肉",
        "amount": "300g"
      },
      {
        "name": "花生米",
        "amount": "50g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "干辣椒",
        "amount": "8个"
      },
      {
        "name": "花椒",
        "amount": "1把"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "醋",
        "amount": "2勺"
      },
      {
        "name": "白糖",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "鸡胸切丁加料酒淀粉盐腌10分钟",
        "step": 1
      },
      {
        "name": "调碗汁:生抽2醋2糖1淀粉1水3勺",
        "step": 2
      },
      {
        "name": "花生米小火炒至金黄盛出",
        "step": 3
      },
      {
        "name": "油热下鸡丁滑炒变白盛出",
        "step": 4
      },
      {
        "name": "留底油爆香花椒干辣椒姜蒜",
        "step": 5
      },
      {
        "name": "下鸡丁和葱段翻炒",
        "step": 6
      },
      {
        "name": "倒碗汁翻炒均匀",
        "step": 7
      },
      {
        "name": "撒花生米翻匀出锅",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "鸡丁不要炒太久会老"
      },
      {
        "name": "花生米最后放保持酥脆"
      },
      {
        "name": "花椒干辣椒量决定麻辣程度"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "加料酒淀粉盐",
        "items": [
          {
            "name": "鸡胸肉",
            "amount": "300g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "洗",
        "note": "鸡胸去筋膜",
        "items": [
          {
            "name": "鸡胸肉"
          },
          {
            "name": "葱"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "鸡胸肉",
            "shape": "1.5cm丁"
          },
          {
            "name": "葱",
            "shape": "小段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "鱼香肉丝",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 20,
    "difficulty": "中等",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "猪里脊",
        "amount": "250g"
      },
      {
        "name": "木耳",
        "amount": "50g"
      },
      {
        "name": "胡萝卜",
        "amount": "1根"
      },
      {
        "name": "青椒",
        "amount": "1个"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      }
    ],
    "seasonings": [
      {
        "name": "郫县豆瓣酱",
        "amount": "1勺"
      },
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "醋",
        "amount": "2勺"
      },
      {
        "name": "白糖",
        "amount": "2勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "里脊切丝加料酒淀粉盐腌10分钟",
        "step": 1
      },
      {
        "name": "木耳泡发切丝胡萝卜青椒切丝",
        "step": 2
      },
      {
        "name": "调鱼香汁:生抽2醋2糖2淀粉1水3勺",
        "step": 3
      },
      {
        "name": "油热下肉丝滑炒变白盛出",
        "step": 4
      },
      {
        "name": "下豆瓣酱炒出红油加姜蒜末炒香",
        "step": 5
      },
      {
        "name": "下胡萝卜木耳青椒翻炒",
        "step": 6
      },
      {
        "name": "倒回肉丝淋鱼香汁翻匀",
        "step": 7
      },
      {
        "name": "撒葱花出锅",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "鱼香汁灵魂是糖醋比例1:1"
      },
      {
        "name": "没有豆瓣酱可用泡椒代替"
      },
      {
        "name": "木耳提前2小时泡发"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "温水泡发",
        "items": [
          {
            "name": "木耳",
            "amount": "50g"
          }
        ],
        "time_minutes": 120
      },
      {
        "act": "腌",
        "note": "料酒淀粉盐",
        "items": [
          {
            "name": "猪里脊",
            "amount": "250g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "胡萝卜"
          },
          {
            "name": "青椒"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "猪里脊",
            "shape": "细丝"
          },
          {
            "name": "胡萝卜",
            "shape": "细丝"
          },
          {
            "name": "青椒",
            "shape": "细丝"
          },
          {
            "name": "木耳",
            "shape": "丝"
          },
          {
            "name": "葱",
            "shape": "葱花"
          },
          {
            "name": "姜",
            "shape": "末"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "水煮肉片",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 30,
    "difficulty": "困难",
    "health_score": 30,
    "main_ingredients": [
      {
        "name": "猪里脊",
        "amount": "300g"
      },
      {
        "name": "豆芽",
        "amount": "200g"
      },
      {
        "name": "生菜",
        "amount": "1棵"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "干辣椒",
        "amount": "15个"
      },
      {
        "name": "花椒",
        "amount": "1把"
      }
    ],
    "seasonings": [
      {
        "name": "郫县豆瓣酱",
        "amount": "3勺"
      },
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "淀粉",
        "amount": "2勺"
      },
      {
        "name": "辣椒面",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "里脊切薄片加料酒淀粉盐腌15分钟",
        "step": 1
      },
      {
        "name": "干辣椒剪段花椒备好",
        "step": 2
      },
      {
        "name": "油热下干辣椒花椒炒香盛出切碎",
        "step": 3
      },
      {
        "name": "锅中炒豆芽和生菜至断生铺碗底",
        "step": 4
      },
      {
        "name": "油热下豆瓣酱炒出红油加姜蒜炒香",
        "step": 5
      },
      {
        "name": "加开水加生抽盐调味",
        "step": 6
      },
      {
        "name": "水开下肉片滑散煮1分钟",
        "step": 7
      },
      {
        "name": "连汤带肉倒碗中",
        "step": 8
      },
      {
        "name": "撒刀口辣椒蒜末辣椒面",
        "step": 9
      },
      {
        "name": "另起锅烧热油浇在上面",
        "step": 10
      }
    ],
    "attentions": [
      {
        "name": "肉片要逆纹切才嫩"
      },
      {
        "name": "最后浇油是灵魂不能省"
      },
      {
        "name": "刀口辣椒比直接放干辣椒香很多"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒淀粉盐",
        "items": [
          {
            "name": "猪里脊",
            "amount": "300g"
          }
        ],
        "time_minutes": 15
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "豆芽"
          },
          {
            "name": "生菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "猪里脊",
            "shape": "薄片"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "段"
          }
        ]
      }
    ]
  },
  {
    "name": "可乐鸡翅",
    "dtype": "硬菜",
    "ftype": "飞",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 25,
    "difficulty": "简单",
    "health_score": 35,
    "main_ingredients": [
      {
        "name": "鸡中翅",
        "amount": "10个"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "葱",
        "amount": "1根"
      }
    ],
    "seasonings": [
      {
        "name": "可乐",
        "amount": "330ml"
      },
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "鸡翅两面划刀",
        "step": 1
      },
      {
        "name": "冷水下锅加姜料酒焯水",
        "step": 2
      },
      {
        "name": "捞出洗净沥干",
        "step": 3
      },
      {
        "name": "油热下鸡翅煎至两面金黄",
        "step": 4
      },
      {
        "name": "倒可乐生抽老抽",
        "step": 5
      },
      {
        "name": "大火烧开转小火炖15分钟",
        "step": 6
      },
      {
        "name": "大火收汁至浓稠",
        "step": 7
      }
    ],
    "attentions": [
      {
        "name": "鸡翅划刀更入味"
      },
      {
        "name": "收汁不停翻动防粘锅"
      },
      {
        "name": "可乐已有甜味不需加糖"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "洗净沥干",
        "items": [
          {
            "name": "鸡中翅"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "鸡中翅",
            "shape": "两面划刀"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "段"
          }
        ]
      }
    ]
  },
  {
    "name": "红烧排骨",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 50,
    "difficulty": "中等",
    "health_score": 35,
    "main_ingredients": [
      {
        "name": "排骨",
        "amount": "600g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "八角",
        "amount": "2个"
      },
      {
        "name": "桂皮",
        "amount": "1小块"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "冰糖",
        "amount": "20g"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "排骨斩段冷水焯水",
        "step": 1
      },
      {
        "name": "炒糖色后下排骨翻炒上色",
        "step": 2
      },
      {
        "name": "加葱姜八角桂皮炒香",
        "step": 3
      },
      {
        "name": "加生抽老抽料酒倒开水",
        "step": 4
      },
      {
        "name": "大火烧开转小火炖40分钟",
        "step": 5
      },
      {
        "name": "加盐转大火收汁",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "焯水冷水下锅才能去血水"
      },
      {
        "name": "炖排骨加开水肉质更嫩"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "冷水浸泡去血水",
        "items": [
          {
            "name": "排骨"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "排骨",
            "shape": "小段"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "红烧鸡块",
    "dtype": "硬菜",
    "ftype": "飞",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 40,
    "difficulty": "简单",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "三黄鸡",
        "amount": "半只"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "干辣椒",
        "amount": "5个"
      },
      {
        "name": "八角",
        "amount": "2个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "冰糖",
        "amount": "15g"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "鸡块冷水焯水捞出",
        "step": 1
      },
      {
        "name": "油热下冰糖炒糖色",
        "step": 2
      },
      {
        "name": "下鸡块翻炒上色",
        "step": 3
      },
      {
        "name": "加葱姜蒜八角干辣椒炒香",
        "step": 4
      },
      {
        "name": "加料酒生抽老抽翻炒",
        "step": 5
      },
      {
        "name": "倒开水没过鸡块炖25分钟",
        "step": 6
      },
      {
        "name": "加盐大火收汁",
        "step": 7
      }
    ],
    "attentions": [
      {
        "name": "鸡肉比猪肉容易熟炖的时间短"
      },
      {
        "name": "土鸡需要多炖10分钟"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "洗净斩块",
        "items": [
          {
            "name": "三黄鸡"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "三黄鸡",
            "shape": "块"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "拍碎"
          }
        ]
      }
    ]
  },
  {
    "name": "红烧牛腩",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 9,
    "end_month": 3,
    "cooking_time": 90,
    "difficulty": "困难",
    "health_score": 35,
    "main_ingredients": [
      {
        "name": "牛腩",
        "amount": "600g"
      },
      {
        "name": "土豆",
        "amount": "2个"
      },
      {
        "name": "胡萝卜",
        "amount": "1根"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "八角",
        "amount": "2个"
      },
      {
        "name": "桂皮",
        "amount": "1块"
      },
      {
        "name": "香叶",
        "amount": "2片"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "3勺"
      },
      {
        "name": "冰糖",
        "amount": "20g"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "番茄酱",
        "amount": "1勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "牛腩切块冷水泡30分钟去血水",
        "step": 1
      },
      {
        "name": "冷水下锅焯水捞出",
        "step": 2
      },
      {
        "name": "炒糖色下牛腩翻炒上色",
        "step": 3
      },
      {
        "name": "加葱姜蒜八角桂皮香叶干辣椒炒香",
        "step": 4
      },
      {
        "name": "加料酒生抽老抽番茄酱",
        "step": 5
      },
      {
        "name": "加足量开水大火烧开转小火炖1小时",
        "step": 6
      },
      {
        "name": "土豆胡萝卜切滚刀块下锅再炖20分钟",
        "step": 7
      },
      {
        "name": "加盐大火收汁",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "牛腩需要长时间炖煮才软烂"
      },
      {
        "name": "番茄酱可让牛肉更易软烂"
      },
      {
        "name": "土豆后放避免煮化"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "冷水浸泡去血水",
        "items": [
          {
            "name": "牛腩"
          }
        ],
        "time_minutes": 30
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "土豆"
          },
          {
            "name": "胡萝卜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "牛腩",
            "shape": "3cm块"
          },
          {
            "name": "土豆",
            "shape": "滚刀块"
          },
          {
            "name": "胡萝卜",
            "shape": "滚刀块"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "拍碎"
          }
        ]
      }
    ]
  },
  {
    "name": "土豆炖牛肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 9,
    "end_month": 3,
    "cooking_time": 80,
    "difficulty": "中等",
    "health_score": 40,
    "main_ingredients": [
      {
        "name": "牛肉",
        "amount": "500g"
      },
      {
        "name": "土豆",
        "amount": "3个"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "八角",
        "amount": "2个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "牛肉切块焯水",
        "step": 1
      },
      {
        "name": "油热下葱姜八角炒香",
        "step": 2
      },
      {
        "name": "下牛肉翻炒加料酒",
        "step": 3
      },
      {
        "name": "加生抽老抽翻炒上色",
        "step": 4
      },
      {
        "name": "加开水炖50分钟",
        "step": 5
      },
      {
        "name": "下土豆块再炖20分钟",
        "step": 6
      },
      {
        "name": "加盐大火收汁",
        "step": 7
      }
    ],
    "attentions": [
      {
        "name": "牛肉逆纹切口感更好"
      },
      {
        "name": "土豆不要切太小块"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "冷水浸泡",
        "items": [
          {
            "name": "牛肉"
          }
        ],
        "time_minutes": 20
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "土豆"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "牛肉",
            "shape": "3cm块"
          },
          {
            "name": "土豆",
            "shape": "滚刀块"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "糖醋里脊",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 25,
    "difficulty": "中等",
    "health_score": 30,
    "main_ingredients": [
      {
        "name": "猪里脊",
        "amount": "300g"
      }
    ],
    "side_ingredients": [
      {
        "name": "鸡蛋",
        "amount": "1个"
      },
      {
        "name": "白芝麻",
        "amount": "少许"
      }
    ],
    "seasonings": [
      {
        "name": "番茄酱",
        "amount": "3勺"
      },
      {
        "name": "白醋",
        "amount": "2勺"
      },
      {
        "name": "白糖",
        "amount": "3勺"
      },
      {
        "name": "淀粉",
        "amount": "100g"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "里脊切条加料酒盐腌10分钟",
        "step": 1
      },
      {
        "name": "鸡蛋加淀粉调成糊",
        "step": 2
      },
      {
        "name": "里脊挂糊六成油温炸至金黄捞出",
        "step": 3
      },
      {
        "name": "油温升高复炸30秒至酥脆",
        "step": 4
      },
      {
        "name": "锅中少许油加番茄酱糖醋水熬至浓稠",
        "step": 5
      },
      {
        "name": "倒里脊快速翻炒均匀",
        "step": 6
      },
      {
        "name": "撒白芝麻出锅",
        "step": 7
      }
    ],
    "attentions": [
      {
        "name": "复炸是酥脆的关键"
      },
      {
        "name": "糖醋汁熬到冒大泡时最合适"
      },
      {
        "name": "裹汁要快否则里脊会软"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒盐",
        "items": [
          {
            "name": "猪里脊",
            "amount": "300g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "猪里脊",
            "shape": "手指粗条"
          }
        ]
      }
    ]
  },
  {
    "name": "京酱肉丝",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 20,
    "difficulty": "中等",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "猪里脊",
        "amount": "300g"
      },
      {
        "name": "大葱",
        "amount": "2根"
      },
      {
        "name": "豆腐皮",
        "amount": "3张"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "3片"
      }
    ],
    "seasonings": [
      {
        "name": "甜面酱",
        "amount": "2勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "白糖",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "香油",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "里脊切丝加料酒淀粉腌10分钟",
        "step": 1
      },
      {
        "name": "大葱白切细丝铺盘底",
        "step": 2
      },
      {
        "name": "豆腐皮切片焯水备用",
        "step": 3
      },
      {
        "name": "油热下肉丝滑炒变白盛出",
        "step": 4
      },
      {
        "name": "留底油下甜面酱白糖炒香",
        "step": 5
      },
      {
        "name": "加生抽和少许水",
        "step": 6
      },
      {
        "name": "倒回肉丝翻炒均匀",
        "step": 7
      },
      {
        "name": "淋香油出锅放在葱丝上",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "甜面酱是灵魂不要用豆瓣酱替代"
      },
      {
        "name": "葱要选葱白部分切细丝"
      },
      {
        "name": "吃的时候用豆腐皮卷肉丝和葱丝"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒淀粉",
        "items": [
          {
            "name": "猪里脊",
            "amount": "300g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "猪里脊",
            "shape": "细丝"
          },
          {
            "name": "大葱",
            "shape": "细丝"
          }
        ]
      }
    ]
  },
  {
    "name": "蒜香排骨",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 35,
    "difficulty": "中等",
    "health_score": 30,
    "main_ingredients": [
      {
        "name": "排骨",
        "amount": "500g"
      },
      {
        "name": "蒜",
        "amount": "1整头"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "青椒",
        "amount": "1个"
      },
      {
        "name": "红椒",
        "amount": "1个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "蚝油",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "胡椒粉",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "排骨斩段加蒜蓉生抽料酒蚝油腌30分钟",
        "step": 1
      },
      {
        "name": "加淀粉拌匀",
        "step": 2
      },
      {
        "name": "六成油温炸排骨5分钟捞出",
        "step": 3
      },
      {
        "name": "升高油温复炸至金黄酥脆",
        "step": 4
      },
      {
        "name": "留底油炒青红椒粒和蒜末",
        "step": 5
      },
      {
        "name": "下排骨翻匀出锅",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "腌制时间越长越入味"
      },
      {
        "name": "复炸是外酥里嫩的关键"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "蒜蓉生抽料酒蚝油",
        "items": [
          {
            "name": "排骨",
            "amount": "500g"
          },
          {
            "name": "蒜",
            "amount": "1整头"
          }
        ],
        "time_minutes": 30
      },
      {
        "act": "切",
        "items": [
          {
            "name": "排骨",
            "shape": "小段"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "青椒",
            "shape": "小粒"
          },
          {
            "name": "红椒",
            "shape": "小粒"
          }
        ]
      }
    ]
  },
  {
    "name": "小炒肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 15,
    "difficulty": "简单",
    "health_score": 55,
    "main_ingredients": [
      {
        "name": "五花肉",
        "amount": "250g"
      },
      {
        "name": "青椒",
        "amount": "4个"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "豆豉",
        "amount": "1勺"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "五花肉切薄片",
        "step": 1
      },
      {
        "name": "青椒切滚刀块不放油干煸至起虎皮",
        "step": 2
      },
      {
        "name": "放少许油下五花肉煸出油",
        "step": 3
      },
      {
        "name": "下蒜片豆豉炒香",
        "step": 4
      },
      {
        "name": "加料酒生抽老抽翻炒",
        "step": 5
      },
      {
        "name": "下青椒翻炒均匀",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "青椒先干煸更香"
      },
      {
        "name": "肉要薄才能快速煸出油"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "青椒"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "五花肉",
            "shape": "薄片"
          },
          {
            "name": "青椒",
            "shape": "滚刀块"
          },
          {
            "name": "蒜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "黄焖鸡",
    "dtype": "硬菜",
    "ftype": "飞",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 35,
    "difficulty": "中等",
    "health_score": 55,
    "main_ingredients": [
      {
        "name": "鸡腿",
        "amount": "3个"
      },
      {
        "name": "土豆",
        "amount": "2个"
      },
      {
        "name": "香菇",
        "amount": "6朵"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "蚝油",
        "amount": "1勺"
      },
      {
        "name": "冰糖",
        "amount": "10g"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "鸡腿斩块冷水焯水",
        "step": 1
      },
      {
        "name": "炒糖色下鸡块翻炒",
        "step": 2
      },
      {
        "name": "加葱姜蒜干辣椒炒香",
        "step": 3
      },
      {
        "name": "加生抽老抽蚝油料酒",
        "step": 4
      },
      {
        "name": "加开水和香菇炖15分钟",
        "step": 5
      },
      {
        "name": "加土豆再炖10分钟",
        "step": 6
      },
      {
        "name": "加盐收汁",
        "step": 7
      }
    ],
    "attentions": [
      {
        "name": "鸡腿比鸡胸更嫩"
      },
      {
        "name": "干香菇比鲜香菇更香"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "温水泡发",
        "items": [
          {
            "name": "干香菇",
            "amount": "6朵"
          }
        ],
        "time_minutes": 30
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "鸡腿"
          },
          {
            "name": "土豆"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "鸡腿",
            "shape": "块"
          },
          {
            "name": "土豆",
            "shape": "滚刀块"
          },
          {
            "name": "香菇",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "啤酒鸭",
    "dtype": "硬菜",
    "ftype": "飞",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 60,
    "difficulty": "中等",
    "health_score": 45,
    "main_ingredients": [
      {
        "name": "鸭肉",
        "amount": "半只"
      },
      {
        "name": "啤酒",
        "amount": "1罐"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "干辣椒",
        "amount": "5个"
      },
      {
        "name": "八角",
        "amount": "2个"
      },
      {
        "name": "桂皮",
        "amount": "1块"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "白糖",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "鸭肉斩块冷水焯水捞出",
        "step": 1
      },
      {
        "name": "锅不放油下鸭肉煸炒出油",
        "step": 2
      },
      {
        "name": "加葱姜蒜八角桂皮干辣椒炒香",
        "step": 3
      },
      {
        "name": "加生抽老抽料酒翻炒",
        "step": 4
      },
      {
        "name": "倒啤酒和适量水",
        "step": 5
      },
      {
        "name": "大火烧开转小火炖40分钟",
        "step": 6
      },
      {
        "name": "加盐大火收汁",
        "step": 7
      }
    ],
    "attentions": [
      {
        "name": "鸭肉先煸出油才不腥"
      },
      {
        "name": "啤酒去腥效果很好"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "洗净斩块",
        "items": [
          {
            "name": "鸭肉"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "鸭肉",
            "shape": "块"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "拍碎"
          }
        ]
      }
    ]
  },
  {
    "name": "孜然牛肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 15,
    "difficulty": "中等",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "牛肉",
        "amount": "300g"
      },
      {
        "name": "洋葱",
        "amount": "半个"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "香菜",
        "amount": "2根"
      }
    ],
    "seasonings": [
      {
        "name": "孜然粉",
        "amount": "2勺"
      },
      {
        "name": "辣椒面",
        "amount": "1勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "牛肉逆纹切薄片加料酒生抽淀粉腌10分钟",
        "step": 1
      },
      {
        "name": "油热下牛肉大火滑炒至变色盛出",
        "step": 2
      },
      {
        "name": "下洋葱丝姜丝爆香",
        "step": 3
      },
      {
        "name": "倒回牛肉加孜然辣椒面盐翻炒",
        "step": 4
      },
      {
        "name": "撒香菜出锅",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "全程大火快炒牛肉才嫩"
      },
      {
        "name": "牛肉不要炒太久会老"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒生抽淀粉",
        "items": [
          {
            "name": "牛肉",
            "amount": "300g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "牛肉",
            "shape": "薄片逆纹"
          },
          {
            "name": "洋葱",
            "shape": "丝"
          },
          {
            "name": "姜",
            "shape": "丝"
          }
        ]
      }
    ]
  },
  {
    "name": "葱爆羊肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 10,
    "end_month": 3,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "羊肉片",
        "amount": "300g"
      },
      {
        "name": "大葱",
        "amount": "3根"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "孜然粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "白胡椒粉",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "羊肉片加料酒白胡椒粉腌5分钟",
        "step": 1
      },
      {
        "name": "大葱斜刀切片",
        "step": 2
      },
      {
        "name": "油热下羊肉大火爆炒至变色",
        "step": 3
      },
      {
        "name": "下姜蒜炒香",
        "step": 4
      },
      {
        "name": "下大葱翻炒30秒",
        "step": 5
      },
      {
        "name": "加生抽孜然盐快速翻匀出锅",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "全程大火爆炒不超过3分钟"
      },
      {
        "name": "大葱不要炒太久保持脆甜"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒白胡椒粉",
        "items": [
          {
            "name": "羊肉片",
            "amount": "300g"
          }
        ],
        "time_minutes": 5
      },
      {
        "act": "切",
        "items": [
          {
            "name": "大葱",
            "shape": "斜刀片"
          },
          {
            "name": "姜",
            "shape": "末"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "干煸豆角",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 15,
    "difficulty": "中等",
    "health_score": 55,
    "main_ingredients": [
      {
        "name": "豆角",
        "amount": "400g"
      },
      {
        "name": "猪肉末",
        "amount": "100g"
      }
    ],
    "side_ingredients": [
      {
        "name": "干辣椒",
        "amount": "8个"
      },
      {
        "name": "花椒",
        "amount": "1把"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "姜",
        "amount": "3片"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "豆角去筋掰段洗净沥干",
        "step": 1
      },
      {
        "name": "六成油温炸至起皱捞出",
        "step": 2
      },
      {
        "name": "留底油下肉末炒至酥香",
        "step": 3
      },
      {
        "name": "下干辣椒花椒姜蒜炒香",
        "step": 4
      },
      {
        "name": "下豆角加生抽盐翻炒",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "豆角一定要炸熟生豆角有毒"
      },
      {
        "name": "也可多放油慢慢煸代替炸"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "去筋洗净沥干",
        "items": [
          {
            "name": "豆角"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "豆角",
            "shape": "5cm段"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "姜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "辣子鸡丁",
    "dtype": "硬菜",
    "ftype": "飞",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 25,
    "difficulty": "困难",
    "health_score": 30,
    "main_ingredients": [
      {
        "name": "鸡腿肉",
        "amount": "400g"
      },
      {
        "name": "干辣椒",
        "amount": "30个"
      },
      {
        "name": "花椒",
        "amount": "2把"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "白芝麻",
        "amount": "少许"
      },
      {
        "name": "花生米",
        "amount": "30g"
      }
    ],
    "seasonings": [
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "白糖",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "2勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "鸡腿去骨切丁加料酒生抽盐淀粉腌15分钟",
        "step": 1
      },
      {
        "name": "干辣椒剪段去籽",
        "step": 2
      },
      {
        "name": "六成油温下鸡丁炸至金黄捞出",
        "step": 3
      },
      {
        "name": "升高油温复炸30秒",
        "step": 4
      },
      {
        "name": "留底油小火炒香花椒干辣椒",
        "step": 5
      },
      {
        "name": "下姜蒜片翻炒出香",
        "step": 6
      },
      {
        "name": "下鸡丁加白糖翻炒均匀",
        "step": 7
      },
      {
        "name": "撒白芝麻花生米出锅",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "花椒和辣椒量要够多"
      },
      {
        "name": "小火炒花椒才不会苦"
      },
      {
        "name": "复炸让外酥里嫩"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒生抽盐淀粉",
        "items": [
          {
            "name": "鸡腿肉",
            "amount": "400g"
          }
        ],
        "time_minutes": 15
      },
      {
        "act": "切",
        "items": [
          {
            "name": "鸡腿肉",
            "shape": "1.5cm丁"
          },
          {
            "name": "干辣椒",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "段"
          }
        ]
      }
    ]
  },
  {
    "name": "木须肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 15,
    "difficulty": "简单",
    "health_score": 60,
    "main_ingredients": [
      {
        "name": "猪里脊",
        "amount": "150g"
      },
      {
        "name": "鸡蛋",
        "amount": "3个"
      },
      {
        "name": "木耳",
        "amount": "30g"
      },
      {
        "name": "黄花菜",
        "amount": "30g"
      },
      {
        "name": "黄瓜",
        "amount": "1根"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "1根"
      },
      {
        "name": "姜",
        "amount": "2片"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "香油",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "里脊切片加料酒淀粉腌",
        "step": 1
      },
      {
        "name": "木耳黄花菜泡发",
        "step": 2
      },
      {
        "name": "鸡蛋打散炒熟盛出",
        "step": 3
      },
      {
        "name": "肉片滑炒变色盛出",
        "step": 4
      },
      {
        "name": "下葱姜炒香下木耳黄花菜黄瓜翻炒",
        "step": 5
      },
      {
        "name": "倒回肉和鸡蛋加生抽盐翻炒",
        "step": 6
      },
      {
        "name": "淋香油出锅",
        "step": 7
      }
    ],
    "attentions": [
      {
        "name": "木耳黄花菜提前2小时泡发"
      },
      {
        "name": "鸡蛋和肉分开炒才能保持口感"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "温水泡发",
        "items": [
          {
            "name": "木耳",
            "amount": "30g"
          },
          {
            "name": "黄花菜",
            "amount": "30g"
          }
        ],
        "time_minutes": 120
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "黄瓜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "猪里脊",
            "shape": "片"
          },
          {
            "name": "黄瓜",
            "shape": "菱形片"
          },
          {
            "name": "葱",
            "shape": "末"
          },
          {
            "name": "姜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "青椒肉丝",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 60,
    "main_ingredients": [
      {
        "name": "猪里脊",
        "amount": "200g"
      },
      {
        "name": "青椒",
        "amount": "3个"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "2片"
      },
      {
        "name": "蒜",
        "amount": "2瓣"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "里脊切丝加料酒淀粉盐腌",
        "step": 1
      },
      {
        "name": "青椒切丝",
        "step": 2
      },
      {
        "name": "油热下肉丝滑炒变色盛出",
        "step": 3
      },
      {
        "name": "下姜蒜炒香下青椒翻炒",
        "step": 4
      },
      {
        "name": "倒回肉丝加生抽盐翻匀出锅",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "最基础的家常菜"
      },
      {
        "name": "肉丝先腌才嫩"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒淀粉盐",
        "items": [
          {
            "name": "猪里脊",
            "amount": "200g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "猪里脊",
            "shape": "丝"
          },
          {
            "name": "青椒",
            "shape": "丝"
          },
          {
            "name": "姜",
            "shape": "末"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "锅包肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 25,
    "difficulty": "困难",
    "health_score": 25,
    "main_ingredients": [
      {
        "name": "猪里脊",
        "amount": "300g"
      }
    ],
    "side_ingredients": [
      {
        "name": "胡萝卜",
        "amount": "半根"
      },
      {
        "name": "大葱",
        "amount": "1根"
      },
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "香菜",
        "amount": "2根"
      }
    ],
    "seasonings": [
      {
        "name": "白糖",
        "amount": "4勺"
      },
      {
        "name": "白醋",
        "amount": "4勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "土豆淀粉",
        "amount": "200g"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "里脊切厚片用刀拍松",
        "step": 1
      },
      {
        "name": "土豆淀粉加水泡30分钟后倒掉上层水",
        "step": 2
      },
      {
        "name": "肉片裹湿淀粉",
        "step": 3
      },
      {
        "name": "六成油温逐片下锅炸至定型捞出",
        "step": 4
      },
      {
        "name": "升高油温复炸至金黄酥脆",
        "step": 5
      },
      {
        "name": "锅中糖醋生抽盐熬至浓稠",
        "step": 6
      },
      {
        "name": "下葱姜胡萝卜丝炒香",
        "step": 7
      },
      {
        "name": "下肉片快速翻炒裹汁",
        "step": 8
      },
      {
        "name": "撒香菜出锅",
        "step": 9
      }
    ],
    "attentions": [
      {
        "name": "必须用土豆淀粉玉米淀粉不够脆"
      },
      {
        "name": "复炸是酥脆关键"
      },
      {
        "name": "糖醋汁要熬到拉丝状态"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "加水沉淀后去上层水",
        "items": [
          {
            "name": "土豆淀粉",
            "amount": "200g"
          }
        ],
        "time_minutes": 30
      },
      {
        "act": "切",
        "items": [
          {
            "name": "猪里脊",
            "shape": "3mm厚片"
          },
          {
            "name": "胡萝卜",
            "shape": "丝"
          },
          {
            "name": "大葱",
            "shape": "丝"
          },
          {
            "name": "姜",
            "shape": "丝"
          }
        ]
      }
    ]
  },
  {
    "name": "东坡肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 120,
    "difficulty": "困难",
    "health_score": 20,
    "main_ingredients": [
      {
        "name": "五花肉",
        "amount": "800g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "4根"
      },
      {
        "name": "姜",
        "amount": "10片"
      },
      {
        "name": "八角",
        "amount": "2个"
      },
      {
        "name": "桂皮",
        "amount": "1块"
      },
      {
        "name": "香叶",
        "amount": "2片"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "3勺"
      },
      {
        "name": "老抽",
        "amount": "2勺"
      },
      {
        "name": "料酒",
        "amount": "200ml"
      },
      {
        "name": "冰糖",
        "amount": "50g"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "五花肉整块冷水煮10分钟定型",
        "step": 1
      },
      {
        "name": "捞出切4cm方块用棉线扎紧",
        "step": 2
      },
      {
        "name": "砂锅底铺葱段姜片",
        "step": 3
      },
      {
        "name": "肉皮朝下码入锅中",
        "step": 4
      },
      {
        "name": "加料酒生抽老抽冰糖八角桂皮香叶",
        "step": 5
      },
      {
        "name": "加开水没过肉",
        "step": 6
      },
      {
        "name": "大火烧开转小火炖90分钟",
        "step": 7
      },
      {
        "name": "翻面肉皮朝上再炖30分钟",
        "step": 8
      },
      {
        "name": "大火收汁至浓稠",
        "step": 9
      }
    ],
    "attentions": [
      {
        "name": "用棉线扎紧防止肉炖散"
      },
      {
        "name": "料酒代替水肉更香"
      },
      {
        "name": "慢炖是关键急不得"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "整块洗净",
        "items": [
          {
            "name": "五花肉"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "五花肉",
            "shape": "4cm方块"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "粉蒸肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 60,
    "difficulty": "中等",
    "health_score": 35,
    "main_ingredients": [
      {
        "name": "五花肉",
        "amount": "500g"
      },
      {
        "name": "蒸肉粉",
        "amount": "150g"
      },
      {
        "name": "红薯",
        "amount": "1个"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      }
    ],
    "seasonings": [
      {
        "name": "郫县豆瓣酱",
        "amount": "1勺"
      },
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "腐乳汁",
        "amount": "1勺"
      },
      {
        "name": "白糖",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "五花肉切厚片加所有调料腌30分钟",
        "step": 1
      },
      {
        "name": "红薯去皮切块铺碗底",
        "step": 2
      },
      {
        "name": "腌好的肉裹蒸肉粉",
        "step": 3
      },
      {
        "name": "肉片铺在红薯上",
        "step": 4
      },
      {
        "name": "上锅大火蒸40分钟",
        "step": 5
      },
      {
        "name": "出锅撒葱花",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "腌肉时间越长越入味"
      },
      {
        "name": "蒸的时候碗上盖保鲜膜防进水"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "所有调料腌制",
        "items": [
          {
            "name": "五花肉",
            "amount": "500g"
          }
        ],
        "time_minutes": 30
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "红薯"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "五花肉",
            "shape": "5mm厚片"
          },
          {
            "name": "红薯",
            "shape": "块"
          },
          {
            "name": "姜",
            "shape": "末"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "红烧鲫鱼",
    "dtype": "硬菜",
    "ftype": "游",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 25,
    "difficulty": "中等",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "鲫鱼",
        "amount": "1条约500g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "白糖",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "鲫鱼处理干净划花刀",
        "step": 1
      },
      {
        "name": "擦干水分两面拍少许淀粉",
        "step": 2
      },
      {
        "name": "油热下鱼煎至两面金黄盛出",
        "step": 3
      },
      {
        "name": "留底油下葱姜蒜干辣椒爆香",
        "step": 4
      },
      {
        "name": "加生抽老抽料酒白糖和水",
        "step": 5
      },
      {
        "name": "放入鱼大火烧开转小火烧8分钟",
        "step": 6
      },
      {
        "name": "翻面再烧3分钟",
        "step": 7
      },
      {
        "name": "大火收汁",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "鱼下锅前一定要擦干水分防溅油"
      },
      {
        "name": "煎鱼时不要翻动等一面定型"
      },
      {
        "name": "烧鱼中途不要频繁翻动"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "去鳞去鳃去内脏洗净",
        "items": [
          {
            "name": "鲫鱼"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "鲫鱼",
            "shape": "两面划花刀"
          },
          {
            "name": "葱",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "拍碎"
          }
        ]
      }
    ]
  },
  {
    "name": "清蒸鲈鱼",
    "dtype": "硬菜",
    "ftype": "游",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 15,
    "difficulty": "简单",
    "health_score": 95,
    "main_ingredients": [
      {
        "name": "鲈鱼",
        "amount": "1条约500g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "3根"
      },
      {
        "name": "姜",
        "amount": "10片"
      },
      {
        "name": "红椒",
        "amount": "半个"
      }
    ],
    "seasonings": [
      {
        "name": "蒸鱼豉油",
        "amount": "3勺"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "鲈鱼处理干净划花刀",
        "step": 1
      },
      {
        "name": "鱼身抹料酒和盐塞姜片",
        "step": 2
      },
      {
        "name": "盘中铺葱段姜片放上鱼",
        "step": 3
      },
      {
        "name": "水开上锅大火蒸8分钟",
        "step": 4
      },
      {
        "name": "倒掉盘中蒸出的汁水",
        "step": 5
      },
      {
        "name": "葱姜红椒切丝撒在鱼上",
        "step": 6
      },
      {
        "name": "淋蒸鱼豉油",
        "step": 7
      },
      {
        "name": "另起锅烧热油浇在葱丝上",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "蒸鱼时间不能太长8分钟刚好"
      },
      {
        "name": "蒸出的汁水一定要倒掉否则腥"
      },
      {
        "name": "最后浇热油是点睛之笔"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "去鳞去鳃去内脏洗净",
        "items": [
          {
            "name": "鲈鱼"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "鲈鱼",
            "shape": "两面划花刀"
          },
          {
            "name": "葱",
            "shape": "丝"
          },
          {
            "name": "姜",
            "shape": "片和丝"
          },
          {
            "name": "红椒",
            "shape": "丝"
          }
        ]
      }
    ]
  },
  {
    "name": "水煮鱼",
    "dtype": "硬菜",
    "ftype": "游",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 30,
    "difficulty": "困难",
    "health_score": 35,
    "main_ingredients": [
      {
        "name": "草鱼",
        "amount": "1条约1kg"
      },
      {
        "name": "豆芽",
        "amount": "200g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "10片"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "干辣椒",
        "amount": "20个"
      },
      {
        "name": "花椒",
        "amount": "2把"
      }
    ],
    "seasonings": [
      {
        "name": "郫县豆瓣酱",
        "amount": "3勺"
      },
      {
        "name": "料酒",
        "amount": "3勺"
      },
      {
        "name": "淀粉",
        "amount": "2勺"
      },
      {
        "name": "蛋清",
        "amount": "1个"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "辣椒面",
        "amount": "1勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "草鱼取肉片薄片鱼骨斩段",
        "step": 1
      },
      {
        "name": "鱼片加料酒蛋清淀粉盐腌15分钟",
        "step": 2
      },
      {
        "name": "豆芽焯水铺碗底",
        "step": 3
      },
      {
        "name": "油热下豆瓣酱炒出红油加姜炒香",
        "step": 4
      },
      {
        "name": "下鱼骨煎一下加开水煮5分钟",
        "step": 5
      },
      {
        "name": "捞出鱼骨放碗中",
        "step": 6
      },
      {
        "name": "汤中下鱼片煮1分钟至变白",
        "step": 7
      },
      {
        "name": "连汤带鱼倒入碗中",
        "step": 8
      },
      {
        "name": "撒干辣椒花椒蒜末辣椒面",
        "step": 9
      },
      {
        "name": "烧热油浇在上面",
        "step": 10
      }
    ],
    "attentions": [
      {
        "name": "鱼片要切得薄逆纹切"
      },
      {
        "name": "煮鱼片时间不超过1分钟"
      },
      {
        "name": "最后浇油是灵魂"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒蛋清淀粉盐",
        "items": [
          {
            "name": "草鱼片",
            "amount": "约500g"
          }
        ],
        "time_minutes": 15
      },
      {
        "act": "洗",
        "note": "洗净沥干",
        "items": [
          {
            "name": "豆芽"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "草鱼",
            "shape": "薄片和骨段"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "段"
          }
        ]
      }
    ]
  },
  {
    "name": "酸菜鱼",
    "dtype": "硬菜",
    "ftype": "游",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 25,
    "difficulty": "中等",
    "health_score": 40,
    "main_ingredients": [
      {
        "name": "草鱼",
        "amount": "1条"
      },
      {
        "name": "酸菜",
        "amount": "200g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "10片"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "干辣椒",
        "amount": "10个"
      },
      {
        "name": "花椒",
        "amount": "1把"
      },
      {
        "name": "泡椒",
        "amount": "5个"
      }
    ],
    "seasonings": [
      {
        "name": "料酒",
        "amount": "3勺"
      },
      {
        "name": "淀粉",
        "amount": "2勺"
      },
      {
        "name": "蛋清",
        "amount": "1个"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "白胡椒粉",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "草鱼取肉片薄片鱼骨斩段",
        "step": 1
      },
      {
        "name": "鱼片加料酒蛋清淀粉盐白胡椒腌15分钟",
        "step": 2
      },
      {
        "name": "酸菜切丝泡椒切段",
        "step": 3
      },
      {
        "name": "油热下鱼骨煎至金黄",
        "step": 4
      },
      {
        "name": "下酸菜泡椒姜蒜炒香",
        "step": 5
      },
      {
        "name": "加开水煮5分钟捞出鱼骨酸菜",
        "step": 6
      },
      {
        "name": "汤中下鱼片煮1分钟",
        "step": 7
      },
      {
        "name": "撒干辣椒花椒蒜末浇热油",
        "step": 8
      }
    ],
    "attentions": [
      {
        "name": "酸菜要先炒一下才香"
      },
      {
        "name": "鱼片不要煮太久"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒蛋清淀粉盐白胡椒",
        "items": [
          {
            "name": "草鱼片"
          }
        ],
        "time_minutes": 15
      },
      {
        "act": "洗",
        "note": "酸菜多洗几遍去咸味",
        "items": [
          {
            "name": "酸菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "草鱼",
            "shape": "薄片和骨段"
          },
          {
            "name": "酸菜",
            "shape": "丝"
          },
          {
            "name": "泡椒",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "排骨玉米汤",
    "dtype": "肉汤",
    "ftype": "跑",
    "start_month": 6,
    "end_month": 10,
    "cooking_time": 90,
    "difficulty": "简单",
    "health_score": 75,
    "main_ingredients": [
      {
        "name": "排骨",
        "amount": "500g"
      },
      {
        "name": "玉米",
        "amount": "2根"
      },
      {
        "name": "胡萝卜",
        "amount": "1根"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "枸杞",
        "amount": "10粒"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "排骨冷水焯水捞出",
        "step": 1
      },
      {
        "name": "玉米胡萝卜切段",
        "step": 2
      },
      {
        "name": "排骨玉米胡萝卜姜片入锅",
        "step": 3
      },
      {
        "name": "加足水大火烧开转小火煲1小时",
        "step": 4
      },
      {
        "name": "加盐调味撒枸杞",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "煲汤水要一次加足"
      },
      {
        "name": "盐要最后放"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "排骨冷水浸泡去血水",
        "items": [
          {
            "name": "排骨"
          },
          {
            "name": "玉米"
          },
          {
            "name": "胡萝卜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "排骨",
            "shape": "段"
          },
          {
            "name": "玉米",
            "shape": "段"
          },
          {
            "name": "胡萝卜",
            "shape": "滚刀块"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "冬瓜排骨汤",
    "dtype": "肉汤",
    "ftype": "跑",
    "start_month": 7,
    "end_month": 9,
    "cooking_time": 90,
    "difficulty": "简单",
    "health_score": 75,
    "main_ingredients": [
      {
        "name": "排骨",
        "amount": "500g"
      },
      {
        "name": "冬瓜",
        "amount": "500g"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "枸杞",
        "amount": "10粒"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "排骨焯水",
        "step": 1
      },
      {
        "name": "冬瓜去皮去瓤切块",
        "step": 2
      },
      {
        "name": "排骨姜片入锅加水煲1小时",
        "step": 3
      },
      {
        "name": "下冬瓜再煲15分钟",
        "step": 4
      },
      {
        "name": "加盐撒枸杞",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "冬瓜不要放太早会煮化"
      },
      {
        "name": "夏天喝非常清爽"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "排骨浸泡去血水",
        "items": [
          {
            "name": "排骨"
          },
          {
            "name": "冬瓜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "排骨",
            "shape": "段"
          },
          {
            "name": "冬瓜",
            "shape": "块"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "山药鸡汤",
    "dtype": "肉汤",
    "ftype": "飞",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 120,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "老母鸡",
        "amount": "半只"
      },
      {
        "name": "山药",
        "amount": "300g"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "枸杞",
        "amount": "15粒"
      },
      {
        "name": "红枣",
        "amount": "5颗"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "鸡块冷水焯水捞出",
        "step": 1
      },
      {
        "name": "鸡块姜片入锅加水大火烧开",
        "step": 2
      },
      {
        "name": "转小火煲90分钟",
        "step": 3
      },
      {
        "name": "山药去皮切段再煲15分钟",
        "step": 4
      },
      {
        "name": "加红枣枸杞盐",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "山药削皮戴手套否则手痒"
      },
      {
        "name": "鸡汤表面浮沫要撇干净"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "鸡洗净斩块",
        "items": [
          {
            "name": "老母鸡"
          },
          {
            "name": "山药"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "老母鸡",
            "shape": "块"
          },
          {
            "name": "山药",
            "shape": "段"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "番茄牛腩汤",
    "dtype": "肉汤",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 100,
    "difficulty": "中等",
    "health_score": 70,
    "main_ingredients": [
      {
        "name": "牛腩",
        "amount": "500g"
      },
      {
        "name": "番茄",
        "amount": "4个"
      },
      {
        "name": "土豆",
        "amount": "2个"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "番茄酱",
        "amount": "2勺"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "料酒",
        "amount": "3勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "牛腩切块焯水",
        "step": 1
      },
      {
        "name": "番茄划十字开水烫去皮切块",
        "step": 2
      },
      {
        "name": "油热下番茄炒出汁加番茄酱",
        "step": 3
      },
      {
        "name": "下牛腩姜葱料酒翻炒",
        "step": 4
      },
      {
        "name": "加开水煲70分钟",
        "step": 5
      },
      {
        "name": "下土豆块再煲20分钟",
        "step": 6
      },
      {
        "name": "加盐调味",
        "step": 7
      }
    ],
    "attentions": [
      {
        "name": "番茄用开水烫皮很好剥"
      },
      {
        "name": "番茄酱能增加汤的浓度"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "冷水浸泡去血水",
        "items": [
          {
            "name": "牛腩"
          }
        ],
        "time_minutes": 20
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "番茄"
          },
          {
            "name": "土豆"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "牛腩",
            "shape": "3cm块"
          },
          {
            "name": "番茄",
            "shape": "块"
          },
          {
            "name": "土豆",
            "shape": "块"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "段"
          }
        ]
      }
    ]
  },
  {
    "name": "萝卜排骨汤",
    "dtype": "肉汤",
    "ftype": "跑",
    "start_month": 10,
    "end_month": 3,
    "cooking_time": 90,
    "difficulty": "简单",
    "health_score": 75,
    "main_ingredients": [
      {
        "name": "排骨",
        "amount": "500g"
      },
      {
        "name": "白萝卜",
        "amount": "1根"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "枸杞",
        "amount": "10粒"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "排骨焯水",
        "step": 1
      },
      {
        "name": "白萝卜去皮切滚刀块",
        "step": 2
      },
      {
        "name": "排骨姜片煲1小时",
        "step": 3
      },
      {
        "name": "下萝卜再煲20分钟",
        "step": 4
      },
      {
        "name": "加盐撒枸杞葱花",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "冬天的白萝卜最甜"
      },
      {
        "name": "萝卜后放保持口感"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "排骨浸泡",
        "items": [
          {
            "name": "排骨"
          },
          {
            "name": "白萝卜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "排骨",
            "shape": "段"
          },
          {
            "name": "白萝卜",
            "shape": "滚刀块"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "番茄蛋花汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "番茄",
        "amount": "2个"
      },
      {
        "name": "鸡蛋",
        "amount": "2个"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "1根"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "番茄切块鸡蛋打散",
        "step": 1
      },
      {
        "name": "油热下番茄炒出汁",
        "step": 2
      },
      {
        "name": "加水煮开",
        "step": 3
      },
      {
        "name": "淋入蛋液搅出蛋花",
        "step": 4
      },
      {
        "name": "加盐香油撒葱花",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "番茄炒出汁再加水汤才浓"
      },
      {
        "name": "蛋液要等水开了再淋"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "番茄"
          },
          {
            "name": "葱"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "番茄",
            "shape": "块"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "紫菜蛋花汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 5,
    "difficulty": "简单",
    "health_score": 90,
    "main_ingredients": [
      {
        "name": "鸡蛋",
        "amount": "2个"
      },
      {
        "name": "紫菜",
        "amount": "1片"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "1根"
      },
      {
        "name": "虾皮",
        "amount": "1小把"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "紫菜撕碎鸡蛋打散",
        "step": 1
      },
      {
        "name": "水烧开下紫菜虾皮",
        "step": 2
      },
      {
        "name": "淋入蛋液",
        "step": 3
      },
      {
        "name": "加盐香油撒葱花",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "紫菜不要煮太久"
      },
      {
        "name": "加虾皮提鲜"
      }
    ],
    "prep_steps": [
      {
        "act": "切",
        "items": [
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "黄瓜蛋花汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 5,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "黄瓜",
        "amount": "1根"
      },
      {
        "name": "鸡蛋",
        "amount": "2个"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "1根"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "黄瓜切片鸡蛋打散",
        "step": 1
      },
      {
        "name": "水开下黄瓜片",
        "step": 2
      },
      {
        "name": "淋蛋液加盐",
        "step": 3
      },
      {
        "name": "香油葱花出锅",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "夏天喝非常清爽"
      },
      {
        "name": "黄瓜不要煮太久"
      }
    ],
    "prep_steps": [
      {
        "act": "切",
        "items": [
          {
            "name": "黄瓜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "豆腐青菜汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 95,
    "main_ingredients": [
      {
        "name": "嫩豆腐",
        "amount": "1块"
      },
      {
        "name": "青菜",
        "amount": "200g"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "2片"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "豆腐切小块青菜洗净",
        "step": 1
      },
      {
        "name": "水开下豆腐煮3分钟",
        "step": 2
      },
      {
        "name": "下青菜烫1分钟",
        "step": 3
      },
      {
        "name": "加盐香油",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "青菜最后放保持翠绿"
      },
      {
        "name": "豆腐先煮一会儿入味"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "逐片洗净",
        "items": [
          {
            "name": "青菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "嫩豆腐",
            "shape": "小块"
          }
        ]
      }
    ]
  },
  {
    "name": "酸辣土豆丝",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 70,
    "main_ingredients": [
      {
        "name": "土豆",
        "amount": "2个"
      }
    ],
    "side_ingredients": [
      {
        "name": "干辣椒",
        "amount": "5个"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "葱",
        "amount": "1根"
      },
      {
        "name": "花椒",
        "amount": "10粒"
      }
    ],
    "seasonings": [
      {
        "name": "醋",
        "amount": "2勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "土豆切细丝泡水洗去淀粉",
        "step": 1
      },
      {
        "name": "油热下花椒炸香捞出",
        "step": 2
      },
      {
        "name": "下干辣椒蒜片爆香",
        "step": 3
      },
      {
        "name": "大火下土豆丝翻炒2分钟",
        "step": 4
      },
      {
        "name": "锅边淋醋加生抽盐翻炒30秒",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "土豆丝一定要泡水去淀粉才脆"
      },
      {
        "name": "全程大火快炒"
      },
      {
        "name": "醋从锅边淋更香"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "泡水5分钟去淀粉",
        "items": [
          {
            "name": "土豆"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "土豆",
            "shape": "细丝"
          },
          {
            "name": "蒜",
            "shape": "片"
          },
          {
            "name": "干辣椒",
            "shape": "段"
          },
          {
            "name": "葱",
            "shape": "段"
          }
        ]
      }
    ]
  },
  {
    "name": "手撕包菜",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 75,
    "main_ingredients": [
      {
        "name": "包菜",
        "amount": "半个"
      }
    ],
    "side_ingredients": [
      {
        "name": "干辣椒",
        "amount": "5个"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "醋",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "包菜手撕成块洗净沥干",
        "step": 1
      },
      {
        "name": "油热下干辣椒蒜片爆香",
        "step": 2
      },
      {
        "name": "大火下包菜翻炒至断生",
        "step": 3
      },
      {
        "name": "加生抽盐醋翻匀出锅",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "手撕比刀切更好吃"
      },
      {
        "name": "全程大火快炒"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "手撕后洗净沥干",
        "items": [
          {
            "name": "包菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "番茄炒蛋",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 70,
    "main_ingredients": [
      {
        "name": "番茄",
        "amount": "3个"
      },
      {
        "name": "鸡蛋",
        "amount": "3个"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "1根"
      },
      {
        "name": "蒜",
        "amount": "2瓣"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "白糖",
        "amount": "半勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "番茄切块鸡蛋打散加少许盐",
        "step": 1
      },
      {
        "name": "油热下蛋液炒凝固盛出",
        "step": 2
      },
      {
        "name": "下番茄炒至出汁",
        "step": 3
      },
      {
        "name": "倒回鸡蛋加糖盐翻炒",
        "step": 4
      },
      {
        "name": "撒葱花",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "鸡蛋先盛出来才不会炒老"
      },
      {
        "name": "加一点点糖提鲜"
      },
      {
        "name": "番茄要炒出汁才好吃"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "番茄"
          },
          {
            "name": "葱"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "番茄",
            "shape": "块"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "蒜蓉西兰花",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "西兰花",
        "amount": "1颗"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      }
    ],
    "side_ingredients": [],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "蚝油",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "西兰花掰小朵盐水泡10分钟",
        "step": 1
      },
      {
        "name": "水开加盐油焯西兰花1分钟",
        "step": 2
      },
      {
        "name": "蒜切末",
        "step": 3
      },
      {
        "name": "油热下蒜末炒香",
        "step": 4
      },
      {
        "name": "下西兰花加蚝油盐翻炒",
        "step": 5
      },
      {
        "name": "水淀粉勾薄芡出锅",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "焯水时加油和盐保持翠绿"
      },
      {
        "name": "蒜末要多才香"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "盐水浸泡",
        "items": [
          {
            "name": "西兰花"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "洗",
        "note": "泡后冲洗",
        "items": [
          {
            "name": "西兰花"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "西兰花",
            "shape": "小朵"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "蚝油生菜",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 5,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "生菜",
        "amount": "1颗"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "5瓣"
      }
    ],
    "seasonings": [
      {
        "name": "蚝油",
        "amount": "2勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "生菜掰开洗净",
        "step": 1
      },
      {
        "name": "水开加盐油焯生菜30秒捞出摆盘",
        "step": 2
      },
      {
        "name": "蒜末爆香加蚝油生抽水淀粉煮至浓稠",
        "step": 3
      },
      {
        "name": "淋在生菜上",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "生菜焯水时间一定要短"
      },
      {
        "name": "水开后再放菜"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "逐片洗净",
        "items": [
          {
            "name": "生菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "地三鲜",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 20,
    "difficulty": "中等",
    "health_score": 55,
    "main_ingredients": [
      {
        "name": "土豆",
        "amount": "2个"
      },
      {
        "name": "茄子",
        "amount": "1个"
      },
      {
        "name": "青椒",
        "amount": "2个"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "葱",
        "amount": "1根"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "糖",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "土豆茄子青椒切滚刀块",
        "step": 1
      },
      {
        "name": "土豆和茄子分别过油至金黄",
        "step": 2
      },
      {
        "name": "调碗汁:生抽老抽糖盐淀粉水",
        "step": 3
      },
      {
        "name": "留底油爆香葱蒜",
        "step": 4
      },
      {
        "name": "下所有食材加碗汁翻炒",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "过油比直接炒好吃很多"
      },
      {
        "name": "茄子吸油可以撒盐腌一下挤水"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "土豆"
          },
          {
            "name": "茄子"
          },
          {
            "name": "青椒"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "土豆",
            "shape": "滚刀块"
          },
          {
            "name": "茄子",
            "shape": "滚刀块"
          },
          {
            "name": "青椒",
            "shape": "块"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "葱",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "干煸四季豆",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 15,
    "difficulty": "中等",
    "health_score": 55,
    "main_ingredients": [
      {
        "name": "四季豆",
        "amount": "400g"
      }
    ],
    "side_ingredients": [
      {
        "name": "干辣椒",
        "amount": "8个"
      },
      {
        "name": "花椒",
        "amount": "1把"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "芽菜",
        "amount": "30g"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "四季豆去筋掰段洗净",
        "step": 1
      },
      {
        "name": "六成油温下四季豆炸至起皱",
        "step": 2
      },
      {
        "name": "留底油下干辣椒花椒蒜末芽菜炒香",
        "step": 3
      },
      {
        "name": "下四季豆加生抽盐炒匀",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "四季豆一定要熟透"
      },
      {
        "name": "芽菜是点睛之笔"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "去筋洗净沥干",
        "items": [
          {
            "name": "四季豆"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "家常豆腐",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 15,
    "difficulty": "简单",
    "health_score": 65,
    "main_ingredients": [
      {
        "name": "老豆腐",
        "amount": "1块"
      },
      {
        "name": "猪肉末",
        "amount": "50g"
      }
    ],
    "side_ingredients": [
      {
        "name": "青椒",
        "amount": "1个"
      },
      {
        "name": "红椒",
        "amount": "1个"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "姜",
        "amount": "2片"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "蚝油",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "豆腐切三角片油煎至两面金黄",
        "step": 1
      },
      {
        "name": "肉末炒变色加姜蒜炒香",
        "step": 2
      },
      {
        "name": "下青红椒翻炒",
        "step": 3
      },
      {
        "name": "下豆腐加生抽蚝油少许水烧2分钟",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "豆腐要煎到位才香"
      },
      {
        "name": "老豆腐煎的时候不容易碎"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "青椒"
          },
          {
            "name": "红椒"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "老豆腐",
            "shape": "三角厚片"
          },
          {
            "name": "青椒",
            "shape": "块"
          },
          {
            "name": "红椒",
            "shape": "块"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "姜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "麻婆豆腐",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 15,
    "difficulty": "中等",
    "health_score": 60,
    "main_ingredients": [
      {
        "name": "嫩豆腐",
        "amount": "1块"
      },
      {
        "name": "猪肉末",
        "amount": "100g"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "葱",
        "amount": "2根"
      }
    ],
    "seasonings": [
      {
        "name": "郫县豆瓣酱",
        "amount": "2勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "花椒粉",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "豆腐切2cm方块盐水焯1分钟",
        "step": 1
      },
      {
        "name": "肉末炒酥加豆瓣酱炒出红油",
        "step": 2
      },
      {
        "name": "加姜蒜末炒香",
        "step": 3
      },
      {
        "name": "加水和豆腐轻轻推匀烧3分钟",
        "step": 4
      },
      {
        "name": "淀粉水分两次淋入勾芡",
        "step": 5
      },
      {
        "name": "撒花椒粉葱花出锅",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "豆腐焯水更嫩不易碎"
      },
      {
        "name": "勾芡分两次更易挂住"
      },
      {
        "name": "花椒粉是灵魂"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "嫩豆腐"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "嫩豆腐",
            "shape": "2cm方块"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "姜",
            "shape": "末"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "红烧茄子",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 15,
    "difficulty": "中等",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "茄子",
        "amount": "2个"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "葱",
        "amount": "1根"
      },
      {
        "name": "青椒",
        "amount": "1个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "糖",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "茄子切滚刀块撒盐腌10分钟挤水",
        "step": 1
      },
      {
        "name": "茄子裹少许淀粉",
        "step": 2
      },
      {
        "name": "调碗汁:生抽老抽糖盐淀粉水",
        "step": 3
      },
      {
        "name": "油热下茄子煎至金黄",
        "step": 4
      },
      {
        "name": "下蒜末炒香加入碗汁",
        "step": 5
      },
      {
        "name": "加青椒翻炒收汁",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "茄子撒盐腌挤水少吸油"
      },
      {
        "name": "茄子皮有营养不要削"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "撒盐腌后挤水",
        "items": [
          {
            "name": "茄子",
            "amount": "2个"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "青椒"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "茄子",
            "shape": "滚刀块"
          },
          {
            "name": "青椒",
            "shape": "块"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "素炒空心菜",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 5,
    "end_month": 9,
    "cooking_time": 5,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "空心菜",
        "amount": "1把"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "5瓣"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "空心菜洗净摘段",
        "step": 1
      },
      {
        "name": "油热下蒜末爆香",
        "step": 2
      },
      {
        "name": "大火下空心菜快炒1分钟",
        "step": 3
      },
      {
        "name": "加盐出锅",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "大火快炒口感脆嫩"
      },
      {
        "name": "不要盖锅盖会变黄"
      },
      {
        "name": "杆先下锅叶后下"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "摘去老茎洗净",
        "items": [
          {
            "name": "空心菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "炝炒白菜",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 75,
    "main_ingredients": [
      {
        "name": "大白菜",
        "amount": "半颗"
      }
    ],
    "side_ingredients": [
      {
        "name": "干辣椒",
        "amount": "5个"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      }
    ],
    "seasonings": [
      {
        "name": "醋",
        "amount": "1勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "白菜帮和叶分开帮斜刀切片",
        "step": 1
      },
      {
        "name": "油热下干辣椒蒜片爆香",
        "step": 2
      },
      {
        "name": "先下白菜帮炒1分钟",
        "step": 3
      },
      {
        "name": "下白菜叶炒软",
        "step": 4
      },
      {
        "name": "加生抽盐醋翻匀",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "帮和叶分开炒口感更好"
      },
      {
        "name": "大火爆炒才香"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "洗净沥干",
        "items": [
          {
            "name": "大白菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "大白菜",
            "shape": "帮切片叶撕块"
          },
          {
            "name": "蒜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "醋溜白菜",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 75,
    "main_ingredients": [
      {
        "name": "大白菜",
        "amount": "半颗"
      }
    ],
    "side_ingredients": [
      {
        "name": "干辣椒",
        "amount": "5个"
      },
      {
        "name": "花椒",
        "amount": "10粒"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      }
    ],
    "seasonings": [
      {
        "name": "醋",
        "amount": "3勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "糖",
        "amount": "半勺"
      },
      {
        "name": "淀粉",
        "amount": "半勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "调碗汁:醋生抽糖盐淀粉",
        "step": 1
      },
      {
        "name": "油热下花椒干辣椒蒜片爆香",
        "step": 2
      },
      {
        "name": "下白菜大火翻炒至软",
        "step": 3
      },
      {
        "name": "淋碗汁快速翻匀",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "醋的量要大"
      },
      {
        "name": "碗汁提前调好才快手"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "洗净沥干",
        "items": [
          {
            "name": "大白菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "大白菜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "清炒豆苗",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 5,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "豆苗",
        "amount": "300g"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "3瓣"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "豆苗洗净",
        "step": 1
      },
      {
        "name": "油热下蒜末爆香",
        "step": 2
      },
      {
        "name": "下豆苗大火快炒30秒",
        "step": 3
      },
      {
        "name": "加盐出锅",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "速度要快炒久了出水"
      },
      {
        "name": "豆苗很嫩不用炒太久"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "洗净沥干",
        "items": [
          {
            "name": "豆苗"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "鱼香茄子",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 20,
    "difficulty": "中等",
    "health_score": 50,
    "main_ingredients": [
      {
        "name": "茄子",
        "amount": "2个"
      },
      {
        "name": "猪肉末",
        "amount": "100g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "郫县豆瓣酱",
        "amount": "1勺"
      },
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "醋",
        "amount": "2勺"
      },
      {
        "name": "白糖",
        "amount": "2勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "茄子切条撒盐腌挤水",
        "step": 1
      },
      {
        "name": "调鱼香汁:生抽醋糖淀粉水",
        "step": 2
      },
      {
        "name": "油热下茄子煎至金黄盛出",
        "step": 3
      },
      {
        "name": "下肉末炒酥加豆瓣酱炒出红油",
        "step": 4
      },
      {
        "name": "加姜蒜末炒香",
        "step": 5
      },
      {
        "name": "下茄子加鱼香汁翻匀撒葱花",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "鱼香味型糖醋比例1:1"
      },
      {
        "name": "茄子先腌后煎少吸油"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "撒盐腌挤水",
        "items": [
          {
            "name": "茄子",
            "amount": "2个"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "茄子",
            "shape": "条"
          },
          {
            "name": "姜",
            "shape": "末"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "蚂蚁上树",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 40,
    "main_ingredients": [
      {
        "name": "粉丝",
        "amount": "2把"
      },
      {
        "name": "猪肉末",
        "amount": "100g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "郫县豆瓣酱",
        "amount": "1勺"
      },
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "粉丝温水泡软剪短",
        "step": 1
      },
      {
        "name": "肉末炒酥加豆瓣酱炒出红油",
        "step": 2
      },
      {
        "name": "加姜蒜末干辣椒炒香",
        "step": 3
      },
      {
        "name": "加少许水生抽老抽料酒",
        "step": 4
      },
      {
        "name": "下粉丝用筷子拨散吸收汤汁",
        "step": 5
      },
      {
        "name": "撒葱花出锅",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "粉丝不要泡太软"
      },
      {
        "name": "水不要太多否则成汤"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "温水泡软",
        "items": [
          {
            "name": "粉丝",
            "amount": "2把"
          }
        ],
        "time_minutes": 15
      },
      {
        "act": "切",
        "items": [
          {
            "name": "姜",
            "shape": "末"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "宫保豆腐",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 15,
    "difficulty": "中等",
    "health_score": 60,
    "main_ingredients": [
      {
        "name": "老豆腐",
        "amount": "1块"
      },
      {
        "name": "花生米",
        "amount": "50g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "干辣椒",
        "amount": "8个"
      },
      {
        "name": "花椒",
        "amount": "1把"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "醋",
        "amount": "2勺"
      },
      {
        "name": "白糖",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "豆腐切丁焯水",
        "step": 1
      },
      {
        "name": "调宫保汁:生抽醋糖淀粉水",
        "step": 2
      },
      {
        "name": "油煎豆腐至金黄盛出",
        "step": 3
      },
      {
        "name": "小火炒香花椒干辣椒姜蒜",
        "step": 4
      },
      {
        "name": "下豆腐和葱段翻炒",
        "step": 5
      },
      {
        "name": "淋宫保汁翻匀撒花生米",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "宫保味型糖醋花椒干辣椒缺一不可"
      },
      {
        "name": "花生米要最后放"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "葱"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "老豆腐",
            "shape": "2cm丁"
          },
          {
            "name": "葱",
            "shape": "小段"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "韭菜炒鸡蛋",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 70,
    "main_ingredients": [
      {
        "name": "韭菜",
        "amount": "200g"
      },
      {
        "name": "鸡蛋",
        "amount": "3个"
      }
    ],
    "side_ingredients": [],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "韭菜洗净切段",
        "step": 1
      },
      {
        "name": "鸡蛋打散加少许盐",
        "step": 2
      },
      {
        "name": "油热炒鸡蛋凝固盛出",
        "step": 3
      },
      {
        "name": "大火下韭菜快炒30秒",
        "step": 4
      },
      {
        "name": "倒回鸡蛋翻匀加盐",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "韭菜不能炒太久"
      },
      {
        "name": "鸡蛋先盛出才不会老"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "逐根洗净",
        "items": [
          {
            "name": "韭菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "韭菜",
            "shape": "3cm段"
          }
        ]
      }
    ]
  },
  {
    "name": "蒜苗炒肉",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 65,
    "main_ingredients": [
      {
        "name": "蒜苗",
        "amount": "300g"
      },
      {
        "name": "五花肉",
        "amount": "150g"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "2片"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "五花肉切薄片",
        "step": 1
      },
      {
        "name": "蒜苗斜刀切段白绿分开",
        "step": 2
      },
      {
        "name": "锅不放油煸五花肉出油",
        "step": 3
      },
      {
        "name": "加姜干辣椒炒香",
        "step": 4
      },
      {
        "name": "下蒜苗白翻炒",
        "step": 5
      },
      {
        "name": "下蒜苗叶加生抽老抽盐",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "五花肉煸出油才香"
      },
      {
        "name": "蒜苗白和绿分开炒"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "逐根洗净",
        "items": [
          {
            "name": "蒜苗"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "五花肉",
            "shape": "薄片"
          },
          {
            "name": "蒜苗",
            "shape": "斜刀段白绿分开"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "西葫芦炒鸡蛋",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 70,
    "main_ingredients": [
      {
        "name": "西葫芦",
        "amount": "1个"
      },
      {
        "name": "鸡蛋",
        "amount": "3个"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "2瓣"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "西葫芦切片鸡蛋打散",
        "step": 1
      },
      {
        "name": "鸡蛋炒熟盛出",
        "step": 2
      },
      {
        "name": "下蒜末炒香",
        "step": 3
      },
      {
        "name": "下西葫芦翻炒至软",
        "step": 4
      },
      {
        "name": "倒回鸡蛋加盐",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "西葫芦不要切太薄"
      },
      {
        "name": "炒到刚刚断生最好"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "西葫芦"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "西葫芦",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "芹菜香干",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 65,
    "main_ingredients": [
      {
        "name": "芹菜",
        "amount": "200g"
      },
      {
        "name": "香干",
        "amount": "4块"
      },
      {
        "name": "猪肉末",
        "amount": "50g"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "2瓣"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "芹菜去叶切段香干切片",
        "step": 1
      },
      {
        "name": "香干焯水30秒",
        "step": 2
      },
      {
        "name": "肉末炒香",
        "step": 3
      },
      {
        "name": "下蒜干辣椒炒香",
        "step": 4
      },
      {
        "name": "下香干翻炒",
        "step": 5
      },
      {
        "name": "下芹菜加生抽盐大火翻炒1分钟",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "芹菜最后放保持脆感"
      },
      {
        "name": "香干焯水去豆腥味"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "去叶洗净",
        "items": [
          {
            "name": "芹菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "芹菜",
            "shape": "段"
          },
          {
            "name": "香干",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "丝瓜炒蛋",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 70,
    "main_ingredients": [
      {
        "name": "丝瓜",
        "amount": "2根"
      },
      {
        "name": "鸡蛋",
        "amount": "3个"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "2瓣"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "丝瓜去皮切滚刀块",
        "step": 1
      },
      {
        "name": "鸡蛋打散炒熟盛出",
        "step": 2
      },
      {
        "name": "蒜末爆香下丝瓜翻炒",
        "step": 3
      },
      {
        "name": "加少许水焖2分钟至软",
        "step": 4
      },
      {
        "name": "倒回鸡蛋加盐",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "丝瓜不要用铁锅炒会变黑"
      },
      {
        "name": "加少许水焖一下更软嫩"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "丝瓜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "丝瓜",
            "shape": "滚刀块"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "红烧豆腐",
    "dtype": "半素",
    "ftype": "草",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 12,
    "difficulty": "简单",
    "health_score": 65,
    "main_ingredients": [
      {
        "name": "老豆腐",
        "amount": "1块"
      },
      {
        "name": "猪肉末",
        "amount": "50g"
      }
    ],
    "side_ingredients": [
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "2片"
      },
      {
        "name": "蒜",
        "amount": "2瓣"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "老抽",
        "amount": "半勺"
      },
      {
        "name": "蚝油",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "豆腐切块焯水",
        "step": 1
      },
      {
        "name": "肉末炒香加姜蒜",
        "step": 2
      },
      {
        "name": "加水和生抽老抽蚝油",
        "step": 3
      },
      {
        "name": "下豆腐烧5分钟",
        "step": 4
      },
      {
        "name": "水淀粉勾芡撒葱花",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "老豆腐烧久一点更入味"
      },
      {
        "name": "翻动要轻防止豆腐碎"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "葱"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "老豆腐",
            "shape": "3cm方块"
          },
          {
            "name": "葱",
            "shape": "葱花"
          },
          {
            "name": "姜",
            "shape": "末"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "苦瓜炒蛋",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "苦瓜",
        "amount": "1根"
      },
      {
        "name": "鸡蛋",
        "amount": "3个"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "2瓣"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "苦瓜对半切开去瓤切薄片",
        "step": 1
      },
      {
        "name": "苦瓜加盐腌10分钟挤去苦水",
        "step": 2
      },
      {
        "name": "鸡蛋打散炒熟盛出",
        "step": 3
      },
      {
        "name": "蒜末爆香下苦瓜翻炒",
        "step": 4
      },
      {
        "name": "倒回鸡蛋加盐翻匀",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "加盐腌挤水可以去掉大部分苦味"
      },
      {
        "name": "切得越薄越不苦"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "加盐腌后挤去苦水",
        "items": [
          {
            "name": "苦瓜",
            "amount": "1根"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "苦瓜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "苦瓜",
            "shape": "薄片"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "苦瓜炒肉",
    "dtype": "硬菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 12,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "苦瓜",
        "amount": "1根"
      },
      {
        "name": "猪肉",
        "amount": "150g"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "豆豉",
        "amount": "1勺"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "猪肉切片加料酒淀粉生抽腌10分钟",
        "step": 1
      },
      {
        "name": "苦瓜去瓤切片，加盐腌后挤水",
        "step": 2
      },
      {
        "name": "油热下肉片滑炒变色盛出",
        "step": 3
      },
      {
        "name": "下蒜豆豉干辣椒爆香",
        "step": 4
      },
      {
        "name": "下苦瓜翻炒1分钟",
        "step": 5
      },
      {
        "name": "倒回肉片加盐翻匀",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "苦瓜腌过挤水后苦味大减"
      },
      {
        "name": "豆豉是点睛之笔"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "加盐腌挤水",
        "items": [
          {
            "name": "苦瓜",
            "amount": "1根"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "腌",
        "note": "料酒生抽淀粉",
        "items": [
          {
            "name": "猪肉",
            "amount": "150g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "猪肉",
            "shape": "片"
          },
          {
            "name": "苦瓜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "冬瓜肉丸汤",
    "dtype": "肉汤",
    "ftype": "跑",
    "start_month": 7,
    "end_month": 9,
    "cooking_time": 40,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "猪肉末",
        "amount": "300g"
      },
      {
        "name": "冬瓜",
        "amount": "500g"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "鸡蛋",
        "amount": "1个"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "白胡椒粉",
        "amount": "少许"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "肉末加蛋清料酒淀粉盐胡椒粉搅上劲",
        "step": 1
      },
      {
        "name": "冬瓜去皮切块",
        "step": 2
      },
      {
        "name": "水开下姜片和冬瓜煮5分钟",
        "step": 3
      },
      {
        "name": "转小火挤肉丸下锅",
        "step": 4
      },
      {
        "name": "煮至肉丸浮起加盐香油",
        "step": 5
      },
      {
        "name": "撒葱花出锅",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "肉馅要一个方向搅上劲才Q弹"
      },
      {
        "name": "小火下丸子不会散"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "冬瓜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "冬瓜",
            "shape": "块"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "黄瓜炒肉",
    "dtype": "硬菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "黄瓜",
        "amount": "2根"
      },
      {
        "name": "猪肉",
        "amount": "150g"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "干辣椒",
        "amount": "3个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "猪肉切片加料酒淀粉生抽腌10分钟",
        "step": 1
      },
      {
        "name": "黄瓜切片",
        "step": 2
      },
      {
        "name": "油热下肉片滑炒变色盛出",
        "step": 3
      },
      {
        "name": "下蒜干辣椒爆香",
        "step": 4
      },
      {
        "name": "下黄瓜大火快炒30秒",
        "step": 5
      },
      {
        "name": "倒回肉片加盐翻匀",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "黄瓜不要炒太久保持脆爽"
      },
      {
        "name": "肉先腌才嫩"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒淀粉生抽",
        "items": [
          {
            "name": "猪肉",
            "amount": "150g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "黄瓜",
            "shape": "片"
          },
          {
            "name": "猪肉",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "凉拌黄瓜",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 5,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "黄瓜",
        "amount": "2根"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "小米辣",
        "amount": "3个"
      },
      {
        "name": "香菜",
        "amount": "2根"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "醋",
        "amount": "2勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "糖",
        "amount": "半勺"
      },
      {
        "name": "香油",
        "amount": "1勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "黄瓜拍碎切段",
        "step": 1
      },
      {
        "name": "蒜切末小米辣切圈",
        "step": 2
      },
      {
        "name": "生抽醋盐糖香油调成汁",
        "step": 3
      },
      {
        "name": "所有材料拌匀",
        "step": 4
      },
      {
        "name": "撒香菜上桌",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "黄瓜用刀拍比切更入味"
      },
      {
        "name": "现拌现吃，不要提前拌"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "黄瓜"
          },
          {
            "name": "香菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "黄瓜",
            "shape": "拍碎切段"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "小米辣",
            "shape": "圈"
          }
        ]
      }
    ]
  },
  {
    "name": "绿豆汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 40,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "绿豆",
        "amount": "200g"
      },
      {
        "name": "冰糖",
        "amount": "50g"
      }
    ],
    "side_ingredients": [],
    "seasonings": [],
    "cooking_steps": [
      {
        "name": "绿豆洗净泡1小时",
        "step": 1
      },
      {
        "name": "绿豆冷水下锅大火煮开",
        "step": 2
      },
      {
        "name": "转小火煮30分钟至开花",
        "step": 3
      },
      {
        "name": "加冰糖搅匀放凉",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "提前泡发更容易煮开花"
      },
      {
        "name": "冷藏后更好喝"
      },
      {
        "name": "体质虚寒少喝"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "冷水泡1小时",
        "items": [
          {
            "name": "绿豆",
            "amount": "200g"
          }
        ],
        "time_minutes": 60
      },
      {
        "act": "洗",
        "note": "洗净沥干",
        "items": [
          {
            "name": "绿豆"
          }
        ]
      }
    ]
  },
  {
    "name": "莲子百合汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 30,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "莲子",
        "amount": "50g"
      },
      {
        "name": "百合",
        "amount": "30g"
      },
      {
        "name": "银耳",
        "amount": "1朵"
      },
      {
        "name": "冰糖",
        "amount": "30g"
      }
    ],
    "side_ingredients": [
      {
        "name": "枸杞",
        "amount": "10粒"
      }
    ],
    "seasonings": [],
    "cooking_steps": [
      {
        "name": "银耳泡发撕小朵，莲子去芯泡1小时",
        "step": 1
      },
      {
        "name": "银耳加足水大火煮开转小火炖20分钟",
        "step": 2
      },
      {
        "name": "加莲子百合继续炖15分钟",
        "step": 3
      },
      {
        "name": "加冰糖枸杞搅匀",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "银耳要泡发充分才出胶"
      },
      {
        "name": "莲子去芯否则会苦"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "银耳泡发撕小朵，莲子去芯泡1小时",
        "items": [
          {
            "name": "银耳",
            "amount": "1朵"
          },
          {
            "name": "莲子",
            "amount": "50g"
          }
        ],
        "time_minutes": 60
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "百合"
          }
        ]
      }
    ]
  },
  {
    "name": "黄瓜皮蛋汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "黄瓜",
        "amount": "1根"
      },
      {
        "name": "皮蛋",
        "amount": "2个"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "葱",
        "amount": "1根"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "黄瓜切片皮蛋切块",
        "step": 1
      },
      {
        "name": "油热下姜片皮蛋煎一下",
        "step": 2
      },
      {
        "name": "加开水煮2分钟至汤变白",
        "step": 3
      },
      {
        "name": "下黄瓜片煮30秒",
        "step": 4
      },
      {
        "name": "加盐香油撒葱花",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "皮蛋先煎一下汤才白"
      },
      {
        "name": "黄瓜最后放保持清香"
      }
    ],
    "prep_steps": [
      {
        "act": "切",
        "items": [
          {
            "name": "黄瓜",
            "shape": "片"
          },
          {
            "name": "皮蛋",
            "shape": "块"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "冬瓜海带汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 7,
    "end_month": 9,
    "cooking_time": 20,
    "difficulty": "简单",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "冬瓜",
        "amount": "500g"
      },
      {
        "name": "海带",
        "amount": "100g"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "虾皮",
        "amount": "1把"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "海带泡发洗净切片",
        "step": 1
      },
      {
        "name": "冬瓜去皮切块",
        "step": 2
      },
      {
        "name": "水开下姜片海带煮10分钟",
        "step": 3
      },
      {
        "name": "下冬瓜再煮5分钟",
        "step": 4
      },
      {
        "name": "加盐虾皮香油",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "海带要泡发完全"
      },
      {
        "name": "虾皮提鲜不用加味精"
      }
    ],
    "prep_steps": [
      {
        "act": "泡",
        "note": "泡发洗净",
        "items": [
          {
            "name": "海带",
            "amount": "100g"
          }
        ],
        "time_minutes": 30
      },
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "冬瓜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "海带",
            "shape": "片"
          },
          {
            "name": "冬瓜",
            "shape": "块"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "蒜泥白肉",
    "dtype": "硬菜",
    "ftype": "跑",
    "start_month": 1,
    "end_month": 12,
    "cooking_time": 25,
    "difficulty": "中等",
    "health_score": 80,
    "main_ingredients": [
      {
        "name": "五花肉",
        "amount": "400g"
      },
      {
        "name": "黄瓜",
        "amount": "1根"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "1整头"
      },
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "姜",
        "amount": "5片"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "醋",
        "amount": "1勺"
      },
      {
        "name": "辣椒油",
        "amount": "2勺"
      },
      {
        "name": "白糖",
        "amount": "半勺"
      },
      {
        "name": "花椒粉",
        "amount": "少许"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "五花肉冷水下锅加姜料酒煮20分钟",
        "step": 1
      },
      {
        "name": "捞出放凉切薄片",
        "step": 2
      },
      {
        "name": "黄瓜切丝铺盘底",
        "step": 3
      },
      {
        "name": "肉片码在黄瓜上",
        "step": 4
      },
      {
        "name": "蒜剁成泥加生抽醋辣椒油糖花椒粉调汁",
        "step": 5
      },
      {
        "name": "淋在肉上撒葱花",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "蒜泥是灵魂一定要多"
      },
      {
        "name": "肉要放凉再切才薄而不散"
      },
      {
        "name": "夏天吃非常爽口"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "五花肉整块洗",
        "items": [
          {
            "name": "五花肉"
          },
          {
            "name": "黄瓜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "五花肉",
            "shape": "薄片"
          },
          {
            "name": "黄瓜",
            "shape": "丝"
          },
          {
            "name": "蒜",
            "shape": "泥"
          },
          {
            "name": "葱",
            "shape": "葱花"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "丝瓜炒肉",
    "dtype": "硬菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 78,
    "main_ingredients": [
      {
        "name": "丝瓜",
        "amount": "2根"
      },
      {
        "name": "猪肉",
        "amount": "150g"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "姜",
        "amount": "2片"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "1勺"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "猪肉切片加料酒淀粉生抽腌10分钟",
        "step": 1
      },
      {
        "name": "丝瓜去皮切滚刀块",
        "step": 2
      },
      {
        "name": "油热下肉片滑炒变色盛出",
        "step": 3
      },
      {
        "name": "下姜蒜爆香",
        "step": 4
      },
      {
        "name": "下丝瓜翻炒加少许水焖2分钟",
        "step": 5
      },
      {
        "name": "倒回肉片加盐翻匀",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "丝瓜出水后自然有汤汁很鲜"
      },
      {
        "name": "铁锅会变黑用不粘锅"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒淀粉生抽",
        "items": [
          {
            "name": "猪肉",
            "amount": "150g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "丝瓜",
            "shape": "滚刀块"
          },
          {
            "name": "猪肉",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "丝瓜豆腐汤",
    "dtype": "素汤",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 10,
    "difficulty": "简单",
    "health_score": 92,
    "main_ingredients": [
      {
        "name": "丝瓜",
        "amount": "1根"
      },
      {
        "name": "嫩豆腐",
        "amount": "1块"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "2片"
      },
      {
        "name": "虾皮",
        "amount": "1把"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "丝瓜去皮切块豆腐切块",
        "step": 1
      },
      {
        "name": "油热下姜片丝瓜略炒",
        "step": 2
      },
      {
        "name": "加开水下豆腐煮3分钟",
        "step": 3
      },
      {
        "name": "加虾皮盐香油",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "丝瓜先炒一下汤更鲜"
      },
      {
        "name": "虾皮代替味精"
      }
    ],
    "prep_steps": [
      {
        "act": "切",
        "items": [
          {
            "name": "丝瓜",
            "shape": "块"
          },
          {
            "name": "嫩豆腐",
            "shape": "块"
          },
          {
            "name": "姜",
            "shape": "片"
          }
        ]
      }
    ]
  },
  {
    "name": "莲藕排骨汤",
    "dtype": "肉汤",
    "ftype": "跑",
    "start_month": 9,
    "end_month": 2,
    "cooking_time": 100,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "排骨",
        "amount": "500g"
      },
      {
        "name": "莲藕",
        "amount": "2节"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "5片"
      },
      {
        "name": "葱",
        "amount": "2根"
      },
      {
        "name": "枸杞",
        "amount": "10粒"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "料酒",
        "amount": "2勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "排骨冷水焯水",
        "step": 1
      },
      {
        "name": "莲藕去皮切滚刀块",
        "step": 2
      },
      {
        "name": "排骨姜片入锅加水大火烧开",
        "step": 3
      },
      {
        "name": "转小火煲1小时",
        "step": 4
      },
      {
        "name": "下莲藕再煲30分钟",
        "step": 5
      },
      {
        "name": "加盐撒枸杞葱花",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "藕选粉藕炖汤才粉糯"
      },
      {
        "name": "藕不要切太早会氧化变黑"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "排骨浸泡去血水",
        "items": [
          {
            "name": "排骨"
          },
          {
            "name": "莲藕"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "排骨",
            "shape": "段"
          },
          {
            "name": "莲藕",
            "shape": "滚刀块"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "清炒藕片",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 9,
    "end_month": 2,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 88,
    "main_ingredients": [
      {
        "name": "莲藕",
        "amount": "2节"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "3瓣"
      },
      {
        "name": "葱",
        "amount": "1根"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "白醋",
        "amount": "半勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "莲藕去皮切薄片泡水防氧化",
        "step": 1
      },
      {
        "name": "水开加白醋焯藕片30秒",
        "step": 2
      },
      {
        "name": "油热下蒜末爆香",
        "step": 3
      },
      {
        "name": "下藕片大火快炒1分钟",
        "step": 4
      },
      {
        "name": "加盐翻匀撒葱花",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "泡水和加醋保持藕片洁白"
      },
      {
        "name": "炒的时间要短保持脆爽"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "",
        "items": [
          {
            "name": "莲藕"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "莲藕",
            "shape": "薄片"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "凉拌藕片",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 10,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 90,
    "main_ingredients": [
      {
        "name": "莲藕",
        "amount": "2节"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "小米辣",
        "amount": "3个"
      },
      {
        "name": "香菜",
        "amount": "2根"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "醋",
        "amount": "2勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "糖",
        "amount": "1勺"
      },
      {
        "name": "辣椒油",
        "amount": "1勺"
      },
      {
        "name": "香油",
        "amount": "1勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "莲藕去皮切薄片",
        "step": 1
      },
      {
        "name": "水开焯藕片1分钟捞出过凉水",
        "step": 2
      },
      {
        "name": "蒜末小米辣圈加生抽醋盐糖辣椒油香油调汁",
        "step": 3
      },
      {
        "name": "藕片和酱汁拌匀",
        "step": 4
      },
      {
        "name": "撒香菜上桌",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "焯水后过凉水更脆"
      },
      {
        "name": "现拌现吃"
      }
    ],
    "prep_steps": [
      {
        "act": "切",
        "items": [
          {
            "name": "莲藕",
            "shape": "薄片"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "小米辣",
            "shape": "圈"
          }
        ]
      }
    ]
  },
  {
    "name": "白灼秋葵",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 5,
    "difficulty": "简单",
    "health_score": 93,
    "main_ingredients": [
      {
        "name": "秋葵",
        "amount": "300g"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      }
    ],
    "side_ingredients": [
      {
        "name": "小米辣",
        "amount": "2个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "蚝油",
        "amount": "1勺"
      },
      {
        "name": "糖",
        "amount": "半勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "秋葵洗净不去蒂",
        "step": 1
      },
      {
        "name": "水开加盐油焯秋葵2分钟",
        "step": 2
      },
      {
        "name": "捞出过凉水切去蒂部",
        "step": 3
      },
      {
        "name": "蒜末加生抽蚝油糖调成蘸汁",
        "step": 4
      },
      {
        "name": "摆盘上桌",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "整根焯水再切不易流失粘液"
      },
      {
        "name": "秋葵粘液是营养所在"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "用盐搓去绒毛",
        "items": [
          {
            "name": "秋葵"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "小米辣",
            "shape": "圈"
          }
        ]
      }
    ]
  },
  {
    "name": "秋葵炒蛋",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 90,
    "main_ingredients": [
      {
        "name": "秋葵",
        "amount": "200g"
      },
      {
        "name": "鸡蛋",
        "amount": "3个"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "2瓣"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      }
    ],
    "cooking_steps": [
      {
        "name": "秋葵焯水后切片",
        "step": 1
      },
      {
        "name": "鸡蛋打散加盐炒熟盛出",
        "step": 2
      },
      {
        "name": "蒜末爆香下秋葵翻炒",
        "step": 3
      },
      {
        "name": "倒回鸡蛋翻匀",
        "step": 4
      }
    ],
    "attentions": [
      {
        "name": "秋葵先焯水再切粘液不会流失"
      },
      {
        "name": "大火快炒"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "搓去绒毛",
        "items": [
          {
            "name": "秋葵"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "秋葵",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "蒜蓉秋葵",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 8,
    "difficulty": "简单",
    "health_score": 92,
    "main_ingredients": [
      {
        "name": "秋葵",
        "amount": "300g"
      },
      {
        "name": "蒜",
        "amount": "1整头"
      }
    ],
    "side_ingredients": [
      {
        "name": "红椒",
        "amount": "半个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "蚝油",
        "amount": "1勺"
      },
      {
        "name": "盐",
        "amount": "少许"
      },
      {
        "name": "淀粉",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "秋葵洗净焯水2分钟摆盘",
        "step": 1
      },
      {
        "name": "蒜剁成末红椒切粒",
        "step": 2
      },
      {
        "name": "油热下一半蒜末炸至金黄",
        "step": 3
      },
      {
        "name": "加另一半生蒜生抽蚝油盐淀粉水煮至浓稠",
        "step": 4
      },
      {
        "name": "淋在秋葵上撒红椒粒",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "金银蒜：一半炸一半生，风味层次丰富"
      },
      {
        "name": "秋葵整根焯保持营养"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "盐搓去绒毛",
        "items": [
          {
            "name": "秋葵"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "红椒",
            "shape": "粒"
          }
        ]
      }
    ]
  },
  {
    "name": "虾仁冬瓜",
    "dtype": "硬菜",
    "ftype": "游",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 12,
    "difficulty": "简单",
    "health_score": 88,
    "main_ingredients": [
      {
        "name": "冬瓜",
        "amount": "500g"
      },
      {
        "name": "虾仁",
        "amount": "200g"
      }
    ],
    "side_ingredients": [
      {
        "name": "姜",
        "amount": "3片"
      },
      {
        "name": "葱",
        "amount": "1根"
      },
      {
        "name": "蒜",
        "amount": "2瓣"
      }
    ],
    "seasonings": [
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "料酒",
        "amount": "1勺"
      },
      {
        "name": "淀粉",
        "amount": "1勺"
      },
      {
        "name": "白胡椒粉",
        "amount": "少许"
      },
      {
        "name": "香油",
        "amount": "几滴"
      }
    ],
    "cooking_steps": [
      {
        "name": "虾仁加料酒淀粉白胡椒粉腌10分钟",
        "step": 1
      },
      {
        "name": "冬瓜去皮切块",
        "step": 2
      },
      {
        "name": "油热下姜蒜爆香下虾仁滑炒变色盛出",
        "step": 3
      },
      {
        "name": "下冬瓜翻炒加少许水焖5分钟",
        "step": 4
      },
      {
        "name": "倒回虾仁加盐翻匀淋香油撒葱花",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "冬瓜焖软后自然出水"
      },
      {
        "name": "虾仁不要炒太久保持Q弹"
      }
    ],
    "prep_steps": [
      {
        "act": "腌",
        "note": "料酒淀粉白胡椒粉",
        "items": [
          {
            "name": "虾仁",
            "amount": "200g"
          }
        ],
        "time_minutes": 10
      },
      {
        "act": "切",
        "items": [
          {
            "name": "冬瓜",
            "shape": "块"
          },
          {
            "name": "姜",
            "shape": "片"
          },
          {
            "name": "蒜",
            "shape": "末"
          },
          {
            "name": "葱",
            "shape": "葱花"
          }
        ]
      }
    ]
  },
  {
    "name": "腐乳空心菜",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 5,
    "end_month": 9,
    "cooking_time": 5,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "空心菜",
        "amount": "1把"
      },
      {
        "name": "腐乳",
        "amount": "2块"
      },
      {
        "name": "蒜",
        "amount": "5瓣"
      }
    ],
    "side_ingredients": [],
    "seasonings": [
      {
        "name": "盐",
        "amount": "少许"
      }
    ],
    "cooking_steps": [
      {
        "name": "腐乳压碎加少许水调成汁",
        "step": 1
      },
      {
        "name": "蒜切末",
        "step": 2
      },
      {
        "name": "油热下蒜末爆香",
        "step": 3
      },
      {
        "name": "大火下空心菜快炒1分钟",
        "step": 4
      },
      {
        "name": "淋腐乳汁翻匀",
        "step": 5
      }
    ],
    "attentions": [
      {
        "name": "腐乳本身有咸味盐要少放"
      },
      {
        "name": "大火快炒才翠绿"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "摘去老茎洗净",
        "items": [
          {
            "name": "空心菜"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  },
  {
    "name": "凉拌毛豆",
    "dtype": "素菜",
    "ftype": "草",
    "start_month": 6,
    "end_month": 9,
    "cooking_time": 12,
    "difficulty": "简单",
    "health_score": 85,
    "main_ingredients": [
      {
        "name": "毛豆",
        "amount": "500g"
      }
    ],
    "side_ingredients": [
      {
        "name": "蒜",
        "amount": "5瓣"
      },
      {
        "name": "干辣椒",
        "amount": "5个"
      },
      {
        "name": "花椒",
        "amount": "1把"
      },
      {
        "name": "八角",
        "amount": "2个"
      }
    ],
    "seasonings": [
      {
        "name": "生抽",
        "amount": "2勺"
      },
      {
        "name": "醋",
        "amount": "2勺"
      },
      {
        "name": "盐",
        "amount": "适量"
      },
      {
        "name": "糖",
        "amount": "1勺"
      },
      {
        "name": "香油",
        "amount": "1勺"
      }
    ],
    "cooking_steps": [
      {
        "name": "毛豆剪去两端洗净",
        "step": 1
      },
      {
        "name": "水开加盐八角煮毛豆5分钟",
        "step": 2
      },
      {
        "name": "捞出过凉水",
        "step": 3
      },
      {
        "name": "油热下花椒干辣椒蒜末爆香",
        "step": 4
      },
      {
        "name": "加生抽醋糖盐香油调汁",
        "step": 5
      },
      {
        "name": "毛豆和酱汁拌匀冷藏半小时",
        "step": 6
      }
    ],
    "attentions": [
      {
        "name": "剪两端更入味"
      },
      {
        "name": "冷藏后更好吃"
      },
      {
        "name": "夏天配啤酒绝了"
      }
    ],
    "prep_steps": [
      {
        "act": "洗",
        "note": "剪去两端",
        "items": [
          {
            "name": "毛豆"
          }
        ]
      },
      {
        "act": "切",
        "items": [
          {
            "name": "蒜",
            "shape": "末"
          }
        ]
      }
    ]
  }
]''')

async def seed():
    async with AsyncSessionLocal() as db:
        await db.execute(sql_delete(DishIngredient))
        await db.execute(sql_delete(Dish.__table__))
        await db.flush()

        for d in DISHES:
            dish = Dish(
                name=d["name"],
                dtype=DtypeEnum(d["dtype"]),
                ftype=FtypeEnum(d["ftype"]),
                start_month=d["start_month"],
                end_month=d["end_month"],
                cooking_time=d["cooking_time"],
                difficulty=DifficultyEnum(d["difficulty"]),
                main_ingredients=d["main_ingredients"],
                side_ingredients=d.get("side_ingredients", []),
                seasonings=d["seasonings"],
                cooking_steps=d["cooking_steps"],
                attentions=d["attentions"],
                prep_steps=d["prep_steps"],
            )
            db.add(dish)
            await db.flush()

            for ing_list, ing_type in [
                (d["main_ingredients"], "main"),
                (d.get("side_ingredients", []), "side"),
                (d["seasonings"], "seasoning"),
            ]:
                for item in ing_list:
                    n = item.get("name", "").strip()
                    if n and n != "None":
                        db.add(DishIngredient(dish_id=dish.id, name=n, type=ing_type))
            await db.flush()
            print(f"  OK {d['dtype']:4s} | {d['name']}")

        await db.commit()
        print(f"\nDone: {len(DISHES)} dishes inserted")

if __name__ == "__main__":
    asyncio.run(seed())
