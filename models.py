from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

class User(auth_models.User):
  first_name = ndb.StringProperty()
  lower_first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  lower_last_name = ndb.StringProperty()
  username = ndb.StringProperty()
  email_address = ndb.StringProperty()
  account_type = ndb.StringProperty()
  profession = ndb.StringProperty()
  lower_profession = ndb.StringProperty()
  employer = ndb.StringProperty()
  lower_employer = ndb.StringProperty()
  activated = ndb.BooleanProperty()
  friends = ndb.KeyProperty(kind= "User", repeated=True)
  friend_count = ndb.IntegerProperty(default=0)
  message_count = ndb.IntegerProperty(default = 0)
  request_count = ndb.IntegerProperty(default = 0)
  skills = ndb.KeyProperty(kind = "Skill", repeated=True)
  skills_count = ndb.IntegerProperty(default = 0)
  avatar =  ndb.BlobProperty()
  subscriptions = ndb.StringProperty(repeated=True)

class Comment(ndb.Model):
  sender_key = ndb.KeyProperty()
  recipient_key = ndb.KeyProperty()
  sender = ndb.StringProperty()
  recipient = ndb.StringProperty()
  text = ndb.TextProperty()
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
  text = ndb.TextProperty()
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
  text = ndb.TextProperty()
  categories = ndb.KeyProperty(kind= "Skill", repeated=True)
  up_voters = ndb.KeyProperty(kind = "User", repeated=True)
  down_voters = ndb.KeyProperty(kind = "User", repeated=True)

class Forum(ndb.Model):
  name = ndb.StringProperty()
  posts = ndb.IntegerProperty()
  subscribers = ndb.KeyProperty(kind = "User", repeated=True)

class Skill(ndb.Model):
  name = ndb.StringProperty()

class Endorsement(ndb.Model):
  endorsers = ndb.KeyProperty(kind="User", repeated=True)
  endorsee = ndb.KeyProperty() 
  skill = ndb.KeyProperty(kind="Skill")
  endorsement_count = ndb.IntegerProperty(default = 0)

class AccessToken(ndb.Model):
  token = ndb.StringProperty()
  granted = ndb.DateTimeProperty()
  user = ndb.KeyProperty(kind= "User")






