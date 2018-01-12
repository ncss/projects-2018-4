from tornado.ncss import Server, ncssbook_log
from db import Category, Meme

print(Category.get_categories())


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


server = Server()

server.register('/', index_handler)
server.register('/upload', upload_handler)
server.register(r'/profile/(.+)', profile_handler)

#---------------
server.register('/photo', photo_handler)

if __name__ == "__main__":
    server.run()
