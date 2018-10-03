#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import flask
from fibonacci import Fibonacci
import json

class Server(object):
	
    MAX_ACCEPTABLE_NUMBER = config.MAX_ACCEPTABLE_NUMBER

    def __init__(self, host=config.HOST, port=config.PORT):
        self._host = host
        self._port = port
        self._app = flask.Flask(__name__)
        self._add_routes()
        self._fib = Fibonacci()

    def index(self):
        msg = ('Currently two API endpoints are supported:\n\n'
                'GET /fib/<start_idx>/<end_idx>\n'
                'GET /health\n')
        return msg, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    def fib(self, start, end):
        # invalid values
        try:
            n1 = int(start)
            n2 = int(end)
        except ValueError:
            return self._response(400)
        if n1 < 0 or n2 < 0:
            return self._response(400)
        if n2 < n1:
            return self._response(400)
        # Payload too large
        if n1 > self.MAX_ACCEPTABLE_NUMBER or n2 > self.MAX_ACCEPTABLE_NUMBER:
            return self._response(413)

        try:
            seq = self._fib.sequence(n1, n2)
            return self._response(200, seq)
        except:
            return self._response(500)

    def _response(self, status, data=None):
        data = data or []
        return flask.Response(json.dumps(data), status=status,
                        mimetype='application/json')

    def run(self):
        self._app.run(host=self._host, port=self._port, threaded=True)

    def _add_routes(self):
        self._app.add_url_rule('/', endpoint='index', view_func=self.index)
        self._app.add_url_rule(
            '/fib/<start>/<end>', endpoint='fib', view_func=self.fib)

    def _test_client(self):
        return self._app.test_client()

if __name__ == '__main__': 

    server = Server()
    server.run()