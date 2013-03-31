import logging
from rfc3339 import rfc3339
from docutils.core import publish_parts

from google.appengine.ext import db

from django.conf import settings
from django.core.urlresolvers import reverse


RATING_CHOICES = ('Poor', 'OK', 'Good', 'Very Good', 'Great')

logger = logging.getLogger('blog')

ATOM_TEMPLATE= """
<entry>
    <title>{title}</title>
    <link href="{url}" />
    <id>{id}</id>
    <summary>{summary}</summary>
    <updated>{updated}</updated>
</entry>
"""

class Entry(db.Model):
    author = db.UserProperty()
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    summary = db.TextProperty()
    body = db.TextProperty(required=True)
    pub_date = db.DateTimeProperty(auto_now_add=True)
    is_public = db.BooleanProperty(default=False)
    updated = db.DateTimeProperty(auto_now=True)


    def render_body(self):
        parts = publish_parts(source=self.body, writer_name='html4css1',
                              settings_overrides={'_disable_config': True})
        return parts['fragment']

    def render_summary(self):
        parts = publish_parts(source=self.summary, writer_name='html4css1',
                              settings_overrides={'_disable_config': True})
        return parts['fragment']

    @property
    def link(self):
        return reverse('blog.views.display_entry', args=(self.slug,))

    @property
    def atom(self):
        atom = ATOM_TEMPLATE.format(title=self.title,
                                    url=''.join(['http://', settings.HOSTNAME, self.link]),
                                    id=self.slug,
                                    summary=self.render_summary(),
                                    updated=rfc3339(self.updated, utc=True))
        return atom


class Comment(db.Model):
    Entry = db.ReferenceProperty(Entry, required=True,
                                 collection_name='comments')
    author = db.UserProperty(required=True)
    body = db.TextProperty(required=True)
    rating = db.StringProperty(choices=RATING_CHOICES, default='Great')
    pub_date = db.DateTimeProperty(auto_now_add=True)
