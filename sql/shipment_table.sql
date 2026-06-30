use smart_logistics;

CREATE TABLE shipment (
    shipment_id VARCHAR(50) PRIMARY KEY,
    order_date DATE NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    weight DECIMAL(10,2) NULL,
    courier_id VARCHAR(50) not null,
    status VARCHAR(50) not null,
    delivery_date DATE
);


ALTER TABLE shipment
ADD CONSTRAINT FK_Shipment_Courier
FOREIGN KEY (courier_id)
REFERENCES courier_staff(courier_id);



