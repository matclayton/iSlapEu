from django import forms 
from google.appengine.ext.db import djangoforms
from slap.models import Slap 
import twitter

#class FullSlapForm(forms.Form):
 #   reason = forms.CharField(max_length=160)
#    slaper = forms.CharField()
#    slapee = forms.CharField()
#    password = forms.CharField()
    
class UserSlapForm(djangoforms.ModelForm):  
    class Meta:
        model = Slap
        exclude = ['created_at', 'modified_at', 'slapee']
    
class FullSlapForm(djangoforms.ModelForm):  
    password = forms.CharField(widget=forms.widgets.PasswordInput())
    
    def clean(self):
        cleaned_data = self._get_cleaned_data
        username = self.cleaned_data.get('slaper')
        password = self.cleaned_data.get('password')
        
        try:
            api = twitter.Api(username=username, password=password)  
            status = api.PostUpdate('testing')
        except:
            forms.ValidationError('Invalid Username and Password')
              
    class Meta:
        model = Slap
        exclude = ['created_at', 'modified_at']