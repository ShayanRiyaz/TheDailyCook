import os
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_uploads import configure_uploads, patch_request_class
from extensions import db, jwt, image_set,cache,limiter
#import flask
from config import Config

from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource, RecipeCoverUploadResource
from resources.user import UserListResource, UserResource, MeResource, UserRecipeListResource, UserActivateResource, UserAvatarUploadResource
from resources.token import TokenResource, RefreshResource,RevokeResource,black_list



def create_app():
    """
    Creates the app in either Production, Staging or Development Configuration.
    Default is set to Development.
    
    """
    env = os.environ.get('ENV','Development')

    if env == 'Production':
        config_str = 'config.ProductionConfig'
    elif env == 'Staging':
        config_str = 'config.StagingConfig'
    else:
        config_str = 'config.DevelopmentConfig'

    app = Flask(__name__)
    app.config.from_object(config_str)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app,db)
    jwt.init_app(app)
    configure_uploads(app, image_set)
    patch_request_class(app, 10 * 1024 * 1024)
    cache.init_app(app)
    limiter.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_black(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list

def register_resources(app):
    """
    Adds all the API resources from the respective directories.
    Divided into three main categories.
    Users, Token (JWT) and Recipes.
    
    :params: app - Flask application.
    """
    api = Api(app)
    api.add_resource(UserListResource,'/users')
    api.add_resource(UserResource,'/users/<string:username>')
    api.add_resource(UserRecipeListResource,'/users/<string:username>/recipes')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserAvatarUploadResource,'/users/avatar')
    
    api.add_resource(TokenResource,'/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    api.add_resource(RecipeListResource,'/recipes')
    api.add_resource(RecipeResource,'/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource,'/recipes/<int:recipe_id>/publish')
    api.add_resource(RecipeCoverUploadResource,'/recipes/<int:recipe_id>/cover')

    api.add_resource(MeResource,'/me')

if __name__ == '__main__':
    app = create_app()
    app.run()
