from tornado.ncss import Server, ncssbook_log

def index_handler(response):
	response.write('sunflower')
	
def upload(response):
	response.write('this is the upload page :)')
	
def profile(response):
	response.write('this is the profile page :)')
	
server = Server()
server.register(r'/', index_handler)
server.register(r'/upload', upload)
server.register(r'/profile', profile)

if __name__ == '__main__':
	server.run()
