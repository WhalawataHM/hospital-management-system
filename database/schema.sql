-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS serenity_hospital_db;
USE serenity_hospital_db;

-- Create departments table
CREATE TABLE IF NOT EXISTS departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Create staff table
CREATE TABLE IF NOT EXISTS staff (
    staff_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    department_id INT,
    contact_number VARCHAR(20),
    email VARCHAR(100),
    date_joined DATE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Create doctors table
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id VARCHAR(10) PRIMARY KEY,
    staff_id VARCHAR(10) NOT NULL,
    specialization VARCHAR(100),
    qualification TEXT,
    consultation_fee DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    contact_number VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    blood_group VARCHAR(5),
    registration_date DATE
);

-- Create appointments table
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id VARCHAR(10) PRIMARY KEY,
    patient_id VARCHAR(10),
    doctor_id VARCHAR(10),
    appointment_date DATETIME,
    department VARCHAR(100),
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Create medical records table
CREATE TABLE IF NOT EXISTS medical_records (
    record_id VARCHAR(10) PRIMARY KEY,
    patient_id VARCHAR(10),
    doctor_id VARCHAR(10),
    visit_date DATE,
    diagnosis TEXT,
    prescriptions TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Create test results table
CREATE TABLE IF NOT EXISTS test_results (
    result_id VARCHAR(10) PRIMARY KEY,
    record_id VARCHAR(10),
    test_name VARCHAR(100),
    test_date DATE,
    result TEXT,
    notes TEXT,
    FOREIGN KEY (record_id) REFERENCES medical_records(record_id)
);

-- Create RBAC authentication table
CREATE TABLE IF NOT EXISTS rbac_auth (
    username VARCHAR(50) PRIMARY KEY,
    password CHAR(12) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Admin', 'Doctor', 'Patient'))
);

-- Insert sample users
INSERT INTO rbac_auth VALUES
('198.130.1.1', 'Test_admin01', 'Admin'),
('198.130.10.1', 'Test_doc01', 'Doctor'),
('1.1.1.1', 'Test_pat01', 'Patient');
    

-- Insert some sample departments
INSERT INTO departments (name, description) VALUES
('General Medicine', 'Primary healthcare and general medical services'),
('Cardiology', 'Heart and cardiovascular system'),
('Pediatrics', 'Medical care for children and adolescents'),
('Orthopedics', 'Musculoskeletal system and injuries'),
('Neurology', 'Nervous system disorders');

