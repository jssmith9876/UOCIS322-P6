from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
import logging
from pymongo import MongoClient
import os

app = Flask(__name__)
api = Api(app)

# Stuff for database interaction
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevetdb

def get_times():
    return list(db.brevetdb.find())

###
# APIs
###
def get_API_results(desired_keys, return_type):
    # Get the times from the db
    data = get_times()

    # Fill the result with only desired values
    desired_keys += ['miles', 'km']
    times = {}
    for entry in data:
        ind = int(entry['index'])
        times[ind] = {key: entry[key] for key in desired_keys}

    app.logger.debug(f"Got a {return_type} request")

    # Return the json
    if (return_type == 'json'):
        return jsonify(times)
    
    # Return the csv
    elif (return_type == 'csv'):
        csv_str = ",".join(desired_keys) + "\n"
        for time in times.values():
            for key in desired_keys:
                csv_str += time[key] + ","
            csv_str += "\n"
        return Response(csv_str, mimetype='text/plain')

# Returns a list of all open and close times
class listAll(Resource):
    def get(self, file_type='json'):
        return get_API_results(['open', 'close'], file_type)

# Returns a list of all open times
class listOpenOnly(Resource):
    def get(self, file_type='json'):
        return get_API_results(['open'], file_type)

# Returns a list of all close times
class listCloseOnly(Resource):
    def get(self, file_type='json'):
        return get_API_results(['close'], file_type)

# List of resources
api.add_resource(listAll, '/listAll', '/listAll/<string:file_type>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:file_type>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:file_type>')


if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)