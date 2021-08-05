import logging

from application.utils.helpers import exclude_mongo_id
from application.api_conf.api_config import ApiConfig


class Pagination:

    def __init__(self, per_page: int = ApiConfig.DEFAULT_PAGE_SIZE):
        self.per_page = per_page

    def paginated_query(self, query={}, page: int = 1, db_instance=None):
        if db_instance and page > 0:
            page = page - 1
            skip = int(page * self.per_page)
            result = db_instance.aggregate([
                {"$match": query},
                {"$facet": {
                    "data": [
                        {"$skip": skip},
                        {"$limit": self.per_page}
                    ],
                    "totalCount": [
                        {"$count": "count"}
                    ]
                }}
            ]).next()
            try:
                data = exclude_mongo_id(result['data'])
                total_count = result['totalCount'][0]['count']
                return_data = {'data': data, 'total': total_count}
                data_cursor = len(data) + skip
                if data_cursor == total_count and skip != 0:
                    return_data['prev'] = page
                elif data_cursor < total_count:
                    if skip > 0:
                        return_data['prev'] = page
                    return_data['next'] = page + 2
                return return_data
            except Exception as e:
                logging.error(f"paginated_query error {str(e)}")
        return {'data': []}
