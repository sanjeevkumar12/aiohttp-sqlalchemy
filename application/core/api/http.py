import typing as t
from http import HTTPStatus


class Response(object):
    def __init__(
            self,
            response: t.Optional[
                t.Union[t.Iterable[bytes], bytes, t.Iterable[str], str]
            ] = None,
            status: t.Optional[t.Union[int, str, HTTPStatus]] = None,
            headers: t.Optional[
                t.Union[
                    t.Mapping[str, t.Union[str, int, t.Iterable[t.Union[str, int]]]],
                    t.Iterable[t.Tuple[str, t.Union[str, int]]],
                ]
            ] = None,
            mimetype: t.Optional[str] = None,
            content_type: t.Optional[str] = None,
    ):
        self.response = response
        self.status = status or 200
        self.headers = headers
        self.mimetype= mimetype
        self.content_type= content_type
