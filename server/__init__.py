import datetime
import time
import uuid

from flask import Flask, g, request
from flask_restplus import Api
from server.pmml import API as PMMLNamespace
from server.utils import AppLogger, NotFoundError, ServerError, RequestError, Config
from flask_cors import CORS


class Server:

    def __init__(self,
                 base_path: str="/",
                 loglevel: str="debug",
                 port: str="8080",
                 debug: bool=True,
                 cors_origins: list=None,
                 config_file_location: str=None):
        if cors_origins is None:
            cors_origins = ["*"]
        if config_file_location is not None:
            Config(config_file_path=config_file_location)
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       version='1.0',
                       title='ML Model Server',
                       description='ML Model Server',
                       doc='/swagger'
                       )
        self.api.add_namespace(PMMLNamespace, path="{}pmml".format(base_path))
        self.base = base_path
        self.port = port
        self.debug = debug
        self.app.logger = AppLogger(log_level=loglevel).get_logger()

        CORS(
            self.app,
            resources={
                r"/*": {
                    "origins": cors_origins
                }
            },
            supports_credentials=True)

        @self.app.before_request
        def setup_request():
            g.start = time.time()
            g.API_REQUEST_ID = uuid.uuid4().hex

        @self.app.after_request
        def setup_response(response):
            now = time.time()
            duration = round(now - g.start, 2) * 1000
            current_time = datetime.datetime.fromtimestamp(now)

            # request details
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            host = request.host.split(':', 1)[0]
            self.app.logger.info(f"request from {ip_address} with host name: {host}")
            self.app.logger.info(f"request took {duration} seconds to fulfill")
            return response

        @self.api.errorhandler(NotFoundError)
        @self.api.errorhandler(RequestError)
        @self.api.errorhandler(ServerError)
        def handle_error(error):
            return error.response()

    def run(self):
        self.app.run(host="0.0.0.0", port=self.port, debug=self.debug)
