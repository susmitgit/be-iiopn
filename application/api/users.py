from flask import request, jsonify, g
from application.utils.auth import generate_token, requires_auth, verify_token
from application.api import api as api_auth
from application.models import User, Favourite, FavouriteBusiness, Business, UserFavourite
from application.api.error_response import ErrorResponses as error
from application.utils.helpers import exclude_mongo_id
from application.api.request_validator import *
from application.app_config import AppConfig
from bson import ObjectId


@api_auth.route("/me", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


@api_auth.route("/favourites", methods=["GET"])
@requires_auth
def get_favourites():
    data = list(UserFavourite.find({'u_id': g.current_user['id']})) or []
    return jsonify(result=exclude_mongo_id(data))


@api_auth.route("/business_search", methods=["GET"])
@requires_auth
def business_search():
    incoming = request.args
    page = incoming.get('page', 1)
    if not Search.valid(incoming):
        return error.bad_request()
    # Business search
    data = Business.search_business(search_txt=incoming['business'], page=page)
    return jsonify(result=exclude_mongo_id(data))


@api_auth.route("/favourite_search", methods=["GET"])
@requires_auth
def favourite_search():
    incoming = request.args
    page = incoming.get('page', 1)
    if not Search.valid(incoming):
        return error.bad_request()
    # Favourite search
    data = Favourite.search_favourite(search_txt=incoming['favourite'], page=page)
    return jsonify(result=exclude_mongo_id(data))


@api_auth.route("/favourite", methods=["POST"])
@requires_auth
def create_favourite():
    fav_id = None
    fav_name = None
    incoming = request.get_json()
    if incoming.get('id', None):
        try:
            fav_id = incoming['id'] if ObjectId.is_valid(incoming['id']) else None
        except:
            return error.required_filed(['name', 'id'])
    if incoming.get('name', None):
        fav_name = incoming['name']
    if fav_id:
        is_exists = Favourite.find_one({'_id': ObjectId(fav_id), 'u_id': g.current_user['id']})
        if is_exists:
            return jsonify(result=exclude_mongo_id(is_exists))
    elif fav_name:
        is_exists = Favourite.find_one({'name': fav_name, 'u_id': g.current_user['id']})
        if is_exists:
            return jsonify(result=exclude_mongo_id(is_exists))
        else:
            favorite = Favourite({'name': fav_name, 'u_id': g.current_user['id']})
            favorite.save()
            is_exists = Favourite.find_one({'name': fav_name, 'u_id': g.current_user['id']}) or None
            if is_exists:
                fav_id = str(is_exists.get("_id", None))
                user_favourite = UserFavourite({'u_id': g.current_user['id'], 'fav_id': fav_id})
                user_favourite.save()
            return jsonify(result=exclude_mongo_id(is_exists)), 201

    return error.required_filed(['name', 'id'])


@api_auth.route("/favourite/<id>/business", methods=["POST"])
@requires_auth
def create_favourite_business(id):
    b_id = None
    fav_id = id
    incoming = request.get_json()
    if fav_id:
        try:
            fav_id = id if Favourite.find_one({'_id': ObjectId(fav_id)}) else None
        except:
            return error.required_filed(['fav_id'])

    if incoming.get('b_id', None):
        try:
            b_id = incoming.get('b_id') if Business.find_one({"_id": ObjectId(incoming['b_id'])}) else None
        except:
            return error.required_filed(['b_id'])

    is_exists = FavouriteBusiness.find_one({'fav_id': fav_id, 'b_id': b_id, 'u_id': g.current_user['id']})
    if is_exists:
        return jsonify(result=exclude_mongo_id(is_exists))
    else:
        fb = FavouriteBusiness({'fav_id': fav_id, 'b_id': b_id, 'u_id': g.current_user['id']})
        fb.save()
        is_exists = FavouriteBusiness.find_one({'fav_id': fav_id, 'b_id': b_id, 'u_id': g.current_user['id']})
        return jsonify(result=exclude_mongo_id(is_exists)), 201


@api_auth.route("/favourite/<id>/business", methods=["GET"])
@requires_auth
def list_favourite_business(id):
    fav_id = id
    if fav_id:
        try:
            fav_id = id if Favourite.find_one({'_id': ObjectId(fav_id)}) else None
        except:
            return error.required_filed(['fav_id'])
    is_exists = list(FavouriteBusiness.find({'fav_id': fav_id, 'u_id': g.current_user['id']})) or []
    return jsonify(result=exclude_mongo_id(is_exists))


@api_auth.route("/share_favourites", methods=["POST"])
@requires_auth
def share_favourites():
    incoming = request.get_json()
    try:
        u_id = incoming['u_id'] if User.find({"_id": ObjectId(incoming['u_id'])}) else None
        fav_id = incoming['fav_id'] if Favourite.find({"_id": ObjectId(incoming['fav_id'])}) else None
        if u_id and fav_id:
            is_exists = UserFavourite.find_one({'fav_id': fav_id, 'u_id': u_id})
            if not is_exists:
                user_favourite = UserFavourite({'fav_id': fav_id, 'u_id': u_id})
                user_favourite.save()
                is_exists = UserFavourite({'fav_id': fav_id, 'u_id': u_id})
                return jsonify(result=exclude_mongo_id(is_exists)), 201
            return jsonify(result=exclude_mongo_id(is_exists))
        else:
            return error.required_filed(
                fields=['u_id', 'fav_id']
            )
    except:
        return error.required_filed(
            fields=['u_id', 'fav_id']
        )


@api_auth.route("/users", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User({'email': incoming["email"], 'password': User.hashed_password(incoming["password"]),
                 'username': incoming['username']})

    try:
        if not User.find_one({'email': incoming["email"]}):
            user.save()
        else:
            return error.resource_exists()
    except Exception:
        return error.resource_exists()

    new_user = User.find_one({'email': incoming["email"]})
    return jsonify(
        id=str(new_user['_id']),
        token=generate_token(new_user)
    ), 201


@api_auth.route("/authenticate", methods=["POST"])
def authorize():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])

    if user:
        return jsonify(token=generate_token(user))

    return error.unauthorised_access()


@api_auth.route("/authorize", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(is_valid=True)
    else:
        return jsonify(is_valid=False), 403
