use smart_logistics;
create table costs(
shipment_id VARCHAR(50) PRIMARY KEY,
fuel_cost DECIMAL(15,2),
labor_cost DECIMAL(15,2),
misc_cost DECIMAL(15,2)
);