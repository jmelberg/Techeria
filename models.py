from google.appengine.ext import ndb

class User(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()
  friends = ndb.KeyProperty(kind= "User", repeated=True)
  skills = ndb.StringProperty(repeated=True)
  profession = ndb.StringProperty()
  employer = ndb.StringProperty()
  major = ndb.StringProperty()
  grad_year = ndb.IntegerProperty()
  activated = ndb.BooleanProperty()
