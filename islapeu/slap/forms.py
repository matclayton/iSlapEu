from django import forms 
from google.appengine.ext.db import djangoforms
from slap.models import Slap 
import twitter
import logging
import re
    
class FullSlapForm(djangoforms.ModelForm):  
    reason = forms.CharField(widget=forms.widgets.Textarea(attrs={'maxLength':'140'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(), required=False)
    
    def __init__(self, data, request, slapee=None):
        self.request = request
        self.slapee = slapee
        return super(FullSlapForm, self).__init__(data)
    
    def clean_slapee(self):
        if self.slapee:
            data=self.slapee
        else:
            data = self.cleaned_data['slapee']
        if not re.match('^[a-zA-Z0-9_]+$', data):
            raise forms.ValidationError('Not a valid Twitter Username')
        return data
    
    def clean_reason(self):
        data = self.cleaned_data['reason']
        if len(data)>140:
            raise forms.ValidationError('Must not exceed 140 characters')
        return data
    
    def clean(self):   
        # Set old credentials are if in the session 
        if self.request.session.get('username', False):
            username = self.cleaned_data['slaper'] = self.request.session.get('username')
            password = self.cleaned_data['password'] = self.request.session.get('password')
            api=twitter.Api(username=username, password=password)
            verify = api.VerifyCredentials(no_cache=False)
        else:
            username = self.cleaned_data.get('slaper')
            password = self.cleaned_data.get('password')
            api=twitter.Api(username=username, password=password)               
            verify = api.VerifyCredentials()     
        
        if verify: 
            slapee = self.cleaned_data.get('slapee')
            msg = 'twitslapped @%s because %s - slap back at http://www.islap.eu/%s/' % (slapee, reason, slapee)
            if len(msg)>140:
                msg = 'twitslapped @%s because %s... - slap back at http://www.islap.eu/%s/' % (slapee, reason[0:len(reason)-(len(msg)+3-140)], slapee)
            status = api.PostUpdate(msg)
            
            msg = 'I just twitslapped you because %s - slap back at http://www.islap.eu/%s/' % (reason, slapee)
            if len(msg)>140:
                msg = 'I just twitslapped you because %s... - slap back at http://www.islap.eu/%s/' % (reason[0:len(reason)-(len(msg)+3-140)], slapee)
            status = api.PostDirectMessage(slapee, msg)
            
            self.cleaned_data['slaper_image_url'] = verify['profile_image_url']
        else:
            raise forms.ValidationError('Invalid Username and Password')
        return self.cleaned_data
              
    class Meta:
        model = Slap
        exclude = ['created_at', 'slaper_image_url']