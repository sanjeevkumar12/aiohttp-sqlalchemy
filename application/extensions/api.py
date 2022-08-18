from aiohttp import web

from polls import urls


def init_api_routes(app: web.Application):
    urls.init_routes(app)


def init_services(app: web.Application):
    pass
