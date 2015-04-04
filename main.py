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
from Messages import *
from Forum import *
from Feed import *
from Authentication import *
from Connections import *
"""Techeria is a professional social network for techies"""

class ProfileHandler(SessionHandler):
  """handler to display a profile page"""
  def get(self, profile_id):
    #TODO remove sleep below for deployment,, for testing only
    viewer = self.user_model
    q = User.query(User.username == profile_id)
    user = q.get()
    skill_list = []
    for skill in user.skills:
      skill_list.append(skill.get())
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
                                        'viewer':viewer, 'skills':skill_list,}))

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
        query_first = User.first_name
        query_last = User.last_name
        full_name = User.query(User.first_name == first_name, User.last_name == last_name)
        if full_name:
          results.append(full_name.get())
      else:
        first_name = User.query(User.first_name == search_string)
        last_name = User.query(User.last_name == search_string)
        username = User.query(User.username == search_string)
        if username.get() is not None:
          results.append(username.get())
        if first_name.get() is not None:
          for result in first_name.fetch(10):
            results.append(result)
        if last_name.get() is not None:
          for result in last_name.fetch(10):
            results.append(result)
    self.response.out.write(template.render('views/search.html', {'results':results, 'search_string':search_string}))

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
  """ Used to ensure no two users can have the same username """
  def get(self):
    username = cgi.escape(self.request.get('username'))
    user_query = User.query(User.username == username)
    taken = user_query.get()
    if taken == None:
      self.response.out.write('Username is available')
    else:
      self.response.out.write('Username is taken')

class UpdateProfile(SessionHandler):
  """ In place update profile capabilities on the user profile page """
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

class SkillsHandler(SessionHandler):
  def post(self):
    user = self.user_model
    role = cgi.escape(self.request.get('role'))
    field = cgi.escape(self.request.get('field'))
    tools = cgi.escape(self.request.get('tools'))
    specialty = cgi.escape(self.request.get('specialty'))
    tool_list = tools.split(',')
    new_skills_count = 2 #for field and specialty
    for i in tool_list:
      if i != " ":
        i = i.lower().strip()
        skill_query = Skill.query(Skill.name == i).get()
        #don't add duplicate skill
        if skill_query == None:
          new_skill = Skill(name=i)
          new_skill.put()
          user.skills.append(new_skill.key)
        else:
          user.skills.append(skill_query.key)
        new_skills_count += 1
    field_skill = Skill(name=field.lower().strip())
    specialty_skill = Skill(name=specialty.lower().strip())
    field_skill.put()
    specialty_skill.put()
    user.skills.append(field_skill.key)
    user.skills.append(specialty_skill.key)
    user.skills_count += new_skills_count
    user.role = role
    user.put()

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
                               ('/tech/', ForumViewer),
                               ('/newskill', SkillsHandler),
                               ('/subscribe', SubscriptionHandler)
                               ], debug=True, config=config)
