from abc import ABC
from functools import wraps

from aiohttp import web
from .api.http import Response

http_method_funcs = frozenset(
    ["get", "post", "head", "options", "delete", "put", "trace", "patch"]
)


def json_response(func):
    @wraps(func)
    async def wrapper_func(*args, **kwargs):
        _r = await func(*args, **kwargs)
        response = Response(_r)
        if getattr(func, "__apispec__"):
            api_specs = getattr(func, "__apispec__")
            api_spec_responses = api_specs.get("responses", {})
            schema = api_spec_responses.get(str(response.status), {"schema": None})
            if schema:
                response.response = schema["schema"].dump(response.response)
        return web.json_response(response.response, status=response.status)

    return wrapper_func


# class APIMeta():
#
#     def __new__(cls, *args, **kwargs):
#         x = super(APIMeta, cls).__new__(cls, *args, **kwargs)
#         for attr in x.__dict__:
#             if callable(getattr(x, attr)) and attr in http_method_funcs:
#                 setattr(x, attr, json_response(getattr(x, attr)))
#         return x
#
#
# class APIMetaClass(type(APIMeta), type(ABC)):
#     pass


class APIResourceView(web.View):
    def __init__(self, *args, **kwargs):
        super(APIResourceView, self).__init__(*args, **kwargs)
        for attr in dir(self):
            if callable(getattr(self, attr)) and attr in http_method_funcs:
                setattr(self, attr, json_response(getattr(self, attr)))
