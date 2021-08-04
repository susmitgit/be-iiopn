import cerberus
from cerberus import Validator
from bson import ObjectId

# mongoid_type = cerberus.TypeDefinition('mongoid', (ObjectId,), ())

class MongoObjectIDValidator(Validator):
    def _check_with_mongoid(self, field, value):
        if not ObjectId.is_valid(value):
            self._error(field, "Must be an Mongo ID")
# class MongoObjectIDValidator(Validator):
#     def _validate_is_mongoid(self, constraint, field, value):
#         """ Test the oddity of a value.
#
#         The rule's arguments are validated against this schema:
#         {'type': 'boolean'}
#         """
#         if constraint is True and not ObjectId.is_valid(value & 1):
#             self._error(field, "Must be an Mongo Object ID")

class Search:
    schema = {'q': {'type': 'string', 'maxlength': 100}}
    valid = Validator(schema)


class CreateFavourite:

    schema = {'id': {'type': 'string', 'check_with': 'mongoid'}}
    valid = MongoObjectIDValidator(Validator(schema))
