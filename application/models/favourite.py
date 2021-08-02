from mongokat import Collection
from flask import request, jsonify, g
from application.utils.helpers import transform_raw_schedule
from bson import ObjectId


class FavouriteCollection(Collection):

    __collection__ = 'favourites'
    structure = {'u_id': str, 'name': str}

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)

    def get_favourites_with_fav_id(self, name):
        business = self.find_one({'name': name})
        if business:
            return transform_raw_schedule(business)
        else:
            return None

    def get_favourites_with_user_id(self, id):
        business = self.find_one({'_id': ObjectId(id)})
        if business:
            return transform_raw_schedule(business)
        else:
            return None

    def search_favourite(self, search_txt):
        return list(self.find({"name": {"$regex": search_txt, "$options": "i"}, 'u_id': g.current_user['id']}))