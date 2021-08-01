import datetime
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from application.utils.helpers import transform_raw_schedule

from mongokat import Collection

client = MongoClient(host=os.getenv('DATABASE_HOST', 'localhost'), port=int(os.getenv('DATABASE_PORT', '27017')),
                     connect=False)
db = client[os.getenv('DATABASE_NAME', 'test')]


class UserCollection(Collection):

    __collection__ = 'users'
    structure = {'email': str, 'password': str, 'username': str}
    protected_fields = ('password')

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)

    @staticmethod
    def hashed_password(password):
        return generate_password_hash(password)

    def get_user_with_email_and_password(self, email, password):
        user = self.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            return user
        else:
            return None


class BusinessCollection(Collection):

    __collection__ = 'business'
    structure = {'name': str, 'raw_schedule': str}

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)

    def get_business_with_name(self, name):
        business = self.find_one({'name': name})
        if business:
            return transform_raw_schedule(business)
        else:
            return None

    def get_business_with_business_id(self, id):
        business = self.find_one({'_id': ObjectId(id)})
        if business:
            return transform_raw_schedule(business)
        else:
            return None


class ScheduleCollection(Collection):

    __collection__ = 'schedule'
    structure = {'b_id': str, 'b_day': int, 'b_open': int, 'b_close': int}

    def __init__(self, db, *args, **kwargs):
        Collection.__init__(self, collection=db[self.__collection__], *args, **kwargs)

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

    def get_schedule_with_business_datetime(self, dt: datetime.datetime):
        b_day = dt.weekday()
        find_time = int(dt.hour * 60 + dt.minute)
        schedules = self.find({'b_day': b_day, 'b_open': {'$lte': find_time}, 'b_close': {'$gte': find_time}})
        if list(schedules) > 0:
            return list(schedules)
        else:
            return []


User = UserCollection(db)
Business = BusinessCollection(db)
Schedule = ScheduleCollection(db)


