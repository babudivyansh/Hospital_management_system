from bson import ObjectId
from sanic import Blueprint, response
from sanic_ext import openapi, validate
from Core.model import Department
from Core.db import connection
from Core.schema import departments_entity
from sanic.exceptions import NotFound

app = Blueprint('department')


# Add Department
@app.post('/add')
@openapi.definition(body={'application/json': Department.schema()})
@validate(json=Department)
async def add_department(request, body):
    """
    Add a new department to the database.

    Parameters:
        request (sanic.request.Request): The request object.
        body (dict): The request body containing department data.

    Returns:
        sanic.response.json: JSON response indicating success or failure.
    """
    department_data = request.json
    department = Department(**department_data)

    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Insert the new department into the database
    result = db.department.insert_one(department.dict())

    return response.json({'message': 'Department added successfully', 'inserted_id': str(result.inserted_id)})


# Get Departments
@app.get('/all')
async def get_departments(request):
    """
    Retrieve all departments from the database.

    Parameters:
        request (sanic.request.Request): The request object.

    Returns:
        sanic.response.json: JSON response containing department data.
    """
    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Retrieve all departments from the database
    departments = departments_entity(db.department.find())

    # Check if the departments list is empty
    if not departments:
        raise NotFound("DataBase Empty!!")
    return response.json(departments)


# Delete Department
@app.delete('/<department_id:str>')
async def delete_department(request, department_id: str):
    """
    Delete a department from the database.

    Parameters:
        request (sanic.request.Request): The request object.
        department_id (str): The ID of the department to delete.

    Returns:
        sanic.response.json: JSON response indicating success or failure.
    """
    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Check if the department with the given ID exists in the database
    existing_department = db.department.find_one({'_id': ObjectId(department_id)})

    if existing_department is None:
        return response.json({'message': 'Department not found'}, status=404)

    # Delete the department from the database
    result = db.department.delete_one({'_id': ObjectId(department_id)})

    # Check if the delete operation was acknowledged by the server and if any documents were matched
    if result.acknowledged and result.deleted_count == 1:
        return response.json({'message': 'Department deleted successfully'})
    else:
        return response.json({'message': 'Failed to delete department'}, status=500)


# Update Department
@app.put('/<department_id:str>')
@openapi.definition(body={'application/json': Department.schema()})
@validate(json=Department)
async def update_department(request, body, department_id: str):
    """
   Update a department in the database.

   Parameters:
       request (sanic.request.Request): The request object.
       body (dict): The request body containing updated department data.
       department_id (str): The ID of the department to update.

   Returns:
       sanic.response.json: JSON response indicating success or failure.
   """
    # The 'body' parameter contains the parsed JSON data based on Department schema
    department_data = request.json

    # Establish connection to MongoDB
    db = connection['hospital']  # Access your database from the connection

    # Check if the department with the given ID exists in the database
    existing_department = db.department.find_one({'_id': ObjectId(department_id)})

    if existing_department is None:
        return response.json({'message': 'Department not found'}, status=404)

    # Update the department in the database
    result = db.department.update_one({'_id': ObjectId(department_id)}, {'$set': dict(department_data)})

    # Check if the update operation was acknowledged by the server and if any documents were matched
    if result.acknowledged and result.matched_count > 0:
        return response.json({'message': 'Department updated successfully'})
    else:
        return response.json({'message': 'Failed to update department'}, status=500)
