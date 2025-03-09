CREATE DATABASE opcua_db;
\c opcua_db;
CREATE TABLE sensor_values (
    sensor_id VARCHAR(255) PRIMARY KEY,
    value FLOAT
);
