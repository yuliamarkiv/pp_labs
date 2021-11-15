from marshmallow import Schema, fields


class LocationSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    locationId = fields.Int()


class AdSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    text = fields.Str()
    price = fields.Float()
    currency = fields.Str()
    date = fields.Date()
    locationId = fields.Int()
    userId = fields.Int()
