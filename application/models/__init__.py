import os
from pymongo import MongoClient
from application.models.user import UserCollection
from application.models.business import BusinessCollection
from application.models.schedule import ScheduleCollection
from application.models.favourite import FavouriteCollection
from application.models.favourite_business import FavouriteBusinessCollection
from application.models.user_favourite import UserFavouriteCollection

client = MongoClient(os.getenv('DATABASE_URI'), tlsAllowInvalidCertificates=True)
db = client[os.getenv('DATABASE_NAME', 'test')]

User = UserCollection(db)
Business = BusinessCollection(db)
Schedule = ScheduleCollection(db)
Favourite = FavouriteCollection(db)
FavouriteBusiness = FavouriteBusinessCollection(db)
UserFavourite = UserFavouriteCollection(db)
