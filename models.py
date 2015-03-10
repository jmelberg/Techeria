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
  friend_count = ndb.IntegerProperty(default=0)
  message_count = ndb.IntegerProperty(default = 0)
  request_count = ndb.IntegerProperty(default = 0)
  skills = ndb.KeyProperty(kind = "Skill", repeated=True)

class Comment(ndb.Model):
  sender = ndb.StringProperty()
  recipient = ndb.StringProperty()
  text = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
  vote_count = ndb.IntegerProperty(default = 0)

class Message(ndb.Model):
  sender = ndb.StringProperty()
  recipient = ndb.StringProperty()
  subject = ndb.StringProperty()
  text = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)

class ConnectionRequest(ndb.Model):
  requestor = ndb.StringProperty()
  requestee = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
  text = ndb.StringProperty()

class ForumPost(ndb.Model):
  forum_name = ndb.StringProperty()
  url = ndb.StringProperty()
  title = ndb.StringProperty()
  author = ndb.StringProperty()
  reference = ndb.StringProperty()
  vote_count = ndb.IntegerProperty(default = 0)
  comment_count = ndb.IntegerProperty(default = 0)
  time = ndb.DateTimeProperty(auto_now_add=True)
  text = ndb.StringProperty()
  categories = ndb.KeyProperty(kind= "Skill", repeated=True)

class Skill(ndb.Model):
  name = ndb.StringProperty()




