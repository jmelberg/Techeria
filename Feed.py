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
    viewer = self.user_model
    comment = Comment()
    if len(replied_to_urlsafe) != 0:
      replied_to_key = ndb.Key(urlsafe=replied_to_urlsafe)
      parent_comment = replied_to_key.get() #parent comment
      comment.parent = replied_to_key
      comment.offset = parent_comment.offset + 20
      recipient_comment = ndb.Key(urlsafe=replied_to_urlsafe).get()
      comment.recipient = recipient_comment.sender
      comment.sender = self.user_model.username
      comment.root = False
    else:
      comment.sender = sender
      comment.recipient = recipient

    # Not double adding User Keys
    if sender != recipient:
      comment.sender_key = User.query(User.username == sender).get().key
      comment.recipient_key = User.query(User.username== recipient).get().key
    else:
      comment.sender_key = User.query(User.username == sender).get().key
      comment.recipient_key = None
    comment.text = text
    comment.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
    comment.put()
    
    if comment.root == False:
      parent_comment.children.append(comment.key)
      parent_comment.put()
    
    if origin == "feed":
      self.redirect('/feed')
    else:
      self.redirect('/profile/{}'.format(recipient))

class FeedHandler(SessionHandler):
  """ Handler for handling user feed """
  def get(self):
    user = self.user_model
    if user == None:
      override_base = "visitorBase.html"
    else:
      override_base = "base.html"
    self.response.out.write(template.render('views/feed.html',
                                              {'viewer':user, 'override_base':override_base}))

class FeedListHandler(SessionHandler):
  """ Handler to handle output of all comments pulled from all users.
      
      CURRENT: Loads 10 comments per page, with ability to load more when user reaches
      end of page.
  """
  def get(self):
    threaded_comments = []
    page = int(cgi.escape(self.request.get('page')))
    items = self.request.get('items')
    offset_count = 10*page
    viewer = self.user_model
    more = 0
    if items == '':
      threaded_comments, more = self.comment_list(offset_count)
      self.response.out.write(template.render('views/feedlist.html', {
                                              'comments': threaded_comments, 'more':more, 'page':page, 'viewer':viewer,
                                              }))
    else:
      posts, more = self.post_list(offset_count)
      self.response.out.write(template.render('views/feedlist.html', {
                                              'posts': posts, 'more':more, 'page':page, 'viewer':viewer
                                              }))
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
    posts = ForumPost.query(ForumPost.forum_name.IN(viewer.subscriptions)).order(-ForumPost.time).fetch(10, offset=offset_count)
    more = len(posts)
    return posts, more


app = webapp2.WSGIApplication([
                               ('/comment', CommentHandler),
                               ('/feed', FeedHandler),
                               ('/feedlist', FeedListHandler),
                               ], debug=True)

