from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from slap.forms import FullSlapForm, UserSlapForm
from slap.models import Slap
from django.conf import settings
import logging
import twitter


def home(request):  
    form = FullSlapForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    return render_to_response('home.html', {'form' : form } , context_instance=RequestContext(request))

def slap(request, username):
    
    api = twitter.Api()
    user = api.GetUser(username)
    
    form = UserSlapForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():     
        slap = form.save(commit=False)
        slap.slapee = username
        slap.put()
             
    page_size = settings.SLAPS_PER_PAGE
    next = None
    slaps = Slap.all().order("-created_at").filter('slapee ==', username).fetch(page_size+1)
    if len(slaps) == page_size+1:
        next = slaps[-1].when
        slaps = slaps[:page_size]

    return render_to_response('slap.html', {'form' : form, 'slaps':slaps, 'user':user } , context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def terms(request):
    return render_to_response('terms.html', context_instance=RequestContext(request))
