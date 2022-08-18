from typing import Callable

from aiohttp import web
from aiohttp_apispec import AiohttpApiSpec as BaseAiohttpApiSpec
from aiohttp_apispec import (docs, marshal_with, use_kwargs,
                             validation_middleware)
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin, common


def resolver(schema):
    schema_instance = common.resolve_schema_instance(schema)
    prefix = "Partial-" if schema_instance.partial else ""
    schema_cls = common.resolve_schema_cls(schema)
    name = prefix + schema_cls.__name__
    if name.endswith("Schema"):
        return name[:-6] or name
    return name


class AiohttpApiSpec(BaseAiohttpApiSpec):
    def __init__(
        self,
        url="/api/docs/swagger.json",
        app=None,
        request_data_name="data",
        swagger_path=None,
        static_path="/static/swagger",
        error_callback=None,
        in_place=False,
        prefix="",
        schema_name_resolver=resolver,
        openapi_version="3.0",
        **kwargs
    ):
        self.plugin = MarshmallowPlugin(schema_name_resolver=schema_name_resolver)
        self.spec = APISpec(
            plugins=(self.plugin,), openapi_version=openapi_version, **kwargs
        )

        self.url = url
        self.swagger_path = swagger_path
        self.static_path = static_path
        self._registered = False
        self._request_data_name = request_data_name
        self.error_callback = error_callback
        self.prefix = prefix
        self._index_page = None
        if app is not None:
            self.register(app, in_place)


def setup_aiohttp_apispec(
    app: web.Application,
    *,
    title: str = "API documentation",
    version: str = "0.0.1",
    url: str = "/api/docs/swagger.json",
    request_data_name: str = "data",
    swagger_path: str = None,
    static_path: str = "/static/swagger",
    error_callback=None,
    in_place: bool = False,
    prefix: str = "",
    schema_name_resolver: Callable = resolver,
    openapi_version="3.0.0",
    **kwargs
) -> None:
    """
    aiohttp-apispec extension.

    Usage:

    .. code-block:: python

        from aiohttp_apispec import docs, request_schema, setup_aiohttp_apispec
        from aiohttp import web
        from marshmallow import Schema, fields


        class RequestSchema(Schema):
            id = fields.Int()
            name = fields.Str(description='name')
            bool_field = fields.Bool()


        @docs(tags=['mytag'],
              summary='Test method summary',
              description='Test method description')
        @request_schema(RequestSchema)
        async def index(request):
            return web.json_response({'msg': 'done', 'data': {}})


        app = web.Application()
        app.router.add_post('/v1/test', index)

        # init docs with all parameters, usual for ApiSpec
        setup_aiohttp_apispec(app=app,
                              title='My Documentation',
                              version='v1',
                              url='/api/docs/api-docs')

        # now we can find it on 'http://localhost:8080/api/docs/api-docs'
        web.run_app(app)

    :param Application app: aiohttp web app
    :param str title: API title
    :param str version: API version
    :param str url: url for swagger spec in JSON format
    :param str request_data_name: name of the key in Request object
                                  where validated data will be placed by
                                  validation_middleware (``'data'`` by default)
    :param str swagger_path: experimental SwaggerUI support (starting from v1.1.0).
                             By default it is None (disabled)
    :param str static_path: path for static files used by SwaggerUI
                            (if it is enabled with ``swagger_path``)
    :param error_callback: custom error handler
    :param in_place: register all routes at the moment of calling this function
                     instead of the moment of the on_startup signal.
                     If True, be sure all routes are added to router
    :param prefix: prefix to add to all registered routes
    :param schema_name_resolver: custom schema_name_resolver for MarshmallowPlugin.
    :param openapi_version : open api version
    :param kwargs: any apispec.APISpec kwargs
    """
    AiohttpApiSpec(
        url,
        app,
        request_data_name,
        title=title,
        version=version,
        swagger_path=swagger_path,
        static_path=static_path,
        error_callback=error_callback,
        in_place=in_place,
        prefix=prefix,
        schema_name_resolver=schema_name_resolver,
        openapi_version=openapi_version,
        **kwargs
    )


def init_apidocs(app: web.Application):
    setup_aiohttp_apispec(
        app=app,
        title="My Documentation",
        version="v1",
        swagger_path="/docs",
        url="/api/docs/api-docs",
        openapi_version="2.0.0",
    )
    app.middlewares.append(validation_middleware)


__all__ = ["docs", "marshal_with", "use_kwargs", "init_apidocs"]
