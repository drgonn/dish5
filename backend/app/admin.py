# 管理后台 — dish5
# 基于 dish4 的 Jinja2 后台路由
# 注意: Starlette 1.0 + Jinja2 3.1.6 有兼容性问题，直接使用 jinja2.Environment
import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

admin_router = APIRouter(prefix="/admin")

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates", "admin")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR))


def _render(template_name: str, request: Request) -> HTMLResponse:
    template = _env.get_template(template_name)
    return HTMLResponse(template.render(request=request))


@admin_router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """管理仪表板"""
    return _render("index.html", request)


@admin_router.get("/dishes", response_class=HTMLResponse)
async def admin_dishes(request: Request):
    """菜品管理"""
    return _render("dishes.html", request)


@admin_router.get("/daily", response_class=HTMLResponse)
async def admin_daily(request: Request):
    """推荐管理"""
    return _render("daily.html", request)
