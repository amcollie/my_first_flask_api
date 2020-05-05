from flask_restful import Resource

from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store is not None:
            return store.json(), 200

        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name) is not None:
            return {'message': f"A store with the name '{name}' already exist."}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return "An error has occurred while creating the store", 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel(name).find_by_name(name)
        if store is not None:
            store.delete_from_db()

        return {'message': f"Store '{name}' deleted"}


class StoreList(Resource):
    def get(self):
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
        return {'stores': [store.json() for store in StoreModel.find_all()]}