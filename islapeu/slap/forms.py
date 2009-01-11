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
        cleaned_data = self.cleaned_data   
        
        username = self.cleaned_data.get('slaper')
        password = self.cleaned_data.get('password')
        
        api=twitter.Api(username=username, password=password)
        verify = api.VerifyCredentials()
            
        if verify: 
            status = api.PostUpdate('Sorted!')
            self.cleaned_data['slaper_image_url'] = verify['profile_image_url']
        else:
            raise forms.ValidationError('Invalid Username and Password')
                
        return cleaned_data
              
    class Meta:
        model = Slap
        exclude = ['created_at', 'modified_at', 'slapee_image_url', 'slaper_image_url']