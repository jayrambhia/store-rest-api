from flask_restful import Resource

from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        return {'store' : store.json()} if store else None, 200 if store else 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message' : "item - {} already exists".format(name)}, 400

        store = StoreModel(name)
        store.save()
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
        return {'message' : "deleted store {}".format(name)} if store else None, 200 if store else 404

class StoreList(Resource):
    def get(self):
        stores = [item.json() for item in StoreModel.get_all()]
        return {'stores' : stores}
