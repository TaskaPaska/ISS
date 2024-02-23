DROP TABLE IF EXISTS satellite;
CREATE TABLE satellite (
    satellite_name VARCHAR(255),
    satellite_id INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    altitude DOUBLE PRECISION,
    velocity DOUBLE PRECISION,
    visibility VARCHAR(255),
    footprint DOUBLE PRECISION,
    timestamp TIMESTAMP,
    daynum INTEGER,
    solar_lat DOUBLE PRECISION,
    solar_lon DOUBLE PRECISION,
    units VARCHAR(255)
);