from datetime import datetime
from mongokat import Collection
from application.models.business import BusinessCollection
from application.utils.helpers import exclude_mongo_id
from application.utils.pagination import Pagination

class ScheduleCollection(Collection):

    __collection__ = 'schedule'
    structure = {'b_id': str, 'b_day': int, 'b_open': int, 'b_close': int}
    business_collection = None

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)
        self.business_collection = BusinessCollection(db)

    def get_schedule_with_business_id(self, id: str):
        schedules = self.find({'b_id': id})
        if schedules:
            return list(schedules)
        else:
            return None

    def get_schedule_with_business_day(self, b_day: int):
        schedules = self.find({'b_day': id})
        if schedules:
            return list(schedules)
        else:
            return None

    def get_schedule_with_business_datetime(self, dt: datetime, page: int = 1):
        b_day = dt.weekday()
        find_time = f'{dt.hour}{dt.minute}'
        paging = Pagination()
        find_q = {'b_day': b_day, 'b_open': {'$lte': int(find_time)}, 'b_close': {'$gte': int(find_time)}}
        schedules = paging.paginated_query(query=find_q, page=page, db_instance=self)
        # schedules = list(self.find(find_q)) or []
        resp_data = []
        # Attach business with the schedule
        business_map = {}
        if schedules and len(schedules['data']) > 0:
            for sch in schedules['data']:
                b_id = sch['b_id']
                if b_id not in business_map:
                    business_map = {**business_map, **{b_id: self.business_collection.get_business_with_business_id(id=b_id)}}
                resp_data.append(exclude_mongo_id({**sch, **{**sch, **{'name': business_map[b_id]['name'], 'raw_schedule': business_map[b_id]['raw_schedule']}}}))
            if len(resp_data) > 0:
                schedules['data'] = resp_data
                return schedules
        return []
