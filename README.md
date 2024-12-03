

Endpoints
1. /vehicle
GET

Fetch vehicles matching query parameters.

    Query Parameters: Any column from the Vehicle table.
    Response:
        200 OK: Returns a list of vehicles matching the query.
        422 Unprocessable Entity: Invalid query parameter or database error.


POST

Create a new vehicle.

    Body Parameters (JSON): Must include all required fields from the Vehicle table except id.
    Response:
        201 Created: Returns the created vehicle.
        400 Malformed JSON: The request body is not a valid JSON.
        422 Unprocessable Entity: Missing or invalid parameters, or the vehicle already exists.


2. /vehicle/<vin>
GET

Retrieve details of a specific vehicle by its VIN.

    Response:
        200 OK: Returns the vehicle details.
        404 Not Found: Vehicle not found.

PUT

Update details of a specific vehicle by its VIN.

    Body Parameters (JSON): Any updatable fields of the Vehicle table.
    Response:
        200 OK: Returns the updated vehicle.
        400 Malformed JSON: The request body is not a valid JSON.
        404 Not Found: Vehicle not found.


DELETE

Delete a vehicle by its VIN.

    Response:
        204 No Content: Vehicle successfully deleted.
        404 Not Found: Vehicle not found.


Setup docker container
    

    docker compose up -d



Error Handling

The API handles the following error scenarios:

    Malformed JSON (400): Returned if the request body is not a valid JSON.
    Invalid Parameters (422): Returned if invalid or missing parameters are provided.
    Database Errors (422): Returned if there are issues with the database query.
    Not Found (404): Returned if a requested vehicle does not exist.