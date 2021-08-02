from mongokat import Collection

class FavouriteBusinessCollection(Collection):

    __collection__ = 'favourites_business'
    structure = {'fav_id': str, 'b_id': str}

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)

    def get_businesses_with_fav_id(self, name):
        business = self.find_one({'name': name})
        if business:
            return transform_raw_schedule(business)
        else:
            return None
