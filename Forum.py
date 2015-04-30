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
from urlparse import urlparse

class VoteHandler(SessionHandler):
  """ Handles upvoting and downvoting on forum postings """
  @login_required
  def post(self):
    post = cgi.escape(self.request.get('key'))
    change = int(cgi.escape(self.request.get('change')))
    voter = cgi.escape(self.request.get('voter'))
    post_key = ndb.Key(urlsafe=post)
    new_post = post_key.get()
    user_key = ndb.Key(urlsafe=voter)
    if change == 1:
      if user_key in new_post.down_voters:
        change+=1
        new_post.down_voters.remove(user_key);
      new_post.up_voters.append(user_key)
    else:
      if user_key in new_post.up_voters:
        change-=1
        new_post.up_voters.remove(user_key);
      new_post.down_voters.append(user_key)
    new_post.vote_count+=change
    new_post.put()

class ForumHandler(SessionHandler):
  """ Handles the forum """
  def get(self, forum_id):
    forum_id = forum_id.lower()
    user = self.user_model
    forum_posts = ForumPost.query(ForumPost.forum_name == forum_id)
    forum = Forum.query(Forum.name == forum_id).get()
    if user == None:
      override_base = "visitorBase.html"
    else:
      override_base = "base.html"
    self.response.out.write(template.render('views/forum.html', {'viewer': user,
                                      'posts': forum_posts, 'forum': forum, 'forum_name': forum_id, 
                                      'override_base': override_base}))
  def post(self, forum_id):
    author = cgi.escape(self.request.get('author'))
    forum_name = cgi.escape(self.request.get('forum'))
    title = cgi.escape(self.request.get('title'))
    url = cgi.escape(self.request.get('url'))
    text = cgi.escape(self.request.get('text'))
    forums = forum_name.strip().replace(" ", "").split(",")
    for submissions in forums[0:3]:
      post = ForumPost()
      forum = Forum.query(Forum.name == submissions).get()
      if forum != None:
        forum.posts += 1
      else:
        forum = Forum(name=submissions, posts=1)
      forum.put()
      post.text = text
      post.author = author
      post.forum_name = submissions
      post.title = title
      post.time = datetime.datetime.now() - datetime.timedelta(hours=7) #For PST
      post.url = url
      post.url_host = urlparse(url).hostname
      post.reference = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
      post.put()
    self.redirect('/tech/{}'.format(forums[0]))

class SubmissionHandler(SessionHandler):
  """Handles user submissions to forums"""
  @login_required
  def get(self):
    user = self.user_model
    forum_name = cgi.escape(self.request.get('forum_name'))
    self.response.out.write(template.render('views/submitPost.html', {'viewer': user, 'forum_name':forum_name}))

class ForumCommentHandler(SessionHandler):
  """retrieves the correct forum post"""
  def get(self, forum_id, post_reference):
    user = self.user_model
    post = ForumPost.query(ForumPost.forum_name == forum_id, ForumPost.reference == post_reference).get()
    comments = Comment.query(Comment.parent==post.key).fetch()
    # Get nested Comments
    index = 0
    while index < len(comments):
      children = Comment.query(Comment.parent == comments[index].key).fetch()
      index +=1
      comments[index:index] = children

    if user == None:
      override_base = "visitorBase.html"
    else:
      override_base = "base.html"
    self.response.out.write(template.render('views/forumComments.html',
      {'override_base':override_base, 'viewer': user, 'post':post,
      'forum_name':forum_id, 'comments':comments, 'post_reference':post_reference}))
  def post(self, forum_id, post_reference):
    user = self.user_model
    post = ForumPost.query(ForumPost.forum_name == forum_id, ForumPost.reference == post_reference).get()
    text = cgi.escape(self.request.get('text'))
    sender = cgi.escape(self.request.get('sender'))
    recipient = cgi.escape(self.request.get('recipient'))
    replied_to_urlsafe = cgi.escape(self.request.get('parent'))
    comment = Comment(parent = post.key)
    if len(replied_to_urlsafe) != 0:
      replied_to_key = ndb.Key(urlsafe=replied_to_urlsafe)
      parent_comment = replied_to_key.get()
      comment.parent = replied_to_key
      comment.offset = parent_comment.offset + 20
      recipient_comment = ndb.Key(urlsafe=replied_to_urlsafe).get()
      comment.recipient = recipient_comment.sender
      comment.sender = user.username
      comment.root = False
    else:
      comment.sender = sender
      comment.recipient = recipient

    comment.text = text
    comment.time = datetime.datetime.now() - datetime.timedelta(hours=7) #For PST
    comment.put()

    if comment.root == False:
      parent_comment.children.append(comment.key)
      parent_comment.put()
      
    post.comment_count += 1
    post.put()
    self.redirect('/tech/{}/{}'.format(forum_id, post_reference))

class ForumViewer(SessionHandler):
  def get(self):
    user = self.user_model
    url = self.request.url
    if url[-1] == '/':
      self.redirect('/tech')
    forums = Forum.query().order(-Forum.posts)
    if user == None:
      override_base = "visitorBase.html"
    else:
      override_base = "base.html"
    self.response.out.write(template.render('views/forumViewer.html', {'viewer': self.user_model, 'forums':forums, 'override_base':override_base}))

class SubscriptionHandler(SessionHandler):
  @login_required
  def post(self):
    forum_name = cgi.escape(self.request.get('forum_name'))
    user_key = self.user_model.key
    forum_model = Forum.query(Forum.name == forum_name).get()
    forum_model.subscribers.append(user_key)
    forum_model.put()
    user = self.user_model
    user.subscriptions.append(forum_name)
    user.put()
    self.redirect('/tech/{}'.format(forum_name))   

app = webapp2.WSGIApplication([
                               ('/tech/(\w+)', ForumHandler),
                               ('/submit', SubmissionHandler),
                               ('/tech/(\w+)/(\w+)', ForumCommentHandler),
                               ('/tech', ForumViewer),
                               ('/tech/', ForumViewer),
                               ('/subscribe', SubscriptionHandler)
                               ], debug=True)

