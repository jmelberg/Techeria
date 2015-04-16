import cgi
import webapp2
import time
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

class LoginHandler(SessionHandler):
  def get(self):
    if self.user_model != None:
      self.redirect('/profile/{}'.format(self.user_model.username))
    else:
      self.response.out.write(template.render('views/login.html', {'user' : self.user_model}))
  def post(self):
    username = cgi.escape(self.request.get('username')).strip().lower()
    password = cgi.escape(self.request.get('password'))
    #TODO Check for non characters in username.
    try:
      if '@' in username:
        user_login = User.query(User.email_address == username).get()
        if user_login != None:
          username = user_login.username
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
    account = cgi.escape(self.request.get('account_type'))
    password = cgi.escape(self.request.get('password'))
    avatar = self.request.get('img')
    avatar = images.resize(avatar,400,400) 
    unique_properties = ['email_address']
    lower_first = first_name.lower()
    lower_last = last_name.lower()
    # Initial Creation of User 
    user_data = User.create_user(username,
      unique_properties, username=username,
      email_address=email, first_name=first_name, lower_first_name=lower_first, password_raw=password,
      last_name=last_name, lower_last_name = lower_last, avatar = avatar, subscriptions=["news", "techeria"], account_type=account, verified=False)
    # TODO: Look for new wait method
    time.sleep(1)
    try:
      u = self.auth.get_user_by_password(username, password, remember=True,
      save_session=True)
      self.redirect('/profile/{}'.format(self.user_model.username))
    except( auth.InvalidAuthIdError, auth.InvalidPasswordError):
      error = "Invalid Email/Password"
      self.response.out.write(template.render('views/login.html', {'error':error}))

class LogoutHandler(SessionHandler):
    """Destroy the user session and return them to the login screen."""
    @login_required
    def get(self):
        self.auth.unset_session()
        self.redirect('/')

app = webapp2.WSGIApplication([
                               ('/', LoginHandler),
                               ('/register', RegisterHandler),
                               ('/logout', LogoutHandler)
                               ], debug=True)
