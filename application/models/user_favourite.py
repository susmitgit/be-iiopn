from mongokat import Collection
from application.utils.pagination import Pagination


class UserFavouriteCollection(Collection):

    __collection__ = 'user_favourite'
    structure = {'u_id': str, 'fav_id': str}

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)

    def get_favourites_with_u_id(self, u_id=None, page: int = 1):

        find_q = {'u_id': u_id}
        paging = Pagination()
        business = paging.paginated_query(query=find_q, page=int(page), db_instance=self)
        # business = list(self.find_one(find_q))
        if business:
            return business
        else:
            return []
