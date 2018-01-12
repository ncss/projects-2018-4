from tornado.ncss import Server, ncssbook_log

from template import render_file

def template_example(response):
    variables = {
        'title': 'A template example',
        'friends': ['Bella', 'Joel', 'Jaxon', 'Owen']
    }
    rendered = render_file('pages/example_body.html', variables)
    response.write(rendered)

def index_handler(response):
    response.write('Download Page <br>')
    response.write('<img src="/photo" alt="{}">'.format(filename))

server = Server()
server.register('/', index_handler)
server.register('/template_example', template_example)

if __name__ == "__main__":
    server.run()
