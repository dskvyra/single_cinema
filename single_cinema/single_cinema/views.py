# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from locking import Queue, Mutex

queue = Queue()
mutex = Mutex()


def decode_url(url):
    """ Takes url string, returns title string with spaces instead underlines """
    return url.replace('_', ' ')


def encode_url(title):
    """ Takes title string, swaps spaces by underlines and returns url string """
    return title.replace(' ', '_')


def get_menu():
    class MenuItem(object):
        def __init__(self, name):
            self.name = name
            self.url = encode_url(name)

        def __unicode__(self):
            return self.name.capitalize()

    class Menu(dict):
        def __init__(self, menu_item):
            super(Menu, self).__init__()
            self[menu_item.name] = menu_item.url

    items = ('home',)
    menu = (MenuItem(item) for item in items)

    return menu


def index(request):
    context = RequestContext(request)
    video_url = 'video'
    menu = get_menu()

    return render_to_response('index.html',
                              {'menu': menu,
                               'video_url': video_url},
                              context)


def video(request):
    if mutex.busy:
        return HttpResponseRedirect('/busy')

    context = RequestContext(request)
    stop_url = 'stop'
    owner = request.COOKIES.get('sessionid')

    mutex.aquire(owner)

    return render_to_response('video.html', {'stop_url': stop_url}, context)


def busy(request):
    context = RequestContext(request)
    try_again_url = 'video'

    return render_to_response('busy.html',
                              {'try_again_url': try_again_url},
                              context)


def stop(request):
    owner = request.COOKIES.get('sessionid')

    mutex.release(owner)

    return HttpResponseRedirect('index')