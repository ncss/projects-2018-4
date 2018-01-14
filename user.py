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
  if username:
    if database_login_handler(username, password, response):
      cookie = 'True,'+username
      response.set_secure_cookie('loggedin', cookie)
      response.redirect('/')
  else:
    rendered = render_file(os.path.join('pages', 'login.html'), {})
    response.write(rendered)


def database_login_handler(username, password, response):
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

    if username:
        if response.get_field('resized_image'):
            base64blob = response.get_field('resized_image')
            print("Got resized profile photo, of %d bytes in base64" % len(base64blob))
        else:
            filename, content_type, photo_blob = response.get_file('image')
            base64blob = "data:{};base64,".format(content_type) + base64.b64encode(photo_blob).decode('ascii')
            print("Got non-resized profile photo, of %d bytes in base64" % len(base64blob))

        database_signup_handler(response, username, password, bio, base64blob)
        if database_login_handler(username, password, response):
            cookie = 'True,'+username
            response.set_secure_cookie('loggedin', cookie)
            response.redirect('/')
    else:
        rendered = render_file('pages/signup.html', {})
        response.write(rendered)


def database_signup_handler(response, user, password, bio, base64blob):
    p = Person.get_user_by_username(user)
    if p == None:
        Person.create_user(password, user, bio, base64blob)
    elif p.name == user:
        response.redirect('/signup')
    else:
        Person.create_user(password, user, bio, base64blob)


def logout_handler(response):
  response.clear_cookie('loggedin')
  response.redirect('/')
