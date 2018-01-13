from tornado.ncss import Server, ncssbook_log
from db import Person, Meme, Category
import os
from template import render_file
import base64


username, password = None, None

def login_handler(response):
  global username, password
  username = response.get_field('username')
  password = response.get_field('password')
  print(username, password)
  if username:
    if database_login_handler(username, password, response):
      cookie = 'True,'+username
      response.set_secure_cookie('loggedin', cookie)
      response.redirect('/')
  else:
    rendered = render_file(os.path.join('pages', 'login.html'), {})
    response.write(rendered)


def database_login_handler(username, password, response):
  print("Details Accepted")
  person = Person.get_user_by_username(username)
  if person:
    if person.password == password:
      return True
    else:
      response.redirect('/login')
  else:
    response.redirect('/login')

def signup_handler(response):
    username = response.get_field('username')
    password = response.get_field('password')
    bio = response.get_field('bio')
    foo, content_type, photo = response.get_file('image')
    print(username, password, bio, photo)
    if username:
        database_signup_handler(response, username, password, bio, photo, content_type)
        response.redirect('/login')
    else:
        rendered = render_file('pages/signup.html', {})
        response.write(rendered)


def database_signup_handler(response, user, password, bio, photo, type):
    print("")
    image = "data:{};base64,".format(type) + base64.b64encode(photo).decode('ascii')
    print(Person.get_user_by_username(user))
    p = Person.get_user_by_username(user)
    if p == None:
        print('Username not detected')
        Person.create_user(password, user, bio, image)
    elif p.name == user:
        print('Username detected')
        response.redirect('/signup')
    else:
        print('Username not detected')
        Person.create_user(password, user, bio, image)


def logout_handler(response):
  response.clear_cookie('loggedin')
  response.redirect('/')
