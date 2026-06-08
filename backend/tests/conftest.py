# 测试配置 — dish5
import os
import sys
import pytest
import asyncio

# 添加 app 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
