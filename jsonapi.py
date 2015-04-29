import cgi
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth
from models import *
from BaseHandler import SessionHandler
from BaseHandler import login_required
from urlparse import urlparse
import json


class BaseHandlerAPI(webapp2.RequestHandler):
  """based in handler for logged in functions"""
  def user_from_token(self, token):
    if type(token) == unicode:
      converter = bytearray(token, "utf-8")
      token = bytes(converter)
    token_key = ndb.Key("AccessToken", token)
    if token_key != None:
      access_token = AccessToken.query(AccessToken.token == token).get()
      user = access_token.user.get()
      return user
    else:
      return None

class FeedListHandlerAPI(BaseHandlerAPI):
  """ Handler to handle output of all comments pulled from all users.
      
      CURRENT: Loads 10 comments per page, with ability to load more when user reaches
      end of page.
  """
  def get(self):
    data = []
    token = cgi.escape(self.request.get('token'))
    threaded_comments = []
    page = int(cgi.escape(self.request.get('page')))
    items = self.request.get('items')
    offset_count = 10*page
    viewer = user_from_token(token)
    more = 0
    if viewer != None:
      if items == '':
        threaded_comments, more = self.comment_list(offset_count)
        self.response.out.write(threaded_comments)
      else:
        posts, more = self.post_list(offset_count)
        self.response.out.write(posts)
  def comment_list(self, offset_count):
    index = 0
    viewer = self.user_model
    # Need to see if user has friends, if not - Query using viewer.friends will break #
    if viewer.friends:
      comments = Comment.query(Comment.root==True, ndb.OR(Comment.sender_key.IN(viewer.friends),
        Comment.recipient_key.IN(viewer.friends), Comment.sender_key == viewer.key)).order(-Comment.time).fetch(10, offset=offset_count)
    else:
      comments = Comment.query(Comment.root==True, Comment.sender_key == viewer.key).order(-Comment.time).fetch(10, offset=offset_count)
    more = len(comments)
    while index < len(comments):
      children = Comment.query(Comment.parent == comments[index].key).fetch()
      index += 1
      comments[index:index] = children
    return comments, more

  def post_list(self, offset_count):
    index = 0
    viewer = self.user_model
    posts = ForumPost.query(ForumPost.forum_name.IN(viewer.subscriptions)).order(-ForumPost.vote_count, -ForumPost.time).fetch(10, offset=offset_count)
    more = len(posts)
    return posts, more

class MessageHandlerAPI(BaseHandlerAPI):
  """ Handler to process user messages"""
  def post(self):
    data = []
    token = cgi.escape(self.request.get('token'))
    arg = cgi.escape(self.request.get('q'))
    user = self.user_from_token(token)
    if user == None:
      data.append("Invalid Token")
      self.response.out.write(json.dumps(data))
    if arg == "sent":
      messages = Message.query(Message.sender == user.username).order(-Message.time)
    else:
      messages = Message.query(Message.recipient == user.username).order(-Message.time)
    for message in messages:
      item = {}
      item["type"] = "message"
      item["sender"] = message.sender
      item["recipient"] = message.recipient
      item["text"] = message.text
      data.append(item)
    self.response.headers['Content-Type'] = 'application/json' 
    self.response.out.write(json.dumps(data))


class ForumAPI(SessionHandler):
  """ Handles the forum """
  def get(self, forum_id):
    forum_id = forum_id.lower()
    user = self.user_model
    forum_posts = ForumPost.query(ForumPost.forum_name == forum_id)
    forum = Forum.query(Forum.name == forum_id).get()
    data = []
    for forum_post in forum_posts:
      post = {}
      post['type'] = "forumpost"
      post['title'] = forum_post.title
      post['votes'] = forum_post.vote_count
      post['author'] = forum_post.author
      post['text'] = forum_post.text
      post['reference'] = forum_post.reference
      if forum_post.url:
        post['url'] = forum_post.url
      data.append(post)
    self.response.headers['Content-Type'] = 'application/json' 
    self.response.out.write(json.dumps(data))

class ForumViewerAPI(SessionHandler):
  def get(self):
    url = self.request.url
    if url[-1] == '/':
      self.redirect('/api/tech')
    forums = Forum.query().order(-Forum.posts)
    data = []
    for forum in forums:
      listing = {}
      listing['name'] = forum.name
      listing['type'] = "forum"
      listing['posts'] = forum.posts
      data.append(listing)
    self.response.headers['Content-Type'] = 'application/json' 
    self.response.out.write(json.dumps(data))

class ProfileHandlerAPI(SessionHandler):
  """handler to display a profile page"""
  def get(self, profile_id):
    viewer = self.user_model
    q = User.query(User.username == profile_id)
    user = q.get()
    user_json = {}
    if user != None:
      #User Vitals
      user_json['type'] = "user"
      user_json['account_type'] = user.account_type
      user_json['username'] = user.username
      user_json['firstname'] = user.first_name
      user_json['lastname'] = user.last_name
      user_json['email'] = user.email_address
      user_json['profession'] = user.profession
      user_json['employer'] = user.employer
      #User Profile Information
      user_json['subscriptions'] = user.subscriptions
      user_json['friend_count'] = user.friend_count
      user_json['picture'] = "/img?user_id={}".format(user.key.urlsafe())
    self.response.headers['Content-Type'] = 'application/json' 
    self.response.out.write(json.dumps(user_json))

#Returns array object from given key
def getObjectsFromKey(keys):
  items = []
  for key in keys:
    items.append(key.get().name)
  return items


class SearchHandlerAPI(SessionHandler):
  """Handler to search for users/jobs"""
  def get(self):
    user = self.user_model
    search = cgi.escape(self.request.get('search'))
    #TODO normalize names in User model to ignore case
    search_list = search.split(',')
    results = []
    names = []
    for search_string in search_list:
      search_string = search_string.strip(' ')
      if "@" in search_string:
        q = User.query(User.email_address == search_string)
        if q:
          results.append(q.get())
      elif " " in search_string:
        person = search_string.split(' ')
        first_name = person[0]
        last_name = person[1]
        query_first = User.first_name
        query_last = User.last_name
        full_name = User.query(User.first_name == first_name, User.last_name == last_name)
        if full_name:
          results.append(full_name.get())
      else:
        first_name = User.query(User.first_name == search_string)
        last_name = User.query(User.last_name == search_string)
        username = User.query(User.username == search_string)
        if username.get() is not None:
          results.append(username.get())
        if first_name.get() is not None:
          for result in first_name.fetch(10):
            results.append(result)
        if last_name.get() is not None:
          for result in last_name.fetch(10):
            results.append(result)
    search_results = []
    for result in results:
      search_result = {}
      search_result['username'] = result.username
      search_results.append(search_result)
    self.response.headers['Content-Type'] = 'application/json' 
    self.response.out.write(json.dumps(search_results))

class DisplayConnectionsAPI(SessionHandler):
  """ Will display all friends/connections of a user"""
  def get(self):
    username = cgi.escape(self.request.get('username'))
    user = User.query(User.username == username).get()
    viewer = self.user_model
    class Friend():
      def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.username = ""
        self.profession = ""
        self.key_urlsafe = ""
        #self.picture = ""
    connection_list = []
    for connection_key in user.friends:
      connection = User.get_by_id(connection_key.id())
      friend = {}
      friend['type'] = "user"
      friend['firstname'] = connection.first_name
      friend['lastname'] = connection.last_name
      friend['username'] = connection.username
      if connection.profession != None:
        friend['profession'] = connection.profession
        friend['employer'] = connection.employer
      connection_list.append(friend)
    self.response.headers['Content-Type'] = 'application/json' 
    self.response.out.write(json.dumps(connection_list))
