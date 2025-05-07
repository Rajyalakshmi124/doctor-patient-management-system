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
