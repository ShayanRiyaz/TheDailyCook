from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet,IMAGES
from flask_caching import Cache

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(key_func =get_remote_address) # get_remote_address will return the IP address for the current request.
cache = Cache()
db = SQLAlchemy()
jwt = JWTManager()
image_set = UploadSet('images',IMAGES)


