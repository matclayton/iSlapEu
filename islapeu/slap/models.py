from appengine_django.models import BaseModel
from google.appengine.ext import db
from counter import *

class Slap(BaseModel):
    
    def put(self):
        # Increment Sharded Counters
        increment('total')
        increment('slaps_given_%s' % self.slaper)
        increment('slaps_received_%s' % self.slapee)
        return super(Slap, self).save()
    
    slaper = db.StringProperty(multiline=False)
    slapee = db.StringProperty(multiline=False)
    
    reason = db.StringProperty(multiline=True)  
    slaper_image_url = db.StringProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
