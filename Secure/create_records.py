from django.contrib.auth.models import User
from .models import SecureRecord

# Assume users already exist
admin = User.objects.get(username='admin')
analyst = User.objects.get(username='analyst')
doctor = User.objects.get(username='doctor')

records = [
    SecureRecord(
        name="Employee Payroll - March 2026",
        secret_data="Encrypted: Salary details, bonuses, tax deductions for all employees. Access restricted to HR and Finance.",
        created_by=admin
    ),
    SecureRecord(
        name="Customer Credit Card Token Vault",
        secret_data="Tokenized card data with masked PAN (**** **** **** 4582), expiry, and encrypted CVV references.",
        created_by=analyst
    ),
    SecureRecord(
        name="Patient Medical Record - ID 78421",
        secret_data="Diagnosis: Type 2 Diabetes. Prescriptions: Metformin 500mg. Notes encrypted under HIPAA compliance.",
        created_by=doctor
    ),
    SecureRecord(
        name="API Secret Keys - Production",
        secret_data="AWS_ACCESS_KEY=****, AWS_SECRET_KEY=****, JWT_SECRET=****. Stored using AES-256 encryption.",
        created_by=admin
    ),
    SecureRecord(
        name="Confidential Legal Document",
        secret_data="Contract draft between Company A and Vendor B. Contains NDA clauses and pricing terms.",
        created_by=analyst
    ),
    SecureRecord(
        name="System Audit Logs - Security Incident",
        secret_data="Unauthorized login attempts detected from IP 192.168.1.45. Logs encrypted and integrity verified.",
        created_by=admin
    ),
    SecureRecord(
        name="Biometric Authentication Templates",
        secret_data="Fingerprint hash templates stored using salted hashing and secure enclave processing.",
        created_by=analyst
    ),
    SecureRecord(
        name="Internal Research Data",
        secret_data="Prototype algorithm performance metrics and experimental results. Access limited to R&D team.",
        created_by=doctor
    ),
]