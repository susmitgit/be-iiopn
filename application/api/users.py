from flask import request, jsonify, g
from application.utils.auth import generate_token, requires_auth, verify_token
from application.api import api as api_auth
from application.models.models import User


@api_auth.route("/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


@api_auth.route("/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User({'email': incoming["email"], 'password': User.hashed_password(incoming["password"]),
                 'username': incoming['username']})

    try:
        if not User.find_one({'email': incoming["email"]}):
            user.save()
    except Exception:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.find_one({'email': incoming["email"]})
    return jsonify(
        id=str(new_user['_id']),
        token=generate_token(new_user)
    )


@api_auth.route("/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])

    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@api_auth.route("/is_valid_token", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403
