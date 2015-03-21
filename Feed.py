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

class CommentHandler(SessionHandler):
  """Handler to process user comments"""
  def post(self):
    origin = cgi.escape(self.request.get('origin'))
    text = cgi.escape(self.request.get('text'))
    sender = cgi.escape(self.request.get('sender'))
    recipient = cgi.escape(self.request.get('recipient'))
    replied_to_urlsafe = cgi.escape(self.request.get('parent'))
    comment = Comment()
    if len(replied_to_urlsafe) != 0:
      replied_to_key = ndb.Key(urlsafe=replied_to_urlsafe)
      comment.parent = replied_to_key
      recipient_comment = ndb.Key(urlsafe=replied_to_urlsafe).get()
      comment.recipient = recipient_comment.sender
      comment.sender = self.user_model.username
      comment.root = False;
    else:
      comment.sender = sender
      comment.recipient = recipient
    comment.text = text
    comment.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
    comment.put()
    if origin == "feed":
      self.redirect('/feed')
    else:
      self.redirect('/profile/{}'.format(recipient))



class FeedHandler(SessionHandler):
  """ Handler for handling user feed """
  def get(self):
    user = self.user_model
    comments = Comment.query().order(-Comment.time)
    if user:
      self.response.out.write(template.render('views/feed.html',
                                              {'viewer':user,
                                              'comments': comments}))

class FeedListHandler(SessionHandler):
  def get(self):
    threaded_comments = []
    page = int(cgi.escape(self.request.get('page')))
    offset_count = 10*page
    more = 0
    comments = Comment.query(Comment.root==True).order(-Comment.time).fetch(10, offset=offset_count)
    for comment in comments:
      threaded_comments.append(comment)
      children = Comment.query(Comment.parent == comment.key).order(Comment.time).fetch()
      if children != None:
        threaded_comments.extend(children)
      if comment != None:
        more += 1
    self.response.out.write(template.render('views/feedlist.html', {
                                              'comments': threaded_comments, 'more':more, 'page':page
                                              }))

app = webapp2.WSGIApplication([
                               ('/comment', CommentHandler),
                               ('/feed', FeedHandler),
                               ('/feedlist', FeedListHandler),
                               ], debug=True)

