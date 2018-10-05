#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import flask
from fibonacci import Fibonacci
import json
import logging
from log4mongo.handlers import MongoHandler
from healthcheck import HealthCheck
from requests import get
from pymongo import MongoClient
import os

class OnlyFibFilter(logging.Filter):

    def filter(self, record):
        msg = record.msg
        path = None
        try:
            path = msg.split(" ")[6]
        except:
            pass
        if not path:
            return False
        return path.startswith('/fib/')


class Server(object):
	
    MAX_ACCEPTABLE_NUMBER = config.MAX_ACCEPTABLE_NUMBER

    def __init__(self, host=config.HOST, port=config.PORT):
        self._host = host
        self._port = port
        self._app = flask.Flask(__name__)
        self._add_routes()
        self._fib = Fibonacci()
        self._init_env()
        self._init_logging()
        self._health = HealthCheck(self._app, "/health")
        self._add_mongo_check()
        self._add_fib_service_check()

    def _init_env(self):
      try:
        dockerized = os.environ['DOCKERIZED']
        self._mongo_host = 'mongo'
      except:
        self._mongo_host = 'localhost'

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
    
    def _init_logging(self):
        logger = logging.getLogger('werkzeug')
        logger.addHandler(MongoHandler(host=self._mongo_host))
        logger.addFilter(OnlyFibFilter())
        logger.setLevel(logging.INFO)
    
    def _mongo_available(self):
        client = MongoClient(host=self._mongo_host)
        client.server_info()
        return True, "mongo ok"

    def _fib_available(self):
        fib_url = 'http://127.0.0.1:8000/fib/3/5'
        res = get(fib_url)
        assert res.status_code == 200
        assert res.json() == [2, 3, 5]
        return True, "fib service ok"

    def _add_mongo_check(self):
        self._health.add_check(self._mongo_available)
    
    def _add_fib_service_check(self):
        self._health.add_check(self._fib_available)

if __name__ == '__main__': 

    server = Server()
    server.run()