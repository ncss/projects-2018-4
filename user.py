from tornado.ncss import Server, ncssbook_log
from db import *
import os
from template import render_file


username, password = None, None

def login_handler(response):
  global username, password
  f = open(os.path.join('pages', 'login.html'))
  html = f.read()
  username = response.get_field('username')
  password = response.get_field('password')
  print(username, password)
  if username:
    print("Username Found")
    if database_login_handler(username, password):
      cookie = 'True,'+username
      response.set_secure_cookie('loggedin', cookie)
      response.redirect('/')
      print("redirected")
  else:
    rendered = render_file(os.path.join('pages', 'login.html'), {})
    response.write(rendered)

def database_login_handler(username, password):
  print("Details Accepted")
  return True

def logout_handler(response):
  response.clear_cookie('loggedin')
  response.redirect('/')
