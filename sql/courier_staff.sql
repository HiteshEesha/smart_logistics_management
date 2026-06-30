use smart_logistics;

CREATE TABLE courier_staff (
    courier_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NULL,
    rating DECIMAL(3,1) NULL,
    vehicle_type VARCHAR(50)
);