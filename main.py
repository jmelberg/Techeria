import cgi
import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import User

"""Techeria is a professional social network for techies"""

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    """checks for user account from users api"""
    user = users.get_current_user()
    if user:
      registered_account = User.get_by_id(user.user_id())
      #checks if account for user exists
      if registered_account:
        logout = users.create_logout_url('/')
        registered_account.email = user.email()
        self.response.out.write(template.render('register.html',
                                                {'user':user, 'logout':logout}))
      else:
        def create_account():
          """creates a user entity"""
          account = User(id=user.user_id())
          account.name = user.email()
          account.put()
        create_account()
        self.redirect('/')
    else:
      self.redirect(users.create_login_url(self.request.uri))

class RegisterHandler(webapp2.RequestHandler):
  def post(self):
    """Registers the user and updates datastore"""
    user = User.get_by_id(users.get_current_user().user_id())
    user.first_name = cgi.escape(self.request.get('first_name'))
    user.last_name = cgi.escape(self.request.get('last_name'))
    user.profession = cgi.escape(self.request.get('profession'))
    user.major = cgi.escape(self.request.get('major'))
    user.put()
    self.redirect('/')
    
app = webapp2.WSGIApplication([
                               ('/', LoginHandler),
                               ('/register', RegisterHandler)
                               ], debug=True)
