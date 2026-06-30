TABLE_CONFIG = {

    # =====================================================
    # Courier Staff
    # =====================================================

    "routes": {

        "file": "data/routes.csv",

        "primary_key": "route_id",

        "required_columns": [
            "route_id",
            "origin",
            "destination",
            "distance_km",
            "avg_time_hours"
        ],

        "duplicate_columns": [
            "route_id"
        ],

        "foreign_keys": {},

        "data_types": {
            "route_id":str,
            "origin":str,
            "destination":str,
            "distance_km":float,
            "avg_time_hours":float
        },

        "business_rules": {
            "salary": {
                "min": 0
            }
        },

        "validators": [
            "null",
            "datatype",
            "duplicate"
        ]
    },
    "courier_staff": {

       "file": "data/courier_staff.csv",

        "primary_key": "courier_id",

        "required_columns": [
            "courier_id",
            "name",
            "rating",
            "vehicle_type"
        ],

        "duplicate_columns": [
            "courier_id"
        ],

        "foreign_keys": {},

        "data_types": {
            "courier_id": str,
            "name": str,
            "vehicle_type": str,
            "rating": float
        },

        "business_rules": {
        },

        "validators": [
            "null",
            "datatype",
            "duplicate"
        ]
    },

    # =====================================================
    # Warehouse
    # =====================================================

    "warehouses": {

        "file": "data/warehouses.json",

        "primary_key": "warehouse_id",

        "required_columns": [
            "warehouse_id",
            "state",
            "city",
            "capacity"
        ],

        "duplicate_columns": [
            "warehouse_id"
        ],

        "foreign_keys": {},

        "data_types": {
            "warehouse_id": str,
            "state": str,
            "city": str,
            "capacity": int
        },

        "business_rules": {
            """"capacity": {
                "min": 1
            } """
        },

        "validators": [
            "null",
            "datatype",
            "duplicate"
        ]
    },

    # =====================================================
    # Shipment
    # =====================================================

    "shipment": {

        "file": "data/shipments.json",

        "primary_key": "shipment_id",

        "required_columns": [

            "shipment_id",

            "origin",

            "destination",

            "weight",

            "courier_id",

            "status"
        ],

        "duplicate_columns": [

            "shipment_id"
        ],

        "foreign_keys": {

                     "courier_id": {

                "table": "courier_staff",

                "column": "courier_id"

            }

        },

        "data_types": {

            "shipment_id": str,

            "status": str,

            "weight": float,

            "courier_id": str,

            "delivery_date": "datetime",

            "order_date": "datetime",

            "origin": str,

            "destination": str
        },

        "business_rules": {

         """   "shipment_date": {

                "future_allowed": False

            },

            "delivery_date": {

                "after": "shipment_date"

            }"""
        },

        "validators": [

            "null",

            "datatype",

            "duplicate",

            "foreign_key"

        ]
    },

    # =====================================================
    # Shipment Cost
    # =====================================================

    "costs": {

        "file": "data/costs.csv",

        "required_columns": [

            "fuel_cost",

            "shipment_id",

            "misc_cost",

            "labor_cost"

        ],

        "duplicate_columns": [

            "shipment_id"

        ],

        "foreign_keys": {

            "shipment_id": {

                "table": "shipment",

                "column": "shipment_id"

            }

        },

        "data_types": {

            "shipment_id": str,

            "labor_cost": float,

            "misc_cost": float,

            "fuel_cost": float

        },

        "business_rules": {

           },

        "validators": [

            "null",

            "datatype",

            "duplicate",

            "foreign_key"

        ]
    },
    # =====================================================
    # Shipment Cost
    # =====================================================

    "shipment_tracking": {

        "file": "data/shipment_tracking.csv",

        "primary_key": "cost_id",

        "required_columns": [

            "tracking_id",
            "shipment_id",
            "status",
            "timestamp"

        ],

        "duplicate_columns": [

            "tracking_id"

        ],

        "foreign_keys": {

            "shipment_id": {

                "table": "shipment",

                "column": "shipment_id"

            }

        },

        "data_types": {

            "tracking_id": int,

            "shipment_id": str,

            "status": str,

            "timestamp": "datetime",

        },

        "business_rules": {

            "amount": {

                "min": 0

            }

        },

        "validators": [

            "null",

            "datatype",

            "duplicate",

            "foreign_key"

        ]
    }
}