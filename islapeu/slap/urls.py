# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *
from slap.views import *

urlpatterns = patterns('',
    # Example:
    url(r'^$', home, name='home' ),
    url(r'^about/$', about, name='about' ),
    url(r'^terms/$', terms, name='terms' ),
    url(r'^logout/$', logout, name='logout' ),
    url(r'^count/$', count, name='count' ),
    url(r'^count_ajax/$', count_ajax, name='count_ajax' ),
    url(r'^testerror/$', error, name='error' ),
    url(r'^(?P<username>[-\w]+)/$', slap, name='slap' ),
)
