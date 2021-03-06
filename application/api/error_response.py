from flask import jsonify


class ErrorResponses:
    @staticmethod
    def not_found(message=None):
        if message:
            return jsonify(error={'status_code': 404, 'message': f'[ {message} ] Resource not found'}), 404
        return jsonify(error={'status_code': 404, 'message': 'Resource not found'}), 404

    @staticmethod
    def bad_request():
        return jsonify(error={'status_code': 400, 'message': 'Bad request'}), 400

    @staticmethod
    def unauthorised_access():
        return jsonify(error={'status_code': 403, 'message': 'Access restricted / Unauthorised'}), 403

    @staticmethod
    def method_not_allowed():
        return jsonify(error={'status_code': 405, 'message': 'Method not allowed'}), 405

    @staticmethod
    def resource_exists(resource=None):
        if resource:
            return jsonify(error={'status_code': 409, 'message': f'[{resource}] Resource exists'}), 409
        return jsonify(error={'status_code': 409, 'message': 'Resource exists'}), 409

    @staticmethod
    def required_filed(fields=[]):
        seperator = ', '
        return jsonify(error={'status_code': 400, 'message': f'Either missing required [ {seperator.join(fields)} ] or '
                                                             f'value error'}), 400

    @staticmethod
    def internal_server_error(message=None):
        return jsonify(error={'status_code': 500, 'message': message}), 500

    @staticmethod
    def api_rate_limit_error(message=None):
        return jsonify(error={'status_code': 429, 'message': message}), 429

