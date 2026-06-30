use smart_logistics;

CREATE TABLE routes(
route_id VARCHAR(50) PRIMARY KEY,
origin VARCHAR(100),
destination VARCHAR(100),
distance_km DECIMAL(10,2),
avg_time_hours DECIMAL(5,2)
);