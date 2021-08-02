from flask import request, jsonify
from application.utils.auth import requires_auth
from application.api import api as api_auth
from application.models import Business
from application.api.error_response import ErrorResponses

error = ErrorResponses()


@api_auth.route("/business", methods=["GET"])
@requires_auth
def get_business_with_name():
    incoming = request.get_json()
    if incoming.get('name', None):
        return jsonify(result=Business.get_business_with_name(name=incoming['name']))
    elif incoming.get('id', None):
        return jsonify(result=Business.get_business_with_business_id(id=incoming['id']))
    else:
        return error.required_filed(fields=['name', 'id'])



