/**********************************************************************
    LOGISTICS DASHBOARD KPI QUERIES
**********************************************************************/

---------------------------------------------------------
-- 1. Total Shipments
---------------------------------------------------------

SELECT COUNT(*) AS total_shipments
FROM shipments;

---------------------------------------------------------
-- 2. Delivered Shipments
---------------------------------------------------------

SELECT COUNT(*) AS delivered_shipments
FROM shipments
WHERE status='Delivered';

---------------------------------------------------------
-- 3. In Transit Shipments
---------------------------------------------------------

SELECT COUNT(*) AS in_transit_shipments
FROM shipments
WHERE status='In Transit';

---------------------------------------------------------
-- 4. Pending Shipments
---------------------------------------------------------

SELECT COUNT(*) AS pending_shipments
FROM shipments
WHERE status='Pending';

---------------------------------------------------------
-- 5. Cancelled Shipments
---------------------------------------------------------

SELECT COUNT(*) AS cancelled_shipments
FROM shipments
WHERE status='Cancelled';

---------------------------------------------------------
-- 6. Delivery Success Rate
---------------------------------------------------------

SELECT
ROUND(
(
COUNT(CASE
WHEN status='Delivered'
THEN 1 END)

*100.0

/

COUNT(*)

),2)

AS delivery_success_rate
FROM shipments;

---------------------------------------------------------
-- 7. Average Delivery Time
---------------------------------------------------------

SELECT

ROUND(

AVG(

DATEDIFF(
delivery_date,
order_date
)

),2)

AS avg_delivery_days

FROM shipments

WHERE delivery_date IS NOT NULL;

---------------------------------------------------------
-- 8. Total Shipment Weight
---------------------------------------------------------

SELECT

SUM(weight)

AS total_weight

FROM shipments;

---------------------------------------------------------
-- 9. Average Shipment Weight
---------------------------------------------------------

SELECT

ROUND(

AVG(weight),

2

)

AS avg_weight

FROM shipments;

---------------------------------------------------------
-- 10. Heaviest Shipment
---------------------------------------------------------

SELECT *

FROM shipments

ORDER BY weight DESC

LIMIT 1;

---------------------------------------------------------
-- 11. Shipments by Status
---------------------------------------------------------

SELECT

status,

COUNT(*) total

FROM shipments

GROUP BY status;

---------------------------------------------------------
-- 12. Shipments by Origin
---------------------------------------------------------

SELECT

origin,

COUNT(*) total_shipments

FROM shipments

GROUP BY origin

ORDER BY total_shipments DESC;

---------------------------------------------------------
-- 13. Shipments by Destination
---------------------------------------------------------

SELECT

destination,

COUNT(*) total_shipments

FROM shipments

GROUP BY destination

ORDER BY total_shipments DESC;

---------------------------------------------------------
-- 14. Monthly Shipment Trend
---------------------------------------------------------

SELECT

DATE_FORMAT(order_date,'%Y-%m') Month,

COUNT(*) Shipments

FROM shipments

GROUP BY Month

ORDER BY Month;

---------------------------------------------------------
-- 15. Top 10 Couriers by Shipment Count
---------------------------------------------------------

SELECT

c.courier_id,

c.name,

COUNT(s.shipment_id)

AS shipment_count

FROM courier_staff c

JOIN shipments s

ON c.courier_id=s.courier_id

GROUP BY

c.courier_id,

c.name

ORDER BY shipment_count DESC

LIMIT 10;

---------------------------------------------------------
-- 16. Average Courier Rating
---------------------------------------------------------

SELECT

ROUND(

AVG(rating),

2

)

AS average_rating

FROM courier_staff;

---------------------------------------------------------
-- 17. Courier Rating Distribution
---------------------------------------------------------

SELECT

rating,

COUNT(*) total

FROM courier_staff

GROUP BY rating

ORDER BY rating DESC;

---------------------------------------------------------
-- 18. Vehicle Type Distribution
---------------------------------------------------------

SELECT

vehicle_type,

COUNT(*) total

FROM courier_staff

GROUP BY vehicle_type;

---------------------------------------------------------
-- 19. Top Rated Couriers
---------------------------------------------------------

SELECT *

FROM courier_staff

ORDER BY rating DESC

LIMIT 10;

---------------------------------------------------------
-- 20. Total Fuel Cost
---------------------------------------------------------

SELECT

SUM(fuel_cost)

AS total_fuel_cost

FROM costs;

---------------------------------------------------------
-- 21. Total Labor Cost
---------------------------------------------------------

SELECT

SUM(labor_cost)

AS total_labor_cost

FROM costs;

---------------------------------------------------------
-- 22. Total Miscellaneous Cost
---------------------------------------------------------

SELECT

SUM(misc_cost)

AS total_misc_cost

FROM costs;

---------------------------------------------------------
-- 23. Total Operational Cost
---------------------------------------------------------

SELECT

SUM(

fuel_cost+

labor_cost+

misc_cost

)

AS total_operational_cost

FROM costs;

---------------------------------------------------------
-- 24. Average Cost Per Shipment
---------------------------------------------------------

SELECT

ROUND(

AVG(

fuel_cost+

labor_cost+

misc_cost

),

2

)

AS avg_cost_per_shipment

FROM costs;

---------------------------------------------------------
-- 25. Top Costly Shipments
---------------------------------------------------------

SELECT

shipment_id,

fuel_cost,

labor_cost,

misc_cost,

(

fuel_cost+

labor_cost+

misc_cost

)

AS total_cost

FROM costs

ORDER BY total_cost DESC

LIMIT 10;

---------------------------------------------------------
-- 26. Longest Routes
---------------------------------------------------------

SELECT *

FROM routes

ORDER BY distance_km DESC

LIMIT 10;

---------------------------------------------------------
-- 27. Average Route Distance
---------------------------------------------------------

SELECT

ROUND(

AVG(distance_km),

2

)

AS avg_distance

FROM routes;

---------------------------------------------------------
-- 28. Average Route Time
---------------------------------------------------------

SELECT

ROUND(

AVG(avg_time_hours),

2

)

AS avg_travel_time

FROM routes;

---------------------------------------------------------
-- 29. Warehouse Capacity
---------------------------------------------------------

SELECT

city,

capacity

FROM warehouses

ORDER BY capacity DESC;

---------------------------------------------------------
-- 30. Warehouse Count by State
---------------------------------------------------------

SELECT

state,

COUNT(*) warehouses

FROM warehouses

GROUP BY state

ORDER BY warehouses DESC;

---------------------------------------------------------
-- 31. Shipment Tracking Events
---------------------------------------------------------

SELECT

status,

COUNT(*) events

FROM shipment_tracking

GROUP BY status;

---------------------------------------------------------
-- 32. Latest Shipment Status
---------------------------------------------------------

SELECT

shipment_id,

MAX(timestamp)

AS latest_update

FROM shipment_tracking

GROUP BY shipment_id;

---------------------------------------------------------
-- 33. Shipment Cost Summary
---------------------------------------------------------

SELECT

s.shipment_id,

s.origin,

s.destination,

c.fuel_cost,

c.labor_cost,

c.misc_cost,

(

c.fuel_cost+

c.labor_cost+

c.misc_cost

)

AS total_cost

FROM shipments s

JOIN costs c

ON s.shipment_id=c.shipment_id;

---------------------------------------------------------
-- 34. Courier Performance Summary
---------------------------------------------------------

SELECT

c.name,

c.rating,

COUNT(s.shipment_id)

AS shipments_handled

FROM courier_staff c

LEFT JOIN shipments s

ON c.courier_id=s.courier_id

GROUP BY

c.courier_id,

c.name,

c.rating

ORDER BY shipments_handled DESC;

---------------------------------------------------------
-- 35. Route Usage
---------------------------------------------------------

SELECT

origin,

destination,

COUNT(*) usage_count

FROM shipments

GROUP BY

origin,

destination

ORDER BY usage_count DESC;