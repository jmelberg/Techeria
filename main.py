import cgi
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from webapp2_extras import sessions, auth, json
from models import User
from models import Comment
from models import Message
from models import ConnectionRequest
from models import ForumPost
from models import Skill
from models import Forum
from models import Endorsement
from models import AccessToken
from models import Profile
from models import EndorsementDetails
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
from jsonapi import *
import json
"""Techeria is a professional social network for techies"""

class ProfileHandler(SessionHandler):
  """handler to display a profile page"""
  @login_required
  def get(self, profile_id):
    viewer = self.user_model
    q = User.query(User.username == profile_id)
    user = q.get()
    profile = Profile.query(Profile.owner == user.key).get()
    #if profile isn't created, create one
    if not profile:
      profile = Profile()
      profile.owner = user.key
      profile.about = ""
      profile.put()
    skill_list = []
    endorsements = Endorsement.query(Endorsement.endorsee == user.key).fetch()
    endorsement_details = EndorsementDetails.query(EndorsementDetails.endorsee == user.key).fetch()
    user.endorsement_count = len(endorsement_details)
    for skill in user.skills:
      skill = skill.get()
      if skill is not None:
        endorsement_list = []
        endorsement_list.append(skill)
        #Get endorsement messages
        #Add number #
        count = 0
        for x in endorsements:
          if x.skill == skill.key:
            count=x.endorsement_count
        endorsement_list.append(count)
        skill_list.append(endorsement_list)

    connection_list = []
    """Get friend count """
    counter = 0
    for connection in user.friends:
      connection = User.get_by_id(connection.id())
      counter+=1
    user.friend_count = counter
    user.put()
    # Get Nested Comments
    comments = Comment.query(Comment.root==True, ndb.OR(Comment.recipient_key == user.key, Comment.sender_key == user.key)).order(-Comment.time).fetch(10)
    index = 0
    while index < len(comments):
      children = Comment.query(Comment.parent == comments[index].key).fetch()
      index += 1
      comments[index:index] = children
    if user:
      self.response.out.write(template.render('views/profile.html',
                                        {'user':user, 'comments': comments,
                                        'viewer':viewer, 'skills':skill_list, 'profile':profile, 'endorsements':endorsement_details}))

class SearchHandler(SessionHandler):
  """Handler to search for users/jobs"""
  def get(self):
    user = self.user_model
    search = cgi.escape(self.request.get('search'))
    #TODO normalize names in User model to ignore case
    search_list = search.split(',')
    results = []
    # For recuiters' advance search #
    jobs = []
    employers = []
    skills = []
    names = []
    forum_query = []
    search_type = " "
    if user.account_type == "Recruiter":
      search_type = "advanced"

    #Search Algorithm
    for search_string in search_list:
      search_string = search_string.strip(' ').lower()
      if "@" in search_string:
        q = User.query(User.email_address == search_string)
        if q:
          results.append(q.get())
      elif " " in search_string:
        person = search_string.split(' ')
        first_name = person[0]
        last_name = person[1]
        full_name = User.query(ndb.OR(User.lower_profession == search_string, 
          User.lower_employer == search_string, ndb.AND(User.lower_first_name == first_name, User.lower_last_name == last_name))).fetch()
        if search_type is "advanced":
          profession_name = User.query(User.lower_profession == search_string).fetch()
          employer_name = User.query(User.lower_employer == search_string).fetch()
          jobs.extend(profession_name)
          employers.extend(employer_name) 
        if full_name:
          results.extend(full_name)
      else:
        if search_type is "advanced":
          jobs_list = User.query(ndb.OR(User.lower_profession == search_string, User.profession == search_string)).fetch()
          employers_list = User.query(ndb.OR(User.lower_employer == search_string, User.employer == search_string)).fetch()
          jobs.extend(jobs_list)
          employers.extend(employers_list)
          # Get Users with skills
          skill_query = Skill.query(Skill.name == search_string).get()
          if skill_query != None:
            users_with_skills = []
            # TODO limit fetch returns entities
            skilled_users = User.query(User.skills == skill_query.key).fetch()
            skills.extend(skilled_users)
            results.extend(skilled_users)
          forum_query = Forum.query(Forum.name == search_string).get()
          
        name_list = User.query(ndb.OR(User.username == search_string, User.lower_first_name == search_string, User.lower_last_name == search_string, 
          User.lower_employer == search_string, User.lower_profession == search_string)).fetch()
        results.extend(name_list)
      self.response.out.write(template.render('views/search.html', {'results':results, 'employers': employers,
        'jobs': jobs, 'search_string':search_string, 'viewer':user, 'skills':skills, 'forums':forum_query}))


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

class UpdatePicture(SessionHandler):
  def post(self):
    user = self.user_model
    avatar = self.request.get('img')
    avatar = images.resize(avatar, 400, 400)
    user.avatar = avatar
    user.put()
    self.redirect('/profile/{}'.format(user.username))



class UpdateProfile(SessionHandler):
  """ In place update profile capabilities on the user profile page """
  def post(self):
    first_name = cgi.escape(self.request.get('first'))
    last_name = cgi.escape(self.request.get('last'))
    profession = cgi.escape(self.request.get('profession'))
    employer = cgi.escape(self.request.get('employer'))
    user_key = ndb.Key(urlsafe=self.request.get('user_key'))
    about = cgi.escape(self.request.get('about'))
    # Decode user key
    user = user_key.get()
    user.first_name = first_name
    user.last_name = last_name
    user.profession = profession
    user.employer = employer
    user.lower_profession = profession.lower()
    user.lower_employer = employer.lower()
    if employer.lower().replace(" ", "") not in user.subscriptions:
      user.subscriptions.append(employer.lower().replace(" ", ""))
    user.lower_first_name = first_name.lower()
    user.lower_last_name = last_name.lower()
    user.put()

    #Update profile
    profile = Profile.query(Profile.owner == user.key).get()
    if profile:
      profile.about = about
      profile.put()
    self.redirect('/profile/{}'.format(user.username))

class AddSkillsHandler(SessionHandler):
  def post(self):
    user = self.user_model
    skills = cgi.escape(self.request.get('skills'))
    new_skills = skills.split(',')
    new_skills = [skill for skill in new_skills if len(skill) >0]
    to_add_skills = []
    to_add_subscriptions = []
    for i in new_skills:
      i = i.lower().strip()
      skill_query = Skill.query(Skill.name == i).get()
      if skill_query == None: # Not in skills database
        new_skill = Skill(name=i)
        new_skill_key = new_skill.put()
        print "New Skill Added to Database"
        print new_skill.name
        to_add_subscriptions.append(new_skill.name.replace(" ", ""))
        to_add_skills.append(new_skill_key)
      else: # In skills database
        # Search user skills to see if exists
        flag = " "
        for skill in user.skills:
          skill = skill.get()
          if skill.name == i:
            flag = "exists"
            print skill.name
            print "already exists in user skills"
            break
        if flag != "exists":
          new_skill = Skill.query(Skill.name == i).get()
          print("Added to user skills:")
          print(new_skill.name)
          to_add_subscriptions.append(new_skill.name.replace(" ", ""))
          to_add_skills.append(new_skill.key)
      
      # Add to user skills
    user.skills.extend(to_add_skills)
    user.skills_count += len(to_add_skills)
      # Add to user subscriptions
    user.subscriptions.extend(to_add_subscriptions)
    time.sleep(1)
    user.put()
    #self.redirect('/profile/{}'.format(user.username))


class SkillsHandler(SessionHandler):
  def post(self):
    user = self.user_model
    employer = cgi.escape(self.request.get('employer')).strip()
    profession = cgi.escape(self.request.get('job')).strip()
    field = cgi.escape(self.request.get('field')).strip()
    tools = cgi.escape(self.request.get('tools'))
    specialty = cgi.escape(self.request.get('specialty')).strip()
    tool_list = tools.split(',')
    new_skills_count = 0 #for field and specialty
    for i in tool_list:
      if i != " ":
        i = i.lower().strip()
        skill_query = Skill.query(Skill.name == i).get()
        #don't add duplicate skill
        if skill_query == None:
          new_skill = Skill(name=i)
          new_skill.put()
          user.skills.append(new_skill.key)
          user.subscriptions.append(new_skill.name.replace(" ",""))
        else:
          user.skills.append(skill_query.key)
          user.subscriptions.append(skill_query.name.replace(" ", ""))
        new_skills_count += 1
    
    # Add new User Info
    if field != "":
      field_skill = Skill(name=field.lower())
      field_skill.put()
      user.skills.append(field_skill.key)
      new_skills_count += 1
    if specialty != "":
      specialty_skill = Skill(name=specialty.lower())
      specialty_skill.put()
      user.skills.append(specialty_skill.key)
      new_skills_count += 1
    if employer != " ":
      user.employer = employer
      user.lower_employer = employer.lower()
    if profession != " ":
      user.profession = profession
      user.lower_profession = profession.lower()

    user.skills_count += new_skills_count
    user.subscriptions.append(employer.lower().replace(" ", ""))
    user.put()

class EndorsementHandler(SessionHandler):
  """ Handles endorsements from user accounts """
  def post(self):
    viewer = self.user_model
    post = cgi.escape(self.request.get('key'))
    #Person getting the endorsement
    endorsee = cgi.escape(self.request.get('endorsee'))
    text = cgi.escape(self.request.get('text'))
    skill_key = ndb.Key(urlsafe=post)
    endorsee_key = ndb.Key(urlsafe=endorsee)
    endorsement = Endorsement.query(Endorsement.endorsee == endorsee_key,
      Endorsement.skill == skill_key).get()
    if text != "empty":
      details = EndorsementDetails()
      details.endorser = viewer.key
      details.endorsee = endorsee_key
      details.skill = skill_key
      details.description = text
      details.time = datetime.datetime.now() - datetime.timedelta(hours=7) #For PST
      details.put()

    if endorsement is not None:
      endorsement.endorsers.append(viewer.key)
      endorsement.endorsement_count +=1
    else:
      endorsement = Endorsement()
      endorsement.endorsers.append(viewer.key)
      endorsement.endorsee = endorsee_key
      endorsement.skill = skill_key
      endorsement.endorsement_count +=1
    endorsement.put()

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
                               ('/endorse', EndorsementHandler),
                               ('/checkusername', CheckUsername),
                               ('/updateprofile', UpdateProfile),
                               ('/updatepicture', UpdatePicture),
                               ('/logout', LogoutHandler),
                               ('/tech', ForumViewer),
                               ('/tech/', ForumViewer),
                               ('/newskill', SkillsHandler),
                               ('/addskill', AddSkillsHandler),
                               ('/subscribe', SubscriptionHandler),
                               ('/api/tech/(\w+)', ForumAPI),
                               ('/api/tech', ForumViewerAPI),
                               ('/api/tech/', ForumViewerAPI),
                               ('/api/profile/(\w+)', ProfileHandlerAPI),
                               ('/api/search', SearchHandlerAPI),
                               ('/api/connections', DisplayConnectionsAPI),
                               ('/api/login', LoginHandlerAPI),
                               ('/api/messages', MessageHandlerAPI),
                               ('/api/feedlist', FeedListHandlerAPI),
                               ('/api/compose', ComposeMessageAPI)
                               ], debug=True, config=config)
