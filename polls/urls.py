from aiohttp import web

routes = web.RouteTableDef()

polls = web.Application()
from .views import PollApiView


def init_routes(app: web.Application):
    polls.router.add_view("/", PollApiView)
    app.add_subapp("/polls", polls)
