# -*- coding: utf-8 -*-
from django.shortcuts import (render_to_response,
                              RequestContext,
                              HttpResponseRedirect,)
from django.core.urlresolvers import reverse
from locking_tools import get_message, put_message


def decode_url(url):
    return url.replace('_', ' ')


def encode_url(title):
    return title.replace(' ', '_')


def get_menu():
    class MenuItem(object):
        def __init__(self, name):
            self.name = name
            self.url = encode_url(name)

        def __unicode__(self):
            return self.name.capitalize()

    items = ('home',)
    menu = (MenuItem(item) for item in items)

    return tuple(menu)

MENU = get_menu()


def index(request):
    print 'INDEX'
    context = RequestContext(request)
    video_url = reverse(video)

    return render_to_response('index.html',
                              {'menu': MENU,
                               'video_url': video_url},
                              context)


def video(request):
    print 'VIDEO'
    access = get_message()

    if not access:
        return HttpResponseRedirect(reverse(busy))

    context = RequestContext(request)
    stop_url = reverse(stop)

    return render_to_response('video.html', {'stop_url': stop_url}, context)


def busy(request):
    context = RequestContext(request)
    try_again_url = reverse(video)

    return render_to_response('busy.html',
                              {'try_again_url': try_again_url,
                               'menu': MENU},
                              context)


def stop(request):
    print 'STOP'
    put_message()

    return HttpResponseRedirect(reverse(index))