USE trainingPoc;

CREATE TABLE IF NOT EXISTS doctor (
    id VARCHAR(36) PRIMARY KEY,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    department VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS patient (
    id VARCHAR(36) PRIMARY KEY,
    firstName VARCHAR(255),
    lastName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS doctorpatientassignment (
    id VARCHAR(36) PRIMARY KEY,
    doctorId VARCHAR(36),
    patientId VARCHAR(36),
    dateOfAdmission DATE,
    is_unassigned BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (doctorId) REFERENCES doctor(id) ON DELETE CASCADE,
    FOREIGN KEY (patientId) REFERENCES patient(id) ON DELETE CASCADE
);
