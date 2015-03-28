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
    text = cgi.escape(self.request.get('text'))
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
      connection_request.text = text
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

    app = webapp2.WSGIApplication([
                               ('/connect', ConnectHandler),
                               ('/confirmconnect', ConfirmConnection),
                               ('/connections', DisplayConnections),
                               ], debug=True)