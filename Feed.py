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
  # TODO: Work on nested comments
  def get(self):
    threaded_comments = []
    page = int(cgi.escape(self.request.get('page')))
    items = self.request.get('items')
    offset_count = 10*page
    viewer = self.user_model
    more = 0
    if items == '':
      comments = Comment.query(Comment.root==True).order(-Comment.time).fetch(10, offset=offset_count)
      for comment in comments:
        threaded_comments.append(comment)
        children_query = Comment.query(Comment.parent == comment.key).order(Comment.time).get()
        if children_query != None:
          children = Comment.query(Comment.parent == comment.key).order(Comment.time).fetch()
          for child in children:
            threaded_comments.append(child)
            grand_query = Comment.query(Comment.parent == child.key).order(Comment.time).get()
            if grand_query != None:
              grandchildren = Comment.query(Comment.parent == child.key).order(Comment.time).fetch()
              for gc in grandchildren:
                threaded_comments.append(gc)
        if comment != None:
          more += 1
      self.response.out.write(template.render('views/feedlist.html', {
                                              'comments': threaded_comments, 'more':more, 'page':page, 'viewer':viewer,
                                              }))
    else:
      posts = ForumPost.query().order(-ForumPost.time).fetch(10, offset=offset_count)
      self.response.out.write(template.render('views/feedlist.html', {
                                              'posts': posts, 'more':more, 'page':page, 'viewer':viewer
                                              }))
  def comment_list(self):
    index = 0
    comments = Comment.query(Comment.root==True).order(-Comment.time).fetch()
    while index < len(comments):
      print(comments[index].text)
      children = Comment.query(Comment.parent == comments[index].key).fetch()
      index += 1
      comments[index:index] = children
    return comments



app = webapp2.WSGIApplication([
                               ('/comment', CommentHandler),
                               ('/feed', FeedHandler),
                               ('/feedlist', FeedListHandler),
                               ], debug=True)

