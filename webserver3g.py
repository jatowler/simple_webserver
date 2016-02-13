#!/usr/bin env python3
'''Zombie-killing web server that stays alive.

Re-start accept() after zombie-killing interruption.
'''

import errno
import os
import signal
import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5


def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,  # any child
                os.WNOHANG)  # do not block
        except OSError:
            return

        if pid == 0:  # no more zombies
            return


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print request.decode()

    http_response = b'''\
HTTP/1.1 200 OK

Hello, World!
'''
    client_connection.sendall(http_response)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET,
                             socket.SOCK_STREAM,
                             1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print 'Serving HTTP on port {port} ...'.format(port=PORT)

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            # Restart 'accept' if it was interrupted
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()
        if pid == 0:  # we are the child
            listen_socket.close()
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)  # child exits here
        else:  # we are the parent
            client_connection.close()  # close parent copy and loop


if __name__ == '__main__':
    serve_forever()
