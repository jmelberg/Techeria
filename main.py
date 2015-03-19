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

"""Techeria is a professional social network for techies"""

class LoginHandler(SessionHandler):
  def get(self):
    if self.user_model != None:
      self.redirect('/profile/{}'.format(self.user_model.username))
    else:
      self.response.out.write(template.render('views/login.html', {'user' : self.user_model}))
  def post(self):
    username = cgi.escape(self.request.get('username'))
    password = cgi.escape(self.request.get('password'))
    #TODO Check for non characters in username.
    try:
      u = self.auth.get_user_by_password(username, password, remember=True,
      save_session=True)
      self.redirect('/profile/{}'.format(self.user_model.username))
    except( auth.InvalidAuthIdError, auth.InvalidPasswordError):
      error = "Invalid Email/Password"
      self.response.out.write(template.render('views/login.html', {'error':error}))

class RegisterHandler(SessionHandler):
  def get(self):
    self.response.out.write(template.render('views/register.html',{}))
  def post(self):
    """Registers the user and updates datastore"""
    first_name = cgi.escape(self.request.get('first_name')).strip()
    last_name = cgi.escape(self.request.get('last_name')).strip()
    username = cgi.escape(self.request.get('username')).strip().lower()
    email = cgi.escape(self.request.get('email')).strip().lower()
    password = cgi.escape(self.request.get('password'))
    avatar = self.request.get('img')
    avatar = images.resize(avatar,400,400) 
    unique_properties = ['email_address']
    user_data = User.create_user(username,
      unique_properties, username=username,
      email_address=email, first_name=first_name, password_raw=password,
      last_name=last_name, avatar = avatar, verified=False)
    self.redirect('/')

class LogoutHandler(SessionHandler):
    """Destroy the user session and return them to the login screen."""
    @login_required
    def get(self):
        self.auth.unset_session()
        self.redirect('/')

class ProfileHandler(SessionHandler):
  """handler to display a profile page"""
  def get(self, profile_id):
    #TODO remove sleep below for deployment,, for testing only
    viewer = self.user_model
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
                                        {'user':user, 'comments': comments,
                                        'viewer':viewer}))

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


class SearchHandler(SessionHandler):
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
        q = User.query(User.email_address == search_string)
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
          for result in first_name.fetch(10):
            results.append(result)
    self.response.out.write(template.render('views/search.html', {'results':results, 'search_string':search_string}))

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
  def post(self):
    key_array = cgi.escape(self.request.get('array'))
    for key in key_array.split(","):
      message_key = ndb.Key(urlsafe=key)
      message_key.delete()
    self.redirect('/messages')

class ReadMessage(SessionHandler):
  def get(self, message_id):
    viewer = self.user_model
    viewer_email = viewer.email_address
    v = User.query(User.email == viewer_email)
    message_key = ndb.Key(urlsafe=message_id)
    message = message_key.get()
    self.response.out.write(template.render('views/readMessage.html', {'viewer':viewer, 'message': message}))

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

class VoteHandler(SessionHandler):
  def post(self):
    post = cgi.escape(self.request.get('key'))
    change = int(cgi.escape(self.request.get('change')))
    post_key = ndb.Key(urlsafe=post)
    new_post = post_key.get()
    new_post.vote_count+=change
    new_post.put()


class ForumHandler(SessionHandler):
  """ Handles the forum """
  def get(self, forum_id):
    forum_id = forum_id.lower()
    user = self.user_model
    forum_posts = ForumPost.query(ForumPost.forum_name == forum_id)
    self.response.out.write(template.render('views/forum.html', {'viewer': user,
                                      'posts': forum_posts, 'forum_name': forum_id}))
  def post(self, forum_id):
    author = cgi.escape(self.request.get('author'))
    forum_name = cgi.escape(self.request.get('forum'))
    title = cgi.escape(self.request.get('title'))
    url = cgi.escape(self.request.get('url'))
    text = cgi.escape(self.request.get('text'))
    post = ForumPost()
    forum = Forum.query(Forum.name == forum_name).get()
    if forum != None:
      forum.posts += 1
    else:
      forum = Forum(name=forum_name, posts=1)
    forum.put()
    post.text = text
    post.author = author
    post.forum_name = forum_name
    post.title = title
    post.time = datetime.datetime.now() - datetime.timedelta(hours=8) #For PST
    post.url = url
    post.reference = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    post.put()
    self.redirect('/tech/{}'.format(forum_name))

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
    comments = Comment.query(ancestor=post.key).fetch()
    self.response.out.write(template.render('views/forumComments.html', {'viewer': user, 'post':post, 'forum_name':forum_id, 'comments':comments}))
  def post(self, forum_id, post_reference):
    user = self.user_model
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

class Image(SessionHandler):
  """Serves the image associated with an avatar"""
  def get(self):
    """receives user by urlsafe key"""
    user_key = ndb.Key(urlsafe=self.request.get('user_id'))
    height = cgi.escape(self.request.get('height'))
    width = cgi.escape(self.request.get('width'))
    user = user_key.get()
    self.response.headers['content-type'] = 'image/png'
    if len(height) > 0 and len(width) > 0:
      height = int(height)
      width = int(width)
      self.response.out.write(images.resize(user.avatar,height,width))
    else:
      self.response.out.write(user.avatar)

class CheckUsername(SessionHandler):
  def get(self):
    username = cgi.escape(self.request.get('username'))
    user_query = User.query(User.username == username)
    taken = user_query.get()
    if taken == None:
      self.response.out.write('Username is available')
    else:
      self.response.out.write('Username is taken')

class UpdateProfile(SessionHandler):
  def post(self):
    first_name = cgi.escape(self.request.get('first'))
    last_name = cgi.escape(self.request.get('last'))
    profession = cgi.escape(self.request.get('profession'))
    employer = cgi.escape(self.request.get('employer'))
    user_key = ndb.Key(urlsafe=self.request.get('user_key'))
    user = user_key.get()
    user.first_name = first_name
    user.last_name = last_name
    user.profession = profession
    user.employer = employer
    user.put()
    self.redirect('/profile/{}'.format(user.username))

class ForumViewer(SessionHandler):
  def get(self):
    forums = Forum.query().order(-Forum.posts)
    self.response.out.write(template.render('views/forumViewer.html', {'viewer': self.user_model, 'forums':forums}))

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'zomg-this-key-is-so-secret',
}
config['webapp2_extras.auth'] = {
    'user_model': User,
}


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
                               ('/vote', VoteHandler),
                               ('/checkusername', CheckUsername),
                               ('/updateprofile', UpdateProfile),
                               ('/logout', LogoutHandler),
                               ('/tech', ForumViewer),
                               ('/tech/', ForumViewer)
                               ], debug=True, config=config)
