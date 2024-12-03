import os
TEST_DATABASE_URI = 'sqlite:///test_database.db'
os.environ['DATABASE_URI'] = TEST_DATABASE_URI

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base, init_db, drop_tables, create_tables
from app import app, session as db_session
from database.vehicle import Vehicle

@pytest.fixture(scope='module')
def test_client():

    # Create a test client
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

    # Tear down the test database
    drop_tables()

@pytest.fixture(scope='function')
def session():
    # Create a new session for each test
    engine = create_engine(TEST_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Drop and recreate tables before each test
    drop_tables()
    create_tables()
    
    yield session
    session.close()

def test_get_vehicle_empty_db(test_client):
    response = test_client.get('/vehicle')
    assert response.status_code == 200
    assert response.json == []

def test_post_vehicle(test_client, session):
    new_vehicle = {
        'vin': '1HGCM82633A123456',
        'manufacturer_name': 'Honda',
        'model_name': 'Accord',
        'model_year': 2003,
        'fuel_type': 'Gasoline',
        'purchase_price': 5000
    }
    response = test_client.post('/vehicle', json=new_vehicle)
    assert response.status_code == 201
    assert response.json['vin'] == new_vehicle['vin']

def test_post_vehicle_missing_parameters(test_client):
    new_vehicle = {
        'vin': '1HGCM82633A123456',
        'manufacturer_name': 'Honda'
    }
    response = test_client.post('/vehicle', json=new_vehicle)
    assert response.status_code == 422
    assert 'Missing parameters' in response.json['error']

def test_post_vehicle_invalid_parameters(test_client):
    new_vehicle = {
        'vin': '1HGCM82633A123456',
        'manufacturer_name': 'Honda',
        'model_name': 'Accord',
        'model_year': 2003,
        'fuel_type': 'Gasoline',
        'purchase_price': 5000,
        'invalid_param': 'invalid'
    }
    response = test_client.post('/vehicle', json=new_vehicle)
    assert response.status_code == 422
    assert 'Invalid parameters' in response.json['error']

def test_get_vehicle(test_client, session):
    new_vehicle = Vehicle(
        vin='1HGCM82633A123456',
        manufacturer_name='Honda',
        model_name='Accord',
        model_year=2003,
        fuel_type='Gasoline',
        purchase_price=5000
    )
    session.add(new_vehicle)
    session.commit()

    response = test_client.get('/vehicle', query_string={'vin': '1HGCM82633A123456'})
    assert response.status_code == 200
    assert response.json[0]['vin'] == new_vehicle.vin

def test_put_vehicle(test_client, session):
    new_vehicle = Vehicle(
        vin='1HGCM82633A123456',
        manufacturer_name='Honda',
        model_name='Accord',
        model_year=2003,
        fuel_type='Gasoline',
        purchase_price=5000
    )
    session.add(new_vehicle)
    session.commit()

    updated_data = {
        'manufacturer_name': 'Toyota',
        'model_name': 'Camry',
        'model_year': 2005,
        'fuel_type': 'Hybrid',
        'purchase_price': 7000
    }
    response = test_client.put('/vehicle/1HGCM82633A123456', json=updated_data)
    assert response.status_code == 200
    assert response.json['manufacturer_name'] == 'Toyota'

def test_delete_vehicle(test_client, session):
    new_vehicle = Vehicle(
        vin='1HGCM82633A123456',
        manufacturer_name='Honda',
        model_name='Accord',
        model_year=2003,
        fuel_type='Gasoline',
        purchase_price=5000
    )
    session.add(new_vehicle)
    session.commit()

    response = test_client.delete('/vehicle/1HGCM82633A123456')
    assert response.status_code == 204

    response = test_client.get('/vehicle', query_string={'vin': '1HGCM82633A123456'})
    assert response.status_code == 200
    assert response.json == []

def test_post_vehicle_duplicate_vin(test_client, session):
    new_vehicle = {
        'vin': '1HGCM82633A123456',
        'manufacturer_name': 'Honda',
        'model_name': 'Accord',
        'model_year': 2003,
        'fuel_type': 'Gasoline',
        'purchase_price': 5000
    }
    session.add(Vehicle(**new_vehicle))
    session.commit()

    response = test_client.post('/vehicle', json=new_vehicle)
    assert response.status_code == 422
    assert 'Vehicle already exists' in response.json['error']

def test_get_vehicle_invalid_parameter(test_client):
    response = test_client.get('/vehicle', query_string={'invalid_param': 'invalid'})
    assert response.status_code == 422
    assert 'Invalid parameters' in response.json['error']

def test_put_vehicle_invalid_vin(test_client):
    updated_data = {
        'manufacturer_name': 'Toyota',
        'model_name': 'Camry',
        'model_year': 2005,
        'fuel_type': 'Hybrid',
        'purchase_price': 7000
    }
    response = test_client.put('/vehicle/INVALIDVIN', json=updated_data)
    assert response.status_code == 422 
    assert 'Invalid VIN' in response.json['error']

def test_put_vehicle_invalid_parameters(test_client, session):
    new_vehicle = Vehicle(
        vin='1HGCM82633A123456',
        manufacturer_name='Honda',
        model_name='Accord',
        model_year=2003,
        fuel_type='Gasoline',
        purchase_price=5000
    )
    session.add(new_vehicle)
    session.commit()

    updated_data = {
        'invalid_param': 'invalid'
    }
    response = test_client.put('/vehicle/1HGCM82633A123456', json=updated_data)
    assert response.status_code == 422
    assert 'Invalid parameters' in response.json['error']

def test_delete_vehicle_invalid_vin(test_client):
    response = test_client.delete('/vehicle/INVALIDVIN')
    assert response.status_code == 422 
    assert 'Invalid VIN' in response.json['error']

def test_post_vehicle_malformed_json(test_client):
    response = test_client.post('/vehicle', json='{"vin": "1HGCM82633A123456", "manufacturer_name": "Honda"')
    assert response.status_code == 400
    assert 'Malformed JSON' in response.json['error']

def test_put_vehicle_malformed_json(test_client, session):
    new_vehicle = Vehicle(
        vin='1HGCM82633A123456',
        manufacturer_name='Honda',
        model_name='Accord',
        model_year=2003,
        fuel_type='Gasoline',
        purchase_price=5000
    )
    session.add(new_vehicle)
    session.commit()

    response = test_client.put('/vehicle/1HGCM82633A123456', json='{"manufacturer_name": "Toyota"')
    assert response.status_code == 400
    assert 'Malformed JSON' in response.json['error']