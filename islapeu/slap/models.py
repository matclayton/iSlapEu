from appengine_django.models import BaseModel
from google.appengine.ext import db

class User(BaseModel):
    username = db.StringProperty()
    password = db.StringProperty()
    
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)

class Slap(BaseModel):
    slaper = db.StringProperty(multiline=False, required=True)
    slapee = db.StringProperty(multiline=False, required=True)
    
    slaper_image_url = db.StringProperty()

    reason = db.StringProperty(multiline=True)

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
