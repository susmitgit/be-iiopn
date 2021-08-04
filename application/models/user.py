from mongokat import Collection
from werkzeug.security import generate_password_hash, check_password_hash


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
