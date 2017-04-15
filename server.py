import cherrypy
import os
from helper import file_handler, status_check, config
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('./template/'))
conf = None

@cherrypy.expose
class Server(object):
    @cherrypy.expose
    def index(self):
        """
        Landing page servers
        """
        global conf
        conf = config.ConfigApp('cloudharmonics')
        template = env.get_template('index.html')
        return template.render()


@cherrypy.expose
class FileHandler(object):
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
        },
        'global': {
            'server.max_request_body_size': 0
        }
    }
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.expose
    def POST(self, contents):
        """
        This function accepts the file uploaded not more than 100MB.
        This file is recieved in format of FormData and passed to the
        POST method.
        """
        template = env.get_template('status.html')
        cherrypy.response.headers['Content-Type'] = 'text/html'
        if contents.filename:
            fh = file_handler.FileHandler(conf)
            cherrypy.session['file_name'] = contents.filename
            print("File Uploaded"+str(cherrypy.session.get('file_name')))
        if fh.save(contents.file, contents.filename):
            result = status_check.StatusCheck(conf).check_upload_status(cherrypy.session.get('file_name'))
            return template.render(rows=result)
        else:
            return error_handler('Upload error')


    @cherrypy.expose
    def GET(self):
        """
        This function helps download the file from the host.
        :return: Returns object if it is ready.
        """
        template = env.get_template('status.html')
        sc = status_check.StatusCheck(conf)
        if cherrypy.session.get('file_name'):
            results = sc.check_upload_status(cherrypy.session.get('file_name'))
        else:
            results = sc.check_status()
        #return template.render(rows=results)
        raise cherrypy.HTTPRedirect('/upload')

@cherrypy.expose
class Status(object):

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')]
        }
    }

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.expose()
    def GET(self):
        sc = status_check.StatusCheck(conf)
        template = env.get_template('status.html')
        results = sc.check_status()
        return template.render(rows=results)


def error_handler(error='Unknown error'):
    template = env.get_template('error.html')
    return template.render(error=error)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/upload': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')]
        },
        '/status': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')]
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        'global': {
            'server.max_request_body_size': 0,
            'error_page.404': error_handler,
        }
    }
    webapp = Server()
    webapp.upload = FileHandler()
    webapp.status = Status()
    cherrypy.tree.mount(FileHandler(), '/upload', FileHandler.conf)
    cherrypy.tree.mount(Status(), '/status', Status.conf)
    cherrypy.tree.mount(Server(), '/', Status.conf)
    #cherrypy.quickstart(webapp, '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
