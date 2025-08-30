import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root@123"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS serenity_hospital_db")
            cursor.execute("USE serenity_hospital_db")
            
            # Create tables
            create_tables = [
                """
                CREATE TABLE IF NOT EXISTS branches (
                    branch_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    location VARCHAR(100) NOT NULL,
                    contact_number VARCHAR(20),
                    email VARCHAR(100)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS departments (
                    department_id INT PRIMARY KEY AUTO_INCREMENT,
                    branch_id INT,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS staff (
                    staff_id VARCHAR(10) PRIMARY KEY,
                    department_id INT,
                    name VARCHAR(100) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    contact_number VARCHAR(20),
                    email VARCHAR(100),
                    date_joined DATE,
                    FOREIGN KEY (department_id) REFERENCES departments(department_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id VARCHAR(10) PRIMARY KEY,
                    staff_id VARCHAR(10),
                    specialization VARCHAR(100),
                    qualification TEXT,
                    consultation_fee DECIMAL(10,2),
                    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    date_of_birth DATE,
                    gender VARCHAR(10),
                    blood_group VARCHAR(5),
                    contact_number VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    insurance_details TEXT
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id VARCHAR(10) PRIMARY KEY,
                    patient_id VARCHAR(10),
                    doctor_id VARCHAR(10),
                    appointment_date DATETIME,
                    status VARCHAR(20),
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS medical_records (
                    record_id VARCHAR(10) PRIMARY KEY,
                    patient_id VARCHAR(10),
                    doctor_id VARCHAR(10),
                    visit_date DATE,
                    diagnosis TEXT,
                    prescription TEXT,
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS resources (
                    resource_id VARCHAR(10) PRIMARY KEY,
                    branch_id INT,
                    type VARCHAR(50),
                    name VARCHAR(100),
                    status VARCHAR(20),
                    last_maintenance DATE,
                    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
                )
                """
            ]
            
            for query in create_tables:
                cursor.execute(query)
                
            # Insert default branches
            insert_branches = """
            INSERT INTO branches (name, location, contact_number, email) 
            VALUES 
                ('Serenity Health Colombo', 'Colombo', '+94112345678', 'colombo@serenityhealth.lk'),
                ('Serenity Health Negombo', 'Negombo', '+94312345678', 'negombo@serenityhealth.lk'),
                ('Serenity Health Kandy', 'Kandy', '+94812345678', 'kandy@serenityhealth.lk')
            """
            try:
                cursor.execute(insert_branches)
                connection.commit()
            except Error as e:
                if e.errno != 1062:  # Ignore duplicate entry errors
                    print(f"Error inserting default branches: {e}")
            
            print("Database and tables created successfully!")
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    create_database()
