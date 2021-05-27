from flask import Flask
from flask_restful import Resource, Api
from brevets.acp_db import get_times
import logging

app = Flask(__name__)
api = Api(app)

###
# APIs
###
# class test(Resource):
#     def get(self):
#         return "Nice"

# api.add_resource(test, '/test')

@api.representation('application/json')
def return_json(data):
    return flask.jsonify(data)

@api.representation('application/csv')
def return_csv(data, headers):
    return data

def get_API_results(desired_keys, return_type):
    # Get the times from the db
    data = get_times()

    # Fill the result with only opening and closing times
    times = {}
    for entry in data:
        ind = int(entry['index'])
        times[ind] = {key: entry[key] for key in desired_keys}

    # Return the json
    app.logger.debug(f"Got a {return_type} request")
    if (return_type == 'json'):
        return return_json(times)
    # Return csv
    elif (return_type == 'csv'):
        return return_csv(times, desired_keys)

# Returns a json list of all open and close times
class listAll(Resource):
    def get(self, file_type='json'):
        return get_API_results(['open', 'close'], file_type)

# Returns a json list of all open times
class listOpenOnly(Resource):
    def get(self, file_type='json'):
        return get_API_results(['open'], file_type)

# Returns a json list of all close times
class listCloseOnly(Resource):
    def get(self, file_type='json'):
        return get_API_results(['close'], file_type)

# Default list all
api.add_resource(listAll, '/listAll')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:file_type>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:file_type>')

# Specified list all
# api.add_resource(listAll, '/listAll/<string:file_type>')
# api.add_resource(listOpenOnly, '/listOpenOnly/<string:file_type>')
# api.add_resource(listCloseOnly, '/listCloseOnly/<string:file_type>')

if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)