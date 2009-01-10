from django import forms 
from google.appengine.ext.db import djangoforms
from slap.models import Slap 

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
    class Meta:
        model = Slap
        exclude = ['created_at', 'modified_at']