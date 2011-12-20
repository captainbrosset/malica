from google.appengine.ext import db

class Present(db.Model):
    title = db.StringProperty(required=True)
    url = db.StringProperty()
    approximatePrice = db.IntegerProperty()
    user = db.StringProperty(required=True)
    image = db.StringProperty()
    dateAdded = db.DateTimeProperty(auto_now_add=True)
    imageFixed = db.BooleanProperty(default=False)

class PresentCounter(db.Model):
    count = db.IntegerProperty(required=True)
