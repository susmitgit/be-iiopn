from application.utils.helpers import transform_raw_schedule
from application.models.base_model import BaseModel


class FavouriteBusinessCollection(BaseModel):

    __collection__ = 'favourite_business'

    def __init__(self, db):
        self.db = db[self.__collection__]
        super(FavouriteBusinessCollection, self).__init__(db=self.db)

    def get_businesses_with_fav_id(self, name):
        business = self.find_one({'name': name})
        if business:
            return transform_raw_schedule(business)
        else:
            return None
