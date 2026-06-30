TABLE_CONFIG = {

    # =====================================================
    # Courier Staff
    # =====================================================

    "courier_staff": {

        "file": "data/courier.csv",

        "primary_key": "courier_id",

        "required_columns": [
            "courier_id",
            "courier_name",
            "phone_number"
        ],

        "duplicate_columns": [
            "courier_id"
        ],

        "foreign_keys": {},

        "data_types": {
            "courier_id": int,
            "courier_name": str,
            "phone_number": str,
            "salary": float
        },

        "business_rules": {
            "salary": {
                "min": 0
            }
        },

        "validators": [
            "null",
            "datatype",
            "duplicate",
            "business"
        ]
    },

    # =====================================================
    # Warehouse
    # =====================================================

    "warehouse": {

        "file": "data/warehouse.csv",

        "primary_key": "warehouse_id",

        "required_columns": [
            "warehouse_id",
            "warehouse_name",
            "city"
        ],

        "duplicate_columns": [
            "warehouse_id"
        ],

        "foreign_keys": {},

        "data_types": {
            "warehouse_id": int,
            "warehouse_name": str,
            "city": str,
            "capacity": int
        },

        "business_rules": {
            "capacity": {
                "min": 1
            }
        },

        "validators": [
            "null",
            "datatype",
            "duplicate",
            "business"
        ]
    },

    # =====================================================
    # Shipment
    # =====================================================

    "shipment": {

        "file": "data/shipment.csv",

        "primary_key": "shipment_id",

        "required_columns": [

            "shipment_id",

            "shipment_number",

            "warehouse_id",

            "courier_id",

            "shipment_date",

            "quantity",

            "shipping_cost"
        ],

        "duplicate_columns": [

            "shipment_number"
        ],

        "foreign_keys": {

            "warehouse_id": {

                "table": "warehouse",

                "column": "warehouse_id"

            },

            "courier_id": {

                "table": "courier_staff",

                "column": "courier_id"

            }

        },

        "data_types": {

            "shipment_id": int,

            "shipment_number": str,

            "warehouse_id": int,

            "courier_id": int,

            "shipment_date": "datetime",

            "delivery_date": "datetime",

            "quantity": int,

            "shipping_cost": float,

            "status": str
        },

        "business_rules": {

            "quantity": {

                "min": 1

            },

            "shipping_cost": {

                "min": 0

            },

            "shipment_date": {

                "future_allowed": False

            },

            "delivery_date": {

                "after": "shipment_date"

            }
        },

        "validators": [

            "null",

            "datatype",

            "duplicate",

            "foreign_key",

            "business"

        ]
    },

    # =====================================================
    # Shipment Cost
    # =====================================================

    "shipment_cost": {

        "file": "data/shipment_cost.csv",

        "primary_key": "cost_id",

        "required_columns": [

            "cost_id",

            "shipment_id",

            "amount"

        ],

        "duplicate_columns": [

            "cost_id"

        ],

        "foreign_keys": {

            "shipment_id": {

                "table": "shipment",

                "column": "shipment_id"

            }

        },

        "data_types": {

            "cost_id": int,

            "shipment_id": int,

            "amount": float

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

            "foreign_key",

            "business"

        ]
    }
}