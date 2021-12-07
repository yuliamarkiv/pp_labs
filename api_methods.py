from flask import jsonify, request, Flask
from lab_8.dbcomands import Session
from lab_8.schemas import UserSchema, LocationSchema, AdSchema
from lab_8.models import *
from marshmallow import ValidationError
import bcrypt
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
session = Session()
auth = HTTPBasicAuth()

if session.query(Location).first() is None:
    location = Location(name='Town')
    session.add(location)
    session.commit()


# USER METHODS
@app.route('/api/v1/user', methods=["POST"])
def create_user():

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    user_find = session.query(User).filter_by(username=data['username']).first()
    if user_find:
        return {"message": "User with such username already exists"}, 400

    user_find = session.query(User).filter_by(email=data['email']).first()
    if user_find:
        return {"message": "User with such email already exists"}, 400

    location_find = session.query(Location).filter_by(id=data['locationId']).first()
    if not location_find:
        return {"message": "Location with such address doesnt exist"}, 400

    if data['password']:
        data['password'] = bcrypt.hashpw(data['password'].encode("utf-8"), bcrypt.gensalt())
    else:
        return {"message": "No password data provided"}, 400

    try:
        user_data = UserSchema().load(data)
    except ValidationError as err:
        return err.messages, 422

    the_user = User(**user_data)

    session.add(the_user)
    session.commit()

    # the_user = session.query(User).filter_by(name=data['name']).first()
    result = UserSchema().dump(the_user)
    return jsonify(result)


@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username= username).first()
    if not user:
        return False
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return False
    if user:
        return user


@app.route('/api/v1/user/<string:username>', methods=['GET'])
@auth.login_required
def get_user(username):
    user_find = session.query(User).filter_by(username=username).first()
    if not user_find:
        return {"message": "User with such username does not exist"}, 404
    if auth.username() != username:
        return {"message": "Access denied"}, 403

    result = UserSchema().dump(user_find)
    return jsonify(result)


@app.route('/api/v1/user/<string:username>', methods=['PUT'])
@auth.login_required
def update_user(username):
    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400
    user_find = auth.current_user()
    if auth.username() != username:
        return {"message": "Access denied"}, 403
    # user_find = session.query(User).filter_by(username=username).first()
    if not user_find:
        return {"message": "User with such name does not exist"}, 400
    if 'id' in data:
        return {"message": "You can not change the id"}, 400

    if 'username' in data:
        check_user = session.query(User).filter_by(username=data['username']).first()
        if check_user:
            return {"message": "User with such name already exists"}, 400

    if 'email' in data:
        check_user = session.query(User).filter_by(email=data['email']).first()
        if check_user:
            return {"message": "User with such email already exists"}, 400

    attributes = User.__dict__.keys()

    for key, value in data.items():
        if key == 'id':
            return {"message": "You can not change id"}, 403

        if key not in attributes:
            return {"message": "Invalid input data provided"}, 404

        if key == 'password':
            value = bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt())

        setattr(user_find, key, value)

    session.commit()
    result = UserSchema().dump(user_find)

    return jsonify(result)


@app.route('/api/v1/user/<string:username>', methods=['DELETE'])
@auth.login_required
def delete_user(username):
    user = auth.current_user()
    user_find = session.query(User).filter_by(username=username).first()
    if not user_find:
        return {"message": "User with such name does not exists"}, 404
    if user.username != user_find.username:
        return {"message": "Access denied"}, 403
    stat_find = session.query(Ad).filter_by(userId=user_find.id).first()
    if stat_find:
        return {"message": "This user has ads"}, 403

    result = UserSchema().dump(user_find)

    session.delete(user_find)
    session.commit()

    return jsonify(result)


# AD METHODS

@app.route('/api/v1/ad', methods=['POST'])
@auth.login_required
def create_ad():
    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400
    if 'name' not in data:
        return {"message": "No required data {name} provided"}, 400

    if 'price' not in data:
        return {"message": "No required data {price} provided"}, 400

    if 'currency' not in data:
        return {"message": "No required data {currency} provided"}, 400

    if 'date' not in data:
        return {"message": "No required data {date} provided"}, 400

    if 'id' in data:
        return {"message": "You can not change id"}, 401

    # user_find = session.query(User).filter_by(id=data['userId']).first()
    user_find = auth.current_user()
    if not user_find:
        return {"message": "User with such id doesnt exists"}, 404

    if 'locationId' in data:
        location_find = session.query(Location).filter_by(id=data['locationId']).first()
        if not location_find:
            return {"message": "Location with such id doesnt exists"}, 404

    try:
        ad_data = AdSchema().load(data)
    except ValidationError as err:
        return err.messages, 422
    the_ad = Ad(**ad_data)
    the_ad.userId = user_find.id

    session.add(the_ad)
    session.commit()

    result = AdSchema().dump(the_ad)
    return jsonify(result)


@app.route('/api/v1/ad/<int:id>', methods=['GET'])
def get_ad(id):

    ad_find = session.query(Ad).filter_by(id=id).first()
    if not ad_find:
        return {"message": "Ad with such id does not exist"}, 404

    if ad_find.locationId:
        return {"message": "This is a local ad. Unauthorized users have access only for public ads."}, 403

    result = AdSchema().dump(ad_find)
    return jsonify(result)


@app.route('/api/v1/ad/<int:id>', methods=['PUT'])
@auth.login_required
def update_ad(id):
    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    ad_find = session.query(Ad).filter_by(id=id).first()
    user = auth.current_user()
    if not ad_find:
        return {"message": "Ad with such id does not exist"}, 400
    if user.id != ad_find.userId:
        return {"message": "Access denied"},403

    if 'id' in data:
        return {"message": "You can not change the id"}, 400

    if 'name' in data:
        check_user = session.query(Ad).filter_by(name=data['name']).first()
        if check_user:
            return {"message": "Ad with such name already exists"}, 400

    attributes = Ad.__dict__.keys()

    for key, value in data.items():
        if key == 'id':
            return {"message": "You can not change id"}, 403

        if key not in attributes:
            return {"message": "Invalid data provided"}, 400

        if key == 'userId':
            return {"message": "You can not change userId"}, 403

        setattr(ad_find, key, value)

    session.commit()
    result = AdSchema().dump(ad_find)

    return jsonify(result)


@app.route('/api/v1/ad/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_ad(id):
    ad_find = session.query(Ad).filter_by(id=id).first()
    user = auth.current_user()
    if not ad_find:
        return {"message": "Ad with such id does not exist"}, 404
    if user.id != ad_find.userId:
        return {"message": "Access denied"}, 403
    result = AdSchema().dump(ad_find)
    session.delete(ad_find)
    session.commit()

    return jsonify(result)


# LOCATION METHODS
@app.route('/api/v1/location', methods=['POST'])
@auth.login_required
def create_location():

    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400
    if 'name' not in data:
        return {"message": "No input data provided"}, 400

    if 'id' in data:
        return {"message": "You can not change id"}, 401

    location_find = session.query(Location).filter_by(name=data['name']).first()
    user = auth.current_user()
    if not user:
        return {"message": "Access denied"}, 403
    if location_find:
        return {"message": "Location already exists"}, 400

    try:
        location_data = LocationSchema().load(data)
    except ValidationError as err:
        return err.messages, 422
    the_location = Location(**location_data)

    session.add(the_location)
    session.commit()

    result = LocationSchema().dump(the_location)
    return jsonify(result)

# AD SERVICE

# showing public notes for unauthorized users
@app.route('/api/v1/service/ads', methods=['GET'])
def get_public_ads():


    find_ads = session.query(Ad).filter_by(locationId=None).all()

    schema = AdSchema(many=True)
    result = (schema.dump(find_ads))

    return jsonify(result)


# showing notes for authorized user (including all: public and accessible local ads for specific user)

@app.route('/api/v1/service/user/<int:id>', methods=['GET'])
@auth.login_required
def get_ads_for_user(id):

    user_find = session.query(User).filter_by(id=id).first()
    user = auth.current_user()
    if not user_find:
        return {"message": "User with such id does not exist"}, 404
    if user.id != id:
        return {"message": "Access denied"}, 403

    public_ads = session.query(Ad).filter_by(locationId=None).all()

    schema = AdSchema(many=True)
    public = (schema.dump(public_ads))

    user_location = session.query(User).filter_by(id=id).first()
    local_ads = session.query(Ad).filter_by(locationId=user_location.locationId).all()
    schema = AdSchema(many=True)
    local = (schema.dump(local_ads))

    return jsonify(public + local)


# showing locations
@app.route('/api/v1/service/locations', methods=['GET'])
def get_locations():
    locations = session.query(Location).all()

    schema = LocationSchema(many=True)
    result = (schema.dump(locations))

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug = True)
