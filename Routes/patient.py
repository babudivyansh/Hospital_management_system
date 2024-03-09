from bson import ObjectId
from sanic import Blueprint, response
from sanic_ext import openapi, validate
from Core.model import Patient
from Core.db import connection
from Core.schema import patients_entity
from sanic.exceptions import NotFound

app = Blueprint('patient')


# Add Patient
@app.post('/add_patient')
@openapi.definition(body={'application/json': Patient.schema()})
@validate(json=Patient)
async def add_patient(request, body):
    """
    Add a new patient to the database.

    Parameters:
        request (sanic.request.Request): The request object.
        body (dict): The request body containing patient data.

    Returns:
        sanic.response.json: JSON response indicating success or failure.
    """
    patient_data = request.json
    patient = Patient(**patient_data)

    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Insert the new patient into the database
    result = db.patient.insert_one(patient.dict())

    return response.json({'message': 'Patient added successfully', 'inserted_id': str(result.inserted_id)})


# Get Patients
@app.get('/all_patients')
async def get_patients(request):
    """
    Retrieve all patients from the database.

    Parameters:
        request (sanic.request.Request): The request object.

    Returns:
        sanic.response.json: JSON response containing patient data.
    """
    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Retrieve all patients from the database
    patients = patients_entity(db.patient.find())

    # Check if the patients list is empty
    if not patients:
        raise NotFound("Database is empty")
    return response.json(patients)


# Delete Patient
@app.delete('/delete/<patient_id:str>')
async def delete_patient(request, patient_id: str):
    """
    Delete a patient from the database.

    Parameters:
        request (sanic.request.Request): The request object.
        patient_id (str): The ID of the patient to delete.

    Returns:
        sanic.response.json: JSON response indicating success or failure.
    """
    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Check if the patient with the given ID exists in the database
    existing_patient = db.patient.find_one({'_id': ObjectId(patient_id)})

    if existing_patient is None:
        return response.json({'message': 'Patient not found'}, status=404)

    # Delete the patient from the database
    result = db.patient.delete_one({'_id': ObjectId(patient_id)})

    # Check if the delete operation was acknowledged by the server and if any documents were matched
    if result.acknowledged and result.deleted_count == 1:
        return response.json({'message': 'Patient deleted successfully'})
    else:
        return response.json({'message': 'Failed to delete patient'}, status=500)


# Update Patient
@app.put('/update/<patient_id:str>')
@openapi.definition(body={'application/json': Patient.schema()})
@validate(json=Patient)
async def update_patient(request, body, patient_id: str):
    """
    Update a patient in the database.

    Parameters:
        request (sanic.request.Request): The request object.
        body (dict): The request body containing updated patient data.
        patient_id (str): The ID of the patient to update.

    Returns:
        sanic.response.json: JSON response indicating success or failure.
    """
    # The 'body' parameter contains the parsed JSON data based on Patient schema
    patient_data = request.json

    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Check if the patient with the given ID exists in the database
    existing_patient = db.patient.find_one({'_id': ObjectId(patient_id)})

    if existing_patient is None:
        return response.json({'message': 'Patient not found'}, status=404)

    # Update the patient in the database
    result = db.patient.update_one({'_id': ObjectId(patient_id)}, {'$set': dict(patient_data)})

    # Check if the update operation was acknowledged by the server and if any documents were matched
    if result.acknowledged and result.matched_count > 0:
        return response.json({'message': 'Patient updated successfully'})
    else:
        return response.json({'message': 'Failed to update patient'}, status=500)
