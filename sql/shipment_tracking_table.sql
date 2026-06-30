use smart_logistics;

CREATE TABLE shipment_tracking(
  tracking_id INT AUTO_INCREMENT PRIMARY KEY,
  shipment_id VARCHAR(50) NOT NULL,
  status VARCHAR(50) not null,
  timestamp DATETIME ,
  
CONSTRAINT FK_Shipment
FOREIGN KEY(shipment_id)
REFERENCES shipment(shipment_id)
);



CREATE INDEX IX_shipment_tracking_shipment_id
ON shipment_tracking(shipment_id);