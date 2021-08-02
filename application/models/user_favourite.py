from mongokat import Collection
from application.utils.helpers import transform_raw_schedule


class UserFavouriteCollection(Collection):

    __collection__ = 'user_favourite'
    structure = {'u_id': str, 'fav_id': str}

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)

    def get_favourites_with_u_id(self, u_id=None):
        business = self.find_one({'u_id': u_id})
        if business:
            return transform_raw_schedule(business)
        else:
            return []