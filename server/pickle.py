from flask_restplus import Namespace, Resource, reqparse
import dill as pickle
import os.path
from server.utils import NotFoundError, ServerError, Config, RequestError
from json import loads, JSONDecodeError

API = Namespace(
    'Pickle',
    description='Loads a Python Pickled Model and scores it')

SCORE_REQUEST_PARSER = reqparse.RequestParser()
SCORE_REQUEST_PARSER.add_argument('scorereq',
                                   type=str,
                                   required=True,
                                   location='args')


@API.route("/score")
class ScorePickle(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = Config().app_config
        if "pickle" in config:
            pickle_config = config["pickle"]
            if "path" in pickle_config:
                pickled_file_path = pickle_config["path"]
                if os.path.exists(pickled_file_path):
                    with open(pickled_file_path, 'r') as p_file:
                        try:
                            self.model = pickle.load(p_file)
                        except Exception as exp:
                            raise ServerError(
                                f"Config file was loaded however pickled file could not be loaded correctly. Error {exp}")
                    raise NotFoundError(f"file: {pickled_file_path} could not be loaded, as it doesn't exist")

    @API.expect(SCORE_REQUEST_PARSER)
    def post(self):
        scorereq: str = SCORE_REQUEST_PARSER.parse_args().get('scorereq')
        try:
            scorereq_dict = loads(scorereq)
        except JSONDecodeError as decodeError:
            raise RequestError(f"unable to decode json request with error {decodeError}")

        try:
            result = self.model.predict(data=scorereq_dict)
            return str(result)
        except Exception as scoreError:
            raise ServerError(f"Unable to score your request with error {scoreError}")
