import requests
import json
import time


def test_login(username, password):
  url="http://localhost:8080/api/login"
  data={"username":username, "password": password}
  r = requests.post(url, data)
  data = r.text
  return data
def test_messages(token):
  url="http://localhost:8080/api/messages"
  params={"token":token}
  r = requests.post(url, params)
  output= r.text
  return output
def test_feed(token):
  url="http://localhost:8080/api/feedlist"
  #add items for posts
  params={"token":token, "page":0, "items":"posts"}
  r = requests.post(url, params)
  output= r.text
  return output

def main():
  response_data = test_login("newuser", "password")
  print "login"
  print response_data
  token_json = json.loads(response_data)
  time.sleep(3)
  if len(token_json) != 0:
    token = token_json[0]["token"]
    messages = test_messages(token)
    print messages
    feed = test_feed(token)
    print feed
if __name__ == '__main__':
  main()