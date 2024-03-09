from typing import Optional
from pydantic import BaseModel


class Department(BaseModel):
    department_name: str
    department_address: str
    description: str
    head_of_department: str
    number_of_staff: int
    capacity: int
    department_phone: int


class Patient(BaseModel):
    patient_name: str
    patient_age: int
    patient_gender: str
    patient_address: str
    patient_phone_number: int
    patient_email: Optional[str] = None


class Doctor(BaseModel):
    doctor_name: str
    doctor_specialization: str
    doctor_phone_number: int
    doctor_email: Optional[str] = None


class MedicalAppointment(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    appointment_time: str
    purpose: str
    notes: Optional[str] = None
