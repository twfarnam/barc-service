import os
import flask


def token_auth(auth_header):
    return auth_header == 'Token token=' + os.environ['BARC_PASSWORD']


def simple_auth():
    auth = flask.request.authorization
    return (
        auth and 
        auth.username == os.environ['BARC_USERNAME'] and
        auth.password == os.environ['BARC_PASSWORD']
    )


def authorize():
    return flask.Response(
        'You have to login with proper credentials',
        401,
        { 'WWW-Authenticate': 'Basic realm="Login Required"' }
    )



