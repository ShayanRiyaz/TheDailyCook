# The Daily Cook

**Currently in Progess** 

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




## Process
[To be added]



## Future
- Switch to MongoDB.
- Add Recipe Book service.

## Book
Python API Development Fundamentals
https://www.amazon.com/Python-API-Development-Fundamentals-application/dp/1838983996
