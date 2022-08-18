from aiohttp import web

from application.extensions import init_extensions


def index_handler(request):
    return web.Response(text="Hello, world")


def create_app(argv=None) -> web.Application:
    app = web.Application()
    init_extensions(app)
    app.router.add_get("/", index_handler)
    return app
