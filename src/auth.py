import os
from base64 import standard_b64encode

class AuthMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        auth_vars = os.environ['BARC_USERNAME'] + ':' + os.environ['BARC_PASSWORD']
        auth_headers = [
            'Token token=' + os.environ['BARC_PASSWORD'],
            'Basic %s' % standard_b64encode(auth_vars.encode()).decode("utf-8") 
        ]

        if environ.get('HTTP_AUTHORIZATION', '') in auth_headers:
            return self.app(environ, start_response)
        else:
            start_response(
                '401 UNAUTHORIZED',
                [('WWW-Authenticate', 'Basic realm="Login Required"')]
            )
            return [ b'You have to login with proper credentials\n' ]



