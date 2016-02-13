#!/usr/bin/env python

def app(environ, start_response):
    '''A barebones WSGI application.

    A starting point for a web framework.
    '''
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world from a simple WSGI application!\n']
