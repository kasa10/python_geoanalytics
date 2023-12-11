CREATE DATABASE IF NOT EXISTS geosurf;
USE geosurf;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password VARCHAR(800) NOT NULL,
    user_type VARCHAR(255) NOT NULL
) ENGINE=InnoDB;