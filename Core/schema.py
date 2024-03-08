def doctor_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "doctor_name": str(item["doctor_name"]),
        "doctor_specialization": str(item["doctor_specialization"]),
        "doctor_phone_number": str(item["doctor_phone_number"]),
        "doctor_email": str(item["doctor_email"])
    }


def doctors_entity(entity) -> list:
    return [doctor_entity(item) for item in entity]


def department_entity(item) -> dict:
    return {
        "department_name": str(item["department_name"]),
        "department_address": str(item["department_address"]),
        "description": str(item["description"]),
        "head_of_department": str(item["head_of_department"]),
        "number_of_staff": int(item["number_of_staff"]),
        "capacity": int(item["capacity"]),
        "department_phone": int(item["department_phone"])
    }


def departments_entity(entity) -> list:
    return [department_entity(item) for item in entity]
