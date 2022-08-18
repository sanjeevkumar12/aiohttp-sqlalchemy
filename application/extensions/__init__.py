from aiohttp import web

from application.core.api.openapi import init_apidocs

from .api import init_api_routes
from .db import init_db


def init_extensions(app: web.Application):
    init_apidocs(app)
    init_api_routes(app)
    app.cleanup_ctx.append(init_db)
