from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

class User(auth_models.User):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
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
  skills_count = ndb.IntegerProperty(default = 0)
  avatar =  ndb.BlobProperty()
  email_address = ndb.StringProperty()
  subscriptions = ndb.StringProperty(repeated=True)

class Comment(ndb.Model):
  sender = ndb.StringProperty()
  recipient = ndb.StringProperty()
  text = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
  vote_count = ndb.IntegerProperty(default = 0)
  root = ndb.BooleanProperty(default = True)
  parent = ndb.KeyProperty()
  children = ndb.KeyProperty(kind="Comment", repeated=True)
  offset = ndb.IntegerProperty(default = 0)

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
  url_host = ndb.StringProperty()
  title = ndb.StringProperty()
  author = ndb.StringProperty()
  reference = ndb.StringProperty()
  vote_count = ndb.IntegerProperty(default = 0)
  comment_count = ndb.IntegerProperty(default = 0)
  time = ndb.DateTimeProperty(auto_now_add=True)
  text = ndb.StringProperty()
  categories = ndb.KeyProperty(kind= "Skill", repeated=True)
  up_voters = ndb.KeyProperty(kind = "User", repeated=True)
  down_voters = ndb.KeyProperty(kind = "User", repeated=True)

class Forum(ndb.Model):
  name = ndb.StringProperty()
  posts = ndb.IntegerProperty()
  subscribers = ndb.KeyProperty(kind = "User", repeated=True)

class Skill(ndb.Model):
  name = ndb.StringProperty()




