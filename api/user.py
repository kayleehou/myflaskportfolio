from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            firstName = body.get('firstName')
            if firstName is None or len(firstName) < 2:
                return {'message': f'first name is missing, or is less than 2 characters'}, 210
            lastName = body.get('lastName')
            if lastName is None or len(lastName) < 2:
                return {'message': f'last name is missing, or is less than 2 characters'}, 210
            extracurricular = body.get('extracurricular')
            if extracurricular is None or len(extracurricular) < 2:
                return {'message': f'extracurricular is missing, or is less than 2 characters'}, 210
            hoursPerWeek = body.get('hoursPerWeek')
            if hoursPerWeek is None or len(hoursPerWeek) < 0:
                return {'message': f'hours has to be at least 1 hour'}, 210
            coachName = body.get('coachName')
            if coachName is None or len(coachName) < 2:
                return {'message': f'coach name has to be at least two letters'}, 210
            # validate uid
            # look for password and dob

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User( firstName=firstName, 
                      lastName=lastName, 
                      extracurricular=extracurricular, 
                      hoursPerWeek=hoursPerWeek,
                      coachName=coachName)
            
            ''' Additional garbage error checking '''
            # set password if provided
            # if password is not None:
            #     uo.set_password(password)
            # # convert to date type
            # if dob is not None:
            #     try:
            #         uo.dob = datetime.strptime(dob, '%m-%d-%Y').date()
            #     except:
            #         return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 210
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {firstName}, either a format error or last name {lastName} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')