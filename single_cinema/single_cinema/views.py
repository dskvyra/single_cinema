# -*- coding: utf-8 -*-
from django.shortcuts import (render_to_response,
                              RequestContext,
                              HttpResponseRedirect,)
from django.core.urlresolvers import reverse
from locking_tools import get_message, put_message


def crypt(key):
    salt = 42

    return hash(key) + salt


def decode_url(url):
    return url.replace('_', ' ')


def encode_url(title):
    return title.replace(' ', '_')


def get_menu(items):
    class MenuItem(object):
        def __init__(self, name):
            self.name = name
            self.url = encode_url(name)

        def __unicode__(self):
            return self.name.capitalize()

    menu = (MenuItem(item) for item in items)

    return tuple(menu)


MENU = get_menu(('home',))


def index(request):
    return render_to_response('index.html',
                              {'menu': MENU,
                               'video_url': reverse(video)},
                              RequestContext(request))


def video(request):
    access = get_message()

    if not access:
        return HttpResponseRedirect(reverse(busy))

    stop_url = reverse(stop, args=(crypt(request.session.session_key),))

    return render_to_response('video.html',
                              {'stop_url': stop_url},
                              RequestContext(request))


def busy(request):
    return render_to_response('busy.html',
                              {'try_again_url': reverse(video),
                               'menu': MENU},
                              RequestContext(request))


def stop(request, key=''):
    if int(key) == crypt(request.session.session_key):
        put_message()

    return HttpResponseRedirect(reverse(index))