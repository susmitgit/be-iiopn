from bson import ObjectId
from application.utils.helpers import transform_raw_schedule, escape_search_special_chars
from application.utils.pagination import Pagination
from application.models.base_model import BaseModel


class BusinessCollection(BaseModel):

    __collection__ = 'business'

    def __init__(self, db):
        self.db = db[self.__collection__]
        super(BusinessCollection, self).__init__(db=self.db)

    def get_business_with_business_id(self, id):
        business = self.find_one({'_id': ObjectId(id)})
        if business:
            return transform_raw_schedule(raw_schedule=business)
        else:
            return []

    def search_business(self, search_txt, page=1):
        find = {"name": {"$regex": escape_search_special_chars(search_txt), "$options": "i"}}
        paging = Pagination()
        return paging.paginated_query(query=find, page=int(page), db_instance=self.db)
