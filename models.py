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
  message_count = ndb.IntegerProperty(default = 0)
  request_count = ndb.IntegerProperty(default = 0)

class Comment(ndb.Model):
  sender = ndb.StringProperty()
  recipient = ndb.StringProperty()
  text = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)

class Message(ndb.Model):
  sender = ndb.StringProperty()
  recipient = ndb.StringProperty()
  text = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)

class ConnectionRequest(ndb.Model):
  requestor = ndb.StringProperty()
  requestee = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
  text = ndb.StringProperty()

