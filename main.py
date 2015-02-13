import cgi
import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
import ystockquote
from models import User
from models import Stock

"""GAE application to simulate stock trading"""

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    """checks for user account from users api"""
    user = users.get_current_user()
    if user:
      registered_account = User.all().filter('user_key =', user.user_id()).count()
      #checks if account for user exists
      if registered_account > 0:
        logout = users.create_logout_url('/')
        stocks = Stock.all().filter('owner =', user.user_id())
        user = User.all().filter('user_key =', user.user_id()).get()
        self.response.out.write(template.render('main.html',
                                                {'stocks': stocks, 'user':user, 'logout':logout}))
      else:
        def create_account():
          """creates a user entity"""
          user = users.get_current_user()
          account = User(key_name=user.user_id())
          account.user_key = user.user_id()
          account.name = user.nickname()
          account.put()
        create_account()
        self.redirect('/')
    else:
      self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([
                               ('/', LoginHandler),
                               ('/addstock', NewStock),
                               ('/updateprices', UpdatePrices),
                               ('/sellstock', SellStock),
                               ('/stocksearch', StockSearch)
                               ], debug=True)