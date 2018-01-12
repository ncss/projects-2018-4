from tornado.ncss import Server, ncssbook_log

html = '''
<html>

	<body>
	
		<form method="POST" enctype="multipart/form-data">
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
    response.write('Download Page')

    #response.write(torchic)
    print(photo)
    response.write('<img src="/photo" alt="{}">'.format(filename))  
    

def upload_handler(response):
    global filename, content_type, photo
    torchic = response.get_field('torchic')
    filename, content_type, photo = response.get_file('photo')
    if torchic == None:
        response.write(html)
    else:
        response.redirect('/view')

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
    response.set_header('Content-Type', content_type)
    response.write(photo)


server = Server()

server.register('/view', index_handler)
server.register('/', upload_handler)
server.register(r'/profile/(.+)', profile_handler)

#---------------
server.register('/photo', photo)

if __name__ == "__main__":
    server.run()
