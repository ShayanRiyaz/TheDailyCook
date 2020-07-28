
from flask_restful import Resource
from http import HTTPStatus
from flask import request,url_for,render_template
from mailgun import MailgunApi


from flask_jwt_extended import jwt_optional, get_jwt_identity,jwt_required
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.recipe import Recipe
from models.user import User
from schemas.recipe import RecipeSchema
from schemas.user import UserSchema

from extensions import image_set
from utils import generate_token,verify_token, save_image

import os

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))
recipe_list_schema = RecipeSchema(many=True)
user_avatar_schema = UserSchema(only=('avatar_url',))

mailgun = MailgunApi(domain=os.environ.get('MAILGUN_DOMAIN'),
                     api_key=os.environ.get('MAILGUN_API_KEY'))
class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()
        data,errors = user_schema.load(data = json_data)

        if errors:
            return {'message':'Validation Errors','Errors':errors},HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message':'username already used'},HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message':'email aready used'},HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        token = generate_token(user.email,
                               salt = 'activate') # Token is used to activate the account

        subject ='Please confirm your registration'
        link = url_for('useractivateresource',
                       token = token,
                       _external = True) # Convert the default relative URL to absolute
        text = f'Hi,Thanks for using The Daily Cook! Please confirm your registration by clicking on the link:{link}'

        mailgun.send_email(to=user.email,
                           subject=subject,
                           text=text,
                           html = render_template('email/confirmation.html',
                                                  link = link))

        return user_schema.dump(user).data,HTTPStatus.CREATED

class UserResource(Resource):

    @jwt_optional #decorator # Implies endpoint is accessible regardless
    def get(self,username): # of the procession of the token
        user = User.get_by_username(username=username) # Check whether username can be found in the db
        if user is None:
            return {'message':'user not found'}, HTTPStatus.NOT_FOUND

        # If found in the database we will further check it matches the identity of the user ID in the JWT
        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data

        else:
            data = user_public_schema.dump(user)

        return data,HTTPStatus.OK

class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id = get_jwt_identity())

        return user_schema.dump(user).data,HTTPStatus.OK


class UserRecipeListResource(Resource):
    @jwt_optional
    @use_kwargs({'visibility':fields.Str(missing = 'public')})

    def get(self,username,visibility):
        user = User.get_by_username(username = username)

        if user is None:
            return {'message':'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user == user.id and visibility in ['all','private']:
            pass
        else:
            visibility = 'public'
        recipes = Recipe.get_all_by_user(user_id = user.id,visibility = visibility)

        return recipe_list_schema.dump(recipes).data,HTTPStatus.OK


class UserActivateResource(Resource):
    def get(self,token):
        email = verify_token(token,salt='activate') #Token is verified, default expiration is 30 minutes
        if email is False:
            return {'message':'Invalid token or token expired'},HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)
        if not user:
            return {'message':'User not found'},HTTPStatus.NOT_FOUND

        if user.is_active is True:
            return {'message':'The user account is already activated'},HTTPStatus.BAD_REQUEST

        user.is_active = True
        user.save()

        return {},HTTPStatus.NO_CONTENT

    # In a real-world scenario the activation in the email will point to
    # to the front-end of the system, the frontend will, in turn communicate with the backend through the API.
    # Therefore, when the frontend receives the HTTP status code 204 No Content, it means the
    # the account is activated. It can then forward the user to the account dashboard


class UserAvatarUploadResource(Resource):
    @jwt_required
    def put(self):
        file = request.files.get('avatar')
        if not file:
            return {'message': 'Not a valid image'}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {'message': 'File type not allowed'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_id(id=get_jwt_identity())

        if user.avatar_image:
            avatar_path = image_set.path(folder='avatars',
                                         filename=user.avatar_image)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)

        filename = save_image(image=file,
                              folder='avatars')
        user.avatar_image = filename
        user.save()

        return user_avatar_schema.dump(user).data, HTTPStatus.OK
