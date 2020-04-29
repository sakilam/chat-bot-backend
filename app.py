# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS

from analyzer import greeting, response

# creating the flask app
app = Flask(__name__)

CORS(app)

# creating an API object
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_input')

class Bot(Resource):

    def post(self):
        user_response = parser.parse_args()
        user_response = user_response['user_input'].lower()
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you' ):
                res = "You're welcome !"
            else:
                if(greeting(user_response)!=None):
                    res = greeting(user_response)
                else:
                    res = response(user_response)
        else:
            res = "Chat with you later !"
        return jsonify({'response': res})

# adding the defined resources along with their corresponding urls
api.add_resource(Bot, '/bot')

# driver function
if __name__ == '__main__':
    app.run(debug = True)
