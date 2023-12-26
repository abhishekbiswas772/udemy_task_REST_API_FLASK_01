from marshmallow import fields, Schema


class CarsSchema(Schema):
    id = fields.Int(dump_only = True)
    brand = fields.Str(requird = True)
    model = fields.Str(requird = True)
    transmission = fields.Str(requird = True)
    price = fields.Float(required = True)
    release_year = fields.DateTime(required=True)

