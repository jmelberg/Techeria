import requests


def test_login(username, password):
  url="http://localhost:8080/api/login"
  data={"username":username, "password": password}
  r = requests.post(url, data)
  data = r.text
  return data


def main():
  response_data = test_login("newuser", "password")
  print response_data
if __name__ == '__main__':
  main()