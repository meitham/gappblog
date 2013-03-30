from google.appengine.ext import db


RATING_CHOICES = ('Poor', 'OK', 'Good', 'Very Good', 'Great')


class Article(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    published = db.BooleanProperty(default=False)
    published_date = db.DateTimeProperty(auto_now=True)


class Comment(db.Model):
    article = db.ReferenceProperty(Article, collection_name='comments')
    author = db.UserProperty()
    text = db.TextProperty()
    rating = db.StringProperty(choices=RATING_CHOICES, default='Great')
    posted_on = db.DateTimeProperty(auto_now_add=True)
