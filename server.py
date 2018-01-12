from tornado.ncss import Server, ncssbook_log

html = '''
<html>

	<body>
	
		<form method="POST" emctype="multipart/form-data">
			<input type="text" name="torchic"><br>
			<input type="file" name="photo"><br>
			<input type="submit">
		</form>
	
	</body>

</html>
'''

content_type = ''
filename = ''
photo = ''

def index_handler(response):
    global filename, content_type, photo
    torchic = response.get_field('torchic')
    filename, content_type, photo = response.get_file('photo')
    if torchic == None:
        response.write(html)
    else:
        response.write(torchic)
        print(photo)
        response.write('<img src="/photo" alt="{}">'.format(filename))

    
    

def upload_handler(response):
    response.write('Upload Page')

def profile_handler(response, user):
    if user.lower() == 'liam':
        response.write("LIAM IS AWESOMEEEEE")
    else:
        response.write('This is the profile page of: ' + str(user))

#------------------
def photo(response):
    global content_type, photo
    print(content_type)
    print(photo)
    response.set_header('Content-Type', 'image/png')
    response.write(photo)

def list_all_photos(response):
    response.write('Hello World')
    list_of_photos = ['kevin_photo.jpg', 'dab.jpg', 'salt_bae.jpg']

    output = ''
    
    for photofile in list_of_photos:
        text_filename = photofile.replace('jpg', 'txt')
        f = open('files/' + text_filename)
        text = f.readlines()
        print(text)
        output += '<div>'
        output += '<p><b> This an awesome mem page have fun :) </b></p>'
        output += '<img src="/meme_image/{}">'.format(photofile)
        output += '<p>' + text[0] + '</p>'
        output += '<p>' + text[1] + '</p>'
        output += '<p>' + text[2] + '</p>'
        output += '<p>' + text[3] + '</p>'
        output += '</div>'
        username = text[0]
        caption = text[1]
        latitude = text[2]
        longitude = text[3]
    
    response.write(output)
    
   
def meme_image(response, filename):
    response.set_header('Content-Type', 'image/png')
    f = open('files/' + filename, 'rb')
    photo = f.read()
    response.write(photo)

server = Server()

server.register('/', index_handler)
server.register('/upload', upload_handler)
server.register(r'/profile/(.+)', profile_handler)
server.register('/list_all_photos', list_all_photos)
server.register(r'/meme_image/(.+)', meme_image)
#---------------
server.register('/photo', photo)

if __name__ == "__main__":
    server.run()
