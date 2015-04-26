from google.appengine.ext import ndb
import webapp2_extras.appengine.auth.models as auth_models

''' User Model 
- Object to hold key value, basic information, user skills/subscriptions, and picture.
- Instantiates when user registers
- Updates during profile edit, engagement, and forum subscribing.
'''
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
  endorsement_count = ndb.IntegerProperty(default =0)
  skills = ndb.KeyProperty(kind = "Skill", repeated=True)
  skills_count = ndb.IntegerProperty(default = 0)
  avatar =  ndb.BlobProperty()
  subscriptions = ndb.StringProperty(repeated=True)

''' Profile Model 
- Object to hold owner property and profile about me section.
- Instantiates or Updates during profile creation/edit.
'''
class Profile(ndb.Model):
  owner = ndb.KeyProperty(kind = "User")
  about = ndb.StringProperty()

''' Comment Model 
- Object to holds recipient, sender, time, and comment details.
- Root, parent, children and offset attributes needed for nested comments.
- Instantiates when user comments on own profile, another's profile, forum post, or nested comment.
'''
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

''' Message Model 
- Object to hold recipient, sender, time, and message details.
- Instantiates when user sends message to another user, or self.
'''
class Message(ndb.Model):
  sender = ndb.StringProperty()
  recipient = ndb.StringProperty()
  subject = ndb.StringProperty()
  text = ndb.TextProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)

''' Connection Model 
- Object to requestee and requestor, with message sending capabilities.
- Instantiates when user requests another for connecting.
'''
class ConnectionRequest(ndb.Model):
  requestor = ndb.StringProperty()
  requestee = ndb.StringProperty()
  time = ndb.DateTimeProperty(auto_now_add=True)
  text = ndb.StringProperty()

''' ForumPost Model 
- Object to hold forum name and other descriptors.
- Includes upvoters/ downvoters listing, in addition to master catagories for easy query.
- Instantiates when user posts to a forum.
'''
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

''' Forum Model 
- Object to hold name of forum, posts and subscribers.
- Instantiates when new skill is created and when user generates new forum.
'''
class Forum(ndb.Model):
  name = ndb.StringProperty()
  posts = ndb.IntegerProperty()
  subscribers = ndb.KeyProperty(kind = "User", repeated=True)

''' Skill Model 
- Object to hold only name of skill.
- Instantiates when user generates new skill. 
'''
class Skill(ndb.Model):
  name = ndb.StringProperty()

''' Endorsement Model 
- Object to list of endorsers, the endorsee,  skill that is endorsed, and number of endorsements.
- Instantiates when user submits new endorsement, with or without written note.
'''
class Endorsement(ndb.Model):
  endorsers = ndb.KeyProperty(kind="User", repeated=True)
  endorsee = ndb.KeyProperty() 
  skill = ndb.KeyProperty(kind="Skill")
  endorsement_count = ndb.IntegerProperty(default = 0)

''' EndorsementDetails Model 
- Object to list of endorsers, the endorsee,  skill that is endorsed, description of endorsement,
time and number of endorsements.
- Instantiates when user submits new endorsement, only with written note attached. Posted to profile.
'''
class EndorsementDetails(ndb.Model):
  endorsee = ndb.KeyProperty()
  endorser = ndb.KeyProperty()
  skill = ndb.KeyProperty(kind="Skill")
  description = ndb.StringProperty()
  time = ndb.DateTimeProperty()

''' AccessToken Model 
- Object includes token property with user key attached, and time of access granted.
- Instantiates when mobile submits login request to API, access is verified throughout login.
'''
class AccessToken(ndb.Model):
  token = ndb.StringProperty()
  granted = ndb.DateTimeProperty()
  user = ndb.KeyProperty(kind= "User")






