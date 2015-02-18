from google.appengine.ext import ndb

class User(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()
  username = ndb.StringProperty()
  friends = ndb.KeyProperty(kind= "User", repeated=True)
  profession = ndb.StringProperty()
  employer = ndb.StringProperty()
  major = ndb.StringProperty()
  grad_year = ndb.IntegerProperty()
  activated = ndb.BooleanProperty()

class Comment(ndb.Model):
  sender = ndb.StringProperty()
  recipient = ndb.StringProperty()
  text = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
