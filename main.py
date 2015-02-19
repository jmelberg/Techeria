import cgi
import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import User
from models import Comment
from models import Message
from models import ConnectionRequest
import logging

"""Techeria is a professional social network for techies"""

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    """checks for user account from users api"""
    user = users.get_current_user()
    if user:
      registered_account = User.get_by_id(user.user_id())
      logout = users.create_logout_url('/')
      #checks if account for user exists
      if registered_account:
        #self.response.out.write(template.render('profile.html',
        #                                        {'user':registered_account, 'logout':logout}))
        self.redirect('/profile/{}'.format(registered_account.username))
      else:
        def create_account():
          """creates a user entity"""
          account = User(id=user.user_id())
          account.email = user.email()
          account.put()
        create_account()
        self.response.out.write(template.render('register.html',
                                                {'user':user, 'logout':logout}))
    else:
      self.redirect(users.create_login_url(self.request.uri))

class RegisterHandler(webapp2.RequestHandler):
  def post(self):
    """Registers the user and updates datastore"""
    user = User.get_by_id(users.get_current_user().user_id())
    user.first_name = cgi.escape(self.request.get('first_name'))
    user.last_name = cgi.escape(self.request.get('last_name'))
    user.username = cgi.escape(self.request.get('username'))
    user.profession = cgi.escape(self.request.get('profession'))
    user.employer = cgi.escape(self.request.get('employer'))
    user.major = cgi.escape(self.request.get('major'))
    user.grad_year = int(self.request.get('grad_year'))
    user.put()
    self.redirect('/')

class ProfileHandler(webapp2.RequestHandler):
  """handler to display a profile page"""
  def get(self, profile_id):
    #profile_id = key name of user
    viewer_email = users.get_current_user()
    v = User.query(User.email == viewer_email.email())
    viewer = v.get()
    logout = users.create_logout_url('/')
    q = User.query(User.username == profile_id)
    user = q.get()
    comments = Comment.query(Comment.recipient == user.username).order(-Comment.time)
    if user:
      self.response.out.write(template.render('profile.html',
                                        {'user':user,
                                              'comments': comments,
                                              'viewer':viewer,
                                              'logout':logout}))

class ConnectHandler(webapp2.RequestHandler):
  """handler to connect users"""
  def get(self):
    user = User.get_by_id(users.get_current_user().user_id())
    requests = ConnectionRequest.query(ConnectionRequest.requestee == user.username).order(-ConnectionRequest.time)
    logout = users.create_logout_url('/')
    self.response.out.write(template.render('requests.html', {'user': user, 'requests': requests, 'logout':logout}))
  def post(self):
    requestor = User.get_by_id(users.get_current_user().user_id())
    q = User.query(User.username == self.request.get('requestee'))
    requestee = q.get()
    connection_request = ConnectionRequest()
    connection_request.requestor = requestor.username
    connection_request.requestee = requestee.username
    connection_request.put()
    requestee.request_count += 1
    requestee.put()
    self.redirect('/')


class SearchHandler(webapp2.RequestHandler):
  """Handler to search for users/jobs"""
  def get(self):
    search = cgi.escape(self.request.get('search'))
    #TODO normalize names in User model to ignore case
    search_list = search.split(',')
    email = []
    for search_string in search_list:
      search_string = search_string.strip(' ')
      if "@" in search_string:
        q = User.query(User.email == search_string)
        email.append(q.get())
    self.response.out.write(template.render('search.html', {'email':email}))

class CommentHandler(webapp2.RequestHandler):
  """Handler to process user comments"""
  def post(self):
    text = cgi.escape(self.request.get('text'))
    sender = cgi.escape(self.request.get('sender'))
    recipient = cgi.escape(self.request.get('recipient'))
    comment = Comment()
    comment.text = text
    comment.sender = sender
    comment.recipient = recipient
    comment.put()
    self.redirect('/profile/{}'.format(recipient))

class MessageHandler(webapp2.RequestHandler):
  """ Handler to process user messages"""
  def get(self):
    user = User.get_by_id(users.get_current_user().user_id())
    messages = Message.query(Message.recipient == user.username).order(-Message.time)
    logout = users.create_logout_url('/')
    self.response.out.write(template.render('messages.html', {'user': user, 'messages': messages, 'logout':logout}))

class ComposeMessage(webapp2.RequestHandler):
  def get(self):
    viewer_email = users.get_current_user()
    v = User.query(User.email == viewer_email.email())
    viewer = v.get()
    logout = users.create_logout_url('/')
    self.response.out.write(template.render('composeMessage.html', {'logout': logout,
                                                                    'viewer':viewer, 'user':viewer}))

  def post(self):
    text = cgi.escape(self.request.get('text'))
    sender = cgi.escape(self.request.get('sender'))
    recipient = cgi.escape(self.request.get('recipient'))
    message = Message()
    message.text = text
    message.sender = sender
    message.recipient = recipient
    message.put()
    #Increment message count for navbar
    q = User.query(User.username == recipient)
    user = q.get()
    user.message_count += 1
    user.put()
    self.redirect('/messages')

class FeedHandler(webapp2.RequestHandler):
  """ Handler for handling user feed """
  def get(self):
    user = User.get_by_id(users.get_current_user().user_id())
    logout = users.create_logout_url('/')
    comments = Comment.query().order(-Comment.time)
    if user:
      self.response.out.write(template.render('feed.html',
                                              {'user':user,
                                              'comments': comments,
                                              'logout':logout}))






app = webapp2.WSGIApplication([
                               ('/', LoginHandler),
                               ('/register', RegisterHandler),
                               ('/profile/(.+)', ProfileHandler),
                               ('/connect', ConnectHandler),
                               ('/search', SearchHandler),
                               ('/comment', CommentHandler),
                               ('/messages', MessageHandler),
                               ('/compose', ComposeMessage),
                               ('/feed', FeedHandler),
                               ], debug=True)
