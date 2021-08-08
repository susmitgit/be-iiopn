from werkzeug.security import generate_password_hash, check_password_hash
from application.models.base_model import BaseModel

class UserCollection(BaseModel):

    __collection__ = 'users'

    def __init__(self, db):
        self.db = db[self.__collection__]
        super(UserCollection, self).__init__(db=self.db)

    @staticmethod
    def hashed_password(password):
        return generate_password_hash(password)

    def get_user_with_email_and_password(self, email, password):
        user = self.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            return user
        else:
            return None

