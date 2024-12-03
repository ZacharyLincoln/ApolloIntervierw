import requests

BASE_URL = 'http://127.0.0.1:8080'

# Example GET request to /vehicle
response = requests.get(f'{BASE_URL}/vehicle', params={'manufacturer_name': 'Toyota'})
print(response.json())

# Example POST request to /vehicle
new_vehicle = {
    'vin': '1HGCM82633A123456',
    'manufacturer_name': 'Honda',
    'model_name': 'Accord',
    'model_year': 2003,
    'fuel_type': 'Gasoline',
    'purchase_price': 15000
}
response = requests.post(f'{BASE_URL}/vehicle', json=new_vehicle)
print(response.json())

# Example GET request to /vehicle/<vin>
vin = '1HGCM82633A123456'
response = requests.get(f'{BASE_URL}/vehicle/{vin}')
print(response.json())

# Example PUT request to /vehicle/<vin>
updated_vehicle = {
    'manufacturer_name': 'Honda',
    'model_name': 'Accord',
    'model_year': 2004,
    'fuel_type': 'Gasoline',
    'purchase_price': 16000
}
response = requests.put(f'{BASE_URL}/vehicle/{vin}', json=updated_vehicle)
print(response.json())

# Example GET request to /vehicle
response = requests.get(f'{BASE_URL}/vehicle', params={'manufacturer_name': 'Honda'})
print(response.json())

# Example DELETE request to /vehicle/<vin>
response = requests.delete(f'{BASE_URL}/vehicle/{vin}')
print(response.status_code)