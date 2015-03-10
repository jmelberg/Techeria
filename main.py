import cgi
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from models import User
from models import Comment
from models import Message
from models import ConnectionRequest
from models import ForumPost
from models import Skill
import logging
import random
import string
import datetime

"""Techeria is a professional social network for techies"""

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    """checks for user account from users api"""
    user = users.get_current_user()
    if user:
      registered_account = User.get_by_id(user.user_id())
      logout = users.create_logout_url('/')
      #checks if account for user exists
      if registered_account and registered_account.username is not None:
        self.redirect('/profile/{}'.format(registered_account.username))
      else:
        def create_account():
          """creates a user entity"""
          account = User(id=user.user_id())
          account.email = user.email()
          account.put()
        create_account()
        self.response.out.write(template.render('views/register.html',
                                                {'user':user, 'logout':logout}))
    else:
      self.redirect(users.create_login_url(self.request.uri))

class RegisterHandler(webapp2.RequestHandler):
  def post(self):
    """Registers the user and updates datastore"""
    user = User.get_by_id(users.get_current_user().user_id())
    user.first_name = cgi.escape(self.request.get('first_name'))
    user.last_name = cgi.escape(self.request.get('last_name'))
    user.username = cgi.escape(self.request.get('username'))
    user.profession = cgi.escape(self.request.get('profession'))
    user.employer = cgi.escape(self.request.get('employer'))
    #avatar = self.request.get('img')
    avatar = images.resize(avatar, 32, 32)
    user.avatar = avatar 
    user.put()
    self.redirect('/')

class ProfileHandler(webapp2.RequestHandler):
  """handler to display a profile page"""
  def get(self, profile_id):
    #profile_id = key name of user
    viewer_email = users.get_current_user()
    v = User.query(User.email == viewer_email.email())
    viewer = v.get()
    logout = users.create_logout_url('/')
    q = User.query(User.username == profile_id)
    user = q.get()
    connection_list = []
    """Get friend count """
    counter = 0
    for connection in user.friends:
      connection = User.get_by_id(connection.id())
      counter+=1
    user.friend_count = counter

    comments = Comment.query(Comment.recipient == user.username).order(-Comment.time)
    if user:
      self.response.out.write(template.render('views/profile.html',
                                        {'user':user,
                                              'comments': comments,
                                              'viewer':viewer,
                                              'logout':logout}))

class ConnectHandler(webapp2.RequestHandler):
  """handler to connect users"""
  def get(self):
    user = User.get_by_id(users.get_current_user().user_id())
    requests = ConnectionRequest.query(ConnectionRequest.requestee == user.username).order(-ConnectionRequest.time)
    logout = users.create_logout_url('/')
    self.response.out.write(template.render('views/requests.html', {'viewer': user, 'requests': requests, 'logout':logout}))
  def post(self):
    requestor = User.get_by_id(users.get_current_user().user_id())
    q = User.query(User.username == self.request.get('requestee'))
    requestee = q.get()
    connection_request = ConnectionRequest()
    connection_request.requestor = requestor.username
    connection_request.requestee = requestee.username
    connection_request.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
    connection_request.put()
    requestee.request_count += 1
    requestee.put()
    self.redirect('/')

class ConfirmConnection(webapp2.RequestHandler):
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
    self.redirect('/')
    
class DisplayConnections(webapp2.RequestHandler):
  """ Will display all friends/connections of a user"""
  def get(self):
    username = cgi.escape(self.request.get('username'))
    user = User.query(User.username == username).get()
    viewer = User.get_by_id(users.get_current_user().user_id())
    class Friend():
      def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.username = ""
        self.profession = ""
        #self.location = ""
        #self.picture = ""
    connection_list = []
    for connection_key in user.friends:
      connection = User.get_by_id(connection_key.id())
      friend = Friend()
      friend.first_name = connection.first_name
      friend.last_name = connection.last_name
      friend.username = connection.username
      friend.profession = connection.profession + " at " + connection.employer
      connection_list.append(friend)
      logout = users.create_logout_url('/')
    self.response.out.write(template.render('views/connections.html', {'connections':connection_list, 'user':user, 'viewer':viewer, 'logout':logout}))


class SearchHandler(webapp2.RequestHandler):
  """Handler to search for users/jobs"""
  def get(self):
    search = cgi.escape(self.request.get('search'))
    #TODO normalize names in User model to ignore case
    search_list = search.split(',')
    results = []
    names = []
    for search_string in search_list:
      search_string = search_string.strip(' ')
      if "@" in search_string:
        q = User.query(User.email == search_string)
        if q:
          results.append(q.get())
      elif " " in search_string:
        person = search_string.split(' ')
        first_name = person[0]
        last_name = person[1]
        full_name = User.query(User.first_name == first_name, User.last_name == last_name)
        if full_name:
          results.append(full_name.get())
      else:
        first_name = User.query(User.first_name == search_string)
        username = User.query(User.username == search_string)
        if username.get() is not None:
          results.append(username.get())
        if first_name.get() is not None:
          results.append(first_name.get())
    self.response.out.write(template.render('views/search.html', {'results':results}))

class CommentHandler(webapp2.RequestHandler):
  """Handler to process user comments"""
  def post(self):
    origin = cgi.escape(self.request.get('origin'))
    text = cgi.escape(self.request.get('text'))
    sender = cgi.escape(self.request.get('sender'))
    recipient = cgi.escape(self.request.get('recipient'))
    comment = Comment()
    comment.text = text
    comment.sender = sender
    comment.recipient = recipient
    comment.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
    comment.put()
    if origin == "feed":
      self.redirect('/feed')
    else:
      self.redirect('/profile/{}'.format(recipient))

class MessageHandler(webapp2.RequestHandler):
  """ Handler to process user messages"""
  def get(self):
    user = User.get_by_id(users.get_current_user().user_id())
    user.message_count = 0
    user.put()
    messages = Message.query(Message.recipient == user.username).order(-Message.time)
    logout = users.create_logout_url('/')
    self.response.out.write(template.render('views/messages.html', {'viewer': user, 'messages': messages, 'logout':logout}))

class ComposeMessage(webapp2.RequestHandler):
  def get(self):
    recipient = cgi.escape(self.request.get('recipient'))
    viewer_email = users.get_current_user()
    v = User.query(User.email == viewer_email.email())
    viewer = v.get()
    logout = users.create_logout_url('/')
    self.response.out.write(template.render('views/composeMessage.html', {'logout': logout,
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

class DeleteMessage(webapp2.RequestHandler):
  def post(self):
    key_array = cgi.escape(self.request.get('array'))
    for key in key_array.split(","):
      message_key = ndb.Key(urlsafe=key)
      message_key.delete()
    self.redirect('/messages')

class ReadMessage(webapp2.RequestHandler):
  def get(self, message_id):
    viewer_email = users.get_current_user()
    v = User.query(User.email == viewer_email.email())
    viewer = v.get()
    message_key = ndb.Key(urlsafe=message_id)
    message = message_key.get()
    logout = users.create_logout_url('/')
    self.response.out.write(template.render('views/readMessage.html', {'logout': logout,
                                                                    'viewer':viewer, 'message': message}))

class FeedHandler(webapp2.RequestHandler):
  """ Handler for handling user feed """
  def get(self):
    user = User.get_by_id(users.get_current_user().user_id())
    logout = users.create_logout_url('/')
    comments = Comment.query().order(-Comment.time)
    if user:
      self.response.out.write(template.render('views/feed.html',
                                              {'viewer':user,
                                              'comments': comments,
                                              'logout':logout}))

class FeedListHandler(webapp2.RequestHandler):
  def get(self):
        comments = Comment.query().order(-Comment.time)
        self.response.out.write(template.render('views/feedlist.html', {
                                              'comments': comments,
                                              }))

class ForumHandler(webapp2.RequestHandler):
  """ Handles the forum """
  def get(self, forum_id):
    forum_id = forum_id.lower()
    user = User.get_by_id(users.get_current_user().user_id())
    forum_posts = ForumPost.query(ForumPost.forum_name == forum_id)
    self.response.out.write(template.render('views/forum.html', {'viewer': user,
                                      'posts': forum_posts, 'forum_name': forum_id}))
  def post(self, forum_id):
    author = cgi.escape(self.request.get('author'))
    forum = cgi.escape(self.request.get('forum'))
    title = cgi.escape(self.request.get('title'))
    url = cgi.escape(self.request.get('url'))
    text = cgi.escape(self.request.get('text'))
    post = ForumPost()
    post.text = text
    post.author = author
    post.forum_name = forum
    post.title = title
    post.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
    post.url = url
    post.reference = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    post.put()
    self.redirect('/tech/{}'.format(forum))

class SubmissionHandler(webapp2.RequestHandler):
  """Handles user submissions to forums"""
  def get(self):
    user = User.get_by_id(users.get_current_user().user_id())
    forum_name = cgi.escape(self.request.get('forum_name'))
    self.response.out.write(template.render('views/submitPost.html', {'viewer': user, 'forum_name':forum_name}))

class ForumCommentHandler(webapp2.RequestHandler):
  """retrieves the correct forum post"""
  def get(self, forum_id, post_reference):
    user = User.get_by_id(users.get_current_user().user_id())
    post = ForumPost.query(ForumPost.forum_name == forum_id, ForumPost.reference == post_reference).get()
    comments = Comment.query(ancestor=post.key).fetch()
    self.response.out.write(template.render('views/forumComments.html', {'viewer': user, 'post':post, 'forum_name':forum_id, 'comments':comments}))
  def post(self, forum_id, post_reference):
    user = User.get_by_id(users.get_current_user().user_id())
    post = ForumPost.query(ForumPost.forum_name == forum_id, ForumPost.reference == post_reference).get()
    text = cgi.escape(self.request.get('text'))
    sender = cgi.escape(self.request.get('sender'))
    recipient = cgi.escape(self.request.get('recipient'))
    comment = Comment(parent=post.key)
    comment.text = text
    comment.sender = sender
    comment.recipient = recipient
    comment.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
    comment.put()
    self.redirect('/tech/{}/{}'.format(forum_id, post_reference))

class Image(webapp2.RequestHandler):
  """Serves the image associated with an avatar"""
  def get(self):
    """receives user by urlsafe key"""
    user_key = ndb.Key(urlsafe=self.request.get('user_id'))
    user = user_key.get()
    self.response.headers['content-type'] = 'image/png'
    self.response.out.write(user.avatar)


app = webapp2.WSGIApplication([
                               ('/', LoginHandler),
                               ('/register', RegisterHandler),
                               ('/profile/(\w+)', ProfileHandler),
                               ('/connect', ConnectHandler),
                               ('/confirmconnect', ConfirmConnection),
                               ('/search', SearchHandler),
                               ('/comment', CommentHandler),
                               ('/messages', MessageHandler),
                               ('/compose', ComposeMessage),
                               ('/feed', FeedHandler),
                               ('/connections', DisplayConnections),
                               ('/tech/(\w+)', ForumHandler),
                               ('/submit', SubmissionHandler),
                               ('/feedlist', FeedListHandler),
                               ('/tech/(\w+)/(\w+)', ForumCommentHandler),
                               ('/messages/(.+)', ReadMessage),
                               ('/trash', DeleteMessage),
                               ('/img', Image),
                               ], debug=True)
