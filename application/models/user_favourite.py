from application.utils.pagination import Pagination
from application.models.base_model import BaseModel
from application.models.favourite import FavouriteCollection
from bson import ObjectId

class UserFavouriteCollection(BaseModel):

    __collection__ = 'user_favourite'

    def __init__(self, db):
        self.db = db[self.__collection__]
        super(UserFavouriteCollection, self).__init__(db=self.db)
        self.favourite = FavouriteCollection(db=db)

    def get_favourites_with_u_id(self, u_id=None, page: int = 1):

        find_q = {'u_id': u_id}
        paging = Pagination()
        favourites = paging.paginated_query(query=find_q, page=int(page), db_instance=self.db)

        if favourites and favourites.get('data', None) and len(favourites['data']) > 0:
            try:
                for fav in favourites['data']:
                    fav['fav_name'] = self.favourite.find_one({"_id": ObjectId(fav['fav_id'])}).get('name', None)
            except:
                pass
            return favourites
        else:
            return []
