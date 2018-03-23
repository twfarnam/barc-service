import os
from base64 import b64encode

class AuthMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        auth_headers = [
            'Token token=' + os.environ['BARC_PASSWORD'],
            'Basic ' + b64encode(
                os.environ['BARC_USERNAME'] + ':' + os.environ['BARC_PASSWORD']
            )
        ]

        if environ.get('HTTP_AUTHORIZATION', '') in auth_headers:
            return self.app(environ, start_response)
        else:
            start_response(
                '401 UNAUTHORIZED',
                [('WWW-Authenticate', 'Basic realm="Login Required"')]
            )
            return [ 'You have to login with proper credentials\n' ]



