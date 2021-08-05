import cerberus
from cerberus import Validator
from bson import ObjectId


# class MongoObjectIDValidator(Validator):
#     def _check_with_mongoid(self, field, value):
#         if not ObjectId.is_valid(value):
#             self._error(field, "Must be an Mongo ID")
# class MongoObjectIDValidator(Validator):
#     def _validate_is_mongoid(self, constraint, field, value):
#         """ Test the oddity of a value.
#
#         The rule's arguments are validated against this schema:
#         {'type': 'boolean'}
#         """
#         if constraint is True and not ObjectId.is_valid(value & 1):
#             self._error(field, "Must be an Mongo Object ID")

class Rules:
    @staticmethod
    def string(key=None, type='string', required=False, maxlength=100, minlength=1):
        try:
            return {key: {'type': type, 'required': required, 'maxlength': maxlength, 'minlength': minlength}}
        except:
            raise Exception(f"Validation error key = {key}, type = {type} ")

    @staticmethod
    def integer(key=None, type='integer', required=False, min=1, max=10):
        try:
            return {key: {'type': type, 'required': required, 'min': min, 'max': max}}
        except:
            raise Exception(f"Validation error key = {key}, type = {type} ")

    @staticmethod
    def email(key=None, type='string', required=False, regex='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'):
        try:
            return {key: {'type': type, 'required': required, 'regex': regex}}
        except:
            raise Exception(f"Validation error key = {key}, type = {type} ")


class ObjectIDValidation:
    @staticmethod
    def is_valid_mongoid(_id):
        return ObjectId.is_valid(_id)


class CreateFavouriteValidation:
    name = Rules.string(key='name', required=True)
    is_valid_name = Validator(name)


class CreateUserValidation:
    email = Rules.email(key='email', required=True)
    password = Rules.string(key='password', required=True, minlength=6)
    username = Rules.string(key='username', required=True, minlength=1)

    is_valid_email = Validator(email)
    is_valid_password = Validator(password)
    is_valid_username = Validator(username)


class SearchRequestValidation:
    search_text = Rules.string(key='q', required=True)
    page = Rules.integer(key='page', required=False, max=1000000)

    is_valid_search_text = Validator(search_text)
    is_valid_page = Validator(page)


# class CreateFavourite:
#
#     schema = {'id': {'type': 'string', 'check_with': 'mongoid'}}
#     valid = MongoObjectIDValidator(Validator(schema))
