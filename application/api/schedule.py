from flask import request, jsonify
from application.utils.auth import requires_auth
from application.api import api as api_auth
from application.models import Schedule
from datetime import datetime
from application.api.error_response import ErrorResponses
from application.utils.pagination import Pagination
from application.api.request_validator import SearchRequestValidation

@api_auth.route("/schedule", methods=["GET"])
@requires_auth
def get_schedule_with_datetime():
    incoming = request.get_json()
    page = 1
    d_time = incoming.get('datetime', None)
    try:
        page = int(request.args.get('page', 1))
        if not SearchRequestValidation.is_valid_page({'page': page}):
            return ErrorResponses.bad_request()
    except:
        return ErrorResponses.bad_request()
    if d_time:
        try:
            dt = datetime.strptime(d_time, '%Y-%m-%d %H:%M:%S')
            return jsonify(result=Schedule.get_schedule_with_business_datetime(dt=dt, page=page))
        except Exception as e:
            return ErrorResponses.required_filed(fields=['datetime'])
    else:
        return ErrorResponses.required_filed(fields=['datetime'])

