try:
    from google.appengine.ext.db import djangoforms
except ImportError:
    from .utils import djangoforms

from .models import Entry, Comment


class EntryForm(djangoforms.ModelForm):
    class Meta:
        model = Entry

