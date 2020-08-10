from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity,jwt_required,jwt_optional
from http import HTTPStatus
from models.recipe import Recipe
from schemas.recipe import RecipeSchema

import os
from extensions import image_set,cache, limiter
from utils import save_image, clear_cache
from webargs import fields
from webargs.flaskparser import use_kwargs
from schemas.recipe import RecipeSchema,RecipePaginationSchema

# Serializing the Schemas
recipe_schema = RecipeSchema()
recipe_cover_schema = RecipeSchema(only=('cover_url',))
recipe_list_schema = RecipeSchema(many=True)
recipe_pagination_schema = RecipePaginationSchema()


class RecipeResource(Resource):

    @jwt_optional
    def get(self,recipe_id):


        """

        :param
        """

        recipe = Recipe.get_by_id(recipe_id = recipe_id)
        if recipe is None:
            return {'message':'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return recipe_schema.dump(recipe).data, HTTPStatus.OK


    @jwt_required
    def patch(self,recipe_id):
        """

        :param
        """

        json_data = request.get_json()

        data,errors = recipe_schema.load(data=json_data,partial=('name',))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        recipe = Recipe.get_by_id(recipe_id = recipe_id)
        if recipe is None:
            return {'message':'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message':'Access is not Allowed'}, HTTPStatus.FORBIDDEN


        recipe.name = data.get('name') or recipe.name
        recipe.description = data.get('description') or recipe.description
        recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings
        recipe.cook_time = data.get('cook_time') or recipe.cook_time
        recipe.directions = data.get('directions') or recipe.directions
        recipe.ingredients = data.get('ingredients') or recipe.ingredients
        recipe.save()

        clear_cache('/recipes') # clears old cache data when updated
        return recipe_schema.dump(recipe).data, HTTPStatus.OK

    @jwt_required
    def delete(self,recipe_id):
        """
        :param

        """
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message':'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message':'Access is no allowed'},HTTPStatus.FORBIDDEN
        recipe.delete()

        clear_cache('/recipes') # clears old cache data when updated
        return {},HTTPStatus.NO_CONTENT

class RecipePublishResource(Resource):
    @jwt_required
    def put(self,recipe_id):
        """

        :param

        """


        recipe = Recipe.get_by_id(recipe_id =recipe_id)
        if recipe is None:
            return {'message':'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message':'Access is not allowed'}, HTTPStatus.FORBIDDEN
        recipe.is_publish = True
        #recipe.is_publish = True
        recipe.save()

        clear_cache('/recipes') # clears old cache data when updated
        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self,recipe_id):
        """
        :param

        """

        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id),None)

        if recipe is None:
            return {'message':'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_pubish = False

        clear_cache('/recipes') # clears old cache data when updated
        return {},HTTPStatus.NO_CONTENT

class RecipeListResource(Resource):

    decorators = [limiter.limit('2 per minute', methods=['GET'], error_message='Too Many Requests')]

    # Default value for the page parameter is 1
    # Default value for the per_page parameter is 20.
    # If nothing is passed we will be getting the first page
    # with the first 20 records

    @use_kwargs({'q':fields.Str(missing=''),
                 'page':fields.Int(missing=1),
                 'per_page': fields.Int(missing=20),
                 'sort':fields.Str(missing='created_at'),
                 'order':fields.Str(missing='desc')})

    @cache.cached(timeout=60,query_string=True) # True means that it allows passing in of arguments
    def get(self,q,page,per_page,sort,order):
        """
        Passes three arguments in the get_all_published method
        and gets the pagination object back. returns the
        paginated recipes as serialized and back to front
        end client. The q parameter passed the search string into the API
        """
        print('Querying database')
        if sort not in['created_at','cook_time','num_of_servings']:
            sort = 'created_at'
        if order not in ['asc','desc']:
            order = 'desc'

        paginated_recipes = Recipe.get_all_published(q,page,per_page,sort,order)
        return recipe_pagination_schema.dump(paginated_recipes).data,HTTPStatus.OK

    @jwt_required
    def post(self):
        """:param

        """
        json_data = request.get_json()
        current_user = get_jwt_identity()

        data, errors = recipe_schema.load(data=json_data)
        if errors:
            return {'message':"Validation Errors",'errors':errors},HTTPStatus.BAD_REQUEST

        recipe = Recipe(**data)
        recipe.user_id = current_user
        recipe.save()

        return recipe_schema.dump(recipe),HTTPStatus.CREATED


class RecipeCoverUploadResource(Resource):
    @jwt_required               # states that the method can only be called after user has logged in.
    def put(self,recipe_id):
        """
        Gets the cover image in request.files
        and verifies whether it exists and if the file
        extension is permitted
        """
        file = request.files.get('cover')
        if not file:
            return {'message':'Not a valid image'}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file,file.filename):
            return {'message':'File type not allowed'}, HTTPStatus.BAD_REQUEST

        # Check whether user hs the right to modify the recipe
        recipe = Recipe.get_by_id(recipe_id = recipe_id)

        if recipe is None:
            return {'message':'Recipe not found'},HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message':'Access in not allowed'},HTTPStatus.FORBIDDEN

        # If the user has the right to, we will go
        # ahead and modify the cover image of the recipe
        if recipe.cover_image:
            cover_path = image_set.path(folder = 'recipes',
                                        filename = recipe.cover_image)
            if os.path.exists(cover_path):
                os.remove(cover_path)

        # User the save_image function to save the uploaded image
        filename = save_image(image=file,folder = 'recipes')

        recipe.cover_image = filename
        recipe.save()
        clear_cache('/recipes') # clears old cache data when updated
        return recipe_cover_schema.dump(recipe).data,HTTPStatus.OK



