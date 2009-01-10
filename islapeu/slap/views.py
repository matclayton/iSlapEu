from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))


def slap(request):
    return render_to_response('slap.html', context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
