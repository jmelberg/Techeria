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

class MessageHandler(SessionHandler):
  """ Handler to process user messages"""
  @login_required
  def get(self):
    user = self.user_model
    user.message_count = 0
    user.put()
    messages = Message.query(Message.recipient == user.username).order(-Message.time)
    self.response.out.write(template.render('views/messages.html', {'viewer': user, 'messages': messages}))

class ComposeMessage(SessionHandler):
  """ Handler to compose messages from one user to another """
  @login_required
  def get(self):
    recipient = cgi.escape(self.request.get('recipient'))
    viewer = self.user_model
    v = User.query(User.email_address == viewer.email_address)
    self.response.out.write(template.render('views/composeMessage.html', {
                                                                    'viewer':viewer, 'user':viewer, 'recipient':recipient}))
  def post(self):
    text = cgi.escape(self.request.get('text'))
    sender = cgi.escape(self.request.get('sender'))
    recipient = cgi.escape(self.request.get('recipient'))
    subject = cgi.escape(self.request.get('subject'))
    parent_message = cgi.escape(self.request.get('parent'))
    q = User.query(User.username == recipient)
    user = q.get()
    if(user):
      if len(parent_message) > 0:
        message_key = ndb.Key(urlsafe=parent_message)
        message = Message(parent = message_key)
      else:
        message = Message()
      message.subject = subject
      message.text = text
      message.sender = sender
      message.recipient = recipient
      message.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
      message.put()
      #Increment message count for navbar
      q = User.query(User.username == recipient)
      user = q.get()
      user.message_count += 1
      user.put()
      self.redirect('/messages')
    else:
      self.redirect('/compose')

class DeleteMessage(SessionHandler):
  """ Handler to delete messages from the datastore """
  def post(self):
    key_array = cgi.escape(self.request.get('array'))
    for key in key_array.split(","):
      message_key = ndb.Key(urlsafe=key)
      message_key.delete()
    self.redirect('/messages')

class ReadMessage(SessionHandler):
  """ Handler to read individual message """
  @login_required
  def get(self, message_id):
    viewer = self.user_model
    viewer_email = viewer.email_address
    v = User.query(User.email_address == viewer_email)
    message_key = ndb.Key(urlsafe=message_id)
    message = message_key.get()
    self.response.out.write(template.render('views/readMessage.html', {'viewer':viewer, 'message': message}))


    app = webapp2.WSGIApplication([
                               ('/messages', MessageHandler),
                               ('/compose', ComposeMessage),
                               ('/messages/(.+)', ReadMessage),
                               ('/trash', DeleteMessage),
                               ], debug=True)
