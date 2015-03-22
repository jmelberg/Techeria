import cgi
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth
from models import User
from models import Comment
from models import Message
from models import ConnectionRequest
from models import ForumPost
from models import Skill
from models import Forum
import logging
import random
import string
import datetime
from BaseHandler import SessionHandler
from BaseHandler import login_required
from Messages import *
from Forum import *
from Feed import *

"""Techeria is a professional social network for techies"""

class LoginHandler(SessionHandler):
  def get(self):
    if self.user_model != None:
      self.redirect('/profile/{}'.format(self.user_model.username))
    else:
      self.response.out.write(template.render('views/login.html', {'user' : self.user_model}))
  def post(self):
    username = cgi.escape(self.request.get('username'))
    password = cgi.escape(self.request.get('password'))
    #TODO Check for non characters in username.
    try:
      u = self.auth.get_user_by_password(username, password, remember=True,
      save_session=True)
      self.redirect('/profile/{}'.format(self.user_model.username))
    except( auth.InvalidAuthIdError, auth.InvalidPasswordError):
      error = "Invalid Email/Password"
      self.response.out.write(template.render('views/login.html', {'error':error}))

class RegisterHandler(SessionHandler):
  def get(self):
    self.response.out.write(template.render('views/register.html',{}))
  def post(self):
    """Registers the user and updates datastore"""
    first_name = cgi.escape(self.request.get('first_name')).strip()
    last_name = cgi.escape(self.request.get('last_name')).strip()
    username = cgi.escape(self.request.get('username')).strip().lower()
    email = cgi.escape(self.request.get('email')).strip().lower()
    password = cgi.escape(self.request.get('password'))
    avatar = self.request.get('img')
    avatar = images.resize(avatar,400,400) 
    unique_properties = ['email_address']
    user_data = User.create_user(username,
      unique_properties, username=username,
      email_address=email, first_name=first_name, password_raw=password,
      last_name=last_name, avatar = avatar, verified=False)
    self.redirect('/')

class LogoutHandler(SessionHandler):
    """Destroy the user session and return them to the login screen."""
    @login_required
    def get(self):
        self.auth.unset_session()
        self.redirect('/')

class ProfileHandler(SessionHandler):
  """handler to display a profile page"""
  def get(self, profile_id):
    #TODO remove sleep below for deployment,, for testing only
    viewer = self.user_model
    q = User.query(User.username == profile_id)
    user = q.get()
    connection_list = []
    """Get friend count """
    counter = 0
    for connection in user.friends:
      connection = User.get_by_id(connection.id())
      counter+=1
    user.friend_count = counter
    comments = Comment.query(Comment.recipient == user.username).order(-Comment.time)
    if user:
      self.response.out.write(template.render('views/profile.html',
                                        {'user':user, 'comments': comments,
                                        'viewer':viewer}))

class ConnectHandler(SessionHandler):
  """handler to connect users"""
  @login_required
  def get(self):
    user = self.user_model
    requests = ConnectionRequest.query(ConnectionRequest.requestee == user.username).order(-ConnectionRequest.time)
    self.response.out.write(template.render('views/requests.html', {'viewer': user, 'requests': requests}))
  def post(self):
    requestor = self.user_model
    q = User.query(User.username == self.request.get('requestee'))
    requestee = q.get()
    #Querying datastore to check for open connection request
    incoming_query = ConnectionRequest.query(ConnectionRequest.requestor == requestee.username, ConnectionRequest.requestee == requestor.username)
    outgoing_query = ConnectionRequest.query(ConnectionRequest.requestor == requestor.username, ConnectionRequest.requestee == requestee.username)
    incoming_request = incoming_query.get()
    outgoing_request = outgoing_query.get()
    #don't create 2 connection requests between users
    if incoming_request == None and outgoing_request == None:
      connection_request = ConnectionRequest()
      connection_request.requestor = requestor.username
      connection_request.requestee = requestee.username
      connection_request.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
      connection_request.put()
      requestee.request_count += 1
      requestee.put()
    self.redirect('/')

class ConfirmConnection(SessionHandler):
  """updates the datastore for user connections"""
  def post(self):
    requestor = User.query(User.username == cgi.escape(self.request.get('requestor'))).get()
    requestee = User.query(User.username == cgi.escape(self.request.get('requestee'))).get()
    connection_request = ConnectionRequest.query(ConnectionRequest.requestee == requestee.username).get()
    requestor.friends.append(requestee.key)
    requestee.friends.append(requestor.key)
    requestee.request_count -= 1
    requestor.put()
    requestee.put()
    connection_request.key.delete()
    self.redirect('/connect')
    
class DisplayConnections(SessionHandler):
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
        #self.location = ""
        #self.picture = ""
    connection_list = []
    for connection_key in user.friends:
      connection = User.get_by_id(connection_key.id())
      friend = Friend()
      friend.first_name = connection.first_name
      friend.last_name = connection.last_name
      friend.username = connection.username
      if connection.profession != None:
        friend.profession = connection.profession + " at " + connection.employer
      friend.key_urlsafe = connection.key.urlsafe
      connection_list.append(friend)
    self.response.out.write(template.render('views/connections.html',
      {'connections': connection_list, 'user':user, 'viewer':viewer}))


class SearchHandler(SessionHandler):
  """Handler to search for users/jobs"""
  def get(self):
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
    self.response.out.write(template.render('views/search.html', {'results':results, 'search_string':search_string}))

class Image(SessionHandler):
  """Serves the image associated with an avatar"""
  def get(self):
    """receives user by urlsafe key"""
    user_key = ndb.Key(urlsafe=self.request.get('user_id'))
    height = cgi.escape(self.request.get('height'))
    width = cgi.escape(self.request.get('width'))
    user = user_key.get()
    self.response.headers['content-type'] = 'image/png'
    if len(height) > 0 and len(width) > 0:
      height = int(height)
      width = int(width)
      self.response.out.write(images.resize(user.avatar,height,width))
    else:
      self.response.out.write(user.avatar)

class CheckUsername(SessionHandler):
  """ Used to ensure no two users can have the same username """
  def get(self):
    username = cgi.escape(self.request.get('username'))
    user_query = User.query(User.username == username)
    taken = user_query.get()
    if taken == None:
      self.response.out.write('Username is available')
    else:
      self.response.out.write('Username is taken')

class UpdateProfile(SessionHandler):
  """ In place update profile capabilities on the user profile page """
  def post(self):
    first_name = cgi.escape(self.request.get('first'))
    last_name = cgi.escape(self.request.get('last'))
    profession = cgi.escape(self.request.get('profession'))
    employer = cgi.escape(self.request.get('employer'))
    user_key = ndb.Key(urlsafe=self.request.get('user_key'))
    user = user_key.get()
    user.first_name = first_name
    user.last_name = last_name
    user.profession = profession
    user.employer = employer
    user.put()
    self.redirect('/profile/{}'.format(user.username))

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'zomg-this-key-is-so-secret',
}
config['webapp2_extras.auth'] = {
    'user_model': User,
}

app = webapp2.WSGIApplication([
                               ('/', LoginHandler),
                               ('/register', RegisterHandler),
                               ('/profile/(\w+)', ProfileHandler),
                               ('/connect', ConnectHandler),
                               ('/confirmconnect', ConfirmConnection),
                               ('/search', SearchHandler),
                               ('/comment', CommentHandler),
                               ('/messages', MessageHandler),
                               ('/compose', ComposeMessage),
                               ('/feed', FeedHandler),
                               ('/connections', DisplayConnections),
                               ('/tech/(\w+)', ForumHandler),
                               ('/submit', SubmissionHandler),
                               ('/feedlist', FeedListHandler),
                               ('/tech/(\w+)/(\w+)', ForumCommentHandler),
                               ('/messages/(.+)', ReadMessage),
                               ('/trash', DeleteMessage),
                               ('/img', Image),
                               ('/vote', VoteHandler),
                               ('/checkusername', CheckUsername),
                               ('/updateprofile', UpdateProfile),
                               ('/logout', LogoutHandler),
                               ('/tech', ForumViewer),
                               ('/tech/', ForumViewer)
                               ], debug=True, config=config)
