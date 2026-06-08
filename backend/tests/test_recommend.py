# 推荐算法单元测试 — dish5
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date


class TestRecommendAlgorithm:
    """推荐算法逻辑验证"""

    def test_merge_ingredients(self):
        """验证同名食材合并逻辑"""
        from services.recommend import RecommendService

        data = [
            {"name": "猪肉", "amount": "500g"},
            {"name": "猪肉", "amount": "300g"},
            {"name": "葱", "amount": "2根"},
        ]
        result = RecommendService._merge_ingredients(data)
        assert len(result) == 2
        pork = next(r for r in result if r["name"] == "猪肉")
        assert "500g" in pork["amount"]
        assert "300g" in pork["amount"]

    def test_shopping_list_generation(self):
        """验证购物清单生成"""
        from services.recommend import RecommendService

        service = RecommendService(db=None)

        # Mock dishes
        dish1 = MagicMock()
        dish1.main_ingredients = [{"name": "五花肉", "amount": "500g"}]
        dish1.side_ingredients = [{"name": "葱", "amount": "2根"}]
        dish1.seasonings = [{"name": "生抽", "amount": "2勺"}]

        dish2 = MagicMock()
        dish2.main_ingredients = []
        dish2.side_ingredients = []
        dish2.seasonings = []

        result = service._generate_shopping_list([dish1, dish2])
        assert len(result) == 3
        assert all("bought" in item and item["bought"] is False for item in result)

    def test_enums_exist(self):
        """验证枚举正确定义"""
        from models.dish import DtypeEnum, FtypeEnum, DifficultyEnum

        assert DtypeEnum.A.value == "硬菜"
        assert DtypeEnum.D.value == "素菜"
        assert FtypeEnum.A.value == "跑"
        assert DifficultyEnum.MEDIUM.value == "中等"
