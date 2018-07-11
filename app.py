from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT
from security import authenticate, identity as identity_function

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'hunter2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=36000)
jwt = JWT(app, authenticate, identity_function)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

@jwt.jwt_error_handler
def customized_error_handler(error):
	return jsonify({
		'message' : error.description,
		'code' : error.status_code
	}), error.status_code

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
	return jsonify({
		"access_token" : access_token.decode('utf-8'),
		"user_id": identity.id,
		"username": identity.username
	})

if __name__ == "__main__":
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)
