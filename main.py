import cgi
import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import User

"""GAE application to simulate stock trading"""

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


app = webapp2.WSGIApplication([
                               ('/', LoginHandler),
                               ], debug=True)