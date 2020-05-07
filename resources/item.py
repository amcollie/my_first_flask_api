from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity
)

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item is not None:
            return item.json(), 200

        return {'message': 'Item not found'}, 400

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name) is not None:
            return {'message': f"An item with name'{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()      
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201
    
    @fresh_jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if item is not None:
            item.delete_from_db()
            return {"messsage": f"Item '{name}' deleted"}, 200
        
        return {'message': 'Item deleted'}, 404

    @fresh_jwt_required
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
        else:
                item.price = data['price']

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id is not None:
            return {'items': items}, 200
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {
            'items': [item['name'] for item in ItemModel.find_all()],
            'message': 'More data available if you log in'
        }, 200
