![The Daily Cook](assets/README_cover.jpg)

# The Daily Cook


## About the Project
In order to practically apply my understanding of API's I'm currently working on a simple Recipe Logging Website that I call the daily cook. The focus of this project is to understand REST API's better and be able to visualize and map out a user based application.

- Building a proper end to end website that allows user to:
	- Log In with verification. [Mailgun]
	- Hashing passwords         [SHA-256] 
	- Creating a log that users can add to (Recipes).   
	- Access Tokens
	- Object Serialization/De-Serialization.
	- Working with Images
- Using CRUD Method to verify storage 
- Testing APIs using Postman.
**Pending**
Deploy app on heroku.

## Instructions to run
```python app.py```

## Applications used:
- PostgreSQL (pgadmin)
- Postman API


|  Libraries        | Version  | Usage                                      |
|-------------------|----------|--------------------------------------------|
|Flask              |1.0.3     | Main Framework for Web Application         |
|Flask-RESTful      |0.3.7     | Works with ORM libraries                   |
|httpie             |1.0.3     | HTTP client in order to test our APIs      |
|Flask-SQLAlchemy   |2.4.0     |-                                           |
|Flask-Migrate      |2.5.2     |-                                           |
|psycopg2-binary    |2.8.3     |-                                           |
|passlib            |1.7.1     |-                                           |
|Flask-JWT-Extended |3.20.0    |-                                           |
|marshmallow        |2.19.5    | Serializing/Deserializing                  |
|webargs            |5.4.0     |-                                           |
|itsdangerous       |1.1.0     |-                                           |
|Flask-Uploads       |0.2.1    | Uploading Image Avatar to the user profile | 
|Pillow             |7.1.0     | Refactoring and compressing images         |
|Flask-Limiter|1.0.1||
|gunicorn           |19.9.0| |
|Werkzeug|0.15.6||



# Process
## Virual Environment set up

## Creating a Recipe Model

1. Define API endpoint for recipe model.
2. Defining Recipe Resource
3. Publishing and Unpublishing

## Create app.py.

1. Make HTTP Request Tests using Postman.
2. SQLAlchemy and PostgreSQL to set up database.
    1. Understand ORM
    2. Define models
    3. Password Hashing

## Add Authentication and Security with JWT.

1. What is JWT?

JWT is used for user authentication and is passed between the user and the server. The full definition of the acronym is JSON WebToken.
It works by encoding the user identity and sign it digitally, making it an unforgeable token that identifies the user, and the application can later control access for the user based on their identity.

2. Flask-JWT-Extended

3. Design methods in the recipe model.

4. Refresh Tokens

5. User Logout Mechanism

## Serializing objects with Marshmallow

1. What is Marshmallow?

it is a package for serialization and deserialization in Python. It also provides validation features.

- Developers can define Schemas. which can be used to represent a field in various ways (required and validation) and automatically perform validation during deserialization.
- We will be defininf a data validation function

2. What is a Schema class in Marshmallow.?

This allows us to specify fields for the objects that we want to serialize/ deserialize.

```python
# Example
from marshmallow import Schema, fields

class SimpleSchema(Schema):
	id = fields.Int()
	username = fields.String()
```

3. User Schema Design

Use Marshmallow to Validate User Data.

```python
# schemas/user.py
from marshmallow import Schema, fields
from utils import hash_password
class UserSchema(Schema):
...

# resource/user.py
from schemas.user import UserSchema
user_schema = UserSchema()
user_public_schema = UserSchema(exclude = ('email',))

# Modify UserListResource()
def post(self):
	...
	data,errors = user_schema_lost(data= json_data)
```

4. Recipe Schema Design

```python

```

## Email Configuration using mailgun

## Working with images

1. Flask uploads
2. Pillow

## Pagination

What is pagination and why do we need it. 

### What is pagination and Why do we need it.

In testing environment, we may only have a few developers putting recipes on the The Daily Cook platform. THere are only a handful of recipes there and performance is never a concert. However,in production environments (after launch). There could be 1000's of user sharing recipes on the platform. If we consider social media platforms, such as FB, the volune will be even bigger.

This is why we use pagination. **Pagination** means instead of querying the whole population of records from the database, we just query a handful of them. When the user wants to see more, the can always go to the next page.

*Example:*

When we are browsing a shopping site, usually we will view the items for sale a page at a time. Each page may display 40 items, and we have to navigate to subsequent pages to view all the items that are available. *This is the nature of pagination*

The number of records that are shown per page is limited by the page's size. This way there will be a huge saving in server loading time and data transfer time and most importantly it will enhance user's navigation experience.

### What are Paginated API's

This means that when we query the API, onl the data records on the current page will be returned, this also includes other information such as the total number of records, the total number of pages, links to other pages and so on.

**Advantage**: We are using a Web Framework to build our API, which makes it very easy to implement. We will use Flask-SQLAlchemy to help us build a paginated API.

*Example response in JSON format*

```json
{ 
"links": { 
		"first": "http://localhost:5000/recipes?per_page=2&page=1", 
"last": "http://localhost:5000/recipes?per_page=2&page=5", 
"prev": "http://localhost:5000/recipes?per_page=2&page=1", 
"next": "http://localhost:5000/recipes?per_page=2&page=3" 
}, 
"page": 2, 
"pages": 5, 
"per_page": 2,
"total": 9,
 "data": [ 
		{ 
		"data": "data" 
		},
		{ 
		"data": "data" 
		} 
	] 
}

```

Here we can see the following attributes in the HTTP Response:

**first, last, prev, next, page, pages, per_page, total, data**

## Searching

A better way to look for a recipe is by searching. The search function is an essential function on the internet. 

In our program we implement a simple search function. We built a recipe searching API that allows the client to provide a *q* parameter to search for recipe recipes by name or recipe description. This can be done by using the I*LIKE*  comparison operator. TheI I*LIKE*  operator works by matching the search string to the target, it is case insensitive. We will also use the similar to method.  

## Sorting and Ordering

This is another important feature that helps user navigation. ALWAYS KEEP USER EXPERIENCE IN MIND. 

Previously, the recipes we sent back were sorted by time by default. Let's implement some other sorting criteria. We can still keep the default sorting critera such as time, but we want to allow the user to define the searching criteria they want; for example, they can specify that they want the recipes to be sorted by cooking time. This is a possibility as the user may want to cook a quick meal, which means that they will only be interested in recipes with short cooking times.

- We can add the *sort* and *order* parmeters to **created_at, cook_time or num_of_servings.**

## Adding more features

We will add the cache function, which will temporarily save data to the application memory. This will allow us to save the time required to query the database every time. This can greatly improve performance and reduce the server burden. There is a Flask extension package, Flask-Caching, that can help us in implementing this function in our Daily Cook application.

Besides caching, we will implement a rate-limiting function. This will prevent certain high-usage users from jeopardizing the whole system by limiting their usage. Ensuring fair usage of our APIs is crucial to guarantee service quality. We will be using a Flask extension package, **Flask-Limiter**.

These two caching and rate limiting functions are very common and powerful in real-world scenarios. 

### Caching to improve API performance and efficiently get the last information

Caching means storing data in a temporary space (a cache) so that it can be retrieved faster in subsequent requests. The temporary space can be application memory, server hard disk space, or something else. **The whole purpose of caching is to lighted the workload by avoiding process for querying the data again.**

*for sever-level caching, most of the time, the cache is stored in the same web server as the application. Technically speaking, it can be stored in another server as well (for example. Redis (Remote Dictionairy Server) or Memcached (a high-performance distributed cached memory))*

### Benefit of Caching and Flask-Caching

Through caching along with reducing the volume of the data transferred we can also improve the overall performance. This is done by reducing the bandwidth required, reducing the server loading time and more.

Flask-Caching is a Flask-extension package that allows us to easily implement caching functionality. 

*Imagine a cache as a dictionary object that contains key-value pairs. The key is here used to specify the resource to cache, where as the value is used to store the actual data to be cached.* 

**Add the cache function to the The Daily Cook application using the Flask-Caching package.**

### Implement rate-limiting functionality to an API

What is API Limiting?

When we provide an API service, we need to ensure fair usage for every user so that the system resources are effectively and fairly serving all. We want to make sure that majority users are getting good performance; therefore we apply restrictions. 

*By limiting a small number of high traffic users, we can make sure that the majority of users are satisfied.*

*The way to approach this is to set a limit per user. For example:*

we can limit a small number of requests per user to be no more than 100 per second. This number will be enough for the normal usage of our API.



## Future
- Switch to MongoDB.
- Add Recipe Book service.

## Book
[Python API Development Fundamentals](https://www.amazon.com/Python-API-Development-Fundamentals-application/dp/1838983996)
