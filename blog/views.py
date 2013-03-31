import logging
import functools
from datetime import datetime

from django import template
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import PermissionDenied
from django.conf import settings

from google.appengine.ext import db

from google.appengine.api import users

from rfc3339 import rfc3339

from .forms import EntryForm
from .models import Entry


logger = logging.getLogger('blog')

def staff_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = users.get_current_user()
        request = args[0]
        if not user:
            if request.method == "GET":
                return HttpResponseRedirect(users.create_login_url(request.path))
            raise PermissionDenied
        elif not users.is_current_user_admin():
            raise PermissionDenied
        else:
            return func(*args, **kwargs)
    return wrapper


def home(request):
    entries = db.Query(Entry).order('-pub_date').filter('is_public =', True).fetch(limit=5)
    return render_to_response('blog/index.html',
                              {'entries': entries},
                              template.RequestContext(request))


@staff_only
def edit_entry(request, a_slug=None):
    author = users.get_current_user()
    if request.method == 'POST':
        # The form was submitted.
        if a_slug:
            # Fetch the existing article and update it from the form.
            entry = Entry.gql("where slug=:1", a_slug).get()
            form = EntryForm(request.POST, instance=entry)
        else:
            # Create a new article based on the form.
            form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = author
            entry.put()
            return HttpResponseRedirect('/')
        # else fall through to redisplay the form with error messages
    else:  # GET
        # The user wants to see the form.
        if a_slug:
            # Show the form to edit an existing article.
            entry = Entry.gql("where slug=:1", a_slug).get()
            form = EntryForm(instance=entry)
        else:
            # Show the form to create a new article.
            form = EntryForm()
    return render_to_response('blog/edit_entry.html',
                              {
                                  'slug': a_slug,
                                  'form': form,
                                  },
                              template.RequestContext(request))

def display_entry(request, slug):
    entry = db.Query(Entry).filter("slug =", slug).get()
    return render_to_response('blog/display_entry.html',
                              { 'entry': entry },
                              template.RequestContext(request))



def archive(request, year=None, month=None, day=None):
    entries = db.Query(Entry).order('-pub_date').filter('is_public =', True)
    return render_to_response('blog/archives.html',
                              {'entries': entries},
                              template.RequestContext(request))


def atom(request):
    entries = db.Query(Entry).order('-pub_date').filter('is_public =', True)
    logger.debug(entries.count())
    return render_to_response('blog/atom_feed.html',
                              {
                                  'entries': entries,
                                  'updated': rfc3339(datetime.now(), utc=True)
                               },
                              template.RequestContext(request),
                              mimetype = "application/atom+xml"
                              )


