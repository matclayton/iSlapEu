from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from slap.forms import FullSlapForm
from slap.models import Slap
from django.conf import settings
from slap.counter import *
import logging
import twitter

def home(request):     
    form = FullSlapForm(data=request.POST or None, request=request)
    if request.method == 'POST' and form.is_valid():
        form.save()
        #Save Username and Password into Session
        if not request.session.get('username',False):
            request.session['username'] = request.POST['slaper']
            request.session['password'] = request.POST['password']
            
        return HttpResponseRedirect(reverse(slap, args=[request.POST['slapee']]))

    slap_count = get_count('total') 
    return render_to_response('home.html', {'form' : form, 'slap_count': slap_count } , context_instance=RequestContext(request))

def logout(request):
    try:
        del request.session['username']
        del request.session['password']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse(home))  

def slap(request, username):    
    form = FullSlapForm(data=request.POST or None, request=request, slapee=username)
    if request.method == 'POST' and form.is_valid():
        slap = form.save(commit=False)
        slap.slapee = username
        slap.put()
        
        #Save Username and Password into Session
        if not request.session.get('username',False):
            request.session['username'] = request.POST['slaper']
            request.session['password'] = request.POST['password']
        
        #Load in Cleared form.
        form = FullSlapForm(None, request=request)    
            
    api=twitter.Api()
    user = api.GetUser(username)
    slapee_image_url = user.profile_image_url
           
    page_size = settings.SLAPS_PER_PAGE
    next = None
    slaps = Slap.all().order("-created_at").filter('slapee ==', username).fetch(page_size+1)
    if len(slaps) == page_size+1:
        next = slaps[-1].created_at
        slaps = slaps[:page_size]
        
    slap_count = get_count('total') 
    slapee_count = get_count('slaps_received_%s' % username)
    return render_to_response('slap.html', {'form' : form, 'username':username, 'slapee_image_url': slapee_image_url , 'slaps':slaps, 'slap_count': slap_count, 'slapee_count': slapee_count } , context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def count(request):
    slap_count = get_count('total')
    return render_to_response('count.html', {'slap_count' : slap_count }, context_instance=RequestContext(request))

def count_ajax(request):
    slap_count = get_count('total')
    return render_to_response('count_ajax.html', {'slap_count' : slap_count })

def terms(request):
    return render_to_response('terms.html', context_instance=RequestContext(request))

def error(request):
    error = 1/0
    return render_to_response('terms.html', context_instance=RequestContext(request))