# 通知服务 — dish5
# Webhook URL 从环境变量读取，修复 dish3 硬编码问题
import logging
import json

import httpx

from ..core.config import settings
from ..models.daily_recommend import DailyRecommend

logger = logging.getLogger("dish5.notification")


async def send_notification(recommend: DailyRecommend):
    """发送每日推荐通知到企业微信"""
    webhook_url = settings.NOTIFICATION_WEBHOOK_URL

    if not webhook_url:
        logger.warning("未配置 NOTIFICATION_WEBHOOK_URL，跳过通知")
        return

    # 格式化消息
    recipes = recommend.recipes or []
    shopping = recommend.shopping_list or []

    lines = [f"🍳 今日推荐 · {recommend.date}"]
    lines.append("")
    lines.append("📋 今日菜单：")
    for i, r in enumerate(recipes):
        emoji = ["🥩", "🥬", "🥬", "🍲"][i] if i < 4 else "🍳"
        lines.append(f"  {emoji} {r.get('name', '?')}（{r.get('dtype', '')}）")

    if shopping:
        # 取前 10 个食材
        top_items = [s for s in shopping if s.get('type') in ('main', 'side')][:10]
        if top_items:
            lines.append("")
            lines.append("🛒 要买的菜：")
            for item in top_items:
                amt = f" {item.get('amount', '')}" if item.get('amount') else ""
                lines.append(f"  · {item['name']}{amt}")

    lines.append("")
    lines.append("📱 查看完整清单：https://dish5.onrender.com")

    message = {
        "msgtype": "text",
        "text": {
            "content": "\n".join(lines),
        },
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(webhook_url, json=message)
            if resp.status_code == 200:
                logger.info("通知发送成功")
                # 标记已通知
                from ..crud import crud_daily
                from ..core.database import AsyncSessionLocal
                async with AsyncSessionLocal() as db:
                    await crud_daily.mark_notified(db, recommend.id)
            else:
                logger.warning(f"通知发送失败，HTTP {resp.status_code}: {resp.text}")
    except Exception as e:
        logger.error(f"通知发送异常: {e}")
