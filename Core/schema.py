def doctor_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "doctor_name": str(item["doctor_name"]),
        "doctor_specialization": str(item["doctor_specialization"]),
        "doctor_phone_number": int(item["doctor_phone_number"]),
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


def patient_entity(item) -> dict:
    return {
        "patient_name": str(item["patient_name"]),
        "patient_age": str(item["patient_age"]),
        "patient_gender": str(item["patient_gender"]),
        "patient_address": str(item["patient_address"]),
        "patient_phone_number": int(item["patient_phone_number"]),
        "patient_email": str(item["patient_email"])
    }


def patients_entity(entity) -> list:
    return [patient_entity(item) for item in entity]
