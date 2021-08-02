from bson import ObjectId
from mongokat import Collection
from application.utils.helpers import transform_raw_schedule


class BusinessCollection(Collection):

    __collection__ = 'business'
    structure = {'name': str, 'raw_schedule': str}

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)

    def get_business_with_business_id(self, id):
        business = self.find_one({'_id': ObjectId(id)})
        if business:
            return transform_raw_schedule(raw_schedule=business)
        else:
            return []

    def search_business(self, search_txt):
        return list(self.find({"name": {"$regex": search_txt, "$options": "i"}}))