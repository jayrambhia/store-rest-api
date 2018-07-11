from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required = True,
        help="This field cannot be left blank")
    parser.add_argument('store_id',
        type=int,
        required = True,
        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        return {'item' : item.json()} if item else None, 200 if item else 404

    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name):
            return {'message' : "item - {} already exists".format(name)}, 400

        item = ItemModel(name, **data)
        item.save()
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
        return {'item' : item.json()} if item else None, 200 if item else 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save()
        return {'item' : item.json()}

class ItemList(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.get_all()]
        return {'items' : items}
