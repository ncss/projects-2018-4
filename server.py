from tornado.ncss import Server, ncssbook_log
from db import Category, Meme
import base64

print(Category.get_categories())
from template import render_file

def photo_save(user: str, caption: str, lat: str, long: str, content_type, photo):
    "This function will take information about a photo and save it to a location."

    photo = "data:{};base64,".format(content_type) + base64.b64encode(photo).decode('ascii')
    Meme.create_meme_post(photo, caption, lat, long, user, 'timestamp', 3)


def index_handler(response):
    response.redirect('/feed')

def profile_handler(response, user):
    if user.lower() == 'liam':
        response.write("LIAM IS AWESOMEEEEE")
    else:
        response.write('This is the profile page of: ' + str(user))

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

def upload_handler(response):
    """Handles displaying the upload form, as well as recieving the data and
    entering it into the database."""
    if response.get_field("username"):
        # The "username" field is not empty, so we are recieving data
        username = response.get_field('username')
        caption = response.get_field('caption')
        latitude = response.get_field('lat')
        longitude = response.get_field('long')
        filename, content_type, photo_blob = response.get_file('photo')

        # Save to the database.
        photo_save(username, caption, latitude, longitude, content_type, photo_blob)
        # Redirect to the feed, where they should see their new photo!
        response.redirect('/feed')
    else:
        # We need to display an upload form.
        variables = {
            'meme_of_week_img': '/static/test.png'
        }
        rendered = render_file('pages/upload.html', variables)
        response.write(rendered)

def index_example(response):
    response.write(render_file('pages/index.html', {}))

# imgsrc = 'http://i0.kym-cdn.com/entries/icons/mobile/000/006/199/responsibility12(alternate).jpg'

def feed_handler(response):
    dp = 'https://www.transparenthands.org/wp-content/themes/transparenthands/images/donor-icon.png'
    photo_list = Meme.get_memes_for_category(3)
    imglink = "/post"
    rendered = render_file("pages/feed.html", {
        "dp": dp,
        "photo_list": photo_list,
        "imglink": imglink
    })
    response.write(rendered)

def meme_page_handler(response, i):
    dp = 'https://www.transparenthands.org/wp-content/themes/transparenthands/images/donor-icon.png'
    photo_list = Meme.get_memes_for_category(3)
    rendered = render_file("pages/meme_pages.html", {
        "dp": dp,
        "meme": photo_list[int(i)]
    })
    response.write(rendered)


server = Server()

server.register('/', index_handler)
server.register('/feed', feed_handler)
server.register('/upload', upload_handler)
#---------------
server.register(r'/profile/(.+)', profile_handler)
server.register(r'/post/(.+)', meme_page_handler)
server.register('/index_example', index_example)

if __name__ == "__main__":
    server.run()
