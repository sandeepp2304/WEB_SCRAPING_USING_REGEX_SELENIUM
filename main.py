from flask import Flask
from flask_restplus import Resource, Api, reqparse
from modules.fetch_about import AboutData
import json

app = Flask(__name__)
api = Api(app, title='Facebook Personal Information')

parser = reqparse.RequestParser()
parser.add_argument('query', type=str, help='Query name')
@api.route('/about')
class AboutFetch(Resource):
    @api.expect(parser, validate=True)
    def get(self):
        # results = dict()
        args = parser.parse_args()
        query_name = args['query']
        obj = AboutData()
        results = obj.final_result(query=query_name)

        return results


if __name__ == '__main__':
    app.run(debug=True)
