from tornado.ncss import Server, ncssbook_log
import user
from datetime import datetime
from db import Category, Meme, Person, Upvote
import base64
from template import render_file
import os


def format_time(date):
    from datetime import datetime, timedelta
    import dateutil.parser

    try:
        date = dateutil.parser.parse(date) # get ISO 8601 as a datetime object
        date += timedelta(hours = 11) # add 11 hours
        cur_time = datetime.utcnow()
        cur_time += timedelta(hours = 11)
        if abs(cur_time.hour - date.hour) <= 1:
            return "Less than 1 hour ago"
        else:
            return date.strftime('%I:%M:%S %d/%m/%Y')
    except ValueError:
        return date

def get_user_from_cookie(response):
    cookie = response.get_secure_cookie('loggedin')
    if cookie:
        cookie = cookie.decode('UTF-8')
        cookie_split = str(cookie).split(',')
        return cookie_split[1]
    else:
        return 'Username not defined in cookie'

def nearby_handler(response):
    dp = 'fixme'
    photo_list = Meme.get_memes_for_category(3)
    rendered = render_file("pages/nearby.html", {
        "dp": dp,
        "photo_list": photo_list,
    })
    response.write(rendered)

def photo_save(user: str, caption: str, lat: str, long: str, base64blob):
    "This function will take information about a photo and save it to a location."


    current_time = datetime.utcnow().isoformat()
    Meme.create_meme_post(base64blob, caption, lat, long, user, current_time, 3)

def login_handler(response):
    user.login_handler(response)

def logout_handler(response):
    user.logout_handler(response)

def requires_login(handler):
    def handler_(response, *args, **kwargs):
        cookie = response.get_secure_cookie('loggedin')
        if cookie:
            cookie = cookie.decode('UTF-8')
            cookie_split = str(cookie).split(',')
            if cookie_split[0] == 'True':
                handler(response, *args, **kwargs)
            else:
                response.redirect('/login')
        else:
            response.redirect('/login')
    return handler_

@requires_login
def index_handler(response):
    response.redirect('/feed')

@requires_login
def profile_handler(response, user):
    profile_picture = '/static/test.png'
    person = Person.get_user_by_username(user)
    if not person:
        response.write('No user found with that name')
        return

    var_dict = {
        'person': person
    }
    rendered = render_file(os.path.join('pages', 'profile.html'), var_dict)
    response.write(rendered)


def signup_handler(response):
    user.signup_handler(response)
#------------------

def meme_image(response, filename):
    response.set_header('Content-Type', 'image/png')
    f = open('files/' + filename, 'rb')
    photo = f.read()
    response.write(photo)


def template_example(response):
    """An unused endpoint giving a demo of the template engine."""
    variables = {
        'title': 'A template example',
        'friends': ['Bella', 'Joel', 'Jaxon', 'Owen']
    }
    rendered = render_file('pages/example_body.html', variables)
    response.write(rendered)

@requires_login
def upload_handler(response):
    """Handles displaying the upload form, as well as recieving the data and
    entering it into the database."""
    if response.get_field("caption"):
        # The "username" field is not empty, so we are recieving data
        username = get_user_from_cookie(response)
        caption = response.get_field('caption')
        latitude = response.get_field('lat')
        longitude = response.get_field('long')
        if response.get_field('resized_image'):
            base64blob = response.get_field('resized_image')
            print("Got resized meme photo, of %d bytes in base64" % len(base64blob))
        else:
            filename, content_type, photo_blob = response.get_file('photo')
            base64blob = "data:{};base64,".format(content_type) + base64.b64encode(photo_blob).decode('ascii')
            print("Got non-resized meme photo, of %d bytes in base64" % len(base64blob))

        # Save to the database.
        photo_save(username, caption, latitude, longitude, base64blob)
        # Redirect to the feed, where they should see their new photo!
        response.redirect('/feed')
    else:
        # We need to display an upload form.
        variables = {
            'meme_of_week_img': '/static/memeOTW.jpg'
        }
        rendered = render_file('pages/upload.html', variables)
        response.write(rendered)

def index_example(response):
    response.write(render_file('pages/index.html', {}))

def nearby_handler(response):
    dp = 'https://www.transparenthands.org/wp-content/themes/transparenthands/images/donor-icon.png'
    photo_list = Meme.get_memes_for_category(3)
    rendered = render_file("pages/nearby.html", {
        "dp": dp,
        "photo_list": photo_list
    })
    response.write(rendered)

# imgsrc = 'http://i0.kym-cdn.com/entries/icons/mobile/000/006/199/responsibility12(alternate).jpg'

@requires_login
def feed_handler(response):
    dp = 'http://i0.kym-cdn.com/profiles/icons/big/000/132/880/awesome%20face%20shrug.jpg'
    photo_list = Meme.get_memes_for_category(3)
    check_upvotes_l = lambda x: check_upvote_l(x)
    imglink = "/post"
    time_func = lambda x: format_time(x)
    rendered = render_file("pages/feed.html", {
        "dp": dp,
        "photo_list": photo_list,
        "imglink": imglink,
        "time_format": time_func,
        'check_upvotes': check_upvotes_l
    })
    response.write(rendered)

def upvote_meme(response, memeid):
    Upvote.create_upvote(0, 0, int(memeid))
    response.write("Success!!")

def check_upvote(response, memeid):
    upvote_data = Upvote.get_upvotes_for_memes(memeid)
    response.write("Yay!!")
    response.write(str(len(upvote_data)))

def check_upvote_l(memeid):
    upvote_data = Upvote.get_upvotes_for_memes(memeid)
    return str(len(upvote_data))

def post_handler(response, i):
    dp = 'http://i0.kym-cdn.com/profiles/icons/big/000/132/880/awesome%20face%20shrug.jpg'
    rendered = render_file("pages/post.html", {
        "dp": dp,
        "meme": Meme.get_meme_from_id(i)
    })
    response.write(rendered)


server = Server()

server.register('/', index_handler)
server.register('/feed', feed_handler)
server.register('/upload', upload_handler)
server.register('/login', login_handler)
server.register('/logout', logout_handler)
server.register('/signup', signup_handler)
server.register(r'/post/(.+)', post_handler)
#---------------
server.register(r'/profile/(.+)', profile_handler)
server.register('/index_example', index_example)
server.register('/nearby', nearby_handler)
server.register(r'/upvote_meme/(.+)', upvote_meme)
server.register(r'/check_upvote/(.+)', check_upvote)

if __name__ == "__main__":
    server.run()
