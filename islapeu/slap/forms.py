from django import forms 
from google.appengine.ext.db import djangoforms
from slap.models import Slap 
import twitter
import logging
import re
    
class UserSlapForm(djangoforms.ModelForm):  
    class Meta:
        model = Slap
        exclude = ['created_at', 'slapee']
    
class FullSlapForm(djangoforms.ModelForm):  
    password = forms.CharField(widget=forms.widgets.PasswordInput(), required=False)
    
    def __init__(self, data, request):
        self.request = request
        return super(FullSlapForm, self).__init__(data)
    
    def clean_slapee(self):
        data = self.cleaned_data['slapee']
        if not re.match('^[a-zA-Z0-9_]+$', data):
            raise forms.ValidationError('Not a valid Twitter Username')
        return data
    
    def clean(self):   
        # Set old credentials are if in the session 
        if self.request.session.get('username', False):
            self.cleaned_data['slaper'] = self.request.session.get('username')
            self.cleaned_data['password'] = self.request.session.get('password')
            
        username = self.cleaned_data.get('slaper')
        password = self.cleaned_data.get('password')
            
        api=twitter.Api(username=username, password=password)    
        verify = api.VerifyCredentials()     
        if verify: 
            status = api.PostUpdate('2')
            self.cleaned_data['slaper_image_url'] = verify['profile_image_url']
        else:
            raise forms.ValidationError('Invalid Username and Password')
        logging.error(self.cleaned_data)
        return self.cleaned_data
              
    class Meta:
        model = Slap
        exclude = ['created_at', 'slaper_image_url']