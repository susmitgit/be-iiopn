from flask import request, jsonify
from application.utils.auth import requires_auth
from application.api import api as api_auth
from application.models import Schedule
from datetime import datetime
from application.api.error_response import ErrorResponses

error = ErrorResponses()


@api_auth.route("/schedule", methods=["GET"])
@requires_auth
def get_schedule_with_datetime():
    incoming = request.get_json()
    if incoming.get('datetime', None):
        try:
            dt = datetime.strptime(incoming['datetime'], '%Y-%m-%d %H:%M:%S')
            return jsonify(result=Schedule.get_schedule_with_business_datetime(dt=dt))
        except Exception as e:
            print(str(e))
            return error.required_filed(fields=['datetime'])
    else:
        return error.required_filed(fields=['datetime'])

