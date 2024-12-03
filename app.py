import os
from database.database import init_db, create_tables
DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///my_database.db')
init_db(DATABASE_URI)

from database.vehicle import Vehicle
create_tables()

from database.database import session
import flask
from flask import request
from sqlalchemy import inspect
from sqlalchemy.exc import StatementError
import json

app = flask.Flask(__name__)

vehicle_inspect = inspect(Vehicle)

VEHICLE_COLUMNS = [column.key for column in vehicle_inspect.mapper.column_attrs]
NOT_REQUIRED_COLUMNS = ['id']

def get_missing_parameters(request, parameters, not_required_columns=NOT_REQUIRED_COLUMNS):
    missing_parameters = [parameter for parameter in parameters if parameter not in request.json.keys()]
    return [parameter for parameter in missing_parameters if parameter not in not_required_columns]

def get_invalid_parameters(request, parameters):
    return [parameter for parameter in request.keys() if parameter not in parameters]

def is_malformed_json(request):
    try:
        print(request.json.keys())
        return False
    except AttributeError:
        return True
    
def malformed_json_error():
    return flask.jsonify({'error': 'Malformed JSON'}), 400

def invalid_json_error():
    return flask.jsonify({'error': 'Invalid JSON'}), 422

def parameters_error(type, parameters):
    return flask.jsonify({'error': f'{type}: {parameters}'}), 422

@app.route('/vehicle', methods=['GET','POST'])
def vehicle():
    
    if request.method == 'GET':
        # Error Checking
        invalid_parameters = get_invalid_parameters(request.args, VEHICLE_COLUMNS)
        if invalid_parameters:
            return parameters_error('Invalid parameters', invalid_parameters)
        
        # Search for vehicles that match the query parameters
        try:
            vehicles = session.query(Vehicle).filter_by(**request.args).all()
        except StatementError as e:
            return flask.jsonify({'error': f'{e.orig}'}), 422 

        return flask.jsonify([vehicle.to_dict() for vehicle in vehicles])

    elif request.method == 'POST':
        # Error Checking
        if is_malformed_json(request):
            return malformed_json_error()

        if not request.json:
            return invalid_json_error()

        invalid_parameters = get_invalid_parameters(request.json, VEHICLE_COLUMNS)
        if invalid_parameters:
            return parameters_error('Invalid parameters', invalid_parameters)
        
        missing_parameters = get_missing_parameters(request, VEHICLE_COLUMNS)
        if missing_parameters:
            return parameters_error('Missing parameters', missing_parameters)
        
        # Create a new vehicle
        try:
            # Check to see if the vehicle already exists
            vehicle = session.query(Vehicle).filter_by(vin=request.json['vin']).first()
            if vehicle:
                return flask.jsonify({'error': 'Vehicle already exists'}), 422 
        
            # Create a new vehicle object
            vehicle = Vehicle(**request.json)
    
            # Add vehicle to the database
            session.add(vehicle)
            session.commit()
        except StatementError as e:
            return flask.jsonify({'error': f'{e.orig}'}), 422 

        return flask.jsonify(vehicle.to_dict()), 201

@app.route('/vehicle/<vin>', methods=['GET','PUT','DELETE'])
def vehicle_detail(vin):
    
    
    # Check if vehicle exists
    try:
        vehicle = session.query(Vehicle).filter_by(vin=vin).first()
    except StatementError as e:
        return flask.jsonify({'error': f'{e.orig}'}), 422 
    if not vehicle:
        return flask.jsonify({'error': 'Vehicle not found'}), 404
    
    if request.method == 'GET':
        return flask.jsonify(vehicle.to_dict()), 200

    elif request.method == 'DELETE':
        session.delete(vehicle)
        session.commit()
        return flask.jsonify({'message': 'Vehicle deleted'}), 204
        
    elif request.method == 'PUT':
        if is_malformed_json(request):
            return malformed_json_error()
        
        invalid_parameters = get_invalid_parameters(request.json, VEHICLE_COLUMNS)
        if invalid_parameters:
            print(invalid_parameters)
            return parameters_error('Invalid parameters', invalid_parameters)

        for key, value in request.json.items():
            setattr(vehicle, key, value)
        
        session.commit()
        return flask.jsonify(vehicle.to_dict()), 200
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)
