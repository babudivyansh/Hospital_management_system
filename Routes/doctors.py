from bson import ObjectId
from sanic import Blueprint, response
from sanic_ext import openapi, validate
from Core.model import Doctor
from Core.db import connection
from Core.schema import doctors_entity
from sanic.exceptions import NotFound

app = Blueprint('user')


# Add Doctor
@app.post('/register')
@openapi.definition(body={'application/json': Doctor.schema()})
@validate(json=Doctor)
async def add_doctor(request, body):
    """
    Add a new doctor to the database.

    Parameters:
    - request: The HTTP request object.
    - body: JSON data containing doctor information.

    Returns:
    A JSON response indicating the success or failure of the operation.
    """
    doctor_data = request.json
    doctor = Doctor(**doctor_data)

    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Insert the new doctor into the database
    result = db.doctor.insert_one(doctor.dict())

    return response.json({'message': 'Doctor added successfully', 'inserted_id': str(result.inserted_id)})


# Get Doctors
@app.get('/doctors')
async def get_doctors(request):
    """
    Retrieve all doctors from the database.

    Parameters:
    - request: The HTTP request object.

    Returns:
    A JSON response containing the list of doctors retrieved from the database.
    """
    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Retrieve all doctors from the database
    doctors = doctors_entity(db.doctor.find())
    # Check if the doctors list is empty
    if not doctors:
        raise NotFound("DataBase Empty!!")
    return response.json(doctors)


# Delete Doctor
@app.delete('/doctor/<doctor_id:str>')
async def delete_doctor(request, doctor_id: str):
    """
    Delete a doctor from the database.

    Parameters:
    - request: The HTTP request object.
    - doctor_id: The ID of the doctor to be deleted.

    Returns:
    A JSON response indicating the success or failure of the operation.
    """
    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Check if the doctor with the given ID exists in the database
    existing_doctor = db.doctor.find_one({'_id': ObjectId(doctor_id)})

    if existing_doctor is None:
        return response.json({'message': 'Doctor not found'}, status=404)

    # Delete the doctor from the database
    result = db.doctor.delete_one({'_id': ObjectId(doctor_id)})

    # Check if the delete operation was acknowledged by the server and if any documents were matched
    if result.acknowledged and result.deleted_count == 1:
        return response.json({'message': 'Doctor deleted successfully'})
    else:
        return response.json({'message': 'Failed to delete doctor'}, status=500)


# Update Doctor
@app.put('/doctor/<doctor_id:str>')
@openapi.definition(body={'application/json': Doctor.schema()})
@validate(json=Doctor)
async def update_doctor(request, body, doctor_id: str):
    """
    Update a doctor in the database.

    Parameters:
    - request: The HTTP request object.
    - body: JSON data containing updated doctor information.
    - doctor_id: The ID of the doctor to be updated.

    Returns:
    A JSON response indicating the success or failure of the operation.
    """
    # The 'body' parameter contains the parsed JSON data based on Doctor schema
    doctor_data = request.json

    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Check if the doctor with the given ID exists in the database
    existing_doctor = db.doctor.find_one({'_id': ObjectId(doctor_id)})

    if existing_doctor is None:
        return response.json({'message': 'Doctor not found'}, status=404)

    # Update the doctor in the database
    result = db.doctor.update_one({'_id': ObjectId(doctor_id)}, {'$set': dict(doctor_data)})

    # Check if the update operation was acknowledged by the server and if any documents were matched
    if result.acknowledged and result.matched_count > 0:
        return response.json({'message': 'Doctor updated successfully'})
    else:
        return response.json({'message': 'Failed to update doctor'}, status=500)
