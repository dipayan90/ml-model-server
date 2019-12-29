from flask_restplus import Namespace, Resource, reqparse
from pypmml import Model
import os.path
from server.utils import NotFoundError, ServerError, Config, RequestError
from json import loads, JSONDecodeError

API = Namespace(
    'PMML',
    description='Loads a PMML Model and scores it')

SCORE_REQUEST_PARSER = reqparse.RequestParser()
SCORE_REQUEST_PARSER.add_argument('scorereq',
                                   type=str,
                                   required=True,
                                   location='args')


@API.route("/score")
class ScorePMML(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = Config().app_config
        if "pmml" in config:
            pmml_config = config["pmml"]
            if "path" in pmml_config:
                pmml_file_path = pmml_config["path"]
                if os.path.exists(pmml_file_path):
                    self.model = Model.fromFile(pmml_file_path)
                else:
                    raise NotFoundError(f"file: {pmml_file_path} could not be loaded")

        if not hasattr(self, 'model'):
            raise ServerError("Config file was loaded however PMML config couldn't be parsed correctly")

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
