from marshmallow import Schema, fields


class PollSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    label = fields.Str(description="name", required=True)


class RequestSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    label = fields.Str(description="name", required=True)


class ResponseSchema(Schema):
    msg = fields.Str()
    data = fields.Dict()
