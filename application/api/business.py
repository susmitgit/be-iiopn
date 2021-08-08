from flask import jsonify
from application.utils.auth import requires_auth
from application.api import api as api_auth
from application.models import Business
from application.api.error_response import ErrorResponses
from application.api.request_validator import *

error = ErrorResponses()


@api_auth.route("/business/<id>", methods=["GET"])
@requires_auth
def get_business_with_name(id):
    try:
        if not ObjectIDValidation.is_valid_mongoid(id):
            return error.not_found(message='business')
    except:
        return error.required_filed(['business ID'])
    b_id = id if Business.get_business_with_business_id(id=id) else None
    if b_id:
        return jsonify(result=Business.get_business_with_business_id(id=b_id))
    else:
        return error.not_found(
            message='business'
        )
