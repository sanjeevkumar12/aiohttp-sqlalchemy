from application.core.api import docs, marshal_with, use_kwargs
from application.core.views import APIResourceView
from polls.services import poll_service

from .schema import PollSchema

from aiohttp.web import Response, json_response
class PollApiView(APIResourceView):
    @docs(
        tags=["mytag"],
        summary="Test method summary",
        description="Test method description",
    )
    @marshal_with(PollSchema(many=True), 200)
    async def get(self, *args, **kwargs):
        db = self.request.config_dict["db"]
        return await poll_service.set_session(db).list_all()

    @docs(
        tags=["mytag"],
        summary="Test method summary",
        description="Test method description",
    )
    @use_kwargs(PollSchema())
    @marshal_with(PollSchema(), 200)
    async def post(self, *args, **kwargs):
        db = self.request.config_dict["db"]
        return await poll_service.set_session(db).create_poll(**self.request["data"])
