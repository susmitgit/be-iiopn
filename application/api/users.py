import logging

from flask import request, jsonify, g
from application.utils.auth import generate_token, requires_auth, verify_token
from application.api import api as api_auth
from application.models import User, Favourite, FavouriteBusiness, Business, UserFavourite

from application.api.error_response import ErrorResponses as error
from application.utils.helpers import exclude_mongo_id
from application.api.request_validator import *
from bson import ObjectId


@api_auth.route("/me", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


@api_auth.route("/favourites", methods=["GET"])
@requires_auth
def my_favourites():
    try:
        page = int(request.args.get('page', 1))
        if not SearchRequestValidation.is_valid_page({'page': page}):
            return error.bad_request()
    except:
        return error.bad_request()

    data = UserFavourite.get_favourites_with_u_id(u_id=g.current_user['id'], page=page)

    return jsonify(result=exclude_mongo_id(data))


@api_auth.route("/business_search", methods=["GET"])
@requires_auth
def business_search():
    incoming = request.args
    try:
        page = incoming.get('page', 1)
        search_text = incoming.get('q', '')
        if not SearchRequestValidation.is_valid_page({'page': int(page)}):
            return error.bad_request()
        if not SearchRequestValidation.is_valid_search_text({'q': search_text}):
            return error.required_filed(['q'])
    except:
        return error.bad_request()
    # Business search
    data = Business.search_business(search_txt=search_text, page=page)
    return jsonify(result=exclude_mongo_id(data))


@api_auth.route("/favourite_search", methods=["GET"])
@requires_auth
def favourite_search():
    incoming = request.args
    try:
        page = incoming.get('page', 1)
        search_text = incoming.get('q', '')
        if not SearchRequestValidation.is_valid_page({'page': int(page)}):
            return error.bad_request()
        if not SearchRequestValidation.is_valid_search_text({'q': search_text}):
            return error.required_filed(['q'])
    except:
        return error.bad_request()
    data = Favourite.search_favourite(search_txt=search_text, page=page)
    return jsonify(result=exclude_mongo_id(data))


@api_auth.route("/favourite", methods=["POST"])
@requires_auth
def create_favourite():
    incoming = request.get_json()
    try:
        fav_name = incoming['name']
        if not CreateFavouriteValidation.is_valid_name({'name': fav_name}):
            return error.required_filed(['name'])
    except:
        return error.bad_request()

    is_exists = Favourite.find_one({'name': fav_name, 'u_id': g.current_user['id']})
    if is_exists:
        return jsonify(result=exclude_mongo_id(is_exists))
    else:
        favorite = {'name': fav_name, 'u_id': g.current_user['id']}
        Favourite.save(doc=favorite)
        is_exists = Favourite.find_one({'name': fav_name, 'u_id': g.current_user['id']}) or None
        if is_exists:
            fav_id = str(is_exists.get("_id", None))
            user_favourite = {'u_id': g.current_user['id'], 'fav_id': fav_id}
            UserFavourite.save(doc=user_favourite)
        return jsonify(result=exclude_mongo_id(is_exists)), 201


@api_auth.route("/favourite/<id>/business", methods=["POST"])
@requires_auth
def create_favourite_business(id):

    fav_id = id
    incoming = request.get_json()
    try:
        b_id = incoming['b_id']
        if not ObjectIDValidation.is_valid_mongoid(b_id):
            return error.required_filed(['b_id'])
        if not ObjectIDValidation.is_valid_mongoid(fav_id):
            return error.required_filed(['fav_id'])
    except:
        return error.required_filed(['b_id'])

    favourite = id if Favourite.find_one({'_id': ObjectId(fav_id)}) else None
    if not favourite:
        return error.not_found(message='favourite')

    business = b_id if Business.find_one({"_id": ObjectId(b_id)}) else None
    if not business:
        return error.not_found(message='business')

    same_exists = FavouriteBusiness.find_one({'fav_id': fav_id, 'b_id': b_id, 'u_id': g.current_user['id']})
    if not same_exists:
        fb = {'fav_id': fav_id, 'b_id': b_id, 'u_id': g.current_user['id']}
        FavouriteBusiness.save(doc=fb)
        inserted = FavouriteBusiness.find_one({'fav_id': fav_id, 'b_id': b_id, 'u_id': g.current_user['id']})
        return jsonify(result=exclude_mongo_id(inserted)), 201
    return jsonify(result=exclude_mongo_id(same_exists))


@api_auth.route("/favourite/<id>/business", methods=["GET"])
@requires_auth
def list_favourite_business(id):
    fav_id = id
    try:
        favourite = id if Favourite.find_one({'_id': ObjectId(fav_id)}) else None
    except:
        return error.required_filed(['fav_id'])
    if not favourite:
        return error.not_found('favourite')

    is_exists = list(FavouriteBusiness.find({'fav_id': fav_id, 'u_id': g.current_user['id']})) or []
    return jsonify(result=exclude_mongo_id(is_exists))


@api_auth.route("/share_favourites", methods=["POST"])
@requires_auth
def share_favourites():
    incoming = request.get_json()
    try:
        u_id = incoming['u_id'] if User.find({"_id": ObjectId(incoming['u_id'])}) else None
    except:
        return error.not_found(message='user')
    try:
        fav_id = incoming['fav_id'] if Favourite.find({"_id": ObjectId(incoming['fav_id'])}) else None
    except:
        return error.not_found(message='favourite')

    if u_id and fav_id:
        is_exists = UserFavourite.find_one({'fav_id': fav_id, 'u_id': u_id})
        if not is_exists:
            user_favourite = {'fav_id': fav_id, 'u_id': u_id}
            inserted = UserFavourite.save(doc=user_favourite)
            inserted_data = UserFavourite.find_one({'_id': ObjectId(inserted.inserted_id)})
            return jsonify(result=exclude_mongo_id(inserted_data)), 201
        return jsonify(result=exclude_mongo_id(is_exists))
    else:
        return error.required_filed(
            fields=['u_id', 'fav_id']
        )


@api_auth.route("/users", methods=["POST"])
def create_user():
    incoming = request.get_json()
    try:
        username = incoming['username']
        if not CreateUserValidation.is_valid_username({'username': username}):
            return error.required_filed(['username'])

        email = incoming['email']
        if not CreateUserValidation.is_valid_email({'email': email}):
            return error.required_filed(['email'])

        password = incoming['password']
        if not CreateUserValidation.is_valid_password({'password': password}):
            return error.required_filed(['password with minimum 6 character length'])
    except:
        return error.bad_request()


    try:
        if not User.find_one({'email': email}):
            insert = User.save({'email': email, 'password': User.hashed_password(password), 'username': username})
            new_user = User.find_one({'_id': insert.inserted_id})
            return jsonify(
                id=str(new_user['_id']),
                token=generate_token(new_user)
            ), 201
        return error.resource_exists(resource='user')
    except Exception as e:
        logging.info(str(e))
        return error.bad_request()


@api_auth.route("/authenticate", methods=["POST"])
def authenticate():
    incoming = request.get_json()
    try:
        email = incoming['email']
        if not CreateUserValidation.is_valid_email({'email': email}):
            return error.required_filed(['email'])

        password = incoming['password']
        if not CreateUserValidation.is_valid_password({'password': password}):
            return error.required_filed(['password with minimum 6 character length'])
    except:
        return error.bad_request()

    user = User.get_user_with_email_and_password(email, password)

    if user:
        return jsonify(token=generate_token(user))

    return error.unauthorised_access()


@api_auth.route("/authorize", methods=["POST"])
def authorize():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(is_valid=True)
    else:
        return jsonify(is_valid=False), 403
