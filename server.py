from tornado.ncss import Server, ncssbook_log
from db import Category, Meme

print(Category.get_categories())
from template import render_file

content_type = ''
filename = ''
photo = ''

def photo_save(user: str, caption: str, lat: str, long: str, photo):
    '''
    This function will take information about a photo and save it to a location.
    '''
    with open('files\{} - {}.txt'.format(user, caption), 'w+') as file:
        file.write(user + "\n")
        file.write(caption + "\n")
        file.write(lat + "\n")
        file.write(long + "\n")

    with open('files\{} - {}.jpg'.format(user, caption), 'wb+') as photo_file:
        photo_file.write(photo)


def index_handler(response):
    response.write('Download Page <br>')
    response.write('<img src="/photo" alt="{}">'.format(filename))


def upload_handler(response):
    f = open('demotemplate.html', 'r')
    html = f.read()
    global filename, content_type, photo
    username = response.get_field('username')
    caption = response.get_field('caption')
    latitude = response.get_field('lat')
    longitude = response.get_field('long')
    filename, content_type, photo = response.get_file('photo')
    if username == None:
        response.write(html)
    else:
        response.redirect('/')
        print(username, caption, latitude, longitude)
        photo_save(username, caption, latitude, longitude, photo)

def profile_handler(response, user):
    if user.lower() == 'liam':
        response.write("LIAM IS AWESOMEEEEE")
    else:
        response.write('This is the profile page of: ' + str(user))

#------------------
def photo_handler(response):
    global content_type, photo
    print(content_type)
    response.set_header('Content-Type', content_type)
    response.write(photo)

def list_all_photos(response):
    list_of_photos = Meme.get_memes_for_category(3)

    output = ''

    for meme in list_of_photos:
        print(meme)
        output += '<div>'
        output += '<p><b> This an awesome meme page have fun :) </b></p>'
        output += '<img src="{}">'.format(meme.image)
        output += '<p>Username: ' + meme.username + '</p>'
        output += '<p>Caption: ' + meme.caption + '</p>'
        output += '<p>Latitude: ' + meme.latitude + '</p>'
        output += '<p>Longitude: ' + meme.longitude + '</p>'
        output += '<p>Timestamp: ' + meme.timestamp + '</p>'
        output += '</div>'

    response.write(output)


def meme_image(response, filename):
    response.set_header('Content-Type', 'image/png')
    f = open('files/' + filename, 'rb')
    photo = f.read()
    response.write(photo)


def template_example(response):
    variables = {
        'title': 'A template example',
        'friends': ['Bella', 'Joel', 'Jaxon', 'Owen']
    }
    rendered = render_file('pages/example_body.html', variables)
    response.write(rendered)


server = Server()

server.register('/', index_handler)
server.register('/upload', upload_handler)
server.register(r'/profile/(.+)', profile_handler)
server.register('/list_all_photos', list_all_photos)
server.register(r'/meme_image/(.+)', meme_image)
#---------------
server.register('/photo', photo_handler)

server.register('/template_example', template_example)

if __name__ == "__main__":
    server.run()
